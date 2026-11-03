# Use PostgreSQL for Transactional Data

## Status

Accepted

## Context

The order service stores customers, orders, payments, and inventory reservations. These records have relationships that must remain consistent across concurrent writes, and operators need reliable backups and familiar query tooling. The expected workload is moderate, but lost or partially committed transactions would directly affect customers.

## Decision

Use managed PostgreSQL as the system of record for transactional data. Apply schema changes through reviewed migrations, use database constraints for core invariants, and keep service ownership of the schema explicit.

## Consequences

The team gains ACID transactions, mature operational tooling, and expressive queries. It must operate connection pooling, monitor slow queries, plan schema migrations carefully, and accept that horizontal write scaling may require additional design as demand grows.
