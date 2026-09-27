# Reflexión y análisis

## Ejercicio 2: Análisis de conflicto de reglas

Para forzar un conflicto real se declararon los síntomas de Gripe y Alergia
al mismo tiempo:

```
fiebre, tos, dolor_garganta, estornudos, congestion_nasal, picazon_ojos
```

Esto cumple simultáneamente las condiciones de la regla `diagnostico_gripe`
y de la regla `diagnostico_alergia`. Resultado obtenido al ejecutar
`casos_prueba.py`:

```
Diagnóstico: Alergia
Recomendación: Evitar el alérgeno sospechoso...

Diagnóstico: Gripe
Recomendación: Reposo, hidratación abundante...

Diagnósticos generados en total: 2 -> ['Alergia', 'Gripe']
```

**Observaciones:**

- **Cuántos diagnósticos se generan:** dos — se declaran ambos hechos
  `Diagnostico` (Alergia y Gripe) en la memoria de trabajo.
- **Orden de ejecución:** se ejecutó primero `diagnostico_alergia` y después
  `diagnostico_gripe`.
- **¿Depende del orden de definición en la clase?** No directamente. En el
  código, la regla de Gripe está definida *antes* que la de Alergia, y sin
  embargo Alergia se disparó primero. Esto se debe a que `experta` (como la
  mayoría de motores basados en el algoritmo RETE/agenda) no ejecuta las
  reglas en el orden en que fueron escritas, sino según el orden en que sus
  activaciones entran a la agenda de conflicto, que a su vez depende del
  orden en que se declaran los hechos (`Sintoma`) y de cómo cada patrón de
  regla los va emparejando. Si se quisiera un orden garantizado, habría que
  usar el parámetro `salience` de `@Rule(...)` para asignar prioridades
  explícitas.

## Preguntas de reflexión

**1. ¿Qué limitaciones observaste en este enfoque durante la práctica?**

- Las reglas están escritas como combinaciones exactas de síntomas (todos
  con valor `True`); el sistema no maneja bien casos parciales, como un
  paciente con solo dos de los tres síntomas de una enfermedad, aunque sea
  clínicamente sugestivo.
- Varias enfermedades comparten síntomas (por ejemplo, congestión nasal
  aparece en Alergia y en Resfriado común), lo que hace que agregar nuevas
  reglas aumente el riesgo de conflictos o falsos positivos si no se es
  cuidadoso al definir las condiciones.
- El sistema no pondera la gravedad ni la probabilidad de cada enfermedad;
  todos los diagnósticos que coinciden se reportan por igual, sin indicar
  cuál es más probable.
- Es un modelo estrictamente booleano (síntoma presente / ausente); no
  contempla intensidad, duración ni interacción entre síntomas.

**2. ¿Cómo podría manejarse la incertidumbre en los síntomas (por ejemplo, un síntoma presente solo parcialmente)?**

Algunas opciones:

- Usar **factores de certeza** (como en sistemas expertos clásicos tipo
  MYCIN): en vez de `Sintoma(fiebre=True)`, declarar algo como
  `Sintoma(fiebre=0.6)` (un valor entre 0 y 1) y que las reglas acumulen o
  combinen esos factores para decidir si el diagnóstico se declara y con
  qué nivel de confianza.
- Aplicar **lógica difusa (fuzzy logic)**, definiendo grados de pertenencia
  para conceptos como "fiebre leve", "fiebre alta", en lugar de un valor
  booleano.
- Usar un enfoque **probabilístico** (por ejemplo, una red bayesiana) que
  calcule la probabilidad de cada enfermedad dado el conjunto de síntomas
  observados, incluso si son parciales o inciertos.
- A nivel más simple, permitir reglas con umbrales ("al menos 2 de 3
  síntomas") en vez de exigir todos los síntomas de forma estricta.

**3. En el Ejercicio 2, ¿qué implicaciones tiene para un sistema experto real que se activen varias reglas a la vez?**

Que varias reglas se activen a la vez refleja una situación real: un
paciente puede tener más de una condición simultáneamente, o presentar
síntomas ambiguos que son compatibles con varios diagnósticos. Para un
sistema experto real esto implica que:

- No basta con mostrar todos los diagnósticos activados como si tuvieran el
  mismo peso; se necesitaría un mecanismo de **resolución de conflictos**
  más sofisticado que el orden implícito del motor (por ejemplo, `salience`,
  especificidad de la regla, o un puntaje de confianza) para decidir cuál
  mostrar primero o si mostrar varios diagnósticos diferenciales.
- El orden de ejecución no debe depender de detalles internos del motor
  (como en este caso, donde no fue el orden de escritura del código); un
  sistema real necesita que ese orden sea explícito y auditable, sobre todo
  en un dominio médico donde las decisions tienen consecuencias reales.
- Sistemas expertos usados en contextos críticos (medicina, diagnóstico
  industrial, etc.) normalmente presentan un **diagnóstico diferencial**
  (una lista ordenada de posibles causas) en vez de un único resultado,
  precisamente para reflejar esta ambigüedad en lugar de ocultarla.
