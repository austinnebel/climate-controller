import logging
import requests
import json
import asyncio
import os
from queue import Queue
from config import Config
from utils.reading import Reading
from websockets import connect

from .now import now


LOGGER = logging.getLogger()

logging.getLogger("websockets").setLevel(logging.WARNING)

class Database():

    def __init__(self, config: Config):
        """
        Utility for posting data to the local database server.
        """
        self.config = config
        """ Application configuration. """

        self.http_url = f"http://{config.server_hostname}:{config.server_port}"
        """ HTTP URL to the database. """

        self.ws_url = f"ws://{config.server_hostname}:{config.server_port}"
        """ Websocket URL to the database. """

        self.user = os.getenv("DJANGO_USERNAME")
        """ Database Username. """

        self.password = os.getenv("DJANGO_PASSWORD")
        """ Database Password. """

        self.websocket = SocketConnector(self.ws_url + config.socket_endpoint, self.user, self.password)
        """ Database websocket connection. """

    def send_climate_data(self, data: Reading):
        self.__send_data(data, self.config.climate_endpoint)

    def send_device_data(self, data):
        self.__send_data(data, self.config.device_endpoint)

    def send_climate_data_websocket(self, data: Reading):
        self.websocket.send(data)

    def __send_data(self, data, endpoint, timeout = 20):
        """
        Makes a post request containing `data` to the database
        server at the specified `endpoint`.
        """
        if "time" not in data.keys():
            data["time"] = str(now())

        try:
            r = requests.post(self.http_url + endpoint, timeout = timeout, json = data, auth = (self.user, self.password))
        except Exception as e:
            LOGGER.error(f"Failed to update database. Error: {e}")
            return False
        if r.status_code == 201:
            LOGGER.debug(f"Database updated successfully with entry {data}")
            return True
        LOGGER.error(f"Database returned status code of {r.status_code}. Content: {r.content}")
        return False

class SocketConnector:

    def __init__(self, url: str, user: str, password: str):
        """
        Utility for posting data to the local database server.
        """
        self.url = url
        self.user = user
        self.password = password
        self.ws = None
        self.message_queue = Queue()
        self.loop = asyncio.get_event_loop()

    async def connect(self, close_timeout = 5):
        """
        This connects to the websocket and verifies a successful
        connection.
        """
        if self.ws and self.ws.open:
            return True

        LOGGER.debug(f"Connecting to {self.url}")
        try:
            self.ws = await connect(self.url, close_timeout = close_timeout)
        except asyncio.TimeoutError as e:
            LOGGER.error("Failed to make socket connection to database.")
            return False

        # makes sure the backend responded with "websocket.accept"
        response = json.loads(await self.ws.recv())
        if "type" in response.keys() and response["type"] == "websocket.accept":
            LOGGER.info("Websocket connection established.")
            return True

        return False

    async def _send(self, message):

        if not await self.connect():
            return False

        if "time" not in message.keys():
            message["time"] = str(now())

        await self.ws.send(
            json.dumps(
                {
                    "type": "receive.json",
                    "text": message
                }
            )
        )
        return True

    async def begin_event_loop(self):

        while True:
            while not self.message_queue.empty():
                await self._send(self.message_queue.popleft())
            asyncio.sleep(1)

    def start(self):
        asyncio.run(self.begin_event_loop())

    async def stop(self):
        if self.ws is not None:
            await self.ws.close()

    def send(self, data, timeout = 5):
        return self.loop.run_until_complete(self._send(data))

