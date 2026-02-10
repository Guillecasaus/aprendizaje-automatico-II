# Ejercicios Prácticos Tema 3 - Unidad 2, Sesión 1
## Fundamentos de Prompt Engineering

---

## Ejercicio 1: Anatomía de un Prompt

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de teoría sobre componentes del prompt

### Contexto
Antes de crear buenos prompts, es importante reconocer los componentes en prompts existentes.

### Objetivo de Aprendizaje
- Identificar los componentes de un prompt (rol, contexto, tarea, formato, restricciones)
- Evaluar la completitud de un prompt

### Enunciado
Analiza los siguientes prompts e identifica sus componentes. Indica qué componentes faltan y como los mejorarías.

### Prompt A
```
Eres un experto en marketing digital especializado en startups tecnológicas.

Contexto: Nuestra startup vende software de gestión de proyectos para equipos remotos.
Acabamos de lanzar una nueva funcionalidad de videoconferencias integradas.

Tarea: Escribe 3 posts para LinkedIn anunciando esta funcionalidad.

Formato:
- Cada post debe tener entre 100-150 palabras
- Incluir un emoji relevante al inicio
- Terminar con un call-to-action

No menciones competidores ni uses jerga demasiado técnica.
```

### Prompt B
```
Dame ideas para mejorar mi aplicación
```

### Prompt C
```
Traduce este texto al inglés y hazlo más formal:

"""
Hola! Queria saber si podemos quedar mañana para hablar del proyecto.
Avisame cuando puedas.
"""
```

### Tabla de Análisis

Completa la siguiente tabla para cada prompt:

| Componente | Prompt A | Prompt B | Prompt C |
|------------|----------|----------|----------|
| Rol | Presente: Experto en marketing digital para startups | No especificado | No especificado |
| Contexto | Presente: Startup de software de gestión, nueva funcionalidad de videoconferencias | No proporcionado | Implícito: texto a traducir |
| Tarea | Presente: Escribir 3 posts para LinkedIn | Vago: "dame ideas" | Presente: Traducir y hacer más formal |
| Formato | Presente: Longitud, estructura con emoji y CTA | No especificado | Parcial: formato de salida implícito |
| Restricciones | Presente: No mencionar competidores ni jerga técnica | Ninguna | Ninguna explícita |
| Ejemplos | No incluye | No incluye | Presente: Incluye el texto a traducir |
| **Evaluación (1-10)** | **9/10** | **2/10** | **6/10** |

### Preguntas de Reflexión
1. **¿Cuál de los tres prompts producirá mejores resultados? ¿Por qué?**

   El Prompt A producirá los mejores resultados porque incluye todos los componentes esenciales: rol específico, contexto detallado, tarea clara, formato estructurado y restricciones explícitas. Esto guía al modelo de manera precisa, reduciendo ambigüedad y aumentando la relevancia del output.

2. **¿Qué añadirías al Prompt B para hacerlo efectivo?**

   - **Rol**: "Eres un consultor de producto especializado en UX/UI"
   - **Contexto**: Detalles de la aplicación (tipo, usuarios, problemas actuales)
   - **Formato**: "Proporciona 5 ideas específicas en formato bullet point"
   - **Restricciones**: "Enfócate en mejoras que se puedan implementar en menos de 1 mes"
   - **Ejemplos**: Proporcionar un ejemplo del tipo de sugerencia esperada

3. **¿El Prompt C necesita rol? ¿Por qué sí o por qué no?**

   Depende del contexto de uso. Para traducciones simples no es crítico, pero añadir un rol como "Eres un traductor profesional especializado en correspondencia empresarial" mejoraría la calidad, especialmente para el aspecto de formalización. El rol ayudaría a mantener el tono apropiado y utilizar terminología adecuada al contexto corporativo.

---

## Ejercicio 2: Zero-shot vs Few-shot

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Experimentación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Acceso a ChatGPT, Claude o Gemini

### Contexto
Comparar el rendimiento de diferentes técnicas de prompting en una tarea de clasificación.

### Objetivo de Aprendizaje
- Experimentar con zero-shot y few-shot prompting
- Comparar resultados y entender cuándo usar cada técnica

### Enunciado
Vas a clasificar sentimientos de reseñas de productos usando tres enfoques diferentes.

### Parte A: Zero-shot (10 min)

Usa el siguiente prompt con 5 reseñas de prueba:

```
Clasifica el sentimiento de la siguiente reseña como: Positivo, Negativo o Neutro.

Reseña: "[INSERTAR RESEÑA]"

Sentimiento:
```

**Reseñas de prueba:**
1. "Excelente producto, superó mis expectativas. Lo recomiendo totalmente."
2. "No funciona como esperaba. Devolución solicitada."
3. "Esta bien para el precio. Hace lo que promete, nada más."
4. "Llegó rápido pero la caja estaba dañada. El producto funciona correctamente."
5. "HORRIBLE. Peor compra de mi vida. NO COMPREN."

### Parte B: Few-shot (15 min)

