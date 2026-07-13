# BookMyShow Backend

- Backend application for serving BookMyShow frontend
- This Backend application is built on python django

## Getting Started

### Prerequisites

- **python**: Version 3.14. You can download and install it from python.org.
- **pip**: python package manager, which comes bundled with python.
- **pipenv**: A python virtual environment management tool that combined pip, virtualenv and pipfile into a single unified interface.

### Installing

To set up the project on your local environment, follow these steps:

1. **Clone the Repository**

    First, you need to clone the repository.

2. **Start environment**

   
```bash
    pipenv shell
```
    
3. **Install the necessary dependencies using pipenv**

```bash
    pipenv install
```
    
4. **Run the Development Server**

   
```bash
    pipenv run start
```

5. ** Set Up Database **
```bash
    docker compose up -d
```

6. **Filled the fixtures in database**
```bash
    python manage.py dump-fixtures
```

7. ** Fill the Movie Posters **
```
    Copy script from scripts/fill-movie-poster.py
    and paste in django shell. 
    for django shell run (python manage.py shell)
```

7. ** Fill the User Profile Pictures **
```
    Copy script from scripts/fill-user-photos.py
    and paste in django shell.
```
