from django.shortcuts import render, get_object_or_404
from .models import Profesional, Especialidad

def lista_profesionales(request):
    profesionales = Profesional.objects.select_related('especialidad').all()
    return render(request, 'profesionales/lista_profesionales.html', {
        'profesionales': profesionales
    })


def detalle_profesional(request, profesional_id):
    profesional = get_object_or_404(
        Profesional.objects.select_related('especialidad').prefetch_related('servicios'),
        id=profesional_id
    )
    return render(request, 'profesionales/detalle_profesional.html', {
        'profesional': profesional
    })


def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'profesionales/lista_especialidades.html', {
        'especialidades': especialidades
    })
