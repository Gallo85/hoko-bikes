from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'telefono', 'direccion') 
        help_texts = {
            'username': "El nombre de usuario debe tener entre 4 y 20 caracteres. Solo letras, números y @/./+/-/_",
            'password 1': "La contraseña debe tener al menos 8 caracteres, incluir letras y números.",
            'password 2': "Confirma la contraseña ingresada.",
        }


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'direccion']
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'direccion': forms.Textarea(attrs={'placeholder': 'Dirección', 'rows': 3}),

   }