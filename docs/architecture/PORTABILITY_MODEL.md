# Portability Model

## Purpose

The platform must remain semantically independent from the operating system,
physical machine, execution location, network topology, and infrastructure
provider.

Portability is a fundamental architectural property.

The machine must be capable of moving between environments without changing
the semantic meaning of Commands, Plans, Executions, Events, Results,
or Verification.

## Core Principle

The platform distinguishes:

Semantic Identity
Execution Environment
Physical Location
Runtime
Infrastructure

These concepts must never be conflated.

The semantic identity of the machine is not its:

- hostname
- IP address
- MAC address
- process ID
- filesystem path
- cloud instance ID
- container ID
- operating system
- geographic location

## Operating System Independence

The Core must not depend on a specific operating system.

Supported environments may include:

- Windows
- Linux
- macOS
- BSD
- future operating systems

OS-specific behavior belongs to adapters.

The Core must interact with operating-system capabilities through
explicit ports and capabilities.

The following must not appear in Core semantics:

- Windows-specific paths
- Linux-specific paths
- shell-specific commands
- process-specific assumptions
- OS-specific environment variables
- platform-specific device identifiers

## Machine Independence

The semantic platform must not depend on a particular physical machine.

A machine may be:

- replaced
- restarted
- upgraded
- downgraded
- moved
- virtualized
- containerized
- removed

without changing the semantic identity of previously created
Commands, Events, Plans, or Executions.

## Runtime Independence

The platform may execute inside:

- a native process
- a virtual environment
- a container
- a virtual machine
- a remote worker
- a cloud runtime
- an edge device
- a future execution substrate

Runtime details belong outside the Core.

## Location Independence

Geographic location is an execution property, not a semantic identity.

The platform may operate from:

- a workstation
- a home server
- a datacenter
- a cloud region
- an edge location
- a remote worker
- multiple geographic regions

Location may influence execution planning.

Location must never redefine the meaning of a Command.

## Control Plane and Execution Plane

The architecture distinguishes:

Control Plane
    ↓
coordination, identity, policy, planning, scheduling, observation

Execution Plane
    ↓
actual work performed by Executors

The Control Plane may coordinate multiple Execution Plane nodes.

Execution Plane nodes may be added or removed dynamically.

The semantic model must remain consistent across both planes.

## Local Execution

The platform must support local execution.

A node may execute work without requiring a remote worker
when the required capabilities are locally available.

Local execution must use the same semantic Execution model
as remote execution.

## Remote Execution

The platform must support remote execution.

A Command or Plan may result in an Execution performed by
a remote Executor.

The semantic model must not change merely because execution
crosses a process or machine boundary.

## Distributed Execution

The platform must eventually support multiple execution nodes.

Nodes may differ in:

- operating system
- architecture
- hardware
- installed software
- capabilities
- permissions
- network connectivity
- geographic location
- resource availability

The Engine must select execution resources based on explicit
capabilities and policies.

## Capability Locality

A capability belongs to an execution environment.

Examples:

filesystem
    local to a node

GPU
    local to a node or resource pool

browser
    local to a worker

credential
    available only within a trust boundary

network access
    dependent on node and policy

Capabilities must therefore expose enough information for
planning and scheduling without leaking infrastructure details
into the Core semantic model.

## Resource Locality

Some resources cannot be treated as globally interchangeable.

Examples:

- local files
- attached devices
- private credentials
- browser sessions
- hardware accelerators
- network-local services

The system must explicitly represent locality requirements.

A Plan must not silently assume that a resource available on
one node is available everywhere.

## Network Independence

The platform must not assume:

- permanent connectivity
- low latency
- ordered delivery
- exactly-once delivery
- immediate responses
- reliable transport

Network communication is an infrastructure concern.

The semantic model must survive:

- latency
- duplication
- reordering
- temporary disconnection
- connection loss
- reconnection

## Offline Operation

A node may continue executing previously authorized work
during temporary loss of connectivity when policy permits.

Offline execution must remain bounded by:

- authorization
- capability availability
- resource availability
- execution policy
- expiration
- security constraints

Offline operation must not create ambiguous ownership of
the same Execution.

## Reconnection

After connectivity is restored, a node must be able to report
previously observed facts.

Reconnection must not require rewriting history.

Previously recorded Events remain immutable.

New information produces new Events.

## Ambiguous Execution

Loss of communication must not automatically imply execution failure.

The platform must distinguish:

- not started
- started
- completed
- failed
- cancelled
- interrupted
- unknown

An unknown state must remain explicitly unknown until sufficient
evidence exists to classify it.

## Node Identity

Execution nodes require stable logical identity.

Node identity must not be based solely on:

- IP address
- hostname
- process ID
- container ID
- temporary cloud instance ID

Physical replacement and runtime restart must be representable
without corrupting historical identity.

## Executor Mobility

An Executor implementation may move between nodes.

The semantic identity of an Executor must remain distinct from
its current process instance.

A logical Executor may have multiple runtime instances.

## Serialization Boundary

Objects crossing machine boundaries must have stable,
canonical representations.

Serialization must not depend on:

- Python object identity
- memory addresses
- local filesystem layout
- process state
- implementation-specific internals

A future implementation in another language must be capable
of interpreting supported serialized contracts.

## Time

Distributed execution must not assume that local clocks are
perfectly synchronized.

The platform must distinguish:

- event occurrence time
- local observation time
- processing time
- deadline
- timeout policy

Causal ordering must not depend exclusively on wall-clock timestamps.

## Upgrade Compatibility

A node running a newer platform version must be able to
interoperate with supported older nodes.

Contracts must be explicitly versioned.

Unsupported versions must fail explicitly.

Silent semantic reinterpretation is forbidden.

## Infrastructure Independence

The platform must not semantically depend on:

- a specific cloud provider
- a specific database
- a specific message broker
- a specific container runtime
- a specific orchestration platform

Infrastructure integrations belong in adapters.

## Migration

The platform must support migration between execution environments.

Migration may involve:

- moving work between machines
- replacing workers
- changing operating systems
- changing infrastructure providers
- changing runtime implementations

Migration must preserve semantic history.

## Evolution

Portability is not only the ability to move existing software.

The platform must be able to acquire new execution environments
without changing the Core semantic model.

New environments become new adapters and capabilities.

## Security

Portability must never bypass security boundaries.

A capability available on one node must not automatically
become available on another node.

Credentials, permissions, trust levels, and policies remain
explicit.

## Architectural Test

The architecture is portable only if the same Command contract
can survive execution across:

Windows
Linux
macOS
container
virtual machine
remote worker
cloud infrastructure

without changing its semantic meaning.

## Long-Term Objective

The machine should be capable of moving through changing
execution environments while preserving:

- identity
- causality
- history
- contracts
- authorization semantics
- execution semantics

The environment may change.

The infrastructure may change.

The Executor may change.

The machine's semantic core must remain stable.

## Ultimate Principle

Environment is replaceable.

Capabilities are discoverable.

Execution is movable.

History is immutable.

Semantics are portable.
