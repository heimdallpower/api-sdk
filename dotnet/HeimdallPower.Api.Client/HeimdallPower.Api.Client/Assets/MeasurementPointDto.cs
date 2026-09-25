namespace HeimdallPower.Api.Client.Assets;

/// <summary>
/// A measurement point is a position on a span phase where a Heimdall Neuron is or has been installed.
/// It is the finest level of the asset hierarchy. Retired measurement points remain in the response so
/// that historical measurements stay attributable.
/// </summary>
public record MeasurementPointDto
{
    /// <summary>
    /// Unique identifier of the measurement point.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid Id { get; init; }

    /// <summary>
    /// The sub-conductor of the span phase that the measurement point sits on, from 1 up to the number of sub-conductors on the span.
    /// </summary>
    /// <example>1</example>
    public int SubConductorNumber { get; init; }

    /// <summary>
    /// The timestamp when Heimdall Power registered the Neuron installation. Not necessarily when the Neuron was physically installed.
    /// </summary>
    public DateTimeOffset RegisteredTimestamp { get; init; }

    /// <summary>
    /// The timestamp when the Neuron was uninstalled. Null while a Neuron is installed.
    /// </summary>
    public DateTimeOffset? UnregisteredTimestamp { get; init; }
}
