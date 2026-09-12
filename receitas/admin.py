"""Admin do domínio de receitas (spec 001, RF-05)."""

from __future__ import annotations

from django.contrib import admin

from .models import Categoria, Receita, Tag


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Listagem e formulário de categorias, com slug preenchido pelo nome."""

    list_display = ["nome", "slug"]
    search_fields = ["nome"]
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Listagem e formulário de tags, com slug preenchido pelo nome."""

    list_display = ["nome", "slug"]
    search_fields = ["nome"]
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    """Listagem e formulário de receitas.

    ``autocomplete_fields`` + ``list_select_related`` evitam que a listagem
    dispare uma query de categoria/autor por linha à medida que o volume de
    receitas cresce (RNF-02).
    """

    list_display = ["titulo", "categoria", "autor", "publicado", "criado_em"]
    list_filter = ["categoria", "publicado"]
    search_fields = ["titulo"]
    prepopulated_fields = {"slug": ("titulo",)}
    autocomplete_fields = ["categoria", "autor"]
    list_select_related = ["categoria", "autor"]
