# ADR Guard demo

[Português (Brasil)](README.pt-BR.md) · [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) · [GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

[![ADR validation](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml)

This small repository demonstrates the published ADR Guard GitHub Action without replacing architectural judgment with automation. It keeps the original deterministic validation example and adds isolated examples for catalog generation, change-impact analysis, architectural drift, and optional AI-assisted review.

## What each demonstration does

| Capability | Purpose | Result | Workflow |
| --- | --- | --- | --- |
| `check` | Validate ADR structure, names, statuses, relationships, and required content. | Deterministic gate; invalid ADRs exit `1`. | [`adr-validation.yml`](.github/workflows/adr-validation.yml) |
| `index` | Generate a deterministic Markdown catalog after validating the ADRs. | Writes only to the runner's ephemeral checkout and displays the catalog in the log and step summary. | [`adr-index.yml`](.github/workflows/adr-index.yml) |
| `impact` | Correlate Git changes with explicit ADR-to-code mappings. | Advisory report; affected and unmapped changes still exit `0`. | [`adr-impact.yml`](.github/workflows/adr-impact.yml) |
| `drift` | Verify narrow, ADR-backed architecture fitness rules from concrete evidence. | Pass, violation, or unknown; this demo enforces only a proven static violation. | [`adr-drift.yml`](.github/workflows/adr-drift.yml) |
| `review` | Ask a configured AI provider for a bounded ADR review. | Optional and advisory; provider or transport failures are not reported as clean reviews. | [`adr-review.yml`](.github/workflows/adr-review.yml) |

`check`, `impact`, and `drift` answer different questions. A valid document may describe architecture that the code no longer follows; a changed file may affect an ADR without violating it; and an inconclusive fitness check is `unknown`, never a pass.

## Original validation history

The original workflow is unchanged. It runs on pull requests targeting `main` and pushes to `main`, checks out without persisting credentials, grants only `contents: read`, and invokes `rodri-oliveira-dev/adr-guard@v1` with `command: check`.

The [original demonstration pull request](https://github.com/rodri-oliveira-dev/adr-guard-demo/pull/1) preserves two real commits:

1. removing the required `Consequences` section from ADR 0002, which produced `ADR005` and exit code `1`;
2. restoring the section with balanced operational trade-offs, which produced exit code `0`.

The [failed workflow run](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41699840621) and [successful workflow run](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41700021294) remain the historical evidence. There is no artificial failure command or `continue-on-error`; the ADR Guard exit is the job result.

## Example ADRs and code

The original ADRs remain intact:

- [Use PostgreSQL for transactional data](docs/adr/0001-use-postgresql-for-transactional-data.md)
- [Use asynchronous communication between services](docs/adr/0002-use-asynchronous-service-communication.md)
- [Use Redis for distributed caching](docs/adr/0003-use-redis-for-distributed-cache.md)

[Protect the domain boundary](docs/adr/0004-protect-the-domain-boundary.md) connects the drift example to the small [.NET solution](AdrGuardDemo.slnx). Infrastructure and application projects depend on the domain; the domain has no infrastructure reference. The source folders also give the impact map concrete PostgreSQL, messaging, Redis, and domain-boundary paths.

## Run the deterministic examples locally

The examples below use the exact published container. Docker must be running, and impact additionally needs local Git history. Building the `.slnx` file requires the .NET 10 SDK; its projects target .NET 8.

```bash
docker run --rm --read-only --network=none --cap-drop=ALL \
  --security-opt=no-new-privileges -v "$PWD:/workspace:ro" -w /workspace \
  ghcr.io/rodri-oliveira-dev/adr-guard:1.11.0 check docs/adr

dotnet build AdrGuardDemo.slnx --configuration Release
```

The equivalent installed-tool command is `adr-guard check docs/adr` after installing `RodriOliveira.AdrGuard` version `1.11.0`.

### Generate the ADR catalog

Run the **ADR index** workflow manually from the Actions tab. It has read-only repository permission, creates no commit, and uploads no artifact. The generated [`docs/adr/README.md`](docs/adr/README.md) is printed to the log and copied to the step summary.

To regenerate it locally with an installed tool:

```bash
adr-guard index docs/adr
git diff -- docs/adr/README.md
```

`index` validates before writing and preserves validation exit `1`, usage exit `2`, and operational exit `3`.

### Inspect change impact

The pull-request workflow checks out complete history because ADR Guard must calculate a merge base. [`.adrguard-impact.json`](.adrguard-impact.json) maps source areas to stable ADR identities. Changes under the mapped `Persistence`, `Messaging`, `Caching`, and `Domain` paths appear as affected decisions; changes to files such as this README remain visible as unmapped coverage gaps. Both are advisory and return `0` after a complete analysis.

```bash
adr-guard impact . --base-ref origin/main --map .adrguard-impact.json
```

The command is read-only and does not fetch. Missing or disconnected history, an invalid manifest, or a Git failure returns `3`. Open a pull request that changes a mapped source file and an unrelated file to see both categories in the Actions step summary.

### Reproduce drift outcomes

[`.adrguard-fitness.json`](.adrguard-fitness.json) prohibits the domain project from referencing infrastructure and links that rule to ADR 0004. The rule is `gate: true`, uses the built-in deterministic `forbid-project-reference` check, and is therefore safe to run with `enforce`.

Pass (`0`):

```bash
adr-guard drift . --rules .adrguard-fitness.json --policy enforce
```

New deterministic violation (`4`):

```bash
dotnet add src/AdrGuardDemo.Domain/AdrGuardDemo.Domain.csproj reference \
  src/AdrGuardDemo.Infrastructure/AdrGuardDemo.Infrastructure.csproj
adr-guard drift . --rules .adrguard-fitness.json --policy enforce
dotnet remove src/AdrGuardDemo.Domain/AdrGuardDemo.Domain.csproj reference \
  src/AdrGuardDemo.Infrastructure/AdrGuardDemo.Infrastructure.csproj
```

Unknown (`3`), caused by a conditional MSBuild reference that ADR Guard deliberately does not evaluate:

```bash
adr-guard drift . --rules .adrguard-fitness.unknown.json --policy advisory
```

The checked-in workflow uses only the conclusive primary rule. It does not use a baseline or external evidence. Missing, conditional, or ambiguous evidence remains `unknown`; absence of evidence is never compliance.

## Optional AI review

Run **Optional ADR AI review** manually with a repository-relative ADR path. The workflow explicitly selects provider `openai`, model `gpt-5`, and policy `advisory`. It requires one repository secret:

- `OPENAI_API_KEY`: an API key with the minimum provider permissions and spending limits appropriate for this demo.

No credential is stored as an Action input or example value. The workflow does not run on pull requests, does not use `pull_request_target`, and has no write permission. The Action mounts the checkout read-only and forwards only the selected provider credential to the review container. The chosen ADR content is sent to the provider, so do not select documents containing secrets or data that policy forbids sharing.

Provider use can incur charges and is nondeterministic. Model availability, rate limits, network failures, and provider output can change. Findings remain advisory and require human review; a missing secret or provider failure returns operational exit `3`. The deterministic demonstrations do not require this secret and continue to work independently.

## Exit codes and interpretation

| Code | Meaning in these demonstrations |
| --- | --- |
| `0` | Successful validation/index, completed advisory impact/review, conclusive drift pass, or advisory drift violation. |
| `1` | Deterministic ADR validation failure. |
| `2` | Invalid command, option, path, or configuration. |
| `3` | Operational/provider failure or inconclusive drift (`unknown`). |
| `4` | Explicit deterministic policy failure, including a new gate-enabled static drift violation. |

The workflows do not mask these codes. Impact candidates and unmapped changes are not compliance violations. AI findings are not policy failures under `advisory`.

## Published-version compatibility and security

The added workflows use Action source commit `ef132507ff3fda22db2128354086cee53b832fb1` and explicitly select runtime `1.11.0`. That commit is the published `v1.11.0` tag. On November 5, 2026, the coordinated `ghcr.io/rodri-oliveira-dev/adr-guard:1.11.0` and moving `:1` manifests resolved to the same multi-platform digest, `sha256:fd2ee26943490b6484a1c55d826b3c8527dcf48ac17a79b0abad51b9ddd90624`. The examples use only contracts already published before or with that release: review (`v1.1.6+`), impact (`v1.5.0+`), and Action drift (`v1.10.0+`). They do not use MADR generation.

All new workflows use `contents: read`, pin third-party Action source to full commit SHAs, disable persisted checkout credentials, and avoid repository writes, automatic artifacts, and `pull_request_target`. Only impact fetches full history, because its contract requires the merge base. The original validation workflow remains unchanged to preserve its demonstration history and moving-v1 behavior.

## Official documentation

- [GitHub Action consumer guide](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/github-action.md)
- [AI review security and usage](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/github-action-review.md)
- [Architecture impact analysis](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/guides/architecture-impact-analysis.md)
- [Architectural drift and fitness evidence](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/guides/architectural-drift.md)
- [CLI reference](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/cli-reference.md)
- [ADR Guard v1.11.0 release](https://github.com/rodri-oliveira-dev/adr-guard/releases/tag/v1.11.0)

## License

This demonstration is available under the [MIT License](LICENSE).
