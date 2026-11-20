# Use an External Delivery Queue

## Status

Accepted

## Context

Notification processing should not block order completion; queue ownership is a separate architectural concern.

## Decision

Use a delivery queue for notification work, but reference the missing ownership decision so the governance check can report it.

## Consequences

The unresolved dependency is deliberately invalid; this is a test case, not an accepted project decision.

## Depends on

[ADR 0099: Queue ownership](0099-queue-ownership.md)