Crea un prompt few-shot con 3 ejemplos (uno por categoría) y pruebalo con las mismas reseñas:

```
Clasifica el sentimiento de reseñas de productos.

Ejemplos:
Reseña: "[Tu ejemplo positivo]"
Sentimiento: Positivo

Reseña: "[Tu ejemplo negativo]"
Sentimiento: Negativo

Reseña: "[Tu ejemplo neutro]"
Sentimiento: Neutro

Ahora clasifica:
Reseña: "[RESEÑA DE PRUEBA]"
Sentimiento:
```

### Parte C: Comparación (5 min)

Completa la tabla:

| Reseña | Zero-shot | Few-shot | ¿Coinciden? |
|--------|-----------|----------|-------------|
| 1 | Positivo | Positivo | Sí |
| 2 | Negativo | Negativo | Sí |
| 3 | Neutro | Neutro | Sí |
| 4 | Neutro / Positivo | Positivo | Puede variar |
| 5 | Negativo | Negativo | Sí |

### Preguntas
1. **¿Hubo diferencias en los resultados? ¿Cuáles?**

   La principal diferencia aparece en la reseña 4 (caso mixto). El enfoque zero-shot podría clasificarla como neutro al detectar aspectos positivos y negativos, mientras que few-shot tiende a ser más consistente siguiendo el patrón de los ejemplos. Las reseñas claras (1, 2, 5) se clasifican igual en ambos enfoques, pero los casos ambiguos muestran mayor variabilidad en zero-shot.

2. **¿La reseña 4 fue difícil de clasificar? ¿Por qué?**

   Sí, la reseña 4 es difícil porque contiene sentimientos mixtos: un aspecto negativo (caja dañada) y uno positivo (producto funciona correctamente). Esto requiere que el modelo decida qué aspecto tiene mayor peso. Sin ejemplos claros de cómo manejar estos casos, diferentes enfoques pueden producir clasificaciones distintas. En producción, esto podría requerir una categoría adicional "Mixto" o reglas de priorización.

3. **¿Qué técnica usarías en producción? ¿Por qué?**

   Usaría **few-shot** en producción por varias razones: (1) Mayor consistencia en casos ambiguos, (2) Permite definir exactamente qué criterios usar para casos edge, (3) Mejor control sobre el comportamiento del modelo, (4) Los ejemplos sirven como documentación implícita de las reglas de clasificación. El costo adicional de tokens es mínimo comparado con la mejora en confiabilidad y predictibilidad del sistema.

---

## Ejercicio 3: Desarrollo Iterativo de Prompts

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Programación/Iteración
- **Modalidad**: Parejas
- **Dificultad**: Intermedia
- **Prerequisitos**: Acceso a un LLM

### Contexto
El desarrollo iterativo es la clave del Prompt Engineering profesional. Vamos a practicar el ciclo completo.

### Objetivo de Aprendizaje
- Aplicar el proceso iterativo de mejora de prompts
- Documentar cambios y su impacto

### Enunciado
Desarrolla un prompt para generar descripciones de productos para e-commerce.

### Escenario
Trabajas en una tienda online de electrónica. Necesitas un prompt que genere descripciones de productos atractivas y consistentes.

**Producto de prueba:**
```
Nombre: EchoBuds Pro X3
Tipo: Auriculares inalambricos
Precio: 149.99€
Características:
- Cancelación de ruido activa
- 30 horas de bateria (con estuche)
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas
```

### Iteración 1: Prompt Básico

```
Escribe una descripción para este producto:
[datos del producto]
```

- Prueba el prompt y pega la respuesta
- ¿Qué problemas identificas?

### Iteración 2: Añadir Estructura

Mejora el prompt añadiendo:
- Formato de salida específico
- Longitud deseada

Documenta:
- Tu nuevo prompt
- La respuesta obtenida
- ¿Qué mejoro?

### Iteración 3: Añadir Contexto y Tono

Mejora añadiendo:
- Audiencia objetivo
- Tono de la marca
- Elementos que debe incluir (beneficios, no solo características)

### Iteración 4: Refinamiento Final

Ajusta para:
- Incluir call-to-action
- Añadir restricciones (evitar ciertas palabras, longitud exacta)
- Optimizar para SEO (si aplica)

### Entregable
Documento con:
1. Los 4 prompts (uno por iteración)
2. Las 4 respuestas obtenidas
3. Análisis de qué cambio tuvo mayor impacto
4. Tu prompt final recomendado

### Solución - Desarrollo Iterativo

**Iteración 1: Prompt Básico**
```
Escribe una descripción para este producto:
EchoBuds Pro X3 - Auriculares inalámbricos - 149.99€
- Cancelación de ruido activa
- 30 horas de batería (con estuche)
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas
```

**Respuesta obtenida:**
"Los EchoBuds Pro X3 son auriculares inalámbricos con cancelación de ruido activa, 30 horas de batería con estuche, resistencia al agua IPX5, Bluetooth 5.3 y tres tamaños de almohadillas. Precio: 149.99€."

**Problemas identificados:**
- Demasiado descriptivo, solo lista características
- No destaca beneficios
- No tiene gancho emocional
- Sin call-to-action

