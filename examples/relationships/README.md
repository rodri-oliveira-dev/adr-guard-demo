# Real invalid ADR relationship examples

[English integration guide](../../docs/align-integration.md) · [Guia em português](../../docs/align-integration.pt-BR.md)

The ADR files in this folder are intentionally invalid, kept **outside** the main `docs/adr` so normal validation and Align's document import still work.

| Scenario | Input | Expected result |
| --- | --- | --- |
| Unresolved reference | [ADR](unresolved/docs/adr/0001-use-external-delivery-queue.md) | `ADR007`; `depends-on` is `unresolved` with a null target |
| Supersession cycle | [ADR A](cycle/docs/adr/0001-use-queue-a.md), [ADR B](cycle/docs/adr/0002-use-queue-b.md) | `ADR010` for both; resolved identities but invalid replacements |
| Export despite errors | [ADR](validation-issues/docs/adr/0001-unapproved-status.md) | `check` exit 1; `export` exit 0 with an invalid status serialized as null and diagnostics |

Reproduce every case from the repository root:

```bash
dotnet tool restore
python3 scripts/verify-relationship-scenarios.py
```

The Python script invokes the **released ADR Guard CLI**, checks the expected exit codes, validates error attribution and target resolution, then repeats the export to prove deterministic bytes. Real outputs are generated under `.adr-guard/scenarios/*.json` and uploaded by CI as `adr-guard-invalid-scenarios`. No handcrafted JSON is presented as actual exporter output.

These cases verify the producer contract, not consumer acceptance by Align. Do not import deliberately invalid decisions into a production decision graph.
