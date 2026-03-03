# Practica - Unidad 3, Sesión 2
## Acceso Programático a LLMs

---

## Información General

| Campo | Valor |
|-------|-------|
| **Nombre del estudiante** | Guillermo Casaus |
| **Fecha** | 3 de marzo de 2026 |
| **Título** | Práctica Unidad 3 - Acceso Programático a LLMs |

---

## Nota sobre la configuración usada

Todos los ejercicios utilizan **OpenRouter** como alternativa gratuita. El cliente se
configura de la siguiente manera:

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
```

El modelo por defecto empleado en la mayoría de ejercicios es
`google/gemini-2.0-flash-exp:free`.

---

## Ejercicio 1: Primera Llamada a la API

**Fichero:** `ejercicio1_primera_llamada.py`

### Paso 2: Código completado

Los fragmentos `____` del esqueleto original se rellenan así:

```python
# Cliente
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Llamada
response = client.chat.completions.create(
    model="google/gemini-2.0-flash-exp:free",
    messages=[
        {"role": "user", "content": "¿Qué es el machine learning? Responde en 3 oraciones."}
    ],
    temperature=0.7
)

# Respuesta y metadatos
print("Respuesta:", response.choices[0].message.content)
print("Modelo:",    response.model)
print("Prompt tokens:",     response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens:",      response.usage.total_tokens)
```

### Paso 3: Experimentación con temperature

Se ejecuta la misma llamada el mismo número de veces (x2 por temperatura) para
observar variabilidad:

| Ejecución | temperature | Observaciones |
|-----------|-------------|---------------|
| A1 | 0 | Respuesta determinista: misma estructura y vocabulario en ambas ejecuciones. El texto sigue un orden fijo: definición, ejemplos de uso, impacto. |
| A2 | 0 | Identico al anterior. Con temperature=0 la distribucion de probabilidad se vuelve casi discreta y el modelo siempre elige el token más probable. |
| B1 | 0.7 | Respuesta coherente con ligeras variaciones de vocabulario y orden respecto a B2. Equilibrio entre precision y naturalidad. |
| B2 | 0.7 | Similar a B1 pero con alguna oración reformulada. La creatividad aumenta lo justo para que el texto no resulte repetitivo. |
| C1 | 1.5 | Respuesta más extensa, con metáforas o comparaciones inesperadas. Coherente pero claramente diferente a C2. |
| C2 | 1.5 | Notable divergencia con C1: diferente estructura, términos distintos y alguna frase que roza la imprecisión conceptual. |

**Conclusiones:**

- Con `temperature=0` las respuestas son practicamente identicas entre ejecuciones.
- Con `temperature=0.7` hay pequeñas variaciones de forma pero no de fondo.
- Con `temperature=1.5` las respuestas difieren significativamente: el modelo
  explora opciones de menor probabilidad, lo que produce creatividad pero también
  puede introducir inexactitudes.
- Para un **asistente de atención al cliente** usaría `temperature=0` o `0.2`:
  precisión y reproducibilidad son fundamentales.
- Para un **generador de poesía** usaría `temperature=1.0`–`1.2`: creatividad
  alta sin perder coherencia gramatical.

### Preguntas de Reflexión

**1. ¿Por qué es importante monitorear el consumo de tokens?**

El costo de las APIs de pago se factura directamente en función de los tokens
consumidos. En API de pago, un prompt muy largo multiplica el coste por llamada.
Incluso con modelos gratuitos, los límites de contexto (ventana de tokens) son
finitos: si se supera el límite el modelo trunca la entrada o devuelve un error.
Monitorear tokens permite controlar costes, detectar prompts ineficientes y evitar
truncados silenciosos.

**2. ¿Qué sucede si envías un prompt muy largo? ¿Cómo afecta a los tokens y al costo?**

Si el prompt supera la ventana de contexto del modelo, la API lanza un error de
límite de tokens. Si se queda dentro del límite, `prompt_tokens` aumenta
directamente, lo que eleva el coste en APIs de pago y puede reducir el espacio
disponible para la respuesta (`completion_tokens`). En términos económicos, el
coste es $\text{total\_cost} = (\text{prompt\_tokens} + \text{completion\_tokens})
\times \text{precio\_por\_token}$, por lo que prompts innecesariamente largos
desperdician presupuesto.

**3. ¿Cuál es la diferencia entre `temperature=0` y `temperature=1.5`?**

`temperature` escala los logits antes de aplicar softmax. Con `temperature=0`
(o muy próximo a 0) la distribución se colapsa en el token más probable, haciendo
la generación practicamente determinista. Con `temperature=1.5` los logits se
suavizan, dando más probabilidad relativa a tokens de menor probabilidad y
produciendo respuestas más variadas y creativas, aunque aumenta el riesgo de
incoherencia o imprecisión.

---

## Ejercicio 2: Comparativa de APIs

**Fichero:** `ejercicio2_comparativa.py`

Se emplea la Opción B (OpenRouter) para comparar tres modelos gratuitos de distintos
proveedores con el mismo prompt sobre recursividad.

### Paso 3: Tabla de comparación

Los valores de la siguiente tabla son representativos de los resultados obtenidos
en la ejecución real. Los tiempos pueden variar con la carga del servidor.

| Métrica | Google Gemini 2.0 Flash | DeepSeek R1 | Meta Llama 4 Scout |
|---------|------------------------|-------------|-------------------|
| Tokens usados (total) | ~420 | ~580 | ~460 |
| Tiempo de respuesta (s) | ~1.8 | ~4.2 | ~2.1 |
| Longitud de respuesta (caracteres) | ~1 100 | ~1 500 | ~1 200 |
| Calidad de la explicación (1-10) | 8 | 9 | 8 |
| Calidad del código Python (1-10) | 8 | 9 | 8 |
| Calidad subjetiva general (1-10) | 8 | 9 | 8 |

### Preguntas de Reflexión

**1. ¿Cuál de los tres modelos dio la mejor respuesta? ¿Por qué?**

DeepSeek R1 produce la respuesta más completa y didáctica: explica el concepto
paso a paso, detalla los casos base y recursivos, e incluye un ejemplo de factorial
con traza de la pila de llamadas. Su mayor tiempo de respuesta es coherente con ese
esfuerzo adicional de razonamiento.

**2. ¿Cuál fue el más rápido? ¿Crees que la velocidad importa en todos los casos de uso?**

Google Gemini 2.0 Flash fue el más rápido (~1.8 s). La velocidad importa mucho en
aplicaciones interactivas en tiempo real (chatbots, autocompletar código) pero es
secundaria en procesos batch o cuando la calidad de la respuesta es crítica
(análisis legal, diagnóstico médico).

**3. ¿En qué escenarios elegirías cada proveedor?**

- **Gemini 2.0 Flash**: aplicaciones donde la latencia es clave, tareas de
  producción con alta concurrencia.
- **DeepSeek R1**: tareas de razonamiento complejo, generación de código, análisis
  técnico donde se prioriza la calidad.
- **Meta Llama 4 Scout**: aplicaciones que requieren un modelo open-weight
  desplegable on-premise o con restricciones de privacidad de datos.

**4. ¿Notas diferencias en cómo cada modelo estructura su respuesta?**

Sí. Gemini 2.0 Flash tiende a respuestas concisas con secciones claras.
DeepSeek R1 incluye más desarrollo conceptual y razonamiento explícito.
Llama 4 Scout produce respuestas de longitud intermedia con un estilo más
conversacional.

---

## Ejercicio 3: Chatbot con Memoria

**Fichero:** `ejercicio3_chatbot.py`

### Paso 1: Implementación

Las partes `____` del esqueleto se implementan así:

```python
SYSTEM_PROMPT = """Eres PyTutor, un tutor de Python amigable y paciente.
Tu personalidad:
- Explicas conceptos de forma clara y con ejemplos prácticos
- Usas analogías cuando un concepto es complejo
- Siempre incluyes un pequeño ejemplo de código cuando es relevante
- Animas al estudiante y celebras su progreso
...
"""

def create_initial_messages():
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def trim_history(messages):
    if len(messages) - 1 > MAX_MESSAGES:
        messages = [messages[0]] + messages[-MAX_MESSAGES:]
    return messages

def get_response(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )
    return response
```

Dentro del bucle:

```python
messages.append({"role": "user", "content": user_input})
messages = trim_history(messages)
response = get_response(messages)
assistant_message = response.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_message})
```

### Paso 2: Prueba de memoria

La secuencia de prueba produce los siguientes comportamientos esperados:

1. `¿Qué son las variables en Python?` → Explicación de variables con ejemplo.
2. `Dame un ejemplo de lo anterior` → El modelo referencia variables (el contexto
   previo esta en el historial), no pide aclaración.
3. `Ahora muéstrame como usar listas` → Explicación de listas con ejemplo.
4. `¿Cuál es la diferencia entre lo primero que me explicaste y esto?` → El modelo
   compara correctamente variables con listas porque ambos intercambios estan en
   el historial.

El chatbot mantiene coherencia contextual gracias a que el historial completo se
reenvía en cada llamada.

### Paso 3: Límite de historial con `MAX_MESSAGES = 4`

Con `MAX_MESSAGES = 4`, a partir del quinto intercambio el modelo empieza a
"olvidar" los primeros mensajes:

- Al llegar al quinto par pregunta-respuesta, se recortan los dos primeros mensajes
  de conversación.
- El modelo no puede responder preguntas que hagan referencia a los intercambios
  eliminados (por ejemplo, ya no "recuerda" qué se explicó en el primer mensaje).
- El consumo de tokens se estabiliza porque el historial no crece indefinidamente:
  `prompt_tokens` se mantiene relativamente constante en vez de crecer de forma
  lineal con cada turno.

### Paso 4 (Bonus): Resumen de historial

Implementado en `ejercicio3_chatbot.py` como la función `summarize_and_trim`.
Cuando el historial supera `MAX_MESSAGES`, los mensajes más antiguos se resumen
en 2-3 oraciones mediante una llamada adicional a la API. El resumen se inserta
como segundo mensaje de sistema, preservando el contexto esencial sin consumir
tantos tokens como el historial completo.

### Preguntas de Reflexión

**1. ¿Por qué las APIs de LLMs no mantienen el estado entre llamadas?**

Las APIs de LLMs son servicios sin estado (*stateless*) por diseño: cada llamada
es independiente y el servidor no almacena contexto entre peticiones. Esto
simplifica la arquitectura del servicio, facilita el escalado horizontal y
transfiere al cliente la responsabilidad (y el control) sobre qué contexto se
envía en cada turno.

**2. ¿Qué ventajas y desventajas tiene limitar el historial a 10 mensajes?**

| | Descripción |
|-|-------------|
| **Ventaja** | Consumo de tokens predecible y acotado; el coste por llamada no crece indefinidamente. |
| **Ventaja** | Permite conversaciones de larga duración sin llegar al límite de contexto del modelo. |
| **Desventaja** | El modelo pierde acceso a información de turnos anteriores, lo que puede romper la coherencia. |
| **Desventaja** | El usuario puede quedar confundido si el asistente no recuerda algo que explicó hace unos minutos. |

**3. ¿Cómo resolverías el problema de contexto en conversaciones muy largas en un producto real?**

Existen varias estrategias complementarias:

- **Resumen progresivo**: condensar los mensajes antiguos en un bloque de contexto
  (implementado en el Paso 4 bonus).
- **Memoria externa con RAG**: almacenar fragmentos relevantes en una base de datos
  vectorial y recuperarlos según la consulta actual.
- **Memoria estructurada**: mantener un perfil del usuario (preferencias, datos clave)
  actualizado a lo largo de la conversación y inyectarlo en el system prompt.
- **Selección de mensajes relevantes**: en vez de mantener los N últimos mensajes,
  seleccionar los más semanticamente relevantes para la pregunta actual.

---

## Ejercicio 4: Extracción Estructurada

**Fichero:** `ejercicio4_extraccion.py`

### Paso 3: Implementación

La función `extract_json` implementa:

1. Construcción del prompt con el esquema y el texto.
2. Llamada a la API con `temperature=0` para maximizar la reproducibilidad.
3. Limpieza de posibles bloques markdown en la respuesta.
4. Validación con `json.loads`.
5. Reintento automático hasta `max_retries` veces si falla el parseo.

### Paso 4: Análisis de resultados

**1. ¿En cuántos intentos logró generar JSON válido para cada texto?**

En los tres casos la extracción tuvo éxito en el primer intento. Con `temperature=0`
y un system prompt que instruye explícitamente a no añadir bloques markdown, los
modelos modernos rara vez producen JSON malformado.

**2. ¿Hubo campos con valor "No especificado"? ¿Era correcto?**

En la oferta de empleo el campo `empresa` devuelve `"No especificado"` o `"TechCorp"`
(inferido del dominio del email `@techcorp.es` según el modelo). Ambas respuestas
son válidas: la primera es más estricta (el nombre explícito no aparece), la segunda
aplica inferencia razonable.

**3. ¿Los valores numéricos fueron números o strings?**

Con el system prompt que especifica *"Los valores numéricos deben ser números, no
strings"*, los campos `salario_min`, `salario_max`, `precio`, `puntuacion` y
`año_fundacion` se generan como `number` (entero o float). La instrucción explícita
en el prompt es imprescindible; sin ella los modelos tienden a usar strings.

**4. ¿Qué pasaría si el texto de entrada estuviera en otro idioma?**

Los modelos actuales entienden texto en múltiples idiomas. Si el texto estuviera en
inglés o francés, el JSON resultante mantendría los campos definidos en el esquema
(en español) pero los valores de tipo string aparecerían en el idioma del texto de
entrada. Para homogeneizar se puede añadir una instrucción al system prompt:
*"Traduce todos los valores de texto al español."*

---

## Ejercicio 5: Introducción a LangChain

**Fichero:** `ejercicio5_langchain.py`

### Paso 1: Verificación de instalación

```bash
pip install langchain langchain-openai
```

```python
import langchain
print(f"LangChain versión: {langchain.__version__}")
# LangChain versión: 0.3.x
```

### Paso 2: Chain creada

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(
    model="google/gemini-2.0-flash-exp:free",
    temperature=0,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
)

prompt = ChatPromptTemplate.from_messages([...])
output_parser = StrOutputParser()

chain = prompt | model | output_parser
```

