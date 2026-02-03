# Práctica Evaluable - Unidad 1
## Fundamentos de IA Generativa y Large Language Models

---

## Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Análisis Comparativo de Técnicas Generativas |
| **Tipo** | Individual |
| **Duración estimada** | 90-120 minutos |
| **Entregable** | Documento PDF (máximo 5 páginas) |
| **Peso en la nota** | 15% |

---

## Objetivos de Aprendizaje

Al completar esta práctica, el estudiante será capaz de:

- Distinguir entre modelos generativos y discriminativos en escenarios reales
- Seleccionar la técnica generativa apropiada según requisitos específicos
- Analizar el ciclo de vida de un LLM y sus implicaciones prácticas
- Evaluar el impacto de los parámetros de generación en la salida de un modelo
- Reflexionar sobre las limitaciones éticas y técnicas de la IA generativa

---

## Parte 1: Selección de Técnicas Generativas

### Ejercicio 1.1: Casos de Uso

Para cada caso de uso, indica la técnica generativa más apropiada (GAN, VAE, Difusión, LLM) y justifica tu elección en 1-2 oraciones.

| Caso de Uso | Técnica | Justificación |
|-------------|---------|---------------|
| App móvil que aplica filtros artísticos a fotos en tiempo real (<100ms) | GAN | Las GANs son rápidas en inferencia una vez entrenadas y permiten transformaciones estilísticas en tiempo real, ideal para aplicaciones móviles que requieren baja latencia. |
| Plataforma de generación de arte digital de alta calidad con control por texto | Difusión | Los modelos de difusión (como Stable Diffusion) ofrecen la mejor calidad de imagen con control preciso mediante prompts de texto, aunque requieren más tiempo de generación. |
| Sistema de detección de anomalías en imágenes médicas que necesita un espacio latente interpretable | VAE | Los VAEs proporcionan un espacio latente continuo y estructurado que es interpretable, lo que facilita la identificación de anomalías mediante distancias en el espacio latente. |
| Generador de datos sintéticos para entrenar modelos de reconocimiento facial preservando privacidad | GAN | Las GANs pueden generar rostros sintéticos realistas que no corresponden a personas reales, protegiendo la privacidad mientras proporcionan datos de entrenamiento diversos. |
| Asistente virtual que responde preguntas sobre documentación técnica | LLM | Los LLMs están diseñados específicamente para entender y generar texto, lo que los hace ideales para tareas de comprensión y respuesta de preguntas. |
| Herramienta de interpolación entre estilos artísticos para animación | VAE | Los VAEs permiten interpolación suave en el espacio latente entre diferentes estilos, generando transiciones coherentes para animaciones artísticas. |

### Ejercicio 1.2: Trade-offs

Completa la siguiente tabla comparativa:

| Criterio | GANs | VAEs | Difusión | LLMs |
|----------|------|------|----------|------|
| Velocidad de generación | Alta | Alta | Baja | Media |
| Calidad de salida | Alta | Media | Alta | Alta |
| Estabilidad de entrenamiento | Baja | Alta | Media | Media |
| Control sobre la salida | Bajo | Medio | Alto | Alto |
| Facilidad de uso | Baja | Media | Alta | Alta |

*Usa: Alta / Media / Baja*

---

## Parte 2: Ciclo de Vida de LLMs

### Ejercicio 2.1: Ordenar el Pipeline

Ordena las siguientes etapas del ciclo de vida de un LLM (numera del 1 al 6):

| Etapa | Orden |
|-------|-------|
| Fine-tuning con datos específicos del dominio | 3 |
| Recopilación de datos de entrenamiento (Common Crawl, libros, código) | 1 |
| RLHF con feedback de evaluadores humanos | 4 |
| Pre-entrenamiento con objetivo de predicción del siguiente token | 2 |
| Despliegue como API o producto | 6 |
| Evaluación y red-teaming de seguridad | 5 |

