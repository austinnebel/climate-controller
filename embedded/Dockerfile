# syntax=docker/dockerfile:1

FROM python:3.7
WORKDIR /embedded
COPY . .
RUN pip install pipenv
RUN pipenv install --dev
CMD [ "pipenv", "run", "python", "main.py"]
