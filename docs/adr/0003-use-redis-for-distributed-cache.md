# Use Redis for Distributed Caching

## Status

Accepted

## Context

Product catalog reads greatly outnumber writes, and repeated reads place avoidable load on PostgreSQL. The service runs on multiple instances, so an in-process cache would produce inconsistent entries and uneven hit rates.

## Decision

Use managed Redis as a cache-aside store for read-heavy product data. Assign explicit time-to-live values, include schema versions in cache keys, and treat PostgreSQL as the source of truth whenever Redis is unavailable or an entry is missing.

## Consequences

Typical catalog reads become faster and database load decreases across all service instances. The team must handle stale data, invalidation, serialization compatibility, memory limits, and Redis outages without allowing the cache to become a system of record.
