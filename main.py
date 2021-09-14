import configparser
import datetime
import logging
import signal
import sys
from threading import Thread, Event
from time import sleep
from devices import TempSensor, Heater, Humidifier
from server import Server


LOGGER = logging.getLogger()

# log inline format and date format
LOG_FORMAT = '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'

LOG_FILE_HANDLER = None
def update_log_file(self, log_file_handler):
    """
    Updates the current log file name to the current date.
    """
    if log_file_handler != None: LOGGER.removeHandler(self.log_file_handler)
    log_file_handler = logging.FileHandler(f"logs/{datetime.datetime.now().date()}.log", mode='a')
    log_file_handler.setFormatter(self.log_formatter)
    log_file_handler.setLevel(logging.DEBUG)
    LOGGER.addHandler(self.log_file_handler)

def log_exception_handler(e_type, value, tb):
    """
    Allows for exceptions to be logged before interupting the program.
    """
    message = f"{e_type.__name__}: {value}\n{''.join(str(line) for line in sys.tracebacklimit.format_tb(tb))}"
    LOGGER.critical(message)
sys.excepthook = log_exception_handler

# log level
LOGGER.setLevel(logging.DEBUG)

# log format
LOG_FORMATTER = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

# stdout logging
log_stdout_handler = logging.StreamHandler(sys.stdout)
log_stdout_handler.setFormatter(LOG_FORMATTER)
log_stdout_handler.setLevel(logging.DEBUG)
LOGGER.addHandler(log_stdout_handler)


def main(config):

    TERM = Event()

    DESIRED_TEMP = config.getint("THERMOSTAT", "desired_temp")
    DESIRED_HUM = config.getint("THERMOSTAT", "desired_humidity")
    TEMP_RANGE = config.getint("THERMOSTAT", "temp_range")
    HUM_RANGE = config.getint("THERMOSTAT", "humidity_range")
    BUFFER_SIZE = config.getint("THERMOSTAT", "buffer_size")

    PORT = config.getint("SERVER", "port")

    heater_gpio = config.getint("GPIO", "heater")
    humidity_gpio = config.getint("GPIO", "humidifier")
    dht22_gpio = config.getint("GPIO", "dht22")

    HEATER = Heater(heater_gpio)
    HUMIDIFIER = Humidifier(humidity_gpio)
    DHT = TempSensor(dht22_gpio, buffer_size=BUFFER_SIZE)

    def exit_handler(sig, frame):
        LOGGER.info("Exiting Session")
        if HEATER: HEATER.on()
        if HUMIDIFIER: HUMIDIFIER.off()
        if DHT: DHT.terminate()
        TERM.set()
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    DHT.start()

    LOGGER.info("Waiting for DHT readings..")
    while not DHT.get_readings() and not TERM.is_set():
        TERM.wait(0.1)

    SERVER = Server(DHT, HEATER, HUMIDIFIER, PORT)
    SERVER.start()

    LOGGER.info("Starting main loop.")
    while not TERM.is_set():

        update_log_file(LOG_FILE_HANDLER)

        # get moving average of temp and humidity
        reading = DHT.avg
        temp = reading.temp
        hum = reading.hum

        if temp is None:
            LOGGER.error("ERROR: Can't read sensor.")
            continue
        else:
            LOGGER.info(f"{reading}   -   Heater: {HEATER.is_on()}   -   Humidifier: {HUMIDIFIER.is_on()}")

        LOGGER.debug(f"Buffer: {[str(r) for r in DHT.get_buffers()]}")

        if not HEATER.is_on() and temp < DESIRED_TEMP-TEMP_RANGE:
            HEATER.on()
        if HEATER.is_on() and temp > DESIRED_TEMP+TEMP_RANGE:
            HEATER.off()

        if hum < DESIRED_HUM-HUM_RANGE and not hum < 0 and not hum > 100:
            HUMIDIFIER.spray(15)

        TERM.wait(60)

    LOGGER.info("Exit successfull.")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    main(config)