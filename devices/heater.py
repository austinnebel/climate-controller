import logging
from .relay import Relay

LOGGER = logging.getLogger()

class Heater:

    def __init__(self, pin):
        self.relay = Relay(pin)

    def is_on(self):
        return self.relay.is_on()

    def on(self):
        if not self.is_on():
            LOGGER.info("Activating heater.")
            self.relay.off()

    def off(self):
        if self.is_on():
            LOGGER.info("Deactivating heater.")
            self.relay.on()
