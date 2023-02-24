import logging

from .reading import Reading
from .now import now

LOGGER = logging.getLogger()

class ReadingBuffer:

    def __init__(self, duration: int):
        """
        This class holds a list containing `Reading` objects. If an entry is older than `duration` seconds,
        it is removed automatically. Therefore all entries in the list stay within the last `duration` seconds.

        All methods that add or retrieve from this list automatically clean out old entries before returning.

        Args:
            duration (int): Amount of time that the entries should span, in seconds.
        """
        self.duration = duration
        self.list: list[Reading] = []

    def all(self):
        """
        Returns all readings in the queue.

        Returns:
            list[Reading]: All reading objects.
        """
        self.remove_old_entries()
        return self.list

    def append(self, reading: Reading):
        """
        Adds a reading to the queue.

        Args:
            reading (Reading): The reading to add to the queue.
        """
        entry = now() if reading is None else reading
        self.remove_old_entries()
        self.list.append(entry)

    def remove_old_entries(self):
        """
        Removes all entries that are older than `self.duration` seconds.
        """
        if len(self.list) == 0:
            return

        for reading in self.list:
            if (now() - reading.time).total_seconds() > self.duration:
                self.list.remove(reading)

    def latest(self):
        """
        Returns latest reading.
        """
        self.remove_old_entries()
        if len(self.list) > 0:
            return self.list[-1]
        return None

    def oldest(self):
        """
        Returns oldest reading.
        """
        self.remove_old_entries()
        if len(self.list) > 0:
            return self.list[0]
        return None

    def toList(self):
        """
        Returns this all readings as a list.
        """
        return self.all()

    def __len__(self):
        return len(self.all())

    def __iter__(self):
        return iter(self.all())