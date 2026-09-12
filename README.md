# 🍲 Blog Culinário

> Um blog de receitas multipáginas construído do zero em Django — para você aprender lendo o código, não só o tutorial.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-banco-003B57?logo=sqlite&logoColor=white)
![Licença](https://img.shields.io/badge/licença-MIT-blue)

## 🎯 Objetivo do projeto

Este repositório não é (só) um blog de receitas — é uma referência para quem
está aprendendo a construir uma aplicação web multipáginas em Python/Django e
quer ver como as peças se encaixam num projeto de verdade, indo além do CRUD
básico de tutorial: modelagem de domínio, views, templates com herança,
formulários, autenticação, admin customizado, upload de imagem e segurança
aplicada — tudo em código que você pode ler de cima a baixo e entender o
porquê de cada decisão.

## 📚 O que você vai encontrar

- Modelagem de domínio com relacionamentos reais (receitas, categorias, tags,
  comentários).
- Views baseadas em função e em classe, lado a lado, para comparar os dois
  estilos.
- Herança de templates (`base.html` + blocks) e um design system próprio em
  CSS puro — sem framework de frontend, sem build step.
- Autenticação com o `django.contrib.auth` nativo do Django (sem lib externa).
- `django.contrib.admin` customizado para gerenciar o conteúdo.
- Configuração por ambiente (`settings/base|dev|prod.py`) com segredos fora do
  código.
- Testes automatizados e um pipeline de CI que roda o mesmo portão de
  qualidade usado localmente.

## 🧠 Guia de Implementação — a lógica por trás do código

1. **Apps por domínio, não por camada.** `nucleo` (institucional), `receitas`
   (o domínio principal) e `usuarios` (autenticação) — cada app cabe numa
   frase, o que facilita entender onde mexer.
2. **`settings/` em pacote, não um arquivo só.** `base.py` tem o que nunca
   muda; `dev.py` e `prod.py` só sobrescrevem o que é específico do ambiente.
   É o padrão que evita o clássico "esqueci de trocar DEBUG antes do deploy".
3. **SQLite de propósito, não por preguiça.** Zero configuração para quem
   clona o repo — o objetivo é aprender Django, não administrar um banco.
4. **CSS sem framework.** Um design system pequeno em `static/css/tokens.css`
   (cores, tipografia, espaçamento como variáveis) mantém o projeto 100%
   focado em Python, e você aprende a montar uma identidade visual do zero.
5. **Cada funcionalidade nova nasce como uma spec** em `specs/` antes do
   código — requisitos, design e tarefas, com aprovação antes de avançar de
   fase. Leia `specs/README.md` para acompanhar o raciocínio por trás de cada
   parte do projeto.

## 🛠️ Tecnologias

| Tecnologia | O que faz aqui |
|---|---|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Linguagem do projeto. |
| ![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white) | Framework web: modelos, views, templates, admin, autenticação. |
| ![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white) | Banco de dados — um arquivo, zero configuração. |
| ![uv](https://img.shields.io/badge/-uv-DE5FE9) | Instala dependências e gerencia o ambiente virtual. |
| Pillow | Processa as imagens de capa das receitas. |
| django-environ | Lê `SECRET_KEY`/`DEBUG` do ambiente em vez de deixá-los no código. |
| WhiteNoise | Serve os arquivos estáticos em produção sem precisar de Nginx/CDN. |
| pytest + pytest-django | Testes automatizados. |
| ruff, black, mypy | Lint, formatação e checagem de tipos. |

Para o porquê de cada escolha (e as alternativas descartadas), veja
[docs/stack.md](docs/stack.md).

## ⚙️ Como rodar

Pré-requisitos: [uv](https://docs.astral.sh/uv/) instalado (cuida do Python e
das dependências para você).

```bash
git clone https://github.com/ryanvmorais/django-blog-culinario.git
cd django-blog-culinario

uv sync                          # instala as dependências e cria o venv
uv run python manage.py migrate  # cria o banco SQLite local
uv run python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Não é preciso configurar nenhuma variável de
ambiente para rodar localmente — veja `.env.example` se quiser customizar algo.

> ⚠️ Quer um usuário para acessar `/admin/`? Rode
> `uv run python manage.py createsuperuser` e siga as instruções no terminal.

## 📋 Atividades para praticar

- **Adicione um campo `tempo_de_preparo` filtrável na listagem de receitas.**
  O Aprendizado: `QuerySet.filter()` combinado com um formulário de busca.
- **Crie uma rota de "receita aleatória".**
  O Aprendizado: `order_by("?")` e os limites de performance dessa abordagem
  num banco maior.
- **Adicione paginação na listagem de receitas.**
  O Aprendizado: o `Paginator` do Django e como ele conversa com o template.
- **Troque o SQLite por PostgreSQL num ambiente separado.**
  O Aprendizado: como `DATABASES` isola o projeto do banco físico — o resto
  do código não muda uma linha.

## 💡 Dúvidas ou sugestões

Encontrou algo que poderia estar mais didático, ou quer sugerir uma atividade
nova? Abra uma [Issue](https://github.com/ryanvmorais/django-blog-culinario/issues)
— toda contribuição que deixa este repositório melhor como material de
referência é bem-vinda. Veja [CONTRIBUTING.md](CONTRIBUTING.md) para o passo a
passo.

## ⚖️ Licença

[MIT](LICENSE) — use, copie e modifique à vontade, inclusive nos seus próprios
projetos.
