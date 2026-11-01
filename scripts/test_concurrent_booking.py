#!/usr/bin/env python
# ruff: noqa: E402
"""
Concurrency Stress Test for BookMyShow Backend
----------------------------------------------
Tests simultaneous booking of the exact same seat coordinate by 100 distinct users
at the exact same instant to verify that race conditions are prevented and no more
than 1 booking can succeed.
"""

import os
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure UTF-8 output across all platforms
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
import requests

# Setup Django Environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookmyshow.settings")
django.setup()

from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.cinema.models import Cinema, Slot
from apps.movie.models import Movie
from apps.seat_booking.models import BookingStatus, SeatBooking
from apps.user.models import User

API_BASE_URL = "http://127.0.0.1:8000/api"
BOOKINGS_ENDPOINT = f"{API_BASE_URL}/bookings/"


def check_database_state():
    """Ensure database has data before proceeding."""
    print("=" * 70)
    print("Step 1: Inspecting Database State")
    print("=" * 70)

    user_count = User.objects.count()
    cinema_count = Cinema.objects.count()
    movie_count = Movie.objects.count()
    slot_count = Slot.objects.count()
    booking_count = SeatBooking.objects.count()

    print(f"  * Users in Database:    {user_count}")
    print(f"  * Cinemas in Database:  {cinema_count}")
    print(f"  * Movies in Database:   {movie_count}")
    print(f"  * Slots in Database:    {slot_count}")
    print(f"  * Bookings in Database: {booking_count}")

    if user_count < 100 or slot_count == 0:
        print("\n[ERROR] Insufficient fixture data in database.")
        print("Please run: pipenv run python manage.py dump-fixtures")
        sys.exit(1)

    print("\n[OK] Database contains fixture data. No seeding needed.\n")


def find_target_slot_and_seat():
    """Find an active future slot and an unbooked seat coordinate."""
    print("=" * 70)
    print("Step 2: Selecting Target Showtime Slot and Unbooked Seat")
    print("=" * 70)

    future_slots = Slot.objects.filter(date_time__gt=timezone.now()).select_related(
        "cinema", "movie"
    )

    target_slot = None
    target_seat = None

    for slot in future_slots:
        booked_coords = set(
            SeatBooking.objects.filter(
                slot=slot,
                status__in=[BookingStatus.BOOKED, BookingStatus.PENDING],
            ).values_list("row_number", "seat_number")
        )

        for r in range(1, slot.cinema.rows + 1):
            for s in range(1, slot.cinema.seats_per_row + 1):
                if (r, s) not in booked_coords:
                    target_slot = slot
                    target_seat = (r, s)
                    break
            if target_seat:
                break
        if target_slot:
            break

    if not target_slot or not target_seat:
        print("[ERROR] Could not find a future slot with an available seat.")
        sys.exit(1)

    print(f"  * Target Slot ID: {target_slot.id}")
    print(f"  * Movie:          {target_slot.movie.name}")
    print(f"  * Cinema:         {target_slot.cinema.name}")
    print(f"  * Showtime:       {target_slot.date_time}")
    print(f"  * Target Seat:    Row {target_seat[0]}, Seat {target_seat[1]}")
    print("[OK] Target coordinate confirmed 100% unbooked.\n")

    return target_slot, target_seat


def prepare_users_and_tokens(num_users=100):
    """Retrieve users from fixtures and generate JWT access tokens."""
    print("=" * 70)
    print(f"Step 3: Preparing {num_users} Users & JWT Authentication Tokens")
    print("=" * 70)

    users = list(User.objects.filter(is_active=True)[:num_users])
    if len(users) < num_users:
        print(f"[ERROR] Need at least {num_users} active users, found {len(users)}.")
        sys.exit(1)

    user_tokens = []
    for u in users:
        token = str(RefreshToken.for_user(u).access_token)
        user_tokens.append((u, token))

    print(f"[OK] Generated JWT tokens for {len(user_tokens)} distinct users.\n")
    return user_tokens


