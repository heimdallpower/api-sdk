from heimdall_api_client.client import HeimdallApiClient
import logging
import pprint

logging.basicConfig(level=logging.WARN)

client = HeimdallApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

assets = client.get_assets()
pprint.pprint(assets)
# new line
print("\nAssets retrieved successfully:\n")
# Print the assets in a readable format
for gridowner in assets.data.grid_owners:
    print(f"Grid Owner: {gridowner.name}")
    for facility in gridowner.facilities:
        print("\n")
        print(f"  Facility: {facility.name}")
        print(f"  ID: {facility.id}")
        if facility.line:  # A Facility can have zero or one line
            print(f"  Line ID: {facility.line.id}")
            print(f"  Line Name: {facility.line.name}")
            for span in facility.line.spans:
                print(f"    Span: {span.id}")
                print(f"    Span: {span.mast_name_a}")
                print(f"    Span: {span.mast_name_b}")
                for span_phase in span.span_phases:
                    print(f"      Span Phase id: {span_phase.id}")
                    print(f"      Span Phase name: {span_phase.name}")
