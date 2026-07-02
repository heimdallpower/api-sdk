"""
Unit tests for latest and forecast endpoint methods in HeimdallApiClient.

These tests mock the underlying HTTP/API layer so they are:
  - Pure   – no network calls, no external state
  - Fast   – run in milliseconds
  - Deterministic – same input always produces same output

Coverage:
  - Grid Insights: get_latest_current, get_latest_conductor_temperature,
                   get_latest_icing, get_latest_sag_and_clearance,
                   get_latest_apparent_power, get_icing_forecast
  - Capacity Monitoring: get_latest_heimdall_dlr, get_latest_heimdall_aar,
                         get_latest_heimdall_dlr_forecasts,
                         get_latest_heimdall_aar_forecasts,
                         get_latest_circuit_rating,
                         get_latest_circuit_rating_forecasts

Each endpoint is tested for:
  1. 200 OK  → the parsed response object is returned to the caller.
  2. 404 Not Found → HeimdallApiError(status_code=404) is raised (no retry).
  3. 404 is not retried → time.sleep must not be called.
"""

import uuid
from unittest.mock import MagicMock, patch

import pytest

from heimdall_api_client.errors import HeimdallApiError

# ---------------------------------------------------------------------------
# Shared test helpers
# ---------------------------------------------------------------------------

_LINE_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
_FACILITY_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")


def _make_client():
    """Return a HeimdallApiClient with auth completely stubbed out."""
    from heimdall_api_client.client import HeimdallApiClient

    client = HeimdallApiClient.__new__(HeimdallApiClient)
    client.logger = MagicMock()
    client.auth_service = MagicMock()
    client.auth_service.get_valid_token.return_value = "stub-token"
    client.auth_service.get_region_from_token.return_value = "no"
    client.api_base_url = "https://stub.heimdallcloud.com"
    client.client_metadata = {}
    client.timeout = None
    return client


def _raises_404():
    return HeimdallApiError("Not Found", status_code=404)


# ---------------------------------------------------------------------------
# Grid Insights – get_latest_current
# ---------------------------------------------------------------------------


class TestGetLatestCurrent:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.grid_insights.get_latest_current", return_value=expected):
            result = client.get_latest_current(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_current", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_current(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        """Non-transient 404 must not trigger any retry delay."""
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_current", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_current(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Grid Insights – get_latest_conductor_temperature
# ---------------------------------------------------------------------------


class TestGetLatestConductorTemperature:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.grid_insights.get_latest_conductor_temperature", return_value=expected):
            result = client.get_latest_conductor_temperature(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_conductor_temperature", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_conductor_temperature(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_conductor_temperature", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_conductor_temperature(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Grid Insights – get_latest_icing
# ---------------------------------------------------------------------------


class TestGetLatestIcing:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.grid_insights.get_latest_icing", return_value=expected):
            result = client.get_latest_icing(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_icing", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_icing(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_icing", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_icing(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Grid Insights – get_latest_sag_and_clearance
# ---------------------------------------------------------------------------


class TestGetLatestSagAndClearance:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.grid_insights.get_latest_sag_and_clearance", return_value=expected):
            result = client.get_latest_sag_and_clearance(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_sag_and_clearance", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_sag_and_clearance(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_sag_and_clearance", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_sag_and_clearance(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Grid Insights – get_latest_apparent_power
# ---------------------------------------------------------------------------


class TestGetLatestApparentPower:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.grid_insights.get_latest_apparent_power", return_value=expected):
            result = client.get_latest_apparent_power(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_apparent_power", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_apparent_power(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_latest_apparent_power", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_apparent_power(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Grid Insights – get_icing_forecast
# ---------------------------------------------------------------------------


class TestGetIcingForecast:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.grid_insights.get_icing_forecast", return_value=expected):
            result = client.get_icing_forecast(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_icing_forecast", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_icing_forecast(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.grid_insights.get_icing_forecast", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_icing_forecast(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Capacity Monitoring – get_latest_heimdall_dlr
# ---------------------------------------------------------------------------


class TestGetLatestHeimdallDlr:
    # get_latest_heimdall_dlr is a top-level import in client.py, so the patch
    # target is the name as bound inside that module.
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.client.get_latest_heimdall_dlr", return_value=expected):
            result = client.get_latest_heimdall_dlr(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_dlr", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_heimdall_dlr(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_dlr", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_heimdall_dlr(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Capacity Monitoring – get_latest_heimdall_aar
# ---------------------------------------------------------------------------


class TestGetLatestHeimdallAar:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.client.get_latest_heimdall_aar", return_value=expected):
            result = client.get_latest_heimdall_aar(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_aar", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_heimdall_aar(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_aar", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_heimdall_aar(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Capacity Monitoring – get_latest_heimdall_dlr_forecasts
# ---------------------------------------------------------------------------


class TestGetLatestHeimdallDlrForecasts:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.client.get_latest_heimdall_dlr_forecasts", return_value=expected):
            result = client.get_latest_heimdall_dlr_forecasts(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_dlr_forecasts", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_heimdall_dlr_forecasts(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_dlr_forecasts", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_heimdall_dlr_forecasts(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Capacity Monitoring – get_latest_heimdall_aar_forecasts
# ---------------------------------------------------------------------------


class TestGetLatestHeimdallAarForecasts:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.client.get_latest_heimdall_arr_forecasts", return_value=expected):
            result = client.get_latest_heimdall_aar_forecasts(line_id=_LINE_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_arr_forecasts", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_heimdall_aar_forecasts(line_id=_LINE_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.client.get_latest_heimdall_arr_forecasts", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_heimdall_aar_forecasts(line_id=_LINE_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Capacity Monitoring – get_latest_circuit_rating
# ---------------------------------------------------------------------------


class TestGetLatestCircuitRating:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch("heimdall_api_client.capacity_monitoring.get_latest_circuit_ratring", return_value=expected):
            result = client.get_latest_circuit_rating(facility_id=_FACILITY_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch("heimdall_api_client.capacity_monitoring.get_latest_circuit_ratring", side_effect=_raises_404()):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_circuit_rating(facility_id=_FACILITY_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch("heimdall_api_client.capacity_monitoring.get_latest_circuit_ratring", side_effect=_raises_404()):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_circuit_rating(facility_id=_FACILITY_ID)
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# Capacity Monitoring – get_latest_circuit_rating_forecasts
# ---------------------------------------------------------------------------


class TestGetLatestCircuitRatingForecasts:
    def test_returns_parsed_response_on_200(self):
        client = _make_client()
        expected = MagicMock()
        with patch(
            "heimdall_api_client.capacity_monitoring.get_latest_circuit_rating_forecasts",
            return_value=expected,
        ):
            result = client.get_latest_circuit_rating_forecasts(facility_id=_FACILITY_ID)
        assert result is expected

    def test_raises_404_error_on_not_found(self):
        client = _make_client()
        with patch(
            "heimdall_api_client.capacity_monitoring.get_latest_circuit_rating_forecasts",
            side_effect=_raises_404(),
        ):
            with pytest.raises(HeimdallApiError) as exc_info:
                client.get_latest_circuit_rating_forecasts(facility_id=_FACILITY_ID)
        assert exc_info.value.status_code == 404

    def test_404_is_not_retried(self):
        client = _make_client()
        with patch(
            "heimdall_api_client.capacity_monitoring.get_latest_circuit_rating_forecasts",
            side_effect=_raises_404(),
        ):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(HeimdallApiError):
                    client.get_latest_circuit_rating_forecasts(facility_id=_FACILITY_ID)
        mock_sleep.assert_not_called()
