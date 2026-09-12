"""
Ponto de entrada ASGI do projeto Blog Culinário.

Expõe o callable ASGI na variável de módulo ``application``, utilizada por
servidores compatíveis com ASGI. Não usado no deploy atual (PythonAnywhere
roda WSGI, ver ``wsgi.py``) — mantido pelo scaffold padrão do Django para o
projeto poder migrar para um servidor ASGI sem retrabalho.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_culinario.settings.dev")

application = get_asgi_application()
