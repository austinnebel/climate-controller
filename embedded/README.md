# Climate Controller Embedded System

This project contains the embedded components of the project. These components record data through hardware
sensors and publish the information to the backend project.

To run this project in a docker container, run the following in this directory:

```bash
docker build -t climate-controller-embedded .

docker run climate-controller-embedded
```

> **WARNING**
>
> If this project is not run in a Raspberry Pi environment, it will automatically switch to a mock implementation of the DHT22 sensor and a warning will be printed to the console. This is done to improve development environment; otherwise, proper testing could only take place on the Raspberry Pi itself.

> **NOTE**
>
> The above command will not be able to communicate with the other containers unless they are on the same virtual network. This is done automatically by `docker compose`.

## Requirements

-   [Python 3.9](https://www.python.org/downloads/release/python-3913/)
-   `pip`
    -   This is generally always installed alongside Python.
-   [pipenv](https://pypi.org/project/pipenv/#installation)

## Installation

1. Copy the contents of **config.example.ini** into a new file **config.ini**
    - This can be easily done in Linux with `cat config.example.ini > config.ini`
    - Most variables can be left alone, however the `username` and `password` fields in the `[SERVER]` section are required. These are the username and password to the backend/ Django project.
2. Run `pipenv install` in this directory.
3. Run `pipenv shell` to enter the Pip environment.
4. Run `python main.py` to start the project.
