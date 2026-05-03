/**
 * Represents an event from the "business-data-events" stream.
 *
 * Contains arbitrary key-value business context data related to a call.
 * Any field in the Redis Stream message other than `callId` and `timestamp`
 * is treated as a business data key-value pair.
 *
 * Examples of keys: `skillName`, `priority`, `queueId`, `language`, etc.
 */
export interface BusinessDataEvent {
  callId: string;
  timestamp: string;
  data: Record<string, string>;
}
