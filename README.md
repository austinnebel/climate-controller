# Climate Controller

## Overview

This repository uses a Raspberry Pi to control and monitor the climate of a given environment. It includes a python-implemented embedded system, a React frontend, and a Django backend that implements both HTTP and WebSocket connections.

### Embedded Components

To control the various hardware elements, it uses a DHT22 sensor to capture humidity and temperature data, averages its values over a configurable amount of time, and uses the results to determine the power states of a series of GPIO relays that control power flow to a humidifier, heat lamp, and any general heating device. The entry point of this code is main.py in the root directory. The device code is in devices/, and utility functions can be found in utils/.

### Django Backend

Climate data is periodically pushed to the Django database. To capture real-time data without overfilling the database (thus reducing performance), data is pushed to a Django channel websocket in real time. The Django channel is implemented with the software `redis-server`. This code can be found in the backend/ directory.

### React Frontend

The frontend service is designed to display real-time information about the climate data captured by the DHT22 sensor. It displays temperature and humidity data, along with two graphs display the history of each.

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
    - `sudo systemctl start terrarium`
    - `sudo systemctl start terrarium_front`
    - `sudo systemctl start terrarium_back`
