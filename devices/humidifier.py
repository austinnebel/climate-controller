import logging
from datetime import datetime as dt
from time import sleep
from threading import Thread
from .relay import Relay

LOGGER = logging.getLogger()

class Humidifier:

    def __init__(self, pin, graph_duration):
        """
        Class to control humidifer device.

        Args:
            pin (int): GPIO pin used to activate humidifier.
            graph_duration (int): Amount of time that the entries in spray_times should span.
        """
        # humidifier should default to off
        self.relay = Relay(pin, normally_closed = False)
        self.graph_duration = graph_duration
        self.spray_times = []

    def clean_spray_times(self):
        """
        Removes all spray times that are older than self.graph_duration seconds.
        """
        if len(self.spray_times) > 0:
            now = dt.now()
            for t in self.spray_times:
                if (now - t).total_seconds() > self.graph_duration:
                    self.spray_times.remove(t)

    def get_spray_times(self):
        """
        Returns list of spray times.

        Returns:
            list[datetime]: List of datetime objects.
        """
        self.clean_spray_times()
        return self.spray_times

    def add_spray(self):
        """
        Adds a time entry to self.spray_times.
        """
        now = dt.now()
        self.spray_times.append(now)
        self.clean_spray_times()

    def last_spray(self):
        """
        Returns last recorded spray time.

        Returns:
            datetime: Last spray time.
        """
        if len(self.spray_times) > 0:
            return self.spray_times[-1]

    def is_on(self):
        return self.relay.is_on()

    def on(self):
        if not self.is_on():
            LOGGER.info("Activating Humidifier.")
            self.relay.on()

    def off(self):
        if self.is_on():
            LOGGER.info("Deactivating Humidifier.")
            self.relay.off()

    def _spray(self, spray_time):
        self.on()
        sleep(spray_time)
        self.off()

    def spray(self, spray_time):
        """
        Sprays the humidifer for spray_time seconds.
        """
        LOGGER.info(f"Spraying humidifier for {spray_time} seconds.")
        t = Thread(target = self._spray, args = [spray_time])
        t.start()
        self.add_spray()
