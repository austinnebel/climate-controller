# Climate Controller Backend

The backend of this project uses Django REST framework for managing the backend API

## Requirements

-   [Python 3.7](https://www.python.org/downloads/release/python-379/)
-   pip
    -   This is generally always installed alongside Python.
-   [pipenv](https://pypi.org/project/pipenv/#installation)
    -   `pip install pipenv`
-   [docker](https://docs.docker.com/get-docker/)

## Installation

1. `pipenv install --dev` - Installs Python dependencies in this directory.
2. `pipenv shell` - Enters the Pip environment.
3. `python manage.py migrate` - Initializes and installs all database migrations.
4. `python manage.py createsuperuser` - Creates a super user for Django.
5. `docker run -p 6379:6379 -d redis:5` - Initializes a redis server in a docker container.
6. `python manage.py runserver` - Starts the DJango development server.

### Secret Key

A secret key is needed to keep Django secure. We can use the `get_random_secret_key` function built into Django to get one.

Run the following to generate the secret key and inject it into a **.env** file:

`pipenv run --quiet python -c 'from django.core.management.utils import get_random_secret_key; print(f"SECRET_KEY=\"{get_random_secret_key()}\"")' > .env`

This will be read by **backend/settings.py** at runtime.
