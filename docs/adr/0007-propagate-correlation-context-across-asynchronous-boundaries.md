# Propagate Correlation Context Across Asynchronous Boundaries

## Status

Accepted

## Context

Order processing publishes events that may be consumed by multiple workers at different times. To make distributed tracing meaningful, consumers must be able to connect message handling with the request or operation that created each event.

## Decision

Carry trace and correlation context in message metadata, without embedding transport details in the business payload. Consumers must extract the available context and start child spans when valid, while treating missing or untrusted metadata safely.

## Consequences

Cross-service traces remain connected when messages pass through the broker. Producers and consumers must agree on metadata propagation, avoid leaking credentials or personal data, and tolerate older messages with no trace context.
