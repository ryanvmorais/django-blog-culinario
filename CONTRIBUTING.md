# Contribuindo com o Blog Culinário

Obrigado pelo interesse! Este repositório não é só um blog de receitas — é um
laboratório de boas práticas em Django, e a sua colaboração ajuda a manter
isto como referência de qualidade para quem está aprendendo.

## O que você pode aprimorar

- Novas camadas de segurança ou hardening que faltaram na spec original.
- Cobertura de testes em cenários que ainda não têm teste.
- Clareza de comentários/docstrings em trechos que confundiram você.
- Novas "Atividades para praticar" no README, com o aprendizado que cada uma
  ensina.

## Como enviar sua sugestão

1. Faça um fork e crie uma branch a partir da `main`.
2. Faça os commits seguindo [Conventional Commits](https://www.conventionalcommits.org/)
   (`feat:`, `fix:`, `docs:`, `chore:`...).
3. Rode o portão de qualidade antes de abrir o PR — veja a skill
   `/qualidade-python` ou, na mão: `ruff check . && black --check . && mypy . && pytest`.
4. Abra o Pull Request descrevendo o quê e o porquê da mudança.

Mudança de funcionalidade (não de documentação/bug pontual)? Considere abrir
uma spec em `specs/` primeiro — veja `specs/README.md` para o formato.

## Diretrizes de qualidade

- Siga o estilo já estabelecido no código (nomes em português, docstrings nas
  funções públicas, type hints completos).
- Nunca desative uma proteção de segurança (CSRF, validação de senha, etc.)
  sem justificar o porquê no PR.
- Mantenha a coerência com o restante do projeto — este é um material de
  estudo, e consistência importa mais que preferência pessoal.

Dúvidas? Abra uma [Issue](https://github.com/ryanvmorais/django-blog-culinario/issues).

Atenciosamente,
Ryan Morais
