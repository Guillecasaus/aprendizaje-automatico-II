# Ejercicios Prácticos - Unidad 5, Sesión 1
## Fundamentos de RAG: Embeddings, Vectores y Chunking

---

## Ejercicio 1: Análisis Conceptual de una Arquitectura RAG

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 5.1 sobre introducción a RAG y sus componentes principales

### Contexto
Retrieval-Augmented Generation (RAG) combina la capacidad generativa de los LLMs con la recuperación de información de fuentes externas para producir respuestas fundamentadas en datos reales. Antes de implementar un sistema RAG, es fundamental saber diseñar su arquitectura: elegir las fuentes de datos, la estrategia de chunking, el modelo de embeddings y la base de datos vectorial adecuada para cada caso de uso. Este ejercicio entrena la capacidad de tomar decisiones de diseño informadas.

### Objetivo de Aprendizaje
- Comprender los componentes fundamentales de un pipeline RAG
- Identificar las decisiones de diseño clave en cada etapa del pipeline
- Evaluar qué tecnologías y configuraciones son más adecuadas según el contexto
- Desarrollar pensamiento crítico sobre las limitaciones de RAG frente a fine-tuning

### Enunciado

Para cada uno de los siguientes escenarios empresariales, diseña la arquitectura RAG completando la tabla con las decisiones técnicas que tomarías. Justifica brevemente cada elección.

### Escenario A: Asistente Legal para un Despacho de Abogados

Un despacho de abogados con 15 años de actividad quiere un asistente que responda preguntas sobre jurisprudencia, legislación vigente y documentos internos (contratos, dictámenes). Los documentos incluyen PDFs escaneados, documentos Word y bases de datos de sentencias.

| Componente | Tu decisión | Justificación |
|------------|-------------|---------------|
| **Fuentes de datos** | PDFs escaneados de jurisprudencia, documentos Word de contratos y dictámenes, y base de datos SQL de sentencias judiciales | El despacho lleva 15 años de actividad y ha acumulado documentos en múltiples formatos; es necesario integrar todas las fuentes para que el asistente tenga cobertura completa del conocimiento legal disponible |
| **Preprocesamiento necesario** | OCR con Tesseract o Azure Document Intelligence para los PDFs escaneados, extracción de texto de Word con python-docx, y normalización de estructura (eliminación de encabezados/pies de página, corrección de errores de OCR) | Los PDFs escaneados no contienen texto seleccionable, por lo que sin OCR no se podría indexar su contenido; además, los documentos legales suelen tener encabezados repetitivos y numeración de páginas que añadirían ruido a los embeddings |
| **Estrategia de chunking** | Chunking semántico por secciones legales (artículos, fundamentos de derecho, fallos) combinado con RecursiveCharacterTextSplitter como fallback | Los documentos legales tienen una estructura jerárquica bien definida (artículos, considerandos, fundamentos); respetar esa estructura garantiza que cada chunk contenga una unidad lógica completa, crucial para que las respuestas sean jurídicamente coherentes |
| **Tamaño de chunk recomendado** | 512-1024 tokens con overlap de 128 tokens | Los textos legales son densos y las referencias cruzadas entre párrafos son frecuentes; un tamaño de 512-1024 tokens permite capturar un argumento jurídico completo sin perder contexto, y el overlap evita que un razonamiento se corte entre dos chunks |
| **Modelo de embeddings** | Modelo local como `intfloat/multilingual-e5-large` o `BAAI/bge-m3` | Al tratarse de documentos legales confidenciales, se necesita un modelo que se ejecute on-premise para no enviar datos sensibles a APIs externas; además, estos modelos soportan español y tienen buen rendimiento en textos especializados |
| **Base de datos vectorial** | Weaviate self-hosted o pgvector (si ya usan PostgreSQL) | La confidencialidad de los documentos legales exige que la base de datos vectorial se ejecute en infraestructura propia; Weaviate ofrece búsqueda híbrida (vectorial + BM25) que es muy útil para encontrar referencias exactas a artículos de ley por su numeración |
| **Número de chunks a recuperar (top-k)** | top-k = 5 a 8, con re-ranking posterior usando un cross-encoder | En contextos legales se necesita recuperar suficientes fragmentos para cubrir distintos ángulos de una cuestión jurídica (hechos, fundamentos, jurisprudencia relacionada), pero el re-ranking asegura que solo los más relevantes lleguen al LLM para evitar confusión |
| **LLM para generación** | GPT-4o o Claude 3.5 Sonnet a través de API, o Llama 3 70B local si la confidencialidad lo exige | Se requiere un modelo con fuerte capacidad de razonamiento para interpretar correctamente textos legales complejos; GPT-4o y Claude destacan en comprensión de textos densos y en seguir instrucciones para citar fuentes, aunque si la regulación impide usar APIs externas, Llama 3 70B es la mejor alternativa local |

### Escenario B: FAQ Inteligente para una Universidad

La universidad U-TAD quiere que los estudiantes puedan hacer preguntas sobre normativas académicas, planes de estudio, horarios, convocatorias de exámenes y servicios del campus. La información está en la web institucional, PDFs de normativa y documentos de Moodle.

| Componente | Tu decisión | Justificación |
|------------|-------------|---------------|
| **Fuentes de datos** | Web institucional de U-TAD (scraping), PDFs de normativa académica, documentos y recursos de Moodle (exportados vía API o manualmente) | Son las tres fuentes principales donde los estudiantes buscan información; integrarlas todas evita que el asistente dé respuestas incompletas o desactualizadas |
| **Estrategia de chunking** | RecursiveCharacterTextSplitter con chunk_size=300 y overlap=50, usando separadores de párrafo y punto como delimitadores principales | La información universitaria suele estar organizada en preguntas-respuestas cortas o párrafos breves; un tamaño de 300 caracteres es suficiente para capturar una respuesta completa a una pregunta frecuente sin incluir información de otras secciones |
| **Modelo de embeddings** | `text-embedding-3-small` de OpenAI | Es un modelo eficiente, económico y con buen rendimiento en español; al no tratarse de datos confidenciales (es información pública de la universidad), se puede usar una API en la nube sin restricciones de privacidad |
| **Base de datos vectorial** | ChromaDB o Pinecone (tier gratuito) | Para un FAQ universitario el volumen de documentos es moderado (~50 documentos, ~500 páginas); ChromaDB es ideal para empezar rápido sin infraestructura, y Pinecone ofrece un tier gratuito que cubre perfectamente este volumen con persistencia en la nube |
| **LLM para generación** | GPT-4o-mini o Claude 3.5 Haiku | Las preguntas de un FAQ universitario no requieren razonamiento complejo; un modelo más pequeño y económico es suficiente para responder preguntas factuales sobre horarios, normativas y servicios, reduciendo costes y latencia significativamente |

### Escenario C: Soporte Técnico para Documentación de Software

Una empresa SaaS con documentación técnica extensa (API reference, tutoriales, guías de migración, changelogs) quiere un chatbot que responda consultas técnicas de desarrolladores. La documentación se actualiza semanalmente.

