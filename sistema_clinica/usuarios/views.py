from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente
from .forms import RegistroCustomForm, LoginForm
from .models import PerfilUsuario

# -----------------------------
# REGISTRO DE USUARIO
# -----------------------------

def login_usuario(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("usuarios:perfil")
    return render(request, "usuarios/login.html", {"form": form})

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroCustomForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Crear usuario
            usuario = User.objects.create_user(
                username=username,
                password=password
            )

            PerfilUsuario.objects.create(usuario=usuario)

            login(request, usuario)
            return redirect("usuarios:perfil")

    else:
        form = RegistroCustomForm()

    return render(request, "usuarios/registrar_custom.html", {"form": form})



# -----------------------------
# USUARIO
# -----------------------------
@login_required
def portal_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Seguridad: asegurar que ese paciente pertenece al usuario
    if paciente not in request.user.perfil.pacientes.all():
        return render(request, "usuarios/acceso_denegado.html")

    return render(request, "pacientes/portal_paciente.html", {
        "usuario": request.user,
        "paciente": paciente
    })

@login_required
def perfil_usuario(request):
    perfil = request.user.perfil
    pacientes = perfil.pacientes.all()  
    
    return render(request, "usuarios/perfil.html", {
        "usuario": request.user,
        "perfil": perfil,
        "pacientes": pacientes,
    })



# -----------------------------
# PACIENTE
# -----------------------------
@login_required
def detalle_paciente_usuario(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if paciente not in request.user.perfil.pacientes.all():
        return render(request, "usuarios/acceso_denegado.html")

    return render(request, "pacientes/paciente_detalle.html", {"paciente": paciente})