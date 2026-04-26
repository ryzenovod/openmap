# ADR 0003: Legacy assets policy

## Status
Accepted

## Decision
Legacy assets are reference-only and used strictly for:
- dictionaries
- field semantics
- import logic reference
- geo reference

No legacy frontend migration is part of MVP backend scope.
No real medical data is committed to repository.

## Rationale
Prevents accidental coupling to legacy runtime and preserves clean backend-first rewrite goals.
