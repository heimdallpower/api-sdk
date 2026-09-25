using HeimdallPower.Api.Client.Assets;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// The facility and asset ids of one line, resolved from <see cref="HeimdallApiClient.GetAssetsAsync"/>,
/// so responses can be cross-checked against the real asset hierarchy.
/// </summary>
public sealed class LineAssets
{
    public const string AmpereUnit = "Ampere";
    public const string MvaUnit = "MVA";

    // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
    public static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

    private LineAssets(FacilityDto facility)
    {
        Facility = facility;
        var spans = facility.Line!.Spans;
        SpanIds = spans.Select(s => s.Id).ToHashSet();
        SpanPhaseIds = spans.SelectMany(s => s.SpanPhases).Select(sp => sp.Id).ToHashSet();
        MeasurementPointIds = spans.SelectMany(s => s.SpanPhases).SelectMany(sp => sp.MeasurementPoints).Select(mp => mp.Id).ToHashSet();
    }

    public FacilityDto Facility { get; }
    public Guid LineId => Facility.Line!.Id;
    public Guid FacilityId => Facility.Id;
    public IReadOnlySet<Guid> SpanIds { get; }
    public IReadOnlySet<Guid> SpanPhaseIds { get; }
    public IReadOnlySet<Guid> MeasurementPointIds { get; }

    /// <summary>
    /// The phase-to-phase voltage the API uses to convert amperes to MVA:
    /// the operational voltage when set and positive, otherwise the nominal voltage.
    /// </summary>
    public double ApparentPowerVoltage => Facility.OperationalVoltage is > 0 ? Facility.OperationalVoltage.Value : Facility.NominalVoltage;

    public static LineAssets Resolve(AssetsResponse assets, Guid lineId)
    {
        var facility = assets.AllFacilities().SingleOrDefault(f => f.Line?.Id == lineId)
                       ?? throw new InvalidOperationException($"Line {lineId} was not found in the assets hierarchy.");
        return new LineAssets(facility);
    }

    /// <summary>
    /// Asserts that <paramref name="mva"/> is the three-phase apparent power of <paramref name="amperes"/>
    /// at this line's voltage: S = sqrt(3) * V * I / 1,000,000.
    /// </summary>
    public void AssertIsApparentPowerOf(double mva, double amperes, string context)
    {
        var expected = Math.Sqrt(3) * ApparentPowerVoltage * amperes / 1_000_000;
        var tolerance = Math.Max(Math.Abs(expected) * 0.005, 1e-6);
        Assert.True(Math.Abs(mva - expected) <= tolerance,
            $"{context}: {mva} MVA should equal sqrt(3) * {ApparentPowerVoltage} V * {amperes} A = {expected} MVA");
    }
}