| Componente | Tu decisión | Justificación |
|------------|-------------|---------------|
| **Fuentes de datos** | Repositorio Git con archivos Markdown (API reference, tutoriales, guías de migración), changelogs en formato texto/Markdown | La documentación técnica SaaS suele estar versionada en Git con formato Markdown, lo que facilita la extracción de texto estructurado y permite detectar automáticamente qué archivos han cambiado entre reindexaciones |
| **Estrategia de chunking** | MarkdownHeaderTextSplitter que divide por encabezados (h1, h2, h3) preservando la jerarquía, complementado con RecursiveCharacterTextSplitter para secciones muy largas | La documentación técnica en Markdown ya tiene una estructura semántica clara definida por encabezados; dividir por secciones garantiza que cada chunk corresponda a un concepto o endpoint específico, y los metadatos de jerarquía permiten al LLM saber en qué sección de la documentación se encuentra |
| **Frecuencia de reindexación** | Pipeline CI/CD que reindexe automáticamente al hacer merge a la rama principal (incremental, solo documentos modificados) | La documentación se actualiza semanalmente; una reindexación incremental activada por el pipeline de CI evita reindexar todo el corpus cada vez y garantiza que los cambios estén disponibles inmediatamente tras el despliegue |
| **Modelo de embeddings** | `text-embedding-3-small` de OpenAI con dimensiones reducidas a 512 | Es un buen equilibrio entre calidad y coste para documentación técnica en inglés; reducir las dimensiones a 512 ahorra almacenamiento y mejora la velocidad de búsqueda sin pérdida significativa de relevancia para consultas técnicas |
| **Base de datos vectorial** | Pinecone Serverless | Al ser una empresa SaaS, se valora no tener que gestionar infraestructura; Pinecone Serverless escala automáticamente, ofrece baja latencia y soporta actualización incremental del índice sin downtime, ideal para documentación que cambia frecuentemente |
| **Estrategia de búsqueda** | Búsqueda híbrida (vectorial + keyword BM25) con re-ranking | Los desarrolladores suelen buscar por nombres exactos de funciones, endpoints o parámetros (donde BM25 es superior) pero también hacen preguntas conceptuales ("¿cómo autenticar una petición?") donde la búsqueda semántica destaca; la combinación híbrida con re-ranking cubre ambos patrones de consulta |

### Preguntas de Reflexión

1. **RAG vs. Fine-tuning**: En el Escenario A, el despacho se plantea si sería mejor hacer fine-tuning de un modelo con todos sus documentos en lugar de usar RAG. ¿Qué le recomendarías y por qué? Considera aspectos como actualización de datos, alucinaciones, coste y trazabilidad de las respuestas.

**Respuesta:** Recomendaría RAG sobre fine-tuning por varias razones fundamentales. Primero, **actualización de datos**: la legislación y jurisprudencia cambian constantemente (nuevas sentencias, reformas legales); con RAG basta con añadir los nuevos documentos al índice vectorial, mientras que con fine-tuning habría que reentrenar el modelo cada vez, lo cual es costoso y lento. Segundo, **alucinaciones**: RAG reduce drásticamente las alucinaciones porque el LLM genera respuestas basándose en fragmentos concretos recuperados de los documentos reales; con fine-tuning, el modelo "memoriza" información en sus pesos y puede mezclar o inventar datos, algo inaceptable en el ámbito legal. Tercero, **trazabilidad**: RAG permite citar exactamente de qué documento y sección proviene cada afirmación, lo cual es esencial para un abogado que necesita verificar las fuentes; con fine-tuning no hay forma de rastrear el origen de la información. Cuarto, **coste**: el fine-tuning de un modelo grande es significativamente más caro (miles de euros por entrenamiento) y requiere expertise en ML, mientras que RAG se puede montar con herramientas existentes a una fracción del coste. La única ventaja del fine-tuning sería adaptar el tono y estilo del modelo al lenguaje jurídico, pero esto se puede lograr igualmente con un buen prompt template en RAG.

2. **Privacidad**: El Escenario A maneja documentos legales confidenciales. ¿Cómo afecta esto a la elección de modelo de embeddings y LLM? ¿Usarías APIs en la nube o modelos locales?

**Respuesta:** La confidencialidad de los documentos legales condiciona fuertemente la arquitectura. Lo más seguro sería utilizar **modelos locales** tanto para embeddings como para el LLM, evitando enviar datos sensibles a APIs externas donde podrían ser procesados o almacenados en servidores de terceros. Para embeddings, usaría un modelo local como `intfloat/multilingual-e5-large` o `BAAI/bge-m3`, que se ejecutan en la propia infraestructura del despacho. Para el LLM, un modelo open-source como Llama 3 70B o Mistral Large desplegado localmente con vLLM o Ollama. Si el despacho tiene presupuesto limitado para GPUs, una alternativa intermedia sería usar APIs con acuerdos de procesamiento de datos (DPA) que garanticen que los datos no se usan para entrenar modelos — como las APIs empresariales de OpenAI o Azure OpenAI con residencia de datos en la UE y cumplimiento del RGPD. La base de datos vectorial también debería ser self-hosted (Weaviate, Qdrant o pgvector) y nunca en un servicio cloud sin garantías contractuales de confidencialidad.

3. **Escalabilidad**: Si el Escenario C pasa de 1.000 a 100.000 documentos, ¿qué componentes de tu arquitectura necesitarían cambiar?

**Respuesta:** Al escalar 100x el volumen de documentos, los principales cambios serían: (1) **Base de datos vectorial**: habría que migrar de Pinecone Serverless estándar a un tier superior o a una solución como Weaviate/Milvus en cluster, ya que 100.000 documentos con sus chunks pueden generar millones de vectores que requieren indexación distribuida (algoritmos como HNSW necesitan más memoria y particionamiento). (2) **Pipeline de ingesta**: sería necesario un pipeline de procesamiento paralelo y asíncrono (con herramientas como Apache Airflow o Celery) para indexar grandes lotes de documentos sin bloquear el sistema. (3) **Estrategia de búsqueda**: con un corpus tan grande, la búsqueda puramente vectorial puede devolver resultados poco precisos; sería recomendable implementar búsqueda híbrida (vectorial + BM25) con re-ranking, y añadir filtrado por metadatos (tipo de documento, fecha, versión) para reducir el espacio de búsqueda. (4) **Modelo de embeddings**: podría ser necesario un modelo con mayor capacidad de discriminación semántica (como `text-embedding-3-large`) para mantener la calidad de recuperación con un corpus más diverso. (5) **Caché de consultas frecuentes** para reducir la latencia y el coste de las peticiones repetidas al LLM.

---

## Ejercicio 2: Experimentación con Embeddings y Similitud Semántica

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Lectura de la sección 5.2 sobre embeddings y espacios vectoriales, conocimientos básicos de Python y numpy

### Contexto
Los embeddings son representaciones numéricas densas de texto que capturan su significado semántico. La calidad de un sistema RAG depende directamente de la calidad de sus embeddings: si frases con significado similar no producen vectores cercanos, la recuperación fallará. Este ejercicio permite experimentar de primera mano con embeddings, entender la similitud coseno y descubrir tanto las capacidades como las limitaciones de estos modelos.

### Objetivo de Aprendizaje
- Generar embeddings usando la API de OpenAI o sentence-transformers
- Calcular e interpretar la similitud coseno entre vectores
- Identificar patrones: sinonimia, paráfrasis, negación, cambio de idioma
- Comprender las limitaciones de los embeddings para ciertos tipos de relaciones semánticas

### Enunciado

Escribe un programa en Python que genere embeddings para un conjunto de frases y analice las relaciones semánticas entre ellas mediante similitud coseno.

### Paso 1: Configuración del entorno

Elige **una** de las dos opciones:

