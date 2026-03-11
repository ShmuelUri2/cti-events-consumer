"""
Event Generator for the Streams-Joiner interview exercise.

Produces call-center events to three Redis Streams.
Runs continuously, producing a new call scenario every 2-5 seconds.
"""

import os
import random
import time
import uuid
from datetime import datetime, timezone

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
EVENT_INTERVAL_MIN = float(os.getenv("EVENT_INTERVAL_MIN", "2.0"))
EVENT_INTERVAL_MAX = float(os.getenv("EVENT_INTERVAL_MAX", "5.0"))

AGENT_STREAM = "agent-events"
CUSTOMER_STREAM = "customer-events"
BUSINESS_STREAM = "business-data-events"

AGENT_NAMES = [
    ("agent-1", "Alice Johnson"),
    ("agent-2", "Bob Smith"),
    ("agent-3", "Carol Davis"),
    ("agent-4", "Dan Wilson"),
    ("agent-5", "Eve Martinez"),
]

CUSTOMER_NAMES = [
    ("cust-101", "+1-555-0101"),
    ("cust-102", "+1-555-0102"),
    ("cust-103", "+1-555-0103"),
    ("cust-104", "+1-555-0104"),
    ("cust-105", "+1-555-0105"),
    ("cust-106", "+1-555-0106"),
]

SKILLS = ["billing-support", "tech-support", "sales", "retention", "general-inquiry"]
PRIORITIES = ["LOW", "NORMAL", "HIGH"]
LANGUAGES = ["en", "es", "fr", "de", "pt"]
QUEUES = ["queue-1", "queue-2", "queue-3", "queue-4"]
SENTIMENTS = ["positive", "neutral", "negative"]
CALL_REASONS = ["billing-inquiry", "technical-issue", "account-update", "cancellation", "new-service"]


def random_business_data():
    """Generate a random subset of business key-value pairs."""
    all_pairs = {
        "skillName": random.choice(SKILLS),
        "priority": random.choice(PRIORITIES),
        "language": random.choice(LANGUAGES),
        "queueId": random.choice(QUEUES),
        "sentiment": random.choice(SENTIMENTS),
        "callReason": random.choice(CALL_REASONS),
    }
    # Pick 1-4 random keys to include in this event
    keys = random.sample(list(all_pairs.keys()), k=random.randint(1, 4))
    return {k: all_pairs[k] for k in keys}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def short_id():
    return str(uuid.uuid4())[:8]


def emit(r, stream, fields):
    """Publish an event to a Redis Stream."""
    r.xadd(stream, fields)
    print(f"  -> {stream}: {fields}")


def sleep_step(min_s=0.3, max_s=1.5):
    """Small delay between events within a scenario."""
    time.sleep(random.uniform(min_s, max_s))


# ---------------------------------------------------------------------------
# Scenario functions
# ---------------------------------------------------------------------------

def scenario_happy_path(r):
    call_id = f"call-{short_id()}"
    agent_id, agent_name = random.choice(AGENT_NAMES)
    cust_id, phone = random.choice(CUSTOMER_NAMES)
    skill = random.choice(SKILLS)
    priority = random.choice(PRIORITIES)

    print(f"\n[SCENARIO] Happy path — {call_id}")

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_JOINED",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, BUSINESS_STREAM, {
        "callId": call_id,
        **random_business_data(),
        "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_JOINED",
        "agentId": agent_id, "agentName": agent_name, "timestamp": now_iso()
    })
    sleep_step(1.0, 3.0)

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_LEFT",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_LEFT",
        "agentId": agent_id, "agentName": agent_name, "timestamp": now_iso()
    })


def scenario_out_of_order(r):
    call_id = f"call-{short_id()}"
    agent_id, agent_name = random.choice(AGENT_NAMES)
    cust_id, phone = random.choice(CUSTOMER_NAMES)

    print(f"\n[SCENARIO] Out-of-order — {call_id}")

    # Agent joins first
    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_JOINED",
        "agentId": agent_id, "agentName": agent_name, "timestamp": now_iso()
    })
    sleep_step()

    # Customer joins after
    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_JOINED",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, BUSINESS_STREAM, {
        "callId": call_id,
        **random_business_data(),
        "timestamp": now_iso()
    })
    sleep_step(1.0, 2.5)

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_LEFT",
        "agentId": agent_id, "agentName": agent_name, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_LEFT",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })


