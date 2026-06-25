from __future__ import annotations

import datetime
import logging
import time
from typing import TYPE_CHECKING, Callable, TypeVar
from uuid import UUID

from heimdall_api_client.assets import get_assets
from heimdall_api_client.assets_api_client.client import AuthenticatedClient
from heimdall_api_client.auth import AuthService
from heimdall_api_client.capacity_monitoring import (
    get_latest_heimdall_aar,
    get_latest_heimdall_arr_forecasts,
    get_latest_heimdall_dlr,
    get_latest_heimdall_dlr_forecasts,
)
from heimdall_api_client.errors import HeimdallApiError
from heimdall_api_client.grid_insights_api_client.models.unit_system import UnitSystem

_T = TypeVar("_T")

if TYPE_CHECKING:
    from heimdall_api_client.assets_api_client.models.assets_v1_get_assets_response_200 import (
        AssetsV1GetAssetsResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_forecasts_response_200 import (  # noqa: E501
        CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_response_200 import (  # noqa: E501
        CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_aar_forecasts_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_aar_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallAarResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_dlr_forecasts_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallDlrForecastsResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_dlr_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_latest_conductor_temperature_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetLatestConductorTemperatureResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_latest_current_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetLatestCurrentResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_latest_icing_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetLatestIcingResponse200,
    )


_MAX_RETRY_ATTEMPTS = 3


class HeimdallApiClient:
    """
    SDK entrypoint for interacting with the Heimdall Power External API.

    Retry behaviour
    ---------------
    All methods automatically retry up to 3 times with exponential backoff
    (1 s → 2 s → 4 s) when the server or Application Gateway returns a
    transient error:

    * ``502 Bad Gateway``
    * ``503 Service Unavailable``
    * ``504 Gateway Timeout``

    A warning is logged for each retry attempt.
    If all 3 retry attempts are exhausted the last
    :class:`~heimdall_api_client.errors.HeimdallApiError` is re-raised.

    Exceptions
    ----------
    All methods raise :class:`~heimdall_api_client.errors.HeimdallApiError` on
    non-transient HTTP errors (e.g. 400, 403, 404, 500) or after all retries
    are exhausted on transient errors. The ``status_code`` attribute carries
    the HTTP status code.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        api_base_url: str = "https://external-api.heimdallcloud.com",
        auth_policy: str = "b2c_1a_clientcredentialsflow",
        tenant: str = "hpadb2cprod",
        auth_authority_domain: str = "hpadb2cprod.b2clogin.com",
        auth_scope: list[str] | None = None,
        logger: logging.Logger | None = None,
        client_metadata: dict[str, str] | None = None,
    ):
        self.logger = logger or logging.getLogger(__name__)

        self.auth_service = AuthService(
            client_id=client_id,
            client_secret=client_secret,
            auth_policy=auth_policy,
            tenant=tenant,
            authority_domain=auth_authority_domain,
            scope=auth_scope,
        )

        self.api_base_url = api_base_url

        default_metadata = {
            "x-client-name": "python-sdk",
            "x-client-version": "0.0.0",
        }

        # Ensure user values override the defaults
        self.client_metadata = {**default_metadata, **(client_metadata or {})}

    def _get_authenticated_client(self) -> AuthenticatedClient:
        token = self.auth_service.get_valid_token()
        return AuthenticatedClient(base_url=self.api_base_url, token=token, headers=self.client_metadata)

    def _get_region(self) -> str:
        return self.auth_service.get_region_from_token()

    def _execute_with_retry(self, func: Callable[[], _T]) -> _T:
        """
        Executes the given callable and retries automatically on transient API errors
        (HTTP 500, 502, 503, 504) with exponential backoff (1s, 2s, 4s).
        """
        attempt = 0
        while True:
            try:
                return func()
            except HeimdallApiError as exc:
                if exc.is_transient() and attempt < _MAX_RETRY_ATTEMPTS:
                    attempt += 1
                    delay = 2 ** (attempt - 1)  # 1s, 2s, 4s
                    self.logger.warning(
                        "Transient error (HTTP %s) on attempt %d/%d. Retrying in %ds...",
                        exc.status_code,
                        attempt,
                        _MAX_RETRY_ATTEMPTS,
                        delay,
                    )
                    time.sleep(delay)
                else:
                    raise

    def get_assets(self) -> AssetsV1GetAssetsResponse200:
        """
        Returns the list of assets from the Assets API.
        """
        return self._execute_with_retry(
            lambda: get_assets(client=self._get_authenticated_client(), x_region=self._get_region())
        )

    def get_latest_heimdall_dlr(self, line_id: UUID) -> CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200:
        """
        Returns the latest Heimdall DLR (Dynamic Line rating) data.
        """
        return self._execute_with_retry(
            lambda: get_latest_heimdall_dlr(
                client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
            )
        )

    def get_latest_heimdall_aar(self, line_id: UUID) -> CapacityMonitoringV1LinesGetLatestHeimdallAarResponse200:
        """
        Returns the latest Heimdall AAR (Available Ampacity Rating) data.
        """
        return self._execute_with_retry(
            lambda: get_latest_heimdall_aar(
                client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
            )
        )

    def get_latest_heimdall_dlr_forecasts(
        self, line_id: UUID
    ) -> CapacityMonitoringV1LinesGetLatestHeimdallDlrForecastsResponse200:
        """
        Returns the latest Heimdall DLR forecasts.
        """
        return self._execute_with_retry(
            lambda: get_latest_heimdall_dlr_forecasts(
                client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
            )
        )

    def get_latest_heimdall_aar_forecasts(
        self, line_id: UUID
    ) -> CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200:
        """
        Returns the latest Heimdall AAR forecasts.
        """
        return self._execute_with_retry(
            lambda: get_latest_heimdall_arr_forecasts(
                client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
            )
        )

    def get_latest_circuit_rating(
        self, facility_id: UUID
    ) -> CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200:
        """
        Returns the latest circuit rating for a given facility.
        """
        from heimdall_api_client.capacity_monitoring import get_latest_circuit_ratring

        return self._execute_with_retry(
            lambda: get_latest_circuit_ratring(
                client=self._get_authenticated_client(), facility_id=facility_id, x_region=self._get_region()
            )
        )

    def get_latest_circuit_rating_forecasts(
        self, facility_id: UUID
    ) -> CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200:
        """
        Returns the latest circuit rating forecasts for a given facility.
        """
        from heimdall_api_client.capacity_monitoring import get_latest_circuit_rating_forecasts

        return self._execute_with_retry(
            lambda: get_latest_circuit_rating_forecasts(
                client=self._get_authenticated_client(), facility_id=facility_id, x_region=self._get_region()
            )
        )

    def get_latest_conductor_temperature(
        self, line_id: UUID
    ) -> GridInsightsV1LinesGetLatestConductorTemperatureResponse200:
        """
        Returns the latest conductor temperature for a given line.
        """
        from heimdall_api_client.grid_insights import get_latest_conductor_temperature

        return self._execute_with_retry(
            lambda: get_latest_conductor_temperature(
                client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
            )
        )

    def get_latest_current(self, line_id: UUID) -> GridInsightsV1LinesGetLatestCurrentResponse200:
        """
        Returns the latest current for a given line.
        """
        from heimdall_api_client.grid_insights import get_latest_current

        return self._execute_with_retry(
            lambda: get_latest_current(
                client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
            )
        )

    def get_latest_icing(
        self,
        line_id: UUID,
        unit_system: UnitSystem | str | None = None,
        since: datetime.datetime | None = None,
    ) -> GridInsightsV1LinesGetLatestIcingResponse200:
        """
        Returns the latest icing measurements for a given line.
        """
        from heimdall_api_client.grid_insights import get_latest_icing

        return self._execute_with_retry(
            lambda: get_latest_icing(
                client=self._get_authenticated_client(),
                line_id=line_id,
                region=self._get_region(),
                unit_system=unit_system,
                since=since,
            )
        )

    def get_latest_sag_and_clearance(
        self,
        line_id: UUID,
        unit_system: UnitSystem | str | None = None,
        since: datetime.datetime | None = None,
    ):
        """
        Returns the latest sag and clearance measurements for a given line.
        """
        from heimdall_api_client.grid_insights import get_latest_sag_and_clearance

        return self._execute_with_retry(
            lambda: get_latest_sag_and_clearance(
                client=self._get_authenticated_client(),
                line_id=line_id,
                region=self._get_region(),
                unit_system=unit_system,
                since=since,
            )
        )
