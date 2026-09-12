"""
Configurações de produção — alvo de deploy: PythonAnywhere.

Ativado via ``DJANGO_SETTINGS_MODULE=blog_culinario.settings.prod``. Exige
``DJANGO_SECRET_KEY`` e ``DJANGO_ALLOWED_HOSTS`` no ambiente (ver
``.env.example``); nunca reaproveita os defaults de desenvolvimento do
``base.py``.
"""

from __future__ import annotations

from .base import *  # noqa: F403 — reexporta as configurações compartilhadas
from .base import env

DEBUG = False

# Ex.: "meuusuario.pythonanywhere.com" — obrigatório, sem default permissivo.
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# Estáticos comprimidos e versionados por hash — o WhiteNoiseMiddleware (já
# ativo via base.py) serve tudo direto do processo Django no PythonAnywhere,
# sem precisar configurar um servidor de arquivos estáticos separado.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Hardening padrão para rodar atrás de HTTPS.
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# 1 semana para começar; suba para 31536000 (1 ano) só depois de confirmar
# que todo o site serve HTTPS sem exceção — HSTS não tem "desfazer" rápido.
SECURE_HSTS_SECONDS = 604_800
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
