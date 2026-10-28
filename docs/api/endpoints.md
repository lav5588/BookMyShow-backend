# BookMyShow Backend - API Endpoints Reference

This document provides a comprehensive specification of all REST endpoints available in the BookMyShow backend.

---

## Table of Contents
1. [Authentication & User Management](#1-authentication--user-management)
2. [Movies Catalog](#2-movies-catalog)
3. [Cinemas & Locations](#3-cinemas--locations)
4. [Seat Booking & Tickets](#4-seat-booking--tickets)
5. [Contact Us](#5-contact-us)
6. [OpenAPI & Schema](#6-openapi--schema)

---

## 1. Authentication & User Management

Base route: `/api/users/`

### 1.1 Register User
- **Method & URL**: `POST /api/users/register/`
- **Auth**: Public
- **Description**: Registers a new user account, returns user details with an access token, and sets the refresh token in an HttpOnly cookie.

#### Request Body
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "password": "SecurePassword123!",
  "confirm_password": "SecurePassword123!",
  "phone_number": "9876543210"
}
```

#### Success Response (`200 OK`)
```json
{
  "id": 15,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "phone_number": "9876543210",
  "profile_pic": null,
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
*Sets cookie: `refresh=<refresh_token>; HttpOnly; SameSite=Lax; Max-Age=86400`*

---

### 1.2 Login User
- **Method & URL**: `POST /api/users/login/`
- **Auth**: Public
- **Description**: Authenticates user via email and password, returning an access token and setting the refresh cookie.

#### Request Body
```json
{
  "email": "jane.doe@example.com",
  "password": "SecurePassword123!"
}
```

#### Success Response (`200 OK`)
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
*Sets cookie: `refresh=<refresh_token>; HttpOnly; SameSite=Lax; Max-Age=86400`*

#### Error Response (`400 Bad Request`)
```json
{
  "error": "Failed to Login"
}
```

---

### 1.3 Refresh Token
- **Method & URL**: `POST /api/users/refresh/`
- **Auth**: Public (Cookie Required)
- **Description**: Refreshes the JWT access token using the HttpOnly `refresh` cookie. Rotates and blacklists the previous refresh token.

#### Headers / Cookie
```http
Cookie: refresh=<refresh_token>
```

#### Success Response (`200 OK`)
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
*Rotates and sets new `refresh` cookie.*

---

### 1.4 Logout
- **Method & URL**: `POST /api/users/logout/`
- **Auth**: Public (Cookie Required)
- **Description**: Blacklists the current refresh token and deletes the `refresh` cookie.

#### Headers / Cookie
```http
Cookie: refresh=<refresh_token>
```

#### Success Response (`200 OK`)
```json
{
  "message": "You have logged out successfully"
}
```

---

### 1.5 Get User Profile
- **Method & URL**: `GET /api/users/profile/`
- **Auth**: `Bearer <access_token>`
- **Description**: Returns profile details for the authenticated user.

#### Success Response (`200 OK`)
```json
{
  "id": 15,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "phone_number": "9876543210",
  "profile_pic": "/public/users/jane.jpg"
}
```

---

### 1.6 Update User Profile
- **Method & URL**: `PATCH /api/users/update-profile/`
- **Auth**: `Bearer <access_token>`
- **Description**: Updates profile attributes (`name`, `phone_number`, `profile_pic`). Supports `multipart/form-data`.

#### Request Body (JSON or Form-Data)
```json
{
  "name": "Jane Smith",
  "phone_number": "9123456780"
}
```

#### Success Response (`200 OK`)
```json
{
  "id": 15,
  "name": "Jane Smith",
  "email": "jane.doe@example.com",
  "phone_number": "9123456780",
  "profile_pic": "/public/users/jane.jpg"
}
```

---

### 1.7 Change Password
- **Method & URL**: `PATCH /api/users/change-password/`
- **Auth**: `Bearer <access_token>`
- **Description**: Updates user password after verifying the old password.

#### Request Body
```json
{
  "old_password": "SecurePassword123!",
  "new_password": "NewUltraSecurePassword456!",
  "confirm_password": "NewUltraSecurePassword456!"
}
```

#### Success Response (`200 OK`)
```json
{
  "success": "password changed successfully"
}
```

---

## 2. Movies Catalog

Base route: `/api/movies/`

### 2.1 List Movies
- **Method & URL**: `GET /api/movies/`
- **Auth**: Public
- **Description**: Returns a paginated list of movies. Filterable by cinema, language, genre, and scheduled slot date.
- **Query Parameters**:
  - `page` (`integer`, optional): Page number (default: 1)
  - `cinema` (`integer`, optional): Filter by cinema ID
  - `language` (`string`, optional): Filter by language name (e.g. `english`)
  - `genre` (`string`, optional): Filter by genre name (e.g. `action`)
  - `slot_date` (`string`, optional): Filter by active slot date (`YYYY-MM-DD`)

#### Success Response (`200 OK`)
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/movies/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Oppenheimer",
      "slug": "oppenheimer",
      "languages": ["english", "hindi"],
      "genres": ["biography", "drama", "history"],
      "description": "The story of American scientist J. Robert Oppenheimer...",
      "duration": "03:00:00",
      "release_date": "2023-07-21",
      "movie_poster": "/public/movies/oppenheimer.jpg"
    }
  ]
}
```

---

### 2.2 List Latest Movies
- **Method & URL**: `GET /api/movies/latest/`
- **Auth**: Public
- **Description**: Returns currently released movies with active showtimes or recent release dates.

#### Success Response (`200 OK`)
```json
[
  {
    "id": 1,
    "name": "Oppenheimer",
    "slug": "oppenheimer",
    "languages": ["english", "hindi"],
    "genres": ["biography", "drama"],
    "description": "...",
    "duration": "03:00:00",
    "release_date": "2023-07-21",
    "movie_poster": "/public/movies/oppenheimer.jpg"
  }
]
```

---

### 2.3 List Upcoming Movies
- **Method & URL**: `GET /api/movies/upcoming/`
- **Auth**: Public
- **Description**: Returns movies scheduled for release in the future (`release_date > today`).

#### Success Response (`200 OK`)
```json
[
  {
    "id": 12,
    "name": "Avatar 3",
    "slug": "avatar-3",
    "languages": ["english"],
    "genres": ["action", "sci-fi"],
    "description": "Continuing the journey of Jake Sully...",
    "duration": "03:15:00",
    "release_date": "2026-12-19",
    "movie_poster": "/public/movies/avatar3.jpg"
  }
]
```

---

### 2.4 Retrieve Movie Details
- **Method & URL**: `GET /api/movies/{slug}/`
- **Auth**: Public
- **Description**: Retrieves single movie details by its URL slug.

#### Success Response (`200 OK`)
```json
{
  "id": 1,
  "name": "Oppenheimer",
  "slug": "oppenheimer",
  "languages": ["english", "hindi"],
  "genres": ["biography", "drama"],
  "description": "The story of American scientist J. Robert Oppenheimer...",
  "duration": "03:00:00",
  "release_date": "2023-07-21",
  "movie_poster": "/public/movies/oppenheimer.jpg"
}
```

---

### 2.5 Movie Showtimes by Movie Slug
- **Method & URL**: `GET /api/movies/{slug}/movie-slots/?date=YYYY-MM-DD`
- **Auth**: Public
- **Description**: Returns cinemas and their corresponding scheduled slots showing this movie on the given date.
- **Query Parameters**:
  - `date` (`string`, required): Showtime date (`YYYY-MM-DD`)

#### Success Response (`200 OK`)
```json
[
  {
    "id": 1,
    "name": "PVR Icon",
    "location": {
      "id": 1,
      "location": "mumbai"
    },
    "rows": 10,
    "seats_per_row": 12,
    "slots": [
      {
        "id": 101,
        "date_time": "2026-11-01T14:30:00+05:30",
        "price": "350.00",
        "language": "english"
      },
      {
        "id": 102,
        "date_time": "2026-11-01T18:00:00+05:30",
        "price": "400.00",
        "language": "hindi"
      }
    ]
  }
]
```

---

### 2.6 Available Show Dates for Movie
- **Method & URL**: `GET /api/movies/{slug}/available-slots-dates/`
- **Auth**: Public
- **Description**: Returns a sorted list of unique dates (`YYYY-MM-DD`) with future showtimes available for this movie.

#### Success Response (`200 OK`)
```json
[
  "2026-11-01",
  "2026-11-02",
  "2026-11-03"
]
```

---

### 2.7 Movie Languages
- **Method & URL**: `GET /api/movies/{movie_id}/languages/`
- **Auth**: Public
- **Description**: Returns all languages in which the specified movie is available.

#### Success Response (`200 OK`)
```json
[
  { "id": 1, "language": "english" },
  { "id": 2, "language": "hindi" }
]
```

---

### 2.8 Genres List
- **Method & URL**: `GET /api/movies/genres/`
- **Auth**: Public
- **Description**: Lists all movie genres in alphabetical order.

#### Success Response (`200 OK`)
```json
[
  { "id": 1, "genre": "action" },
  { "id": 2, "genre": "adventure" },
  { "id": 3, "genre": "drama" }
]
```

---

### 2.9 Languages List
- **Method & URL**: `GET /api/movies/languages/`
- **Auth**: Public
- **Description**: Lists all supported movie languages.

#### Success Response (`200 OK`)
```json
[
  { "id": 1, "language": "english" },
  { "id": 2, "language": "hindi" },
  { "id": 3, "language": "telugu" }
]
```

---

## 3. Cinemas & Locations

Base route: `/api/cinemas/`

### 3.1 List Cinemas
- **Method & URL**: `GET /api/cinemas/`
- **Auth**: Public
- **Description**: Returns cinemas having upcoming active showtimes. Supports location filtering.
- **Query Parameters**:
  - `location` (`string`, optional): Case-insensitive location filter (e.g. `mumbai`, `delhi`)

#### Success Response (`200 OK`)
```json
[
  {
    "id": 1,
    "name": "PVR Icon",
    "location": {
      "id": 1,
      "location": "mumbai"
    },
    "rows": 10,
    "seats_per_row": 12
  }
]
```

---

### 3.2 Retrieve Cinema Details
- **Method & URL**: `GET /api/cinemas/{id}/`
- **Auth**: Public
- **Description**: Returns cinema venue layout dimensions and location.

#### Success Response (`200 OK`)
```json
{
  "id": 1,
  "name": "PVR Icon",
  "location": {
    "id": 1,
    "location": "mumbai"
  },
  "rows": 10,
  "seats_per_row": 12
}
```

---

### 3.3 Movies & Slots by Cinema
- **Method & URL**: `GET /api/cinemas/{id}/movie-slots/?date=YYYY-MM-DD`
- **Auth**: Public
- **Description**: Returns all movies and showtimes scheduled at the specified cinema for a given date.
- **Query Parameters**:
  - `date` (`string`, required): Show date (`YYYY-MM-DD`)

#### Success Response (`200 OK`)
```json
[
  {
    "id": 1,
    "name": "Oppenheimer",
    "slug": "oppenheimer",
    "duration": "03:00:00",
    "languages": ["english", "hindi"],
    "genres": ["drama", "history"],
    "slots": [
      {
        "id": 101,
        "date_time": "2026-11-01T14:30:00+05:30",
        "price": "350.00",
        "language": "english"
      }
    ]
  }
]
```

---

### 3.4 Available Show Dates for Cinema
- **Method & URL**: `GET /api/cinemas/{id}/available-slots-dates/`
- **Auth**: Public
- **Description**: Returns all upcoming calendar dates that have active showtimes at this cinema.

#### Success Response (`200 OK`)
```json
[
  "2026-11-01",
  "2026-11-02",
  "2026-11-03"
]
```

---

### 3.5 List Cinema Locations
- **Method & URL**: `GET /api/cinemas/locations/`
- **Auth**: Public
- **Description**: Lists all distinct locations/cities hosting cinemas.

#### Success Response (`200 OK`)
```json
[
  { "id": 1, "location": "mumbai" },
  { "id": 2, "location": "delhi" },
  { "id": 3, "location": "bengaluru" }
]
```

---

## 4. Seat Booking & Tickets

Base route: `/api/bookings/`

### 4.1 Get Slot Details & Booked Seat Grid
- **Method & URL**: `GET /api/bookings/slot-details/{slot_id}/`
- **Auth**: Public
- **Description**: Returns the showtime metadata, cinema dimensions (rows, seats_per_row), and currently occupied seat coordinates for real-time seat map rendering.

#### Success Response (`200 OK`)
```json
{
  "slot": {
    "id": 101,
    "date_time": "2026-11-01T14:30:00+05:30",
    "price": "350.00",
    "language": "english"
  },
  "cinema": {
    "id": 1,
    "name": "PVR Icon",
    "location": {
      "id": 1,
      "location": "mumbai"
    },
    "rows": 10,
    "seats_per_row": 12
  },
  "movie": {
    "id": 1,
    "name": "Oppenheimer",
    "slug": "oppenheimer",
    "duration": "03:00:00",
    "release_date": "2023-07-21"
  },
  "booked_seats": [
    { "row_number": 1, "seat_number": 5 },
    { "row_number": 1, "seat_number": 6 },
    { "row_number": 3, "seat_number": 8 }
  ]
}
```

---

### 4.2 Book Multiple Seats
- **Method & URL**: `POST /api/bookings/`
- **Auth**: `Bearer <access_token>`
- **Description**: Atomically reserves one or more seats in a single showtime slot. Validates coordinates against cinema boundaries and prevents double-booking using database constraints and atomic transactions.

#### Request Body
```json
{
  "slot_id": 101,
  "seats": [
    { "row_number": 4, "seat_number": 7 },
    { "row_number": 4, "seat_number": 8 }
  ]
}
```

#### Success Response (`201 Created`)
```json
{
  "message": "2 seat(s) booked successfully"
}
```

#### Error: Seat Already Reserved (`409 Conflict`)
```json
{
  "message": "Some seats are already booked"
}
```

#### Error: Invalid Seat Coordinates (`400 Bad Request`)
```json
{
  "message": "Invalid row_number 15"
}
```

---

### 4.3 User Upcoming Tickets
- **Method & URL**: `GET /api/bookings/tickets/`
- **Auth**: `Bearer <access_token>`
- **Description**: Lists upcoming active tickets (`slot__date_time > now`) booked by the authenticated user.

#### Success Response (`200 OK`)
```json
[
  {
    "id": 55,
    "row_number": 4,
    "seat_number": 7,
    "status": "BOOKED",
    "created_at": "2026-10-28T10:00:00+05:30",
    "slot": {
      "id": 101,
      "date_time": "2026-11-01T14:30:00+05:30",
      "price": "350.00",
      "movie": {
        "id": 1,
        "name": "Oppenheimer",
        "slug": "oppenheimer",
        "movie_poster": "/public/movies/oppenheimer.jpg"
      },
      "cinema": {
        "id": 1,
        "name": "PVR Icon",
        "location": { "location": "mumbai" }
      },
      "language": "english"
    }
  }
]
```

---

### 4.4 User Past Booking History
- **Method & URL**: `GET /api/bookings/history/`
- **Auth**: `Bearer <access_token>`
- **Description**: Lists historical/past tickets (`slot__date_time < now`) booked by the authenticated user.

#### Success Response (`200 OK`)
```json
[
  {
    "id": 32,
    "row_number": 2,
    "seat_number": 4,
    "status": "BOOKED",
    "created_at": "2026-08-15T12:00:00+05:30",
    "slot": {
      "id": 40,
      "date_time": "2026-08-16T19:00:00+05:30",
      "price": "300.00",
      "movie": {
        "name": "Interstellar",
        "slug": "interstellar"
      },
      "cinema": {
        "name": "Inox Megaplex",
        "location": { "location": "mumbai" }
      },
      "language": "english"
    }
  }
]
```

---

### 4.5 Cancel Booking
- **Method & URL**: `PATCH /api/bookings/cancel/{id}/`
- **Auth**: `Bearer <access_token>`
- **Description**: Cancels an existing seat booking. Only valid if the booking belongs to the authenticated user and the showtime is in the future.

#### Request Body
```json
{}
```

#### Success Response (`200 OK`)
```json
{
  "id": 55,
  "message": "seat cancelled successfully"
}
```

---

## 5. Contact Us

Base route: `/api/contact-us/`

### 5.1 Submit Query / Feedback
- **Method & URL**: `POST /api/contact-us/`
- **Auth**: Public
- **Description**: Saves a user contact inquiry or feedback.

#### Request Body
```json
{
  "email": "customer@example.com",
  "query": "I had a question regarding refund policies for cancelled shows."
}
```

#### Success Response (`201 Created`)
```json
{
  "id": 1,
  "email": "customer@example.com",
  "query": "I had a question regarding refund policies for cancelled shows.",
  "created_at": "2026-10-28T15:30:00+05:30"
}
```

---

## 6. OpenAPI & Schema

### 6.1 Download OpenAPI YAML Schema
- **Method & URL**: `GET /api/schema/`
- **Auth**: Public
- **Description**: Downloads the dynamic OpenAPI 3.0 YAML schema document.

### 6.2 Interactive Swagger UI
- **Method & URL**: `GET /api/schema/swagger-ui/`
- **Auth**: Public
- **Description**: Web-based graphical interface for exploring and executing API requests in real time.