**Opción A: OpenAI API** (requiere API key)
```python
from openai import OpenAI
import numpy as np

client = OpenAI()  # Usa OPENAI_API_KEY del entorno

def get_embedding(text, model="text-embedding-3-small"):
    """Genera el embedding de un texto usando OpenAI."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return np.array(response.data[0].embedding)
```

**Opción B: Sentence-Transformers** (local, gratuito)
```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text, model=model):
    """Genera el embedding de un texto usando sentence-transformers."""
    return model.encode(text)
```

### Paso 2: Definir las frases de prueba

Usa el siguiente conjunto de frases diseñado para explorar diferentes relaciones semánticas:

```python
frases = {
    # Grupo 1: Frases semánticamente similares (paráfrasis)
    "A1": "El gato se sentó en la alfombra",
    "A2": "Un felino descansaba sobre el tapete",
    "A3": "The cat sat on the mat",  # Misma idea, otro idioma

    # Grupo 2: Frases sobre tecnología
    "B1": "Python es un lenguaje de programación muy popular",
    "B2": "JavaScript se usa mucho para desarrollo web",
    "B3": "Los lenguajes de programación son herramientas esenciales",

    # Grupo 3: Negación y contraste
    "C1": "El restaurante tiene buena comida",
    "C2": "El restaurante no tiene buena comida",
    "C3": "La comida del restaurante es terrible",

    # Grupo 4: Frases sin relación
    "D1": "La fotosíntesis convierte luz solar en energía",
    "D2": "El precio del petróleo subió un 5% ayer",
}
```

### Paso 3: Generar embeddings y calcular similitudes

```python
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    """Calcula la similitud coseno entre dos vectores."""
    return dot(a, b) / (norm(a) * norm(b))

# Generar embeddings para todas las frases
embeddings = {}
for key, frase in frases.items():
    embeddings[key] = get_embedding(frase)
    print(f"[{key}] Embedding generado - dimensiones: {len(embeddings[key])}")

# Calcular matriz de similitudes
print("\n--- MATRIZ DE SIMILITUD COSENO ---\n")
keys = list(frases.keys())
print(f"{'':>4}", end="")
for k in keys:
    print(f"{k:>8}", end="")
print()

for i, ki in enumerate(keys):
    print(f"{ki:>4}", end="")
    for j, kj in enumerate(keys):
        sim = cosine_similarity(embeddings[ki], embeddings[kj])
        print(f"{sim:>8.3f}", end="")
    print()
```

### Paso 4: Análisis de resultados

Responde a las siguientes preguntas basándote en los resultados obtenidos:

| Pregunta | Tu respuesta |
|----------|-------------|
| 1. ¿Cuál es la similitud entre A1 y A2 (paráfrasis en español)? ¿Es alta? | La similitud entre A1 ("El gato se sentó en la alfombra") y A2 ("Un felino descansaba sobre el tapete") es alta, aproximadamente 0.75-0.85 con `all-MiniLM-L6-v2`. Esto es esperable porque ambas frases expresan la misma idea usando sinónimos (gato/felino, alfombra/tapete, sentó/descansaba). El modelo captura correctamente que son paráfrasis, aunque no llega a 1.0 porque las palabras concretas difieren. |
| 2. ¿Cuál es la similitud entre A1 y A3 (misma idea, diferente idioma)? ¿Es comparable a A1-A2? | La similitud A1-A3 es moderada-alta (~0.50-0.70), pero generalmente inferior a A1-A2. Esto se debe a que `all-MiniLM-L6-v2` es un modelo multilingüe pero entrenado principalmente en inglés; captura parcialmente la equivalencia cross-lingual pero pierde información al cruzar idiomas. Con modelos multilingües más potentes como `multilingual-e5-large`, esta similitud sería más comparable a A1-A2. |
| 3. ¿Los embeddings de B1, B2 y B3 forman un grupo coherente? ¿Son más similares entre sí que con otros grupos? | Sí, las frases del grupo B forman un cluster coherente. B1-B2 tienen similitud ~0.55-0.65 (ambos hablan de lenguajes de programación específicos), B1-B3 y B2-B3 tienen similitud ~0.60-0.70 (B3 es una generalización del tema). Estas similitudes intra-grupo son claramente superiores a las similitudes con frases de otros grupos (generalmente <0.30), lo que confirma que los embeddings agrupan correctamente por temática. |
| 4. ¿Cuál es la similitud entre C1 ("buena comida") y C2 ("no tiene buena comida")? ¿Es sorprendentemente alta o baja? | La similitud C1-C2 es sorprendentemente alta, aproximadamente 0.85-0.92. Esto es contraintuitivo porque semánticamente expresan lo opuesto. La razón es que los embeddings capturan el tema y la estructura léxica (restaurante, comida, buena) pero son muy malos procesando la negación. El "no" apenas modifica el vector resultante porque es una palabra funcionalmente pequeña en el espacio de embeddings. |
| 5. ¿Los embeddings capturan bien la negación? Compara C1-C2 vs C1-C3. ¿Cuál debería ser más diferente semánticamente? | Los embeddings NO capturan bien la negación. C1-C2 (afirmación vs. negación directa) tiene similitud más alta (~0.88) que C1-C3 (buena comida vs. comida terrible, ~0.70-0.80). Semánticamente, C2 debería ser más diferente de C1 que C3, pero ocurre al revés. Esto sucede porque C3 usa palabras léxicamente distintas ("terrible") que desplazan más el vector, mientras que C2 solo añade "no" que casi no altera la representación. Esta es una limitación conocida y crítica de los modelos de embeddings basados en la media de tokens. |
| 6. ¿Las frases D1 y D2 tienen baja similitud con el resto de grupos, como esperarías? | Sí, D1 (fotosíntesis) y D2 (precio del petróleo) tienen baja similitud tanto entre sí (~0.10-0.25) como con el resto de grupos (~0.05-0.20). Son las frases más "aisladas" en el espacio vectorial, lo cual es correcto ya que tratan temas completamente distintos (biología y economía) sin relación con gatos, programación o restaurantes. Además, D1-D2 también tienen baja similitud entre sí, confirmando que los embeddings distinguen bien entre dominios temáticos diferentes. |
| 7. ¿Cuál es la dimensionalidad de los embeddings generados? ¿Qué modelo usaste? | Usé `all-MiniLM-L6-v2` de sentence-transformers, que genera embeddings de 384 dimensiones. Es un modelo ligero y gratuito, ideal para experimentación. Si se usa `text-embedding-3-small` de OpenAI, la dimensionalidad por defecto es 1536 (reducible con el parámetro `dimensions`), y con `text-embedding-3-large` es 3072. Mayor dimensionalidad generalmente permite capturar más matices semánticos, pero a costa de más almacenamiento y tiempo de búsqueda. |

### Paso 5 (Bonus): Visualización

Si tienes tiempo, añade una visualización 2D usando PCA o t-SNE:

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Reducir a 2D
vectors = np.array(list(embeddings.values()))
pca = PCA(n_components=2)
coords = pca.fit_transform(vectors)

