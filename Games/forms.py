from django import forms
from .models import Game


class GameForms(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["name", "desc", "genre", "age_rating", "creator", "created_at"]
        widgets = {
            "type": forms.Select(choices=Game.GENRES),
            "user": forms.HiddenInput(),
        }
