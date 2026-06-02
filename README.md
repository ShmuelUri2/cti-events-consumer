# Stream Joiner — Interview Exercise

## About

This is a coding exercise used during technical interviews. The exercise details will be provided by your interviewer at the start of the session.

---

## Quick Start

### Prerequisites

- Docker & Docker Compose

### Run

```bash
docker-compose up --build
```

This starts four services:
1. **Redis** — the streaming backbone (port 6379)
2. **RedisInsight** — web UI for monitoring streams at [http://localhost:5540](http://localhost:5540)
3. **Event Generator** — continuously produces events to Redis Streams
4. **Streams Joiner App** — your .NET worker service

### Inspect Streams

**Via RedisInsight UI** — Open [http://localhost:5540](http://localhost:5540), add a database connection with host `redis` and port `6379`, then browse the streams visually.

**Via `redis-cli`:**

```bash
docker exec -it streams-joiner-redis-1 redis-cli XRANGE agent-events - +
docker exec -it streams-joiner-redis-1 redis-cli XRANGE customer-events - +
docker exec -it streams-joiner-redis-1 redis-cli XRANGE business-data-events - +
docker exec -it streams-joiner-redis-1 redis-cli XRANGE joined-call-events - +
```

### Rebuild After Code Changes

```bash
docker-compose up --build streams-joiner-app
```

---

## Project Structure

| Component | Purpose |
|-----------|---------|
| `Program.cs` | Application entry point — bootstraps the host and Redis connection |
| `Services/CallJoinerService.cs` | Starting point for your implementation |
| Model classes (`Models/`) | `AgentEvent`, `CustomerEvent`, `BusinessDataEvent`, `CallEvent` |
| `appsettings.json` | Redis connection configuration |
| `StreamsJoiner.csproj` | Project file — dependency: `StackExchange.Redis` |
| Docker Compose | Redis + RedisInsight + event generator + app |

You may create new classes, namespaces, and configuration files as needed.
