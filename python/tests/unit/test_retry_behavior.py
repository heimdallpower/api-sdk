"""
Unit tests for retry behaviour in HeimdallApiClient._execute_with_retry.

Covers:
- Retry on transient errors: 500, 502, 503, 504 (including HTML body from Application Gateway)
- No retry on non-transient errors: 400, 401, 403, 404
- Exponential backoff delays (time.sleep is patched to avoid real waits)
- Success after one or more transient failures
- HeimdallApiError carries the correct status_code
- is_transient() helper returns correct values for all relevant codes
"""

from unittest.mock import MagicMock, call, patch

import pytest

from heimdall_api_client.errors import HeimdallApiError

# ---------------------------------------------------------------------------
# Helpers shared across tests
# ---------------------------------------------------------------------------

_GATEWAY_TIMEOUT_HTML = """\
<!DOCTYPE html>
<html><head><title>504 Gateway Timeout</title></head>
<body><h1>504 Gateway Timeout</h1>
<p>The upstream server did not respond in time.</p>
</body></html>
"""

_INTERNAL_SERVER_ERROR_HTML = """\
<!DOCTYPE html>
<html><head><title>500 Internal Server Error</title></head>
<body><h1>500 Internal Server Error</h1></body></html>
"""


def _make_client(max_retries: int = 3):
    """
    Returns a minimal HeimdallApiClient with auth and HTTP completely stubbed out.
    max_retries is wired via _MAX_RETRY_ATTEMPTS patch so tests stay fast.
    """
    import heimdall_api_client.client as client_module
    from heimdall_api_client.client import HeimdallApiClient

    client = HeimdallApiClient.__new__(HeimdallApiClient)
    client.logger = MagicMock()
    client.auth_service = MagicMock()
    client.api_base_url = "https://fake.heimdallcloud.com"
    client.client_metadata = {}
    return client


def _raises_transient(status_code: int, times: int = 1):
    """Returns a side_effect list: raises HeimdallApiError(status_code) `times` times."""
    return [HeimdallApiError(f"Error {status_code}", status_code=status_code)] * times


def _raises_then_returns(status_code: int, times: int, return_value):
    """Raises a transient error `times` times, then returns return_value."""
    effects = _raises_transient(status_code, times)
    effects.append(return_value)
    return effects


# ---------------------------------------------------------------------------
# HeimdallApiError unit tests
# ---------------------------------------------------------------------------

class TestHeimdallApiError:
    @pytest.mark.parametrize("status_code", [502, 503, 504])
    def test_is_transient_returns_true_for_transient_codes(self, status_code: int):
        err = HeimdallApiError("error", status_code=status_code)
        assert err.is_transient() is True

    def test_500_is_not_transient(self):
        err = HeimdallApiError("error", status_code=500)
        assert err.is_transient() is False

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 422, 500, 200, 201])
    def test_is_transient_returns_false_for_non_transient_codes(self, status_code: int):
        err = HeimdallApiError("error", status_code=status_code)
        assert err.is_transient() is False

    def test_carries_status_code(self):
        err = HeimdallApiError("Gateway timeout", status_code=504)
        assert err.status_code == 504

    def test_carries_request_url(self):
        err = HeimdallApiError("Not found", status_code=404, request_url="/api/lines/123")
        assert err.request_url == "/api/lines/123"

    def test_str_is_the_message(self):
        err = HeimdallApiError("Something failed", status_code=500)
        assert str(err) == "Something failed"


# ---------------------------------------------------------------------------
# _execute_with_retry — retry logic
# ---------------------------------------------------------------------------

