# Code Owners

This document defines repository code ownership for the **BookMyShow Backend** codebase, specifying the teams and individuals responsible for reviewing and approving changes across various modules and paths.

---

## Codeowners Specification

Below is the active CODEOWNERS definition based on GitHub's code ownership specification:

```text
# ==============================================================================
# GLOBAL REPOSITORY OWNERSHIP
# ==============================================================================
# Default owner for everything in the repository unless explicitly overridden
*                       @lav5588

# ==============================================================================
# CORE ARCHITECTURE & SETTINGS
# ==============================================================================
/bookmyshow/            @lav5588
/apps/core/             @lav5588
manage.py               @lav5588
Pipfile                 @lav5588
Pipfile.lock            @lav5588

# ==============================================================================
# DOMAIN APPLICATIONS
# ==============================================================================
# Cinema, Locations & Showtimes
/apps/cinema/           @lav5588

# Movies, Genres, Languages & Schedules
/apps/movie/            @lav5588

# Seat Booking Engine & Concurrency
/apps/seat_booking/     @lav5588

# User Authentication, Profiles & JWT Security
/apps/user/             @lav5588

# Contact Us Queries
/apps/contactus/        @lav5588

# ==============================================================================
# INFRASTRUCTURE & AUTOMATION
# ==============================================================================
compose.yaml            @lav5588
/.github/               @lav5588
/scripts/               @lav5588
/fixtures/              @lav5588
schema.yml              @lav5588

# ==============================================================================
# DOCUMENTATION
# ==============================================================================
/docs/                  @lav5588
README.md               @lav5588
```
