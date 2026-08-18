# Executor Contract

## Purpose

An Executor is a mechanism capable of attempting an Execution.

An Executor performs work.

An Executor does not own the Execution lifecycle.

The Execution Engine owns lifecycle orchestration.

## Fundamental distinction

Execution Engine = orchestration

Executor = execution mechanism

The Engine decides:

- whether an Execution may start
- when it starts
- which Executor is selected
- how cancellation is handled
- how timeout is handled
- how retries are represented
- how lifecycle Events are produced
- how failures are classified
- when an Execution is terminal

The Executor decides:

- how the requested work is physically performed
- how the external system is contacted
- how local or remote mechanisms are used
- which observations are returned

## Executor independence

The Core must not depend on a concrete Executor implementation.

Executors may eventually represent:

- local processes
- subprocesses
- HTTP clients
- browser automation
- containers
- remote workers
- virtual machines
- cloud jobs
- AI agents
- human operators
- external services

The Core must not contain implementation-specific logic for these mechanisms.

## Executor identity

Every Executor has a stable logical name.

The name identifies the execution mechanism,
not a particular process instance.

Executor identity must not depend on:

- memory addresses
- process IDs
- machine-local paths
- network addresses
- temporary identifiers

## Execution lifecycle ownership

An Executor must not independently mutate an Execution lifecycle.

An Executor must not decide that an Execution is:

- ready
- running
- succeeded
- failed
- cancelled
- interrupted

These are Execution Engine decisions.

The Executor reports observations and execution outcomes.

## Immutability

The supplied Execution is immutable.

An Executor must never mutate it.

The Executor may create external side effects
when the execution contract permits them.

## Events

An Executor may produce or report observable facts.

Events representing the platform lifecycle remain under
Execution Engine control.

An Executor must not fabricate historical facts.

An Event must represent something that actually happened.

## Results

An Executor may produce an observed execution outcome.

A Result is not automatically proof that the Command objective
was achieved.

Verification remains a separate concern.

Therefore:

Executor outcome != verified objective

## Failure

Executor failure must be observable.

Failures must not be silently converted into success.

The Engine is responsible for translating execution failures
into the appropriate Execution lifecycle and Events.

## Cancellation

Cancellation is controlled by the Execution Engine.

An Executor may support cooperative cancellation.

An Executor must not assume that cancellation is always immediate.

External systems may continue running after cancellation is requested.

The Engine must therefore distinguish:

- cancellation requested
- cancellation acknowledged
- execution actually stopped

## Timeout

Timeout policy belongs to the Execution Engine or
an explicit policy component.

An Executor may enforce a local timeout as an implementation mechanism,
but timeout semantics must remain visible to the Engine.

## Retry

An Executor must never silently retry an Execution in a way
that changes the meaning of the Execution history.

A retry is a new Execution attempt.

Therefore:

Execution #1 != Execution #2

The original Execution remains immutable.

## Idempotency

The Executor must not assume that repeated delivery means
repeated intent.

Idempotency policy belongs to the Engine and/or execution boundary.

Where external side effects are involved,
the system must eventually support explicit idempotency semantics.

## Distribution

The Executor may execute locally or remotely.

The Core must not assume:

- shared memory
- local filesystem
- local process
- synchronous execution
- reliable network
- immediate response

## Security boundary

An Executor is not automatically trusted.

The Engine may eventually enforce:

- authentication
- authorization
- capability restrictions
- resource limits
- trust levels
- sandboxing
- provenance
- policy evaluation

Executor identity must never itself be treated as authorization.

## Capability model

Executor selection should eventually depend on capabilities.

Examples:

- filesystem access
- browser access
- network access
- GPU
- operating system
- container runtime
- credentials
- external service access

Capabilities describe what an Executor can do.

Capabilities must not redefine the semantic meaning of a Command.

## Long-term invariant

The platform must be able to replace an Executor implementation
without changing the semantic meaning of:

- Command
- Plan
- Execution
- Event
- Result

The execution mechanism may change.

The intent must not.

## Ultimate rule

The Execution Engine owns orchestration.

The Executor performs execution.

Neither may be confused with the other.