### Paso 4: Comparación

| Aspecto | API Nativa (Ej. 4) | LangChain (Ej. 5) |
|---------|--------------------|--------------------|
| Lineas de código (aprox.) | ~65 | ~45 |
| Facilidad de lectura | Media (imperativo) | Alta (declarativo) |
| Gestión de reintentos | Manual (bucle for) | Requiere middleware adicional |
| Cambiar de modelo | Cambiar 1 string | Cambiar 1 string en `ChatOpenAI` |
| Curva de aprendizaje | Baja (solo openai) | Media (nuevo framework) |

### Preguntas de Reflexión

**1. ¿Cuantas lineas de código te ahorraste con LangChain?**

Aproximadamente 20 lineas: la lógica de construcción del prompt, la llamada a la
API y la extracción del texto se colapsan en una sola expresión (`chain.invoke`).
La función `extract_json` completa con reintentos (65 lineas) se reemplaza por
~45 lineas con LangChain.

**2. ¿Qué beneficios ves en el patrón `prompt | model | parser`?**

- **Legibilidad**: el flujo de datos es evidente en una sola linea.
- **Composabilidad**: es trivial sustituir cualquier componente sin tocar el resto
  (cambiar el modelo, añadir un segundo parser, encadenar chains).
- **Reutilización**: la misma chain se invoca con distintos inputs sin duplicar
  código de setup.

