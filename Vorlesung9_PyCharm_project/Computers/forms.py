from django import forms
from .models import Computer


class ComputerForm(forms.ModelForm):

    class Meta:
        model = Computer
        fields = ['brand', 'type', 'operating_system', 'memory', 'serial_number']
        widgets = {
            'brand': forms.Select(choices=Computer.BRANDS),
            'type': forms.Select(choices=Computer.TYPES),
            'operating_system': forms.Select(choices=Computer.OPERATING_SYSTEMS),
            'myuser': forms.HiddenInput(),
        }
