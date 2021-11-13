import logging
from datetime import datetime as dt
from time import sleep
from threading import Thread
from datetime import datetime
from .relay import Relay

LOGGER = logging.getLogger()

class Humidifier:

    def __init__(self, pin, db):
        """
        Class to control humidifer device.

        Args:
            pin (int): GPIO pin used to activate humidifier.
            db (utils.Database): Database to post activation events to.
        """
        # humidifier should default to off
        self.relay = Relay(pin, normally_closed = False)
        self.db = db

    def is_on(self):
        return self.relay.is_on()

    def on(self):
        if not self.is_on():
            LOGGER.info("Activating Humidifier.")
            self.relay.on()

            data = {
                "name": "Humidifier",
                "event": "SPRAY",
                "time": str(datetime.now()),
            }
            self.db.send_data(data)

    def off(self):
        if self.is_on():
            LOGGER.info("Deactivating Humidifier.")
            self.relay.off()

    def _spray(self, spray_time):
        self.on()
        sleep(spray_time)
        self.off()

    def spray(self, spray_time):
        """
        Sprays the humidifer for spray_time seconds.
        """
        LOGGER.info(f"Spraying humidifier for {spray_time} seconds.")
        t = Thread(target = self._spray, args = [spray_time])
        t.start()