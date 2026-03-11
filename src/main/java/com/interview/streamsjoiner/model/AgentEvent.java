package com.interview.streamsjoiner.model;

/**
 * Represents an event from the "agent-events" stream.
 * Agents join or leave calls.
 */
public class AgentEvent {

    private String callId;
    private AgentEventType eventType;
    private String agentId;
    private String agentName;
    private String timestamp;

    public AgentEvent() {
    }

    public AgentEvent(String callId, AgentEventType eventType, String agentId, String agentName, String timestamp) {
        this.callId = callId;
        this.eventType = eventType;
        this.agentId = agentId;
        this.agentName = agentName;
        this.timestamp = timestamp;
    }

    public String getCallId() {
        return callId;
    }

    public void setCallId(String callId) {
        this.callId = callId;
    }

    public AgentEventType getEventType() {
        return eventType;
    }

    public void setEventType(AgentEventType eventType) {
        this.eventType = eventType;
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

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "AgentEvent{callId='" + callId + "', eventType='" + eventType +
                "', agentId='" + agentId + "', agentName='" + agentName +
                "', timestamp='" + timestamp + "'}";
    }
}
