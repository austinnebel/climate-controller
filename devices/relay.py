import atexit
import logging
import RPi.GPIO as GPIO

LOGGER = logging.getLogger()
GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

class Relay:

    def __init__(self, relay_pin, normally_closed = True):
        """
        Controls a GPIO-controlled relay module.

        Args:
            relay_pin (int): GPIO pin used to open/close the relay.
            normally_closed (bool, optional): If True, voltage initially starts low and voltage is applied to close the relay.
                                            If False, voltage initially starts high and is cut to close the relay.
                                            Defaults to True.
        """
        self.pin = relay_pin
        self.normally_closed = normally_closed

        if self.normally_closed:
            self.ON = GPIO.LOW
            self.OFF = GPIO.HIGH
        else:
            self.ON = GPIO.HIGH
            self.OFF = GPIO.LOW

        GPIO.setup(self.pin, GPIO.OUT)

    def is_on(self):
        """
        Returns the current state of the relay.

        Returns:
            bool: True if self.normally_open is True and GPIO is active, or if self.normally_open is False and GPIO is inactive.
                  False if self.normally_open is True and GPIO is inactive, or if self.normally_open is False and GPIO is active.
        """
        pin_state = bool(GPIO.input(self.pin))
        if self.normally_closed:
            return not pin_state
        return pin_state

    def on(self):
        GPIO.output(self.pin, self.ON)

    def off(self):
        GPIO.output(self.pin, self.OFF)
