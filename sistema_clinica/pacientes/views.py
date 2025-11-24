import os
import calendar
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paciente, Mensaje, Estudio
from profesionales.models import Especialidad, Profesional
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import activate

def cargar_paciente(request, paciente_id):
    perfil = request.user.perfil
    return perfil.pacientes.get(pk=paciente_id)

@login_required
def portal_paciente(request, paciente_id):
    usuario = request.user
    perfil = usuario.perfil

    paciente_seleccionado = perfil.pacientes.get(pk=paciente_id)

    request.session["paciente_id"] = paciente_id

    return render(request, "portal_paciente.html", {
        "usuario": usuario,
        "pacientes": perfil.pacientes.all(),
        "paciente_seleccionado": paciente_seleccionado,
        "paciente": paciente_seleccionado,
        "especialidades": Especialidad.objects.all(),
        "profesionales": Profesional.objects.all(),
        "paciente_id": paciente_id,
    })

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        obra_social = request.POST.get('obra_social')
        
        # Validación DNI duplicado
        if Paciente.objects.filter(dni=dni).exists():
            error = "Ya existe un paciente con ese DNI."
            return render(request, "pacientes/crear_paciente.html", {"error": error})

        # Crear el paciente con la FK correcta
        nuevo_paciente = Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            obra_social=obra_social,
            perfil_usuario=request.user.perfil   # ← FK obligatoria
        )
        
        # Asociarlo también al M2M
        request.user.perfil.pacientes.add(nuevo_paciente)

        return redirect('pacientes:creacion_paciente_exitosa')

    # GET → mostrar formulario
    return render(request, 'pacientes/crear_paciente.html')



@login_required
def creacion_paciente_exitosa(request):
    return render(request, 'pacientes/creacion_paciente_exitosa.html')


@login_required
def paciente_detalle(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'pacientes/paciente_detalle.html', {'paciente': paciente})


@login_required
def ver_turnos(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    turnos = paciente.turno_set.all()
    return render(request, "turnos/ver_turnos.html", {
        "paciente": paciente,
        "turnos": turnos
    })

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by("apellido", "nombre")
    return render(request, "pacientes/lista_pacientes.html", {
        "pacientes": pacientes
    })

def cambiar_paciente(request, paciente_id):
    return redirect("usuarios:portal_paciente", paciente_id=paciente_id)

@login_required
def buscar_turnos(request):
    especialidades = Especialidad.objects.all()
    profesionales = Profesional.objects.all()

    return render(request, "buscar_turnos.html", {
        "especialidades": especialidades,
        "profesionales": profesionales,
    })


"""@login_required
def resultados_turnos(request):
    especialidad_id = request.GET.get("especialidad")
    profesional_id = request.GET.get("profesional")
    tipo = request.GET.get("tipo")
    fecha = request.GET.get("fecha")

    profesionales = Profesional.objects.filter(especialidad_id=especialidad_id)

    if profesional_id:
        profesionales = profesionales.filter(id=profesional_id)

    if tipo != "AMBOS":
        profesionales = profesionales.filter(tipo_consulta=tipo)

    resultados = []

    for prof in profesionales:
        horarios_disponibles = obtener_disponibilidad(prof, fecha)
        for h in horarios_disponibles:
            resultados.append({
                "fecha": fecha,
                "hora": h,
                "profesional": prof,
                "especialidad": prof.especialidad,
                "tipo": prof.tipo_consulta
            })

    return render(request, "lista_turnos.html", {"resultados": resultados}) """

def indicaciones(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/indicaciones.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })


