# ADR Guard + Align: exportação real de relacionamentos

[English](align-integration.md) · [ADR Guard v1.12.0](https://github.com/rodri-oliveira-dev/adr-guard/releases/tag/v1.12.0) · [PR de integração do Align](https://github.com/aligndottech/align-cli/pull/692)

Este exemplo público é reproduzível a partir de **arquivos Markdown de ADR reais**, sem JSONs de teste escritos manualmente. O ADR Guard v1.12.0 gera o arquivo, que pode ser consumido pelo Align para registrar substituições confirmadas.

## Decisões do exemplo

Os ADRs originais 0001–0004 permanecem intactos. O novo cenário inclui:

- [ADR 0005](adr/0005-correlate-requests-with-application-logs.md), **Superseded**: decisão histórica baseada apenas em logs, que declara `superseded-by` ADR 0006.
- [ADR 0006](adr/0006-use-distributed-tracing-for-cross-service-requests.md), **Accepted**: decisão atual de rastreamento distribuído, que declara `supersedes` ADR 0005 e `depends-on` ADR 0007.
- [ADR 0007](adr/0007-propagate-correlation-context-across-asynchronous-boundaries.md), **Accepted**: pré-requisito para propagação de contexto de rastreamento.

As declarações recíprocas de 0005 e 0006 precisam resultar em **uma** substituição confirmada no Align, e não duas. A dependência é exportada, mas não importada como substituição.

## Reproduzir a exportação

Com o SDK do .NET 10 instalado, execute **na raiz deste repositório**:

```bash
dotnet tool restore
dotnet tool run adr-guard check docs/adr
dotnet tool run adr-guard export relationships docs/adr
```

O [manifesto de ferramentas](../.config/dotnet-tools.json) fixa `RodriOliveira.AdrGuard` na versão **1.12.0**. Não são necessárias chaves de API, servidor MCP, modelo de IA ou acesso a serviços externos para gerar o JSON.

O resultado fica em `.adr-guard/relationships.json`, com caminhos relativos à raiz. Com os sete ADRs atuais, o esperado é:

| Campo | Resultado esperado |
| --- | --- |
| `schemaVersion` | `1.0` |
| `adrs` | 7 registros |
| `relationships` | 3 registros: duas declarações recíprocas e uma dependência |
| `issues` | Array vazio |
| `resolution` | `resolved` nos três relacionamentos |

O código de saída `0` do **export** significa apenas que o arquivo foi gerado. O comando `check` executado antes faz a validação independente dos ADRs.

## Importar no Align

Com uma instalação do Align CLI que inclua o [PR #692](https://github.com/aligndottech/align-cli/pull/692), execute **na mesma raiz do repositório**, após gerar o JSON:

```bash
align connect docs
align connect adr-guard
align ask "Which approach should we use to trace cross-service requests?"
```

Primeiro, `align connect docs` importa os documentos. Depois, `align connect adr-guard` lê por padrão `.adr-guard/relationships.json` e associa os relacionamentos pelos caminhos relativos ao repositório. Espera-se que o Align registre **ADR 0006 substitui ADR 0005**, marque ADR 0005 como substituído e priorize ADR 0006 nas respostas. Uma segunda execução do importador não deve criar duplicidade. O Align pode solicitar confirmação interativa e um grafo local inicializado.

## Cenários adicionais de validação

Os [ADRs isolados de exemplo](../examples/relationships/README.md) demonstram uma **referência inexistente** (`ADR007`), uma **substituição circular** (`ADR010` nos dois ADRs) e uma **exportação com erros de validação** (status inválido). Eles não ficam na pasta principal `docs/adr`.

O CI executa `python3 scripts/verify-relationship-scenarios.py`. Para cada cenário, a CLI publicada deve retornar `1` com `check`, mas retornar `0` com `export relationships`, registrando os problemas em `issues`. O script verifica caminhos relativos à raiz, resolução dos relacionamentos e determinismo byte a byte. Os três JSONs reais são publicados no artefato `adr-guard-invalid-scenarios`.

## Teste interativo ponta a ponta com Align

Em um clone Git, com a CLI do Align que inclua o [PR #692](https://github.com/aligndottech/align-cli/pull/692) e um grafo local inicializado (`align local start`, se necessário), execute:

```bash
bash scripts/verify-align-e2e.sh
```

O roteiro executa o ADR Guard v1.12.0, importa os ADRs por `align connect docs`, importa os relacionamentos duas vezes por `align connect adr-guard`, consulta o estado do grafo e executa `align ask`. Verifique no resultado **uma** substituição confirmada (ADR 0006 substituindo 0005), nenhuma duplicação, o ADR antigo como substituído, o novo como decisão atual e a dependência sem ser importada como substituição. O comando `align ask` pode exigir um modelo de IA configurado.

**Esse teste ponta a ponta é interativo e não é marcado como aprovado no CI.** O Align exige um terminal real antes de registrar a substituição confirmada por uma pessoa; o workflow automatizado respeita essa restrição.

## Evidências no CI

O [workflow de exportação](../.github/workflows/adr-align-export.yml) usa a CLI publicada para validar, exportar, conferir o grafo esperado e verificar o determinismo byte a byte com duas execuções. Cada execução bem-sucedida disponibiliza o **JSON produzido pela ferramenta** como artefato `adr-guard-align-relationships` na aba Actions. Não há fixture JSON mantida manualmente.

O workflow tem apenas permissão de leitura, usa Actions de terceiros fixadas por SHA e não exige credenciais adicionais. A demonstração valida interoperabilidade de contratos, sem aprovar automaticamente decisões arquiteturais.
