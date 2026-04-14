from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING
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
from heimdall_api_client.grid_insights_api_client.models.unit_system import UnitSystem

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


class HeimdallApiClient:
    """
    SDK entrypoint for interacting with the Heimdall Power External API.
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

    def get_assets(self) -> AssetsV1GetAssetsResponse200:
        """
        Returns the list of assets from the Assets API.
        """
        return get_assets(client=self._get_authenticated_client(), x_region=self._get_region())

    def get_latest_heimdall_dlr(self, line_id: UUID) -> CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200:
        """
        Returns the latest Heimdall DLR (Dynamic Line rating) data.
        """
        return get_latest_heimdall_dlr(
            client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
        )

    def get_latest_heimdall_aar(self, line_id: UUID) -> CapacityMonitoringV1LinesGetLatestHeimdallAarResponse200:
        """
        Returns the latest Heimdall AAR (Available Ampacity Rating) data.
        """
        return get_latest_heimdall_aar(
            client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
        )

    def get_latest_heimdall_dlr_forecasts(
        self, line_id: UUID
    ) -> CapacityMonitoringV1LinesGetLatestHeimdallDlrForecastsResponse200:
        """
        Returns the latest Heimdall DLR forecasts.
        """
        return get_latest_heimdall_dlr_forecasts(
            client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
        )

    def get_latest_heimdall_aar_forecasts(
        self, line_id: UUID
    ) -> CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200:
        """
        Returns the latest Heimdall AAR forecasts.
        """
        return get_latest_heimdall_arr_forecasts(
            client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
        )

    def get_latest_circuit_rating(
        self, facility_id: UUID
    ) -> CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200:
        """
        Returns the latest circuit rating for a given facility.
        """
        from heimdall_api_client.capacity_monitoring import get_latest_circuit_ratring

        return get_latest_circuit_ratring(
            client=self._get_authenticated_client(), facility_id=facility_id, x_region=self._get_region()
        )

    def get_latest_circuit_rating_forecasts(
        self, facility_id: UUID
    ) -> CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200:
        """
        Returns the latest circuit rating forecasts for a given facility.
        """
        from heimdall_api_client.capacity_monitoring import get_latest_circuit_rating_forecasts

        return get_latest_circuit_rating_forecasts(
            client=self._get_authenticated_client(), facility_id=facility_id, x_region=self._get_region()
        )

    def get_latest_conductor_temperature(
        self, line_id: UUID
    ) -> GridInsightsV1LinesGetLatestConductorTemperatureResponse200:
        """
        Returns the latest conductor temperature for a given line.
        """
        from heimdall_api_client.grid_insights import get_latest_conductor_temperature

        return get_latest_conductor_temperature(
            client=self._get_authenticated_client(), line_id=line_id, region=self._get_region()
        )

    def get_latest_current(self, line_id: UUID) -> GridInsightsV1LinesGetLatestCurrentResponse200:
        """
        Returns the latest current for a given line.
        """
        from heimdall_api_client.grid_insights import get_latest_current

        return get_latest_current(client=self._get_authenticated_client(), line_id=line_id, region=self._get_region())

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

        return get_latest_icing(
            client=self._get_authenticated_client(),
            line_id=line_id,
            region=self._get_region(),
            unit_system=unit_system,
            since=since,
        )
