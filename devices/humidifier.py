import logging
from time import sleep
from .relay import Relay

LOGGER = logging.getLogger()

class Humidifier:

    def __init__(self, pin):
        self.relay = Relay(pin)

    def is_on(self):
        return self.relay.value()

    def on(self):
        LOGGER.info("Activating Humidifier.")
        self.relay.value(0)

    def off(self):
        LOGGER.info("Deactivating Humidifier.")
        self.relay.value(1)

    def spray(self, spray_time):
        print("Spraying humidifier for {} seconds.".format(self.spray_time))
        self.on()
        sleep(spray_time)
        self.off()
