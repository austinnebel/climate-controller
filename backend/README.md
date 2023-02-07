# Climate Controller Backend

The backend of this project uses Django.

## Requirements

-   [Python 3.7](https://www.python.org/downloads/release/python-379/)
-   `pip`
    -   This is generally always installed alongside Python.
-   [`pipenv`](https://pypi.org/project/pipenv/#installation)
    -   `pip install pipenv`

## Installation

1. Run `pipenv install` in this directory.
2. Run `pipenv shell` to enter the Pip environment.
3. Run `python manage.py migrate` to install all database migrations.
4. Run `python manage.py createsuperuser` and follow the steps to make a user.
5. Run `python manage.py runserver` to start the development server.
