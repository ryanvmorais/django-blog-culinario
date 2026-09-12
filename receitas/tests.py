"""
Testes do domínio de receitas (spec 001): slug único, relacionamentos,
validação de imagem e admin.

Estratégia de isolamento: tudo aqui é ORM puro do Django rodando contra o
banco de teste do pytest-django (`@pytest.mark.django_db`) — sem mock. Não
há I/O externo (rede, storage remoto) neste domínio ainda; o upload de
imagem usa `SimpleUploadedFile` em memória.
"""

from __future__ import annotations

from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.deletion import ProtectedError
from django.test import Client

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
