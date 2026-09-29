namespace HeimdallPower.Api.Client;

internal class ApiResponse<T> where T : class
{
    public required T Data { get; set; }
}
