"""
Resume os relatórios do Lighthouse CI numa tabela em Markdown.

O workflow ``lighthouse.yml`` roda o ``lhci`` duas vezes (mobile e desktop) e cada
passada grava um ``manifest.json`` e os relatórios em ``.lighthouseci/<perfil>/``.
Este script lê o relatório representativo (a mediana) de cada página e imprime uma
tabela por perfil, para o workflow anexar ao resumo do job
(``$GITHUB_STEP_SUMMARY``). Só usa a biblioteca padrão: roda sem instalar nada.

Uso (da raiz do repositório)::

    python3 .github/lighthouse/resumo.py mobile >> "$GITHUB_STEP_SUMMARY"

Sem argumento, resume os dois perfis (útil para rodar localmente). O workflow roda
um perfil por job (matriz), então passa o nome do perfil.

Os valores locais ou do CI são comparação relativa entre PRs; o Lighthouse só dá
números reais em produção.
"""

import json
import sys
from pathlib import Path
from typing import Any

# Onde o `lhci autorun` grava os relatórios (o `outputDir` dos JSON é subpasta).
PASTA = Path(".lighthouseci")
# Os dois perfis que o workflow audita; sem argumento, o script resume os dois.
PERFIS = ("mobile", "desktop")

# Categorias exibidas, na ordem das colunas, com o rótulo de cada uma.
CATEGORIAS = [
    ("performance", "Perf."),
    ("accessibility", "Acessib."),
    ("best-practices", "Boas práticas"),
    ("seo", "SEO"),
]


# ---------------------------------------------------------------------------
# Leitura dos relatórios
# ---------------------------------------------------------------------------
def relatorios_representativos(perfil: str) -> list[dict[str, Any]]:
    """
    Carrega o relatório representativo de cada URL de um perfil.

    O Lighthouse CI marca no ``manifest.json`` qual das rodadas de cada URL é a
    mediana (``isRepresentativeRun``).

    Args:
        perfil (str): ``"mobile"`` ou ``"desktop"``.

    Returns:
        list[dict[str, Any]]: Relatórios (JSON do Lighthouse) na ordem do manifesto.
            Vazia se o perfil não gerou relatórios (por exemplo, se o passo falhou
            antes).
    """
    manifesto = PASTA / perfil / "manifest.json"
    if not manifesto.is_file():
        return []
    entradas = json.loads(manifesto.read_text(encoding="utf-8"))
    return [
        json.loads(Path(entrada["jsonPath"]).read_text(encoding="utf-8"))
        for entrada in entradas
        if entrada.get("isRepresentativeRun")
    ]


def pagina(relatorio: dict[str, Any]) -> str:
    """
    Extrai o caminho da URL de um relatório (``/receitas/``, ``/``).

    Args:
        relatorio (dict[str, Any]): JSON de um relatório do Lighthouse.

    Returns:
        str: Caminho da página, sem host.
    """
    url = relatorio["finalUrl"]
    return "/" + url.split("/", 3)[3] if url.count("/") > 2 else url


# ---------------------------------------------------------------------------
# Tabela
# ---------------------------------------------------------------------------
def tabela(perfil: str, relatorios: list[dict[str, Any]]) -> str:
    """
    Monta a tabela Markdown de um perfil.

    Args:
        perfil (str): Nome do perfil, usado no título.
        relatorios (list[dict[str, Any]]): Relatórios representativos do perfil.

    Returns:
        str: Título e tabela em Markdown, com notas de 0 a 100, LCP, CLS e o peso
            transferido em KiB.
    """
    cabecalho = [rotulo for _, rotulo in CATEGORIAS] + ["LCP", "CLS", "Peso (KiB)"]
    linhas = [
        f"### Lighthouse — {perfil}",
        "",
        "| Página | " + " | ".join(cabecalho) + " |",
        "|---|" + "---:|" * len(cabecalho),
    ]
    for r in relatorios:
        notas = [round((r["categories"][c]["score"] or 0) * 100) for c, _ in CATEGORIAS]
        a = r["audits"]
        celulas = [
            *notas,
            f"{a['largest-contentful-paint']['numericValue'] / 1000:.1f} s",
            f"{a['cumulative-layout-shift']['numericValue']:.3f}",
            f"{a['total-byte-weight']['numericValue'] / 1024:.0f}",
        ]
        linhas.append(f"| `{pagina(r)}` | " + " | ".join(map(str, celulas)) + " |")
    return "\n".join(linhas)


def main(argumentos: list[str]) -> int:
    """
    Imprime a tabela de cada perfil pedido que gerou relatórios.

    Args:
        argumentos (list[str]): Perfis a resumir (``mobile``, ``desktop``). Vazio
            resume os dois.

    Returns:
        int: ``0`` sempre; um perfil sem relatórios só é mencionado no texto, para o
            resumo aparecer mesmo quando um passo anterior falhou.
    """
    for perfil in argumentos or PERFIS:
        relatorios = relatorios_representativos(perfil)
        if relatorios:
            print(tabela(perfil, relatorios), end="\n\n")
        else:
            print(
                f"### Lighthouse — {perfil}\n\nSem relatórios (o passo falhou antes).\n"
            )
    print(
        "_Valores do CI são comparação relativa entre PRs; os números reais "
        "só existem em produção._"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
