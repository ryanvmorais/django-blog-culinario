# Specs do Blog Culinário

Este projeto usa spec-driven development: toda funcionalidade de domínio nasce
como uma spec em `specs/NNN-nome/` antes do código, passando por três
documentos com portão de aprovação humana entre cada um. As specs são
Markdown puro — legíveis e úteis mesmo fora do Claude Code.

## Convenções

- **Pasta:** `specs/NNN-kebab-case/`, `NNN` sequencial de 3 dígitos
  (`001`, `002`, ...), nome curto e estável (não renomeie depois de aprovado).
- **Arquivos:** `requirements.md` (o quê/porquê) → `design.md` (como) →
  `tasks.md` (quebra executável). Frontmatter YAML idêntico nos três:
  ```yaml
  ---
  feature: <título legível>
  status: rascunho | aprovado | em andamento | concluído
  data: AAAA-MM-DD
  relacionado:
    - 000-outra/requirements.md
  origem: concepcao | engenharia reversa
  ---
  ```
- **Critério de aceite:** notação **Given/When/Then**, um `### RF-NN` (heading,
  linkável) por requisito funcional; `### RNF-NN` para não-funcionais.
- **Rastreabilidade:** toda tarefa em `tasks.md` cita o(s) `RF-NN`/`ADR-N` que
  satisfaz; a última tarefa de cada etapa é o portão de qualidade
  (`/qualidade-python`), com o resultado real anotado ao executar.
- **Idioma:** português — nomes, prosa, valores de frontmatter (convenção do
  projeto, ver `/idioma`).

## Workflow

```
requirements.md ──(aprovação)──> design.md ──(aprovação)──> tasks.md ──(aprovação)──> implementação
```

Nenhuma fase avança sem o "ok" explícito do Ryan. Comandos: `/spec nova <nome>`,
`/spec design`, `/spec tasks`, `/spec implementar`, `/spec status`.

## Índice / Roadmap

| Spec | Escopo | Status |
|---|---|---|
| [001-modelagem-receitas](001-modelagem-receitas/requirements.md) | Modelos `Categoria`, `Receita`, `Tag` + admin | concluído |
| [002-listagem-detalhe-receitas](002-listagem-detalhe-receitas/requirements.md) | Views públicas: listagem paginada + detalhe de receita | concluído |
| [003-busca-e-filtros](003-busca-e-filtros/requirements.md) | Busca textual + filtro por categoria/tag na listagem | concluído |

## Notas de manutenção

Nenhuma ainda — este é o início do projeto.

## Spec-ouro

[001-modelagem-receitas](001-modelagem-receitas/) — primeira spec concluída
do projeto; use como referência de formato e de nível de detalhe.
