# Getting Started Guide - BookMyShow Backend

Welcome to the **BookMyShow Backend** setup guide. This guide will walk you through setting up, configuring, seeding, and running the backend API server on your local development machine.

---

## 1. Prerequisites

Before getting started, make sure the following dependencies are installed on your workstation:

| Tool | Recommended Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.14` (or 3.12+) | Primary runtime environment |
| **Pipenv** | Latest | Python virtual environment & dependency manager |
| **Docker & Docker Compose** | Latest | Runs the PostgreSQL 18 database container |
| **Git** | Latest | Source control management |

Verify installations:
```bash
python --version
pipenv --version
docker --version
docker compose version
```

---

## 2. Clone the Repository

Clone the backend repository and switch to the project directory:

```bash
git clone git@github.com:lav5588/BookMyShow-backend.git
cd BookMyShow-backend
```

---

## 3. Environment Configuration

The application uses `django-environ` to manage environment configurations. Create your `.env` file from `.env.example`:

### On macOS / Linux:
```bash
cp .env.example .env
```

### On Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

### Configuration Variables Reference:
| Variable | Default Example | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `django-insecure-...` | Secret key used by Django for cryptographic signing |
| `DEBUG` | `True` (dev) / `False` (prod) | Toggle Django debug mode |
| `ACCESS_TOKEN_LIFETIME` | `15` | JWT Access Token expiration in **minutes** |
| `REFRESH_TOKEN_LIFETIME`| `1` | JWT Refresh Token expiration in **days** |
| `ROTATE_REFRESH_TOKENS` | `True` | Rotate refresh tokens upon `/api/users/refresh/` |
| `BLACKLIST_AFTER_ROTATION`| `True` | Invalidate previous refresh token when rotated |
| `SIGNING_KEY` | `"lav kumar"` | HMAC signing key for JWT tokens |

---

## 4. Start the Database Container

The project includes a ready-to-run `compose.yaml` file configured for PostgreSQL 18.

Start the database container in the background:
```bash
docker compose up -d
```

### Check Database Health:
```bash
docker compose ps
```

The database container runs on:
- **Host**: `127.0.0.1`
- **Port**: `5432`
- **Database**: `bookmyshowdb`
- **Username**: `lav`
- **Password**: `password1`

*(To stop the database later: `docker compose down`)*

---

## 5. Install Dependencies & Activate Environment

Use `pipenv` to create the virtual environment and install all application and development packages:

```bash
# Install both application and development dependencies
pipenv install --dev

# Activate the virtual environment
pipenv shell
```

---

## 6. Run Database Migrations

Apply the database schema to your local PostgreSQL instance:

```bash
# If inside pipenv shell:
python manage.py migrate

# Or directly with pipenv:
pipenv run migrate
```

---

## 7. Create an Admin Account

To access the Django admin portal, create a superuser:

```bash
pipenv run createsuperuser
```
Provide an email, name, and strong password when prompted.

---

## 8. Seed Data with Fixtures

The backend provides a custom management command (`dump-fixtures`) that loads comprehensive sample data from `fixtures/`:
- Locations (Mumbai, Delhi, Bengaluru, etc.)
- Languages & Genres
- Movies & Details
- Cinemas & Auditory Dimensions
- Active & Upcoming Showtimes (Slots)
- Demo Users
- Realistic Initial Seat Bookings

Run the seeding command:
```bash
pipenv run python manage.py dump-fixtures
```

You should see output confirming the sequential population of all tables:
```
Starting fixture dump...
Dumping locations... ✓ Locations dumped successfully.
Dumping Languages... ✓ languages dumped successfully.
Dumping Genres... ✓ genres dumped successfully.
...
🎉 All fixtures were dumped successfully.
```

---

## 9. Populate Media Assets (Posters & Profile Photos)

To populate movie posters and mock user photos with real images, execute the provided helper scripts via the Django shell.

Open the Django interactive shell:
```bash
python manage.py shell
```

### 9.1 Movie Posters:
Copy and paste the code from [`scripts/fill-movie-poster.py`](../../scripts/fill-movie-poster.py) into the shell, or execute:
```python
with open("scripts/fill-movie-poster.py") as f:
    exec(f.read())
```

### 9.2 User Profile Avatars:
Copy and paste the code from [`scripts/fill-user-photos.py`](../../scripts/fill-user-photos.py) into the shell, or execute:
```python
with open("scripts/fill-user-photos.py") as f:
    exec(f.read())
```

Exit the shell:
```python
exit()
```

---

## 10. Start the Development Server

Launch the Django development server:

```bash
pipenv run start
```
*(Alternatively: `python manage.py runserver`)*

The server will be accessible at:
- **API Base URL**: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
- **Swagger UI Interactive Docs**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- **Django Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 11. Pipenv Helper Scripts

The `Pipfile` comes pre-configured with productive shorthand commands:

| Shorthand | Command | What it does |
| :--- | :--- | :--- |
| `pipenv run start` | `python manage.py runserver` | Starts local dev server |
| `pipenv run migrate` | `python manage.py migrate` | Runs pending migrations |
| `pipenv run makemigrations` | `python manage.py makemigrations` | Creates new migrations |
| `pipenv run createsuperuser` | `python manage.py createsuperuser` | Creates superuser |
| `pipenv run test` | `python manage.py test` | Executes full test suite |
| `pipenv run lint` | `ruff check` | Runs Ruff linter |
| `pipenv run lint-fix` | `ruff check --fix` | Automatically fixes linting issues |
| `pipenv run format` | `ruff format` | Formats code with Ruff |
| `pipenv run format-check` | `ruff format --check` | Validates formatting |
| `pipenv run flushexpiredtokens` | `python manage.py flushexpiredtokens` | Purges expired JWTs from blacklist |
| `pipenv run generate-schema` | `python manage.py spectacular --color --file schema.yml` | Regenerates OpenAPI schema |

---

## 12. Connecting with Frontend

This backend is designed to seamlessly pair with the BookMyShow Frontend:
- **Frontend Repository**: [BookMyShow-frontend](https://github.com/lav5588/BookMyShow-frontend)
- **CORS Allowed Origins**: Configured for `http://localhost:3000` (React/Next dev server) and `http://localhost:4173` (Vite preview).
- **Credentials Support**: Enabled (`CORS_ALLOW_CREDENTIALS = True`) to allow cookie transmission for JWT refresh tokens.
