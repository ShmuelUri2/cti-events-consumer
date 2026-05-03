import { CallStatus } from './callStatus';

/**
 * Represents a joined call lifecycle event published to the "joined-call-events" output stream.
 */
export interface CallEvent {
  callId: string;
  status: CallStatus;
  agentId?: string;
  agentName?: string;
  customerId?: string;
  phoneNumber?: string;
  businessData: Record<string, string>;
  timestamp: string;
}

/**
 * Converts a CallEvent to a flat key-value map for publishing to a Redis Stream.
 * Business data keys are namespaced with a "data." prefix.
 */
export function callEventToMap(event: CallEvent): Record<string, string> {
  const map: Record<string, string> = {};
  map.callId = event.callId;
  map.status = event.status;
  if (event.agentId !== undefined) map.agentId = event.agentId;
  if (event.agentName !== undefined) map.agentName = event.agentName;
  if (event.customerId !== undefined) map.customerId = event.customerId;
  if (event.phoneNumber !== undefined) map.phoneNumber = event.phoneNumber;
  if (event.businessData) {
    for (const [k, v] of Object.entries(event.businessData)) {
      map[`data.${k}`] = v;
    }
  }
  map.timestamp = event.timestamp;
  return map;
}
