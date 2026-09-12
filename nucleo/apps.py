from django.apps import AppConfig


class NucleoConfig(AppConfig):
    """
    Configuração da aplicação ``nucleo``.

    Registra a aplicação no Django e define seu nome canônico para uso em
    ``INSTALLED_APPS`` e na resolução de modelos.

    Attributes:
        name (str): Caminho Python da aplicação — ``"nucleo"``.
    """

    name = "nucleo"
