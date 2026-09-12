"""Rotas públicas de receitas: listagem e detalhe (spec 002)."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "receitas"

urlpatterns = [
    path("", views.ReceitaListView.as_view(), name="lista"),
    path("<slug:slug>/", views.ReceitaDetailView.as_view(), name="detalhe"),
]
