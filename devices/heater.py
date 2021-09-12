import logging
from .relay import Relay

LOGGER = logging.getLogger()

class Heater:

    def __init__(self, pin):
        self.relay = Relay(pin)

    def is_on(self):
        return self.relay.value()

    def on(self):
        LOGGER.info("Activating heater.")
        self.relay.value(0)

    def off(self):
        LOGGER.info("Deactivating heater.")
        self.relay.value(1)
