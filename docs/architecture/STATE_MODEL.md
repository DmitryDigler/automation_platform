# State Model

## Principle

State is explicit.

State must not be represented by arbitrary mutable flags
distributed throughout the implementation.

Every meaningful state transition must be observable.

## State dimensions

The platform must avoid collapsing all state into a single status field.

At minimum, the architecture distinguishes:

- Intent state
- Plan state
- Execution state
- Authorization state
- Verification state

Additional dimensions may be introduced without changing
the fundamental model.

## Intent state

An intent may be:

- issued
- accepted
- rejected
- cancelled
- expired
- superseded

## Plan state

A Plan may be:

- proposed
- accepted
- rejected
- superseded
- invalidated

A rejected or invalidated Plan does not necessarily invalidate
the original Command.

## Execution state

An Execution may be:

- created
- queued
- running
- paused
- interrupted
- completed
- failed
- timed_out
- cancelled

## Authorization state

Authorization is independent from execution.

An operation may be:

- unauthorized
- authorized
- authorization_expired
- authorization_revoked

Authorization state must never be inferred solely from
execution state.

## Verification state

Verification is independent from execution.

A Result may be:

- unverified
- verifying
- verified
- rejected
- inconclusive

Successful execution does not imply successful verification.

## State transitions

A state transition must:

1. have a defined source state;
2. have a defined target state;
3. have an explicit cause;
4. be observable as an Event;
5. preserve causal relationships;
6. be rejected if the transition is invalid.

## No arbitrary transitions

The implementation must not allow:

any_state → any_state

Valid transitions must be defined explicitly.

## Recovery

Failure is a state, not necessarily a terminal condition.

A failed Execution may lead to:

- retry
- recovery
- replanning
- fallback execution
- human intervention
- terminal failure

## Replanning

If an Execution demonstrates that a Plan is invalid,
the original Command may remain active.

A new Plan may be created.

Therefore:

Command
    ├── Plan A
    │     └── invalidated
    │
    └── Plan B
          └── active

## Distributed execution

State must remain meaningful when execution occurs across:

- multiple processes
- multiple machines
- delayed messages
- duplicated messages
- reordered messages
- unavailable workers

## Persistence

Important state must be recoverable from durable information.

The architecture must not depend exclusively on
in-memory state.

## Event relationship

Events represent transitions and facts.

Current state is a derived or explicitly persisted view
of those facts.

The architecture must permit rebuilding state from history
where required.

## Long-term objective

The state model must remain valid when the platform evolves
from a local single-process runtime into a distributed system.

The addition of new execution mechanisms must not require
rewriting the fundamental state model.
