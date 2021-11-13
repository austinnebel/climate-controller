from .now import now


class Reading:

    def __init__(self, temp, hum, time = None, convert = True, repr_fahrenheit = True):
        """
         Holds temperature and humidity data, as well as the time of data capture.

        Args:
            temp (float): Temperature.
            hum (float): Humidity percentage.
            time (datetime): If present, will set this objects timestamp.
            convert (bool): If True, will convert temp from Celsius to Fahrenheit.
            repr_fahrenheit (bool, optional): If True and convert is False, assumes that temp is already in Fahrenheit units.
                                              If True and convert is True, temp will be converted to Fahrenheit units.
                                              If False, temp will remain in Celsius.
        """
        self.repr_fahrenheit = repr_fahrenheit

        if temp != None:
            if convert and self.repr_fahrenheit:
                temp = (temp * 9/5) + 32
            temp = round(temp, 2)
        if hum != None:
            hum = round(hum, 2)

        self.temp = temp
        self.hum = hum
        self.time = now() if time is None else time

    def __str__(self):
        if self.temp == None or self.hum == None:
            return "Read error."

        unit = "F" if self.repr_fahrenheit else "C"
        return f"{self.temp}°{unit} {self.hum}% {self.time.strftime('%H:%M:%S')}"

