# Climate Controller Embedded System

This project contains the embedded components of the project. These components record data through hardware
sensors and publish the information to the backend project.

## Requirements

-   [Python 3.7](https://www.python.org/downloads/release/python-379/)
-   `pip`
    -   This is generally always installed alongside Python.
-   [`pipenv`](https://pypi.org/project/pipenv/#installation)
    -   `pip install pipenv`

## Installation

1. Copy the contents of **config.ini.example** into a new file **config.ini**
    - This can be easily done in Linux with `cat config.ini.example > config.ini`
    - Most variables can be left alone, however the `username` and `password` fields in the `[SERVER]` section are required.
2. Run `pipenv install` in this directory.
3. Run `pipenv shell` to enter the Pip environment.
4. Run `python main.py` to start the project.

## Docker

This package can be easily run with docker. To allow docker to have access to the Raspberry Pi's GPIO system, the container must be run with the following flags:

`docker run --device /dev/gpiomem -t climate-controller-embedded .`

The `--device /dev/gpiomem` snippet gives docker access to the GPIO system device.

> **NOTE**
> See [this StackOverflow answer](https://stackoverflow.com/a/48234752) for more information.
