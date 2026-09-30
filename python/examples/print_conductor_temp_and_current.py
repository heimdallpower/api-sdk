import logging

from heimdall_api_client.client import HeimdallApiClient

logging.basicConfig(level=logging.WARN)

client = HeimdallApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Only lines with active measurement points; other lines return 404 or no data.
for instrumented in client.get_instrumented_lines():
    line_id = instrumented.line.id

    print(f"Facility: {instrumented.facility.name}, Line: {instrumented.line.name} (ID: {line_id})")

    latest_conductor_temperature_response = client.get_latest_conductor_temperature(line_id=line_id)
    latest_conductor_temp = latest_conductor_temperature_response.data.conductor_temperature
    latest_current_response = client.get_latest_current(line_id=line_id)
    latest_current = latest_current_response.data.current

    temp_unit = latest_conductor_temperature_response.data.unit
    current_unit = latest_current_response.data.unit
    print(f"  Max Conductor Temperature, {latest_conductor_temp.timestamp}: {latest_conductor_temp.max_} {temp_unit}")
    print(f"  Min Conductor Temperature, {latest_conductor_temp.timestamp}: {latest_conductor_temp.min_} {temp_unit}")
    print(f"  Current,                   {latest_current.timestamp}: {latest_current.value} {current_unit}")
