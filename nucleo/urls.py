"""Rotas institucionais: home, sobre e contato."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "nucleo"

urlpatterns = [
    path("", views.home, name="home"),
]
