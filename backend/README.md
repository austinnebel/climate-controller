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
