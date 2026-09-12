"""
Views de autenticação: cadastro, login e logout (spec 004).

Login e logout reaproveitam ``LoginView``/``LogoutView`` do Django (RNF-01)
— só acrescentam a mensagem de feedback (ADR-3). Cadastro precisa de uma
view própria porque o Django não fornece uma pronta.
"""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import FormularioCadastro


class CadastroView(FormView):
    """Cria a conta e autentica o usuário automaticamente (ADR-1)."""

    template_name = "usuarios/cadastro.html"
    form_class = FormularioCadastro
    success_url = reverse_lazy("nucleo:home")

    def form_valid(self, form: FormularioCadastro) -> HttpResponse:
        """Salva o usuário, autentica a sessão e mostra a mensagem de boas-vindas.

        Args:
            form (FormularioCadastro): formulário já validado.

        Returns:
            HttpResponse: redireciona para ``success_url``.
        """
        usuario = form.save()
        login(self.request, usuario)
        messages.success(self.request, f"Bem-vindo(a), {usuario.username}!")
        return super().form_valid(form)


class EntrarView(LoginView):
    """Login nativo do Django, só com template e mensagem próprios."""

    template_name = "usuarios/login.html"

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        """Autentica via `LoginView` e acrescenta a mensagem de boas-vindas.

        Args:
            form (AuthenticationForm): formulário já validado pelo `LoginView`.

        Returns:
            HttpResponse: redireciona para `?next=` ou `LOGIN_REDIRECT_URL`.
        """
        resposta = super().form_valid(form)
        messages.success(
            self.request, f"Bem-vindo(a) de volta, {self.request.user.username}!"
        )
        return resposta


class SairView(LogoutView):
    """Logout nativo do Django — só aceita POST (ADR-2)."""

    # django-stubs tipa next_page como `str | None`; reverse_lazy() devolve um
    # proxy preguiçoso que só vira str quando avaliado — comportamento correto
    # em runtime, só a anotação do stub que é estrita demais aqui.
    next_page = reverse_lazy("nucleo:home")  # type: ignore[assignment]

    def post(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        """Registra a mensagem de despedida antes de encerrar a sessão.

        Args:
            request (HttpRequest): requisição POST recebida.
            *args (object): argumentos posicionais repassados ao `super().post()`.
            **kwargs (object): argumentos nomeados repassados ao `super().post()`.

        Returns:
            HttpResponse: redireciona para `next_page`.
        """
        messages.info(request, "Você saiu da sua conta.")
        return super().post(request, *args, **kwargs)
