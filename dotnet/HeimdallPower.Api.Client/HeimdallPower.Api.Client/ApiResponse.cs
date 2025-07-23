namespace HeimdallPower.Api.Client;

public class ApiResponse<T> where T : class
{
    public T Data { get; set; }
    public string Message { get; set; }
}
