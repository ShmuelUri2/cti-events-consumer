import http from 'node:http';
import pino from 'pino';

import { createRedis, loadRedisConfig } from './config/redisClient';
import { CallJoinerService } from './service/callJoinerService';

const log = pino({ name: 'streams-joiner' });

const HTTP_PORT = Number.parseInt(process.env.PORT ?? '8080', 10);

async function main(): Promise<void> {
  const config = loadRedisConfig();
  log.info({ host: config.host, port: config.port }, 'Starting streams-joiner (TypeScript)');

  const redis = createRedis(config);
  const service = new CallJoinerService();
  void service;

  const server = http.createServer((_req, res) => {
    res.statusCode = 404;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Not Found');
  });
  server.listen(HTTP_PORT, () => {
    log.info({ port: HTTP_PORT }, 'streams-joiner started');
  });

  const shutdown = async (signal: string): Promise<void> => {
    log.info({ signal }, 'Shutting down');
    server.close();
    await redis.quit().catch(() => undefined);
    process.exit(0);
  };

  process.on('SIGINT', () => void shutdown('SIGINT'));
  process.on('SIGTERM', () => void shutdown('SIGTERM'));
}

main().catch((err) => {
  log.error({ err }, 'Fatal error');
  process.exit(1);
});
