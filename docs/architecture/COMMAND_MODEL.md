# Command Model

## Purpose

A Command represents an explicit intent to cause a state transition
or initiate an operation within the platform.

A Command is not an implementation instruction.

## Architectural distinction

Command != Action

A Command expresses intent.

Execution determines how that intent is fulfilled.

## Properties

Every Command must have:

- command_id
- command_type
- command_version
- issued_at
- issuer
- correlation_id
- causation_id
- payload
- metadata

## Identity

Every Command has a globally unique command_id.

## Versioning

Command contracts are versioned.

Older command versions must remain interpretable
where backward compatibility is required.

## Correlation

Commands participate in execution chains through:

- correlation_id
- causation_id

This allows the platform to reconstruct causal relationships.

## Determinism

The Command itself must be deterministic data.

Decision-making and probabilistic reasoning must occur outside
the Command model.

## Serialization

Commands must be serializable across:

- process boundaries
- machines
- queues
- persistent storage
- future distributed execution systems

## Extensibility

The Command model must not contain domain-specific logic.

Examples such as:

- freelance
- trading
- scraping
- document processing
- browser automation

must be represented as capabilities or command types,
not embedded into the Core.

## Security

Commands must eventually support:

- authorization
- provenance
- policy evaluation
- trust boundaries
- auditability

## Lifecycle

A command may progress through:

issued
accepted
planned
executing
completed
failed
cancelled
expired

The lifecycle itself must be observable through Events.

## Long-term objective

A Command must remain meaningful even when:

- the execution engine changes
- the AI provider changes
- the storage backend changes
- the worker architecture changes
- the interface changes
- execution becomes distributed

The command represents intent,
not implementation.
