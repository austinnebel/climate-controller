# Build image
FROM python:3.9.16-bullseye AS builder

# Tell pipenv to create .venv folder in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /usr/src

# Install Pipenv
RUN pip install --user pipenv

# Copy Pipfile
COPY Pipfile .

ARG TARGETPLATFORM

# Install dependencies based on platform
RUN if [ "${TARGETPLATFORM}" = "linux/arm/v6" ] ; then \
        echo "Installing for linux/arm/v6."; \
        /root/.local/bin/pipenv install --skip-lock; \
        # Manually install these libraries since installation will cause an error if not running on Raspberry Pi systems
        /root/.local/bin/pipenv run pip install Adafruit_DHT --install-option="--force-pi2"; \
        /root/.local/bin/pipenv run pip install RPi.GPIO; \
    else  \
        echo "Installing for host platform."; \
        /root/.local/bin/pipenv install --skip-lock; \
    fi


# Runtime image
FROM python:3.9.16-slim-bullseye AS runtime

WORKDIR /usr/src/

# Copy .venv from builder
COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

WORKDIR /usr/src/

COPY .env .
COPY config.ini .
COPY config.py .
COPY main.py .
COPY utils/ utils/
COPY devices/ devices/
COPY conditional_dependencies/ conditional_dependencies/

# Add "gpio" group with ID 997 (this is the name/ID of the group on RPi allowed to access GPIO systems).
# Add user "embedded" and add them to "gpio" group
RUN addgroup --gid 997 gpio && adduser --gid 997 embedded

# Make "embedded" the the owner of /usr/src/
RUN chown embedded -R .

USER embedded
ENTRYPOINT export $(cat .env | xargs) && ./.venv/bin/python main.py $0 $@