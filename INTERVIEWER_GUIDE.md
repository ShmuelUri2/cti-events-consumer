# Interviewer Guide — AI-Assisted Coding Session

This guide helps interviewers evaluate candidates who use AI coding agents (e.g., GitHub Copilot Chat, Cursor, ChatGPT) during the Stream Joiner exercise.

---

## Goals of This Evaluation

We are **not** testing whether the candidate can write code from memory. We are evaluating:

1. **Engineering effectiveness** — Can the candidate deliver a working solution using all tools at their disposal?
2. **AI collaboration skill** — Does the candidate use AI as a force multiplier or as a crutch?
3. **Technical judgment** — Can the candidate validate, critique, and steer AI-generated output?
4. **Ownership & understanding** — Does the candidate understand what was built, regardless of who (or what) wrote it?

---

## What to Observe During the Session

### 1. Problem Decomposition (Before Touching Code)

| Green Flags | Red Flags |
|---|---|
| Reads the README and explores the project structure before prompting | Immediately pastes the entire README into the AI and says "solve this" |
| Breaks the problem into sub-tasks (consume, correlate, state machine, publish) | Issues a single monolithic prompt and accepts whatever comes back |
| Sketches a mental model or asks clarifying questions about edge cases | Shows no curiosity about the problem domain |
| Uses RedisInsight or `redis-cli` to inspect actual event data | Never looks at real data flowing through the streams |

### 2. Prompt Quality & Iteration

| Green Flags | Red Flags |
|---|---|
| Writes specific, scoped prompts ("implement a Redis Stream listener for the agent-events stream using Spring Data Redis") | Writes vague prompts ("make it work", "fix this") |
| Provides context in prompts (stream names, field names, expected behavior) | Relies on the AI to guess project structure and requirements |
| Iterates on AI output — refines prompts when results are off | Accepts first output without review, even when it contains issues |
| Uses the AI for targeted subtasks (parsing, config, boilerplate) while handling orchestration themselves | Delegates all decision-making to the AI |

### 3. Code Review & Validation

| Green Flags | Red Flags |
|---|---|
| Reads and understands AI-generated code before moving on | Pastes code blindly and only checks if it compiles |
| Catches incorrect logic, missing edge cases, or wrong API usage in AI output | Cannot explain what a block of generated code does when asked |
| Modifies or restructures AI output to match their design intent | Keeps code exactly as generated, even when it's awkward or suboptimal |
| Tests incrementally — runs the app, checks output, fixes issues | Only runs the app once at the very end |
| Uses logs, RedisInsight, or `redis-cli` to verify correctness | Has no verification strategy beyond "no errors in console" |

### 4. Technical Decision-Making

| Green Flags | Red Flags |
|---|---|
| Makes deliberate choices about state management (ConcurrentHashMap vs. external store, etc.) | Cannot explain why a particular data structure was chosen |
| Understands threading implications of stream consumers | Ignores concurrency even when the AI generates thread-unsafe code |
| Considers what happens with out-of-order events, duplicates, or missing events | Only considers the happy path |
| Designs a clear state model (e.g., explicit states, participant tracking) | State logic is ad-hoc and hard to follow |

### 5. Debugging & Problem-Solving

| Green Flags | Red Flags |
|---|---|
| Reads error messages and stack traces before prompting the AI | Copies entire stack traces into the AI without reading them |
| Narrows down the problem area before asking for help | Says "it doesn't work" without any diagnosis attempt |
| Uses breakpoints, logs, or print statements strategically | Has no debugging strategy |
| Knows when the AI is wrong and overrides its suggestions | Follows AI suggestions in circles without recognizing the loop |

---

## During-Session Interview Techniques

### Lightweight Check-ins (Non-Disruptive)

Ask these periodically without breaking flow:

- **"What's your plan for the next step?"** — Reveals whether they have a mental roadmap or are prompting aimlessly.
- **"Can you walk me through what that code does?"** — Tests comprehension of AI-generated code. Do this at least 2-3 times during the session.
- **"Why did you choose this approach?"** — Distinguishes between intentional design and "the AI suggested it."
- **"What would happen if two events for the same call arrive simultaneously?"** — Tests awareness of concurrency concerns.

### Targeted Probes (When You Spot Something)

- If they accept dubious AI output: **"Are you confident in how that handles the DISCONNECTED → ENDED transition?"**
- If they're stuck in a loop: **"Let's step back — what do you think the root cause is?"**
- If everything is AI-generated: **"If you couldn't use the AI for the next 5 minutes, what would you do first?"**

