import logging
from heimdall_api_client.client import HeimdallApiClient

logging.basicConfig(level=logging.WARN)

client = HeimdallApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

assets = client.get_assets()
grid_owner = assets.data.grid_owners[0]

print(f"\nGrid Owner: {grid_owner.name}\n")

for facility in grid_owner.facilities:
    facility_id = facility.id
    try:
        circuit_rating_response = client.get_latest_circuit_rating(facility_id=facility_id)
        circuit_rating = circuit_rating_response.data.circuit_rating
        circuit_rating_forecast_response = client.get_latest_circuit_rating_forecasts(facility_id=facility_id)
        circuit_rating_forecast = circuit_rating_forecast_response.data.circuit_rating_forecasts
        print(f"Facility: {facility.name}")
        print(f"    {circuit_rating_response.data.metric}, timestamp {circuit_rating.timestamp}\n")
        print(f"        {circuit_rating.value} {circuit_rating_response.data.unit}\n")
        print(
            f"    {circuit_rating_forecast_response.data.metric}, updated at {circuit_rating_forecast_response.data.updated_timestamp}:"
        )
        for forecast in circuit_rating_forecast:
            print(
                f"      {forecast.timestamp}: {forecast.prediction.value} {circuit_rating_forecast_response.data.unit}"
            )
    except Exception as e:
        print(f"  Failed to fetch circuit rating for facility '{facility.name}' (ID: {facility.id}): {e}\n")
