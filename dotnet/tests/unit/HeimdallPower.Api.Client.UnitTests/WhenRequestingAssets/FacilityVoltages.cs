using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingAssets;

/// <summary>
/// Verifies that the facility voltages used for apparent-power conversions deserialize.
/// </summary>
[Trait("Category", "Unit")]
public class FacilityVoltages
{
    private const string Json = """
        {
          "data": {
            "grid_owners": [
              {
                "name": "Grid owner A",
                "facilities": [
                  { "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "name": "With operational voltage", "nominal_voltage": 132000, "operational_voltage": 130000, "components": [], "line": null },
                  { "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "name": "Nominal only", "nominal_voltage": 66000, "operational_voltage": null, "components": [], "line": null }
                ]
              }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldDeserializeNominalAndOperationalVoltage()
    {
        var facilities = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(Json)).GetFacilitiesAsync();

        Assert.Collection(facilities,
            withOperational =>
            {
                Assert.Equal(132000, withOperational.NominalVoltage);
                Assert.Equal(130000, withOperational.OperationalVoltage);
            },
            nominalOnly =>
            {
                Assert.Equal(66000, nominalOnly.NominalVoltage);
                Assert.Null(nominalOnly.OperationalVoltage);
            });
    }
}
