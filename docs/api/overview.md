# BookMyShow Backend - API Overview

Welcome to the BookMyShow RESTful API documentation. This API powers the BookMyShow movie discovery, cinema scheduling, seat booking, and user management ecosystem.

---

## 1. Base URL & Environments

| Environment | Base URL | Description |
| :--- | :--- | :--- |
| **Local Development** | `http://localhost:8000/api` | Local development server |
| **Production** | `https://api.yourdomain.com/api` | Live production gateway |

Interactive Swagger UI documentation is available at:
- **Swagger UI**: `/api/schema/swagger-ui/`
- **OpenAPI Schema (YAML)**: `/api/schema/`

---

## 2. Authentication & Authorization

The API uses **JSON Web Tokens (JWT)** via `djangorestframework-simplejwt` paired with secure **HttpOnly Cookies** for token storage.

### 2.1 Token Pair Model
- **Access Token**: Short-lived bearer token (default: 15 minutes) passed in the HTTP Authorization header:
  ```http
  Authorization: Bearer <access_token>
  ```
- **Refresh Token**: Long-lived token (default: 1 day) stored automatically in an **HttpOnly, Secure, Lax SameSite** cookie named `refresh`. This protects against Cross-Site Scripting (XSS) attacks.

### 2.2 Token Lifecycle & Rotation
- When logging in or registering, the response returns the `access` token in the JSON body and sets the `refresh` cookie.
- When refreshing `/api/users/refresh/`, token rotation is enforced: the old refresh token is blacklisted (`rest_framework_simplejwt.token_blacklist`) and a brand new refresh token cookie and access token are issued.
- When logging out `/api/users/logout/`, the server blacklists the current refresh token and deletes the cookie.

---

## 3. Request & Response Conventions

### 3.1 Headers
All API requests must supply standard HTTP headers:

```http
Content-Type: application/json
Accept: application/json
```

For endpoints requiring authentication, include:
```http
Authorization: Bearer <your_jwt_access_token>
```

### 3.2 Response Format
Successful API responses return JSON data directly or wrapped in domain objects:

```json
{
  "id": 1,
  "name": "Inception",
  "slug": "inception",
  "duration": "02:28:00",
  "release_date": "2010-07-16"
}
```

### 3.3 Error Format
When an error occurs, responses return descriptive error messages matching standard DRF formats:

#### Validation Error (`400 Bad Request`)
```json
{
  "email": ["Enter a valid email address."],
  "password": ["This password is too short. It must contain at least 8 characters."]
}
```

#### Booking Conflict (`409 Conflict`)
```json
{
  "message": "Some seats are already booked",
  "seats": [[1, 5], [1, 6]]
}
```

#### Unauthorized (`401 Unauthorized`)
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

---

## 4. Pagination

Endpoints returning collections (e.g., `/api/movies/`) utilize Django REST Framework's `PageNumberPagination`:

- **Default Page Size**: `10`
- **Query Parameter**: `?page=<number>`

### Paginated Response Structure
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/movies/?page=3",
  "previous": "http://localhost:8000/api/movies/?page=1",
  "results": [
    { ... }
  ]
}
```

*Note: Certain specific relationship views (such as slots filtered by movie or cinema) intentionally disable pagination to deliver complete real-time showtime matrices.*

---

## 5. Filtering & Query Parameters

The API supports precise filtering for scheduling and catalog discovery:

| Parameter | Type | Example | Applicable Endpoints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `location` | `string` | `?location=mumbai` | `/api/cinemas/` | Filter cinemas by normalized city/location name |
| `date` | `string (YYYY-MM-DD)` | `?date=2026-11-01` | `.../movie-slots/` | Filter showtimes for a specific calendar date |
| `cinema` | `integer` | `?cinema=2` | `/api/movies/` | Filter movies running at a specific cinema venue |
| `language` | `string` | `?language=english` | `/api/movies/` | Filter movies by audio language |
| `genre` | `string` | `?genre=sci-fi` | `/api/movies/` | Filter movies by genre |
| `slot_date`| `string (YYYY-MM-DD)` | `?slot_date=2026-11-01` | `/api/movies/` | Filter movies having slots on a specific date |

---

## 6. Next Steps

- Explore the full endpoint reference: [`docs/api/endpoints.md`](endpoints.md)
- Learn how to run the project locally: [`docs/guides/getting_started.md`](../guides/getting_started.md)
- Understand the architecture: [`docs/architecture/system_overview.md`](../architecture/system_overview.md)
