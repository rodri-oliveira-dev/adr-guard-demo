# Use a Provisional Cache Strategy

## Status

Approved

## Context

This isolated scenario deliberately uses an invalid canonical ADR status.

## Decision

Document a provisional cache strategy solely for testing diagnostics.

## Consequences

The invalid status should generate a validation error, without being silently converted to Accepted.
