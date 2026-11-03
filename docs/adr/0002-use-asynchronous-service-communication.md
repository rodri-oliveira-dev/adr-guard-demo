# Use Asynchronous Communication Between Services

## Status

Accepted

## Context

Order placement triggers billing, inventory, notification, and analytics work. Performing every step synchronously couples availability and latency across services, while some follow-up work can complete after the customer receives confirmation.

## Decision

Publish versioned domain events through a durable message broker for non-immediate cross-service workflows. Keep operations that require an immediate customer response synchronous, and require consumers to be idempotent because delivery is at least once.

## Consequences

Services can absorb traffic spikes and fail independently for deferred work. The system also becomes eventually consistent and requires correlation identifiers, retry and dead-letter policies, schema evolution discipline, and observability across asynchronous boundaries.