---

**Iteración 2: Añadir Estructura**
```
Escribe una descripción de producto para e-commerce.

Producto: EchoBuds Pro X3 - Auriculares inalámbricos - 149.99€
Características:
- Cancelación de ruido activa
- 30 horas de batería (con estuche)
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas

Formato de salida:
- Párrafo inicial atractivo (2-3 oraciones)
- Lista de características clave con viñetas
- Longitud total: 80-100 palabras
```

**Respuesta obtenida:**
"Sumérgete en tu música sin distracciones con los EchoBuds Pro X3. Estos auriculares inalámbricos ofrecen una experiencia de audio superior con tecnología de punta.

- Cancelación de ruido activa para concentración total
- 30 horas de batería con estuche de carga
- Resistencia IPX5 contra agua y sudor
- Conexión Bluetooth 5.3 estable
- 3 tamaños de almohadillas para ajuste perfecto"

**Mejora:** Estructura clara, más atractivo, pero aún falta personalización y CTA.

---

**Iteración 3: Añadir Contexto y Tono**
```
Eres un copywriter experto en e-commerce de tecnología.

Tarea: Escribe una descripción de producto que convierta visitantes en compradores.

Contexto:
- Audiencia: Profesionales jóvenes (25-40 años) que valoran calidad y productividad
- Tono: Profesional pero cercano, enfocado en beneficios
- Competencia: AirPods Pro, Sony WF-1000XM5

Producto: EchoBuds Pro X3
Precio: 149.99€
Características:
- Cancelación de ruido activa
- 30 horas de batería con estuche
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas

Formato:
- Título gancho (1 oración)
- Párrafo de beneficios (3-4 oraciones)
- Lista de características destacadas
- Longitud: 100-120 palabras

Enfócate en BENEFICIOS sobre características técnicas.
```

**Respuesta obtenida:**
"Productividad sin interrupciones, a tu alcance.

Imagina trabajar desde casa, en la oficina o en el gimnasio sin que nada te distraiga. Los EchoBuds Pro X3 eliminan el ruido del mundo exterior para que te concentres en lo que importa. Con batería para más de una semana laboral, no volverás a quedarte sin música en el momento menos oportuno. Y cuando llueve o sudas en el gym, siguen funcionando perfectamente.

- Silencia el mundo: Cancelación de ruido de nivel profesional
- Olvídate de cargar: 30h de autonomía real
- A prueba de todo: Certificación IPX5
- Conexión perfecta: Bluetooth 5.3 sin cortes
- Tu ajuste ideal: 3 tamaños incluidos"

**Mejora:** Mucho más persuasivo, enfocado en beneficios, conecta emocionalmente.

---

**Iteración 4: Refinamiento Final**
```
Eres un copywriter experto en e-commerce de tecnología especializado en páginas de producto de alta conversión.

Tarea: Escribe una descripción de producto optimizada para conversión y SEO.

Contexto:
- Audiencia: Profesionales jóvenes (25-40 años) que valoran calidad y productividad
- Tono: Profesional pero cercano, enfocado en beneficios concretos
- Objetivo: Destacar la relación calidad-precio vs competidores premium

Producto: EchoBuds Pro X3
Precio: 149.99€ (vs AirPods Pro: 279€)
Características:
- Cancelación de ruido activa
- 30 horas de batería con estuche
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas

Formato:
- Título gancho destacando propuesta de valor (1 oración, max 12 palabras)
- Párrafo persuasivo de beneficios (3-4 oraciones, usar "tú/tu")
- Lista de 4-5 características como beneficios concretos
- Call-to-action final (1 oración)
- Longitud total: exactamente 110-130 palabras

Restricciones:
- NO uses: "increíble", "revolucionario", "único"
- NO menciones marcas competidoras directamente
- Incluye términos SEO: "auriculares inalámbricos", "cancelación ruido"
- Formato para web: párrafos cortos, escaneable
```

**Respuesta final:**
"Calidad premium sin el precio premium.

¿Por qué pagar el doble por auriculares inalámbricos de alta gama? Los EchoBuds Pro X3 te ofrecen cancelación de ruido activa profesional, batería que dura toda la semana y resistencia total al agua, por menos de la mitad del precio de otras opciones premium. Perfectos para tu rutina diaria, desde el tren al gimnasio.

- Concéntrate sin distracciones: Cancelación de ruido activa de nivel profesional
- Batería para toda la semana: 30 horas reales de reproducción
- Entrena sin preocupaciones: Certificación IPX5 contra agua y sudor  
- Conexión estable siempre: Bluetooth 5.3 de última generación
- Comodidad garantizada: 3 tamaños de almohadillas incluidos

Consigue la experiencia premium que mereces por solo 149.99€."

**Análisis de impacto:**
1. **Mayor impacto: Iteración 3** - Cambiar de características a beneficios transformó completamente la persuasión
2. **Segundo impacto: Iteración 4** - Añadir propuesta de valor (precio vs competencia) y CTA específico
3. **Menor impacto: Iteración 2** - Estructura ayuda pero sin contexto no es suficiente