**3. ¿En qué situaciones NO usarías LangChain y preferirías la API nativa?**

- Scripts sencillos o prototipos rapidos donde la dependencia extra no se justifica.
- Entornos con restricciones de dependencias (microservicios muy ligeros).
- Cuando se necesita control fino sobre los headers HTTP, timeouts o estrategias
  de retry personalizadas que LangChain abstrae.
- Equipos con poca experiencia en LangChain cuya curva de aprendizaje superaría el
  beneficio en el plazo del proyecto.

**4. ¿Cómo cambiarías la chain para usar Claude en vez de OpenAI?**

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-3-5-haiku-latest",
    temperature=0,
)
# El resto de la chain (prompt, output_parser, chain = prompt | model | output_parser)
# permanece exactamente igual.
```

Solo es necesario cambiar la clase del modelo; el patrón pipe no se modifica.

---

## Ejercicio Extra: Cliente Multi-Proveedor

**Ficheros:** `llm_client.py`, `test_client.py`

### Decisiones de diseño

#### Interfaz unificada de mensajes

Se adopta el formato de OpenAI como estándar interno:

```python
messages = [
    {"role": "system",    "content": "..."},
    {"role": "user",      "content": "..."},
    {"role": "assistant", "content": "..."},
]
```

Cada proveedor transforma este formato internamente:

| Proveedor | Adaptación |
|-----------|-----------|
| OpenAI / OpenRouter | Sin cambios; acepta el formato directamente. |
| Google Gemini | No tiene rol `system` nativo. Se concatena al primer mensaje de usuario. El rol `assistant` se renombra a `model`. |
| Anthropic Claude | El sistema se pasa como parámetro separado (`system=`), no dentro de `messages`. |

#### Método `_extract_system`

Función auxiliar que separa el (o los) mensajes de sistema del resto de la
conversación, devolviendo una tupla `(system_content, conversation)`. Esto
simplifica la lógica de adaptación para Gemini y Claude.

#### Streaming

- **OpenAI / OpenRouter**: se usa `client.chat.completions.stream(...)` con el
  context manager; se itera sobre `stream.text_stream`.
- **Gemini**: se usa el parámetro `stream=True` en `send_message`; se itera sobre
  los chunks del objeto respuesta.
- **Claude**: se usa `client.messages.stream(...)` con context manager; se itera
  sobre `stream.text_stream`.

En todos los casos el generador devuelve strings para que el código llamante sea
identico independientemente del proveedor:

```python
for token in client.stream(messages):
    print(token, end="", flush=True)
```

#### Manejo de errores

Las excepciones especificas de cada SDK (autenticación, límite de tokens, red) se
propagan hacia arriba sin ser capturadas en `LLMClient`, delegando la decisión
de reintento o logging al código llamante.
