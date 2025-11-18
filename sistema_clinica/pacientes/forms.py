from django import forms
from django.core.validators import RegexValidator

class PacienteCustomForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$',
                message="El nombre solo puede contener letras y espacios."
            )
        ]
    )

    apellido = forms.CharField(
        label="Apellido",
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$',
                message="El apellido solo puede contener letras y espacios."
            )
        ]
    )
    dni = forms.CharField(
        label="DNI",
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{1,8}$',
                message="El DNI debe tener hasta 8 dígitos numéricos."
            )
        ]
    )
    email = forms.EmailField(label="Email")
    telefono = forms.CharField(
        label="Teléfono",
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{1,10}$',
                message="El teléfono debe tener hasta 10 dígitos numéricos."
            )
        ]
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    dni = forms.CharField(
        label="DNI",
        max_length=10,
        required=True
    )