import datetime
import logging
import os
import signal
import sys
import time
import traceback

from threading import Event
from config import Config
from utils import SocketConnector, now


from devices import TempSensor, RelayDevice
from utils import Database
from utils.reading import Reading


LOGGER = logging.getLogger()

# log inline format and date format
LOG_FORMAT = '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'

# log format
LOG_FORMATTER = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

# log level
LOGGER.setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

LOG_FILE_HANDLER = None
def update_log_file():
    """
    Updates the current log file name to the current date.
    """
    global LOG_FILE_HANDLER, LOG_FORMATTER

    if(not os.path.exists("logs")):
        os.mkdir("logs")

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
        self.config = Config(config_file)

        LOGGER.debug("Starting service.")

        # terminate event
        self.term = Event()

        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)

        self.init_devices()

    def exit_handler(self, sig, frame):
        LOGGER.info("Exiting Session")
        if self.heater: self.heater.on()
        if self.humidifier: self.humidifier.off()
        if self.lamp: self.lamp.off()
        if self.dht: self.dht.terminate()
        self.term.set()

    def init_devices(self):
        """
        Initializes the database connection and all GPIO devices.
        """

        self.database = Database(self.config)

        self.heater = RelayDevice(self.config.heater_gpio, self.database, name = "Heating Pad", normally_closed = True)

        self.lamp = RelayDevice(self.config.lamp_gpio, self.database, name = "Lamp", normally_closed = False)

        self.humidifier = RelayDevice(self.config.humidifier_gpio, self.database, name = "Humidifier", normally_closed = False)

        self.dht = TempSensor(self.config.dht_gpio, self.database, buffer_duration=self.config.buffer_dur)

    def begin_reading(self):
        """
        Starts a thread to start reading data from the DHT sensor.
        This waits for the sensor to to fully available before returning.

        NOTE: Is blocking if the sensor is unresponsive.
        """
        self.dht.start()

        LOGGER.info("Waiting for self.dht readings..")
        while not self.dht.available() and not self.term.is_set():
            self.term.wait(0.1)

    def start(self):
        """
        Starts the main service thread.
        """
        self.begin_reading()

        LOGGER.info("Starting main loop.")

        last_hardware_update = time.time()
        last_db_update = time.time()

        while not self.term.is_set():

            update_log_file()

            reading = self.dht.get_avg()
            if reading is None or reading.temp is None or reading.hum is None:
                LOGGER.error("ERROR: Failed to read averages from sensor.")
                self.term.wait(60)
                continue

            LOGGER.info(f"{reading}   -   Heater: {self.heater.is_on()}   -   Lamp: {self.lamp.is_on()}")
            LOGGER.debug(f"DHT Reading Buffer: {[str(r) for r in self.dht.get_buffer()]}")

            # only update hardware every hardware_interval seconds
            if time.time() - last_hardware_update > self.config.hardware_interval:
                last_hardware_update = time.time()
                self.update_devices(reading)

            if time.time() - last_db_update > self.config.db_interval:
                last_db_update = time.time()
                self.dht.send_to_database(reading)

            # update database every minute
            self.term.wait(60)

        LOGGER.info("Exited main loop.")


    def update_devices(self, reading: Reading):
        """
        Updates power state of heating and humidity devices.

        During daytime hours the lamp is prioritized as a heating device.
        At night, only the heat mat is used.

        Args:
            reading (Reading): Reading object to get environment data from.
        """
        temp = reading.temp
        hum = reading.hum

        # run thermostat checks
        current_hour = datetime.datetime.now().hour
        is_daytime = current_hour > self.config.day_start and current_hour < self.config.day_end

        # forces lamp to be off at night
        if not is_daytime:
            self.lamp.off()

        if temp < self.config.desired_temp - self.config.temp_range:
            if is_daytime:
                # if the lamp is not on, turn it on first.
                # If its still too cold on next check, turn on heater
                if not self.lamp.is_on():
                    self.lamp.on()
                else:
                    self.heater.on()
            else:
                self.heater.on()

        if temp > self.config.desired_temp + self.config.temp_range:
            if is_daytime:
                # if the heater is on, turn it off first.
                # If its still too hot on next check, turn off lamp
                if self.heater.is_on():
                    self.heater.off()
                else:
                    self.lamp.off()
            else:
                self.heater.off()


        if hum < self.config.desired_hum-self.config.hum_range and not hum < 0 and not hum > 100:
            self.humidifier.on_timed(self.config.spray_dur)

if __name__ == "__main__":
    service = Service("config.ini")
    service.start()
