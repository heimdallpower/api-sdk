using System.Text;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming.Fakes;

/// <summary>
/// A stream that yields a fixed initial payload, then blocks (respecting cancellation) as if the
/// connection were still open with no further data - used to test clean cancellation mid-stream.
/// </summary>
internal sealed class NeverEndingSseStream(string initialBody) : System.IO.Stream
{
    private readonly byte[] _initial = Encoding.UTF8.GetBytes(initialBody);
    private int _position;

    public override bool CanRead => true;
    public override bool CanSeek => false;
    public override bool CanWrite => false;
    public override long Length => throw new NotSupportedException();
    public override long Position { get => throw new NotSupportedException(); set => throw new NotSupportedException(); }

    public override int Read(byte[] buffer, int offset, int count) =>
        ReadAsync(buffer, offset, count, CancellationToken.None).GetAwaiter().GetResult();

    public override async Task<int> ReadAsync(byte[] buffer, int offset, int count, CancellationToken cancellationToken)
    {
        if (_position < _initial.Length)
        {
            var toCopy = Math.Min(count, _initial.Length - _position);
            Array.Copy(_initial, _position, buffer, offset, toCopy);
            _position += toCopy;
            return toCopy;
        }

        await Task.Delay(Timeout.Infinite, cancellationToken);
        return 0;
    }

    public override void Flush() { }
    public override long Seek(long offset, SeekOrigin origin) => throw new NotSupportedException();
    public override void SetLength(long value) => throw new NotSupportedException();
    public override void Write(byte[] buffer, int offset, int count) => throw new NotSupportedException();
}
