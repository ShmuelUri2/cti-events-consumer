package com.interview.streamsjoiner.model;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Represents an event from the "business-data-events" stream.
 * <p>
 * Contains arbitrary key-value business context data related to a call.
 * Any field in the Redis Stream message other than {@code callId} and {@code timestamp}
 * is treated as a business data key-value pair.
 * <p>
 * Examples of keys: {@code skillName}, {@code priority}, {@code queueId}, {@code language}, etc.
 */
public class BusinessDataEvent {

    private String callId;
    private String timestamp;
    private Map<String, String> data;

    public BusinessDataEvent() {
        this.data = new LinkedHashMap<>();
    }

    public BusinessDataEvent(String callId, String timestamp, Map<String, String> data) {
        this.callId = callId;
        this.timestamp = timestamp;
        this.data = data != null ? new LinkedHashMap<>(data) : new LinkedHashMap<>();
    }

    public String getCallId() {
        return callId;
    }

    public void setCallId(String callId) {
        this.callId = callId;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    /**
     * Returns the business data key-value pairs.
     * Keys are arbitrary business field names (e.g., "skillName", "priority", "queueId").
     */
    public Map<String, String> getData() {
        return data;
    }

    public void setData(Map<String, String> data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "BusinessDataEvent{callId='" + callId +
                "', data=" + data +
                ", timestamp='" + timestamp + "'}";
    }
}
