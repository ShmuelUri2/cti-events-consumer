export enum CallStatus {
  STARTED = 'STARTED',
  CONNECTED = 'CONNECTED',
  DISCONNECTED = 'DISCONNECTED',
  ENDED = 'ENDED',
}

export enum AgentEventType {
  AGENT_JOINED = 'AGENT_JOINED',
  AGENT_LEFT = 'AGENT_LEFT',
}

export enum CustomerEventType {
  CUSTOMER_JOINED = 'CUSTOMER_JOINED',
  CUSTOMER_LEFT = 'CUSTOMER_LEFT',
}
