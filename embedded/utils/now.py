from datetime import datetime
import pytz

def now():
    """
    Returns the current time in the US/Central timezone.
    """
    current_time = datetime.now()
    tz = pytz.timezone("US/Central")

    return current_time.replace(tzinfo=tz)