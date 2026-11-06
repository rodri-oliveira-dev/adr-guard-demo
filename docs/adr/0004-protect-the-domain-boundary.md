# Protect the Domain Boundary

## Status

Accepted

## Context

The domain model contains business concepts that must remain usable without database, cache, messaging, or framework concerns. Allowing the domain project to reference infrastructure would reverse the intended dependency direction and make business rules harder to test and evolve independently.

## Decision

Keep the domain project free of project references to infrastructure. Application and infrastructure projects may depend on the domain, but the domain must not depend on either of them. Verify the boundary with an ADR Guard fitness rule over the exact .NET project references.

## Consequences

Business concepts remain isolated from delivery and storage choices, and a deterministic static check can detect a reversed dependency. The team must maintain interfaces at the appropriate boundary and cannot place infrastructure-specific types in the domain merely for convenience.
