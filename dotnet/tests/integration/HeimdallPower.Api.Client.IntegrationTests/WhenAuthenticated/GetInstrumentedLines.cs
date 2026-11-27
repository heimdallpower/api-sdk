using System.Net;
using HeimdallPower.Api.Client.Assets;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Fetches the instrumented lines and the latest current for each, proving the helper only returns lines
/// with active measurement points that the data endpoints can serve. The latest current uses the API's default
/// <c>since</c> (20 minutes), so a line that has not reported in that time answers 404, which is not a failure.
/// </summary>
[Trait("Category", "Integration")]
public class GetInstrumentedLines(GetInstrumentedLines.Scenario scenario) : IClassFixture<GetInstrumentedLines.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public IReadOnlyList<InstrumentedLine> Result { get; }
        public AssetsResponse Assets { get; }
        public IReadOnlyDictionary<Guid, HttpStatusCode?> LatestCurrentFailures { get; }

        public Scenario()
        {
            Result = Client.GetInstrumentedLinesAsync().GetAwaiter().GetResult();
            Assets = Client.GetAssetsAsync().GetAwaiter().GetResult();

            var failures = new Dictionary<Guid, HttpStatusCode?>();
            foreach (var instrumented in Result)
            {
                try
                {
                    Client.GetLatestCurrentAsync(instrumented.Line.Id).GetAwaiter().GetResult();
                }
                catch (HeimdallApiException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
                {
                    // No current in the last 20 minutes (the API's default since): not a failure.
                }
                catch (HeimdallApiException ex)
                {
                    failures[instrumented.Line.Id] = ex.StatusCode;
                }
            }

            LatestCurrentFailures = failures;
        }
    }

    [Fact]
    public void EveryLineShouldHaveAnActiveMeasurementPoint()
    {
        // The test client has lines with installed Neurons; an empty result means the filter dropped them all.
        Assert.NotEmpty(scenario.Result);
        var now = DateTimeOffset.UtcNow;
        Assert.All(scenario.Result, instrumented =>
        {
            Assert.NotEmpty(instrumented.ActiveMeasurementPoints);
            Assert.All(instrumented.ActiveMeasurementPoints, mp =>
                Assert.True(mp.UnregisteredTimestamp is null || mp.UnregisteredTimestamp > now,
                    $"Measurement point {mp.Id} on line {instrumented.Line.Id} is retired"));
        });
    }

    [Fact]
    public void EveryLineShouldBelongToItsFacilityInTheAssets()
    {
        var facilities = scenario.Assets.AllFacilities().ToDictionary(f => f.Id);
        Assert.All(scenario.Result, instrumented =>
        {
            Assert.True(facilities.TryGetValue(instrumented.Facility.Id, out var facility), $"Facility {instrumented.Facility.Id} not in assets");
            Assert.Equal(facility!.Line?.Id, instrumented.Line.Id);
        });
    }

    [Fact]
    public void ActiveMeasurementPointsShouldExistOnTheLineInTheAssets()
    {
        Assert.All(scenario.Result, instrumented =>
        {
            var line = LineAssets.Resolve(scenario.Assets, instrumented.Line.Id);
            Assert.All(instrumented.ActiveMeasurementPoints, mp => Assert.Contains(mp.Id, line.MeasurementPointIds));
        });
    }

    [Fact]
    public void LatestCurrentShouldSucceedOrReportNoRecentDataForEveryInstrumentedLine()
    {
        Assert.True(scenario.LatestCurrentFailures.Count == 0,
            "Latest current failed for lines: " + string.Join(", ", scenario.LatestCurrentFailures.Select(f => $"{f.Key} ({(int?)f.Value})")));
    }
}