def peso_altura(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/peso_altura.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def temperatura(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/temperatura.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def frecuencia_cardiaca(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/frecuencia_cardiaca.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def presion_arterial(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/presion_arterial.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def glucemia(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/glucemia.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def frecuencia_respiratoria(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/frecuencia_respiratoria.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def saturacion_oxigeno(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/saturacion_oxigeno.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def disnea(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "pacientes/disnea.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

@login_required
def mensajeria(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)

    mensajes = Mensaje.objects.filter(
        remitente=request.user
    ).order_by('-creado')

    return render(request, "pacientes/mensajeria.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "mensajes": mensajes,
    })

@login_required
def nuevo_mensaje(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    profesionales = Profesional.objects.filter(estado=True).order_by("nombre")

    if request.method == "POST":
        profesional_id = request.POST.get("profesional")
        texto = request.POST.get("texto", "").strip()

        if profesional_id and texto:
            prof = get_object_or_404(Profesional, id=profesional_id)

            Mensaje.objects.create(
                remitente=request.user,
                profesional_destino=prof,
                texto=texto,
            )

            return redirect("pacientes:mensajeria", paciente_id=paciente_id)

    return render(request, "pacientes/nuevo_mensaje.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "profesionales": profesionales,
    })

@login_required
def estudios(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    lista_estudios = Estudio.objects.filter(
        paciente_id=paciente_id
    ).order_by("-fecha_estudio", "-creado")

    return render(request, "pacientes/estudios.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "estudios": lista_estudios,
    })


@login_required
def cargar_estudio(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)

    if request.method == "POST":
        fecha = request.POST.get("fecha_estudio")
        obs = request.POST.get("observaciones", "")
        archivo = request.FILES.get("archivo")

        # Validación: fecha obligatoria
        if not fecha:
            messages.error(request, "Debe indicar la fecha del estudio.")
            return redirect("pacientes:cargar_estudio", paciente_id=paciente_id)

        # Validación: archivo obligatorio
        if not archivo:
            messages.error(request, "Debe seleccionar un archivo antes de subir.")
            return redirect("pacientes:cargar_estudio", paciente_id=paciente_id)

        # Validación: extensión permitida
        ext = os.path.splitext(archivo.name)[1].lower()
        extensiones_validas = [".pdf", ".jpg", ".jpeg", ".png"]
        if ext not in extensiones_validas:
            messages.error(request, "Solo se permiten archivos PDF o imágenes.")
            return redirect("pacientes:cargar_estudio", paciente_id=paciente_id)

        # Guardar estudio
        Estudio.objects.create(
            paciente=paciente,
            fecha_estudio=fecha,
            observaciones=obs,
            archivo=archivo
        )

        messages.success(request, "Estudio cargado correctamente.")
        return redirect("pacientes:estudios", paciente_id=paciente_id)

    return render(request, "pacientes/cargar_estudio.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

def medicamentos(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)

    recetas = []  # cuando agregues modelo real

    return render(request, "pacientes/medicamentos.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "recetas": recetas,
    })

def mis_medicos(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)

    profesionales = Profesional.objects.filter(estado=True).order_by("nombre")

    return render(request, "pacientes/mis_medicos.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "profesionales": profesionales,
    })

def teleconsultas(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)

    return render(request, "pacientes/teleconsultas.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })


def cartilla(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    query = request.GET.get("q", "")
    especialidad = request.GET.get("especialidad", "")

    profesionales = Profesional.objects.all()

    if query:
        profesionales = profesionales.filter(
            Q(nombre__icontains=query) | Q(email__icontains=query)
        )

    if especialidad:
        profesionales = profesionales.filter(
            especialidad__nombre__icontains=especialidad
        )

    return render(request, "pacientes/cartilla.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "profesionales": profesionales,
        "q": query,
        "especialidad": especialidad,
    })

def consultas_gestiones(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)

    if request.method == "POST":
        # Crear ticket más adelante
        return redirect("pacientes:consultas_gestiones", paciente_id=paciente_id)

    return render(request, "pacientes/consultas_gestiones.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
    })

@login_required
def mensaje_detalle(request, paciente_id, mensaje_id):
    paciente = cargar_paciente(request, paciente_id)
    mensaje = get_object_or_404(Mensaje, id=mensaje_id, remitente=request.user)

    # Marcar como leído si aún no lo está
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()

    return render(request, "pacientes/mensaje_detalle.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "mensaje": mensaje,
    })



def mi_diario(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    # Activar español 
    activate('es')

    estudios = Estudio.objects.filter(paciente=paciente)

    # Obtener parámetro del radio button
    ordenar = request.GET.get("ordenar", "fecha")

    if ordenar == "descripcion":
        estudios = estudios.order_by("descripcion")
    else:
        estudios = estudios.order_by("-fecha_estudio")

    # Agrupado por fecha (solo para visualización)
    grupos = {}
    for doc in estudios:
        mes_ano = doc.fecha_estudio.strftime("%B %Y")  # ej: "diciembre 2023"
        mes_ano = mes_ano.capitalize() 
        grupos.setdefault(mes_ano, []).append(doc)

    context = {
        "ordenar": ordenar,
        "grupos": grupos,
        "paciente": paciente,
        "paciente_id": paciente_id,
    }
    
    return render(request, "pacientes/mi_diario.html", context)