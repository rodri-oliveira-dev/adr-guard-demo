# ADR Guard Demo

[Português (Brasil)](README.pt-BR.md) · [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) · [GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

[![ADR validation](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml)
[![Architecture drift](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-drift.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-drift.yml)
[![Relationships export](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-align-export.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-align-export.yml)

A hands-on repository for **Architecture Decision Records (ADRs)** using the [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) CLI and GitHub Action. Explore how decisions are validated, indexed, linked to source code, checked for architectural drift, and exported for the Align CLI.

**Start here:** run a validation and export in a few commands, then follow a real ADR replacement from its Markdown declarations to a machine-readable JSON file. No AI provider or API key is needed for the deterministic examples.

## Quick start

**Prerequisites:** Git and the **.NET 10 SDK**. The pinned tool manifest installs ADR Guard CLI **v1.12.0**. Run from the repository root:

```bash
git clone https://github.com/rodri-oliveira-dev/adr-guard-demo.git
cd adr-guard-demo
dotnet tool restore
dotnet tool run adr-guard check docs/adr
dotnet tool run adr-guard export relationships docs/adr
```

The main example has **7 valid ADRs and 3 declared relationships** (two reciprocal supersession declarations and one dependency). The generated file, `.adr-guard/relationships.json`, contains `adrs`, `relationships` and `issues` (expected: empty). It is ignored by Git. A successful export means the JSON was written; `check` is the separate validation step.

No .NET environment? Start with the [GitHub Actions workflows](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions) and their logs.

## Explore the capabilities

| Capability | Example to inspect | How to run or verify |
| --- | --- | --- |
| **Validate** (`check`) | [Seven ADRs](docs/adr/README.md), including required sections, status and relationships | [Validation workflow](.github/workflows/adr-validation.yml) |
| **Index** (`index`) | [ADR catalog](docs/adr/README.md) | [Run the index workflow manually](.github/workflows/adr-index.yml) |
| **Impact** (`impact`) | [ADR-to-code mappings](.adrguard-impact.json) and [source files](src/AdrGuardDemo.Infrastructure/Persistence/PostgresOrderRepository.cs) | [Impact workflow on PRs](.github/workflows/adr-impact.yml) |
| **Architectural drift** (`drift`) | [Fitness rule](.adrguard-fitness.json) and [domain project](src/AdrGuardDemo.Domain/AdrGuardDemo.Domain.csproj) | [Enforced drift workflow](.github/workflows/adr-drift.yml) |
| **AI review** (`review`) | [ADR 0004](docs/adr/0004-protect-the-domain-boundary.md) | [Manual review workflow](.github/workflows/adr-review.yml); requires an `OPENAI_API_KEY` secret |
| **JSON relationships** (`export relationships`) | [ADR Guard + Align walkthrough](docs/align-integration.md) | [Export and contract checks](.github/workflows/adr-align-export.yml) |

For exact CLI commands, expected exit codes, the historical failing/passing PR, and security notes, see the [advanced examples and CI reference](docs/demo-reference.md).

## ADR Guard + Align: a real integration example

Three linked ADRs demonstrate a real decision lifecycle:

- **[ADR 0005](docs/adr/0005-correlate-requests-with-application-logs.md)**: a historical logging-only decision, marked **Superseded**.
- **[ADR 0006](docs/adr/0006-use-distributed-tracing-for-cross-service-requests.md)**: the accepted replacement, declaring `supersedes` ADR 0005.
- **[ADR 0007](docs/adr/0007-propagate-correlation-context-across-asynchronous-boundaries.md)**: a prerequisite referenced through `depends-on`.

The two reciprocal declarations between ADRs 0005 and 0006 should become **one** confirmed replacement in Align. The dependency is exported but is **not** imported as a replacement.

The [integration guide](docs/align-integration.md) includes the JSON contract, exact commands, and an [interactive end-to-end script](scripts/verify-align-e2e.sh). **GitHub Actions verifies the real ADR Guard export, not the interactive Align import**; Align requires a local graph and a person's terminal confirmation.

## Valid and invalid scenarios

| Scenario | What it demonstrates | Where to look |
| --- | --- | --- |
| Valid supersession + dependency | Resolved relationships, no validation issues | [ADRs 0005–0007](docs/adr/README.md) |
| Unresolved reference | `ADR007` and null target | [Missing dependency example](examples/relationships/unresolved/docs/adr/0001-use-external-delivery-queue.md) |
| Supersession cycle | `ADR010` on both ADRs; invalid replacements are held back | [Circular example](examples/relationships/cycle/docs/adr/0001-use-queue-a.md) |
| Export with validation findings | `check` fails; export still writes `issues` | [Invalid-status example](examples/relationships/validation-issues/docs/adr/0001-unapproved-status.md) |

Invalid examples live under `examples/relationships/`, **outside** `docs/adr` so the main validation stays green. To verify them locally:

```bash
python3 scripts/verify-relationship-scenarios.py
```

Run `dotnet tool restore` first. The [scenario guide](examples/relationships/README.md) explains expected outcomes, while the [export workflow](.github/workflows/adr-align-export.yml) uploads both the valid and diagnostic JSON artifacts.

## More documentation

- [Detailed examples, CI and security](docs/demo-reference.md)
- [ADR Guard + Align integration](docs/align-integration.md)
- [ADR Guard CLI reference](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/cli-reference.md)
- [ADR Guard v1.12.0 release](https://github.com/rodri-oliveira-dev/adr-guard/releases/tag/v1.12.0)

This demo uses the [MIT License](LICENSE). ADR Guard findings support architectural review; they do **not** replace human approval or guarantee compliance.
