from django import forms
from .models import Publicacion, Bicycle, BicycleImage

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'descripcion', 'estado', 'precio']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la publicación'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe el estado de la bicicleta'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en USD'}),
        }


class BicycleForm(forms.ModelForm):
    class Meta:
        model = Bicycle
        fields = ['titulo', 'descripcion', 'color', 'rodado', 'estado', 'precio']

class BicycleImageForm(forms.ModelForm):
    class Meta:
        model = BicycleImage
        fields = ['image']
        
