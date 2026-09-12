"""
Configuração raiz de URLs do projeto Blog Culinário.

Mapeia as rotas principais: painel Admin do Django, e as URLs de cada app de
domínio (``nucleo``, ``receitas``, ``usuarios``), cada um com seu próprio
namespace via ``app_name`` em ``urls.py``.

Em desenvolvimento (``DEBUG=True``), acrescenta a rota de ``media/`` para
servir os uploads de imagem das receitas diretamente pelo Django — em
produção, o WhiteNoise cuida só de estáticos, e mídia real usaria um
storage externo (fora do escopo deste projeto educacional).
"""

from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path("", include("nucleo.urls")),
    path("receitas/", include("receitas.urls")),
    path("usuarios/", include("usuarios.urls")),
]

if settings.DEBUG:
    # Em produção o WhiteNoise/servidor web cuida disso; em dev o Django serve
    # media/ diretamente para não exigir configuração extra de quem clona o repo.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
