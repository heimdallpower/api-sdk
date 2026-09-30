using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingAssets;

/// <summary>
/// Verifies that <see cref="HeimdallApiClientAssetsExtensions.GetInstrumentedLinesAsync"/> keeps only lines with an
/// active measurement point (unregistered timestamp null or in the future), maps each to its facility, and returns
/// only the active points.
/// </summary>
[Trait("Category", "Unit")]
public class GetInstrumentedLines
{
    private static readonly Guid FacilityWithActive = Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");
    private static readonly Guid FacilityWithFutureUnregistration = Guid.Parse("dddddddd-dddd-dddd-dddd-dddddddddddd");
    private static readonly Guid LineWithActive = Guid.Parse("a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1");
    private static readonly Guid LineWithFutureUnregistration = Guid.Parse("d1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1");
    private static readonly Guid ActiveOnFirstSpan = Guid.Parse("44444444-4444-4444-4444-444444444444");
    private static readonly Guid ActiveOnSecondSpan = Guid.Parse("77777777-7777-7777-7777-777777777777");
    private static readonly Guid UnregistersInFuture = Guid.Parse("88888888-8888-8888-8888-888888888888");

    private static readonly string Future = DateTimeOffset.UtcNow.AddYears(1).ToString("yyyy-MM-ddTHH:mm:ssZ");

