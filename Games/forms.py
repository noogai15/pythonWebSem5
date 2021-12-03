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


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "star_rating"]
        widgets = {
            "user": forms.HiddenInput(),
            "game": forms.HiddenInput(),
        }

class SearchForm(forms.ModelForm):

    desc = forms.CharField(required=False)
    average_stars = forms.IntegerField(required=False)
    name = forms.CharField(required=False)


    class Meta:
        model = Game
        # GET GAME FROM STAR_RATING
        fields = ['name', 'desc', 'average_stars']