from django import forms

from .models import Fact


class FactForm(forms.ModelForm):
    class Meta:
        model = Fact
        fields = ['fact']
        widgets = {
            'fact': forms.Textarea(attrs={
                'placeholder': 'Ingrese su hecho favorito'
            })
        }
        labels = {
            'fact': 'Hecho'
        }
