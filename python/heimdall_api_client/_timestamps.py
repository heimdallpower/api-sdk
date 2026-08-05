"""
UTC timestamp normalization for query parameters.

The API accepts only Z-suffixed UTC timestamps: `2024-07-02T00:00:00Z` returns
200 where the equivalent `2024-07-02T00:00:00+00:00` is rejected with
`400 {"errors": {"to_timestamp": ["The value '...' is not valid."]}}`.

The generated clients serialize every datetime query parameter with
`datetime.isoformat()`, which always emits the `+00:00` offset and never `Z`, so
no `datetime` a caller passes can produce a valid request. Rather than patch the
generated packages -- which `scripts/generate-module-client.ps1` overwrites --
the hand-written wrappers normalize timestamps through `as_zulu` on the way in.

Naive datetimes are assumed to be UTC; aware ones are converted, so a caller
passing a local-timezone datetime gets the window they asked for.
"""

from __future__ import annotations

import datetime


class ZuluDatetime(datetime.datetime):
    """A datetime whose isoformat() renders as UTC with a `Z` suffix."""

    def isoformat(self, sep: str = "T", timespec: str = "auto") -> str:
        # Built explicitly rather than via astimezone()/replace(), which return
        # this subclass and would recurse back into this method.
        utc = datetime.datetime.fromtimestamp(self.timestamp(), datetime.UTC)
        naive_utc = datetime.datetime(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second, self.microsecond)
        return f"{naive_utc.isoformat(sep=sep, timespec=timespec)}Z"


def as_zulu(timestamp: datetime.datetime) -> ZuluDatetime:
    """
    Returns `timestamp` as a UTC ZuluDatetime. Naive input is treated as UTC.
    """
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=datetime.UTC)
    utc = timestamp.astimezone(datetime.UTC)
    return ZuluDatetime(
        utc.year,
        utc.month,
        utc.day,
        utc.hour,
        utc.minute,
        utc.second,
        utc.microsecond,
        tzinfo=datetime.UTC,
    )
