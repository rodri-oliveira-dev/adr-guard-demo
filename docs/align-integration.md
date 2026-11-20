# ADR Guard + Align: real relationships export

[Português (Brasil)](align-integration.pt-BR.md) · [ADR Guard v1.12.0](https://github.com/rodri-oliveira-dev/adr-guard/releases/tag/v1.12.0) · [Align integration PR](https://github.com/aligndottech/align-cli/pull/692)

This is a public, reproducible integration example built from **actual ADR Markdown files**, not hand-authored JSON fixtures. ADR Guard v1.12.0 produces the export, and Align can consume it to record confirmed replacement decisions.

## Decisions included

The original ADRs 0001–0004 are unchanged. The added example consists of:

- [ADR 0005](adr/0005-correlate-requests-with-application-logs.md), **Superseded**: the historical logging-only approach, declaring `superseded-by` ADR 0006.
- [ADR 0006](adr/0006-use-distributed-tracing-for-cross-service-requests.md), **Accepted**: the active distributed-tracing approach, declaring `supersedes` ADR 0005 and `depends-on` ADR 0007.
- [ADR 0007](adr/0007-propagate-correlation-context-across-asynchronous-boundaries.md), **Accepted**: the active prerequisite for reliable trace propagation.

The reciprocal declarations between ADRs 0005 and 0006 must yield **one** confirmed replacement in Align, not two. The `depends-on` edge is exported but not imported as a replacement.

## Reproduce the export

With the .NET 10 SDK installed, run these commands **from the root of this repository**:

```bash
dotnet tool restore
dotnet tool run adr-guard check docs/adr
dotnet tool run adr-guard export relationships docs/adr
```

The repository's [tool manifest](../.config/dotnet-tools.json) pins `RodriOliveira.AdrGuard` to **1.12.0**. No API keys, MCP server, AI model, or remote service are required to generate the JSON.

The resulting `.adr-guard/relationships.json` has repository-root-relative paths. With the current seven ADRs, expect:

| Field | Expected result |
| --- | --- |
| `schemaVersion` | `1.0` |
| `adrs` | 7 records |
| `relationships` | 3 records: two reciprocal supersession declarations and one dependency |
| `issues` | Empty array |
| `resolution` | `resolved` on all three declarations |

An exit code of `0` from **export** only means the artifact was written. The preceding `check` step independently validates the ADRs.

## Import into Align

With a local Align CLI that includes [PR #692](https://github.com/aligndottech/align-cli/pull/692), run from the **same repository root** after generating the JSON:

```bash
align connect docs
align connect adr-guard
align ask "Which approach should we use to trace cross-service requests?"
```

`align connect docs` imports the ADR documents before the relationships are joined by their repository-relative paths. `align connect adr-guard` uses `.adr-guard/relationships.json` by default. Align should record **ADR 0006 replaces ADR 0005**, mark ADR 0005 as superseded, and base answers on ADR 0006. Run the importer a second time to check that it does not create a duplicate relationship. The command may require interactive confirmation and an initialized local Align graph.

## CI evidence

The [ADR relationships export workflow](../.github/workflows/adr-align-export.yml) uses the published CLI to validate, export, assert the expected graph, and verify byte-for-byte determinism by exporting twice. It uploads the **tool-generated JSON** as the `adr-guard-align-relationships` artifact on each successful run. Download it from the GitHub Actions run; no JSON fixture is manually maintained in this repository.

The workflow is read-only, uses pinned third-party Actions, and does not need credentials beyond GitHub's standard read-only checkout permissions. This example demonstrates contract interoperability, not automatic approval of architectural decisions.
