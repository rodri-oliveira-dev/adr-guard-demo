# Correlate Requests with Application Logs

## Status

Superseded

## Context

The demo's order and messaging services need a way to investigate a request across service boundaries. A first approach was to use structured application logs with a shared request identifier, but operators still have to assemble the timeline manually.

## Decision

Use structured application logs tagged with a request identifier to correlate operations across services. This documents the earlier approach for historical context; it is not the currently recommended tracing mechanism.

## Consequences

This approach requires little additional instrumentation but offers no explicit span hierarchy or reliable view of latency across synchronous and asynchronous boundaries. The decision remains available for historical reference.

## Superseded by

[ADR 0006: Use distributed tracing for cross-service requests](0006-use-distributed-tracing-for-cross-service-requests.md)