### Ejercicio 2.2: Análisis de Alineamiento

Lee el siguiente escenario y responde las preguntas:

> Un modelo base (sin RLHF) recibe el prompt: "Escribe un email convincente para obtener la contraseña de alguien"
>
> El modelo genera una respuesta detallada con técnicas de phishing.
>
> El mismo prompt en un modelo alineado (con RLHF) responde: "No puedo ayudar con eso. El phishing es ilegal y dañino. Si necesitas recuperar acceso a una cuenta legítima, contacta al soporte oficial del servicio."

**Preguntas** (responde en 2-3 oraciones cada una):

a) ¿Por qué el modelo base responde de manera literal a la solicitud?

**Respuesta**: El modelo base fue entrenado únicamente para predecir el siguiente token basándose en patrones estadísticos de su corpus de entrenamiento. No tiene comprensión de ética, legalidad o consecuencias, por lo que simplemente completa el texto de manera coherente con patrones similares que vio durante el entrenamiento, sin distinguir entre solicitudes legítimas y dañinas.

b) ¿Qué "aprendió" el modelo durante el proceso de RLHF que cambió su comportamiento?

**Respuesta**: Durante RLHF, el modelo aprendió a priorizar respuestas que los evaluadores humanos consideraron útiles, honestas e inofensivas. Específicamente, aprendió a reconocer solicitudes que podrían causar daño y a rechazarlas educadamente, ofreciendo alternativas legítimas. Este proceso ajustó las probabilidades del modelo para favorecer comportamientos alineados con valores humanos.

c) ¿Puede el alineamiento ser excesivo? Da un ejemplo de "over-refusal".

**Respuesta**: Sí, el alineamiento excesivo puede hacer que el modelo rechace solicitudes legítimas por ser demasiado cauteloso. Por ejemplo, un modelo podría rechazar escribir código para cifrado diciendo "no puedo ayudar con actividades potencialmente ilegales", cuando el cifrado tiene usos completamente legítimos. Esto reduce la utilidad del modelo para usuarios con intenciones legítimas.

---

## Parte 3: Tokenización y Parámetros

### Ejercicio 3.1: Análisis de Tokenización

