# Demonstração do ADR Guard

[English](README.md) · [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) · [GitHub Marketplace](https://github.com/marketplace/actions/adr-guard-architecture-decision-validator)

[![Validação de ADRs](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml/badge.svg?branch=main)](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/workflows/adr-validation.yml)

Este repositório pequeno demonstra a GitHub Action publicada do ADR Guard sem substituir julgamento arquitetural por automação. O exemplo original de validação determinística foi preservado e agora convive com demonstrações isoladas de geração de catálogo, análise de impacto, drift arquitetural e revisão opcional por IA.

## O papel de cada demonstração

| Funcionalidade | Para que serve | Resultado | Workflow |
| --- | --- | --- | --- |
| `check` | Valida estrutura, nomes, status, relacionamentos e conteúdo obrigatório dos ADRs. | Gate determinístico; ADR inválido retorna `1`. | [`adr-validation.yml`](.github/workflows/adr-validation.yml) |
| `index` | Gera um catálogo Markdown determinístico depois de validar os ADRs. | Escreve apenas no checkout efêmero do runner e mostra o catálogo no log e no resumo. | [`adr-index.yml`](.github/workflows/adr-index.yml) |
| `impact` | Relaciona mudanças do Git a mapeamentos explícitos entre código e ADRs. | Relatório consultivo; mudanças afetadas ou sem mapeamento ainda retornam `0`. | [`adr-impact.yml`](.github/workflows/adr-impact.yml) |
| `drift` | Verifica regras arquiteturais restritas, ligadas a ADRs e sustentadas por evidência concreta. | Pass, violation ou unknown; este exemplo impõe apenas uma violação estática comprovada. | [`adr-drift.yml`](.github/workflows/adr-drift.yml) |
| `review` | Solicita a um provedor de IA configurado uma revisão limitada do ADR. | Opcional e consultivo; falha do provedor ou de transporte não aparece como revisão limpa. | [`adr-review.yml`](.github/workflows/adr-review.yml) |

`check`, `impact` e `drift` respondem a perguntas diferentes. Um documento válido pode descrever uma arquitetura que o código deixou de seguir; um arquivo alterado pode afetar um ADR sem violá-lo; e uma regra inconclusiva resulta em `unknown`, nunca em aprovação.

## Histórico da validação original

O workflow original não foi alterado. Ele roda em Pull Requests destinados à `main` e em pushes na `main`, faz checkout sem persistir credenciais, concede apenas `contents: read` e chama `rodri-oliveira-dev/adr-guard@v1` com `command: check`.

O [Pull Request original da demonstração](https://github.com/rodri-oliveira-dev/adr-guard-demo/pull/1) preserva dois commits reais:

1. remoção da seção obrigatória `Consequences` do ADR 0002, gerando `ADR005` e código de saída `1`;
2. restauração da seção com benefícios e custos operacionais, gerando código de saída `0`.

A [execução que falhou](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41699840621) e a [execução bem-sucedida](https://github.com/rodri-oliveira-dev/adr-guard-demo/actions/runs/41700021294) continuam sendo a evidência histórica. Não há comando artificial de falha nem `continue-on-error`: o resultado do job é o código de saída do ADR Guard.

## ADRs e código do exemplo

Os ADRs originais permanecem intactos:

- [PostgreSQL para dados transacionais](docs/adr/0001-use-postgresql-for-transactional-data.md)
- [Comunicação assíncrona entre serviços](docs/adr/0002-use-asynchronous-service-communication.md)
- [Redis como cache distribuído](docs/adr/0003-use-redis-for-distributed-cache.md)

O ADR [Proteger o limite do domínio](docs/adr/0004-protect-the-domain-boundary.md) conecta o exemplo de drift à pequena [solução .NET](AdrGuardDemo.slnx). Os projetos de infraestrutura e aplicação dependem do domínio; o domínio não referencia infraestrutura. As pastas de código também dão ao mapa de impacto caminhos concretos de PostgreSQL, mensageria, Redis e limite do domínio.

## Executar os exemplos determinísticos localmente

Os comandos abaixo usam a imagem publicada exata. O Docker precisa estar em execução; a análise de impacto também precisa do histórico Git local. A compilação do arquivo `.slnx` requer o SDK do .NET 10; os projetos têm .NET 8 como alvo.

```bash
docker run --rm --read-only --network=none --cap-drop=ALL \
  --security-opt=no-new-privileges -v "$PWD:/workspace:ro" -w /workspace \
  ghcr.io/rodri-oliveira-dev/adr-guard:1.11.0 check docs/adr

dotnet build AdrGuardDemo.slnx --configuration Release
```

Com a ferramenta instalada, o comando equivalente é `adr-guard check docs/adr`, usando o pacote `RodriOliveira.AdrGuard` na versão `1.11.0`.

### Gerar o catálogo de ADRs

Execute manualmente o workflow **ADR index** na aba Actions. Ele tem permissão de leitura, não cria commit e não publica artifact. O arquivo gerado [`docs/adr/README.md`](docs/adr/README.md) aparece no log e no resumo da etapa.

Para recriar o catálogo localmente com a ferramenta instalada:

```bash
adr-guard index docs/adr
git diff -- docs/adr/README.md
```

`index` valida antes de escrever e preserva os códigos `1` para falha de validação, `2` para uso inválido e `3` para falha operacional.

### Inspecionar o impacto de mudanças

O workflow de Pull Request baixa o histórico completo porque o ADR Guard precisa calcular a base comum. O arquivo [`.adrguard-impact.json`](.adrguard-impact.json) associa áreas do código a identidades estáveis dos ADRs. Alterações nas pastas mapeadas `Persistence`, `Messaging`, `Caching` e `Domain` aparecem como decisões afetadas; mudanças em arquivos como este README permanecem visíveis como lacunas de mapeamento. Depois de uma análise completa, ambos os casos são consultivos e retornam `0`.

```bash
adr-guard impact . --base-ref origin/main --map .adrguard-impact.json
```

O comando é somente leitura e não executa `fetch`. Histórico ausente ou desconectado, manifesto inválido ou falha do Git retorna `3`. Para ver as duas categorias no resumo do GitHub Actions, abra um PR que altere um arquivo de código mapeado e outro arquivo sem mapeamento.

### Reproduzir os resultados de drift

O arquivo [`.adrguard-fitness.json`](.adrguard-fitness.json) proíbe o projeto de domínio de referenciar infraestrutura e liga essa regra ao ADR 0004. A regra usa `gate: true` e a verificação determinística nativa `forbid-project-reference`, portanto pode rodar com política `enforce`.

Conforme (`0`):

```bash
adr-guard drift . --rules .adrguard-fitness.json --policy enforce
```

Nova violação determinística (`4`):

```bash
dotnet add src/AdrGuardDemo.Domain/AdrGuardDemo.Domain.csproj reference \
  src/AdrGuardDemo.Infrastructure/AdrGuardDemo.Infrastructure.csproj
adr-guard drift . --rules .adrguard-fitness.json --policy enforce
dotnet remove src/AdrGuardDemo.Domain/AdrGuardDemo.Domain.csproj reference \
  src/AdrGuardDemo.Infrastructure/AdrGuardDemo.Infrastructure.csproj
```

Inconclusivo (`3`), causado por uma referência condicional do MSBuild que o ADR Guard deliberadamente não avalia:

```bash
adr-guard drift . --rules .adrguard-fitness.unknown.json --policy advisory
```

O workflow versionado usa somente a regra principal, que é conclusiva. Não há baseline nem evidência externa. Evidência ausente, condicional ou ambígua continua sendo `unknown`; falta de evidência nunca é conformidade.

## Revisão opcional por IA

Execute manualmente **Optional ADR AI review** informando o caminho de um ADR dentro do repositório. O workflow seleciona explicitamente o provider `openai`, o modelo `gpt-5` e a política `advisory`. Ele exige um único secret do repositório:

- `OPENAI_API_KEY`: chave de API com as menores permissões e limites de gasto adequados à demonstração.

Nenhuma credencial é armazenada como input da Action ou como valor de exemplo. O workflow não roda em Pull Requests, não usa `pull_request_target` e não possui permissão de escrita. A Action monta o checkout como somente leitura e encaminha ao contêiner apenas a credencial do provider selecionado. O conteúdo do ADR escolhido é enviado ao provider; não selecione documentos com segredos ou dados que não possam ser compartilhados segundo as políticas aplicáveis.

O uso do provider pode gerar custos e não é determinístico. Disponibilidade do modelo, limites de requisição, rede e respostas podem variar. Os achados são consultivos e exigem revisão humana; secret ausente ou falha do provider retorna `3`. As demonstrações determinísticas não usam esse secret e continuam independentes.

## Códigos de saída e interpretação

| Código | Significado nestas demonstrações |
| --- | --- |
| `0` | Validação/indexação concluída, impacto/revisão consultiva concluídos, drift conforme ou violação em modo consultivo. |
| `1` | Falha na validação determinística de ADRs. |
| `2` | Comando, opção, caminho ou configuração inválida. |
| `3` | Falha operacional/do provider ou drift inconclusivo (`unknown`). |
| `4` | Falha de política determinística explícita, incluindo nova violação estática com gate habilitado. |

Os workflows não mascaram esses códigos. Decisões afetadas e mudanças sem mapeamento não são violações de conformidade. Achados da IA não são falhas de política em `advisory`.

## Compatibilidade publicada e segurança

Os workflows adicionados usam o commit da Action `ef132507ff3fda22db2128354086cee53b832fb1` e selecionam explicitamente o runtime `1.11.0`. Esse commit corresponde à tag publicada `v1.11.0`. Em 5 de novembro de 2026, os manifestos coordenados `ghcr.io/rodri-oliveira-dev/adr-guard:1.11.0` e `:1` apontavam para o mesmo digest multiplataforma, `sha256:fd2ee26943490b6484a1c55d826b3c8527dcf48ac17a79b0abad51b9ddd90624`. Os exemplos usam somente contratos já publicados antes ou junto dessa versão: review (`v1.1.6+`), impact (`v1.5.0+`) e drift na Action (`v1.10.0+`). A geração MADR não é usada.

Todos os workflows novos concedem apenas `contents: read`, fixam Actions de terceiros por SHA completo, desativam a persistência de credenciais no checkout e evitam escrita no repositório, artifacts automáticos e `pull_request_target`. Somente impact baixa o histórico completo, pois seu contrato exige a base comum. O workflow de validação original permanece inalterado para preservar o histórico da demonstração e o comportamento da referência móvel v1.

## Documentação oficial

- [Guia da GitHub Action](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/github-action.pt-BR.md)
- [Segurança e uso da revisão por IA](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/github-action-review.pt-BR.md)
- [Análise de impacto arquitetural](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/guides/architecture-impact-analysis.pt-BR.md)
- [Drift arquitetural e evidências de fitness](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/guides/architectural-drift.pt-BR.md)
- [Referência da CLI](https://github.com/rodri-oliveira-dev/adr-guard/blob/main/docs/cli-reference.pt-BR.md)
- [Release ADR Guard v1.11.0](https://github.com/rodri-oliveira-dev/adr-guard/releases/tag/v1.11.0)

## Licença

Esta demonstração está disponível sob a [Licença MIT](LICENSE).
