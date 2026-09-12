from django.apps import AppConfig


class ReceitasConfig(AppConfig):
    """
    Configuração da aplicação ``receitas``.

    Registra a aplicação no Django e define seu nome canônico para uso em
    ``INSTALLED_APPS`` e na resolução de modelos.

    Attributes:
        name (str): Caminho Python da aplicação — ``"receitas"``.
    """

    name = "receitas"
