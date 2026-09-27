"""
Sistema Experto de Diagnóstico Médico Simple
==============================================
Práctica de Sistemas Expertos - Motor de inferencia hacia adelante (forward chaining)
usando la librería `experta`.
"""

# --- Parche de compatibilidad ---
# `experta` (y su dependencia frozendict) usan `collections.Mapping`, que en
# Python 3.10+ se movió a `collections.abc.Mapping`. Este parche restaura los
# alias necesarios antes de importar la librería, sin tocar su código fuente.
import collections
import collections.abc
for _name in ("Mapping", "MutableMapping", "Sequence"):
    if not hasattr(collections, _name):
        setattr(collections, _name, getattr(collections.abc, _name))

from experta import Fact, Field, KnowledgeEngine, Rule, NOT


# ---------------------------------------------------------------------------
# Parte 1: Definición de hechos
# ---------------------------------------------------------------------------

class Sintoma(Fact):
    """
    Representa un síntoma presente (o ausente) en el paciente.
    Se instancia con atributos booleanos con nombre, por ejemplo:
        Sintoma(fiebre=True)
        Sintoma(tos=True)
    Cada síntoma se declara como un hecho independiente en la memoria de
    trabajo, lo que permite que las reglas verifiquen combinaciones de
    varios hechos de este tipo a la vez.
    """
    pass


class Diagnostico(Fact):
    """
    Representa el diagnóstico generado por el motor de inferencia.
    Almacena el nombre de la enfermedad identificada, por ejemplo:
        Diagnostico(enfermedad="Gripe")
    Al declararse, funciona también como bandera para que la regla de
    respaldo sepa que ya se encontró un diagnóstico y no deba activarse.
    """
    pass


# ---------------------------------------------------------------------------
# Parte 2: Construcción del sistema experto
# ---------------------------------------------------------------------------

class SistemaExpertoMedico(KnowledgeEngine):
    """
    Motor de inferencia para diagnóstico médico simple.
    Cada regla verifica una combinación de síntomas, declara el diagnóstico
    correspondiente y muestra una recomendación asociada.
    """

    @Rule(
        Sintoma(fiebre=True),
        Sintoma(tos=True),
        Sintoma(dolor_garganta=True),
    )
    def diagnostico_gripe(self):
        self.declare(Diagnostico(enfermedad="Gripe"))
        print("Diagnóstico: Gripe")
        print("Recomendación: Reposo, hidratación abundante y control de la "
              "fiebre. Consultar a un médico si los síntomas empeoran o "
              "duran más de una semana.")

    @Rule(
        Sintoma(fiebre=True),
        Sintoma(dolor_cabeza=True),
        Sintoma(nauseas=True),
    )
    def diagnostico_migrana(self):
        self.declare(Diagnostico(enfermedad="Migraña"))
        print("Diagnóstico: Migraña")
        print("Recomendación: Descansar en un lugar oscuro y silencioso, "
              "evitar pantallas y consultar a un médico si el dolor es "
              "muy intenso o recurrente.")

    @Rule(
        Sintoma(estornudos=True),
        Sintoma(congestion_nasal=True),
        Sintoma(picazon_ojos=True),
    )
    def diagnostico_alergia(self):
        self.declare(Diagnostico(enfermedad="Alergia"))
        print("Diagnóstico: Alergia")
        print("Recomendación: Evitar el alérgeno sospechoso, considerar un "
              "antihistamínico y consultar a un médico si los síntomas "
              "persisten.")

    @Rule(
        Sintoma(dolor_estomago=True),
        Sintoma(diarrea=True),
        Sintoma(vomito=True),
    )
    def diagnostico_gastroenteritis(self):
        self.declare(Diagnostico(enfermedad="Gastroenteritis"))
        print("Diagnóstico: Gastroenteritis")
        print("Recomendación: Mantener hidratación con suero oral, dieta "
              "blanda y acudir al médico si hay signos de deshidratación "
              "o fiebre alta.")

    # -----------------------------------------------------------------
    # Ejercicio 1: reglas nuevas (misma estructura que las anteriores)
    # -----------------------------------------------------------------

    @Rule(
        Sintoma(fiebre=True),
        Sintoma(tos_seca=True),
        Sintoma(perdida_olfato=True),
    )
    def diagnostico_covid19(self):
        self.declare(Diagnostico(enfermedad="COVID-19"))
        print("Diagnóstico: COVID-19")
        print("Recomendación: Aislarse, realizar una prueba de detección y "
              "contactar a un médico para dar seguimiento a los síntomas.")

    @Rule(
        Sintoma(congestion_nasal=True),
        Sintoma(estornudos=True),
        Sintoma(tos_leve=True),
    )
    def diagnostico_resfriado_comun(self):
        self.declare(Diagnostico(enfermedad="Resfriado común"))
        print("Diagnóstico: Resfriado común")
        print("Recomendación: Descanso, líquidos abundantes y, si es "
              "necesario, un descongestionante. Suele resolverse en pocos "
              "días.")

    @Rule(
        Sintoma(tos_persistente=True),
        Sintoma(produccion_flema=True),
        Sintoma(dificultad_respiratoria=True),
    )
    def diagnostico_bronquitis(self):
        self.declare(Diagnostico(enfermedad="Bronquitis"))
        print("Diagnóstico: Bronquitis")
        print("Recomendación: Reposo, evitar irritantes como el humo y "
              "acudir al médico si la dificultad respiratoria empeora.")

    @Rule(
        Sintoma(fatiga=True),
        Sintoma(palidez=True),
        Sintoma(mareo=True),
    )
    def diagnostico_anemia(self):
        self.declare(Diagnostico(enfermedad="Anemia (sospecha)"))
        print("Diagnóstico: Anemia (sospecha)")
        print("Recomendación: Acudir con un médico para un análisis de "
              "sangre; no autodiagnosticarse ni automedicarse con hierro "
              "sin confirmación clínica.")

    # -----------------------------------------------------------------
    # Regla de respaldo (debe evaluarse después de todas las anteriores)
    # -----------------------------------------------------------------

    @Rule(NOT(Diagnostico()))
    def sin_diagnostico(self):
        print("Diagnóstico: No determinado")
        print("Recomendación: No se encontró una coincidencia con los "
              "síntomas registrados. Se recomienda consultar a un médico "
              "para una evaluación adecuada.")


if __name__ == "__main__":
    # Prueba rápida de humo: caso de gripe
    motor = SistemaExpertoMedico()
    motor.reset()
    motor.declare(Sintoma(fiebre=True))
    motor.declare(Sintoma(tos=True))
    motor.declare(Sintoma(dolor_garganta=True))
    motor.run()