**Prompt final recomendado:** Iteración 4, ya que combina todos los elementos esenciales y produce copy comercialmente efectivo.

---

## Ejercicio 4: Diseño de Prompts para Casos de Uso

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Diseño
- **Modalidad**: Grupal (3-4 personas)
- **Dificultad**: Intermedia
- **Prerequisitos**: Comprensión de componentes del prompt

### Contexto
En equipos, diseñaran prompts para casos de uso empresariales reales.

### Objetivo de Aprendizaje
- Aplicar los componentes del prompt a problemas reales
- Colaborar en el diseño y crítica de prompts

### Enunciado
Cada grupo recibira un caso de uso y deberá diseñar el prompt completo.

### Caso A: Generador de Emails de Seguimiento

**Contexto del problema:**
Un equipo de ventas necesita enviar emails de seguimiento personalizados después de demos de producto.

**Input disponible:**
- Nombre del prospecto
- Empresa
- Puntos discutidos en la demo
- Objeciones mencionadas
- Siguiente paso acordado

**Output deseado:**
Email profesional, personalizado, que refuerce los puntos fuertes y aborde las objeciones.

### Caso B: Resumidor de Reuniones

**Contexto del problema:**
Un asistente que convierte transcripciones de reuniones en resumenes estructurados.

**Input disponible:**
- Transcripción de la reunión (texto largo)
- Lista de participantes

**Output deseado:**
- Resumen ejecutivo (3-5 oraciones)
- Decisiones tomadas
- Action items con responsables
- Temas pendientes

### Caso C: Revisor de Código Automatizado

**Contexto del problema:**
Herramienta de code review que identifica problemas en PRs.

**Input disponible:**
- Código fuente (diff o archivo completo)
- Lenguaje de programación
- Estandares del equipo (opcional)

**Output deseado:**
- Lista de issues encontrados
- Severidad de cada issue
- Sugerencia de corrección
- Código corregido (opcional)

### Formato de Entrega

Para cada caso, entregar:

```markdown
## Caso [A/B/C]: [Nombre]

### Prompt Diseñado

[Prompt completo con todos los componentes]

### Justificación de Decisiones

- ¿Por qué elegimos este rol?
- ¿Qué contexto incluimos y por qué?
- ¿Por qué este formato de salida?
- ¿Qué restricciones añadimos?

### Limitaciones Identificadas

- ¿Qué casos edge podrían fallar?
- ¿Qué mejoras futuras considerariamos?
```

### Solución Ejercicio 4

## Caso A: Generador de Emails de Seguimiento

### Prompt Diseñado

```
Eres un Sales Development Representative (SDR) experto con 10 años de experiencia en ventas B2B de software empresarial. Tu especialidad es escribir emails de seguimiento que mantienen el momentum sin ser intrusivos.

Contexto:
Acabas de finalizar una demo de producto con un prospecto. Necesitas enviar un email de seguimiento personalizado que refuerce los puntos fuertes discutidos, aborde las objeciones de manera constructiva y mantenga el proceso de venta avanzando.

Tarea:
Genera un email de seguimiento profesional y personalizado.

Input que recibirás:
- Nombre del prospecto: [NOMBRE]
- Empresa: [EMPRESA]
- Puntos discutidos: [LISTA]
- Objeciones mencionadas: [LISTA]
- Siguiente paso acordado: [ACCIÓN]

Formato de salida:
Asunto: [línea de asunto personalizada, max 60 caracteres]

[Saludo personalizado]

[Párrafo 1: Agradecimiento y referencia específica a algo discutido]

[Párrafo 2: Refuerzo de beneficios relevantes para sus necesidades]

[Párrafo 3: Abordaje de objeciones de forma constructiva con evidencia/datos]

[Párrafo 4: Siguiente paso claro con fecha específica]

[Despedida profesional]

Restricciones:
- Tono: Profesional pero cálido, consultivo no agresivo
- Longitud: 150-200 palabras (sin contar asunto y firma)
- NO uses: "solo quería", "disculpa por molestar", "espero no ser pesado"
- EVITA: lenguaje demasiado comercial o presión excesiva
- INCLUYE: Al menos una pregunta abierta o un dato específico mencionado en la demo
- Personalización mínima: 3 referencias específicas a la conversación

Formato técnico:
- Usar saltos de línea entre párrafos
- Negrita en fechas/acciones específicas
- Un solo call-to-action claro
```

### Justificación de Decisiones

- **¿Por qué elegimos este rol?** SDR experimentado proporciona el contexto y expertise necesarios para generar emails que balanceen persuasión con profesionalismo, evitando tono amateur o demasiado agresivo.

- **¿Qué contexto incluimos y por qué?** Contexto post-demo es crucial porque establece la relación existente y el momento del customer journey. Esto permite al modelo generar contenido apropiado para esta fase específica (no es cold email ni cierre final).

