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
    line = facility.line
    if not line:
        print(f"Facility: {facility.name} has no lines.\n")
        continue
    line_id = line.id

    print(f"Line: {line.name} (ID: {line_id})")

    latest_conductor_temperature_response = client.get_latest_conductor_temperature(line_id=line_id)
    latest_conductor_temp = latest_conductor_temperature_response.data.conductor_temperature
    latest_current_response = client.get_latest_current(line_id=line_id)
    latest_current = latest_current_response.data.current

    print(f"  Max Conductor Temperature, {latest_conductor_temp.timestamp}: {latest_conductor_temp.max_} {latest_conductor_temperature_response.data.unit}")
    print(f"  Min Conductor Temperature, {latest_conductor_temp.timestamp}: {latest_conductor_temp.min_} {latest_conductor_temperature_response.data.unit}")
    print(f"  Current,                   {latest_current.timestamp}: {latest_current.value} {latest_current_response.data.unit}")