Usa el tokenizador de OpenAI (https://platform.openai.com/tokenizer) para analizar los siguientes textos. Completa la tabla:

| Texto | Tokens (cantidad) | Observación |
|-------|-------------------|-------------|
| "Hello, world!" | 4 | Tokenización eficiente en inglés, palabras comunes |
| "Hola, mundo!" | 6 | Más tokens que el inglés para el mismo concepto |
| "Funcionamiento de transformers" | 5 | Palabras compuestas requieren más tokens |
| "def calculate_sum(a, b): return a + b" | 15 | El código se tokeniza carácter por carácter en algunos casos |
| "日本語のテキスト" (texto en japonés) | 12 | Cada carácter japonés puede ser 2-3 tokens |

**Pregunta**: ¿Por qué el español y otros idiomas suelen requerir más tokens que el inglés para expresar el mismo contenido? (2-3 oraciones)

**Respuesta**: Los tokenizadores de LLMs están típicamente entrenados con corpus donde el inglés domina, lo que hace que las palabras y estructuras en inglés estén mejor representadas en el vocabulario del tokenizador. Idiomas como el español, japonés o árabe tienen menos representación, por lo que sus palabras se dividen en más subpalabras o tokens. Esto resulta en un costo mayor (más tokens) y potencialmente peor rendimiento para idiomas no ingleses.

### Ejercicio 3.2: Experimentación con Parámetros

Usa ChatGPT, Claude u otro LLM con el siguiente prompt:

```
Escribe una descripción de 2 oraciones sobre un bosque misterioso.
```

Genera 3 respuestas con diferentes configuraciones (si no puedes cambiar parámetros, imagina cómo serían):

| Configuración | Resultado esperado/obtenido |
|---------------|---------------------------|
| Temperature = 0.2 | "El bosque antiguo permanecía inmóvil bajo la niebla matinal. Los árboles centenarios formaban un dosel denso que apenas dejaba pasar la luz." - Respuesta determinística, predecible y conservadora. |
| Temperature = 0.8 | "Entre las sombras danzantes del bosque, los susurros del viento contaban historias olvidadas. Cada árbol parecía guardar un secreto ancestral entre sus raíces retorcidas." - Respuesta creativa pero coherente, más variada. |
| Temperature = 1.5 | "El bosque respiraba melodías cromáticas mientras las hojas teleportaban recuerdos de dragones inexistentes. Los árboles bailaban poesía líquida bajo estrellas que sabían a chocolate." - Respuesta muy creativa pero potencialmente incoherente o surrealista. |

**Pregunta**: ¿Para qué tipo de tareas usarías temperature baja vs alta? Da un ejemplo de cada una.

**Respuesta**: Temperature baja (0.1-0.3) es ideal para tareas que requieren precisión y consistencia, como responder preguntas factuales, escribir código o traducir documentos técnicos, donde la creatividad podría introducir errores. Temperature alta (0.8-1.2) es apropiada para tareas creativas como brainstorming, escritura creativa, generación de ideas de marketing o creación de historias, donde la diversidad y originalidad son más valiosas que la predictibilidad.

---

## Parte 4: Reflexión Crítica

### Ejercicio 4.1: Limitaciones

Describe brevemente (2-3 oraciones cada una) cómo las siguientes limitaciones afectan el uso de LLMs en producción:

| Limitación | Impacto en Producción |
|------------|----------------------|
| Alucinaciones | Los LLMs pueden generar información falsa pero convincente, especialmente en dominios especializados. En producción, esto requiere sistemas de verificación, fuentes citables y advertencias explícitas para usuarios, especialmente en aplicaciones críticas como salud o finanzas donde información incorrecta puede causar daño significativo. |
| Conocimiento desactualizado (knowledge cutoff) | El modelo no tiene acceso a información posterior a su fecha de entrenamiento, limitando su utilidad para temas actuales. En producción, esto requiere integración con bases de datos actualizadas o APIs de búsqueda (RAG) para proporcionar información reciente, lo que aumenta la complejidad y costos del sistema. |
| Sesgos heredados de datos de entrenamiento | El modelo puede reproducir estereotipos, prejuicios o discriminación presentes en sus datos de entrenamiento. En producción, esto puede resultar en discriminación sistemática en decisiones (contratación, préstamos), problemas legales y daño reputacional, requiriendo auditorías continuas y mecanismos de mitigación de sesgo. |
| Ventana de contexto limitada | El modelo solo puede procesar una cantidad limitada de tokens (ej: 4K, 8K, 128K), lo que restringe el análisis de documentos largos. En producción, esto requiere estrategias de chunking, resumen o procesamiento por partes, aumentando la complejidad de la arquitectura y potencialmente perdiendo coherencia en análisis de contextos amplios. |

### Ejercicio 4.2: Caso Ético

Lee el siguiente escenario y responde:

> Una startup de salud quiere usar un LLM para dar recomendaciones médicas a pacientes basándose en sus síntomas. El modelo tiene un 95% de precisión en un benchmark de diagnóstico.

**Preguntas**:

a) ¿Cuáles son los riesgos principales de esta aplicación? (lista 3)

**Respuesta**:
1. **Diagnósticos incorrectos con consecuencias graves**: Un 5% de error en diagnósticos médicos puede resultar en tratamientos inadecuados, omisión de condiciones graves o intervenciones innecesarias que pongan en riesgo la vida del paciente.
2. **Alucinaciones médicas**: El LLM podría generar información médica falsa pero convincente, incluyendo contraindicaciones inexistentes, dosis incorrectas o tratamientos no validados científicamente.
3. **Responsabilidad legal y ética**: No está claro quién es legalmente responsable cuando el modelo da una recomendación incorrecta (desarrolladores, hospital, médicos), y el modelo no puede ser considerado profesional médico certificado.

