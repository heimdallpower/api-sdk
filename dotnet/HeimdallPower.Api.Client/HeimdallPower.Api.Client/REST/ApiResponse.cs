namespace HeimdallPower.Api.Client.REST;

public class ApiResponse<T> where T : class
{
    public required T Data { get; set; }
}
