import logging

from threading import Thread, Event
from utils import Reading, Database, SocketConnector
from conditional_dependencies.adafruit_dht import Adafruit_DHT

LOGGER = logging.getLogger()

class TempSensor(Thread):

    def __init__(self, pin: int, db: Database, use_fahrenheit = True, buffer_duration = 30):
        """
        Continuously captures temperature and humidity data from DHT22. This class
        can be instantiated, and then run as a thread using its run() method.

        Args:
            pin (int): GPIO data pin for DHT sensor.
            db (Database): `Database` object to use to publish data.
            use_fahrenheit (bool, optional): If True, uses fahrenheit units, else uses Celsius. Defaults to True.
            buffer_duration (int, optional): How many seconds of history should be contained in the reading buffer. Defaults to 30.
        """
        Thread.__init__(self)
        from utils import ReadingBuffer

        self.daemon = True
        """
        Sets this thread in `daemon` mode. This makes the thread forcibly
        shutdown when no non-daemon threads are left. See more: https://docs.python.org/3/library/threading.html#thread-objects
        """

        self.sensor = Adafruit_DHT.DHT22
        """ The `DHT22` sensor object."""

        self.pin = pin
        """ The GPIO pin used to read from the sensor."""

        self.reading_buff = ReadingBuffer(buffer_duration)
        """ A reading buffer that will only hold readings that are less than `buffer_duration` old. """

        self.use_fahrenheit = use_fahrenheit
        """ If true, Celsius readings are converted to fahrenheit. """

        self.db = db
        """ Database instance to send data to. """

        self.term = Event()
        """ Used to terminate this thread. """

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

            return Reading(t_avg, h_avg, time = latest.time, convert = False, is_fahrenheit=True)
        return None

    def add_to_buffer(self, reading : Reading):
        """
        Adds a Reading object to the reading buffer. If the Reading, its temperature or its humidity is None,
        no entry is added, but the buffer is cleaned to avoid old entries from not being removed.

        Args:
            reading (Reading): Reading object captured from sensor.
        """
        if reading is None or reading.temp is None or reading.hum is None:
            self.reading_buff.remove_old_entries()
            return
        self.reading_buff.append(reading)

    def send_to_database(self, reading : Reading):
        """
        Sends a Reading object to the backend database for storage.

        Args:
            reading (Reading): Reading object to send.
        """
        self.db.send_climate_data(reading.to_dict())

    def send_to_websocket(self, reading : Reading):
        """
        Sends a Reading object to the backend database's websocket.

        Args:
            reading (Reading): Reading object to send.
        """
        self.db.send_climate_data_websocket(reading.to_dict())

    def get_buffer(self):
        """
        Returns all values in the buffer.

        Returns:
            RotatingTimeList: List of captured `Reading` entries.
        """
        return self.reading_buff

    def read(self):
        """
        Reads from the DHT sensor.

        Returns:
            Reading: Reading object containing the captured data.
        """
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            humidity = round(humidity, 2)
            temperature = round(temperature, 2)
            return Reading(temperature, humidity, convert = self.use_fahrenheit, is_fahrenheit=False)
        else:
            LOGGER.error(f"Failed to read sensor. Sensor returned {temperature}, {humidity}.")
            return None

    def run(self):
        """
        Continuously reads from sensor every 2 seconds.
        Runs indefinitely until terminate() is called.
        """
        while not self.term.is_set():

            try:
                reading = self.read()
                average = self.get_avg()
            except Exception as e:
                LOGGER.error(f"Error reading from DHT22: {str(e)}")
                self.term.wait(2)
                continue

            try:
                self.add_to_buffer(reading)
                self.send_to_websocket(average)
            except Exception as e:
                LOGGER.error(f"Error sending data to database: {str(e)}")

            # dht sensors need a minimum of 2 seconds between readings
            self.term.wait(2)

    def terminate(self, sig, frame):
        """
        Stops this thread.
        """
        print("Terminating temp sensor.")
        self.term.set()