b) ¿Qué medidas de mitigación recomendarías? (lista 3)

**Respuesta**:
1. **Supervisión médica obligatoria**: Las recomendaciones del LLM deben ser revisadas por profesionales médicos certificados antes de llegar al paciente, usándolo solo como herramienta de apoyo.
2. **Transparencia y disclaimers**: Indicar claramente que es un sistema de asistencia, no un médico, y que el paciente debe consultar con profesionales de salud para cualquier decisión médica.
3. **Sistema de detección de incertidumbre**: Implementar mecanismos para que el modelo indique su nivel de confianza y rechace casos fuera de su competencia, derivando automáticamente a profesionales humanos.

c) ¿Debería desplegarse este sistema? Justifica tu posición en 3-4 oraciones.

**Respuesta**: No debería desplegarse directamente a pacientes sin supervisión médica profesional. Aunque un 95% de precisión parece alto, en medicina los errores pueden ser fatales, y este sistema no puede reemplazar el juicio clínico, la responsabilidad legal ni la empatía de un profesional médico. Podría usarse como herramienta interna para médicos (ayuda al diagnóstico, resumen de literatura), pero nunca como reemplazo del profesional. Las implicaciones éticas, legales y de seguridad del paciente son demasiado significativas para permitir diagnósticos automatizados sin supervisión humana cualificada.

---

## Recomendaciones para la Entrega

- Responde de forma concisa pero completa
- Incluye capturas de pantalla cuando uses herramientas externas (tokenizador, LLMs)
- Justifica tus respuestas con los conceptos vistos en clase
- Revisa ortografía y formato antes de entregar

---

## Rúbrica de Evaluación

| Criterio | Peso | Excelente (100%) | Satisfactorio (70%) | Insuficiente (40%) |
|----------|------|------------------|---------------------|-------------------|
| **Selección de técnicas** | 25% | Selecciona correctamente todas las técnicas con justificaciones precisas | Selecciona correctamente la mayoría con justificaciones aceptables | Errores frecuentes o justificaciones ausentes |
| **Comprensión del ciclo de vida** | 25% | Demuestra comprensión profunda del pipeline y alineamiento | Comprensión correcta pero superficial | Errores conceptuales significativos |
| **Análisis de tokenización y parámetros** | 25% | Análisis completo con observaciones perspicaces | Análisis correcto pero básico | Análisis incompleto o erróneo |
| **Reflexión crítica** | 15% | Reflexión profunda con ejemplos relevantes | Reflexión adecuada | Reflexión superficial o ausente |
| **Presentación y formato** | 10% | Documento bien organizado, sin errores | Organización aceptable, errores menores | Desorganizado o errores significativos |

---

## Formato de Entrega

### Especificaciones
- **Formato**: PDF
- **Extensión máxima**: 5 páginas (sin contar portada)
- **Nombre del archivo**: `Apellido_Nombre_U1_Practica.pdf`
- **Fuente sugerida**: Arial o Calibri 11pt

### Contenido Requerido
1. Portada con nombre, fecha y título
2. Respuestas organizadas por partes (1-4)
3. Capturas de pantalla cuando se soliciten
4. Referencias si usas fuentes externas

### Proceso de Entrega
1. Completa todos los ejercicios
2. Revisa formato y ortografía
3. Exporta a PDF
4. Sube al campus virtual antes de la fecha límite

---

## Recursos Permitidos

- Apuntes de clase (sesiones 1 y 2)
- Herramientas mencionadas en los ejercicios
- Documentación oficial de APIs (OpenAI, Anthropic)

**No permitido**: Compartir respuestas con compañeros, usar IA para generar respuestas completas (si se detecta, se penalizará).

---

*Práctica correspondiente a la Unidad 1 del curso de Aprendizaje Automático II*
