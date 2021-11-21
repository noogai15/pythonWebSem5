from django.contrib.auth.models import User
from django import forms


class MySignUpForm(forms.ModelForm):
    # Fields zusaetzlich zum User-Model
    date_of_birth = forms.DateField()
    profile_picture = forms.ImageField()

    class Meta:
        model = User
        fields = ('username','first_name','last_name','password','email')
        widgets = {
            'password': forms.PasswordInput(),
        }