    private static readonly string Json = $$"""
        {
          "data": {
            "grid_owners": [
              {
                "name": "Grid owner A",
                "facilities": [
                  {
                    "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                    "name": "Facility with active point",
                    "nominal_voltage": 132000,
                    "components": [],
                    "line": {
                      "id": "a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1",
                      "name": "Line with active point",
                      "available_forecast_hours": 72,
                      "spans": [
                        {
                          "id": "11111111-1111-1111-1111-111111111111",
                          "span_phases": [
                            {
                              "id": "33333333-3333-3333-3333-333333333333",
                              "name": "Phase A",
                              "measurement_points": [
                                { "id": "44444444-4444-4444-4444-444444444444", "sub_conductor_number": 1, "registered_timestamp": "2026-03-15T09:30:00Z", "unregistered_timestamp": null },
                                { "id": "55555555-5555-5555-5555-555555555555", "sub_conductor_number": 1, "registered_timestamp": "2024-07-01T12:00:00Z", "unregistered_timestamp": "2026-03-15T09:00:00Z" }
                              ]
                            }
                          ]
                        },
                        {
                          "id": "22222222-2222-2222-2222-222222222222",
                          "span_phases": [
                            {
                              "id": "66666666-6666-6666-6666-666666666666",
                              "name": "Phase B",
                              "measurement_points": [
                                { "id": "77777777-7777-7777-7777-777777777777", "sub_conductor_number": 2, "registered_timestamp": "2025-01-01T00:00:00Z" }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  },
                  {
                    "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                    "name": "Facility with only retired points",
                    "nominal_voltage": 132000,
                    "components": [],
                    "line": {
                      "id": "b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1",
                      "name": "Decommissioned line",
                      "available_forecast_hours": 72,
                      "spans": [
                        {
                          "id": "b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2",
                          "span_phases": [
                            {
                              "id": "b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3",
                              "measurement_points": [
                                { "id": "b4b4b4b4-b4b4-b4b4-b4b4-b4b4b4b4b4b4", "sub_conductor_number": 1, "registered_timestamp": "2024-07-01T12:00:00Z", "unregistered_timestamp": "2025-07-01T12:00:00Z" }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  },
                  {
                    "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
                    "name": "Facility without neurons",
                    "nominal_voltage": 132000,
                    "components": [],
                    "line": {
                      "id": "c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1",
                      "name": "Line without neurons",
                      "available_forecast_hours": 72,
                      "spans": [
                        {
                          "id": "c2c2c2c2-c2c2-c2c2-c2c2-c2c2c2c2c2c2",
                          "span_phases": [
                            { "id": "c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3", "measurement_points": [] }
                          ]
                        }
                      ]
                    }
                  },
                  {
                    "id": "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
                    "name": "Facility without line",
                    "nominal_voltage": 0,
                    "components": [],
                    "line": null
                  }
                ]
              },
              {
                "name": "Grid owner B",
                "facilities": [
                  {
                    "id": "dddddddd-dddd-dddd-dddd-dddddddddddd",
                    "name": "Facility with future unregistration",
                    "nominal_voltage": 66000,
                    "components": [],
                    "line": {
                      "id": "d1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1",
                      "name": "Line with future unregistration",
                      "available_forecast_hours": 48,
                      "spans": [
                        {
                          "id": "d2d2d2d2-d2d2-d2d2-d2d2-d2d2d2d2d2d2",
                          "span_phases": [
                            {
                              "id": "d3d3d3d3-d3d3-d3d3-d3d3-d3d3d3d3d3d3",
                              "measurement_points": [
                                { "id": "88888888-8888-8888-8888-888888888888", "sub_conductor_number": 1, "registered_timestamp": "2025-01-01T00:00:00Z", "unregistered_timestamp": "{{Future}}" }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  }
                ]
              }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldRequestAssetsOnce()
    {
        var handler = new RecordingHttpMessageHandler(Json);

        await HeimdallApiClientFactory.Create(handler).GetInstrumentedLinesAsync();

        var request = Assert.Single(handler.Requests);
        Assert.Equal("/assets/v1/assets", request.RequestUri!.AbsolutePath);
    }

    [Fact]
    public async Task ShouldKeepOnlyLinesWithActiveMeasurementPoints()
    {
        var lines = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(Json)).GetInstrumentedLinesAsync();

        Assert.Equal([LineWithActive, LineWithFutureUnregistration], lines.Select(l => l.Line.Id));
    }

    [Fact]
    public async Task ShouldMapEachLineToItsFacility()
    {
        var lines = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(Json)).GetInstrumentedLinesAsync();

        Assert.Collection(lines,
            first =>
            {
                Assert.Equal(FacilityWithActive, first.Facility.Id);
                Assert.Equal("Facility with active point", first.Facility.Name);
                Assert.Equal(132000, first.Facility.NominalVoltage);
                Assert.Equal("Line with active point", first.Line.Name);
                Assert.Same(first.Facility.Line, first.Line);
            },
            second =>
            {
                Assert.Equal(FacilityWithFutureUnregistration, second.Facility.Id);
                Assert.Equal("Facility with future unregistration", second.Facility.Name);
                Assert.Equal(48, second.Line.AvailableForecastHours);
                Assert.Same(second.Facility.Line, second.Line);
            });
    }

    [Fact]
    public async Task ShouldReturnOnlyActiveMeasurementPointsAcrossAllSpans()
    {
        var lines = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(Json)).GetInstrumentedLinesAsync();

        var line = lines.Single(l => l.Line.Id == LineWithActive);
        Assert.Collection(line.ActiveMeasurementPoints,
            first =>
            {
                Assert.Equal(ActiveOnFirstSpan, first.Id);
                Assert.Null(first.UnregisteredTimestamp);
            },
            second =>
            {
                Assert.Equal(ActiveOnSecondSpan, second.Id);
                Assert.Equal(2, second.SubConductorNumber);
            });
    }

    [Fact]
    public async Task ShouldTreatFutureUnregisteredTimestampAsActive()
    {
        var lines = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(Json)).GetInstrumentedLinesAsync();

        var point = Assert.Single(lines.Single(l => l.Line.Id == LineWithFutureUnregistration).ActiveMeasurementPoints);
        Assert.Equal(UnregistersInFuture, point.Id);
        Assert.True(point.UnregisteredTimestamp > DateTimeOffset.UtcNow);
    }

    [Fact]
    public async Task InstrumentedLinesShouldMatchTheClientHelper_WhenCalledOnAssets()
    {
        var client = HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(Json));

        var fromAssets = (await client.GetAssetsAsync()).InstrumentedLines();

        Assert.Equal([LineWithActive, LineWithFutureUnregistration], fromAssets.Select(l => l.Line.Id));
        Assert.Equal([FacilityWithActive, FacilityWithFutureUnregistration], fromAssets.Select(l => l.Facility.Id));
    }

    [Fact]
    public void InstrumentedLinesShouldBeEmpty_WhenNoGridOwners()
    {
        var assets = new AssetsResponse { GridOwners = [] };

        Assert.Empty(assets.InstrumentedLines());
    }
}
