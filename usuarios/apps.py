from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """
    Configuração da aplicação ``usuarios``.

    Registra a aplicação no Django e define seu nome canônico para uso em
    ``INSTALLED_APPS`` e na resolução de modelos.

    Attributes:
        name (str): Caminho Python da aplicação — ``"usuarios"``.
    """

    name = "usuarios"
