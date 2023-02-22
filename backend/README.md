# Climate Controller Backend

The backend of this project uses Django REST framework for managing the backend API.

To run this project in a docker container, run the following in this directory:

```bash
docker build -t climate-controller-backend .

docker run -p 8000:8000 climate-controller-backend
```

> **NOTE**
>
> The above command will not be able to communicate with the other containers unless they are on the same virtual network. This is done automatically by `docker compose`.

## Development Requirements

-   [Python 3.9](https://www.python.org/downloads/release/python-3913/)
-   pip
    -   This is generally always installed alongside Python.
-   [pipenv](https://pypi.org/project/pipenv/#installation)
-   [docker](https://docs.docker.com/get-docker/)

## Installation

1. `pipenv install --dev` - Installs Python dependencies in this directory.
2. `pipenv shell` - Enters the Pip environment.
3. `python manage.py migrate` - Initializes and installs all database migrations.
4. `python manage.py createsuperuser` - Creates a super user for Django.
5. `docker run -p 6379:6379 -d redis:5` - Initializes a redis server in a docker container.
6. `python manage.py runserver` - Starts the DJango development server.

To deploy the server, run:

`pipenv run daphne backend.asgi:application -b 0.0.0.0 -p 8000`

### Secret Key

A secret key is needed to keep Django secure. We can use the `get_random_secret_key` function built into Django to get one.

Run the following to generate the secret key and inject it into a **.env** file:

`pipenv run --quiet python -c 'from django.core.management.utils import get_random_secret_key; print(f"SECRET_KEY=\"{get_random_secret_key()}\"")' > .env`

This will be read by **backend/settings.py** at runtime.
