from pacientes.models import Paciente
from profesionales.models import Profesional
from pacientes.models import Receta


def run():
    # ===================================
    # CONFIGURACIÓN RÁPIDA Y EDITABLE
    # ===================================
    PACIENTE_ID = 13     # ← Cambialo rápido para probar con otro paciente
    print(f"📌 Cargando recetas para paciente {PACIENTE_ID}...")

    # -----------------------------------
    # Obtener paciente
    # -----------------------------------
    try:
        paciente = Paciente.objects.get(pk=PACIENTE_ID)
    except Paciente.DoesNotExist:
        print("❌ Error: el paciente no existe.")
        return

    # -----------------------------------
    # Limpiar recetas previas (opcional)
    # -----------------------------------
    Receta.objects.filter(paciente=paciente).delete()

    # -----------------------------------
    # Buscar profesionales (de ejemplo)
    # Si no existen, el script te avisa
    # -----------------------------------
    def get_prof(nombre):
        try:
            return Profesional.objects.filter(nombre__icontains=nombre).first()
        except:
            return None

    prof_martinez = get_prof("Martínez")
    prof_gomez = get_prof("Gómez")
    prof_garcia = get_prof("García")

    if not (prof_martinez and prof_gomez and prof_garcia):
        print("⚠ Algunos profesionales no se encontraron. Creá profesionales ejemplo.")
    
    # -----------------------------------
    # Crear recetas
    # -----------------------------------
    recetas_data = [
        {
            "nombre": "Ibuprofeno 600 mg",
            "dosis": "1 comprimido",
            "frecuencia": "Cada 8 horas",
            "descripcion": "Tomar después de las comidas.",
            "profesional": prof_martinez,
        },
        {
            "nombre": "Amoxicilina 500 mg",
            "dosis": "1 cápsula",
            "frecuencia": "Cada 12 horas",
            "descripcion": "Completar el tratamiento por 7 días.",
            "profesional": prof_gomez,
        },
        {
            "nombre": "Enalapril 10 mg",
            "dosis": "1 tableta",
            "frecuencia": "Una vez por la mañana",
            "descripcion": "Control de presión arterial.",
            "profesional": prof_garcia,
        },
        {
            "nombre": "Paracetamol 1 g",
            "dosis": "1 comprimido",
            "frecuencia": "Cada 8 horas según dolor",
            "descripcion": "No exceder 3 g al día.",
            "profesional": prof_martinez,
        },
    ]

    # Crear objetos
    creadas = []
    for data in recetas_data:
        if not data["profesional"]:
            print(f"⚠ Profesional no encontrado para {data['nombre']}. Saltando…")
            continue

        receta = Receta.objects.create(
            paciente=paciente,
            profesional=data["profesional"],
            nombre=data["nombre"],
            dosis=data["dosis"],
            frecuencia=data["frecuencia"],
            descripcion=data["descripcion"],
            activa=True,
        )

        creadas.append(receta)

    print(f"✅ {len(creadas)} recetas cargadas correctamente.")
    for r in creadas:
        print(f"  - {r.nombre} ({r.profesional.nombre})")

    print("🎉 Seed completado.")
