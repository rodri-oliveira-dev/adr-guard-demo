# ADR Guard demo

[Português (Brasil)](README.pt-BR.md) · [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) · [GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

[![ADR validation](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml)

This small repository demonstrates a real ADR Guard validation in GitHub Actions: the main branch contains valid Architecture Decision Records (ADRs), while a demonstration pull request preserves both a failing run and the successful run produced after fixing the document.

## What is ADR Guard?

[ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) is a .NET tool that creates and deterministically validates Architecture Decision Records. It checks documentation rules such as canonical headings, file names, statuses, relationships, and required content. It does **not** judge whether PostgreSQL, asynchronous messaging, Redis, or any other technical choice is good for a particular system. Technical quality and approval remain human decisions.

## Why validate ADRs?

ADRs preserve the context, selected option, and consequences behind important changes. Automated structural checks catch incomplete or inconsistent records during review, while the reasoning is still fresh, without pretending that a formatter can approve an architecture.

## How the demo works

The workflow runs on pull requests targeting `main` and on pushes to `main`. It checks out the repository without persisting credentials, grants only `contents: read`, and invokes the published `rodri-oliveira-dev/adr-guard@v1` Action with `command: check`.

The [demonstration pull request](https://github.com/rodri-oliveira-dev/adr-guard-demo/pull/1) follows two real commits:

1. remove the required `Consequences` section from one ADR, producing `ADR005` and exit code `1`;
2. restore the section with balanced operational trade-offs, producing exit code `0`.

See the [failed workflow run](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41699840621) and the [successful workflow run](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41700021294).

The workflow does not use secrets, `continue-on-error`, or an artificial failing command. ADR Guard's exit code is the job result. GitHub's raw log, file annotation, and step summary provide the diagnostic evidence supported by the Action.

## Example Architecture Decision Records

- [Use PostgreSQL for transactional data](docs/adr/0001-use-postgresql-for-transactional-data.md)
- [Use asynchronous communication between services](docs/adr/0002-use-asynchronous-service-communication.md)
- [Use Redis for distributed caching](docs/adr/0003-use-redis-for-distributed-cache.md)

Each example uses the canonical minimal structure: one title followed by `Status`, `Context`, `Decision`, and `Consequences` sections.

## Failing validation

The first demonstration commit removes the `Consequences` heading and content from ADR 0002. This is a genuine structural violation. ADR Guard reports `ADR005`, marks the file in the workflow UI, writes a compact job summary, and returns validation exit code `1`.

## Fixing the problem

The second commit restores `## Consequences` and explains both the benefits and costs of asynchronous communication. The earlier commit is not rewritten, so the pull request keeps the failed workflow run as reproducible history.

## Passing validation

After the correction, all three files satisfy the same deterministic rules and the [rerun exits successfully](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41700021294). The earlier [failed run](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41699840621) remains in the pull request history.

## Run locally

Install the published .NET tool and validate the directory from the repository root:

```bash
dotnet tool install --global RodriOliveira.AdrGuard
adr-guard check docs/adr
```

If the tool is already installed, update it with `dotnet tool update --global RodriOliveira.AdrGuard`.

## Use ADR Guard in your repository

Copy this minimal workflow to `.github/workflows/adr-validation.yml`:

```yaml
name: ADR validation

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  adr-guard:
    name: ADR Guard
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v7
        with:
          persist-credentials: false
      - name: Validate ADRs
        uses: rodri-oliveira-dev/adr-guard@v1
        with:
          path: docs/adr
          command: check
```

The Action requires a Linux runner with Docker. The `path` must be a repository-relative ADR directory. The moving `@v1` reference follows compatible v1 releases; use the official version-pinning guidance if your update policy requires an exact release or commit.

## Additional resources

- [GitHub Action consumer guide](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/github-action.md)
- [Complete ADR examples](https://github.com/rodri-oliveira-dev/adr-guard/tree/main/docs/examples)
- [CLI reference](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/cli-reference.md)
- [ADR Guard on GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

## License

This demonstration is available under the [MIT License](LICENSE).
