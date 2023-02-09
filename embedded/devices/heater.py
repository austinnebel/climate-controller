from datetime import datetime
import logging

from utils import Database
from .relay import Relay

LOGGER = logging.getLogger()

class Heater:

    def __init__(self, pin: int, db: Database, name = "Heater", normally_closed = True):
        """
        Controls a heating device.

        Args:
            pin (int): GPIO pin to activate the heater.
            database (Database): Database object to upload data to.
            normally_closed (bool, optional): If True, the relay for this device is normally closed i.e. turns off when its GPIO is activated.
                                              If False, the relay for this device is normally open i.e. turns on when its GPIO is activated.
                                              Defaults to True.
        """
        self.relay = Relay(pin, normally_closed = normally_closed)
        self.name = name
        self.db = db

    def is_on(self):
        return self.relay.is_on()

    def on(self):
        if not self.is_on():
            LOGGER.info(f"Activating {self.name}.")
            self.relay.on()

            data = {
                "name": self.name,
                "event": "ON",
                "time": str(datetime.now()),
            }
            self.db.send_data(data)

    def off(self):
        if self.is_on():
            LOGGER.info(f"Deactivating {self.name}.")
            self.relay.off()

            data = {
                "name": self.name,
                "event": "OFF",
                "time": str(datetime.now()),
            }
            self.db.send_data(data)