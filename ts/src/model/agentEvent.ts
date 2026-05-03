import { AgentEventType } from './callStatus';

/**
 * Represents an event from the "agent-events" stream.
 * Agents join or leave calls.
 */
export interface AgentEvent {
  callId: string;
  eventType: AgentEventType;
  agentId: string;
  agentName?: string;
  timestamp: string;
}
