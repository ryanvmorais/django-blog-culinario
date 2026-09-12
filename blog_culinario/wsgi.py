"""
Ponto de entrada WSGI do projeto Blog Culinário.

Expõe o callable WSGI na variável de módulo ``application``, utilizada por
servidores compatíveis com WSGI para servir a aplicação de forma síncrona —
o modelo de deploy do PythonAnywhere (ver ``settings/prod.py``).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_culinario.settings.dev")

application = get_wsgi_application()