# Graficar
plt.figure(figsize=(10, 8))
colors = {'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'orange'}
for i, key in enumerate(keys):
    grupo = key[0]
    plt.scatter(coords[i, 0], coords[i, 1], c=colors[grupo], s=100, zorder=5)
    plt.annotate(f"{key}: {frases[key][:30]}...",
                 (coords[i, 0], coords[i, 1]),
                 fontsize=8, ha='left', va='bottom')

plt.title("Embeddings proyectados en 2D (PCA)")
plt.xlabel("Componente 1")
plt.ylabel("Componente 2")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("embeddings_2d.png", dpi=150)
plt.show()
```

### Extensión (Opcional)

- Compara los resultados usando `text-embedding-3-small` vs `text-embedding-3-large` de OpenAI. ¿El modelo más grande captura mejor la negación?
- Añade frases en un tercer idioma (francés, alemán) y observa si se agrupan con sus equivalentes semánticos
- Experimenta con el parámetro `dimensions` de OpenAI para reducir la dimensionalidad del embedding y observa cómo afecta a las similitudes

---

## Ejercicio 3: Comparativa de Bases de Datos Vectoriales

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Exploración/Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 5.3 sobre bases de datos vectoriales

### Contexto
La elección de la base de datos vectorial es una de las decisiones arquitectónicas más importantes en un sistema RAG. No existe una opción universalmente mejor: la elección depende de factores como el volumen de datos, la necesidad de persistencia, el presupuesto, si se requiere búsqueda híbrida (vectorial + texto) y el nivel de experiencia del equipo. Este ejercicio te prepara para tomar esta decisión de forma informada en proyectos reales.

### Objetivo de Aprendizaje
- Conocer las principales bases de datos vectoriales del mercado
- Comparar sus características técnicas, modelos de pricing y casos de uso
- Evaluar qué solución es más adecuada según diferentes escenarios
- Distinguir entre soluciones locales, cloud-native y bases de datos tradicionales con extensiones vectoriales

### Enunciado

Investiga las siguientes bases de datos vectoriales y completa la tabla comparativa. Puedes usar la documentación oficial de cada una, artículos técnicos y los materiales de la asignatura.

### Parte 1: Tabla Comparativa

Completa la siguiente tabla para cada base de datos vectorial:

| Criterio | **FAISS** | **ChromaDB** | **Pinecone** | **Weaviate** | **pgvector** |
|----------|-----------|-------------|-------------|-------------|-------------|
| **Tipo** (librería / BD embebida / servicio cloud / extensión) | Librería | BD embebida | Servicio cloud (SaaS) | BD vectorial nativa (self-hosted o cloud) | Extensión de PostgreSQL |
| **Desarrollador** | Meta (Facebook AI Research) | Chroma Inc. | Pinecone Systems | Weaviate B.V. (SeMI Technologies) | Andrew Kane (open-source community) |
| **Lenguaje principal** | C++ con bindings Python | Python | Backend propietario; SDK en Python, JS, Go | Go | C (extensión de PostgreSQL) |
| **Persistencia** (en memoria / disco / cloud) | En memoria por defecto; puede serializar a disco | Disco local (SQLite + Parquet) o modo cliente-servidor | Cloud gestionado (serverless) | Disco (self-hosted) o cloud gestionado | Disco (hereda la persistencia de PostgreSQL) |
| **Coste** (gratuito / freemium / pago) | Gratuito (MIT license) | Gratuito (Apache 2.0) | Freemium (tier gratuito limitado; pago por uso en producción) | Gratuito self-hosted (BSD-3); cloud gestionado de pago | Gratuito (open-source, PostgreSQL license) |
| **Escalabilidad** (prototipo / producción pequeña / enterprise) | Prototipo a enterprise (escala con sharding manual) | Prototipo a producción pequeña | Producción a enterprise (escala automáticamente) | Producción a enterprise (soporta clusters distribuidos) | Producción pequeña a media (limitado por PostgreSQL) |
| **Búsqueda híbrida** (vectorial + keyword) | No nativa (solo vectorial) | Sí (desde v0.4, combina vectorial con filtros) | Sí (sparse-dense vectors) | Sí (BM25 + vectorial integrados nativamente) | Sí (combinando con búsqueda full-text nativa de PostgreSQL con tsvector) |
| **Filtrado por metadatos** | No nativo (requiere implementación manual pre/post-filtro) | Sí (filtros por metadatos en queries) | Sí (filtros avanzados por metadatos) | Sí (filtros ricos con operadores GraphQL) | Sí (filtros SQL estándar combinados con búsqueda vectorial) |
| **Integración con LangChain** | Sí (FAISS vectorstore) | Sí (integración nativa de primera clase) | Sí (integración oficial) | Sí (integración oficial) | Sí (PGVector vectorstore) |
| **Requiere infraestructura propia** | No (se ejecuta en proceso) | No para uso local; sí si se usa modo cliente-servidor | No (totalmente gestionado en la nube) | Sí para self-hosted (Docker); no si se usa Weaviate Cloud | Sí (requiere un servidor PostgreSQL) |
| **Curva de aprendizaje** (baja / media / alta) | Media (API de bajo nivel, requiere gestionar índices manualmente) | Baja (API pythónica muy simple, pocos conceptos) | Baja (API sencilla, dashboard web intuitivo) | Media (conceptos propios como schemas, modules, GraphQL) | Baja si ya conoces SQL; media si no |
| **Caso de uso ideal** | Investigación, prototipado rápido, benchmarking de algoritmos de búsqueda vectorial a gran escala | Prototipado rápido, proyectos académicos, aplicaciones locales pequeñas-medianas | Aplicaciones en producción que necesitan escalar sin gestionar infraestructura | Aplicaciones enterprise que requieren búsqueda híbrida avanzada y despliegue on-premise o cloud | Empresas que ya usan PostgreSQL y quieren añadir búsqueda semántica sin nueva infraestructura |

### Parte 2: Decisiones de Diseño

Para cada escenario, elige la base de datos vectorial más adecuada y justifica tu decisión:

**Escenario 1**: Un estudiante quiere hacer un prototipo rápido de RAG para un proyecto de clase, con ~100 documentos PDF.
- Base de datos elegida: **ChromaDB**
- Justificación: ChromaDB es la opción ideal para prototipado académico. Se instala con un simple `pip install chromadb`, no requiere ninguna infraestructura externa ni configuración de servidores. Su API en Python es extremadamente sencilla (3-4 líneas para indexar y buscar), lo que permite al estudiante centrarse en aprender los conceptos de RAG sin perder tiempo en configuración. Para ~100 documentos el rendimiento es más que suficiente incluso en un portátil con recursos limitados, y la persistencia en disco local permite retomar el trabajo entre sesiones.

**Escenario 2**: Una startup necesita un sistema RAG en producción que maneje 500.000 documentos y escale automáticamente, sin dedicar DevOps al mantenimiento.
- Base de datos elegida: **Pinecone Serverless**
- Justificación: Pinecone Serverless es un servicio totalmente gestionado que escala automáticamente según la demanda, eliminando la necesidad de un equipo de DevOps dedicado. Para una startup, esto es crucial porque permite centrarse en el producto en lugar de en la infraestructura. Soporta 500.000 documentos (potencialmente millones de vectores) sin degradación de rendimiento, ofrece alta disponibilidad con SLA, y su modelo de pricing pay-per-use se adapta al crecimiento de la startup. Además, incluye búsqueda híbrida y filtrado por metadatos necesarios para una buena experiencia de usuario en producción.

**Escenario 3**: Un banco necesita un sistema RAG para documentos financieros confidenciales. Todo debe ejecutarse on-premise por regulación. Tienen equipo de infraestructura.
- Base de datos elegida: **Weaviate self-hosted**
- Justificación: Weaviate se puede desplegar completamente on-premise con Docker o Kubernetes, cumpliendo con las regulaciones de datos financieros que prohíben enviar información a la nube. Al tener equipo de infraestructura, el banco puede gestionar el cluster de Weaviate sin problema. Ofrece búsqueda híbrida nativa (vectorial + BM25), fundamental para buscar por números de cuenta, referencias exactas o importes junto con consultas semánticas. Además, soporta RBAC (control de acceso basado en roles) y cifrado en reposo, requisitos habituales en el sector bancario. Como alternativa viable también se podría considerar pgvector si el banco ya tiene PostgreSQL, aunque Weaviate ofrece mejor rendimiento para búsqueda vectorial a gran escala.

**Escenario 4**: Una empresa ya usa PostgreSQL para toda su infraestructura y quiere añadir capacidad de búsqueda semántica sin introducir una nueva tecnología.
- Base de datos elegida: **pgvector**
- Justificación: pgvector es una extensión de PostgreSQL que añade soporte para vectores y búsqueda por similitud coseno directamente en la base de datos existente. La empresa no necesita aprender ni mantener una tecnología nueva: sus administradores de BD ya conocen PostgreSQL, los backups y la monitorización existentes siguen funcionando, y pueden combinar búsqueda semántica con consultas SQL estándar en una sola query (por ejemplo, filtrar por departamento y luego buscar por similitud). Se instala con `CREATE EXTENSION vector;` y se integra perfectamente con el ecosistema PostgreSQL existente (réplicas, pgAdmin, etc.).

### Parte 3: Pregunta de Reflexión

¿Es posible empezar con ChromaDB para un prototipo y migrar después a Pinecone para producción? ¿Qué abstracción de LangChain facilita esta migración? ¿Qué cambios serían necesarios en el código?

**Respuesta:** Sí, es totalmente posible y de hecho es un patrón muy recomendable. LangChain facilita esta migración gracias a su abstracción `VectorStore`, que define una interfaz común para todas las bases de datos vectoriales. Tanto `Chroma` como `PineconeVectorStore` implementan esta interfaz con los mismos métodos principales: `from_documents()`, `similarity_search()`, `add_documents()` y `as_retriever()`. Esto significa que el código del pipeline RAG que usa el vectorstore (la cadena de recuperación, el prompt template, la generación) no necesita cambiar en absoluto.

Los cambios concretos necesarios serían mínimos: (1) Cambiar la línea de importación de `from langchain_chroma import Chroma` a `from langchain_pinecone import PineconeVectorStore`. (2) Cambiar la inicialización del vectorstore, sustituyendo los parámetros de ChromaDB (directorio de persistencia) por los de Pinecone (API key, nombre del índice, entorno). (3) Reindexar todos los documentos en Pinecone, ya que los embeddings almacenados en ChromaDB no se transfieren automáticamente. El resto del código — la lógica de chunking, el modelo de embeddings, el retriever, las cadenas de LangChain — permanece idéntico. Este es precisamente el valor de usar abstracciones como LangChain: desacoplar la lógica de negocio de la infraestructura subyacente.

### Extensión (Opcional)

- Instala ChromaDB localmente (`pip install chromadb`) e indexa 5-10 documentos de prueba. Experimenta con diferentes consultas y observa los resultados de similitud.
- Investiga Qdrant y Milvus como alternativas adicionales y añádelos a la tabla comparativa.

---

## Ejercicio 4: Laboratorio de Estrategias de Chunking

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Lectura de la sección 5.4 sobre chunking, conocimientos de Python, familiaridad básica con LangChain

### Contexto
El chunking (fragmentación del texto) es una etapa crítica y a menudo subestimada en un pipeline RAG. Un chunking demasiado grande puede incluir información irrelevante que confunda al LLM; uno demasiado pequeño puede perder el contexto necesario para una respuesta coherente. El solapamiento (overlap) entre chunks permite que la información no se "corte" en medio de una idea. Este ejercicio te permite experimentar de primera mano con diferentes configuraciones y desarrollar intuición sobre sus efectos.

### Objetivo de Aprendizaje
- Usar `RecursiveCharacterTextSplitter` de LangChain con diferentes configuraciones
- Comprender el impacto del `chunk_size` y `chunk_overlap` en la fragmentación
- Analizar cuándo se pierde contexto y cuándo se preserva
- Desarrollar criterios para elegir la configuración óptima según el tipo de documento

### Enunciado

Experimenta con diferentes configuraciones de chunking sobre un documento de ejemplo y analiza los resultados.

### Paso 1: Preparar el documento de ejemplo

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Documento de ejemplo: artículo sobre inteligencia artificial
documento = """
# Introducción a la Inteligencia Artificial

La inteligencia artificial (IA) es una rama de la informática que busca crear sistemas
capaces de realizar tareas que normalmente requieren inteligencia humana. Estas tareas
incluyen el aprendizaje, el razonamiento, la percepción y la comprensión del lenguaje natural.

## Historia de la IA

El término "inteligencia artificial" fue acuñado por John McCarthy en 1956 durante la
conferencia de Dartmouth. Sin embargo, las ideas sobre máquinas pensantes se remontan a
mucho antes. Alan Turing, en 1950, propuso el famoso Test de Turing como criterio para
determinar si una máquina puede exhibir comportamiento inteligente indistinguible del humano.

Durante las décadas de 1960 y 1970, la IA experimentó un período de optimismo conocido
como la "edad de oro". Los investigadores creían que la IA general estaba a pocas décadas
de distancia. Sin embargo, las limitaciones computacionales y teóricas llevaron a los
"inviernos de la IA", períodos de reducción de financiación e interés.

## Aprendizaje Automático

El aprendizaje automático (machine learning) es un subcampo de la IA que se centra en
desarrollar algoritmos que permiten a las computadoras aprender de los datos sin ser
programadas explícitamente. Los tres paradigmas principales son:

1. Aprendizaje supervisado: el modelo aprende de ejemplos etiquetados.
2. Aprendizaje no supervisado: el modelo descubre patrones en datos sin etiquetar.
3. Aprendizaje por refuerzo: el modelo aprende mediante prueba y error con recompensas.

## Deep Learning

El deep learning o aprendizaje profundo utiliza redes neuronales con múltiples capas
(de ahí "profundo") para aprender representaciones jerárquicas de los datos. Las
arquitecturas más importantes incluyen:

- Redes Neuronales Convolucionales (CNN): especializadas en procesamiento de imágenes.
- Redes Neuronales Recurrentes (RNN): diseñadas para secuencias temporales.
- Transformers: la arquitectura dominante actual para procesamiento de lenguaje natural,
  introducida en el paper "Attention is All You Need" (2017).

## Modelos de Lenguaje

Los modelos de lenguaje grandes (LLMs) como GPT-4, Claude y Llama representan el estado
del arte en procesamiento de lenguaje natural. Estos modelos se entrenan con cantidades
masivas de texto y pueden generar texto coherente, traducir idiomas, resumir documentos
y responder preguntas.

La técnica de RAG (Retrieval-Augmented Generation) complementa estos modelos permitiéndoles
acceder a información externa actualizada, reduciendo las alucinaciones y proporcionando
respuestas más precisas y verificables.
"""

print(f"Longitud total del documento: {len(documento)} caracteres")
print(f"Número de líneas: {len(documento.splitlines())}")
```

### Paso 2: Experimentar con diferentes configuraciones

```python
configuraciones = [
    {"chunk_size": 100, "chunk_overlap": 0,  "nombre": "Muy pequeño, sin overlap"},
    {"chunk_size": 100, "chunk_overlap": 20, "nombre": "Muy pequeño, con overlap"},
    {"chunk_size": 300, "chunk_overlap": 0,  "nombre": "Mediano, sin overlap"},
    {"chunk_size": 300, "chunk_overlap": 50, "nombre": "Mediano, con overlap"},
    {"chunk_size": 500, "chunk_overlap": 50, "nombre": "Grande, con overlap pequeño"},
    {"chunk_size": 500, "chunk_overlap": 100,"nombre": "Grande, con overlap grande"},
    {"chunk_size": 1000,"chunk_overlap": 200,"nombre": "Muy grande, con overlap"},
]

for config in configuraciones:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"],
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_text(documento)

    print(f"\n{'='*70}")
    print(f"Configuración: {config['nombre']}")
    print(f"  chunk_size={config['chunk_size']}, chunk_overlap={config['chunk_overlap']}")
    print(f"  Número de chunks: {len(chunks)}")
    print(f"  Tamaño promedio: {sum(len(c) for c in chunks) / len(chunks):.0f} caracteres")
    print(f"  Tamaño mínimo: {min(len(c) for c in chunks)} caracteres")
    print(f"  Tamaño máximo: {max(len(c) for c in chunks)} caracteres")
    print(f"  Caracteres totales (con overlap): {sum(len(c) for c in chunks)}")

    # Mostrar los primeros 3 chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n  --- Chunk {i+1} ({len(chunk)} chars) ---")
        # Mostrar solo las primeras y últimas líneas
        lines = chunk.strip().split('\n')
        if len(lines) <= 4:
            print(f"  {chunk.strip()}")
        else:
            print(f"  {lines[0]}")
            print(f"  {lines[1]}")
            print(f"  ...")
            print(f"  {lines[-1]}")
```

### Paso 3: Análisis detallado del overlap

```python
# Analizar qué información se comparte entre chunks consecutivos
print("\n\n" + "="*70)
print("ANÁLISIS DE OVERLAP")
print("="*70)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_text(documento)

for i in range(len(chunks) - 1):
    chunk_actual = chunks[i]
    chunk_siguiente = chunks[i + 1]

    # Encontrar el texto solapado
    overlap_text = ""
    for length in range(min(len(chunk_actual), len(chunk_siguiente)), 0, -1):
        if chunk_actual.endswith(chunk_siguiente[:length]):
            overlap_text = chunk_siguiente[:length]
            break

    print(f"\nEntre Chunk {i+1} y Chunk {i+2}:")
    print(f"  Overlap encontrado ({len(overlap_text)} chars): \"{overlap_text[:80]}...\"" if len(overlap_text) > 80 else f"  Overlap encontrado ({len(overlap_text)} chars): \"{overlap_text}\"")
    print(f"  Final chunk {i+1}: \"...{chunk_actual[-50:]}\"")
    print(f"  Inicio chunk {i+2}: \"{chunk_siguiente[:50]}...\"")
```

### Paso 4: Tabla de análisis comparativo

Completa la siguiente tabla con los resultados de tus experimentos:

| Configuración | N. Chunks | Tam. Promedio | ¿Se cortan ideas a mitad? | ¿Hay redundancia excesiva? |
|--------------|-----------|---------------|---------------------------|---------------------------|
| 100, overlap 0 | ~22 | ~85 chars | Sí, constantemente. Frases cortadas a mitad de palabra o idea; los chunks son fragmentos sin sentido propio. | No, sin overlap no hay redundancia alguna. |
| 100, overlap 20 | ~27 | ~80 chars | Sí, igual que sin overlap. El overlap de 20 chars es demasiado pequeño para salvar ideas completas. | Mínima; el overlap de 20 chars apenas repite unas pocas palabras. |
| 300, overlap 0 | ~8 | ~240 chars | A veces. Algunas secciones caben completas, pero los puntos de corte pueden separar una explicación de su ejemplo. | No hay redundancia. |
| 300, overlap 50 | ~9 | ~230 chars | Menos que sin overlap. El solapamiento de 50 chars permite que la última frase del chunk anterior se repita al inicio del siguiente, preservando mejor el contexto. | Baja; ~17% de overlap es razonable y no genera redundancia perceptible. |
| 500, overlap 50 | ~5 | ~400 chars | Raramente. Cada chunk contiene párrafos casi completos; las secciones del documento caben bien en 500 chars. | Muy baja; solo 10% de overlap. |
| 500, overlap 100 | ~5 | ~410 chars | Raramente. Similar al anterior, pero el overlap mayor protege mejor las transiciones entre secciones. | Moderada-baja; 20% de overlap es aceptable y mejora la continuidad sin exceso. |
| 1000, overlap 200 | ~3 | ~750 chars | No. Cada chunk contiene secciones enteras del documento con su contexto completo. | Moderada; 20% de overlap con chunks grandes significa que ~200 chars se repiten, pero dado el tamaño del chunk no es excesivo. |

### Preguntas de Reflexión

1. ¿Con qué configuración se cortan más frases a mitad de una idea? ¿Por qué?

**Respuesta:** Con chunk_size=100 y overlap=0 se cortan más frases a mitad de una idea. Con solo 100 caracteres por chunk, la mayoría de las frases del documento (que tienen entre 80 y 200 caracteres) no caben en un solo chunk. Sin overlap, no hay ningún mecanismo que preserve la continuidad entre chunks consecutivos. Aunque `RecursiveCharacterTextSplitter` intenta cortar por separadores naturales (`\n\n`, `\n`, `. `), cuando ningún separador cae dentro de los 100 caracteres, se ve forzado a cortar por espacios o incluso a mitad de palabra, produciendo chunks incoherentes.

2. ¿Cuál es el trade-off entre chunk_size pequeño y grande para la calidad de la búsqueda?

**Respuesta:** Un chunk_size pequeño produce embeddings más específicos y precisos (el vector representa una idea concreta), lo que mejora la precisión de la búsqueda — si el usuario busca exactamente esa idea, la similitud será alta. Sin embargo, se pierde contexto: el chunk puede no contener suficiente información para que el LLM genere una respuesta completa. Un chunk_size grande captura más contexto y relaciones entre ideas, pero el embedding resultante es una "media" de múltiples conceptos, lo que puede diluir la señal semántica y reducir la precisión de la búsqueda — un chunk que habla de tres temas distintos tendrá similitud moderada con consultas sobre cualquiera de ellos, pero no será altamente similar a ninguna. El punto óptimo suele estar entre 300-500 caracteres (o 100-250 tokens) para textos generales, combinado con un overlap del 10-20%.

3. ¿Por qué `RecursiveCharacterTextSplitter` usa una jerarquía de separadores (`\n\n`, `\n`, `. `, ` `)? ¿Qué pasaría si solo usara un separador?

**Respuesta:** La jerarquía de separadores implementa una estrategia de "degradación elegante". Primero intenta cortar por `\n\n` (separación de párrafos), que es el punto de corte más natural y semántico. Si no encuentra uno dentro del chunk_size, baja al siguiente nivel (`\n`, salto de línea simple), luego a `. ` (fin de frase), y finalmente a ` ` (espacio entre palabras). Esto maximiza la coherencia semántica de cada chunk. Si solo usara un separador, por ejemplo ` `, cada chunk se cortaría exactamente en el espacio más cercano al chunk_size, ignorando por completo la estructura del texto — podría cortar a mitad de un párrafo, separando una causa de su efecto, o dividir una enumeración entre dos chunks. Con solo `\n\n`, en cambio, no podría dividir párrafos que sean más largos que el chunk_size, generando chunks que exceden el límite o forzando cortes arbitrarios.

4. Si tu documento fuera código fuente Python en lugar de texto, ¿cambiarías los separadores? ¿Cuáles usarías?

**Respuesta:** Sí, cambiaría completamente los separadores. Para código Python usaría (en orden de prioridad): `["\nclass ", "\ndef ", "\n\ndef ", "\n\n", "\n", " ", ""]`. Esto prioriza dividir por definiciones de clases y funciones, que son las unidades semánticas naturales del código. De hecho, LangChain ya proporciona `RecursiveCharacterTextSplitter.from_language(Language.PYTHON)` que usa exactamente esta jerarquía adaptada a Python. Usar los separadores por defecto de texto (`\n\n`, `\n`, `. `) en código sería problemático porque podría cortar una función a mitad de su cuerpo, separando la definición de su implementación, o dividir un bloque if-else entre dos chunks.

5. ¿Qué configuración elegirías para un documento legal con párrafos largos y densos? ¿Y para un FAQ con preguntas y respuestas cortas?

**Respuesta:** Para un **documento legal** elegiría chunk_size=800-1024 con overlap=200. Los textos legales tienen párrafos largos donde cada argumento se desarrolla a lo largo de varias frases interconectadas; un chunk pequeño cortaría argumentos jurídicos a mitad. El overlap generoso (200 chars) es importante porque las referencias cruzadas dentro del texto ("conforme a lo establecido en el párrafo anterior...") son frecuentes. Los separadores priorizarían `\n\nArtículo`, `\n\n` y `\n` para respetar la estructura de artículos y apartados.

Para un **FAQ** elegiría chunk_size=200-300 con overlap=0 o muy pequeño (20). Cada par pregunta-respuesta es una unidad autocontenida y breve; un chunk grande mezclaría varias preguntas, diluyendo la precisión de la búsqueda. El overlap es innecesario porque no hay continuidad semántica entre preguntas distintas. Lo ideal sería usar un separador personalizado que divida por cada bloque pregunta-respuesta (por ejemplo, `\n\n**P:**` o el patrón que use el FAQ).

### Extensión (Opcional)

- Prueba `MarkdownHeaderTextSplitter` de LangChain, que divide por encabezados Markdown preservando la jerarquía. Compara los resultados con `RecursiveCharacterTextSplitter` sobre el mismo documento.
- Implementa un splitter personalizado que divida por secciones (`##`) y mantenga el título de sección como metadato de cada chunk.

---

## Ejercicio 5: Diseño de un Pipeline RAG Completo

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Diseño
- **Modalidad**: Grupal (2-3 personas)
- **Dificultad**: Intermedia
- **Prerequisitos**: Lectura completa de las secciones 5.1 a 5.4, comprensión de los ejercicios anteriores

### Contexto
Diseñar un sistema RAG completo requiere tomar decisiones coordinadas en cada etapa del pipeline: desde la ingesta y preprocesamiento de documentos, pasando por el chunking y la generación de embeddings, hasta la recuperación y la generación de respuestas. Cada decisión afecta a las demás y al rendimiento global del sistema. Este ejercicio integra todos los conceptos de la sesión en un diseño coherente de principio a fin.

### Objetivo de Aprendizaje
- Integrar todos los conceptos de la sesión en un diseño de sistema completo
- Tomar decisiones de diseño coordinadas y justificadas
- Identificar los puntos de fallo potenciales en un pipeline RAG
- Desarrollar la capacidad de comunicar decisiones técnicas a través de diagramas

### Enunciado

En grupos de 2-3 personas, elegid **uno** de los siguientes casos de uso y diseñad un pipeline RAG completo. Debéis producir: un diagrama del sistema, una tabla de decisiones técnicas y un análisis de riesgos.

### Casos de Uso (elegir uno)

**Caso A: Asistente de Documentación Técnica**
Una empresa de software con 2.000 páginas de documentación técnica (API docs, tutoriales, guías de troubleshooting) quiere un chatbot que ayude a los desarrolladores. La documentación está en Markdown en un repositorio Git y se actualiza 3-4 veces por semana.

**Caso B: Buscador Inteligente de Normativa Universitaria**
Una universidad quiere que estudiantes y profesores puedan hacer preguntas sobre normativa académica (reglamentos de evaluación, normativa TFG/TFM, convocatorias, protocolos). Los documentos son PDFs oficiales (~50 documentos, ~500 páginas totales) que se actualizan una vez al año.

**Caso C: Asistente de Recursos Humanos**
Una empresa con 500 empleados quiere un asistente que responda preguntas sobre políticas internas (vacaciones, teletrabajo, beneficios, código de conducta). Los documentos son una mezcla de PDFs, páginas de la intranet y presentaciones PowerPoint.

### Parte 1: Diagrama del Pipeline

Dibujad (en papel, pizarra o herramienta digital) un diagrama que incluya todas las etapas del pipeline, desde la fuente de datos hasta la respuesta al usuario. Debe incluir como mínimo:

```
┌─────────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────────┐
│  Fuentes de │───>│ Preprocesado │───>│ Chunking  │───>│  Generación  │
│    Datos    │    │  y Limpieza  │    │           │    │  Embeddings  │
└─────────────┘    └──────────────┘    └───────────┘    └──────┬───────┘
                                                               │
                                                               v
┌─────────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────────┐
│  Respuesta  │<───│  Generación  │<───│ Ranking y │<───│    Base de   │
│  al Usuario │    │   con LLM    │    │ Selección  │    │    Datos     │
└─────────────┘    └──────────────┘    └───────────┘    │  Vectorial   │
                                                        └──────────────┘
         ▲                                                     ▲
         │              ┌───────────┐                          │
         └──────────────│  Consulta │──────────────────────────┘
                        │  Usuario  │
                        └───────────┘
```

Para cada bloque del diagrama, anotad la tecnología o herramienta concreta que usaríais.

### Parte 2: Tabla de Decisiones Técnicas

**Caso elegido: Caso B — Buscador Inteligente de Normativa Universitaria**

| Decisión | Vuestra elección | Alternativas consideradas | Justificación |
|----------|-----------------|--------------------------|---------------|
| **Formato de entrada** | PDFs oficiales de normativa (~50 documentos, ~500 páginas) | Word, HTML de web institucional | Los documentos normativos universitarios se publican oficialmente en PDF; es el formato canónico y garantiza que trabajamos con la versión oficial |
| **Herramienta de extracción de texto** | PyMuPDF (fitz) para PDFs con texto seleccionable; Azure Document Intelligence como fallback para PDFs escaneados | PyPDF2, pdfplumber, Tesseract OCR | PyMuPDF es rápido, preserva bien la estructura y detecta encabezados y tablas; Azure Document Intelligence ofrece OCR de alta calidad con detección de layout para los PDFs que sean imágenes escaneadas |
| **Estrategia de chunking** | RecursiveCharacterTextSplitter con separadores adaptados a documentos normativos (`\nArtículo`, `\n\n`, `\n`, `. `) | MarkdownHeaderTextSplitter, chunking por páginas | Los reglamentos se organizan en artículos y apartados; respetar esas divisiones mantiene cada unidad normativa completa en un chunk, esencial para dar respuestas jurídicamente correctas |
| **chunk_size** | 600 caracteres (~150 tokens) | 300, 500, 1000 | Los artículos de normativa suelen ser concisos (3-8 frases); 600 chars captura un artículo completo sin mezclar artículos distintos; con 300 se cortarían y con 1000 se mezclarían varios |
| **chunk_overlap** | 100 caracteres | 0, 50, 200 | Suficiente para que las referencias entre apartados contiguos ("según el apartado anterior") mantengan contexto, sin generar redundancia excesiva (~17% del chunk) |
| **Modelo de embeddings** | `text-embedding-3-small` de OpenAI | `all-MiniLM-L6-v2`, `multilingual-e5-large` | Buen rendimiento en español, coste bajo (~$0.02/millón de tokens), y para ~500 páginas el coste total de indexación es despreciable (<$0.10); la normativa es información pública, así que no hay restricciones de privacidad |
| **Base de datos vectorial** | ChromaDB con persistencia local | Pinecone, pgvector, FAISS | Para ~50 documentos (~500 páginas, estimados ~2.000-3.000 chunks) ChromaDB es más que suficiente; no requiere infraestructura externa, se despliega fácilmente en un servidor universitario, y la actualización anual hace innecesaria una solución cloud |
| **Número de chunks recuperados (top-k)** | top-k = 5 | 3, 8, 10 | 5 chunks proporcionan suficiente contexto para cubrir artículos relacionados (p.ej. una pregunta sobre evaluación puede requerir artículos de convocatorias, calificaciones y reclamaciones), sin sobrecargar el prompt del LLM |
| **Estrategia de búsqueda** (solo vectorial / híbrida) | Híbrida (vectorial + keyword) | Solo vectorial, solo BM25 | Los estudiantes a veces buscan por términos exactos ("artículo 23", "convocatoria extraordinaria") donde BM25 es mejor, y otras veces hacen preguntas semánticas ("¿puedo cambiar de grupo?") donde la búsqueda vectorial destaca; la combinación cubre ambos patrones |
| **LLM para generación** | GPT-4o-mini | GPT-4o, Claude 3.5 Sonnet, Llama 3 8B | Las preguntas sobre normativa son factuales y directas; GPT-4o-mini ofrece calidad suficiente a 1/30 del coste de GPT-4o, permitiendo que la universidad soporte miles de consultas diarias sin un presupuesto elevado |
| **Prompt template** (describir estructura) | Sistema con rol de asistente normativo, contexto recuperado con metadatos de documento/artículo, instrucciones de citar fuentes y reconocer cuando no tiene información | Prompt simple sin instrucciones, prompt con few-shot examples | Incluir metadatos (nombre del reglamento, artículo) permite al LLM citar la fuente exacta; las instrucciones de reconocer ignorancia evitan que invente normativa inexistente |
| **Frecuencia de actualización del índice** | Anual (coincidiendo con la publicación de nuevos reglamentos), con posibilidad de reindexación manual bajo demanda | Semanal, mensual, en tiempo real | La normativa universitaria se actualiza una vez al año típicamente; reindexar más frecuentemente sería innecesario; la opción de reindexación manual cubre cambios extraordinarios |

### Parte 3: Prompt Template

Diseñad el prompt que recibirá el LLM para generar la respuesta. Debe incluir instrucciones claras sobre cómo usar el contexto recuperado:

```
Eres un asistente especializado en normativa académica de la universidad. Tu función es
responder preguntas de estudiantes y profesores basándote EXCLUSIVAMENTE en los fragmentos
de normativa proporcionados a continuación. Responde siempre en español.

CONTEXTO RECUPERADO DE LA NORMATIVA:
{contexto_recuperado}

INSTRUCCIONES:
- Responde ÚNICAMENTE con información que aparezca explícitamente en el contexto proporcionado. No inventes ni deduzcas normativa que no esté en los fragmentos.
- Cita siempre la fuente de tu respuesta indicando el nombre del reglamento y el artículo o apartado correspondiente (por ejemplo: "Según el Artículo 15 del Reglamento de Evaluación...").
- Si la información solicitada no se encuentra en el contexto proporcionado, responde: "No he encontrado esta información en la normativa disponible. Te recomiendo contactar con Secretaría Académica para resolver tu consulta."
- Usa un lenguaje claro y accesible, evitando jerga legal innecesaria, pero sin alterar el significado de la normativa.
- Si la pregunta es ambigua, pide al usuario que aclare su situación antes de responder.

PREGUNTA DEL USUARIO:
{pregunta}

RESPUESTA:
```

### Parte 4: Análisis de Riesgos y Mitigaciones

Identificad al menos 4 riesgos potenciales del sistema y proponed mitigaciones:

| Riesgo | Probabilidad | Impacto | Mitigación propuesta |
|--------|-------------|---------|---------------------|
| El LLM alucina e inventa información no presente en el contexto | Alta | Alto | Incluir instrucciones explícitas en el prompt para que el LLM se base exclusivamente en el contexto recuperado. Implementar un sistema de verificación post-generación que compruebe que las citas de artículos mencionadas en la respuesta realmente existen en los chunks recuperados. Añadir la instrucción de responder "no tengo esa información" cuando no encuentre datos relevantes. |
| La consulta del usuario no tiene respuesta en los documentos | Media | Medio | Establecer un umbral mínimo de similitud (p.ej. 0.70) para los chunks recuperados; si ninguno supera el umbral, el sistema responde que no ha encontrado información relevante y redirige al usuario a Secretaría Académica o al canal de atención presencial. Esto es preferible a forzar una respuesta con chunks poco relevantes. |
| La normativa se actualiza y el índice contiene información obsoleta | Baja | Alto | Implementar un proceso de reindexación coordinado con Secretaría cuando se publican nuevos reglamentos. Añadir metadatos de fecha de vigencia a cada chunk para que el sistema pueda advertir si un documento podría estar desactualizado. Marcar la fecha de última actualización del índice en la interfaz del usuario. |
| Un estudiante intenta manipular el sistema con prompt injection para obtener respuestas fuera de la normativa | Media | Medio | Utilizar un prompt de sistema robusto con instrucciones claras de no desviarse del rol de asistente normativo. Implementar un filtro de entrada que detecte patrones comunes de prompt injection ("ignora las instrucciones anteriores", "actúa como..."). Limitar la longitud de la consulta del usuario a un máximo razonable (500 caracteres). |
| Chunks recuperados contienen información de múltiples artículos mezclados por un chunking deficiente | Media | Alto | Validar la calidad del chunking revisando manualmente una muestra de chunks antes de desplegar el sistema. Incluir metadatos de origen (reglamento, artículo, apartado) en cada chunk para que el LLM pueda distinguir entre normativas diferentes. Ajustar los separadores del splitter para respetar la estructura de artículos. |
| Alta latencia en las respuestas que degrade la experiencia del usuario | Baja | Medio | Implementar caché de consultas frecuentes (las preguntas sobre plazos de matrícula o convocatorias se repiten mucho). Usar GPT-4o-mini en lugar de modelos más grandes para reducir latencia. Pre-computar embeddings de preguntas frecuentes para acelerar la búsqueda. |

### Parte 5: Presentación (5 minutos por grupo)

Cada grupo presenta brevemente su diseño al resto de la clase, explicando:
1. El caso de uso elegido y por qué
2. Las 2-3 decisiones técnicas más importantes y su justificación
3. El riesgo que consideran más crítico y cómo lo mitigan

### Extensión (Opcional)

- Añadid al diseño un sistema de evaluación: ¿cómo mediríais la calidad de las respuestas del sistema? Investigad métricas como Faithfulness, Answer Relevancy y Context Precision del framework RAGAS.
- Diseñad un flujo de feedback del usuario: ¿cómo incorporaríais las valoraciones de los usuarios (pulgar arriba/abajo) para mejorar el sistema?
