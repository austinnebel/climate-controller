from threading import Thread, Event
import logging
import time
import datetime
import Adafruit_DHT

LOGGER = logging.getLogger()


class Reading:

    def __init__(self, temp, hum, convert = True, use_fahrenheit = True):
        """
         Holds temperature and humidity data, as well as the time of data capture.

         Automatically will make conversions from Celcius to Fahrenheit if `convert` is true.

         NOTE: use_fahrenheit is only used for logging output.


        Args:
            temp (float): Temperature.
            hum (float): Humidity percentage.
            convert (bool, optional): If true, makes conversion to fahrenheit if use_fahrenheit is True. Defaults to True.
            use_fahrenheit (bool, optional): Whether to use fahrenheit units in logging output. Defaults to True.
        """
        self.use_fahrenheit = use_fahrenheit

        if temp != None:
            if self.use_fahrenheit and convert == True:
                temp = (temp * 9/5) + 32
            temp = round(temp, 2)
        if hum != None:
            hum = round(hum, 2)

        self.temp = temp
        self.hum = hum
        self.time = datetime.datetime.now()

    def __str__(self):
        if self.temp == None or self.hum == None:
            return "Read error."
        unit = "C"
        if self.use_fahrenheit:
            unit = "F"
        return f"{self.temp}{unit} {self.hum}% {self.time.strftime('%H:%M:%S')}"

class TempSensor(Thread):

    def __init__(self, pin, use_fahrenheit = True, buffer_size = 10):
        """
        Continuously captures temperature and humidity data from DHT22. This class
        can be instantiated, and then run as a thread using its run() method.

        Args:
            pin (int): GPIO data pin for DHT sensor.
            use_fahrenheit (bool, optional): If True, uses fahrenheit units, else uses Celcius. Defaults to True.
            buffer_size (int, optional): Max amount of readings to store in memory at a time. Defaults to 10.
        """
        Thread.__init__(self)
        self.daemon = True
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin
        self.reading_buff = []
        self.use_fahrenheit = use_fahrenheit
        self.buffer_size = buffer_size

        self.term = Event()

    @property
    def temperature(self):
        """
        Returns the latest recorded temperature.

        Returns:
            float: Last recorded temperature.
        """
        if len(self.reading_buff) > 0:
            return self.reading_buff[-1].temp
        return None

    @property
    def humidity(self):
        """
        Returns the latest recorded humidity percentage.

        Returns:
            float: Last recorded humidity percentage.
        """
        if len(self.reading_buff) > 0:
            return self.reading_buff[-1].hum
        return None

    @property
    def avg(self):
        """
        Returns a `Reading` object containing the average values of all Readings stored in the buffer.

        Returns:
            Reading, None: Reading object if readings are available in the buffer. False otherwise.
        """
        if len(self.reading_buff) > 0:
            t_avg = sum([r.temp for r in self.reading_buff])/len(self.reading_buff)
            h_avg = sum([r.hum for r in self.reading_buff])/len(self.reading_buff)

            return Reading(t_avg, h_avg,  self.reading_buff[-1].time)
        return None

    @property
    def read(self):
        """
            Reading: Latest recorded reading. None if unavailable.
        """
        if len(self.reading_buff) > 0:
            return self.reading_buff[-1]
        return None

    @read.setter
    def read(self, reading : Reading):
        """
        Adds a Reading object to the reading buffer. If the buffer is full,
        removes first item before appending.

        Args:
            reading (Reading): Reading object captured from sensor.
        """
        if len(self.reading_buff) >= self.buffer_size:
            self.reading_buff.pop(0)
        self.reading_buff.append(reading)

    def get_readings(self):
        """
        Returns the latest recorded reading.
        """
        return self.read

    def get_buffers(self):
        """
        Returns all values in the buffer.

        Returns:
            list[Reading]: List of captured Reading entries.
        """
        return self.reading_buff

    def get_data(self):
        """
        Reads from the DHT sensor.

        Returns:
            Reading: Reading object containing the captured data.
        """
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity != None: humidity = round(humidity, 2)
        if temperature != None: temperature = round(temperature, 2)
        return Reading(temperature, humidity, use_fahrenheit=self.use_fahrenheit)

    def run(self):
        """
        Continously reads from sensor every secondl.
        Runs indefinitely until terminate() is called.
        """
        while not self.term.is_set():
            try:
                self.read = self.get_data()
            except Exception as e:
                LOGGER.error(f"Error reading from DHT22: {str(e)}")
            self.term.wait(1)

    def terminate(self):
        """
        Stops this threads run() method.
        """
        self.term.set()



