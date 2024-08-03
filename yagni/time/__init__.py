from datetime import datetime, timezone


def now_utc():
    """
    This function is a drop-in replacement for datetime.utcnow that returns a timezone-aware datetime object.

    When working with time-critical applications, it is important to be aware of the limitations of the datetime.utcnow function.

    Motivation: https://aaronoellis.com/articles/python-datetime-utcnow-considered-harmful
    """
    return datetime.now(tz=timezone.utc)
