import logging

from heimdall_api_client import HeimdallApiClient, HeimdallApiError

logging.basicConfig(level=logging.INFO)  # INFO shows automatic retry warnings

client = HeimdallApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    # Optional: abort any request (including each retry attempt) after 10 seconds.
    # timeout=10.0,
)

# All calls below automatically retry up to 3 times (1 s → 2 s → 4 s backoff)
# on transient gateway errors (502, 503, 504). No extra retry logic needed.

assets = client.get_assets()
grid_owner = assets.data.grid_owners[0]

print(f"\nGrid Owner: {grid_owner.name}\n")

for facility in grid_owner.facilities:
    line = facility.line
    if not line:
        print(f"Facility: {facility.name} has no lines.\n")
        continue
    try:
        dlr_response = client.get_latest_heimdall_dlr(line_id=line.id)
        dlr = dlr_response.data.heimdall_dlr
        dlr_forecast_response = client.get_latest_heimdall_dlr_forecasts(line_id=line.id)
        dlr_forecast = dlr_forecast_response.data.heimdall_dlr_forecasts
        print(f"Facility: {facility.name}")
        print(f"  Line: {line.name} (ID: {line.id})\n")
        print(f"    {dlr_response.data.metric}, timestamp {dlr.timestamp}\n")
        print(f"        {dlr.value} {dlr_response.data.unit}, isFallback = {dlr.is_fallback}\n")
        print(f"    {dlr_forecast_response.data.metric}, updated at {dlr_forecast_response.data.updated_timestamp}:")
        for forecast in dlr_forecast:
            print(f"      {forecast.timestamp}: {forecast.prediction.value} {dlr_forecast_response.data.unit}")
    except HeimdallApiError as e:
        # Retries already exhausted automatically before reaching here
        print(f"  API error {e.status_code} for line '{line.name}' (ID: {line.id}): {e}\n")