---

## Post-Session Evaluation Rubric

### Scoring Scale

| Score | Level | Description |
|---|---|---|
| **1** | Ineffective | Could not produce a working solution; showed no understanding of the generated code |
| **2** | Below Expectations | Partial solution with significant issues; heavily dependent on AI with little critical thinking |
| **3** | Meets Expectations | Working solution for core scenarios; demonstrated understanding of the code and made some independent decisions |
| **4** | Exceeds Expectations | Robust solution; effectively used AI as a tool while maintaining clear ownership and judgment |
| **5** | Exceptional | Elegant, well-structured solution; AI amplified their effectiveness beyond what either could do alone |

### Evaluation Dimensions

Rate each dimension 1–5:

#### A. Solution Completeness & Correctness

- [ ] Consumes all three input streams
- [ ] Correctly correlates events by `callId`
- [ ] Emits STARTED on first participant join
- [ ] Emits CONNECTED when agent + customer are both present
- [ ] Emits DISCONNECTED when one side leaves a connected call
- [ ] Emits ENDED when all participants leave
- [ ] Accumulates and includes business data in output events
- [ ] Handles agent transfers
- [ ] Handles out-of-order arrivals

**Score: __ / 5**

#### B. AI Collaboration Quality

| Aspect | Questions to Consider |
|---|---|
| Prompt engineering | Were prompts specific, scoped, and context-rich? |
| Critical evaluation | Did the candidate review and modify AI output? |
| Iteration | Did they refine prompts based on results? |
| Independence | Could they work without AI when needed (e.g., debugging, design)? |
| Tool selection | Did they use the right tool for each subtask? |

**Score: __ / 5**

#### C. Technical Understanding

| Aspect | Questions to Consider |
|---|---|
| Code comprehension | Can they explain any block of the generated code? |
| Design rationale | Can they justify architectural choices? |
| Edge case awareness | Do they anticipate failure modes and race conditions? |
| Redis Streams knowledge | Do they understand consumer groups, acknowledgment, and offsets? |
| Spring ecosystem | Are they comfortable with Spring Data Redis, bean lifecycle, configuration? |

**Score: __ / 5**

#### D. Engineering Process

| Aspect | Questions to Consider |
|---|---|
| Problem decomposition | Did they break the problem into manageable steps? |
| Incremental progress | Did they build and test incrementally? |
| Verification | Did they verify output correctness (RedisInsight, CLI, logs)? |
| Code organization | Is the final code well-structured and readable? |
| Time management | Did they allocate time wisely across subtasks? |

**Score: __ / 5**

---

## Scorecard Template

```
Candidate: ___________________    Date: ___________
Interviewer: _________________    Duration: _______

A. Solution Completeness:   __ / 5
B. AI Collaboration:        __ / 5
C. Technical Understanding: __ / 5
D. Engineering Process:     __ / 5

TOTAL:                      __ / 20

AI Tool Used: ___________________

Hire Recommendation:  [ ] Strong No  [ ] No  [ ] Lean No  [ ] Lean Yes  [ ] Yes  [ ] Strong Yes

Notes:
_______________________________________________
_______________________________________________
_______________________________________________
```

---

## Common Patterns & What They Mean

### The Orchestrator (Strong Hire Signal)
The candidate treats the AI as a junior developer — gives it clear specs, reviews its output, rejects bad suggestions, and maintains a coherent architecture. They understand every line of the finished code.

### The Collaborator (Positive Signal)
The candidate has a productive back-and-forth with the AI. They don't always get it right on the first prompt, but they iterate effectively and learn from the AI's suggestions while applying their own judgment.

### The Passenger (Concern)
The candidate defers almost entirely to the AI. They accept generated code without review, can't explain what it does, and struggle when the AI produces incorrect output. The AI is driving; they're along for the ride.

### The Resister (Neutral — Evaluate Independently)
The candidate barely uses the AI, preferring to write code manually. This isn't inherently bad — evaluate their raw coding ability separately. However, in a modern engineering environment, effective AI usage is a valuable skill.

---

## Combining with Discussion Points

After the coding session, use [DISCUSSION.md](DISCUSSION.md) for the design debrief. Pay special attention to whether the candidate can discuss trade-offs for concepts they implemented with AI help (e.g., if the AI chose `ConcurrentHashMap`, can they explain why and what alternatives exist?).
