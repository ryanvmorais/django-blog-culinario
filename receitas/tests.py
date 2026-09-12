"""
Testes do domínio de receitas: models (spec 001) e views públicas de
listagem/detalhe (spec 002).

Estratégia de isolamento: tudo aqui é ORM/HTTP de teste do Django rodando
contra o banco de teste do pytest-django (`@pytest.mark.django_db`) — sem
mock. Não há I/O externo (rede, storage remoto) neste domínio ainda; o
upload de imagem usa `SimpleUploadedFile` em memória.
"""

from __future__ import annotations

from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.deletion import ProtectedError
from django.test import Client
from django.urls import reverse

from .models import Categoria, Receita, Tag

pytestmark = pytest.mark.django_db

User = get_user_model()


# -----------------------------------------------------------------------------
# Builders
# -----------------------------------------------------------------------------
def _categoria(**kwargs: Any) -> Categoria:
    """Cria uma Categoria com defaults sensatos, sobrescrevíveis por teste.

    Args:
        **kwargs (Any): campos que sobrescrevem o default (``nome``, etc.).

    Returns:
        Categoria: instância já persistida.
    """
    dados = {"nome": "Sobremesas"}
    dados.update(kwargs)
    return Categoria.objects.create(**dados)


def _tag(**kwargs: Any) -> Tag:
    """Cria uma Tag com defaults sensatos, sobrescrevíveis por teste.

    Args:
        **kwargs (Any): campos que sobrescrevem o default (``nome``, etc.).

    Returns:
        Tag: instância já persistida.
    """
    dados = {"nome": "Vegana"}
    dados.update(kwargs)
    return Tag.objects.create(**dados)


def _receita(**kwargs: Any) -> Receita:
    """Cria uma Receita mínima válida, sobrescrevível por teste.

    Args:
        **kwargs (Any): campos que sobrescrevem o default (``titulo``,
            ``categoria``, ``autor``, etc.).

    Returns:
        Receita: instância já persistida.
    """
    dados: dict[str, Any] = {
        "titulo": "Bolo de cenoura",
        "resumo": "Um clássico simples de fazer.",
        "ingredientes": "2 cenouras\n3 ovos\n2 xícaras de farinha",
        "modo_de_preparo": "Bata tudo no liquidificador e asse por 40 minutos.",
        "tempo_preparo_minutos": 50,
        "porcoes": 8,
        "categoria": kwargs.pop("categoria", None) or _categoria(),
    }
    dados.update(kwargs)
    return Receita.objects.create(**dados)


# -----------------------------------------------------------------------------
# Slug único (RF-01, RF-02)
# -----------------------------------------------------------------------------
def test_categoria_gera_slug_a_partir_do_nome() -> None:
    categoria = _categoria(nome="Pratos Rápidos")
    assert categoria.slug == "pratos-rapidos"


def test_categoria_com_nome_repetido_gera_slug_com_sufixo() -> None:
    """Duas categorias com o mesmo nome não colidem no slug (RF-01)."""
    primeira = _categoria(nome="Sobremesas")
    segunda = _categoria(nome="Sobremesas")

    assert primeira.slug == "sobremesas"
    assert segunda.slug == "sobremesas-2"


def test_tag_com_nome_repetido_gera_slug_com_sufixo() -> None:
    primeira = _tag(nome="sem glúten")
    segunda = _tag(nome="sem glúten")

    assert primeira.slug == "sem-gluten"
    assert segunda.slug == "sem-gluten-2"


# -----------------------------------------------------------------------------
# Relacionamentos e defaults (RF-03, RNF-01)
# -----------------------------------------------------------------------------
def test_receita_nasce_como_rascunho_com_timestamps() -> None:
    receita = _receita()

    assert receita.publicado is False
    assert receita.slug == "bolo-de-cenoura"
    assert receita.criado_em is not None
    assert receita.atualizado_em is not None


def test_excluir_categoria_em_uso_e_bloqueado() -> None:
    """`on_delete=PROTECT` impede apagar uma categoria com receita associada."""
    categoria = _categoria()
    _receita(categoria=categoria)

    with pytest.raises(ProtectedError):
        categoria.delete()


def test_excluir_tag_nao_afeta_a_receita() -> None:
    tag = _tag()
    receita = _receita()
    receita.tags.add(tag)

    tag.delete()

    receita.refresh_from_db()
    assert receita.tags.count() == 0


def test_excluir_autor_preserva_a_receita_sem_autor() -> None:
    """`on_delete=SET_NULL` preserva o conteúdo mesmo sem o usuário (ADR-2)."""
    autor = User.objects.create_user(username="cozinheira", password="senha-forte-123")
    receita = _receita(autor=autor)

    autor.delete()

    receita.refresh_from_db()
    assert receita.autor is None


