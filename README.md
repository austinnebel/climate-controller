# Climate Controller

## Overview

This repository uses a Raspberry Pi to control and monitor the climate of a given environment. It includes a python-implemented embedded system, a React frontend, and a Django backend that implements both HTTP and WebSocket connections.

The Raspberry Pi will continuously read temperature and humidity information from a DHT22 sensor and publish that information to a websocket on the Django backend. The React frontend can connect to that websocket to read information in real time, and can publish GET requests to certain endpoints to receive past data over a specified period of time.

This repository was designed to work with a raspberry-pi nano.

### Embedded Components

> **NOTE**
> The documentation for the embedded project can be found [here](embedded/README.md).

The embedded project is designed to work with a raspberry Pi nano, DHT22 sensor, GPIO relay, humidifier, heat lamp, and heating pad. The DHT22 sensor captures humidity and temperature data, and the GPIO relay provides or cuts power from the heat lamp, humidifier, and heating pad. The software in the embedded project takes the running average of readings from the DHT22 and uses the results to determine what devices to turn on or off. The project will also push this data to a websocket in the backend project and store data in the backend database.

### Django Backend

> **NOTE**
> The documentation for the backend can be found [here](backend/README.md).

The `embedded` package periodically pushes climate information to the backend. This data can both be saved in the database as well as published to a websocket. The websocket can be used to broadcast real-time data without bloating the database, while saving data to the database allows for reading past information over a period of time. The websocket channels in Django are implemented by connecting to a [redis](https://redis.io/docs/getting-started/) instance.

### React Frontend

> **NOTE**
> The documentation for the frontend can be found [here](frontend/README.md).

The frontend service is designed to display real-time information about the climate data captured by the DHT22 sensor in the `embedded` project. It displays temperature and humidity data, along with two graphs display the history of each.

### Configuration

To configure the program, create a file called config.ini in the root directory, and create the values as described in config.ini.example.

## Installation

### Requirements

-   pipenv
-   python3.7+
-   redis-server
-   Node.js
-   npm

### Instructions

1. In root directory, install Python dependencies: `pipenv install`
2. In frontend directory, install Node dependencies: `npm install`
3. Install redis server: `sudo apt install redis-server`
    - Make sure the server is on and enabled by default:
        - `sudo systemctl start redis-server`
        - `sudo systemctl enable redis-server`
4. Copy all .service files from the install/ directory to /etc/systemd/system/
5. Reload system services: `systemctl daemon-reload`
6. Each service file is with respect to the frontend, backend, and embedded components. To start them, run the following:
    - `sudo systemctl start climate_emb`
    - `sudo systemctl start climate_front`
    - `sudo systemctl start climate_back`
