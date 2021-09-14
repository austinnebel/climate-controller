import logging
from time import sleep
from threading import Thread
from .relay import Relay

LOGGER = logging.getLogger()

class Humidifier:

    def __init__(self, pin):
        self.relay = Relay(pin)

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
        print(f"Spraying humidifier for {spray_time} seconds.")
        t = Thread(target = self._spray, args = [spray_time])
        t.start()