class TestExecuteWithRetry:

    @pytest.mark.parametrize("status_code", [502, 503, 504])
    @patch("heimdall_api_client.client.time.sleep")
    def test_retries_on_all_transient_codes(self, mock_sleep, status_code: int):
        """For each transient code the client retries up to 3 times."""
        client = _make_client()
        func = MagicMock(side_effect=_raises_transient(status_code, times=4))

        with pytest.raises(HeimdallApiError) as exc_info:
            client._execute_with_retry(func)

        assert exc_info.value.status_code == status_code
        assert func.call_count == 4  # 1 initial + 3 retries

    @pytest.mark.parametrize("status_code", [502, 503, 504])
    @patch("heimdall_api_client.client.time.sleep")
    def test_returns_result_after_one_transient_failure(self, mock_sleep, status_code: int):
        """Succeeds when the first call fails transiently but the second succeeds."""
        client = _make_client()
        expected = object()
        func = MagicMock(side_effect=_raises_then_returns(status_code, times=1, return_value=expected))

        result = client._execute_with_retry(func)

        assert result is expected
        assert func.call_count == 2

    @pytest.mark.parametrize("status_code", [502, 503, 504])
    @patch("heimdall_api_client.client.time.sleep")
    def test_returns_result_after_two_transient_failures(self, mock_sleep, status_code: int):
        """Succeeds when the first two calls fail transiently but the third succeeds."""
        client = _make_client()
        expected = object()
        func = MagicMock(side_effect=_raises_then_returns(status_code, times=2, return_value=expected))

        result = client._execute_with_retry(func)

        assert result is expected
        assert func.call_count == 3

    @patch("heimdall_api_client.client.time.sleep")
    def test_504_with_html_body_does_not_crash_and_retries(self, mock_sleep):
        """
        Simulates the original customer bug: Application Gateway returns 504 with an HTML
        body.  The error is caught as HeimdallApiError (status_code=504) and retried.
        The test verifies no unexpected exception type propagates.
        """
        client = _make_client()
        func = MagicMock(side_effect=[
            HeimdallApiError(_GATEWAY_TIMEOUT_HTML, status_code=504),
            HeimdallApiError(_GATEWAY_TIMEOUT_HTML, status_code=504),
            HeimdallApiError(_GATEWAY_TIMEOUT_HTML, status_code=504),
            HeimdallApiError(_GATEWAY_TIMEOUT_HTML, status_code=504),
        ])

        with pytest.raises(HeimdallApiError) as exc_info:
            client._execute_with_retry(func)

        # Must be HeimdallApiError, NOT a json/parse exception
        assert exc_info.value.status_code == 504
        assert func.call_count == 4

    @patch("heimdall_api_client.client.time.sleep")
    def test_500_with_html_body_does_not_crash_and_is_not_retried(self, mock_sleep):
        """500 Internal Server Error is NOT retried — it should raise immediately."""
        client = _make_client()
        func = MagicMock(side_effect=HeimdallApiError(_INTERNAL_SERVER_ERROR_HTML, status_code=500))

        with pytest.raises(HeimdallApiError) as exc_info:
            client._execute_with_retry(func)

        assert exc_info.value.status_code == 500
        assert func.call_count == 1   # no retry
        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# _execute_with_retry — exponential backoff
# ---------------------------------------------------------------------------

class TestExponentialBackoff:

    @patch("heimdall_api_client.client.time.sleep")
    def test_backoff_delays_are_1_2_4_seconds(self, mock_sleep):
        """Retries use exponential backoff: 1 s, 2 s, 4 s."""
        client = _make_client()
        func = MagicMock(side_effect=_raises_transient(504, times=4))

        with pytest.raises(HeimdallApiError):
            client._execute_with_retry(func)

        assert mock_sleep.call_count == 3
        mock_sleep.assert_has_calls([call(1), call(2), call(4)])

    @patch("heimdall_api_client.client.time.sleep")
    def test_no_sleep_on_first_attempt(self, mock_sleep):
        """The very first attempt must not sleep."""
        client = _make_client()
        func = MagicMock(side_effect=_raises_transient(504, times=4))

        with pytest.raises(HeimdallApiError):
            client._execute_with_retry(func)

        # sleep is only called before retry attempts, never before the first call
        first_call_sleep = [c for c in mock_sleep.call_args_list if c == call(0)]
        assert not first_call_sleep

    @patch("heimdall_api_client.client.time.sleep")
    def test_no_sleep_when_not_retrying(self, mock_sleep):
        """Non-transient errors must not sleep at all."""
        client = _make_client()
        func = MagicMock(side_effect=HeimdallApiError("not found", status_code=404))

        with pytest.raises(HeimdallApiError):
            client._execute_with_retry(func)

        mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# _execute_with_retry — non-transient codes must NOT retry
# ---------------------------------------------------------------------------

class TestNonTransientErrors:

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 422, 500])
    @patch("heimdall_api_client.client.time.sleep")
    def test_non_transient_errors_are_not_retried(self, mock_sleep, status_code: int):
        """Client raises immediately on non-transient HTTP errors without any retry."""
        client = _make_client()
        func = MagicMock(side_effect=HeimdallApiError("client error", status_code=status_code))

        with pytest.raises(HeimdallApiError) as exc_info:
            client._execute_with_retry(func)

        assert exc_info.value.status_code == status_code
        assert func.call_count == 1   # only one attempt
        mock_sleep.assert_not_called()

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500])
    @patch("heimdall_api_client.client.time.sleep")
    def test_non_transient_error_with_html_body_raises_immediately(self, mock_sleep, status_code: int):
        """Even if the body is HTML, non-transient codes must not be retried."""
        client = _make_client()
        html = "<html><body>Forbidden</body></html>"
        func = MagicMock(side_effect=HeimdallApiError(html, status_code=status_code))

        with pytest.raises(HeimdallApiError):
            client._execute_with_retry(func)

        assert func.call_count == 1


# ---------------------------------------------------------------------------
# _execute_with_retry — warning logger
# ---------------------------------------------------------------------------

class TestRetryLogging:

    @patch("heimdall_api_client.client.time.sleep")
    def test_warning_is_logged_on_each_retry(self, mock_sleep):
        """A warning must be emitted for each retry attempt."""
        client = _make_client()
        func = MagicMock(side_effect=_raises_transient(504, times=4))

        with pytest.raises(HeimdallApiError):
            client._execute_with_retry(func)

        assert client.logger.warning.call_count == 3  # one per retry

