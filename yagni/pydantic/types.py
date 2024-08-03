"""
Custom Pydantic types (v1.x).
"""

from enum import Enum
from datetime import datetime, timezone
import re

from pydantic import ConstrainedStr
from pydantic.validators import parse_datetime


class StringEnum(str, Enum):
    """
    Sane enum that behaves like a string.

    Can be safely used for JSON serialization. Convenient for API responses and storing in NoSQL or key-value databases.

    >>> class Gender(str, Enum):
    ...     MALE = 'male'
    ...     FEMALE = 'female'
    >>> str(Gender.MALE)
    'Gender.MALE'

    >>> class Gender(StringEnum):
    ...     MALE = 'male'
    ...     FEMALE = 'female'
    >>> str(Gender.MALE)
    'male'

    >>> class Gender(StringEnum):
    ...     MALE = 'male'
    ...     FEMALE = 'female'
    >>> f'{Gender.MALE}'
    'male'
    """

    def __str__(self):
        return str(self.value)


class NonEmptyStr(ConstrainedStr):
    """
    Non-empty string in a shorthand form.

    White space is stripped by default.
    """

    min_length = 1
    strip_whitespace = True


class CaseInsensitiveEnum(StringEnum):
    """
    >>> class Gender(CaseInsensitiveEnum):
    ...     MALE = 'male'
    ...     FEMALE = 'female'
    >>> Gender('mAlE')
    <Gender.MALE: 'male'>
    >>> Gender('FEMALE')
    <Gender.FEMALE: 'female'>
    >>> Gender('helicopter')
    Traceback (most recent call last):
    ...
    ValueError: 'helicopter' is not a valid Gender
    """

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return super()._missing_(value)


class SSN(ConstrainedStr):
    """
    10-digit US SSN with optional dashes.

    Dashes are automatically removed during validation.

    >>> from pydantic import parse_obj_as
    >>> parse_obj_as(SSN, '123456789')
    '123456789'
    >>> parse_obj_as(SSN, '1234-5-6789')
    '123456789'
    """

    regex = r"^\d(-?\d){8}$"

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield cls.cleanup_ssn

    @classmethod
    def cleanup_ssn(cls, value) -> str:
        """
        Remove dashes.
        """
        return value.replace("-", "")


class MBI(ConstrainedStr):
    """
    Medicare Beneficiary Identifier (MBI).

    https://www.cms.gov/medicare/new-medicare-card/understanding-the-mbi-with-format.pdf

    Implementation credits to https://stackoverflow.com/a/47683670/3455614

    >>> import re
    >>> from pydantic import parse_obj_as
    >>> parse_obj_as(MBI, '1ax0Y67Dw34')
    '1AX0Y67DW34'
    >>> all(re.match(MBI.regex, mbi) for mbi in [
    ...     '1AX0Y67DW34', '4C56de7FG00', '9EN1EQ3TT59', '2H52CD7GQ83', '3U90VV3UV09',
    ... ])
    True
    >>> any(re.match(MBI.regex, mbi) for mbi in ['0AX0Y67DW34', '4256DE7FG00'])
    False
    """

    to_upper = True

    regex = re.sub(
        r"\s+",
        "",
        r"""
        ^
        ([1-9])
        ((?![sloibzSLOIBZ])[a-zA-Z])
        (\d|(?![sloibzSLOIBZ])[a-zA-Z])
        (\d)
        ((?![sloibzSLOIBZ])[a-zA-Z])
        (\d|(?![sloibzSLOIBZ])[a-zA-Z])
        (\d)
        ((?![sloibzSLOIBZ])[a-zA-Z])
        ((?![sloibzSLOIBZ])[a-zA-Z])
        (\d)
        (\d)
        $
        """,
    )


class UTCDatetime(datetime):
    """
    Datetime with UTC timezone.

    Enforces UTC timezone and disallows naive timestamps.

    >>> from pydantic import BaseModel
    >>> import pytz
    >>> class Message(BaseModel):
    ...     text: str
    ...     created: UTCDatetime
    >>> naive_str = '1991-08-24 10:00:00'
    >>> naive = datetime.fromisoformat(naive_str)

    >>> Message(text='Do the barrel roll!', created=naive)
    Traceback (most recent call last):
    ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Message
    created
      Naive timestamps are not allowed (type=value_error)

    >>> Message(text='Do the barrel roll!', created=naive_str)
    Traceback (most recent call last):
    ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Message
    created
      Naive timestamps are not allowed (type=value_error)


    >>> Message(text='Батько наш Бандера!', created=naive.replace(tzinfo=pytz.timezone('Europe/Kyiv')))
    Traceback (most recent call last):
    ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Message
    created
      Timestamp must be in UTC timezone (type=value_error)

    >>> Message(text='Батько наш Бандера!', created=f'{naive_str}+03:00')
    Traceback (most recent call last):
    ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Message
    created
      Timestamp must be in UTC timezone (type=value_error)

    >>> Message(text='Slava Ukraini!', created=naive.replace(tzinfo=timezone.utc))
    Message(text='Slava Ukraini!', created=datetime.datetime(1991, 8, 24, 10, 0, tzinfo=datetime.timezone.utc))

    >>> Message(text='Slava Ukraini!', created=f'{naive_str}+00:00')
    Message(text='Slava Ukraini!', created=datetime.datetime(1991, 8, 24, 10, 0, tzinfo=datetime.timezone.utc))

    >>> Message(text='Slava Ukraini!', created=f'{naive_str}+00:00').json()
    '{"text": "Slava Ukraini!", "created": "1991-08-24T10:00:00+00:00"}'
    """

    @classmethod
    def __get_validators__(cls):
        yield parse_datetime
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not value.tzinfo:
            raise ValueError("Naive timestamps are not allowed")
        if value.tzinfo != timezone.utc:
            raise ValueError("Timestamp must be in UTC timezone")
        return value
