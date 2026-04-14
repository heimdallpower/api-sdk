import logging
from datetime import UTC, datetime, timedelta

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

    since = datetime.now(UTC) - timedelta(minutes=30)
    latest_icing_response = client.get_latest_icing(line_id=line_id, since=since)
    latest_icing = latest_icing_response.data.icing

    max_icing = latest_icing.max_
    iw = max_icing.ice_weight
    tn = max_icing.tension
    tp = max_icing.tension_percentage_of_break_strength
    print(f"  Max Ice Weight: {iw.value} {iw.unit} (span phase {iw.span_phase_id}, {iw.timestamp})")
    print(f"  Max Tension:    {tn.value} {tn.unit} (span phase {tn.span_phase_id}, {tn.timestamp})")
    print(f"  Max Tension %:  {tp.value} {tp.unit} (span phase {tp.span_phase_id}, {tp.timestamp})")
