namespace HeimdallPower.Api.Client;

/// <summary>
/// Represents a generic API response that encapsulates a data payload of type T.
/// </summary>
/// <typeparam name="T">The type of data contained in the response.</typeparam>
public class ApiResponse<T> where T : class
{
    /// <summary>
    /// Gets or sets the data payload of the API response.
    /// </summary>
    /// <remarks>
    /// This property represents the core data within the API response object.
    /// It holds the deserialized content of type T, which is defined when creating an instance
    /// of <see cref="ApiResponse{T}"/>.
    /// </remarks>
    public required T Data { get; set; }
}
