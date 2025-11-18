from django import forms
from profesionales.models import Profesional
from servicios.models import Servicio

class SolicitarTurnoForm(forms.Form):
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),
        label="Profesional"
    )
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        label="Servicio"
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha"
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Hora"
    )
    observaciones = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Observaciones"
    )