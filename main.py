import configparser
import datetime
import logging
import signal
import sys
from threading import Event
import time
import traceback
from devices import TempSensor, Heater, Humidifier
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


def main(config):

    LOGGER.debug("Starting service.")

    # terminate event
    TERM = Event()

    # general settings
    UPDATE_TIME = config.getint("GENERAL", "update_time")
    GRAPH_DURATION = config.getint("GENERAL", "graph_duration") * 60

    # thermostat settings
    DESIRED_TEMP = config.getint("THERMOSTAT", "desired_temp")
    DESIRED_HUM = config.getint("THERMOSTAT", "desired_humidity")
    TEMP_RANGE = config.getint("THERMOSTAT", "temp_range")
    HUM_RANGE = config.getint("THERMOSTAT", "humidity_range")
    BUFFER_DUR = config.getint("THERMOSTAT", "buffer_duration")
    SPRAY_DUR = config.getint("THERMOSTAT", "spray_duration")

    # schedule settings
    DAY_START = config.getint("SCHEDULE", "day_start")
    DAY_END = config.getint("SCHEDULE", "day_end")

    # server settings
    PORT = config.getint("SERVER", "port")
    GRAPH_LOCATION = config.get("SERVER", "graph_location")

    # gpio settings
    HEATER_GPIO = config.getint("GPIO", "heater")
    HUMIDITY_GPIO = config.getint("GPIO", "humidifier")
    LAMP_GPIO = config.getint("GPIO", "lamp")
    DHT_GPIO = config.getint("GPIO", "dht22")

    # initialize devices
    HEATER = Heater(HEATER_GPIO, name = "Heating Pad", normally_closed = True)
    LAMP = Heater(LAMP_GPIO, name = "Lamp", normally_closed = False)
    HUMIDIFIER = Humidifier(HUMIDITY_GPIO, GRAPH_DURATION)
    DHT = TempSensor(DHT_GPIO, buffer_duration=BUFFER_DUR)

    def exit_handler(sig, frame):
        LOGGER.info("Exiting Session")
        if HEATER: HEATER.on()
        if HUMIDIFIER: HUMIDIFIER.off()
        if LAMP: LAMP.off()
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

        if temp is None or hum is None:
            LOGGER.error("ERROR: Can't read sensor.")
            continue
        else:
            LOGGER.info(f"{reading}   -   Heater: {HEATER.is_on()}   -   Humidifier: {HUMIDIFIER.last_spray()}")

        LOGGER.debug(f"Buffer: {[str(r) for r in DHT.get_buffers()]}")

        # make sure plot_points only keeps data recorded within roughly the last GRAPH_DURATION minutes
        if len(plot_points) >= GRAPH_DURATION/UPDATE_TIME:
            plot_points.pop(0)
        plot_points.append(reading)

        # generate new graphs, and updated HTML page
        generate_graphs(plot_points, HUMIDIFIER.get_spray_times(), GRAPH_LOCATION)


        current_hour = datetime.datetime.now().hour

        # run thermostat checks
        is_daytime = current_hour > DAY_START and current_hour < DAY_END
        print(temp)
        print(DESIRED_TEMP)
        print(TEMP_RANGE)
        print(temp < DESIRED_TEMP-TEMP_RANGE)
        print(is_daytime)
        print(current_hour)
        if temp < DESIRED_TEMP-TEMP_RANGE:
            # only use heat lamp during daytime hours. If not daytime, use heat pad
            if is_daytime:
                LAMP.on()
            else:
                LAMP.off()
                HEATER.on()
        if temp > DESIRED_TEMP+TEMP_RANGE:
            HEATER.off()
            LAMP.off()

        if hum < DESIRED_HUM-HUM_RANGE and not hum < 0 and not hum > 100:
            HUMIDIFIER.spray(SPRAY_DUR)

        # wait UPDATE_TIME seconds, subtracting execution time of loop
        TERM.wait(UPDATE_TIME-(time.time()-s))

    LOGGER.info("Exited main loop.")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    main(config)
