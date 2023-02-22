
import configparser

class Config:

    def __init__(self, file: str):
        self.load(file)

    def load(self, file: str):
        config = configparser.ConfigParser()
        config.read(file)

        # thermostat settings

        self.desired_temp = config.getint("THERMOSTAT", "desired_temp")
        """ The desired temperature levels in Fahrenheit. """

        self.desired_hum = config.getint("THERMOSTAT", "desired_humidity")
        """ The desired humidity level, from 0 to 100. """

        self.temp_range = config.getint("THERMOSTAT", "temp_range")
        """ Acceptable range from `desired_temp` before a heater is activated. """

        self.hum_range = config.getint("THERMOSTAT", "humidity_range")
        """ Acceptable range from `desired_hum` before humidifier is activated. """

        self.buffer_dur = config.getint("THERMOSTAT", "buffer_duration")
        """ How many readings to store in a buffer for calculating averages. """

        self.spray_dur = config.getint("THERMOSTAT", "spray_duration")
        """ How long to spray the humidifier for. """

        self.hardware_interval = config.getint("THERMOSTAT", "hardware_interval")
        """ Minimum amount of time to wait between updating hardware power status. """

        # schedule settings

        self.day_start = config.getint("SCHEDULE", "day_start")
        """ What time to consider daytime, in military hours. """

        self.day_end = config.getint("SCHEDULE", "day_end")
        """ What time to consider nighttime, in military hours. """

        # server settings

        self.server_hostname = config.get("SERVER", "server_hostname")
        """ Hostname of the server. """

        self.server_port = config.get("SERVER", "server_port")
        """ Port of the server. """

        self.socket_endpoint = config.get("SERVER", "socket_endpoint")
        """ Websocket endpoint. """

        self.db_interval = config.getint("SERVER", "data_update_interval")
        """ How often to update the server climate information. """

        self.device_endpoint = config.get('SERVER', 'device_endpoint')
        """ Server endpoint used to post device information. """

        self.climate_endpoint = config.get('SERVER', 'climate_endpoint')
        """ Server endpoint used to post climate information. """

        # gpio settings

        self.heater_gpio = config.getint("GPIO", "heater")
        """ The GPIO pin controlling the heater, in BCM. """

        self.humidifier_gpio = config.getint("GPIO", "humidifier")
        """ The GPIO pin controlling the humidifier, in BCM. """

        self.lamp_gpio = config.getint("GPIO", "lamp")
        """ The GPIO pin controlling the lamp, in BCM. """

        self.dht_gpio = config.getint("GPIO", "dht22")
        """ The GPIO pin reading from the DHT22 sensor, in BCM. """
