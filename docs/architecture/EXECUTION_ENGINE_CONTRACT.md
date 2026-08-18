# Execution Engine Contract

## Purpose

The Execution Engine is the authoritative orchestration boundary
for Execution lifecycle.

It coordinates immutable Execution attempts and Executors.

It does not perform domain work.

## Responsibilities

The Engine is responsible for:

- admitting an Execution
- validating lifecycle eligibility
- selecting an Executor
- transitioning Execution state
- invoking the Executor
- observing the Executor outcome
- producing authoritative lifecycle Events
- classifying failures
- enforcing timeout policy
- handling cancellation
- creating retry Executions
- determining terminal state

## Non-responsibilities

The Engine must not:

- implement domain logic
- mutate Command objects
- mutate Plan objects
- mutate Execution objects
- perform executor-specific work
- depend on a concrete Executor implementation
- persist directly to a specific database
- depend on a specific queue
- depend on a specific transport
- contain UI logic
- contain AI-provider-specific logic

## Input boundary

The Engine operates on:

- immutable Execution
- Executor selection mechanism
- execution policy
- authoritative time
- external observations

## Output boundary

The Engine produces:

- immutable Execution states
- lifecycle Events
- observed Executor outcomes
- retry Executions where policy permits

## Lifecycle authority

Only the Engine may authoritatively advance Execution lifecycle.

The Engine must never silently skip a lifecycle transition
when that transition is semantically observable.

## Executor isolation

Executors are invoked through the Executor Port.

The Engine must depend on the Executor contract,
not on concrete implementations.

## Failure isolation

An Executor failure must become an explicit Engine outcome.

The Engine must never interpret an exception,
missing response,
timeout,
or infrastructure failure as success.

## Historical integrity

The Engine must never rewrite an existing Execution.

The Engine must never rewrite historical Events.

A new lifecycle state is represented as a new immutable state.

## Retry semantics

Retry creates a new Execution.

The original Execution remains terminal and immutable.

A retry must preserve:

- command identity
- correlation identity
- plan identity

A retry must receive a new execution identity
and a new attempt number.

## Idempotency

The Engine must eventually support an idempotency boundary
that survives process restart and distributed delivery.

Repeated invocation of the same Execution must not
silently create duplicate external side effects.

## Recovery

The Engine must tolerate ambiguity.

If an Executor response is lost, the Engine must not assume
that the external operation did not happen.

Recovery policy must distinguish:

- definitely not started
- started
- completed
- failed
- unknown

## Distribution

The Engine contract must remain valid when:

- Executor runs locally
- Executor runs remotely
- communication is asynchronous
- messages are duplicated
- messages arrive out of order
- workers restart
- machines fail

## Determinism

Given equivalent:

- Execution state
- policy
- executor capabilities
- authoritative observations
- time inputs

the Engine should produce equivalent orchestration decisions.

## Security

The Engine must distinguish:

valid
→ authentic
→ authorized
→ executable

Executor identity is not authorization.

## Ultimate invariant

The Engine orchestrates.

The Executor performs.

The Event records.

The Execution remains immutable.

The history remains append-only.
