"""Rotas públicas de receitas: listagem, detalhe (spec 002) e comentário (spec 005)."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "receitas"

urlpatterns = [
    path("", views.ReceitaListView.as_view(), name="lista"),
    path("<slug:slug>/", views.ReceitaDetailView.as_view(), name="detalhe"),
    path(
        "<slug:slug>/comentar/", views.ComentarioCreateView.as_view(), name="comentar"
    ),
]
