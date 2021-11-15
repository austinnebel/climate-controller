import logging
import requests
import json
import asyncio
from queue import Queue
from websockets import connect

from .now import now


LOGGER = logging.getLogger()

logging.getLogger("websockets").setLevel(logging.WARNING)

class Database():

    def __init__(self, url, user, password):
        """
        Utility for posting data to the local database server.
        """
        self.url = url
        self.user = user
        self.password = password

    def send_data(self, data, timeout = 20):

        if "time" not in data.keys():
            data["time"] = str(now())

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
        if self.ws and self.ws.open:
            return True

        LOGGER.debug(f"Connecting to {self.url}")
        try:
            self.ws = await connect(self.url, close_timeout = close_timeout)
        except asyncio.TimeoutError as e:
            LOGGER.error("Failed to make socket connection to database.")
            return False
        return True

    async def _send(self, message):

        if not await self.connect():
            return False

        if "time" not in message.keys():
            message["time"] = str(now())

        await self.ws.send(json.dumps(
            {
                "type": "receive.json",
                "text": message
                }
            )
        )
        r = json.loads(await self.ws.recv())
        if "type" in r.keys() and r["type"] == "websocket.accept":
            LOGGER.debug(f"Sent message over socket: {message}")
            return True
        return False

    async def begin_event_loop(self):

        while True:
            while not self.queue.empty():
                await self.send(self.queue.popleft())
            asyncio.sleep(1)

    def start(self):
        asyncio.run(self.begin_event_loop())

    def send(self, data, timeout = 5):
        return self.loop.run_until_complete(self._send(data))

