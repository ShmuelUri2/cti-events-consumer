package com.interview.streamsjoiner.service;


import org.springframework.stereotype.Service;

/**
 * ===================================================================
 *  YOUR TASK: Implement the stream joining logic.
 * ===================================================================
 *
 * This service should:
 * 1. Consume events from three Redis Streams: agent-events, customer-events,
 *    and business-data-events.
 * 2. Correlate events by callId and track call state.
 * 3. Publish joined lifecycle events to the "joined-call-events" output stream.
 *
 * You are responsible for:
 * - Configuring Redis Stream consumption (listener container, threading, polling)
 * - Parsing raw stream records into the provided model objects
 * - Implementing the state tracking and join logic
 * - Publishing output events to the output stream
 *
 * You may restructure this class, create new classes, or organize the code
 * however you see fit. The model POJOs and application.yml are provided.
 */
@Service
public class CallJoinerService {

    // TODO: Implement stream consumption, join logic, and output publishing
}
