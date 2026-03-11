# Discussion Points — Post-Exercise Debrief

Use these questions to guide the conversation after the candidate completes (or presents) their implementation.

## Idempotency
- What if the same event is delivered twice?
- How would you detect and handle duplicate events?

## Memory Management
- What happens to calls that never complete?
- How would you handle memory growth from accumulated call state?
- Would you introduce TTLs, eviction policies, or external state stores?

## Horizontal Scaling
- How would you scale this service to multiple instances?
- How would you partition work so two instances don't process the same call?
- What role do Redis consumer groups play here?

## Fault Tolerance
- What if the service restarts mid-call?
- How would you recover in-flight call state?
- What trade-offs exist between in-memory state and persisted state?

## Exactly-Once Semantics
- How would you ensure each output event is published exactly once?
- What guarantees does Redis Streams provide out of the box?
