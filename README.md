# Stream Joiner — Interview Exercise

## About

This is a coding exercise used during technical interviews. The exercise details will be provided by your interviewer at the start of the session.

---

## Quick Start

### Prerequisites

- Docker & Docker Compose

### Run

Pick one app implementation via a Compose profile:

```bash
# Java (Spring Boot) — exposed on host port 8081
docker-compose --profile java up --build

# TypeScript (Node.js) — exposed on host port 8082
docker-compose --profile ts up --build
```

This starts four services:
1. **Redis** — the streaming backbone (port 6379)
2. **RedisInsight** — web UI for monitoring streams at [http://localhost:5540](http://localhost:5540)
3. **Event Generator** — continuously produces events to Redis Streams
4. **Streams Joiner App** — Spring Boot (`java` profile) or Node.js / TypeScript (`ts` profile)

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
# Java
docker-compose --profile java up --build streams-joiner-app

# TypeScript
docker-compose --profile ts up --build streams-joiner-app-ts
```

---

## Project Structure

Two equivalent implementations live side by side. Pick the one that matches the language you want to work in.

### Java (Spring Boot) — repo root

| Component | Purpose |
|-----------|---------|
| `StreamsJoinerApplication.java` | Spring Boot entry point |
| `CallJoinerService.java` | Starting point for your implementation |
| Model POJOs | `AgentEvent`, `CustomerEvent`, `BusinessDataEvent`, `CallEvent` |
| `application.yml` | Redis connection configuration |
| `pom.xml` | Dependencies: `spring-boot-starter-data-redis`, `spring-boot-starter-web` |

### TypeScript (Node.js) — `ts/`

| Component | Purpose |
|-----------|---------|
| `ts/src/index.ts` | Application entry point |
| `ts/src/service/callJoinerService.ts` | Starting point for your implementation |
| `ts/src/model/*.ts` | `AgentEvent`, `CustomerEvent`, `BusinessDataEvent`, `CallEvent` types + enums |
| `ts/package.json` | Dependencies: `ioredis`, `pino`, `jest`, `ts-node`, `typescript` |

The Redis streams used (`agent-events`, `customer-events`, `business-data-events`, `joined-call-events`) and the event-generator are shared. You may create new files, modules, and configuration as needed.
