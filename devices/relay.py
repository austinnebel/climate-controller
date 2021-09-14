import atexit
import logging
import RPi.GPIO as GPIO

LOGGER = logging.getLogger()
GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

class Relay:

    def __init__(self, relay_pin):
        self.pin = relay_pin
        GPIO.setup(self.pin, GPIO.OUT)

    def is_on(self):
        return bool(GPIO.input(self.pin))

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
