import configparser
import logging
from threading import Thread
from time import sleep
from devices import TempSensor, Heater, Humidifier

LOGGER = logging.getLogger()

def main(config):

    DESIRED_TEMP = config.getint("RANGES", "desired_temp")
    DESIRED_HUM = config.getint("RANGES", "desired_humidity")
    TEMP_RANGE = config.getint("RANGES", "temp_range")
    HUM_RANGE = config.getint("RANGES", "humidity_range")

    heater_gpio = config.getint("GPIO", "heater")
    humidity_gpio = config.getint("GPIO", "heater")
    dht22_gpio = config.getint("GPIO", "dht22")

    HEATER = Heater(heater_gpio)
    HUMIDIFIER = Humidifier(humidity_gpio)
    DHT = TempSensor(dht22_gpio, buffer_size=15)

    while True:
        #get temp, convert to fahrenheit
        temp, hum = DHT.get_readings()

        if temp is None:
            print("ERROR: Can't read sensor.")
            continue
        else:
            LOGGER.info("{:3.1f}'F  {:3.1f}%".format(temp, hum))

        if not HEATER.is_on and temp < DESIRED_TEMP-TEMP_RANGE:
            HEATER.on()
        if HEATER.is_on and temp > DESIRED_TEMP+TEMP_RANGE:
            HEATER.off()

        if hum < DESIRED_HUM-HUM_RANGE and not hum < 0 and not hum > 100:
            HUMIDIFIER.spray()

        sleep(2)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    main()