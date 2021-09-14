import configparser
import datetime
import logging
import sys
from threading import Thread
from time import sleep
from devices import TempSensor, Heater, Humidifier


LOGGER = logging.getLogger()
LOGFILE = 'logs/%s.log' % (str(datetime.datetime.today()).split()[0])
log_format = f'%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s'
log_date_format = '%H:%M:%S'
logging.basicConfig(filename=LOGFILE, level=logging.INFO, format=log_format, datefmt=log_date_format)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(log_format, datefmt=log_date_format))
handler.setLevel(logging.INFO)
LOGGER.addHandler(handler)

def main(config):

    DESIRED_TEMP = config.getint("THERMOSTAT", "desired_temp")
    DESIRED_HUM = config.getint("THERMOSTAT", "desired_humidity")
    TEMP_RANGE = config.getint("THERMOSTAT", "temp_range")
    HUM_RANGE = config.getint("THERMOSTAT", "humidity_range")
    BUFFER_SIZE = config.getint("THERMOSTAT", "buffer_size")

    heater_gpio = config.getint("GPIO", "heater")
    humidity_gpio = config.getint("GPIO", "humidifier")
    dht22_gpio = config.getint("GPIO", "dht22")

    HEATER = Heater(heater_gpio)
    HUMIDIFIER = Humidifier(humidity_gpio)
    DHT = TempSensor(dht22_gpio, buffer_size=BUFFER_SIZE)

    DHT.start()

    while not DHT.get_readings():
        sleep(0.1)

    print("Starting")
    while True:
        #get temp, convert to fahrenheit
        reading = DHT.get_readings()
        temp = reading.temp
        hum = reading.hum

        if temp is None:
            print("ERROR: Can't read sensor.")
            continue
        else:
            LOGGER.info(reading)

        if not HEATER.is_on and temp < DESIRED_TEMP-TEMP_RANGE:
            HEATER.on()
        if HEATER.is_on and temp > DESIRED_TEMP+TEMP_RANGE:
            HEATER.off()

        if hum < DESIRED_HUM-HUM_RANGE and not hum < 0 and not hum > 100:
            HUMIDIFIER.spray(15)

        sleep(60)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    main(config)