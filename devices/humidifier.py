import logging
from datetime import datetime as dt
from time import sleep
from threading import Thread
from .relay import Relay

LOGGER = logging.getLogger()

class Humidifier:

    def __init__(self, pin):
        self.relay = Relay(pin)
        self.spray_times = []

    def add_spray(self):
        now = dt.now()
        if len(self.spray_times) >= 0:
            for t in self.spray_times:
                if (now-t).total_seconds() > 120*60:
                    self.spray_times.remove(t)
        self.spray_times.append(now)

    def last_spray(self):
        """
        Returns last recorded spray time.

        Returns:
            datetime: Last spray time.
        """
        if len(self.spray_times) >= 0:
            return self.spray_times[-1]

    def is_on(self):
        return self.relay.is_on()

    def on(self):
        if not self.is_on():
            LOGGER.info("Activating Humidifier.")
            self.relay.on()

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
        self.add_spray()
