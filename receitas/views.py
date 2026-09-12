"""
Views públicas de receitas: listagem paginada com busca/filtros, e detalhe
(specs 002 e 003).

Class-based views de propósito (ADR-1 da spec 002) — em contraste com as
views baseadas em função de ``nucleo``, para o repositório mostrar os dois
estilos lado a lado.
"""

from __future__ import annotations

from typing import Any

from django.db.models import Q, QuerySet
from django.views.generic import DetailView, ListView

from .models import Receita


class ReceitaListView(ListView):
    """Lista as receitas publicadas, 9 por página, mais recentes primeiro.

    Aceita três parâmetros GET opcionais e combináveis (spec 003, ADR-1):
    ``q`` (busca em título/ingredientes), ``categoria`` e ``tag`` (slugs).
    """

    model = Receita
    template_name = "receitas/lista.html"
    context_object_name = "receitas"
    paginate_by = 9

    def get_queryset(self) -> QuerySet[Receita]:
        """Restringe a listagem a receitas publicadas, filtradas e sem N+1.

        Returns:
            QuerySet[Receita]: receitas com ``publicado=True``, com
            categoria/autor pré-carregados via ``select_related``, tags via
            ``prefetch_related``, e os filtros de busca/categoria/tag da
            querystring aplicados (RF-01 a RF-04, RNF-01, RNF-02).
        """
        queryset = (
            Receita.objects.filter(publicado=True)
            .select_related("categoria", "autor")
            .prefetch_related("tags")
        )

        termo = self.request.GET.get("q", "").strip()
        if termo:
            queryset = queryset.filter(
                Q(titulo__icontains=termo) | Q(ingredientes__icontains=termo)
            )

        categoria_slug = self.request.GET.get("categoria", "").strip()
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)

        tag_slug = self.request.GET.get("tag", "").strip()
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Expõe os filtros ativos e a querystring sem `page` (RF-06, RF-07, ADR-3).

        Args:
            **kwargs (Any): argumentos repassados ao ``super().get_context_data()``.

        Returns:
            dict[str, Any]: contexto do template, com ``termo_busca``,
            ``categoria_selecionada``, ``tag_selecionada`` (ecoam a
            querystring atual) e ``querystring`` (GET sem ``page``,
            urlencoded, usada pela paginação para preservar o filtro).
        """
        contexto = super().get_context_data(**kwargs)

        parametros = self.request.GET.copy()
        parametros.pop("page", None)

        contexto["termo_busca"] = self.request.GET.get("q", "")
        contexto["categoria_selecionada"] = self.request.GET.get("categoria", "")
        contexto["tag_selecionada"] = self.request.GET.get("tag", "")
        contexto["querystring"] = parametros.urlencode()
        return contexto


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
