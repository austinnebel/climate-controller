from threading import Thread
import logging
import Adafruit_DHT


LOGGER = logging.getLogger()

class TempSensor(Thread):

    def __init__(self, pin, use_fahrenheit = True, buffer_size = 15):
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin
        self.humidity_buff = []
        self.temperature_buff = []
        self.use_fahrenheit = use_fahrenheit
        self.buffer_size = buffer_size

    @property
    def temperature(self):
        if len(self.temperature_buff) > 0:
            return self.temperature_buff[-1]
        return None

    @property
    def humidity(self):
        if len(self.humidity_buff) > 0:
            return self.humidity_buff[-1]
        return None

    @temperature.setter
    def temperature(self, temp):
        if len(self.temperature_buff) > self.buffer_size:
            self.temperature_buff.pop(0)
        if self.use_fahrenheit:
            temp = (temp * 9/5) + 32
        self.temperature_buff.append(temp)

    @humidity.setter
    def humidity(self, hum):
        if len(self.humidity_buff) > self.buffer_size:
            self.humidity_buff.pop(0)
        self.humidity_buff.append(hum)

    def get_readings(self):
        return self.temperature, self.humidity

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return humidity, temperature

    def run(self):
        while True:
            try:
                self.humidity, self.temperature = self.read()
            except Exception as e:
                LOGGER.error(f"Error reading from DHT22: {str(e)}")



