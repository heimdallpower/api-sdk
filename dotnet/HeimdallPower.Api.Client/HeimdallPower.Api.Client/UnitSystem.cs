namespace HeimdallPower.Api.Client;

/// <summary>
/// The unit system used for measurement values in a response.
/// </summary>
public enum UnitSystem
{
    /// <summary>
    /// Metric units (default), e.g. Celsius, kg/m, N and meters.
    /// </summary>
    Metric,

    /// <summary>
    /// Imperial units, e.g. Fahrenheit, lb/ft, lbf and feet.
    /// </summary>
    Imperial,
}

internal static class UnitSystemExtensions
{
    public static string ToQueryValue(this UnitSystem unitSystem) => unitSystem switch
    {
        UnitSystem.Metric => "metric",
        UnitSystem.Imperial => "imperial",
        _ => throw new ArgumentOutOfRangeException(nameof(unitSystem), unitSystem, "Unsupported unit system."),
    };
}
