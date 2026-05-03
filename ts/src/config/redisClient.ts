import Redis from 'ioredis';

export interface RedisConfig {
  host: string;
  port: number;
}

export function loadRedisConfig(): RedisConfig {
  const host = process.env.SPRING_DATA_REDIS_HOST ?? process.env.REDIS_HOST ?? 'localhost';
  const portStr = process.env.SPRING_DATA_REDIS_PORT ?? process.env.REDIS_PORT ?? '6379';
  return { host, port: Number.parseInt(portStr, 10) };
}

export function createRedis(config: RedisConfig = loadRedisConfig()): Redis {
  return new Redis({
    host: config.host,
    port: config.port,
    lazyConnect: false,
    maxRetriesPerRequest: null,
  });
}
