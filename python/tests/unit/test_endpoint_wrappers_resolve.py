"""
HeimdallApiClient imports most endpoint wrappers inside the method body, which
means a wrapper that was never written stays invisible to ruff and to import of
the package — it only fails when a caller reaches the method. These tests
resolve every wrapper the client methods import, so a missing one fails in CI.
"""

import pytest

from heimdall_api_client import capacity_monitoring, grid_insights

_GRID_INSIGHTS_WRAPPERS = [
    "get_latest_conductor_temperature",
    "get_latest_current",
    "get_latest_icing",
    "get_latest_sag_and_clearance",
    "get_currents",
    "get_conductor_temperatures",
    "get_icing",
    "get_sag_and_clearance",
    "get_apparent_power",
    "get_latest_apparent_power",
    "get_icing_forecast",
]

_CAPACITY_MONITORING_WRAPPERS = [
    "get_latest_heimdall_dlr",
    "get_latest_heimdall_aar",
    "get_latest_heimdall_dlr_forecasts",
    "get_latest_heimdall_arr_forecasts",
    "get_latest_circuit_ratring",
    "get_latest_circuit_rating_forecasts",
    "get_heimdall_dlrs",
    "get_heimdall_aars",
    "get_circuit_ratings",
]

_CLIENT_METHODS = [
    "get_assets",
    "get_currents",
    "get_conductor_temperatures",
    "get_icing",
    "get_sag_and_clearance",
    "get_apparent_power",
    "get_latest_apparent_power",
    "get_icing_forecast",
    "get_heimdall_dlrs",
    "get_heimdall_aars",
    "get_circuit_ratings",
]


@pytest.mark.parametrize("name", _GRID_INSIGHTS_WRAPPERS)
def test_grid_insights_wrapper_is_defined(name: str):
    assert callable(getattr(grid_insights, name, None)), f"grid_insights.{name} is missing"


@pytest.mark.parametrize("name", _CAPACITY_MONITORING_WRAPPERS)
def test_capacity_monitoring_wrapper_is_defined(name: str):
    assert callable(getattr(capacity_monitoring, name, None)), f"capacity_monitoring.{name} is missing"


@pytest.mark.parametrize("name", _CLIENT_METHODS)
def test_client_exposes_method(name: str):
    from heimdall_api_client import HeimdallApiClient

    assert callable(getattr(HeimdallApiClient, name, None)), f"HeimdallApiClient.{name} is missing"


# The API added `since` to these after the wrappers were first written; the
# generated endpoints accept it, so the wrappers must not silently drop it.
_METHODS_ACCEPTING_SINCE = [
    "get_latest_current",
    "get_latest_conductor_temperature",
    "get_latest_apparent_power",
    "get_latest_icing",
    "get_latest_sag_and_clearance",
    "get_latest_heimdall_dlr",
    "get_latest_heimdall_aar",
    "get_latest_circuit_rating",
]


@pytest.mark.parametrize("name", _METHODS_ACCEPTING_SINCE)
def test_client_method_accepts_since(name: str):
    import inspect

    from heimdall_api_client import HeimdallApiClient

    parameters = inspect.signature(getattr(HeimdallApiClient, name)).parameters
    assert "since" in parameters, f"HeimdallApiClient.{name} should accept since"
    assert parameters["since"].default is None, f"HeimdallApiClient.{name} should default since to None"
