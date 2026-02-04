import logging
from datetime import datetime, timedelta, timezone

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

    since = datetime.now(timezone.utc) - timedelta(minutes=30)
    latest_icing_response = client.get_latest_icing(line_id=line_id, since=since)
    latest_icing = latest_icing_response.data.icing

    max_icing = latest_icing.max_
    print(
        f"  Max Ice Weight: {max_icing.ice_weight.value} {max_icing.ice_weight.unit} (span phase {max_icing.ice_weight.span_phase_id}, {max_icing.ice_weight.timestamp})"
    )
    print(
        f"  Max Tension:    {max_icing.tension.value} {max_icing.tension.unit} (span phase {max_icing.tension.span_phase_id}, {max_icing.tension.timestamp})"
    )
    print(
        "  Max Tension %:  "
        f"{max_icing.tension_percentage_of_break_strength.value} {max_icing.tension_percentage_of_break_strength.unit} "
        f"(span phase {max_icing.tension_percentage_of_break_strength.span_phase_id}, {max_icing.tension_percentage_of_break_strength.timestamp})"
    )