- **¿Por qué este formato de salida?** Estructura de 4 párrafos sigue best practices de sales emails: establecer rapport, reforzar valor, manejar objeciones, llamado a acción. Asunto personalizado mejora open rates. Formato técnico asegura legibilidad.

- **¿Qué restricciones añadimos?** 
  - Longitud controlada (150-200 palabras) previene emails largos que no se leen
  - Prohibición de frases débiles mantiene autoridad profesional
  - Requisito de 3 referencias personalizadas evita emails genéricos
  - Un solo CTA previene confusión sobre siguiente paso

### Limitaciones Identificadas

- **Casos edge que podrían fallar:**
  - Demos muy negativas donde no hubo engagement real
  - Objeciones fundamentales que realmente bloquean la venta (ej: "no tenemos presupuesto")
  - Prospectos que pidieron explícitamente no recibir seguimiento
  - Industrias altamente reguladas donde compliance importa (healthcare, finance)
  - Culturas empresariales muy diferentes (emails formales vs casuales)

- **Mejoras futuras:**
  - Añadir parámetro de "temperatura" de la relación (cálida/fría) para ajustar tono
  - Incluir plantilla de respuesta FAQ para objeciones comunes
  - Sistema de A/B testing de líneas de asunto
  - Integración con CRM para contexto histórico
  - Variantes por industria/sector
  - Detección de señales de compra para priorizar seguimiento

---

## Caso B: Resumidor de Reuniones

### Prompt Diseñado

```
Eres un asistente ejecutivo profesional especializado en sintetizar información de reuniones corporativas de manera clara, accionable y objetiva.

Contexto:
Trabajas en una empresa tecnológica donde el tiempo es valioso y las decisiones necesitan documentación clara. Tu tarea es convertir transcripciones largas de reuniones en resúmenes estructurados que permitan a los participantes (y ausentes) entender rápidamente qué se decidió y qué necesita hacerse.

Tarea:
Genera un resumen ejecutivo estructurado de una transcripción de reunión.

Input que recibirás:
- Transcripción: [TEXTO LARGO]
- Participantes: [LISTA DE NOMBRES]

Formato de salida:

# Resumen de Reunión
**Fecha:** [Extraer de transcripción o usar "fecha no especificada"]
**Participantes:** [Lista]
**Duración:** [Estimar basado en transcripción]

## Resumen Ejecutivo (3-5 oraciones)
[Captura la esencia: ¿de qué fue la reunión? ¿Qué se logró?]

## Decisiones Tomadas
1. [Decisión 1 - ser específico y concreto]
2. [Decisión 2]
   - Contexto adicional si relevante
[Continuar...]

## Action Items
| Tarea | Responsable | Fecha Límite | Prioridad |
|-------|-------------|--------------|----------|
| [Descripción específica] | [Nombre] | [Fecha o "No especificada"] | Alta/Media/Baja |

## Temas Pendientes / Próximos Pasos
- [Tema que quedó sin resolver]
- [Preguntas abiertas]
- [Seguimientos necesarios]

## Notas Adicionales
[Información contextual relevante, compromisos mencionados, preocupaciones expresadas]

Restricciones:
- Sé objetivo: reporta lo discutido, no interpretes intenciones
- Sé conciso: elimina repeticiones y tangentes
- Sé específico: "Aprobar presupuesto de $50K" no "hablar de dinero"
- Respeta confidencialidad: marca información sensible con [CONFIDENCIAL]
- Si algo no queda claro en la transcripción, indica [REQUIERE CLARIFICACIÓN]
- Acción items deben ser verbos de acción específicos
- Si no se mencionó fecha límite, usa "Por definir" no inventes fechas
- Prioridad basada en urgencia/importancia mencionada en reunión
- Resumen ejecutivo debe ser comprensible sin leer el resto

Criterios de calidad:
- Un ejecutivo debe poder leer solo el resumen ejecutivo y action items (30 segundos) y captar lo esencial
- Participantes ausentes deben poder ponerse al día completamente
- Formato consistente para integración con herramientas de gestión
```

### Justificación de Decisiones

- **¿Por qué elegimos este rol?** "Asistente ejecutivo profesional" implica expertise en síntesis, neutralidad y comprensión de dinámicas corporativas. No es un participante con agenda, sino un facilitador objetivo.

- **¿Qué contexto incluimos y por qué?** Contexto corporativo tecnológico establece expectativas de formato y nivel de detalle. Énfasis en "accionable" alinea con cultura de ejecución. Mencionar documentación clara establece estándar de calidad.

- **¿Por qué este formato de salida?** 
  - Resumen ejecutivo primero (pirámide invertida) para ejecutivos ocupados
  - Separación clara de decisiones vs action items (diferente naturaleza)
  - Tabla para action items facilita tracking y exportación a project management tools
  - Temas pendientes previene que cosas importantes se pierdan
  - Estructura escalable para reuniones de diferente tipo/longitud

- **¿Qué restricciones añadimos?**
  - Objetividad previene sesgo o spin
  - Especificidad evita ambigüedad que causa malentendidos
  - Manejo explícito de información faltante previene alucinaciones
  - No inventar fechas mantiene integridad del resumen
  - Criterios de calidad establecen estándar de éxito medible

