import configparser
import datetime
import logging
import signal
import sys
from threading import Event
import time
import traceback
from devices import TempSensor, RelayDevice
from utils import RotatingTimeList
from server import Server, generate_graphs


LOGGER = logging.getLogger()

# log inline format and date format
LOG_FORMAT = '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'

# log format
LOG_FORMATTER = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

# log level
LOGGER.setLevel(logging.DEBUG)

LOG_FILE_HANDLER = None
def update_log_file():
    """
    Updates the current log file name to the current date.
    """
    global LOG_FILE_HANDLER, LOG_FORMATTER
    if LOG_FILE_HANDLER != None: LOGGER.removeHandler(LOG_FILE_HANDLER)
    LOG_FILE_HANDLER = logging.FileHandler(f"logs/{datetime.datetime.now().date()}.log", mode='a')
    LOG_FILE_HANDLER.setFormatter(LOG_FORMATTER)
    LOG_FILE_HANDLER.setLevel(logging.DEBUG)
    LOGGER.addHandler(LOG_FILE_HANDLER)

def log_exception_handler(e_type, value, tb):
    """
    Allows for exceptions to be logged before interupting the program.
    """
    message = f"{e_type.__name__}: {value}\n{''.join(str(line) for line in traceback.format_tb(tb))}"
    LOGGER.critical(message)
sys.excepthook = log_exception_handler

# stdout logging
log_stdout_handler = logging.StreamHandler(sys.stdout)
log_stdout_handler.setFormatter(LOG_FORMATTER)
log_stdout_handler.setLevel(logging.DEBUG)
LOGGER.addHandler(log_stdout_handler)

class Service:

    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()

        LOGGER.debug("Starting service.")

        # terminate event
        self.term = Event()

        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)

        self.plot_points = RotatingTimeList(self.graph_duration)

        self.init_devices()

    def exit_handler(self, sig, frame):
        LOGGER.info("Exiting Session")
        if self.heater: self.heater.on()
        if self.humidifier: self.humidifier.off()
        if self.lamp: self.lamp.off()
        if self.dht: self.dht.terminate()
        self.term.set()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        # general settings
        self.update_time = config.getint("GENERAL", "update_time")
        self.graph_duration = config.getint("GENERAL", "graph_duration") * 60

        # thermostat settings
        self.desired_temp = config.getint("THERMOSTAT", "desired_temp")
        self.desired_hum = config.getint("THERMOSTAT", "desired_humidity")
        self.temp_range = config.getint("THERMOSTAT", "temp_range")
        self.hum_range = config.getint("THERMOSTAT", "humidity_range")
        self.buffer_dur = config.getint("THERMOSTAT", "buffer_duration")
        self.spray_dur = config.getint("THERMOSTAT", "spray_duration")

        # schedule settings
        self.day_start = config.getint("SCHEDULE", "day_start")
        self.day_end = config.getint("SCHEDULE", "day_end")

        # server settings
        self.server_port = config.getint("SERVER", "port")
        self.graph_location = config.get("SERVER", "graph_location")

        # gpio settings
        self.heater_gpio = config.getint("GPIO", "heater")
        self.humidifier_gpio = config.getint("GPIO", "humidifier")
        self.lamp_gpio = config.getint("GPIO", "lamp")
        self.dht_gpio = config.getint("GPIO", "dht22")

    def init_devices(self):
        # initialize devices
        self.heater = RelayDevice(self.heater_gpio, self.graph_duration, name = "Heating Pad", normally_closed = True)
        self.lamp = RelayDevice(self.lamp_gpio, self.graph_duration, name = "Lamp", normally_closed = False)
        self.humidifier = RelayDevice(self.humidifier_gpio, self.graph_duration, name = "Humidifier", normally_closed = False)
        self.dht = TempSensor(self.dht_gpio, buffer_duration=self.buffer_dur)

    def begin_reading(self):
        """
        Starts a thread to start reading data from the DHT sensor.

        NOTE: Is blocking if the sensor is unresponsive.
        """
        self.dht.start()

        LOGGER.info("Waiting for self.dht readings..")
        while not self.dht.available() and not self.term.is_set():
            self.term.wait(0.1)

    def get_reading(self):
        """
        Returns the average temperature and humidity from the DHT.

        Returns:
            tuple: Tuple of data, in the form (temp, humidity)
        """
        reading = self.dht.avg
        return reading.temp, reading.hum

    def start_html_server(self):
        """
        Starts the HTML server.
        """
        self.server = Server(self.dht, self.heater, self.humidifier, self.server_port)
        self.server.start()

    def start(self):
        """
        Starts the main service thread.
        """
        self.begin_reading()
        self.start_html_server()

        LOGGER.info("Starting main loop.")
        while not self.term.is_set():
            s = time.time()

            update_log_file()

            reading = self.dht.get_avg()
            temp, hum = (reading.temp, reading.hum)
            if temp is None or hum is None:
                LOGGER.error("ERROR: Failed to read sensor.")
                continue

            self.plot_points.append(reading)

            LOGGER.info(f"{reading}   -   Heater: {self.heater.is_on()}   -   Lamp: {self.lamp.is_on()}")
            LOGGER.debug(f"DHT Reading Buffer: {[str(r) for r in self.dht.get_buffer()]}")
            LOGGER.debug(f"Graph Point Buffer: {[str(r) for r in self.plot_points.all()]}")

            self.update_devices(reading)
            self.graph_data(self.plot_points.all())

            # wait self.update_time seconds, subtracting execution time of loop
            self.term.wait(self.update_time-(time.time()-s))

        LOGGER.info("Exited main loop.")

    def graph_data(self, data_points):
        """
        Graphs climate data to a png file.

        Args:
            data_points (list): List of Reading objects to plot in a graph.
        """
        generate_graphs(data_points, self.heater, self.lamp, self.humidifier, self.graph_location)

    def update_devices(self, reading):
        """
        Updates power state of heating and humidity devices.

        Args:
            reading (Reading): Reading object to get environment data from.
        """
        temp = reading.temp
        hum = reading.hum

        # run thermostat checks
        current_hour = datetime.datetime.now().hour
        is_daytime = current_hour > self.day_start and current_hour < self.day_end

        if temp < self.desired_temp-self.temp_range:
            if is_daytime:
                self.lamp.on()
            else:
                self.lamp.off()
                self.heater.on()
        if temp > self.desired_temp+self.temp_range:
            self.heater.off()
            self.lamp.off()

        if hum < self.desired_hum-self.hum_range and not hum < 0 and not hum > 100:
            self.humidifier.on_timed(self.spray_dur)

if __name__ == "__main__":
    service = Service("config.ini")
    service.start()
