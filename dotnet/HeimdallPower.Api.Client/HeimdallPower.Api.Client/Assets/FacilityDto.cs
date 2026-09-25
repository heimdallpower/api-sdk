namespace HeimdallPower.Api.Client.Assets;

/// <summary>
/// A facility is a collection of components that allows grid owners to define limiting components and configurations for a power line.
/// Among the components that a facility can have is a line.
/// A facility can have zero or one line.
/// </summary>
public record FacilityDto
{
    /// <summary>
    /// Unique identifier of the facility.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid Id { get; init; }

    /// <summary>
    /// Name of the facility.
    /// </summary>
    /// <example>Facility A</example>
    public required string Name { get; init; }

    /// <summary>
    /// The facility's nominal (rated) phase-to-phase voltage in volts.
    /// Used in apparent-power calculations as a fallback when <see cref="OperationalVoltage"/> is not set or not positive.
    /// </summary>
    /// <example>132000</example>
    public double NominalVoltage { get; init; }

    /// <summary>
    /// The facility's operational phase-to-phase voltage in volts, if configured.
    /// When set and positive, this value is preferred over <see cref="NominalVoltage"/> for apparent-power calculations.
    /// </summary>
    /// <example>130000</example>
    public double? OperationalVoltage { get; init; }

    /// <summary>
    /// Line associated with the facility, if available.
    /// </summary>
    public LineDto? Line { get; init; }

    /// <summary>
    /// List of components associated with the facility
    /// </summary>
    public required IReadOnlyList<FacilityComponentDto> Components { get; init; }
}
