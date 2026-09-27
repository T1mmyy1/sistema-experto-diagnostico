# Sistema Experto de Diagnóstico Médico Simple

Práctica de Sistemas Expertos: implementación de un motor de inferencia hacia
adelante (*forward chaining*) usando la librería [`experta`](https://github.com/nilp0inter/experta),
un fork mantenido de `pyknow`.

## Descripción

El sistema recibe un conjunto de síntomas del paciente (declarados como
hechos `Sintoma`) y, mediante un conjunto de reglas `SI-ENTONCES`, determina
un diagnóstico probable (`Diagnostico`) junto con una recomendación. Si
ninguna regla coincide, una regla de respaldo indica que no se pudo
determinar un diagnóstico.

Enfermedades cubiertas:

| Enfermedad | Síntomas requeridos |
|---|---|
| Gripe | fiebre, tos, dolor de garganta |
| Migraña | fiebre, dolor de cabeza, náuseas |
| Alergia | estornudos, congestión nasal, picazón en los ojos |
| Gastroenteritis | dolor de estómago, diarrea, vómitos |
| COVID-19 | fiebre, tos seca, pérdida de olfato |
| Resfriado común | congestión nasal, estornudos, tos leve |
| Bronquitis | tos persistente, producción de flema, dificultad respiratoria |
| Anemia (sospecha) | fatiga, palidez, mareo |

## Estructura del proyecto

```
.
├── sistema_experto.py   # Hechos (Sintoma, Diagnostico) y motor de reglas
├── casos_prueba.py      # Ejecuta Parte 3, Ejercicio 1 y Ejercicio 2
├── reflexion.md          # Respuestas a las preguntas de reflexión
└── README.md
```

## Requisitos

- Python 3.x
- Librería `experta`

```bash
pip install experta
```

> **Nota de compatibilidad:** `experta` (y su dependencia `frozendict`) usan
> `collections.Mapping`, que en Python 3.10+ fue removido de `collections` y
> ahora vive en `collections.abc`. `sistema_experto.py` incluye un pequeño
> parche al inicio del archivo que restaura esos alias antes de importar la
> librería, para que el proyecto funcione en versiones recientes de Python
> sin modificar el código fuente de `experta`.

## Ejecución

Correr el motor por sí solo (incluye una prueba de humo con un caso de
gripe):

```bash
python3 sistema_experto.py
```

Correr todos los casos de prueba (Parte 3), los casos del Ejercicio 1 y el
análisis de conflicto de reglas del Ejercicio 2:

```bash
python3 casos_prueba.py
```

## Ejemplo de uso

```python
from sistema_experto import SistemaExpertoMedico, Sintoma

motor = SistemaExpertoMedico()
motor.reset()
motor.declare(Sintoma(fiebre=True))
motor.declare(Sintoma(tos=True))
motor.declare(Sintoma(dolor_garganta=True))
motor.run()
# Diagnóstico: Gripe
# Recomendación: Reposo, hidratación abundante y control de la fiebre...
```
