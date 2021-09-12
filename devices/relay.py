import logging
from rpi.GPIO import Pin

LOGGER = logging.getLogger()

class Relay:

    def __init__(self, relay_pin):
        self.pin = relay_pin
        self.relay = Pin(relay_pin, Pin.OUT)
        self.is_on = False

    def value(self):
        return self.relay.value

    def on(self):
        self.relay.value(0)

    def off(self):
        self.relay.value(1)