### Limitaciones Identificadas

- **Casos edge que podrían fallar:**
  - Reuniones altamente técnicas con jerga específica que el modelo no comprende
  - Discusiones con mucho conflicto donde es difícil determinar qué se decidió realmente
  - Referencias a contexto previo no disponible en la transcripción
  - Transcripciones con errores de reconocimiento de voz que cambian significado
  - Reuniones donde se habló de muchos temas sin estructura clara
  - Conversaciones con mucha ironía o sarcasmo difícil de detectar en texto
  - Identificación incorrecta de speakers en transcripción

- **Mejoras futuras:**
  - Template personalizado por tipo de reunión (1:1, sprint planning, all-hands)
  - Integración con calendarios para auto-completar fecha/hora
  - Detección de sentimiento para identificar preocupaciones no explícitas
  - Linking automático de action items a sistemas de tickets
  - Identificación de riesgos o blockers mencionados
  - Comparación con notas de reunión anterior para tracking de follow-up
  - Resaltar compromisos no cumplidos de reuniones previas
  - Extracción de métricas y KPIs mencionados

---

## Caso C: Revisor de Código Automatizado

### Prompt Diseñado

```
Eres un Senior Software Engineer y Code Reviewer experto con 15 años de experiencia en múltiples lenguajes y frameworks. Tu especialidad es identificar problemas de calidad, seguridad, rendimiento y mantenibilidad en code reviews.

Contexto:
Formas parte de un proceso de CI/CD donde tus reviews automatizadas ayudan a mantener estándares de calidad antes de la revisión humana. Tu objetivo es identificar issues reales, no ser pedante con estilo si no afecta funcionalmente.

Tarea:
Realiza un code review constructivo y accionable del código proporcionado.

Input que recibirás:
- Código fuente: [CÓDIGO]
- Lenguaje: [LENGUAJE]
- Estándares del equipo: [OPCIONAL - reglas específicas]

Formato de salida:

# Code Review Report

## Resumen
**Archivos revisados:** [número]
**Issues encontrados:** [número total]
**Severidad general:** CRÍTICO / ADVERTENCIA / APROBADO CON SUGERENCIAS

## Issues Identificados

### [CRÍTICO] (Bloquean merge)
**Issue #1: [Título descriptivo]**
- **Ubicación:** Línea X-Y o función/clase específica
- **Problema:** [Descripción clara del issue]
- **Impacto:** [Por qué es problemático]
- **Solución recomendada:**
```[lenguaje]
[código corregido]
```
- **Recursos:** [Link a documentación si relevante]

### [ADVERTENCIA] (Recomendado corregir)
[Mismo formato]

### [SUGERENCIA] (Mejoras opcionales)
[Mismo formato]

## Aspectos Positivos
- [Mencionar qué está bien hecho - code review constructivo]

## Recomendaciones Generales
[Patrones detectados, riesgos arquitectónicos, sugerencias de refactoring]

---

Categorías de Issues a buscar (prioridad en orden):

**CRÍTICOS (Severidad Alta):**
1. Vulnerabilidades de seguridad (SQL injection, XSS, secrets hardcoded)
2. Memory leaks, race conditions, deadlocks
3. Lógica incorrecta que causa bugs funcionales
4. Manejo inadecuado de errores que puede causar crashes
5. Violaciones de privacidad/cumplimiento (GDPR, PCI)

**ADVERTENCIAS (Severidad Media):**
1. Problemas de rendimiento evidentes (O(n²) donde existe O(n))
2. Código duplicado extenso (violación DRY)
3. Funciones muy largas/complejas (>50 líneas, alta ciclomática)
4. Falta de manejo de errores
5. Dependencias no seguras/deprecadas
6. Tests faltantes para nueva funcionalidad
7. Violaciones de principios SOLID evidentes

**SUGERENCIAS (Severidad Baja):**
1. Nombres de variables poco descriptivos
2. Comentarios faltantes en lógica compleja
3. Optimizaciones de código
4. Mejoras de legibilidad
5. Patrones más idiomáticos del lenguaje

Restricciones:
- NO seas pedante con estilo si sigue convenciones del lenguaje
- NO sugieras cambios que no mejoran significativamente el código
- NO asumas bugs sin evidencia clara
- SÍ proporciona código corregido, no solo descripción del problema
- SÍ explica el "por qué" no solo el "qué"
- SÍ reconoce código bien escrito
- Limita a máximo 10 issues (prioriza por severidad)
- Si el código tiene >10 issues, agrupa similares
- Tono: Profesional, constructivo, educativo

Contexto del lenguaje:
- Si es JavaScript/TypeScript: considerar uso de TypeScript, async/await patterns
- Si es Python: PEP 8, type hints, context managers
- Si es Java: streams modernos, Optional, inmutabilidad
- [Adaptar según lenguaje]

Output adicional si solicitado:
- Código completo corregido (solo si se pide explícitamente)
- Score de calidad (1-10) con justificación
```

