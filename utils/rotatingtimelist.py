import logging

from .reading import Reading
from .now import now

LOGGER = logging.getLogger()

class RotatingTimeList:

    def __init__(self, duration):
        """
        This class holds a list containing time entries, with each entry being either a datetime
        object or a Reading object. If an entry is older than [duration] seconds, it is removed automatically.
        Therefore all entries in the list stay within the last [duration] seconds.

        All methods that add or retrieve from this list automatically clean out old entries before returning.

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
            curr_time = now()
            for t in self.list:
                entry_time = t.time if isinstance(t, Reading) else t
                if (curr_time - entry_time).total_seconds() > self.duration:
                    self.list.remove(t)
        return self.list

    def all(self):
        """
        Returns all entries.

        Returns:
            list[datetime]: List of datetime objects.
        """
        return self.clean()

    def append(self, time_entry = None):
        """
        Adds a time entry to self.list.

        Args:
            time_entry (Datetime, Reading): Optional. If not present, creates and appends a new datetime object.
        """
        entry = now() if time_entry is None else time_entry
        self.clean()
        self.list.append(entry)

    def latest(self):
        """
        Returns latest time entry.
        """
        self.clean()
        if len(self.list) > 0:
            return self.list[-1]
        return None

    def oldest(self):
        """
        Returns oldest time entry.
        """
        self.clean()
        if len(self.list) > 0:
            return self.list[0]
        return None

    def toList(self):
        return [i for i in self.all()]

    def __len__(self):
        return len(self.all())

    def __iter__(self):
        return iter(self.all())