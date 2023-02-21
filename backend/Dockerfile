# Build image
FROM --platform=$BUILDPLATFORM python:3.9.16-bullseye AS builder

WORKDIR /usr/src

# Tell pipenv to create ".venv" folder in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

# Install all build requirements
RUN apt update && \
    apt install -y \
    build-essential \
    libssl-dev  \
    libffi-dev \
    python3-dev \
    cargo \
    pkg-config && \
    apt clean


# Install Pipenv
RUN pip install --user pipenv

# Copy Pipfile
COPY Pipfile .

# Run Sync
RUN /root/.local/bin/pipenv install --verbose

# Runtime image
FROM python:3.9.16-slim-bullseye AS runtime

WORKDIR /usr/src/

# Copy .venv from builder
COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

COPY manage.py .
COPY application/ application/
COPY backend/ backend/

# Add backend user and make them the owner of /usr/src/
RUN adduser backend
RUN chown backend -R .

USER backend

# Make initial migrations and create user
RUN ./.venv/bin/python manage.py migrate
RUN ./.venv/bin/python manage.py createsuperuser --noinput

EXPOSE 8000

CMD [ "./.venv/bin/daphne", "backend.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
