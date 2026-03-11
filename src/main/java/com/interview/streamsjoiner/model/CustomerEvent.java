package com.interview.streamsjoiner.model;

/**
 * Represents an event from the "customer-events" stream.
 * Customers call in to the call center or hang up.
 */
public class CustomerEvent {

    private String callId;
    private CustomerEventType eventType;
    private String customerId;
    private String phoneNumber;
    private String timestamp;

    public CustomerEvent() {
    }

    public CustomerEvent(String callId, CustomerEventType eventType, String customerId, String phoneNumber, String timestamp) {
        this.callId = callId;
        this.eventType = eventType;
        this.customerId = customerId;
        this.phoneNumber = phoneNumber;
        this.timestamp = timestamp;
    }

    public String getCallId() {
        return callId;
    }

    public void setCallId(String callId) {
        this.callId = callId;
    }

    public CustomerEventType getEventType() {
        return eventType;
    }

    public void setEventType(CustomerEventType eventType) {
        this.eventType = eventType;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "CustomerEvent{callId='" + callId + "', eventType='" + eventType +
                "', customerId='" + customerId + "', phoneNumber='" + phoneNumber +
                "', timestamp='" + timestamp + "'}";
    }
}
