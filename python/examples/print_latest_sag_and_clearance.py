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
    latest_sag_and_clearance_response = client.get_latest_sag_and_clearance(line_id=line_id, since=since)
    sag_and_clearance = latest_sag_and_clearance_response.data.sag_and_clearance

    for span in sag_and_clearance.spans:
        print(f"  Span: {span.span_id}")
        for phase in span.span_phases:
            sag = phase.sag
            clearance = phase.clearance
            clearance_str = (
                f"{clearance.value} {clearance.unit}" if clearance is not None else "N/A"
            )
            print(f"    Phase {phase.span_phase_id} ({phase.timestamp})")
            print(f"      Sag:       {sag.value} {sag.unit}")
            print(f"      Clearance: {clearance_str}")
