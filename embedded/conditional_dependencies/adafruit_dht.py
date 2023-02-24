"""
This will attempt to import RPi.GPIO. If this fails (due to not running on a GPIO-capable device),
this will import `Mock.GPIO`
"""
from random import random

class DHT22:
    """
    Mock DHT22 sensor object. This is used as the input to
    `Adafruit_DHT.read_sensor`.
    """
    pass

class Mock_Adafruit_DHT:
    """
    Mock `Adafruit_DHT` import.
    """

    DHT22 = DHT22()

    def read_retry(sensor: DHT22, pin: int):
        return (random() * 10 + 60, random() * 10 + 20)

try:
    import Adafruit_DHT
except (ImportError, ModuleNotFoundError):
    print("Warning: Using Mock DHT subsystem.")
    Adafruit_DHT = Mock_Adafruit_DHT
