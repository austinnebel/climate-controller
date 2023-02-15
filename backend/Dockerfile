# syntax=docker/dockerfile:1

FROM python:3.7
WORKDIR /backend
COPY . .
RUN pip install pipenv
RUN pipenv install
RUN pipenv run python manage.py migrate
RUN pipenv run python manage.py createsuperuser --noinput
EXPOSE 8000
CMD [ "pipenv", "run", "daphne", "backend.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
