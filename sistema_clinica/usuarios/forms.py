from django import forms

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