def scenario_agent_transfer(r):
    call_id = f"call-{short_id()}"
    agents = random.sample(AGENT_NAMES, 2)
    agent_a_id, agent_a_name = agents[0]
    agent_b_id, agent_b_name = agents[1]
    cust_id, phone = random.choice(CUSTOMER_NAMES)

    print(f"\n[SCENARIO] Agent transfer — {call_id}")

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_JOINED",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_JOINED",
        "agentId": agent_a_id, "agentName": agent_a_name, "timestamp": now_iso()
    })
    sleep_step(1.0, 2.0)

    # Agent A leaves
    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_LEFT",
        "agentId": agent_a_id, "agentName": agent_a_name, "timestamp": now_iso()
    })
    sleep_step(0.5, 1.0)

    # Agent B joins
    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_JOINED",
        "agentId": agent_b_id, "agentName": agent_b_name, "timestamp": now_iso()
    })
    sleep_step(1.0, 2.5)

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_LEFT",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_LEFT",
        "agentId": agent_b_id, "agentName": agent_b_name, "timestamp": now_iso()
    })


def scenario_two_agents_no_customer(r):
    call_id = f"call-{short_id()}"
    agents = random.sample(AGENT_NAMES, 2)

    print(f"\n[SCENARIO] Two agents, no customer — {call_id}")

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_JOINED",
        "agentId": agents[0][0], "agentName": agents[0][1], "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_JOINED",
        "agentId": agents[1][0], "agentName": agents[1][1], "timestamp": now_iso()
    })
    sleep_step(1.5, 3.0)

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_LEFT",
        "agentId": agents[0][0], "agentName": agents[0][1], "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_LEFT",
        "agentId": agents[1][0], "agentName": agents[1][1], "timestamp": now_iso()
    })


def scenario_customer_hangs_up_early(r):
    call_id = f"call-{short_id()}"
    cust_id, phone = random.choice(CUSTOMER_NAMES)

    print(f"\n[SCENARIO] Customer hangs up early — {call_id}")

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_JOINED",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step(1.5, 3.0)

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_LEFT",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })


def scenario_late_business_data(r):
    call_id = f"call-{short_id()}"
    agent_id, agent_name = random.choice(AGENT_NAMES)
    cust_id, phone = random.choice(CUSTOMER_NAMES)

    print(f"\n[SCENARIO] Late business data — {call_id}")

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_JOINED",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_JOINED",
        "agentId": agent_id, "agentName": agent_name, "timestamp": now_iso()
    })
    sleep_step(1.0, 2.0)

    # Business data arrives late
    emit(r, BUSINESS_STREAM, {
        "callId": call_id,
        **random_business_data(),
        "timestamp": now_iso()
    })
    sleep_step(1.0, 2.5)

    emit(r, CUSTOMER_STREAM, {
        "callId": call_id, "eventType": "CUSTOMER_LEFT",
        "customerId": cust_id, "phoneNumber": phone, "timestamp": now_iso()
    })
    sleep_step()

    emit(r, AGENT_STREAM, {
        "callId": call_id, "eventType": "AGENT_LEFT",
        "agentId": agent_id, "agentName": agent_name, "timestamp": now_iso()
    })


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

SCENARIOS = [
    (scenario_happy_path, 3),            # weight 3 — most common
    (scenario_out_of_order, 2),
    (scenario_agent_transfer, 2),
    (scenario_two_agents_no_customer, 1),
    (scenario_customer_hangs_up_early, 1),
    (scenario_late_business_data, 2),
]

# Build weighted list
WEIGHTED_SCENARIOS = []
for fn, weight in SCENARIOS:
    WEIGHTED_SCENARIOS.extend([fn] * weight)


def main():
    print(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT} ...")
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()
    print("Connected to Redis. Starting event generation...\n")

    call_count = 0
    while True:
        scenario = random.choice(WEIGHTED_SCENARIOS)
        scenario(r)
        call_count += 1
        wait = random.uniform(EVENT_INTERVAL_MIN, EVENT_INTERVAL_MAX)
        print(f"\n--- Call #{call_count} complete. Next call in {wait:.1f}s ---")
        time.sleep(wait)


if __name__ == "__main__":
    main()
