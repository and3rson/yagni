import datetime


def now_utc():
    """
    This function is a drop-in replacement for datetime.utcnow that returns a timezone-aware datetime object.

    When working with time-critical applications, it is important to be aware of the limitations of the datetime.utcnow function.
    Specifically, datetime.utcnow returns a timezone-naive datetime object.
    ``now_utc``, on the other hand, returns a timezone-aware datetime object with the UTC timezone.

    Motivation: https://aaronoellis.com/articles/python-datetime-utcnow-considered-harmful

    >>> from freezegun import freeze_time
    >>> with freeze_time("2021-01-01 00:00:00"):
    ...     # Timezone-naive... Might not be what you want.
    ...     print(datetime.datetime.utcnow())
    2021-01-01 00:00:00
    >>> with freeze_time("2021-01-01 00:00:00"):
    ...     # Timezone-aware!
    ...     print(now_utc())
    2021-01-01 00:00:00+00:00
    """
    return datetime.datetime.now(tz=datetime.timezone.utc)
