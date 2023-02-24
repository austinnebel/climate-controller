from datetime import datetime
from .now import now


class Reading:
    def __init__(self, temp: int, hum: int, time: datetime = None, is_fahrenheit = False, convert = True):
        """
         Holds temperature and humidity data, as well as the time of data capture.

        Args:
            temp (float): Temperature.
            hum (float): Humidity percentage.
            time (datetime): If present, will set this objects timestamp.
            is_fahrenheit (bool, optional): If True, `temp` will be treated as a Fahrenheit measurement.
                Otherwise, it will be treated as a Celsius measurement.
            convert (bool, optional): If True, will convert `temp` to Celsius if `is_fahrenheit` is true.
                If `is_fahrenheit` is false, `temp` will be converted to Celsius.
                If false, no conversion will take place.
        """
        self.temp = temp
        self.hum = hum
        self.time = now() if time is None else time
        self.is_fahrenheit = is_fahrenheit

        if self.temp != None:
            if convert:
                self.convert()
            self.temp = round(self.temp, 2)
        if self.hum != None:
            self.hum = round(hum, 2)

    def convert(self):
        """
        Converts between Celsius and Fahrenheit units.
        """
        if self.temp is None:
            return

        if self.is_fahrenheit:
            self.convert_to_celsius()
        else:
            self.convert_to_fahrenheit()

    def convert_to_fahrenheit(self):
        """
        Converts the current temperature into fahrenheit units.
        """
        self.temp = round((self.temp * 9/5) + 32, 2)
        self.is_fahrenheit = True

    def convert_to_celsius(self):
        """
        Converts the current temperature into celsius units.
        """
        self.temp = round((self.temp - 32) * (5/9), 2)
        self.is_fahrenheit = False

    def to_dict(self):
        """
        Converts this reading into a JSON-compatible dictionary.
        """
        return {
            "temperature": self.temp,
            "humidity": self.hum,
            "time": str(self.time)
        }

    def __str__(self):
        if self.temp == None or self.hum == None:
            return "Read error."

        unit = "F" if self.is_fahrenheit else "C"
        return f"{self.temp}°{unit} {self.hum}% {self.time.strftime('%H:%M:%S')}"

