from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import MyUser


class MySignUpForm(UserCreationForm):
    # Fields zusaetzlich zum User-Model
    date_of_birth = forms.DateField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = MyUser
        fields = ('username','first_name','last_name','email')
