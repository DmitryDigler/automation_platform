# Execution Engine Model

## Purpose

The Execution Engine is the orchestration authority responsible
for coordinating the lifecycle of Execution attempts.

It does not perform domain work itself.

It selects and invokes Executors.

## Fundamental responsibility

The Engine transforms an immutable Execution attempt
into an observable lifecycle.

The Engine owns:

- admission
- lifecycle transitions
- executor selection
- execution start
- outcome observation
- failure classification
- timeout policy
- cancellation policy
- retry creation
- lifecycle Events
- terminal state determination

## Fundamental distinction

Execution Engine != Executor

The Engine answers:

"How is an Execution attempt orchestrated?"

The Executor answers:

"How is the requested work physically performed?"

## Execution ownership

The Engine is the authoritative owner of Execution lifecycle semantics.

An Executor must never directly mutate Execution state.

The Engine must treat Execution as immutable.

Every lifecycle change produces a new Execution representation
or an equivalent immutable state transition.

## Executor selection

Executor selection must be explicit.

The Engine must not depend on:

- concrete Executor classes
- process-local globals
- hard-coded worker implementations
- operating-system-specific behavior

Selection may eventually depend on:

- capabilities
- policies
- resource requirements
- trust level
- locality
- cost
- availability
- compatibility

## Lifecycle

The Engine must preserve the following semantic distinction:

created
ready
running
succeeded
failed
cancelled
interrupted

Terminal states must never silently become non-terminal states.

## Events

Every meaningful lifecycle transition must be observable.

The Engine is responsible for producing authoritative lifecycle Events.

Executor observations must remain distinguishable from
Engine-owned lifecycle Events.

## Failure

Failure must be classified explicitly.

The Engine must distinguish at least:

- execution failure
- timeout
- cancellation
- interruption
- infrastructure failure
- executor unavailable
- invalid execution
- policy rejection

Failure classification must not silently change the historical meaning
of an Execution.

## Retry

Retry never rewinds an Execution.

A retry creates a new Execution attempt.

Therefore:

Execution #1
    ↓
failed

Execution #2
    ↓
new attempt

The original Execution remains immutable and historically valid.

## Cancellation

Cancellation is a request to stop an Execution.

The Engine must distinguish:

cancellation requested
    ↓
cancellation acknowledged
    ↓
execution stopped

A cancellation request is not proof that execution has stopped.

## Timeout

Timeout is an Engine-level semantic.

A local Executor timeout may exist as an implementation mechanism,
but the Engine must retain authoritative timeout semantics.

## Idempotency

The Engine must prevent accidental duplicate execution.

Repeated delivery of the same Execution must not automatically
produce repeated side effects.

Idempotency boundaries must eventually survive:

- process restart
- worker restart
- network retry
- message redelivery
- distributed execution

## Recovery

The Engine must be designed for recovery after:

- process crash
- machine restart
- executor failure
- network interruption
- partial execution
- lost response

The absence of a response must never automatically mean
that the external operation did not happen.

## Distribution

The Engine must not assume:

- one process
- one machine
- shared memory
- synchronous execution
- reliable network
- immediate executor response

The same semantic model must survive distributed execution.

## Determinism

The orchestration rules of the Engine should be deterministic
where the available inputs are deterministic.

External observations must remain explicit.

Probabilistic planning or AI reasoning must not silently alter
historical Execution state.

## Historical integrity

The Engine must never rewrite history.

Past Events remain immutable.

Past Executions remain immutable.

A new decision produces a new state transition,
new Event, or new Execution attempt.

## Long-term objective

The Execution Engine must survive replacement of:

- Executors
- storage
- queues
- transport
- operating system
- worker architecture
- cloud infrastructure
- AI providers

without changing the semantic meaning of the Command.

## Ultimate invariant

The Execution Engine owns orchestration.

The Executor performs work.

Events record what actually happened.

The Engine must never confuse these responsibilities.
