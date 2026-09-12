"""Rotas de autenticação: cadastro, login e logout (spec 004)."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.CadastroView.as_view(), name="cadastro"),
    path("entrar/", views.EntrarView.as_view(), name="entrar"),
    path("sair/", views.SairView.as_view(), name="sair"),
]
