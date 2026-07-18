import json
from datetime import timedelta
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection, transaction

from apps.cinema import (
    models as cinema_models,
)
from apps.core.management import constants as core_management_constants
from apps.movie import models as movie_models
from apps.seat_booking.models import SeatBooking
from apps.user.models import User


class Command(BaseCommand):
    help = "Dump project fixtures into the database."

    def handle(self, *args, **options):
        self.stdout.write("Starting fixture dump...\n")
        try:
            self.dump_fixtures()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Fixture dump failed: {e}"))
            raise
        self.stdout.write(
            self.style.SUCCESS("\n🎉 All fixtures were dumped successfully.")
        )

    @transaction.atomic
    def dump_fixtures(self):
        """Dump all project fixtures."""

        # Dump Locations
        self.stdout.write("Dumping locations...")
        self.dump_locations()
        self.stdout.write(self.style.SUCCESS("✓ Locations dumped successfully."))

        # Dump languages
        self.stdout.write("Dumping Languages...")
        self.dump_languages()
        self.stdout.write(self.style.SUCCESS("✓ languages dumped successfully."))

        # Dump genres
        self.stdout.write("Dumping Genres...")
        self.dump_genres()
        self.stdout.write(self.style.SUCCESS("✓ genres dumped successfully."))

        # dump cinemas
        self.stdout.write("Dumping Cinemas...")
        self.dump_cinemas()
        self.stdout.write(self.style.SUCCESS("✓ cinemas dumped successfully."))

        # dump movies
        self.stdout.write("Dumping Movies...")
        self.dump_movies()
        self.stdout.write(self.style.SUCCESS("✓ movies dumped successfully."))

        # dump slots
        self.stdout.write("Dumping Slots...")
        self.dump_slots()
        self.stdout.write(self.style.SUCCESS("✓ slots dumped successfully."))

        # dump users
        self.stdout.write("Dumping users...")
        self.dump_users()
        self.stdout.write(self.style.SUCCESS("✓ users dumped successfully."))

        # dump seatbookings
        self.stdout.write("Dumping seatbookings...")
        self.dump_seat_bookings()
        self.stdout.write(self.style.SUCCESS("✓ seatbookings dumped successfully."))

        # reset sequence
        self.stdout.write("Sequence resetting...")
        sequence_sql = connection.ops.sequence_reset_sql(
            no_style(),
            [
                cinema_models.Cinema,
                cinema_models.Location,
                cinema_models.Slot,
                movie_models.Language,
                movie_models.Genre,
                movie_models.Movie,
                SeatBooking,
                User,
            ],
        )
        self.stdout.write(self.style.SUCCESS("✓ Sequence resetted successfully."))

        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

    def dump_locations(self):
        """Dump locations from JSON into the database."""
        locations = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.LOCATIONS_FILE_PATH
        )
        locations_to_create = [
            cinema_models.Location(**location) for location in locations
        ]
        cinema_models.Location.objects.bulk_create(locations_to_create)

    def json_to_dict(self, filepath):
        file_path = Path(filepath)
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def dump_languages(self):
        languages = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.LANGUAGES_FILE_PATH
        )
        languages_to_create = [
            movie_models.Language(**language) for language in languages
        ]
        movie_models.Language.objects.bulk_create(languages_to_create)

    def dump_genres(self):
        genres = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.GENRES_FILE_PATH
        )
        genres_to_create = [movie_models.Genre(**genre) for genre in genres]
        movie_models.Genre.objects.bulk_create(genres_to_create)

    def dump_cinemas(self):
        cinemas = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.CINEMAS_FILE_PATH
        )
        location_ids = {cinema["location_id"] for cinema in cinemas}
        location_map = {
            loc.id: loc
            for loc in cinema_models.Location.objects.filter(id__in=location_ids)
        }
        cinemas_to_create = []
        for cinema in cinemas:
            loc_id = cinema.pop("location_id")
            location_obj = location_map.get(loc_id)
            if location_obj:
                cinemas_to_create.append(
                    cinema_models.Cinema(**cinema, location=location_obj)
                )
            else:
                raise Exception(f"Location {loc_id} Not Found")
        cinema_models.Cinema.objects.bulk_create(cinemas_to_create)

    def dump_movies(self):
        movies = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.MOVIES_FILE_PATH
        )
        language_ids = {
            lang_id for movie in movies for lang_id in movie["language_ids"]
        }
        language_map = {
            lang.id: lang
            for lang in movie_models.Language.objects.filter(id__in=language_ids)
        }
        genre_ids = {genre_id for movie in movies for genre_id in movie["genre_ids"]}
        genre_map = {
            genre.id: genre
            for genre in movie_models.Genre.objects.filter(id__in=genre_ids)
        }
        movies_to_create = []
        movie_relations = []
        for movie in movies:
            language_objs = []
            for lang_id in movie["language_ids"]:
                lang_obj = language_map.get(lang_id)
                if lang_obj:
                    language_objs.append(lang_obj)
                else:
                    raise Exception(f"Language {lang_id} Not Found")
            genre_objs = []
            for genre_id in movie["genre_ids"]:
                genre_obj = genre_map.get(genre_id)
                if genre_obj:
                    genre_objs.append(genre_obj)
                else:
                    raise Exception(f"Genre {genre_id} Not Found")
            movie.pop("language_ids")
            movie.pop("genre_ids")
            duration = movie.pop("duration")
            movies_to_create.append(
                movie_models.Movie(**movie, duration=self.parse_duration(duration))
            )
            movie_relations.append(
                {
                    "languages": language_objs,
                    "genres": genre_objs,
                }
            )
        movie_models.Movie.objects.bulk_create(movies_to_create)
        for movie, relation in zip(movies_to_create, movie_relations):
            movie.languages.set(relation["languages"])
            movie.genres.set(relation["genres"])

    def parse_duration(self, duration):
        h, m, s = map(int, duration.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def dump_slots(self):
        slots = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.SLOTS_FILE_PATH
        )
        cinema_ids = [slot["cinema_id"] for slot in slots]
        cinema_map = {
            cinema.id: cinema
            for cinema in cinema_models.Cinema.objects.filter(id__in=cinema_ids)
        }
        movie_ids = [slot["movie_id"] for slot in slots]
        movie_map = {
            movie.id: movie
            for movie in movie_models.Movie.objects.filter(id__in=movie_ids)
        }
        language_ids = [slot["language_id"] for slot in slots]
        language_map = {
            lang.id: lang
            for lang in movie_models.Language.objects.filter(id__in=language_ids)
        }
        slot_to_create = []
        for slot in slots:
            cinema_id = slot["cinema_id"]
            movie_id = slot["movie_id"]
            language_id = slot["language_id"]
            cinema_obj = cinema_map.get(cinema_id)
            movie_obj = movie_map.get(movie_id)
            lang_obj = language_map.get(language_id)
            if not cinema_obj:
                raise Exception(f"cinema {cinema_id} Not Found")
            if not movie_obj:
                raise Exception(f"movie {movie_id} not found")
            if not lang_obj:
                raise Exception(f"language {language_id} not found")
            slot.pop("cinema_id")
            slot.pop("movie_id")
            slot.pop("language_id")
            slot_to_create.append(
                cinema_models.Slot(
                    **slot, cinema=cinema_obj, movie=movie_obj, language=lang_obj
                )
            )
        cinema_models.Slot.objects.bulk_create(slot_to_create)

    def dump_users(self):
        users = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.USERS_FILE_PATH
        )

        users_to_create = []
        for user in users:
            new_user = User(**user)
            new_user.set_password(user["password"])
            users_to_create.append(new_user)
            print(user["id"])

        with transaction.atomic():
            User.objects.bulk_create(users_to_create, batch_size=1000)

    def dump_seat_bookings(self):
        seat_bookings = self.json_to_dict(
            core_management_constants.COMMANDS_CONSTANTS.SEAT_BOOKINGS_FILE_PATH
        )

        slot_ids = [seat_booking["slot"] for seat_booking in seat_bookings]
        slot_map = {
            slot.id: slot for slot in cinema_models.Slot.objects.filter(id__in=slot_ids)
        }

        user_ids = [seat_booking["user"] for seat_booking in seat_bookings]
        user_map = {user.id: user for user in User.objects.filter(id__in=user_ids)}

        seat_bookings_to_create = []

        for seat_booking in seat_bookings:
            slot_id = seat_booking["slot"]
            slot_obj = slot_map.get(slot_id)
            if not slot_obj:
                raise Exception(f"slot {slot_id} Not Found")

            user_id = seat_booking["user"]
            user_obj = user_map.get(user_id)
            if not user_obj:
                raise Exception(f"user {user_id} not found")

            seat_booking.pop("slot")
            seat_booking.pop("user")

            seat_bookings_to_create.append(
                SeatBooking(**seat_booking, slot=slot_obj, user=user_obj)
            )
            print(seat_booking["id"])

        SeatBooking.objects.bulk_create(seat_bookings_to_create)