def run_concurrent_stress_test(target_slot, target_seat, user_tokens):
    """Execute concurrent requests from 100 users attempting to book the exact same seat."""
    num_users = len(user_tokens)
    print("=" * 70)
    print(f"Step 4: Launching {num_users} Concurrent Booking Requests")
    print("=" * 70)
    print(
        f"Firing {num_users} simultaneous POST requests to {BOOKINGS_ENDPOINT} for Seat {target_seat}..."
    )

    barrier = threading.Barrier(num_users)
    results = []

    def attempt_booking(user, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "slot_id": target_slot.id,
            "seats": [
                {
                    "row_number": target_seat[0],
                    "seat_number": target_seat[1],
                }
            ],
        }

        # Synchronize all threads to fire at the exact same instant
        barrier.wait()

        try:
            resp = requests.post(
                BOOKINGS_ENDPOINT, json=payload, headers=headers, timeout=45
            )
            return {
                "user": user.email,
                "status_code": resp.status_code,
                "body": resp.json() if resp.content else {},
            }
        except Exception as e:
            return {
                "user": user.email,
                "status_code": 0,
                "error": str(e),
            }

    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = [
            executor.submit(attempt_booking, user, token) for user, token in user_tokens
        ]
        for future in as_completed(futures):
            results.append(future.result())

    return results


def verify_results(target_slot, target_seat, results):
    """Analyze HTTP responses and query database to confirm zero double-booking."""
    print("\n" + "=" * 70)
    print("Step 5: Stress Test Analysis & Database Verification")
    print("=" * 70)

    status_counts = Counter(r["status_code"] for r in results)

    print("HTTP Response Breakdown:")
    for code, count in sorted(status_counts.items()):
        status_label = (
            "201 Created (Success)"
            if code == 201
            else (
                "409 Conflict (Seat already taken)" if code == 409 else f"Status {code}"
            )
        )
        print(f"  * HTTP {code} [{status_label}]: {count} request(s)")

    # Identify which user secured the seat
    successful_bookings = [r for r in results if r["status_code"] == 201]
    conflict_bookings = [r for r in results if r["status_code"] == 409]

    if successful_bookings:
        winner = successful_bookings[0]["user"]
        print(f"\nWinning User (Secured Booking): {winner}")
    else:
        print("\n[WARNING] No user received HTTP 201.")

    # Database Verification
    db_bookings = SeatBooking.objects.filter(
        slot=target_slot,
        row_number=target_seat[0],
        seat_number=target_seat[1],
        status__in=[BookingStatus.BOOKED, BookingStatus.PENDING],
    )
    db_count = db_bookings.count()

    print(f"\nDatabase Verification for Slot {target_slot.id}, Seat {target_seat}:")
    print(f"  * Active Bookings in DB: {db_count}")
    for b in db_bookings:
        print(
            f"    - ID: {b.id} | User: {b.user.email} | Status: {b.status} | Created: {b.created_at}"
        )

    print("\n" + "=" * 70)
    print("FINAL VERDICT:")
    if db_count == 1 and len(successful_bookings) == 1:
        print("[PASSED] Exactly 1 booking was created in the database!")
        print("         - 1 user received HTTP 201 Created.")
        print(f"         - {len(conflict_bookings)} users received HTTP 409 Conflict.")
        print("         - Zero double-booking occurred across 100 concurrent requests.")
        print(
            "         - Database constraints and atomic transactions successfully prevented race conditions."
        )
        print("=" * 70)
        return True
    else:
        print("[FAILED] Race condition detected!")
        print(f"         Expected exactly 1 booking, but found {db_count} in database.")
        print("=" * 70)
        return False


def main():
    check_database_state()
    target_slot, target_seat = find_target_slot_and_seat()
    user_tokens = prepare_users_and_tokens(num_users=100)
    results = run_concurrent_stress_test(target_slot, target_seat, user_tokens)
    success = verify_results(target_slot, target_seat, results)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
