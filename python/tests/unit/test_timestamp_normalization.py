"""
Unit tests for as_zulu, which exists because the API accepts only Z-suffixed UTC
timestamps while datetime.isoformat() always emits a `+00:00` offset.
"""

import datetime

import pytest

from heimdall_api_client._timestamps import as_zulu

_OSLO = datetime.timezone(datetime.timedelta(hours=2))


class TestAsZulu:
    def test_naive_is_treated_as_utc(self):
        assert as_zulu(datetime.datetime(2024, 7, 2, 10, 0, 0)).isoformat() == "2024-07-02T10:00:00Z"

    def test_utc_aware_keeps_its_wall_clock(self):
        timestamp = datetime.datetime(2024, 7, 2, 10, 0, 0, tzinfo=datetime.UTC)
        assert as_zulu(timestamp).isoformat() == "2024-07-02T10:00:00Z"

    def test_other_offset_is_converted_to_utc(self):
        timestamp = datetime.datetime(2024, 7, 2, 12, 0, 0, tzinfo=_OSLO)
        assert as_zulu(timestamp).isoformat() == "2024-07-02T10:00:00Z"

    def test_microseconds_are_preserved(self):
        timestamp = datetime.datetime(2024, 7, 2, 10, 0, 0, 123456, tzinfo=datetime.UTC)
        assert as_zulu(timestamp).isoformat() == "2024-07-02T10:00:00.123456Z"

    @pytest.mark.parametrize(
        "timestamp",
        [
            datetime.datetime(2024, 7, 2, 10, 0, 0),
            datetime.datetime(2024, 7, 2, 10, 0, 0, tzinfo=datetime.UTC),
            datetime.datetime(2024, 7, 2, 12, 0, 0, tzinfo=_OSLO),
        ],
    )
    def test_never_emits_an_offset(self, timestamp: datetime.datetime):
        rendered = as_zulu(timestamp).isoformat()
        assert rendered.endswith("Z")
        assert "+" not in rendered

    def test_represents_the_same_instant(self):
        timestamp = datetime.datetime(2024, 7, 2, 12, 0, 0, tzinfo=_OSLO)
        assert as_zulu(timestamp).timestamp() == timestamp.timestamp()

    def test_is_a_datetime_so_generated_clients_accept_it(self):
        assert isinstance(as_zulu(datetime.datetime(2024, 7, 2)), datetime.datetime)
