"""Formulário de comentário em receita (spec 005)."""

from __future__ import annotations

from django import forms

from .models import Comentario


class FormularioComentario(forms.ModelForm):
    """Comentário de uma linha só: o texto.

    ``receita`` e ``autor`` são preenchidos pela view a partir da URL e do
    usuário autenticado — não fazem parte do formulário.
    """

    class Meta:
        model = Comentario
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Deixe seu comentário..."}
            ),
        }
        labels = {"texto": "Comentário"}

    def clean_texto(self) -> str:
        """Rejeita comentário vazio ou só com espaços em branco (RF-05).

        ``TextField`` sem ``blank=False`` já rejeita string vazia, mas uma
        string só de espaços passa pela validação padrão do Django (é
        "verdadeira") — daí o `.strip()` explícito aqui.

        Returns:
            str: o texto já sem espaços nas pontas.

        Raises:
            django.core.exceptions.ValidationError: se o texto, após
                `.strip()`, ficar vazio.
        """
        texto = self.cleaned_data["texto"].strip()
        if not texto:
            raise forms.ValidationError("O comentário não pode ficar vazio.")
        return texto
