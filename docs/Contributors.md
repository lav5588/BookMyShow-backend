# Contributors

Thank you for your interest in contributing to the **BookMyShow Backend**! Open-source contributions from developers of all skill levels are warmly welcomed.

---

## Current Contributors

| Contributor | GitHub Profile | Primary Contributions |
| :--- | :--- | :--- |
| **Lav Kumar Yadav** | [@lav5588](https://github.com/lav5588) | Architecture, core APIs, seat booking engine, data fixtures, and testing suite. |

---

## How to Contribute

We follow standard GitHub Flow for managing changes and improvements:

### 1. Find or Propose an Issue
- Browse existing open issues or create a new issue detailing a bug or proposed feature.
- Discuss architectural changes before writing large blocks of code.

### 2. Fork and Branch
1. Fork the repository to your own GitHub account.
2. Clone your fork locally:
   ```bash
   git clone git@github.com:<your-username>/BookMyShow-backend.git
   cd BookMyShow-backend
   ```
3. Create a descriptive feature branch:
   ```bash
   git checkout -b feature/seat-reservation-hold
   ```

### 3. Local Setup & Testing
Follow the [`docs/guides/getting_started.md`](file:///c:/Users/lavku/Projects/BookMyShow/backend/docs/guides/getting_started.md) guide:
1. Launch database: `docker compose up -d`
2. Install packages: `pipenv install --dev`
3. Run migrations: `pipenv run migrate`
4. Run tests: `pipenv run test`

### 4. Code Quality & Standards
Ensure all code conforms to our Ruff linting and formatting standards before opening a pull request:
```bash
# Verify formatting
pipenv run format-check

# Run linter
pipenv run lint

# Auto-fix issues
pipenv run lint-fix
```

### 5. Writing Tests
- Any new endpoint or bugfix must be accompanied by relevant unit or integration tests in `apps/<app_name>/tests/`.
- Ensure test coverage remains green across all existing tests.

### 6. Submitting a Pull Request
1. Commit your changes with clear, descriptive commit messages.
2. Push your branch to GitHub:
   ```bash
   git push origin feature/seat-reservation-hold
   ```
3. Open a Pull Request against the `main` branch. Provide a clear summary of what changed and link any related issues.

---

## Roadmap & Contribution Opportunities

Looking for ideas to contribute? Here are key areas open for enhancement:
- [ ] **Redis Caching**: Cache cinema listings and movie catalogs for faster throughput.
- [ ] **Payment Gateway Integration**: Webhook handlers for Stripe / Razorpay transactions.
- [ ] **Celery / Redis Task Queue**: Asynchronous processing for booking confirmation emails.
- [ ] **Dynamic Seat Pricing**: Tiered pricing support for VIP, Premium, and Standard rows.
- [ ] **WebSocket Notifications**: Real-time push updates for live seat status changes.
