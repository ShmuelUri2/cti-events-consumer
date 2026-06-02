using StackExchange.Redis;
using StreamsJoiner.Services;

var builder = Host.CreateApplicationBuilder(args);

// Redis connection settings (from appsettings.json, overridable via Redis__Host / Redis__Port env vars).
var redisHost = builder.Configuration["Redis:Host"] ?? "localhost";
var redisPort = builder.Configuration["Redis:Port"] ?? "6379";

// Register a single shared Redis connection for the whole application.
builder.Services.AddSingleton<IConnectionMultiplexer>(_ =>
    ConnectionMultiplexer.Connect($"{redisHost}:{redisPort}"));

// Register the candidate's stream-joining service as a hosted background service.
builder.Services.AddHostedService<CallJoinerService>();

var host = builder.Build();
host.Run();
