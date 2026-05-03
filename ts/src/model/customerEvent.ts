import { CustomerEventType } from './callStatus';

/**
 * Represents an event from the "customer-events" stream.
 * Customers call in to the call center or hang up.
 */
export interface CustomerEvent {
  callId: string;
  eventType: CustomerEventType;
  customerId: string;
  phoneNumber?: string;
  timestamp: string;
}
