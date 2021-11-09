import logging
import time
import datetime
import Adafruit_DHT


from threading import Thread, Event

LOGGER = logging.getLogger()


class Reading:

    def __init__(self, temp, hum, time = None, convert = True, repr_fahrenheit = True):
        """
         Holds temperature and humidity data, as well as the time of data capture.

        Args:
            temp (float): Temperature.
            hum (float): Humidity percentage.
            time (datetime): If present, will set this objects timestamp.
            convert (bool): If True, will convert temp from Celsius to Fahrenheit.
            repr_fahrenheit (bool, optional): If True and convert is False, assumes that temp is already in Fahrenheit units.
                                              If True and convert is True, temp will be converted to Fahrenheit units.
                                              If False, temp will remain in Celsius.
        """
        self.repr_fahrenheit = repr_fahrenheit

        if temp != None:
            if convert and self.repr_fahrenheit:
                temp = (temp * 9/5) + 32
            temp = round(temp, 2)
        if hum != None:
            hum = round(hum, 2)

        self.temp = temp
        self.hum = hum
        self.time = datetime.datetime.now() if time is None else time

    def __str__(self):
        if self.temp == None or self.hum == None:
            return "Read error."

        unit = "F" if self.repr_fahrenheit else "C"
        return f"{self.temp}°{unit} {self.hum}% {self.time.strftime('%H:%M:%S')}"


class TempSensor(Thread):

    def __init__(self, pin, db, use_fahrenheit = True, buffer_duration = 30):
        """
        Continuously captures temperature and humidity data from DHT22. This class
        can be instantiated, and then run as a thread using its run() method.

        Args:
            pin (int): GPIO data pin for DHT sensor.
            use_fahrenheit (bool, optional): If True, uses fahrenheit units, else uses Celsius. Defaults to True.
            buffer_duration (int, optional): How many seconds of history should be contained in the reading buffer. Defaults to 30.
        """
        Thread.__init__(self)
        from utils import RotatingTimeList

        self.daemon = True
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin
        self.reading_buff = RotatingTimeList(buffer_duration)
        self.use_fahrenheit = use_fahrenheit
        self.buffer_duration = buffer_duration
        self.db = db
        self.term = Event()

    def available(self):
        return len(self.reading_buff.all()) > 0

    def get_avg(self):
        """
        Returns a `Reading` object containing the average values of all Readings stored in the buffer.
        The returned time value will be the time value stored in the most recent reading.

        Returns:
            Reading, None: Reading object if readings are available in the buffer. False otherwise.
        """
        if len(self.reading_buff) > 0:
            t_avg = sum([r.temp for r in self.reading_buff])/len(self.reading_buff)
            h_avg = sum([r.hum for r in self.reading_buff])/len(self.reading_buff)

            return Reading(t_avg, h_avg, time = self.reading_buff.latest().time, convert = False, repr_fahrenheit = self.use_fahrenheit)
        return None

    def add_reading(self, reading : Reading):
        """
        Adds a Reading object to the reading buffer. If temperature or humidity is None,
        no entry is added, but the buffer is cleaned to avoid old entries from being removed.

        Args:
            reading (Reading): Reading object captured from sensor.
        """
        if reading.temp is None or reading.hum is None:
            self.reading_buff.clean()
            return
        self.reading_buff.append(reading)

    def post_data(self, reading : Reading):
        json = {
                "temperature": reading.temp,
                "humidity": reading.hum,
                "time": str(reading.time)
            }
        self.db.send_data(json)

    def get_buffer(self):
        """
        Returns all values in the buffer.

        Returns:
            list[Reading]: List of captured Reading entries.
        """
        return self.reading_buff

    def read(self):
        """
        Reads from the DHT sensor.

        Returns:
            Reading: Reading object containing the captured data.
        """
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity != None and temperature != None:
            humidity = round(humidity, 2)
            temperature = round(temperature, 2)
        else:
            LOGGER.error(f"Failed to read sensor. Sensor returned {temperature}, {humidity}.")
        return Reading(temperature, humidity, convert = self.use_fahrenheit, repr_fahrenheit = self.use_fahrenheit)

    def run(self):
        """
        Continuously reads from sensor every second.
        Runs indefinitely until terminate() is called.
        """
        while not self.term.is_set():
            try:
                self.add_reading(self.read())
            except Exception as e:
                LOGGER.error(f"Error reading from DHT22: {str(e)}")
            # dht sensors need a minimum of 2 seconds between readings
            self.term.wait(2)

    def terminate(self):
        """
        Stops this threads run() method.
        """
        self.term.set()



