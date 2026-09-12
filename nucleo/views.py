"""
Views institucionais: home, sobre e contato.

Ficam de fora do app ``receitas`` porque não pertencem ao domínio de
receitas — são as páginas que sustentam a navegação do site como um todo.
"""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Renderiza a página inicial do blog.

    Args:
        request (HttpRequest): requisição recebida.

    Returns:
        HttpResponse: ``nucleo/home.html`` renderizado.
    """
    return render(request, "nucleo/home.html")
