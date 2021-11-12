import logging
import requests
import json
import asyncio
from queue import Queue
from websockets import connect

LOGGER = logging.getLogger()

class Database():

    def __init__(self, url, user, password):
        """
        Utility for posting data to the local database server.
        """
        self.url = url
        self.user = user
        self.password = password

    def send_data(self, data, timeout = 5):

        try:
            r = requests.post(self.url, timeout = timeout, json = data, auth = (self.user, self.password))
        except Exception as e:
            LOGGER.error(f"Failed to update database. Error: {e}")
            return False
        if r.status_code == 201:
            LOGGER.debug(f"Database updated successfully with entry {data}")
            return True
        LOGGER.error(f"Database returned status code of {r.status_code}. Content: {r.content}")
        return False

class SocketConnector:

    def __init__(self, url, user, password):
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
        LOGGER.debug(f"Connecting to {self.url}")
        try:
            self.ws = await connect(f"ws://{self.url}", close_timeout = close_timeout)
        except asyncio.TimeoutError as e:
            LOGGER.error("Failed to make socket connection to database.")
            return False
        return True

    async def send(self, message):
        if self.ws is None:
            connected = await self.connect()
            if not connected:
                return False

        await self.ws.send(json.dumps(
            {
                "type": "receive.json",
                "text": message
                }
            )
        )
        LOGGER.debug(f"Sent message over socket: {message}")
        return True

    async def begin_event_loop(self):

        while True:
            while not self.queue.empty():
                await self.send(self.queue.popleft())
            asyncio.sleep(1)

    def start(self):
        asyncio.run(self.begin_event_loop())

    def send_data(self, data, timeout = 5):
        return self.loop.run_until_complete(self.send(data))

