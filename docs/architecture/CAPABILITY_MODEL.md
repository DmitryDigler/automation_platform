# Capability Model

## Purpose

A Capability describes an ability available to an execution environment.

Capabilities are used for planning, scheduling, authorization,
and executor selection.

A Capability describes WHAT an environment can provide.

It must not describe HOW the capability is implemented.

## Fundamental distinction

Capability != Executor

Capability != Node

Capability != Resource

Capability != Permission

Capability != Credential

A Node provides capabilities.

An Executor consumes capabilities.

A Policy determines whether a capability may be used.

## Examples

Examples of capabilities include:

- filesystem.read
- filesystem.write
- network.outbound
- browser
- subprocess
- container
- gpu
- cpu
- memory
- python
- shell
- http
- database
- object_storage
- secret.access

The Core must not depend on a fixed universal list.

New capabilities must be introducible without modifying
the semantic meaning of existing Commands.

## Capability identity

Every capability must have a stable logical identifier.

Capability identity must not depend on:

- hostname
- IP address
- process ID
- filesystem path
- operating system
- cloud provider
- container ID

## Capability attributes

A capability may expose attributes such as:

- identifier
- version
- provider
- locality
- constraints
- limits
- trust level
- availability
- expiration

Attributes describe the execution environment.

They must not redefine Command semantics.

## Capability discovery

Execution nodes may advertise capabilities.

Capability discovery may be:

- static
- dynamic
- local
- remote
- periodically refreshed
- policy-filtered

Discovery must not automatically imply authorization.

## Capability availability

A capability may be:

- available
- unavailable
- degraded
- reserved
- expired
- unknown

Availability is an execution-environment property.

## Capability locality

Capabilities may be:

- node-local
- cluster-local
- region-local
- network-local
- globally addressable

Locality must remain explicit.

A capability available on one Node must not silently
be assumed available on another Node.

## Capability versioning

Capabilities may evolve.

A capability contract must therefore support explicit versions.

An executor requiring:

    browser >= 2

must not silently receive an incompatible capability.

## Capability matching

Planning and scheduling may match:

Required Capabilities
        against
Available Capabilities

The matching process must consider:

- capability identity
- version
- constraints
- locality
- policy
- trust
- resource availability

## Security

Capability availability does not imply permission.

The platform must distinguish:

capability exists
    ↓
capability is reachable
    ↓
capability is trusted
    ↓
capability is authorized
    ↓
capability may be used

## Evolution

The Capability Model must support new capabilities without
requiring changes to:

- Command
- Event
- Execution
- Result
- Verification

New physical or virtual abilities become new capabilities.

## Portability

Capabilities are environment-specific.

The semantic Core must remain independent from their implementation.

For example:

Windows and Linux may both provide:

    filesystem.read

while implementing it differently.

The Command semantics remain identical.

## Architectural Test

A capability model is valid if the same Command can be planned
against different environments by matching requirements
against available capabilities.

## Ultimate Principle

Commands express intent.

Plans express requirements.

Nodes provide capabilities.

Executors consume capabilities.

Policies determine whether capabilities may be used.
