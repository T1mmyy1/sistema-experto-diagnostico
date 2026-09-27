"""
Casos de prueba del Sistema Experto de Diagnóstico Médico
============================================================
Ejecuta:
  - Parte 3: los 5 casos de prueba obligatorios.
  - Ejercicio 1: un caso por cada enfermedad nueva.
  - Ejercicio 2: análisis de conflicto de reglas (varias reglas activadas
    a la vez).
"""

from sistema_experto import SistemaExpertoMedico, Sintoma


def encabezado(texto):
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)


def ejecutar_caso(titulo, sintomas: dict):
    """
    Crea una nueva instancia del motor, la reinicia, declara los síntomas
    recibidos como diccionario {nombre_sintoma: True} y ejecuta el motor.
    """
    print(f"\n--- {titulo} ---")
    print(f"Síntomas declarados: {list(sintomas.keys())}")
    motor = SistemaExpertoMedico()
    motor.reset()
    motor.declare(Sintoma(**sintomas))
    motor.run()
    return motor


# ---------------------------------------------------------------------------
# Parte 3: casos de prueba obligatorios
# ---------------------------------------------------------------------------

encabezado("PARTE 3: CASOS DE PRUEBA")

# Caso 1: fiebre, tos y dolor de garganta -> Gripe
ejecutar_caso("Caso 1", {
    "fiebre": True,
    "tos": True,
    "dolor_garganta": True,
})

# Caso 2: estornudos, congestión nasal y picazón en los ojos -> Alergia
ejecutar_caso("Caso 2", {
    "estornudos": True,
    "congestion_nasal": True,
    "picazon_ojos": True,
})

# Caso 3: dolor de estómago, diarrea y vómitos -> Gastroenteritis
ejecutar_caso("Caso 3", {
    "dolor_estomago": True,
    "diarrea": True,
    "vomito": True,
})

# Caso 4: cansancio y mareo -> no coincide con ninguna regla
ejecutar_caso("Caso 4", {
    "cansancio": True,
    "mareo": True,
})

# Caso 5: fiebre, tos, dolor de garganta, estornudos y congestión nasal
# -> activa Gripe Y Alergia al mismo tiempo (caso de conflicto)
ejecutar_caso("Caso 5", {
    "fiebre": True,
    "tos": True,
    "dolor_garganta": True,
    "estornudos": True,
    "congestion_nasal": True,
})


# ---------------------------------------------------------------------------
# Ejercicio 1: un caso de prueba por cada enfermedad nueva
# ---------------------------------------------------------------------------

encabezado("EJERCICIO 1: ENFERMEDADES NUEVAS")

ejecutar_caso("COVID-19", {
    "fiebre": True,
    "tos_seca": True,
    "perdida_olfato": True,
})

ejecutar_caso("Resfriado común", {
    "congestion_nasal": True,
    "estornudos": True,
    "tos_leve": True,
})

ejecutar_caso("Bronquitis", {
    "tos_persistente": True,
    "produccion_flema": True,
    "dificultad_respiratoria": True,
})

ejecutar_caso("Anemia (enfermedad elegida)", {
    "fatiga": True,
    "palidez": True,
    "mareo": True,
})


# ---------------------------------------------------------------------------
# Ejercicio 2: análisis de conflicto de reglas
# ---------------------------------------------------------------------------

encabezado("EJERCICIO 2: CONFLICTO DE REGLAS (Gripe + Alergia)")

motor_conflicto = ejecutar_caso("Síntomas de Gripe + Alergia a la vez", {
    "fiebre": True,
    "tos": True,
    "dolor_garganta": True,
    "estornudos": True,
    "congestion_nasal": True,
    "picazon_ojos": True,
})

diagnosticos = [
    hecho["enfermedad"]
    for hecho in motor_conflicto.facts.values()
    if hecho.__class__.__name__ == "Diagnostico"
]
print(f"\nDiagnósticos generados en total: {len(diagnosticos)} -> {diagnosticos}")
print("(Ver reflexion.md para el análisis completo de este ejercicio)")
