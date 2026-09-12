"""
Views públicas de receitas: listagem paginada e detalhe (spec 002).

Class-based views de propósito (ADR-1 da spec) — em contraste com as views
baseadas em função de ``nucleo``, para o repositório mostrar os dois
estilos lado a lado.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.views.generic import DetailView, ListView

from .models import Receita


class ReceitaListView(ListView):
    """Lista as receitas publicadas, 9 por página, mais recentes primeiro."""

    model = Receita
    template_name = "receitas/lista.html"
    context_object_name = "receitas"
    paginate_by = 9

    def get_queryset(self) -> QuerySet[Receita]:
        """Restringe a listagem a receitas publicadas, sem N+1 (RNF-01).

        Returns:
            QuerySet[Receita]: receitas com ``publicado=True``, com
            categoria/autor pré-carregados via ``select_related`` e tags
            via ``prefetch_related``.
        """
        return (
            Receita.objects.filter(publicado=True)
            .select_related("categoria", "autor")
            .prefetch_related("tags")
        )


class ReceitaDetailView(DetailView):
    """Exibe uma receita publicada pelo slug.

    O comportamento padrão do ``DetailView`` já cobre RF-04: como a
    queryset só contém receitas publicadas, um slug de rascunho ou
    inexistente resulta em 404 sem código extra.
    """

    model = Receita
    template_name = "receitas/detalhe.html"
    context_object_name = "receita"

    def get_queryset(self) -> QuerySet[Receita]:
        """Restringe o detalhe a receitas publicadas, sem N+1 (RNF-01).

        Returns:
            QuerySet[Receita]: receitas com ``publicado=True``, com
            categoria/autor/tags pré-carregados.
        """
        return (
            Receita.objects.filter(publicado=True)
            .select_related("categoria", "autor")
            .prefetch_related("tags")
        )
