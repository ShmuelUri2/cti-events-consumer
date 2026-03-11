package com.interview.streamsjoiner.model;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Represents a joined call lifecycle event published to the "joined-call-events" output stream.
 *
 * Status values:
 *   STARTED       - First participant (agent or customer) joined the call
 *   CONNECTED     - At least 1 agent AND at least 1 customer are present
 *   DISCONNECTED  - Was connected, but now only one participant type remains
 *   ENDED         - No participants remain on the call
 */
public class CallEvent {

    private String callId;
    private CallStatus status;
    private String agentId;
    private String agentName;
    private String customerId;
    private String phoneNumber;
    private Map<String, String> businessData;
    private String timestamp;

    public CallEvent() {
    }

    public String getCallId() {
        return callId;
    }

    public void setCallId(String callId) {
        this.callId = callId;
    }

    public CallStatus getStatus() {
        return status;
    }

    public void setStatus(CallStatus status) {
        this.status = status;
    }

    public String getAgentId() {
        return agentId;
    }

    public void setAgentId(String agentId) {
        this.agentId = agentId;
    }

    public String getAgentName() {
        return agentName;
    }

    public void setAgentName(String agentName) {
        this.agentName = agentName;
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

    /**
     * Returns all accumulated business data key-value pairs for this call.
     * Keys are arbitrary business field names (e.g., "skillName", "priority", "queueId").
     */
    public Map<String, String> getBusinessData() {
        return businessData;
    }

    public void setBusinessData(Map<String, String> businessData) {
        this.businessData = businessData;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    /**
     * Converts this event to a flat map for publishing to a Redis Stream.
     */
    public Map<String, String> toMap() {
        Map<String, String> map = new LinkedHashMap<>();
        map.put("callId", callId);
        map.put("status", status != null ? status.name() : null);
        if (agentId != null) map.put("agentId", agentId);
        if (agentName != null) map.put("agentName", agentName);
        if (customerId != null) map.put("customerId", customerId);
        if (phoneNumber != null) map.put("phoneNumber", phoneNumber);
        if (businessData != null && !businessData.isEmpty()) {
            // Prefix business data keys with "data." to namespace them in the flat Redis map
            for (Map.Entry<String, String> entry : businessData.entrySet()) {
                map.put("data." + entry.getKey(), entry.getValue());
            }
        }
        map.put("timestamp", timestamp);
        return map;
    }

    @Override
    public String toString() {
        return "CallEvent{callId='" + callId + "', status='" + (status != null ? status.name() : null) +
                "', agentId='" + agentId + "', customerId='" + customerId +
                "', timestamp='" + timestamp + "'}";
    }
}
