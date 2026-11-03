# Demonstração do ADR Guard

[English](README.md) · [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) · [GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

[![Validação de ADRs](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml)

Este repositório pequeno mostra o ADR Guard funcionando de verdade no GitHub Actions. A branch `main` contém Architecture Decision Records (ADRs) válidos, enquanto um Pull Request de demonstração preserva uma execução que falhou e outra que passou depois da correção.

## O que é o ADR Guard?

O [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) é uma ferramenta .NET para criar e validar ADRs de maneira determinística. Ela confere regras documentais, como títulos canônicos, nomes de arquivo, status, relacionamentos e conteúdo obrigatório. A ferramenta **não** decide se PostgreSQL, mensageria assíncrona, Redis ou qualquer outra escolha é adequada para um sistema. A análise técnica e a aprovação continuam sendo responsabilidade das pessoas.

## Por que validar ADRs?

ADRs registram o contexto, a escolha e as consequências de mudanças importantes. A validação automática encontra documentos incompletos ou inconsistentes durante a revisão, quando o raciocínio ainda está fresco, sem confundir estrutura correta com aprovação arquitetural.

## Como a demonstração funciona

O workflow roda em Pull Requests destinados à `main` e em pushes na `main`. Ele faz checkout sem manter credenciais, concede apenas `contents: read` e chama a Action publicada `rodri-oliveira-dev/adr-guard@v1` com `command: check`.

O [Pull Request de demonstração](https://github.com/rodri-oliveira-dev/adr-guard-demo/pulls) contém dois commits reais:

1. remoção da seção obrigatória `Consequences` de um ADR, gerando `ADR005` e código de saída `1`;
2. restauração da seção com benefícios e custos operacionais, gerando código de saída `0`.

O workflow não usa segredos, `continue-on-error` nem um comando artificial para provocar a falha. O resultado do job é o próprio código de saída do ADR Guard. O log bruto, a anotação no arquivo e o resumo da etapa apresentam as evidências oferecidas pela Action.

## ADRs usados no exemplo

- [PostgreSQL para dados transacionais](docs/adr/0001-use-postgresql-for-transactional-data.md)
- [Comunicação assíncrona entre serviços](docs/adr/0002-use-asynchronous-service-communication.md)
- [Redis como cache distribuído](docs/adr/0003-use-redis-for-distributed-cache.md)

Cada arquivo usa a estrutura canônica mínima: um título e as seções `Status`, `Context`, `Decision` e `Consequences`.

## Validação com falha

O primeiro commit da demonstração remove o título e o conteúdo de `Consequences` do ADR 0002. É uma violação estrutural real. O ADR Guard informa `ADR005`, associa o diagnóstico ao arquivo na interface do workflow, escreve um resumo compacto e retorna o código de validação `1`.

## Corrigindo o documento

O segundo commit restaura `## Consequences` e descreve ganhos e custos da comunicação assíncrona. O commit anterior não é reescrito; assim, o Pull Request mantém a execução com falha em seu histórico reproduzível.

## Validação aprovada

Depois da correção, os três arquivos atendem às mesmas regras determinísticas e a nova execução termina com código `0`. O histórico do workflow pode ser aberto pelo badge; os links diretos das execuções são registrados no repositório depois que o GitHub as conclui.

## Executar localmente

Instale a ferramenta publicada e valide o diretório a partir da raiz do repositório:

```bash
dotnet tool install --global RodriOliveira.AdrGuard
adr-guard check docs/adr
```

Se ela já estiver instalada, use `dotnet tool update --global RodriOliveira.AdrGuard`.

## Usar no seu repositório

Copie este exemplo mínimo para `.github/workflows/adr-validation.yml`:

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

A Action exige um runner Linux com Docker. O `path` deve apontar para um diretório de ADRs relativo ao repositório. A referência móvel `@v1` acompanha releases compatíveis da linha v1; consulte a orientação oficial de pinning caso sua política exija uma versão ou commit exato.

## Recursos adicionais

- [Guia da GitHub Action](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/github-action.pt-BR.md)
- [Exemplos completos de ADR](https://github.com/rodri-oliveira-dev/adr-guard/tree/main/docs/examples)
- [Referência da CLI](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/cli-reference.pt-BR.md)
- [ADR Guard no GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

## Licença

Esta demonstração está disponível sob a [Licença MIT](LICENSE).