# -----------------------------------------------------------------------------
# Validação de imagem de capa (RF-04)
# -----------------------------------------------------------------------------
def test_imagem_muito_grande_e_rejeitada() -> None:
    arquivo_grande = SimpleUploadedFile(
        "capa.jpg",
        b"0" * (5 * 1024 * 1024 + 1),
        content_type="image/jpeg",
    )
    receita = _receita(imagem_capa=arquivo_grande)

    with pytest.raises(ValidationError):
        receita.full_clean()


def test_extensao_de_imagem_invalida_e_rejeitada() -> None:
    arquivo_invalido = SimpleUploadedFile(
        "capa.txt",
        b"nao e uma imagem",
        content_type="text/plain",
    )
    receita = _receita(imagem_capa=arquivo_invalido)

    with pytest.raises(ValidationError):
        receita.full_clean()


def test_receita_sem_imagem_e_valida() -> None:
    receita = _receita()

    receita.full_clean()  # não deve levantar


# -----------------------------------------------------------------------------
# Admin (RF-05)
# -----------------------------------------------------------------------------
def test_listagens_do_admin_respondem_200(client: Client) -> None:
    staff = User.objects.create_user(
        username="admin-teste",
        password="senha-forte-123",
        is_staff=True,
        is_superuser=True,
    )
    client.force_login(staff)

    for url in [
        "/admin/receitas/categoria/",
        "/admin/receitas/tag/",
        "/admin/receitas/receita/",
    ]:
        resposta = client.get(url)
        assert resposta.status_code == 200


# -----------------------------------------------------------------------------
# Listagem pública (RF-01, RF-02, RNF-01)
# -----------------------------------------------------------------------------
def test_listagem_mostra_somente_publicadas(client: Client) -> None:
    publicada = _receita(titulo="Receita publicada", publicado=True)
    _receita(titulo="Receita rascunho", publicado=False)

    resposta = client.get(reverse("receitas:lista"))

    conteudo = resposta.content.decode()
    assert publicada.titulo in conteudo
    assert "Receita rascunho" not in conteudo


def test_listagem_ordena_mais_recentes_primeiro(client: Client) -> None:
    mais_antiga = _receita(titulo="Receita antiga", publicado=True)
    mais_nova = _receita(titulo="Receita nova", publicado=True)

    resposta = client.get(reverse("receitas:lista"))

    titulos = [r.titulo for r in resposta.context["receitas"]]
    assert titulos.index(mais_nova.titulo) < titulos.index(mais_antiga.titulo)


def test_listagem_pagina_com_mais_de_9_receitas(client: Client) -> None:
    categoria = _categoria()
    for i in range(10):
        _receita(titulo=f"Receita {i}", categoria=categoria, publicado=True)

    primeira_pagina = client.get(reverse("receitas:lista"))
    segunda_pagina = client.get(reverse("receitas:lista"), {"page": 2})

    assert len(primeira_pagina.context["receitas"]) == 9
    assert len(segunda_pagina.context["receitas"]) == 1


def test_listagem_pagina_inexistente_retorna_404(client: Client) -> None:
    _receita(publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"page": 999})

    assert resposta.status_code == 404


def test_listagem_nao_tem_n_mais_1_com_tags(
    client: Client, django_assert_num_queries: Any
) -> None:
    """`select_related`/`prefetch_related` mantêm a query constante (RNF-01)."""
    categoria = _categoria()
    for i in range(3):
        receita = _receita(titulo=f"Receita {i}", categoria=categoria, publicado=True)
        receita.tags.add(_tag(nome=f"tag-{i}-a"), _tag(nome=f"tag-{i}-b"))

    # 1 count (paginação) + 1 select principal (join de categoria/autor) + 1
    # prefetch de tags — não cresce com o número de receitas nem de tags.
    with django_assert_num_queries(3):
        client.get(reverse("receitas:lista"))


# -----------------------------------------------------------------------------
# Busca e filtros (RF-01 a RF-06, RNF-02)
# -----------------------------------------------------------------------------
def test_busca_por_titulo_encontra_receita(client: Client) -> None:
    receita = _receita(titulo="Bolo de cenoura", publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"q": "cenoura"})

    assert receita.titulo in [r.titulo for r in resposta.context["receitas"]]


def test_busca_por_ingrediente_encontra_receita(client: Client) -> None:
    """ "cenoura" só aparece em `ingredientes`, não no título (RF-01)."""
    receita = _receita(
        titulo="Bolo simples", ingredientes="2 cenouras\n1 ovo", publicado=True
    )

    resposta = client.get(reverse("receitas:lista"), {"q": "cenoura"})

    assert receita.titulo in [r.titulo for r in resposta.context["receitas"]]


