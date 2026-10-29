"""
Testes de que o README em inglês mantém a forma do README em português.

O ``README.en.md`` é uma tradução, e tradução envelhece: uma seção acrescentada ao
``README.md`` que ninguém leva para o outro arquivo deixa o leitor estrangeiro com
um projeto mais velho do que o publicado. Os testes comparam estrutura, nunca
redação: a ordem dos títulos, as linhas da tabela de tecnologias, os desafios
numerados, os links de troca entre os dois arquivos e os arquivos do repositório
para onde os links do inglês apontam.

Estratégia de isolamento: só os dois READMEs e a existência dos arquivos que eles
linkam são lidos, sem banco nem cliente HTTP.
"""

from __future__ import annotations

import re
from pathlib import Path

# -----------------------------------------------------------------------------
# Constantes
# -----------------------------------------------------------------------------

# Os dois READMEs ficam na raiz do repositório.
RAIZ = Path(__file__).resolve().parent.parent
PORTUGUES = RAIZ / "README.md"
INGLES = RAIZ / "README.en.md"

# Alvo de link ou de imagem Markdown: o texto entre "](" e o parêntese que fecha.
ALVO = re.compile(r"\]\(([^)\s]+)\)")

# Título ATX; a sequência de "#" é o nível.
TITULO = re.compile(r"^(#{1,6}) ")

# Item de lista numerada no nível raiz ("1. ", "2. "...).
ITEM_NUMERADO = re.compile(r"^\d+\.\s")


# -----------------------------------------------------------------------------
# Apoio
# -----------------------------------------------------------------------------


def _fora_dos_blocos(caminho: Path) -> list[str]:
    """
    Lê um arquivo Markdown e descarta as linhas dentro de blocos de código.

    Args:
        caminho (Path): O arquivo Markdown.

    Returns:
        list[str]: As linhas restantes, para que um comentário ``#`` num bloco de
            shell não seja tomado por título.
    """
    mantidas: list[str] = []
    em_bloco = False
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if linha.startswith("```") or linha.lstrip().startswith("```"):
            em_bloco = not em_bloco
        elif not em_bloco:
            mantidas.append(linha)
    return mantidas


def _niveis(caminho: Path) -> list[int]:
    """
    Lista os níveis de título de um README, em ordem.

    Args:
        caminho (Path): O arquivo Markdown.

    Returns:
        list[int]: Um nível (1 a 6) por título.
    """
    achados = (TITULO.match(linha) for linha in _fora_dos_blocos(caminho))
    return [len(m.group(1)) for m in achados if m]


def _linhas_da_tabela(caminho: Path, primeira_celula: str) -> int:
    """
    Conta as linhas de dados da tabela cujo cabeçalho começa com uma célula.

    Args:
        caminho (Path): O arquivo Markdown.
        primeira_celula (str): O texto da primeira célula do cabeçalho.

    Returns:
        int: As linhas abaixo do cabeçalho, sem contar o cabeçalho e o separador.
    """
    linhas = _fora_dos_blocos(caminho)
    inicio = next(
        i for i, linha in enumerate(linhas) if linha.startswith(f"| {primeira_celula} ")
    )
    total = 0
    for linha in linhas[inicio + 2 :]:
        if not linha.startswith("|"):
            break
        total += 1
    return total


# -----------------------------------------------------------------------------
# Testes
# -----------------------------------------------------------------------------


def test_os_dois_readmes_tem_os_mesmos_titulos_na_mesma_ordem() -> None:
    assert _niveis(INGLES) == _niveis(PORTUGUES)


def test_os_dois_readmes_tem_as_mesmas_linhas_na_tabela_de_tecnologias() -> None:
    assert _linhas_da_tabela(INGLES, "Tool") == _linhas_da_tabela(
        PORTUGUES, "Ferramenta"
    )


def test_os_dois_readmes_tem_a_mesma_quantidade_de_itens_numerados() -> None:
    def contar(caminho: Path) -> int:
        return sum(
            1 for linha in _fora_dos_blocos(caminho) if ITEM_NUMERADO.match(linha)
        )

    assert contar(INGLES) == contar(PORTUGUES)


def test_cada_readme_linka_o_outro_nas_primeiras_linhas() -> None:
    ingles = "\n".join(_fora_dos_blocos(INGLES)[:5])
    portugues = "\n".join(_fora_dos_blocos(PORTUGUES)[:5])

    assert "(README.md)" in ingles
    assert "(README.en.md)" in portugues


def test_os_links_relativos_do_ingles_apontam_para_arquivos_que_existem() -> None:
    texto = INGLES.read_text(encoding="utf-8")
    relativos = [
        a for a in ALVO.findall(texto) if not a.startswith(("https://", "#", "mailto:"))
    ]

    ausentes = [a for a in relativos if not (RAIZ / a.split("#")[0]).exists()]

    assert relativos
    assert ausentes == []
