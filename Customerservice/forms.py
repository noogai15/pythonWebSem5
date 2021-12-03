from django import forms
from Games.models import Comment, Game


class CS_CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "star_rating"]
        widgets = {
            "user": forms.HiddenInput(),
            "game": forms.HiddenInput(),
        }
