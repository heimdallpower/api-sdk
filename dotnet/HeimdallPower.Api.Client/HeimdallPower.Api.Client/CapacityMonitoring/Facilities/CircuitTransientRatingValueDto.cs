namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

/// <summary>
/// The circuit transient rating for a single duration at a given timestamp, including the limiting facility component.
/// </summary>
public record CircuitTransientRatingValueDto
{
    /// <summary>
    /// The transient rating duration in minutes. Transient ratings are not calculated for durations longer than one hour.
    /// </summary>
    /// <example>10</example>
    public int DurationMinutes { get; init; }

    /// <summary>
    /// The circuit transient rating value for this duration. The unit is given by the Unit property on the response:
    /// amperes for current (default), MVA for apparent power.
    /// </summary>
    /// <example>590.2</example>
    public double Value { get; init; }

    /// <summary>
    /// Facility component ID of the component that caps the circuit transient rating for this duration.
    /// Null when the value is not limited by a facility component, i.e. the line transient rating is the binding constraint.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid? LimitingComponentId { get; init; }
}