def test_busca_sem_correspondencia_nao_encontra_nada(client: Client) -> None:
    _receita(titulo="Bolo de cenoura", publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"q": "abobora"})

    assert list(resposta.context["receitas"]) == []


def test_filtro_por_categoria_existente(client: Client) -> None:
    sobremesas = _categoria(nome="Sobremesas")
    massas = _categoria(nome="Massas")
    receita_sobremesa = _receita(titulo="Bolo", categoria=sobremesas, publicado=True)
    _receita(titulo="Lasanha", categoria=massas, publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"categoria": sobremesas.slug})

    titulos = [r.titulo for r in resposta.context["receitas"]]
    assert titulos == [receita_sobremesa.titulo]


def test_filtro_por_categoria_inexistente_retorna_lista_vazia(client: Client) -> None:
    """Slug sem correspondência é resultado vazio, não erro (RNF-02)."""
    _receita(publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"categoria": "nao-existe"})

    assert resposta.status_code == 200
    assert list(resposta.context["receitas"]) == []


def test_filtro_por_tag_existente(client: Client) -> None:
    tag_vegana = _tag(nome="vegana")
    com_tag = _receita(titulo="Receita vegana", publicado=True)
    com_tag.tags.add(tag_vegana)
    _receita(titulo="Receita comum", publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"tag": tag_vegana.slug})

    titulos = [r.titulo for r in resposta.context["receitas"]]
    assert titulos == [com_tag.titulo]


def test_filtro_por_tag_inexistente_retorna_lista_vazia(client: Client) -> None:
    _receita(publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"tag": "nao-existe"})

    assert resposta.status_code == 200
    assert list(resposta.context["receitas"]) == []


def test_busca_e_categoria_combinam_com_e_logico(client: Client) -> None:
    """Busca + categoria aplicam interseção, não união (RF-04)."""
    sobremesas = _categoria(nome="Sobremesas")
    massas = _categoria(nome="Massas")
    # ingredientes explícitos: o default do builder já contém "cenoura",
    # o que contaminaria justamente o cenário que este teste quer excluir.
    alvo = _receita(titulo="Bolo de cenoura", categoria=sobremesas, publicado=True)
    _receita(
        titulo="Lasanha de cenoura",
        categoria=massas,
        ingredientes="massa, molho, queijo",
        publicado=True,
    )
    _receita(
        titulo="Bolo de chocolate",
        categoria=sobremesas,
        ingredientes="chocolate, farinha, ovos",
        publicado=True,
    )

    resposta = client.get(
        reverse("receitas:lista"), {"q": "cenoura", "categoria": sobremesas.slug}
    )

    titulos = [r.titulo for r in resposta.context["receitas"]]
    assert titulos == [alvo.titulo]


def test_estado_vazio_mostra_mensagem_com_termo_buscado(client: Client) -> None:
    resposta = client.get(reverse("receitas:lista"), {"q": "abobora"})

    assert "Nenhuma receita encontrada" in resposta.content.decode()
    assert "abobora" in resposta.content.decode()


def test_paginacao_preserva_filtro_de_categoria_na_querystring(client: Client) -> None:
    categoria = _categoria()
    for i in range(10):
        _receita(titulo=f"Receita {i}", categoria=categoria, publicado=True)

    resposta = client.get(reverse("receitas:lista"), {"categoria": categoria.slug})

    conteudo = resposta.content.decode()
    assert f"categoria={categoria.slug}" in conteudo


# -----------------------------------------------------------------------------
# Detalhe público (RF-03, RF-04)
# -----------------------------------------------------------------------------
def test_detalhe_receita_publicada_retorna_200_com_campos(client: Client) -> None:
    receita = _receita(publicado=True)

    resposta = client.get(reverse("receitas:detalhe", kwargs={"slug": receita.slug}))

    assert resposta.status_code == 200
    conteudo = resposta.content.decode()
    assert receita.titulo in conteudo
    assert "cenouras" in conteudo  # vem de `ingredientes`, via splitlines


def test_detalhe_receita_nao_publicada_retorna_404(client: Client) -> None:
    receita = _receita(publicado=False)

    resposta = client.get(reverse("receitas:detalhe", kwargs={"slug": receita.slug}))

    assert resposta.status_code == 404


def test_detalhe_slug_inexistente_retorna_404(client: Client) -> None:
    resposta = client.get(reverse("receitas:detalhe", kwargs={"slug": "nao-existe"}))

    assert resposta.status_code == 404


def test_detalhe_sem_autor_nao_quebra(client: Client) -> None:
    receita = _receita(publicado=True, autor=None)

    resposta = client.get(reverse("receitas:detalhe", kwargs={"slug": receita.slug}))

    assert resposta.status_code == 200
    assert "Autor removido" in resposta.content.decode()
