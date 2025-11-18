from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator

class RegistroCustomForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nombre de usuario"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su contraseña"
        })
    )

    password_confirm = forms.CharField(
        label="Repetir contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Repita su contraseña"
        })
    )


    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ese nombre de usuario ya existe.")
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        password_confirm = cleaned.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden.")

        return cleaned
    
class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))