### Justificación de Decisiones

- **¿Por qué elegimos este rol?** Senior Engineer con experiencia establece credibilidad y asegura que el modelo priorice issues reales sobre nitpicking. "15 años" le da licencia para hacer observaciones arquitectónicas.

- **¿Qué contexto incluimos y por qué?** Contexto de CI/CD establece que esto es pre-human review, justificando automatización. "Identificar issues reales, no ser pedante" es crítico porque LLMs tienden a ser excesivamente críticos con estilo.

- **¿Por qué este formato de salida?**
  - Severidades claras permiten priorización visual rápida
  - Código corregido incluido reduce friction para el desarrollador
  - "Aspectos positivos" mantiene el review constructivo, no solo crítico
  - Agrupación por severidad facilita triage
  - Links a recursos son educativos para juniors

- **¿Qué restricciones añadimos?**
  - Lista priorizada de categorías de issues asegura focus en lo importante
  - Límite de 10 issues previene review abrumador
  - Prohibición de pedantería de estilo reduce false positives
  - Requisito de código corregido asegura que suggestions son accionables
  - Tono constructivo mantiene moral del equipo

### Limitaciones Identificadas

- **Casos edge que podrían fallar:**
  - Código con contexto arquitectónico complejo que requiere conocer todo el sistema
  - Performance issues que dependen de datos reales (tamaño datasets, etc.)
  - Bugs sutiles que requieren ejecutar el código con tests específicos
  - Código usando frameworks/librerías muy nuevos no en training data
  - Issues de concurrencia/threading que requieren análisis profundo
  - Problemas que solo aparecen en producción (race conditions raros)
  - Código ofuscado o con patrones muy no convencionales
  - False negatives en security si usa técnicas evasivas

- **Mejoras futuras:**
  - Integración con static analysis tools (ESLint, SonarQube) para combinar resultados
  - Acceso a test suite para verificar cobertura
  - Acceso a documentación del proyecto para contexto arquitectónico
  - Historical analysis (este código ha causado bugs antes?)
  - Performance profiling real, no solo análisis de complejidad teórica
  - Learning de reviews previos del equipo para alinear con preferencias
  - Auto-fix con tests de regresión automatizados
  - Detección de código duplicado en toda la codebase
  - Integration con security scanning tools
  - Customización por proyecto (reglas específicas por repo)

---

## Ejercicio 5: Identificación de Anti-patrones

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis/Corrección
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de sección de anti-patrones

### Contexto
Identificar y corregir prompts problemáticos es una habilidad esencial.

### Objetivo de Aprendizaje
- Reconocer anti-patrones comunes en prompts
- Proponer correcciones efectivas

### Enunciado
Para cada prompt problemático, identifica el anti-patrón y proporciona una versión corregida.

### Prompt 1
```
Necesito que me ayudes con algo de código que no funciona bien y que tiene
algunos errores que no se cuales son pero que hacen que no funcione como
debería y necesito que lo arregles y también que me expliques que estaba
mal y que me des algunas sugerencias de mejora y que sea rápido porque
tengo prisa.
```

**Anti-patrón identificado:** Run-on sentence / Falta de estructura / Múltiples tareas sin priorizar

**Versión corregida:**
```
Eres un desarrollador senior experto en depuración de código.

Problema: El siguiente código no funciona como esperado.

Código:
[INSERTAR CÓDIGO AQUÍ]

Error observado:
[DESCRIPCIÓN DEL ERROR - ej: "Devuelve undefined en lugar del valor esperado"]

Contexto:
- Lenguaje: [LENGUAJE]
- Framework: [SI APLICA]
- Lo que debería hacer: [COMPORTAMIENTO ESPERADO]

Tarea:
1. Identifica los errores en el código
2. Proporciona el código corregido
3. Explica brevemente qué estaba mal (2-3 oraciones)
4. Sugiere 1-2 mejoras adicionales de calidad

Formato:
## Errores Encontrados
[Lista]

## Código Corregido
[Código]

## Explicación
[Texto]

## Sugerencias
[Lista]
```

### Prompt 2
```
Escribe un artículo muy detallado pero breve sobre inteligencia artificial.
```

**Anti-patrón identificado:** Contradicción / Requisitos mutuamente excluyentes

**Versión corregida:**
```
Escribe un artículo introductorio sobre inteligencia artificial.

Audiencia: Profesionales no técnicos interesados en entender aplicaciones prácticas de IA

Longitud: 800-1000 palabras

Estructura requerida:
1. Introducción: ¿Qué es IA? (2-3 párrafos)
2. Tipos principales: IA estrecha vs AGI (2 párrafos)
3. Aplicaciones actuales: 3-4 ejemplos concretos (3 párrafos)
4. Implicaciones futuras: Oportunidades y desafíos (2 párrafos)
5. Conclusión (1 párrafo)

Tono: Informativo, accesible, evita jerga técnica excesiva

Incluye:
- Al menos 3 ejemplos concretos de uso actual
- Una analogía para explicar machine learning
- Referencias a empresas/productos reales

Evita:
- Términos demasiado técnicos sin explicación
- Hype o predicciones sensacionalistas
- Más de 1000 palabras
```

