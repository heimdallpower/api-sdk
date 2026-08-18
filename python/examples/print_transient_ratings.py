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
    print(f"Facility: {facility.name}")

    if facility.line:
        try:
            line_response = client.get_latest_line_transient_rating(line_id=facility.line.id)
            line_transient_rating = line_response.data.line_transient_rating
            print(f"    {line_response.data.metric}, timestamp {line_transient_rating.timestamp}:")
            for rating in line_transient_rating.ratings:
                print(f"      {rating.duration_minutes} min: {rating.value} {line_response.data.unit}")
        except Exception as e:
            print(f"  Failed to fetch line transient rating for line '{facility.line.name}': {e}")

    try:
        circuit_response = client.get_latest_circuit_transient_rating(facility_id=facility.id)
        circuit_transient_rating = circuit_response.data.circuit_transient_rating
        print(f"    {circuit_response.data.metric}, timestamp {circuit_transient_rating.timestamp}:")
        for rating in circuit_transient_rating.ratings:
            # A null limiting component id means the line transient rating is the binding constraint.
            limiting_component = rating.limiting_component_id or "none"
            print(
                f"      {rating.duration_minutes} min: {rating.value} {circuit_response.data.unit}, "
                f"limited by {limiting_component}"
            )
    except Exception as e:
        print(f"  Failed to fetch circuit transient rating for facility '{facility.name}': {e}")

    print()
