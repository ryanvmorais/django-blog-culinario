# CLAUDE.md

Este arquivo orienta o Claude Code ao trabalhar neste repositório.

## Visão geral do projeto

Blog culinário multipáginas em Django, com propósito educacional: servir de
referência para quem está aprendendo a construir uma aplicação web completa
em Python (modelagem, views, templates, autenticação, admin, segurança).
Stack mínima de propósito — SQLite, CSS puro sem framework, sem build step —
para manter o foco em Django. Deploy futuro: PythonAnywhere (ver
`blog_culinario/settings/prod.py`).

## Comandos comuns

```bash
# Instalar dependências e criar o ambiente virtual
uv sync

# Rodar o servidor de desenvolvimento
uv run python manage.py runserver

# Criar/aplicar migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Criar um usuário para acessar /admin/
uv run python manage.py createsuperuser

# Portão de qualidade (ver skill /qualidade-python)
uv run ruff check .
uv run black --check .
uv run mypy .
uv run pytest

# Rodar um único teste
uv run pytest caminho/para/tests.py::NomeDoTeste::test_caso
```

## Variáveis de ambiente

Nenhuma é obrigatória em desenvolvimento — `settings/dev.py` roda com
defaults seguros. Ver `.env.example` para a lista completa e
`blog_culinario/settings/prod.py` para o que produção exige
(`DJANGO_SECRET_KEY` e `DJANGO_ALLOWED_HOSTS` sem default).

## Arquitetura

```
blog_culinario/settings/   # base.py (comum) + dev.py / prod.py (por ambiente)
nucleo/                    # home, sobre, contato — páginas institucionais
receitas/                  # domínio principal: Receita, Categoria, Tag
usuarios/                  # autenticação (django.contrib.auth)
templates/                 # base.html + includes/ (navbar, rodapé)
static/css/                # design system: tokens.css (variáveis) + base.css
specs/                     # spec-driven development — ver specs/README.md
docs/stack.md              # o que compõe a stack, por que e o que estudar
```

Cada app novo do domínio segue o padrão de `nucleo`: `views.py` com funções
simples primeiro, `urls.py` com `app_name` namespaced, templates em
`<app>/templates/<app>/`.

## Convenções

- **Idioma do código:** português (nomes, commits, specs, docs) — ver a regra
  completa e as exceções em `/idioma`.
- **Estilo de arquivo** (docstrings, type hints, seções, comentários): sempre
  consulte `/estilo-arquivos` antes de criar ou editar um arquivo.

## Qualidade e automação

Sequência do portão: `ruff check` → `black --check` → `mypy` → `pytest` (skill
`/qualidade-python`). CI (`.github/workflows/ci.yml`) roda a mesma sequência
em todo push/PR.

## Spec-driven development

Toda funcionalidade nova (modelagem, views, autenticação, etc.) nasce como uma
spec em `specs/NNN-nome/` antes do código — requisitos → design → tasks, cada
fase com aprovação humana. Ver `specs/README.md` para o formato e o roadmap
atual. Conduzido pela skill `/spec`.

## Gestão de dependências

`uv` gerencia o ambiente. Commite `pyproject.toml` **e** `uv.lock`. PRs do
Dependabot (`.github/dependabot.yml`) são revisados com `/revisar-dependabot`,
não mergeados automaticamente.

## Skills deste projeto

Nenhuma skill específica do repositório ainda — usa as skills globais do
Ryan (`~/.claude/skills/`), listadas no `CLAUDE.md` global.
