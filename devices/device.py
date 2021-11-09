import logging
from datetime import datetime as dt
from time import sleep
from threading import Thread
from .relay import Relay

LOGGER = logging.getLogger()

class RelayDevice:

    def __init__(self, pin, database, name = "Device", normally_closed = True):
        """
        Class to control a relay-controlled device.

        Args:
            pin (int): GPIO pin used to activate relay that powers the device.
            databse (utils.Database): Databse object to upload data to.
            normally_closed (bool, optional): If True, the relay for this device is normally closed i.e. turns off when its GPIO is activated.
                                    If False, the relay for this device is normally open i.e. turns on when its GPIO is activated.
                                    Defaults to True.
        """
        self.relay = Relay(pin, normally_closed = normally_closed)
        self.name = name
        self.db = database

    def is_on(self):
        """
        Returns True if Device is on, False otherwise.
        """
        return self.relay.is_on()

    def on(self):
        """
        Turns device on.
        """
        if not self.is_on():
            self.relay.on()
            LOGGER.info(f"Activating {self.name}.")

            data = {
                "name": self.name,
                "event": "ON",
                "time": str(dt.now()),
            }
            self.db.send_data(data)

    def off(self):
        """
        Turns device off.
        """
        if self.is_on():
            self.relay.off()
            LOGGER.info(f"Deactivating {self.name}.")
            data = {
                "name": self.name,
                "event": "OFF",
                "time": str(dt.now()),
            }
            self.db.send_data(data)

    def _activate_timed(self, activation_time):
        """
        Activates the device for activation_time seconds.
        """
        self.on()
        sleep(activation_time)
        self.off()

    def on_timed(self, activation_time):
        """
        Activates the device for activation_time seconds in a separate thread.
        """
        t = Thread(target = self._activate_timed, args = [activation_time])
        t.start()