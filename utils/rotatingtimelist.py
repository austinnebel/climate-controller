from devices.tempsensor import Reading
import logging
from datetime import datetime as dt

LOGGER = logging.getLogger()

class RotatingTimeList:

    def __init__(self, duration):
        """
        This class holds a list containing time entries, with each entry being either a datetime
        object or a Reading object. If an entry is older than [duration] seconds, it is removed automatically.
        Therefore all entries in the list stay within the last [duration] seconds.


        Args:
            duration (int): Amount of time that the entries should span, in seconds.
        """
        self.duration = duration
        self.list = []

    def clean(self):
        """
        Removes all entries that are older than self.duration seconds.
        """
        if len(self.list) > 0:
            now = dt.now()
            for t in self.list:
                entry_time = t.time if isinstance(t, Reading) else t
                if (now - entry_time).total_seconds() > self.duration:
                    self.list.remove(t)
        return self.list

    def all(self):
        """
        Cleans old entries, then returns all entries.

        Returns:
            list[datetime]: List of datetime objects.
        """
        return self.clean()

    def append(self, time_entry = None):
        """
        Adds a time entry to self.list, then cleans old entries.

        Args:
            time_entry (Datetime, Reading): Optional. If not present, creates and appends a new datetime object.
        """
        entry = dt.now() if time_entry is None else time_entry
        self.list.append(entry)
        self.clean()

    def latest(self):
        """
        Returns latest time entry.
        """
        if len(self.list) > 0:
            return self.list[-1]
        return None

    def oldest(self):
        """
        Returns oldest time entry.
        """
        if len(self.list) > 0:
            return self.list[0]
        return None

    def __len__(self):
        return len(self.all())

    def __iter__(self):
        return iter(self.all())