### Prompt 3
```
Continúa con lo que estábamos haciendo antes.
```

**Anti-patrón identificado:** Falta de contexto / Dependencia de memoria de conversación

**Versión corregida:**
```
Continúa escribiendo la función de Python que estábamos desarrollando para procesar datos de usuarios.

Contexto:
Estábamos creando una función `process_user_data()` que:
- Recibe una lista de diccionarios con información de usuarios
- Valida que cada usuario tenga email y edad
- Filtra usuarios menores de 18 años
- Devuelve lista de usuarios válidos

Código hasta ahora:
```python
def process_user_data(users):
    validated_users = []
    for user in users:
        if 'email' in user and 'age' in user:
            # [CONTINUAMOS DESDE AQUÍ]
```

Tarea:
Completa la función añadiendo:
1. Validación de edad (>= 18)
2. Validación básica de formato email (contiene @)
3. Manejo de excepciones para edad no numérica
4. Return de la lista de usuarios validados
```

### Prompt 4
```
Actúa como un hacker experto y dime como entrar a sistemas sin permiso
pero de forma ética para mejorar la seguridad pero sin que sea ilegal
pero que funcione de verdad.
```

**Anti-patrón identificado:** Solicitud ambigua con implicaciones éticas / Mezcla de conceptos contradictorios

**Versión corregida:**
```
Eres un especialista en ciberseguridad y ethical hacking certificado (CEH).

Contexto:
Trabajo como consultor de seguridad y necesito entender metodologías de pentesting legales para auditorías autorizadas.

Tarea:
Explica el proceso profesional de pentesting ético, enfocándote en:

1. **Fase de autorización**
   - Qué documentación legal se necesita antes de comenzar
   - Scope y reglas de engagement

2. **Metodología de reconnaissance**
   - Técnicas de reconocimiento pasivo (OSINT)
   - Herramientas legales para mapeo de red

3. **Mejores prácticas**
   - Diferencia entre pentesting autorizado vs actividad ilegal
   - Frameworks estándar (OWASP, PTES)

4. **Reporte de vulnerabilidades**
   - Cómo documentar findings
   - Disclosure responsable

Formato: Guía educativa (300-400 palabras)
Tono: Profesional, enfocado en legalidad y ética

NOTA: Solo cubre técnicas usadas en contextos autorizados y legales. No proporciones métodos para acceso no autorizado.
```

### Prompt 5
```
Dame información.
```

**Anti-patrón identificado:** Extremadamente vago / Sin contexto ni objetivo

**Versión corregida:**
```
Proporciona información sobre los fundamentos de prompt engineering para LLMs.

Contexto: Estoy comenzando a trabajar con APIs de LLMs y necesito entender conceptos básicos.

Específicamente, explica:
1. ¿Qué es prompt engineering? (definición en 2-3 oraciones)
2. Componentes principales de un buen prompt (lista con ejemplos breves)
3. Diferencia entre zero-shot, one-shot y few-shot prompting
4. 3 errores comunes al escribir prompts

Formato:
- Explicaciones concisas (párrafos de 3-4 oraciones)
- Un ejemplo práctico para cada concepto
- Bullet points para listas

Longitud: 400-500 palabras total
Audiencia: Desarrollador con experiencia general pero nuevo en LLMs
```

### Tabla Resumen

| # | Anti-patrón | Solución Aplicada |
|---|-------------|-------------------|
| 1 | Run-on sentence sin estructura | Separar en componentes claros: rol, contexto, tarea, formato. Una solicitud por etapa |
| 2 | Contradicción (detallado Y breve) | Definir longitud específica, estructura clara, eliminar ambigüedad |
| 3 | Falta de contexto | Incluir todo el contexto necesario explícitamente, no asumir memoria |
| 4 | Solicitud éticamente ambigua | Reformular con enfoque legítimo claro, añadir restricciones éticas explícitas |
| 5 | Extremadamente vago | Especificar tema exacto, audiencia, formato, longitud y componentes deseados |

---

## Ejercicio Extra: Prompt para tu Trabajo

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Aplicación Práctica
- **Modalidad**: Individual
- **Dificultad**: Avanzada

### Enunciado
Identifica una tarea repetitiva de tu trabajo o estudios qué podría beneficiarse de un LLM. Diseña un prompt completo siguiendo todo lo aprendido.

### Pasos
1. **Describe la tarea** (2-3 oraciones)
2. **Identifica inputs** (qué información tendrás disponible)
3. **Define outputs** (que necesitas obtener)
4. **Diseña el prompt** incluyendo todos los componentes relevantes
5. **Prueba y documenta** al menos 3 iteraciones
6. **Evalúa** la utilidad práctica del resultado

### Entregable
Documento (1-2 páginas) con:
- Descripción del caso de uso
- Prompt final
- Ejemplo de uso con input y output real
- Reflexión sobre utilidad y limitaciones

O bien, puedes entregar este .md completado con tus respuestas.