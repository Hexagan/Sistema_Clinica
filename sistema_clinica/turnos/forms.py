from django import forms
from .models import Turno

class SolicitarTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['paciente', 'profesional', 'servicio', 'fecha', 'hora', 'piso', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
