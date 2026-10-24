# CLAUDE.md

Este arquivo orienta o Claude Code ao trabalhar neste repositório.

## Visão geral do projeto

Blog culinário multipáginas em Django, com propósito educacional: servir de
referência para quem está aprendendo a construir uma aplicação web completa
em Python (modelagem, views, templates, autenticação, admin, segurança).
Stack mínima de propósito — SQLite, CSS puro sem framework, sem build step —
para manter o foco em Django. Deploy futuro: PythonAnywhere (ver
`blog_culinario/settings/prod.py`).

> **Python 3.12 é o piso (`requires-python = ">=3.12"`):** o PythonAnywhere lista Python só até o 3.13 e o servidor roda o 3.12, que também é o mínimo do Django 6.1. O `.python-version` fixa o 3.12 no desenvolvimento, o CI testa o 3.12 e o 3.14 (matriz) e `ruff`, `black` e `mypy` apontam para o 3.12: não use sintaxe exclusiva de versão mais nova (ex.: `except A, B:` sem parênteses, do 3.14).

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
blog_culinario/limitacao.py # rate limit por IP via cache do Django (login e comentário — spec 006)
nucleo/                    # páginas institucionais: hoje só a home (sobre e contato entram em specs futuras)
receitas/                  # domínio principal: Receita, Categoria, Tag, Comentario
usuarios/                  # autenticação (django.contrib.auth)
templates/                 # base.html + includes/ (navbar, rodapé) + 404, 403 e 500
static/css/                # design system: tokens.css (variáveis e tema escuro), fontes.css (@font-face) e base.css
static/fonts/              # Inter e Fraunces (woff2 variável, subconjunto latin, licença OFL)
specs/                     # spec-driven development — ver specs/README.md
docs/stack.md              # o que compõe a stack, por que e o que estudar
docs/design-system.html    # catálogo visual (tokens, tipografia, componentes); abra direto no navegador — usa o tokens.css e o base.css do site
.github/                   # CI (ci.yml), pip-audit semanal (pip-audit.yml), Dependabot (uv + github-actions), formulário de issue e template de PR
```

Cada app novo do domínio segue o padrão de `nucleo`: `views.py` com funções
simples primeiro, `urls.py` com `app_name` namespaced, templates em
`<app>/templates/<app>/`.

## Convenções

- **Idioma do código:** português (nomes, commits, specs, docs) — ver a regra
  completa e as exceções em `/idioma`.
- **Estilo de arquivo** (docstrings, type hints, seções, comentários): sempre
  consulte `/estilo-arquivos` antes de criar ou editar um arquivo.

## Interface (spec 008)

Regras que a auditoria de interface de 18/10/2026 deixou, guardadas por
`nucleo/test_interface.py` e `nucleo/test_tema_escuro.py`:

- **Botão:** `.botao` herda a fonte (`font: inherit`: o `<button>` do navegador
  não herda e saía em Arial 13 px), tem o rótulo no centro da caixa e 48 px de
  altura. Em formulário, largura dos campos no celular e tamanho do rótulo acima
  de 720 px. Um botão novo passa por `auditar_proporcoes.py` (skill
  `/auditoria-interface`).
- **Alinhamento:** o que é curto e isolado (aviso, formulário de acesso, botão de
  largura total) fica no centro; leitura (receita, comentários, rótulo de campo)
  à esquerda. Aviso que acompanha um título à esquerda segue o título.
- **Cor só por token:** nenhum valor de cor fora do `tokens.css`. O tema escuro é
  um bloco `prefers-color-scheme: dark` com variáveis; mudou uma cor, mude as duas
  paletas (o `test_tema_escuro.py` confere o contraste de cada par).
- **Borda de campo:** `--cor-borda-campo` (3:1); `--cor-borda` é só divisória.
- **Fontes:** hospedadas em `static/fonts/`; não volte ao Google Fonts (LGPD).
- **Cartão:** um link por cartão para teclado e leitor (a foto é `aria-hidden`);
  a lista leva um `h2` oculto entre o `h1` e os `h3`.
- **Mensagens:** na página da receita ficam dentro de `#comentarios`.
- **Erros:** o 500 é HTML completo, sem herdar o `base.html`.

## Qualidade e automação

Sequência do portão: `ruff check` → `black --check` → `mypy` → `pytest` (skill
`/qualidade-python`). CI (`.github/workflows/ci.yml`) roda a mesma sequência
em todo push/PR. O `.github/workflows/pip-audit.yml` audita o `uv.lock` com `pip-audit`
toda segunda, 09:00 de São Paulo (e à mão): o CI só roda em PR, e o Dependabot nem sempre
abre PR de correção.

## Skills deste projeto

Nenhuma skill específica do repositório ainda — usa as skills globais do
Ryan (`~/.claude/skills/`), listadas no `CLAUDE.md` global.

## Spec-driven development

Toda funcionalidade nova (modelagem, views, autenticação, etc.) nasce como uma
spec em `specs/NNN-nome/` antes do código — requisitos → design → tasks, cada
fase com aprovação humana. Ver `specs/README.md` para o formato e o roadmap
atual. Conduzido pela skill `/spec`.

## Gestão de dependências

`uv` gerencia o ambiente. Commite `pyproject.toml` **e** `uv.lock`. PRs do
Dependabot (`.github/dependabot.yml`) são revisados com `/revisar-dependabot`,
não mergeados automaticamente.
