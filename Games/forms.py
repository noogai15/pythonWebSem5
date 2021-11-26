from django import forms

from .models import Comment, Game


class GameForms(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "name",
            "desc",
            "genre",
            "age_rating",
            "creator",
            "created_at",
            "price",
            "image",
        ]
        widgets = {
            "type": forms.Select(choices=Game.GENRES),
            "user": forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "star_rating"]
        widgets = {
            "user": forms.HiddenInput(),
            "game": forms.HiddenInput(),
        }
