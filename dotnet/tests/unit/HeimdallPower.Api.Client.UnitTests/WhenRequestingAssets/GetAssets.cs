using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingAssets;

/// <summary>
/// Verifies that measurement points in the assets hierarchy deserialize, including retired ones,
/// and that <see cref="AssetsResponseExtensions.AllMeasurementPoints"/> flattens them.
/// </summary>
[Trait("Category", "Unit")]
public class GetAssets
{
    private static readonly Guid ActiveMeasurementPoint = Guid.Parse("44444444-4444-4444-4444-444444444444");
    private static readonly Guid RetiredMeasurementPoint = Guid.Parse("55555555-5555-5555-5555-555555555555");

    private const string Json = """
        {
          "data": {
            "grid_owners": [
              {
                "name": "Grid owner A",
                "facilities": [
                  {
                    "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                    "name": "Facility A",
                    "nominal_voltage": 132000,
                    "operational_voltage": null,
                    "components": [],
                    "line": {
                      "id": "d67d2205-6629-4bbd-aa9f-436bf22842ad",
                      "name": "Line A",
                      "available_forecast_hours": 72,
                      "spans": [
                        {
                          "id": "11111111-1111-1111-1111-111111111111",
                          "mast_name_a": "Mast A",
                          "mast_name_b": "Mast B",
                          "span_phases": [
                            {
                              "id": "33333333-3333-3333-3333-333333333333",
                              "name": "Phase A",
                              "measurement_points": [
                                {
                                  "id": "44444444-4444-4444-4444-444444444444",
                                  "sub_conductor_number": 1,
                                  "registered_timestamp": "2026-03-15T09:30:00Z",
                                  "unregistered_timestamp": null
                                },
                                {
                                  "id": "55555555-5555-5555-5555-555555555555",
                                  "sub_conductor_number": 1,
                                  "registered_timestamp": "2024-07-01T12:00:00.001Z",
                                  "unregistered_timestamp": "2026-03-15T09:00:00Z"
                                }
                              ]
                            },
                            {
                              "id": "66666666-6666-6666-6666-666666666666",
                              "name": "Phase B",
                              "measurement_points": []
                            }
                          ]
                        }
                      ]
                    }
                  },
                  {
                    "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                    "name": "Facility without line",
                    "nominal_voltage": 0,
                    "components": [],
                    "line": null
                  }
                ]
              }
            ]
          }
        }
        """;

    private static async Task<AssetsResponse> Fetch() =>
        await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(Json)).GetAssetsAsync();

    [Fact]
    public async Task ShouldDeserializeActiveAndRetiredMeasurementPoints()
    {
        var assets = await Fetch();

        var spanPhase = assets.AllLines().Single()!.Spans.Single().SpanPhases.First();
        Assert.Collection(spanPhase.MeasurementPoints,
            active =>
            {
                Assert.Equal(ActiveMeasurementPoint, active.Id);
                Assert.Equal(1, active.SubConductorNumber);
                Assert.Equal(new DateTimeOffset(2026, 3, 15, 9, 30, 0, TimeSpan.Zero), active.RegisteredTimestamp);
                Assert.Null(active.UnregisteredTimestamp);
            },
            retired =>
            {
                Assert.Equal(RetiredMeasurementPoint, retired.Id);
                Assert.Equal(new DateTimeOffset(2026, 3, 15, 9, 0, 0, TimeSpan.Zero), retired.UnregisteredTimestamp);
            });
    }

    [Fact]
    public async Task SpanPhaseWithoutNeuronShouldHaveNoMeasurementPoints()
    {
        var assets = await Fetch();

        var spanPhase = assets.AllLines().Single()!.Spans.Single().SpanPhases.Last();
        Assert.Empty(spanPhase.MeasurementPoints);
    }

    [Fact]
    public async Task AllMeasurementPointsShouldFlattenAcrossLinesAndSkipFacilitiesWithoutLine()
    {
        var assets = await Fetch();

        var ids = assets.AllMeasurementPoints().Select(mp => mp.Id);

        Assert.Equal([ActiveMeasurementPoint, RetiredMeasurementPoint], ids);
    }

    [Fact]
    public void MeasurementPointsShouldDefaultToEmpty_WhenConstructedWithoutThem()
    {
        var spanPhase = new SpanPhaseDto { Id = Guid.NewGuid(), Name = "Phase A" };

        Assert.Empty(spanPhase.MeasurementPoints);
    }
}
