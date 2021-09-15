import configparser
import datetime
import logging
import signal
import sys
from threading import Thread, Event
from time import sleep
import time
import traceback
from devices import TempSensor, Heater, Humidifier
from server import Server, save_graph


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


def main(config):

    TERM = Event()

    # general settings
    UPDATE_TIME = config.getint("GENERAL", "update_time")
    GRAPH_DURATION = config.getint("GENERAL", "graph_duration")

    # thermostat settings
    DESIRED_TEMP = config.getint("THERMOSTAT", "desired_temp")
    DESIRED_HUM = config.getint("THERMOSTAT", "desired_humidity")
    TEMP_RANGE = config.getint("THERMOSTAT", "temp_range")
    HUM_RANGE = config.getint("THERMOSTAT", "humidity_range")
    BUFFER_DUR = config.getint("THERMOSTAT", "buffer_duration")

    # server settings
    PORT = config.getint("SERVER", "port")
    GRAPH_LOCATION = config.get("SERVER", "graph_location")

    HEATER_GPIO = config.getint("GPIO", "heater")
    HUMIDITY_GPIO = config.getint("GPIO", "humidifier")
    DHT_GPIO = config.getint("GPIO", "dht22")

    HEATER = Heater(HEATER_GPIO)
    HUMIDIFIER = Humidifier(HUMIDITY_GPIO)
    DHT = TempSensor(DHT_GPIO, buffer_duration=BUFFER_DUR)

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

    plot_points = []

    LOGGER.info("Starting main loop.")
    while not TERM.is_set():

        s = time.time()

        update_log_file()

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

        # make sure plot_points only keeps data recorded within roughly the last GRAPH_DURATION minutes
        if len(plot_points) >= (GRAPH_DURATION*60)/UPDATE_TIME:
            plot_points.pop(0)
        plot_points.append(reading)

        save_graph("Graph", plot_points, GRAPH_LOCATION)

        # run thermostat checks
        if temp < DESIRED_TEMP-TEMP_RANGE:
            HEATER.on()
        if temp > DESIRED_TEMP+TEMP_RANGE:
            HEATER.off()

        if hum < DESIRED_HUM-HUM_RANGE and not hum < 0 and not hum > 100:
            HUMIDIFIER.spray(15)

        # wait UPDATE_TIME seconds, subtracting execution time of loop
        TERM.wait(UPDATE_TIME-(time.time()-s))

    LOGGER.info("Exit successfull.")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    main(config)