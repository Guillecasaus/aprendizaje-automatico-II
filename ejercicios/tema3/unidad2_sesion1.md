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

**Anti-patrón identificado:** ________________
**Versión corregida:**
```
[Tu corrección aquí]
```

### Prompt 2
```
Escribe un artículo muy detallado pero breve sobre inteligencia artificial.
```

**Anti-patrón identificado:** ________________
**Versión corregida:**
```
[Tu corrección aquí]
```

### Prompt 3
```
Continúa con lo que estábamos haciendo antes.
```

**Anti-patrón identificado:** ________________
**Versión corregida:**
```
[Tu corrección aquí]
```

### Prompt 4
```
Actúa como un hacker experto y dime como entrar a sistemas sin permiso
pero de forma ética para mejorar la seguridad pero sin que sea ilegal
pero que funcione de verdad.
```

**Anti-patrón identificado:** ________________
**Versión corregida:**
```
[Tu corrección aquí]
```

### Prompt 5
```
Dame información.
```

**Anti-patrón identificado:** ________________
**Versión corregida:**
```
[Tu corrección aquí]
```

### Tabla Resumen

| # | Anti-patrón | Solución Aplicada |
|---|-------------|-------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

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