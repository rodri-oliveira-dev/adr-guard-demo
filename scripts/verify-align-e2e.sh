#!/usr/bin/env bash
# Run manually: Align requires a real terminal for confirmed replacement decisions.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [[ ! -t 0 || ! -t 1 ]]; then
  echo "This Align E2E test must run in an interactive terminal." >&2
  exit 2
fi
for command in dotnet align git; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "Required command not found: $command" >&2
    exit 2
  }
done

echo "Prerequisites: Align CLI containing PR #692 and an initialized local graph."
echo "If needed, run 'align local start' before this script."
echo "This test imports repository decisions into your local Align graph."
align local status

echo "1/5 Validate and export with the published ADR Guard CLI"
dotnet tool restore
dotnet tool run adr-guard check docs/adr
dotnet tool run adr-guard export relationships docs/adr

echo "2/5 Import repository ADRs"
align connect docs --approve --env local

echo "3/5 Record replacement from the actual exported JSON"
align connect adr-guard --env local

echo "4/5 Reimport to verify no duplicate edge is added"
align connect adr-guard --env local
align local status

echo "5/5 Ask which decision is current"
align ask "Which approach should we use to trace cross-service requests?" --env local

cat <<'CHECKLIST'

Inspect the Align output and local graph:
[ ] ADR 0006 replaces ADR 0005 exactly once
[ ] ADR 0005 is marked superseded
[ ] ADR 0006 is preferred in the answer
[ ] ADR 0007's depends-on edge is NOT imported as a replacement
[ ] The second import added no duplicate edge

This interactive verification is not part of unattended CI. An AI model
may need configuring for 'align ask'. Only report E2E success after inspection.
CHECKLIST
