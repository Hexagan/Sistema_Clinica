from django import forms
from django.contrib.auth.models import User

class PacienteCustomForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    dni = forms.CharField(label="DNI", max_length=20)
    email = forms.EmailField(label="Email")
    telefono = forms.CharField(label="Teléfono", max_length=30)
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date"})
    )
    obra_social = forms.CharField(
        label="Obra social",
        required=False,
        max_length=100
    )

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