using HeimdallPower.Api.Client.Assets;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

[Trait("Category", "Integration")]
public class GetAssets(GetAssets.Scenario scenario) : IClassFixture<GetAssets.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public Scenario()
        {
            Result = Client.GetAssetsAsync().GetAwaiter().GetResult();
        }

        public AssetsResponse Result { get; }
    }

    [Fact]
    public void ShouldReturnAssets()
    {
        Assert.NotNull(scenario.Result);
    }

    [Fact]
    public void ResultShouldIncludeGridOwners()
    {
        Assert.NotNull(scenario.Result.GridOwners);
    }

    [Fact]
    public void ResultShouldIncludeLines()
    {
        Assert.NotEmpty(scenario.Result.AllLines());
    }

    [Fact]
    public void ResultShouldIncludeFacilities()
    {
        Assert.NotEmpty(scenario.Result.AllFacilities());
    }

    [Fact]
    public void ResultShouldIncludeMeasurementPoints()
    {
        Assert.NotEmpty(scenario.Result.AllMeasurementPoints());
    }

    [Fact]
    public void AllFacilitiesShouldHaveNonNegativeVoltages()
    {
        Assert.All(scenario.Result.AllFacilities(), facility =>
        {
            Assert.True(facility.NominalVoltage >= 0, $"Facility {facility.Id} nominal voltage {facility.NominalVoltage} V should not be negative");
            Assert.True(facility.OperationalVoltage is null or >= 0, $"Facility {facility.Id} operational voltage {facility.OperationalVoltage} V should not be negative");
        });
    }

    [Fact]
    public void AtLeastOneFacilityShouldHaveANominalVoltage()
    {
        // Guards against the field silently deserializing to its default for every facility.
        Assert.Contains(scenario.Result.AllFacilities(), facility => facility.NominalVoltage > 0);
    }

    [Fact]
    public void OperationalVoltageShouldBeNearNominal_WhenBothAreSet()
    {
        // Grids run within a few percent of nominal; 20 % catches unit mix-ups (V vs kV) without being brittle.
        var facilities = scenario.Result.AllFacilities().Where(f => f is { NominalVoltage: > 0, OperationalVoltage: > 0 });
        Assert.All(facilities, facility =>
        {
            var ratio = facility.OperationalVoltage!.Value / facility.NominalVoltage;
            Assert.InRange(ratio, 0.8, 1.2);
        });
    }
}
