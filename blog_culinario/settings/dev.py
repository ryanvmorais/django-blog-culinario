"""
Configurações de desenvolvimento local.

É o settings padrão do ``manage.py`` — quem clona o repo roda
``python manage.py runserver`` sem precisar definir nenhuma variável de
ambiente.
"""

from __future__ import annotations

from .base import *  # noqa: F403 — reexporta as configurações compartilhadas

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Emails (ex.: confirmação de cadastro) só aparecem no console, sem SMTP real.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
