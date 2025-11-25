from pacientes.models import Paciente
from profesionales.models import Profesional
from pacientes.models import Receta


def run():
    # ===================================
    # CONFIGURACIÓN RÁPIDA Y EDITABLE
    # ===================================
    PACIENTE_ID = 11     
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
    prof_aguirre = get_prof("Aguirre")
    prof_torres = get_prof("Torres")
    prof_silva = get_prof("Silva")
    prof_aguilar = get_prof("Aguilar")
    prof_angelo = get_prof("D'Angelo")

    if not (prof_martinez and prof_gomez and prof_aguirre, prof_torres, prof_silva, prof_aguilar, prof_angelo):
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
            "profesional": prof_aguirre,
        },
        {
            "nombre": "Paracetamol 1 g",
            "dosis": "1 comprimido",
            "frecuencia": "Cada 8 horas según dolor",
            "descripcion": "No exceder 3 g al día.",
            "profesional": prof_torres,
        },
        {
            "nombre": "Metformina 850 mg",
            "dosis": "1 comprimido",
            "frecuencia": "Dos veces al día",
            "descripcion": "Tomar con desayuno y cena. Controlar niveles de glucemia.",
            "profesional": prof_silva,
        },
        {
            "nombre": "Losartán 50 mg",
            "dosis": "1 tableta",
            "frecuencia": "Una vez al día",
            "descripcion": "Mantener horario fijo. Usar junto con control periódico de tensión.",
            "profesional": prof_aguilar,
        },
        {
            "nombre": "Omeprazol 20 mg",
            "dosis": "1 cápsula",
            "frecuencia": "Una vez por la mañana",
            "descripcion": "Tomar en ayunas. No usar más de 14 días sin supervisión médica.",
            "profesional": prof_angelo,
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
