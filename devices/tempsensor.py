from threading import Thread
import logging
import time
import datetime
import Adafruit_DHT

LOGGER = logging.getLogger()


class Reading:

    def __init__(self, temp, hum, use_fahrenheit = True):
        self.use_fahrenheit = use_fahrenheit

        if temp != None:
            if self.use_fahrenheit:
                temp = (temp * 9/5) + 32
            temp = round(temp, 2)
        if hum != None:
            hum = round(hum, 2)

        self.temp = temp
        self.hum = hum
        self.time = datetime.datetime.now()

    def __str__(self):
        unit = "C"
        if self.use_fahrenheit:
            unit = "F"
        return f"{self.temp}{unit} {self.hum}% {self.time.strftime('%H:%M:%S')}"

class TempSensor(Thread):

    def __init__(self, pin, use_fahrenheit = True, buffer_size = 10):
        Thread.__init__(self)
        self.daemon = True
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin
        self.reading_buff = []
        self.use_fahrenheit = use_fahrenheit
        self.buffer_size = buffer_size

    @property
    def temperature(self):
        if len(self.reading_buff) > 0:
            return self.reading_buff[-1].temp
        return None

    @property
    def humidity(self):
        if len(self.reading_buff) > 0:
            return self.reading_buff[-1].hum
        return None

    @property
    def read(self):
        if len(self.reading_buff) > 0:
            return self.reading_buff[-1]
        return None

    @read.setter
    def read(self, reading : Reading):
        if len(self.reading_buff) >= self.buffer_size:
            self.reading_buff.pop(0)
        self.reading_buff.append(reading)

    def get_readings(self):
        return self.read

    def get_buffers(self):
        return self.reading_buff

    def get_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity != None: humidity = round(humidity, 2)
        if temperature != None: temperature = round(temperature, 2)
        return Reading(temperature, humidity, use_fahrenheit=self.use_fahrenheit)

    def run(self):
        while True:
            try:
                self.read = self.get_data()
            except Exception as e:
                LOGGER.error(f"Error reading from DHT22: {str(e)}")
            time.sleep(2)



