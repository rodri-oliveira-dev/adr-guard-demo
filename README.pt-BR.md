# Demonstração do ADR Guard

[English](README.md) · [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) · [GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

[![Validação de ADRs](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml)
[![Desvio arquitetural](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-drift.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-drift.yml)
[![Exportação de relacionamentos](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-align-export.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-align-export.yml)

Repositório prático para explorar **registros de decisões arquiteturais (ADRs)** com a CLI e a GitHub Action do [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard). Veja como validar e catalogar decisões, relacioná-las ao código, identificar desvios arquiteturais e exportar relacionamentos para o Align.

**Comece por aqui:** execute a validação e a exportação com poucos comandos. Depois, acompanhe a substituição de uma decisão, dos arquivos Markdown até o JSON. Os exemplos determinísticos não exigem modelo de IA nem chave de API.

## Início rápido

**Pré-requisitos:** Git e **SDK do .NET 10**. O manifesto de ferramentas instala o ADR Guard CLI **v1.12.0**. Execute na raiz do repositório:

```bash
git clone https://github.com/rodri-oliveira-dev/adr-guard-demo.git
cd adr-guard-demo
dotnet tool restore
dotnet tool run adr-guard check docs/adr
dotnet tool run adr-guard export relationships docs/adr
```

O exemplo principal possui **7 ADRs válidos e 3 declarações de relacionamento** (duas declarações recíprocas de substituição e uma dependência). O arquivo gerado, `.adr-guard/relationships.json`, contém `adrs`, `relationships` e `issues` (esperado: vazio). O arquivo é ignorado pelo Git. Exportação bem-sucedida significa que o JSON foi escrito; a validação é feita separadamente pelo `check`.

Sem .NET instalado? Explore os [workflows do GitHub Actions](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions) e seus registros de execução.

## Funcionalidades e exemplos

| Funcionalidade | Exemplo prático | Como executar ou verificar |
| --- | --- | --- |
| **Validação** (`check`) | [Sete ADRs](docs/adr/README.md), com estrutura, status e relacionamentos | [Workflow de validação](.github/workflows/adr-validation.yml) |
| **Catálogo** (`index`) | [Índice de ADRs](docs/adr/README.md) | [Workflow de geração manual](.github/workflows/adr-index.yml) |
| **Impacto** (`impact`) | [Mapeamento ADR–código](.adrguard-impact.json) e [arquivo de código](src/AdrGuardDemo.Infrastructure/Persistence/PostgresOrderRepository.cs) | [Workflow de impacto em PRs](.github/workflows/adr-impact.yml) |
| **Desvio arquitetural** (`drift`) | [Regra de arquitetura](.adrguard-fitness.json) e [projeto de domínio](src/AdrGuardDemo.Domain/AdrGuardDemo.Domain.csproj) | [Workflow com validação obrigatória](.github/workflows/adr-drift.yml) |
| **Revisão com IA** (`review`) | [ADR 0004](docs/adr/0004-protect-the-domain-boundary.md) | [Workflow manual de revisão](.github/workflows/adr-review.yml); requer o segredo `OPENAI_API_KEY` |
| **Relacionamentos em JSON** (`export relationships`) | [Guia ADR Guard + Align](docs/align-integration.pt-BR.md) | [Workflow de exportação e contrato](.github/workflows/adr-align-export.yml) |

Consulte a [referência avançada dos exemplos e do CI](docs/demo-reference.pt-BR.md) para comandos completos, códigos de saída, histórico da validação e detalhes de segurança.

## ADR Guard + Align: exemplo real de integração

Três ADRs relacionados demonstram o ciclo de vida de uma decisão:

- **[ADR 0005](docs/adr/0005-correlate-requests-with-application-logs.md)**: decisão histórica baseada apenas em logs, com status **Superseded** (substituída).
- **[ADR 0006](docs/adr/0006-use-distributed-tracing-for-cross-service-requests.md)**: substituta aceita, que declara `supersedes` (substitui) o ADR 0005.
- **[ADR 0007](docs/adr/0007-propagate-correlation-context-across-asynchronous-boundaries.md)**: pré-requisito indicado por `depends-on` (depende de).

As duas declarações recíprocas entre os ADRs 0005 e 0006 devem resultar em **uma única substituição** confirmada no Align. A dependência aparece na exportação, mas **não** é importada como substituição.

O [guia de integração](docs/align-integration.pt-BR.md) apresenta o contrato JSON, os comandos e o [roteiro interativo de ponta a ponta](scripts/verify-align-e2e.sh). **O GitHub Actions valida a exportação real do ADR Guard, não a importação interativa no Align**, que exige um grafo local e confirmação da pessoa no terminal.

## Cenários válidos e inválidos

| Cenário | O que demonstra | Exemplo |
| --- | --- | --- |
| Substituição e dependência válidas | Relacionamentos identificados, sem erros de validação | [ADRs 0005–0007](docs/adr/README.md) |
| Referência inexistente | `ADR007` e destino nulo | [Dependência ausente](examples/relationships/unresolved/docs/adr/0001-use-external-delivery-queue.md) |
| Substituição circular | `ADR010` nos dois ADRs; substituições inválidas são rejeitadas | [Exemplo circular](examples/relationships/cycle/docs/adr/0001-use-queue-a.md) |
| Exportação com problemas | `check` falha, mas a exportação registra `issues` | [Exemplo de status inválido](examples/relationships/validation-issues/docs/adr/0001-unapproved-status.md) |

Os exemplos inválidos ficam em `examples/relationships/`, **fora** de `docs/adr`, para preservar a validação principal. Para verificá-los localmente:

```bash
python3 scripts/verify-relationship-scenarios.py
```

Execute `dotnet tool restore` antes. O [guia dos cenários](examples/relationships/README.md) explica os resultados esperados, e o [workflow de exportação](.github/workflows/adr-align-export.yml) publica os arquivos JSON válidos e de diagnóstico.

## Documentação complementar

- [Exemplos detalhados, CI e segurança](docs/demo-reference.pt-BR.md)
- [Integração ADR Guard + Align](docs/align-integration.pt-BR.md)
- [Referência da CLI do ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/cli-reference.pt-BR.md)
- [Release ADR Guard v1.12.0](https://github.com/rodri-oliveira-dev/adr-guard/releases/tag/v1.12.0)

Este exemplo usa a [Licença MIT](LICENSE). Os diagnósticos do ADR Guard apoiam a revisão arquitetural, mas **não** substituem aprovação humana nem garantem conformidade.
