"""
Testes de autenticação: cadastro, login, logout e reflexo na navbar (spec 004).

Estratégia de isolamento: ORM/HTTP de teste do Django, sem mock — login e
logout são o comportamento nativo do ``django.contrib.auth``, exercitado
via `Client` como um navegador faria.
"""

from __future__ import annotations

from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db

User = get_user_model()


# -----------------------------------------------------------------------------
# Builders
# -----------------------------------------------------------------------------
def _dados_cadastro(**kwargs: Any) -> dict[str, Any]:
    """Payload válido para o formulário de cadastro, sobrescrevível por teste.

    Args:
        **kwargs (Any): campos que sobrescrevem o default (``username``,
            ``password1``, etc.).

    Returns:
        dict[str, Any]: dados prontos para o POST em `usuarios:cadastro`.
    """
    dados = {
        "username": "chef-teste",
        "email": "chef@example.com",
        "password1": "uma-senha-bem-forte-123",
        "password2": "uma-senha-bem-forte-123",
    }
    dados.update(kwargs)
    return dados


# -----------------------------------------------------------------------------
# Cadastro (RF-01, RF-06)
# -----------------------------------------------------------------------------
def test_cadastro_com_dados_validos_cria_e_autentica(client: Client) -> None:
    resposta = client.post(reverse("usuarios:cadastro"), _dados_cadastro(), follow=True)

    assert User.objects.filter(username="chef-teste").exists()
    assert resposta.wsgi_request.user.is_authenticated
    assert "Bem-vindo(a)" in resposta.content.decode()


def test_cadastro_com_username_duplicado_nao_cria_conta(client: Client) -> None:
    User.objects.create_user(username="chef-teste", password="outra-senha-123")

    client.post(reverse("usuarios:cadastro"), _dados_cadastro())

    assert User.objects.filter(username="chef-teste").count() == 1


def test_cadastro_com_senha_fraca_nao_cria_conta(client: Client) -> None:
    client.post(
        reverse("usuarios:cadastro"), _dados_cadastro(password1="123", password2="123")
    )

    assert not User.objects.filter(username="chef-teste").exists()


def test_cadastro_com_senhas_divergentes_nao_cria_conta(client: Client) -> None:
    client.post(
        reverse("usuarios:cadastro"),
        _dados_cadastro(password2="uma-senha-completamente-diferente"),
    )

    assert not User.objects.filter(username="chef-teste").exists()


# -----------------------------------------------------------------------------
# Login (RF-02, RF-05, RF-06)
# -----------------------------------------------------------------------------
def test_login_com_credenciais_corretas_autentica(client: Client) -> None:
    User.objects.create_user(username="chef-teste", password="uma-senha-bem-forte-123")

    resposta = client.post(
        reverse("usuarios:entrar"),
        {"username": "chef-teste", "password": "uma-senha-bem-forte-123"},
        follow=True,
    )

    assert resposta.wsgi_request.user.is_authenticated
    assert "Bem-vindo(a) de volta" in resposta.content.decode()


def test_login_com_credenciais_erradas_mostra_mensagem_generica(client: Client) -> None:
    User.objects.create_user(username="chef-teste", password="uma-senha-bem-forte-123")

    resposta = client.post(
        reverse("usuarios:entrar"),
        {"username": "chef-teste", "password": "senha-errada"},
    )

    assert not resposta.wsgi_request.user.is_authenticated
    # mensagem genérica do AuthenticationForm — não diz qual campo errou
    assert "corretos" in resposta.content.decode()


def test_login_redireciona_para_next_apos_autenticar(client: Client) -> None:
    User.objects.create_user(username="chef-teste", password="uma-senha-bem-forte-123")

    resposta = client.post(
        reverse("usuarios:entrar") + "?next=/receitas/",
        {"username": "chef-teste", "password": "uma-senha-bem-forte-123"},
    )

    assert resposta.status_code == 302
    assert resposta["Location"] == "/receitas/"


# -----------------------------------------------------------------------------
# Logout (RF-03, RF-06, ADR-2)
# -----------------------------------------------------------------------------
def test_logout_encerra_sessao(client: Client) -> None:
    usuario = User.objects.create_user(
        username="chef-teste", password="uma-senha-bem-forte-123"
    )
    client.force_login(usuario)

    resposta = client.post(reverse("usuarios:sair"), follow=True)

    assert not resposta.wsgi_request.user.is_authenticated
    assert "Você saiu da sua conta." in resposta.content.decode()


def test_logout_via_get_nao_e_permitido(client: Client) -> None:
    """`LogoutView` só aceita POST desde o Django 4.1 (ADR-2)."""
    usuario = User.objects.create_user(
        username="chef-teste", password="uma-senha-bem-forte-123"
    )
    client.force_login(usuario)

    resposta = client.get(reverse("usuarios:sair"))

    assert resposta.status_code == 405


# -----------------------------------------------------------------------------
# Navbar reflete autenticação (RF-04)
# -----------------------------------------------------------------------------
def test_navbar_mostra_entrar_para_anonimo(client: Client) -> None:
    resposta = client.get(reverse("nucleo:home"))

    conteudo = resposta.content.decode()
    assert "Entrar" in conteudo
    assert "Cadastrar" in conteudo


def test_navbar_mostra_username_e_sair_para_autenticado(client: Client) -> None:
    usuario = User.objects.create_user(
        username="chef-teste", password="uma-senha-bem-forte-123"
    )
    client.force_login(usuario)

    resposta = client.get(reverse("nucleo:home"))

    conteudo = resposta.content.decode()
    assert "chef-teste" in conteudo
    assert "Sair" in conteudo
    assert "Entrar" not in conteudo
