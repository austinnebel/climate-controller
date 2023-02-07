from datetime import datetime
import pytz

def now():

    current_time = datetime.now()
    tz = pytz.timezone("US/Central")

    return current_time.replace(tzinfo=tz)