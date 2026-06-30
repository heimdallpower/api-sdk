using HeimdallPower.Api.Client.CapacityMonitoring.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries historical Heimdall DLR values for "Heimdall Power Line" (2026-01-01).</summary>
[Trait("Category", "Integration")]
public class GetHeimdallDlrs(GetHeimdallDlrs.Scenario scenario) : IClassFixture<GetHeimdallDlrs.Scenario>
{
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To   = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        private static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public HeimdallDlrsResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetHeimdallDlrsAsync(HeimdallPowerLineId, From, To).GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void ShouldReturnResponse()
    {
        Assert.NotNull(scenario.Result);
    }

    [Fact]
    public void ResultShouldHaveMetric()
    {
        Assert.False(string.IsNullOrEmpty(scenario.Result?.Metric), "Metric should not be empty");
    }

    [Fact]
    public void ResultShouldHaveUnit()
    {
        Assert.False(string.IsNullOrEmpty(scenario.Result?.Unit), "Unit should not be empty");
    }

    [Fact]
    public void ResultShouldHaveDlrsList()
    {
        // The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
        Assert.NotNull(scenario.Result?.HeimdallDlrs);
    }

    [Fact]
    public void AllDlrsShouldHaveTimestampsWithinRequestedRange()
    {
        Assert.All(scenario.Result!.HeimdallDlrs, dlr =>
        {
            Assert.True(dlr.Timestamp >= From, $"Timestamp {dlr.Timestamp} is before {From}");
            Assert.True(dlr.Timestamp <= To,   $"Timestamp {dlr.Timestamp} is after {To}");
        });
    }

    [Fact]
    public void AllDlrsShouldHavePositiveValues()
    {
        Assert.All(scenario.Result!.HeimdallDlrs, dlr =>
            Assert.True(dlr.Value > 0, $"DLR value {dlr.Value} at {dlr.Timestamp} should be positive"));
    }
}

