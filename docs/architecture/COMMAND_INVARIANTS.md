# Command Invariants

## 1. Identity

Every Command must have exactly one immutable command_id.

A command_id must never be reused.

## 2. Intent purity

A Command represents intent.

A Command must not directly execute external side effects.

## 3. Immutability

Once issued, a Command is immutable.

Changes in execution state must be represented by Events,
not by mutating the original Command.

## 4. Causality

Every Command must belong to a causal chain.

correlation_id identifies the overall operation.

causation_id identifies the event or command that caused
the current Command.

The root Command may have no causation_id.

## 5. Version integrity

command_type and command_version together identify
the semantic contract of the Command.

Changing the meaning of an existing version is forbidden.

## 6. Serialization stability

A Command must be serializable into a canonical representation.

Equivalent Commands must produce equivalent serialized data.

The serialized representation must not depend on:

- memory addresses
- process-local state
- object identity
- execution environment
- Python-specific implementation details

## 7. Explicit issuer

Every Command must have an explicit issuer.

The issuer may represent:

- human
- system
- plugin
- worker
- agent
- external service

The Core must not assume that the issuer is a human.

## 8. Idempotency

The platform must be able to determine whether
the same Command has already been accepted or executed.

Command identity must therefore be usable as an idempotency boundary.

Repeated delivery must not automatically imply repeated execution.

## 9. Lifecycle separation

Command data and Command lifecycle are separate concepts.

The Command does not mutate when its lifecycle changes.

Lifecycle transitions are represented by Events.

## 10. Validation boundary

A Command must be structurally valid before entering the execution system.

Semantic validation may additionally depend on:

- capabilities
- resources
- policies
- current state

Therefore validation must not be completely embedded
inside the immutable Command object.

## 11. No hidden dependencies

A Command must not depend on:

- global variables
- local process state
- active database connections
- network connections
- mutable singleton objects
- current UI state

A Command must remain meaningful outside the process that created it.

## 12. Security boundary

A valid Command is not automatically an authorized Command.

The platform must distinguish:

valid
→ authentic
→ authorized
→ executable

These are separate decisions.

## 13. Replayability

A stored Command must be replayable or explicitly rejected
as non-replayable according to its contract.

Replay semantics must be defined before introducing
distributed execution.

## 14. Compatibility

A newer runtime must be able to identify the version
of a Command before attempting to interpret it.

Unsupported versions must fail explicitly.

Silent reinterpretation is forbidden.

## 15. Core independence

The Command model must not depend on:

- Telegram
- HTTP
- databases
- message brokers
- AI providers
- cloud providers
- operating systems
- specific worker implementations

These belong outside the Core.

## 16. Failure transparency

A Command must never be considered successfully completed
merely because an execution attempt returned without an error.

Completion requires an explicit Result and,
where necessary, independent verification.

## 17. Future distribution

Nothing in the Command model may assume:

- single process
- single machine
- shared memory
- synchronous execution
- reliable network
- immediate response

## 18. Architectural test

A Command implementation is acceptable only if the same
Command contract can survive replacement of:

- execution engine
- storage engine
- transport
- AI provider
- interface
- worker architecture

without changing the meaning of the Command.

## Ultimate invariant

The Command describes WHAT is intended.

It must never encode HOW the platform happens to perform it.
