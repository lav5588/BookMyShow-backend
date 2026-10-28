# 🎬 BookMyShow Backend

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/django--rest--framework-3.16-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-18-blue.svg)](https://www.postgresql.org/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Swagger](https://img.shields.io/badge/Swagger-OpenAPI%203.0-brightgreen.svg)](http://localhost:8000/api/schema/swagger-ui/)

The robust, production-grade backend engine powering the **BookMyShow** movie ticket discovery and reservation ecosystem. Built on **Python 3.14**, **Django 5.2**, and **Django REST Framework**, featuring atomic multi-seat booking with race-condition prevention, hybrid JWT + HttpOnly Cookie authentication, automated Swagger/OpenAPI documentation, and Dockerized PostgreSQL storage.

> 🌐 **Frontend Application**: [BookMyShow-frontend Repository](https://github.com/lav5588/BookMyShow-frontend)

---

## 📚 Documentation Index

Explore the comprehensive project documentation:

### 🚀 Guides
- **[Getting Started Guide](docs/guides/getting_started.md)**: Complete step-by-step installation, environment setup, database seeding, and development workflow.

### 🔌 API Reference
- **[API Overview](docs/api/overview.md)**: Conventions, base URLs, authentication headers, error formats, and pagination.
- **[API Endpoints Reference](docs/api/endpoints.md)**: Full REST endpoint catalog with request/response schemas, sample JSON, and status codes.

### 🏛️ Architecture & System Design
- **[System Overview](docs/architecture/system_overview.md)**: Architectural layers, component diagram, technology rationale, and request lifecycle.
- **[Database Design & ERD](docs/architecture/database_design.md)**: Detailed entity-relationship diagram, table definitions, foreign keys, and constraints.
- **[Seat Booking Engine](docs/architecture/booking_engine.md)**: Concurrency model, atomic batch reservations, race-condition mitigation, and double-booking guards.
- **[Authentication & Security Flow](docs/architecture/authentication_flow.md)**: Hybrid JWT + HttpOnly cookie model, token rotation, blacklisting, and security protocols.

### 👥 Community & Governance
- **[Authors](docs/AUTHORS.md)**: Project maintainer and contributor profile details.
- **[Contributors](docs/Contributors.md)**: Contributor recognition and primary contributions.
- **[Code Owners](docs/codeowners.md)**: Repository code ownership specification.

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.14** (or 3.12+)
- **Pipenv**
- **Docker & Docker Compose**

### 2. Configure Environment
```bash
# Clone the repository
git clone git@github.com:lav5588/BookMyShow-backend.git
cd BookMyShow-backend

# Set up environment variables
cp .env.example .env
```

### 3. Launch PostgreSQL Database
```bash
docker compose up -d
```

### 4. Install Dependencies
```bash
pipenv install --dev
pipenv shell
```

### 5. Run Migrations & Load Sample Data
```bash
# Apply schema
python manage.py migrate

# Seed database with locations, movies, cinemas, slots, and bookings
python manage.py dump-fixtures
```

### 6. Start the Server
```bash
pipenv run start
```

The API is live at **[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)**  
Interactive Swagger UI: **[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)**  
Django Admin: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

---

## 📂 Project Structure

```text
BookMyShow-backend/
├── apps/
│   ├── cinema/             # Venues, locations, auditoriums, and showtime slots
│   ├── contactus/          # Customer feedback and inquiry processing
│   ├── core/               # Shared utilities, base models, fixture management
│   ├── movie/              # Movies, genres, languages, and catalog browsing
│   ├── seat_booking/       # Atomic seat booking engine & ticket tracking
│   └── user/               # Custom User model, JWT authentication, and profiles
├── bookmyshow/             # Django project configuration, settings, and URLs
├── docs/                   # Project documentation
│   ├── api/                # API overview and endpoint specifications
│   │   ├── endpoints.md
│   │   └── overview.md
│   ├── architecture/       # Architectural deep dives and diagrams
│   │   ├── authentication_flow.md
│   │   ├── booking_engine.md
│   │   ├── database_design.md
│   │   └── system_overview.md
│   ├── guides/             # Developer setup and onboarding guides
│   │   └── getting_started.md
│   ├── AUTHORS.md          # Project author and maintainer information
│   ├── codeowners.md       # CODEOWNERS documentation and review policy
│   └── Contributors.md     # Contribution guidelines and community roadmap
├── fixtures/               # Seed data for movies, cinemas, slots, users, etc.
├── scripts/                # Utility scripts for downloading posters and photos
├── compose.yaml            # Docker Compose service definition for PostgreSQL 18
├── manage.py               # Django management script
├── Pipfile                 # Application dependencies and task runners
├── Pipfile.lock            # Deterministic dependency lockfile
├── README.md               # Repository landing documentation
├── ruff.toml               # Ruff linter and formatter configuration
└── schema.yml              # Exported OpenAPI 3.0 specification
```

---

## 🛠️ CLI Task Runner Reference

The following shorthand commands are available via `pipenv run`:

| Command | Action |
| :--- | :--- |
| `pipenv run start` | Launch the local development server |
| `pipenv run migrate` | Apply database migrations |
| `pipenv run makemigrations` | Generate new database migration files |
| `pipenv run test` | Run automated test suite across all apps |
| `pipenv run lint` | Analyze code with Ruff linter |
| `pipenv run lint-fix` | Automatically resolve autofixable Ruff violations |
| `pipenv run format` | Format code using Ruff formatter |
| `pipenv run flushexpiredtokens` | Purge expired JWT refresh tokens from blacklist |
| `pipenv run generate-schema` | Regenerate `schema.yml` OpenAPI specification |

---

## 🧪 Testing

Execute the comprehensive test suite across all applications:

```bash
pipenv run test
```

To run tests for a single module:
```bash
python manage.py test apps.seat_booking
python manage.py test apps.cinema
python manage.py test apps.movie
python manage.py test apps.user
```
