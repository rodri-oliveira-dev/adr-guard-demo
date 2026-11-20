#!/usr/bin/env python3
"""Verify error cases with the published ADR Guard CLI, not hand-authored JSON."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cli(*arguments):
    return subprocess.run(
        ["dotnet", "tool", "run", "adr-guard", *arguments],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )


def require_exit(result, expected, label):
    assert result.returncode == expected, (
        f"{label}: expected exit {expected}, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


for name in ("unresolved", "cycle", "validation-issues"):
    folder = f"examples/relationships/{name}/docs/adr"
    output = f".adr-guard/scenarios/{name}.json"

    require_exit(cli("check", folder), 1, f"{name} check")
    require_exit(cli("export", "relationships", folder, "--output", output),
                 0, f"{name} export")
    file = ROOT / output
    raw = file.read_bytes()
    payload = json.loads(raw)
    adrs = payload["adrs"]
    relations = payload["relationships"]
    issues = payload["issues"]
    assert payload["schemaVersion"] == "1.0"
    assert issues and any(item["severity"] == "error" for item in issues)
    assert all(item["path"].startswith(folder + "/") for item in issues)
    assert all(item["path"].startswith(folder + "/") for item in adrs)

    if name == "unresolved":
        assert len(adrs) == 1 and len(relations) == 1
        relation = relations[0]
        assert relation["type"] == "depends-on"
        assert relation["resolution"] == "unresolved"
        assert relation["targetPath"] is None and relation["targetIdentifier"] is None
        assert any(item["code"] == "ADR007" for item in issues)
    elif name == "cycle":
        assert len(adrs) == 2 and len(relations) == 2
        assert all(item["resolution"] == "resolved" for item in relations)
        assert all(item["type"] == "superseded-by" for item in relations)
        cycle_errors = {item["path"] for item in issues
                        if item["code"] == "ADR010" and item["severity"] == "error"}
        assert cycle_errors == {item["path"] for item in adrs}
    else:
        assert len(adrs) == 1 and adrs[0]["status"] is None
        assert not relations

    require_exit(cli("export", "relationships", folder, "--output", output),
                 0, f"{name} repeat export")
    assert file.read_bytes() == raw, f"{name}: export should be deterministic"
    print(f"PASS {name}: check=1, export=0, {len(relations)} relations, "
          f"{len(issues)} issues, deterministic output")

print("PASS all isolated relationship scenarios.")
