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

## Evidências no CI

O [workflow de exportação](../.github/workflows/adr-align-export.yml) usa a CLI publicada para validar, exportar, conferir o grafo esperado e verificar o determinismo byte a byte com duas execuções. Cada execução bem-sucedida disponibiliza o **JSON produzido pela ferramenta** como artefato `adr-guard-align-relationships` na aba Actions. Não há fixture JSON mantida manualmente.

O workflow tem apenas permissão de leitura, usa Actions de terceiros fixadas por SHA e não exige credenciais adicionais. A demonstração valida interoperabilidade de contratos, sem aprovar automaticamente decisões arquiteturais.
