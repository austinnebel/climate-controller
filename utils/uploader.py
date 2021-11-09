import logging
import requests


LOGGER = logging.getLogger()

class Database():

    def __init__(self, url, user, password):
        """
        Utility for posting data to the local database server.
        """
        self.url = url
        self.user = user
        self.password = password

    def send_data(self, data, timeout = 5):

        try:
            r = requests.post(self.url, timeout = timeout, json = data, auth = (self.user, self.password))
        except Exception as e:
            LOGGER.error(f"Failed to update database. Error: {e}")
            return False
        if r.status_code == 201:
            LOGGER.debug(f"Database updated successfully with entry {data}")
            return True
        LOGGER.error(f"Database returned status code of {r.status_code}. Content: {r.content}")
        return False
