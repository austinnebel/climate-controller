import logging
import datetime
import Adafruit_DHT

from threading import Thread, Event
from embedded.utils.uploader import Database, SocketConnector

from utils import Reading

LOGGER = logging.getLogger()

class TempSensor(Thread):

    def __init__(self, pin: int, db: Database, sock: SocketConnector, use_fahrenheit = True, buffer_duration = 30):
        """
        Continuously captures temperature and humidity data from DHT22. This class
        can be instantiated, and then run as a thread using its run() method.

        Args:
            pin (int): GPIO data pin for DHT sensor.
            db (Database): `Database` object to use to publish data.
            sock (SocketConnector): `SocketConnector` object to use to post real-time data.
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
        self.db = db
        self.sock = sock
        self.term = Event()

    def available(self):
        """
        Returns true if the data buffer is full of data.
        """
        return len(self.reading_buff.all()) > 0

    def get_avg(self):
        """
        Returns a `Reading` object containing the average values of all Readings stored in the buffer.
        The returned time value will be the time value stored in the most recent reading.

        Returns:
            Reading, None: Reading object if readings are available in the buffer. False otherwise.
        """
        # toList creates shallow copy to prevent threads from modifying during iteration
        buff = self.reading_buff.toList()
        buff_size = len(buff)

        if buff_size > 0:
            latest = buff[-1]
            t_avg = sum([r.temp for r in buff])/buff_size
            h_avg = sum([r.hum for r in buff])/buff_size

            return Reading(t_avg, h_avg, time = latest.time, convert = False, repr_fahrenheit = self.use_fahrenheit)
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
        """
        Posts data in Reading object to database.

        Args:
            reading (Reading): Reading object to store.
        """
        json = {
                "temperature": reading.temp,
                "humidity": reading.hum,
                "time": str(reading.time)
            }
        self.db.send_data(json)

    def publish_data(self, reading : Reading):
        """
        Publishes data to a real-time socket.

        Args:
            reading (Reading): Reading object to publish.
        """
        json = {
            "temperature": reading.temp,
            "humidity": reading.hum,
            "time": str(reading.time)
        }
        self.sock.send(json)

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
                self.publish_data(self.get_avg())
            except Exception as e:
                LOGGER.error(f"Error reading from DHT22: {str(e)}")
            # dht sensors need a minimum of 2 seconds between readings
            self.term.wait(2)

    def terminate(self):
        """
        Stops this threads run() method.
        """
        self.term.set()



