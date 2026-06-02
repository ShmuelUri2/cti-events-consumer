using StackExchange.Redis;
using StreamsJoiner.Models;

namespace StreamsJoiner.Services;

/// <summary>
/// Your implementation goes here.
/// <para>
/// This is the starting point for the exercise. It runs as a hosted background service:
/// the application host starts it on launch and stops it on shutdown.
/// </para>
/// <para>
/// A configured <see cref="IConnectionMultiplexer"/> is injected and ready to use —
/// call <c>_redis.GetDatabase()</c> to read from and write to Redis Streams.
/// </para>
/// <para>
/// You are free to restructure this class, add new classes/files, and organize your
/// solution however you like. Model types live in <see cref="StreamsJoiner.Models"/>.
/// </para>
/// </summary>
public class CallJoinerService : BackgroundService
{
    private readonly IConnectionMultiplexer _redis;
    private readonly ILogger<CallJoinerService> _logger;

    public CallJoinerService(IConnectionMultiplexer redis, ILogger<CallJoinerService> logger)
    {
        _redis = redis;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("CallJoinerService started. Implement your stream-joining logic here.");

        // ---------------------------------------------------------------------
        // Your implementation goes here.
        //
        // Suggested starting points (using the injected _redis connection):
        //   var db = _redis.GetDatabase();
        //   - Read from the input streams: "agent-events", "customer-events",
        //     "business-data-events" (e.g. db.StreamReadAsync / db.StreamRead).
        //   - Parse entries into AgentEvent / CustomerEvent / BusinessDataEvent.
        //   - Correlate by callId and track each call's state.
        //   - Publish CallEvent.ToMap() to the "joined-call-events" output stream
        //     (e.g. db.StreamAddAsync("joined-call-events", entries)).
        // ---------------------------------------------------------------------

        // Keep the service alive until shutdown is requested.
        await Task.Delay(Timeout.Infinite, stoppingToken);
    }
}
