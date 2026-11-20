# Use Distributed Tracing for Cross-Service Requests

## Status

Accepted

## Context

Application logs alone make it difficult to reconstruct the execution path and latency of an order request across APIs and asynchronous consumers. The earlier logging-only approach is preserved in ADR 0005, but the demonstration needs a more precise tracing decision.

## Decision

Instrument cross-service operations using distributed traces and propagate trace context through HTTP calls and asynchronous messages. Keep structured logs as complementary evidence, and follow the correlation-context propagation rules in ADR 0007.

## Consequences

Operators can navigate related spans and identify slow or failing components without manually joining logs. The team must manage instrumentation, sampling, telemetry costs, and safe handling of sensitive information. Missing trace context at asynchronous boundaries can still fragment a trace.

## Supersedes

[ADR 0005: Correlate requests with application logs](0005-correlate-requests-with-application-logs.md)

## Depends on

[ADR 0007: Propagate correlation context across asynchronous boundaries](0007-propagate-correlation-context-across-asynchronous-boundaries.md)
