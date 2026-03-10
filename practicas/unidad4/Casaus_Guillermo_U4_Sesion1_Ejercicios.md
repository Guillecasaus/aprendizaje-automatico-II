# Ejercicios Resueltos - Unidad 4, Sesion 1
## Agentes de IA y Fundamentos de n8n

---

## Informacion General

| Campo | Valor |
|-------|-------|
| **Nombre del estudiante** | Guillermo Casaus |
| **Fecha** | 10 de marzo de 2026 |
| **Titulo** | Ejercicios Unidad 4, Sesion 1 - Agentes de IA y Fundamentos de n8n |

---

## Ejercicio 1: Analisis del Paradigma PDA

### Escenario A: Agente de Soporte Tecnico (eCommerce)

Una tienda online quiere un agente que atienda consultas de clientes sobre el estado de sus pedidos, gestione devoluciones sencillas y escale a un humano los casos complejos.

| Componente | Descripcion |
|------------|-------------|
| **Percepcion** (Que informacion recibe?) | Mensajes del cliente en lenguaje natural a traves de chat en vivo, email o WhatsApp. Tambien recibe el contexto del cliente (identificador de usuario, pedidos asociados) y el historial de la conversacion actual. |
| Fuentes de datos | Chat en vivo del sitio web, correo electronico, WhatsApp Business API, base de datos de pedidos (ERP/CRM), historial de interacciones previas, catalogo de politicas de devolucion. |
| Formato de entrada | Texto libre (lenguaje natural del cliente), complementado con datos estructurados (JSON) provenientes de la base de datos de pedidos (numero de pedido, estado, fecha de entrega estimada). |
| **Decision** (Como procesa?) | Un LLM analiza el mensaje del cliente, identifica la intencion (consulta de estado de pedido, solicitud de devolucion, queja, otra consulta) y determina la accion mas adecuada segun las instrucciones del prompt y los datos disponibles. |
| Modelo de IA utilizado | GPT-4o-mini. Ofrece un buen equilibrio entre coste y rendimiento para tareas de soporte, donde no se requiere razonamiento extremadamente complejo sino comprension del lenguaje natural y seguimiento de instrucciones. |
| Instrucciones clave del prompt | "Eres un agente de soporte de [nombre de la tienda]. Responde siempre de forma amable, profesional y concisa. Antes de responder sobre un pedido, consulta su estado en la base de datos. Para devoluciones, verifica que cumplan la politica vigente (plazo de 30 dias, producto sin usar). Si el cliente menciona problemas legales, defectos de seguridad del producto o solicita expresamente hablar con una persona, escala de inmediato." |
| Criterios para escalar a humano | 1) El cliente solicita explicitamente hablar con un agente humano. 2) El tema involucra cuestiones legales o reclamaciones formales. 3) Se trata de una devolucion de alto valor (superior a 200 EUR). 4) La misma consulta se ha repetido mas de dos veces sin resolucion satisfactoria. 5) El agente no tiene confianza suficiente en su respuesta. |
| **Accion** (Que ejecuta?) | Responde al cliente con la informacion solicitada, ejecuta operaciones sobre sistemas externos o transfiere la conversacion a un humano, segun la decision tomada. |
| Acciones posibles | Consultar el estado de un pedido via API de tracking, responder al cliente con informacion del pedido, iniciar un proceso de devolucion en el ERP, crear un ticket de soporte en el sistema de helpdesk (ej. Zendesk), escalar la conversacion a un agente humano, enviar un email de confirmacion al cliente. |
| Sistemas externos que necesita | Base de datos de pedidos / ERP, API de seguimiento de envios (courier), sistema de helpdesk (Zendesk, Freshdesk), servicio de email (SMTP o Gmail API), CRM para registro del historial del cliente, WhatsApp Business API. |

---

### Escenario B: Agente de Recursos Humanos

Una empresa quiere automatizar la primera fase de seleccion de candidatos: recibir CVs, analizarlos segun los requisitos del puesto y enviar respuestas personalizadas a los candidatos.

| Componente | Descripcion |
|------------|-------------|
| **Percepcion** | CVs recibidos como archivos adjuntos por correo electronico o subidos a traves de un formulario web. Tambien recibe la descripcion del puesto vacante con los requisitos (experiencia minima, formacion requerida, idiomas, habilidades tecnicas) y, opcionalmente, el historial de candidatos previamente evaluados para el mismo puesto. Los CVs pueden venir en formato PDF, DOCX o texto plano. |
| **Decision** | El LLM extrae informacion estructurada de cada CV (nombre, experiencia laboral, formacion, habilidades tecnicas, idiomas). A continuacion, compara esos datos con los requisitos del puesto y genera una puntuacion de idoneidad. Segun esa puntuacion, clasifica al candidato en una de tres categorias: (1) apto para entrevista, (2) descartado, o (3) requiere revision manual por parte del reclutador (casos ambiguos o perfiles interesantes que no encajan exactamente). |
| **Accion** | Envia un email personalizado al candidato segun la categoria asignada: invitacion a entrevista con fecha/hora propuesta, rechazo cortes agradeciendo la candidatura, o solicitud de informacion adicional. Actualiza el ATS (Applicant Tracking System) con el estado del candidato y la puntuacion asignada. Notifica al reclutador humano cuando hay candidatos destacados o casos para revision manual. |

---

### Escenario C: Agente de Marketing de Contenidos

Un equipo de marketing necesita un agente que monitorice menciones de su marca en redes sociales, analice el sentimiento y genere borradores de respuesta para el community manager.

| Componente | Descripcion |
|------------|-------------|
| **Percepcion** | Menciones de la marca recogidas en tiempo real o periodicamente desde multiples redes sociales: Twitter/X, Instagram, LinkedIn, Facebook y foros relevantes. La informacion se obtiene a traves de APIs de redes sociales o herramientas de social listening (ej. Brandwatch, Mention). Los datos incluyen el texto de la mencion, el autor, la plataforma, la fecha y el alcance (numero de seguidores o impresiones). Es una percepcion activa, ya que el agente monitoriza las fuentes de forma continua. |
| **Decision** | El LLM clasifica cada mencion segun su sentimiento (positivo, negativo o neutro), evalua la urgencia (mencion casual frente a posible crisis reputacional), y determina si requiere respuesta. Para las menciones que requieren respuesta, genera un borrador adaptado al tono de la marca y al contexto de la plataforma. Las menciones con sentimiento muy negativo o alto alcance se priorizan y se marcan como urgentes. |
| **Accion** | Almacena cada mencion con su analisis de sentimiento en una base de datos para reporting. Envia los borradores de respuesta al community manager a traves de Slack o email para su revision y aprobacion. En caso de detectar una crisis potencial (varias menciones negativas simultaneas o una mencion viral negativa), alerta inmediatamente al equipo de comunicacion. Genera un informe semanal consolidado con estadisticas de menciones, tendencias de sentimiento y tiempo medio de respuesta. |

---

### Escenario D: Agente Educativo (Tutor IA)

Una universidad quiere un agente que ayude a estudiantes con dudas sobre una asignatura, proporcionando explicaciones personalizadas y recomendando recursos de estudio.

| Componente | Descripcion |
|------------|-------------|
| **Percepcion** | Preguntas formuladas por los estudiantes a traves de una interfaz de chat (web o aplicacion movil). Ademas, el agente tiene acceso al historial de preguntas previas de cada estudiante, los materiales del curso (apuntes, presentaciones, ejercicios resueltos, bibliografia) indexados en una base de conocimiento vectorial, y opcionalmente la informacion sobre el progreso academico del alumno (notas parciales, ejercicios entregados). |
| **Decision** | El LLM interpreta la duda del estudiante, identifica el tema concreto dentro del temario y evalua el nivel de comprension del alumno basandose en su historial. Realiza busqueda semantica en los materiales del curso para recuperar los fragmentos mas relevantes (RAG). A partir de esa informacion, genera una explicacion adaptada al nivel del estudiante. Decide si basta con una explicacion textual, si conviene recomendar recursos adicionales (videos, capitulos del libro, ejercicios) o si la dificultad detectada justifica sugerir una tutoria presencial con el profesor. |
| **Accion** | Responde al estudiante con una explicacion personalizada que referencia los materiales del curso. Proporciona enlaces directos a recursos recomendados (secciones del libro, videos, ejercicios de practica). Registra la interaccion en una base de datos para que el profesor pueda hacer seguimiento. Si detecta que un estudiante tiene dificultades recurrentes en un mismo tema (mas de tres preguntas sin progreso), envia una alerta al profesor para que intervenga de forma proactiva. |

---

### Preguntas de Reflexion

**1. Cual de los cuatro escenarios tiene la percepcion mas compleja? Por que? Como afecta la complejidad de la percepcion al diseno del agente?**

El Escenario C (Marketing de Contenidos) presenta la percepcion mas compleja. Esto se debe a que el agente necesita monitorizar multiples fuentes de datos heterogeneas en tiempo real (varias redes sociales, cada una con su propia API y formato de datos), procesar grandes volumenes de informacion continua, y filtrar el ruido para quedarse solo con las menciones relevantes. A diferencia de los otros escenarios, donde el agente responde a un input discreto (un mensaje de un cliente, un CV, una pregunta de un estudiante), aqui el agente debe estar activamente escaneando flujos de informacion.

Esta complejidad en la percepcion tiene un impacto directo en el diseno del agente. Se necesitan multiples conectores (uno por plataforma), un sistema de filtrado previo al LLM para evitar procesar menciones irrelevantes (lo que dispararia el coste), y una arquitectura capaz de manejar picos de volumen (por ejemplo, si la marca se viraliza). El agente requiere mas infraestructura y mas puntos potenciales de fallo que los otros escenarios.

**2. En el Escenario A, el agente debe decidir cuando escalar a un humano. Que criterios usarias para esta decision? Es mejor pecar de cauteloso (escalar demasiado) o de autonomo (intentar resolver todo)?**

Los criterios que usaria son:

- Solicitud explicita del cliente de hablar con una persona.
- Temas legales, amenazas de denuncia o reclamaciones formales.
- Quejas reiteradas: si el cliente ha contactado mas de dos veces por el mismo problema sin resolucion.
- Devoluciones o compensaciones de alto valor economico (umbral configurable).
- Baja confianza del modelo en su respuesta (cuando el LLM no tiene datos suficientes o el caso es ambiguo).
- Deteccion de tono emocional muy negativo o frustracion elevada por parte del cliente.

Es preferible pecar de cauteloso, especialmente en las fases iniciales del despliegue del agente. Un agente que intenta resolver todo pero falla en un caso complejo puede danar la confianza del cliente y la reputacion de la marca. El coste de escalar de mas es un leve aumento de carga para el equipo humano; el coste de no escalar cuando se deberia es un cliente insatisfecho. Con el tiempo, a medida que se recopilan datos sobre el rendimiento del agente, se pueden ir relajando los criterios de escalado de forma controlada.

**3. Compara los Escenarios B y C: ambos analizan texto, pero uno analiza documentos estructurados (CVs) y otro texto libre (redes sociales). Como cambia esto el componente de decision?**

Aunque ambos escenarios requieren que el LLM procese texto, la naturaleza del texto es muy diferente y esto afecta directamente al componente de decision:

- En el Escenario B, los CVs tienen una estructura semi-predecible: secciones diferenciadas de datos personales, experiencia laboral, formacion y habilidades. El LLM puede apoyarse en esa estructura para extraer informacion de forma sistematica y compararla con los requisitos del puesto de forma relativamente objetiva. La decision se basa en criterios cuantificables (anos de experiencia, titulaciones, presencia de habilidades concretas).

- En el Escenario C, las menciones en redes sociales son texto completamente libre, a menudo breve, con jerga, abreviaturas, emojis, ironia, sarcasmo y un fuerte componente de contexto cultural. El analisis de sentimiento debe lidiar con estas ambiguedades, y la decision de si una mencion es positiva o negativa puede ser mucho menos clara. El margen de error del modelo es mayor, y se necesita un enfoque mas conservador (por ejemplo, marcar menciones ambiguas para revision humana en lugar de decidir automaticamente).

En resumen, la decision en B es mas una tarea de extraccion y matching estructurado, mientras que en C es una tarea de comprension pragmatica del lenguaje, que es intrinsecamente mas dificil para un LLM.

**4. Si tuvieras que elegir un escenario para implementar como tu primer agente en n8n, cual elegirias y por que?**

Elegiria el Escenario A (Agente de Soporte Tecnico).

- Complejidad tecnica moderada: la percepcion es un unico canal de entrada (chat), las acciones son acotadas y bien definidas (consultar pedido, responder, escalar), y la logica de decision se puede definir con reglas claras en el prompt.
- Alto valor de negocio inmediato: el soporte al cliente es una de las areas donde los agentes de IA generan ahorro medible rapidamente, al reducir el volumen de tickets que llegan al equipo humano.
- Riesgo controlable: al incluir el mecanismo de escalado a humano, los errores del agente no llegan al cliente final sin supervision. Es un despliegue con red de seguridad.
- Buena disponibilidad de integraciones en n8n: existen nodos nativos o faciles de configurar para los sistemas mas comunes (Zendesk, Gmail, HTTP Request para APIs de pedidos).

Los escenarios C y D requieren integraciones mas complejas o mayor volumen de datos; el B requiere procesamiento de documentos (PDFs) que anade complejidad tecnica innecesaria para un primer agente.

---

## Ejercicio 2: Comparativa de Plataformas de Automatizacion

### Parte A: Tabla de Decision

**Caso**: Una clinica dental con 3 sedes quiere automatizar la gestion de citas. El sistema debe: (1) recibir solicitudes de cita por WhatsApp, (2) consultar la disponibilidad en Google Calendar, (3) confirmar la cita al paciente, y (4) enviar recordatorios 24h antes. Ademas, quieren que un agente de IA responda preguntas frecuentes sobre tratamientos. Los datos de pacientes son sensibles (normativa sanitaria) y el presupuesto es limitado.

| Criterio | n8n | Make | Zapier | Peso (importancia) |
|----------|-----|------|--------|---------------------|
| Coste (menor es mejor) | 5 | 3 | 2 | Alta (x3) |
| Facilidad de uso | 3 | 4 | 5 | Media (x2) |
| Integracion con WhatsApp | 4 | 4 | 4 | Alta (x3) |
| Capacidades de IA nativas | 5 | 3 | 3 | Alta (x3) |
| Despliegue on-premise (datos sensibles) | 5 | 1 | 1 | Muy Alta (x4) |
| Numero de integraciones disponibles | 3 | 4 | 5 | Media (x2) |
| Soporte de la comunidad | 4 | 3 | 4 | Baja (x1) |
| Escalabilidad | 4 | 4 | 3 | Media (x2) |
| **Total ponderado** | **86** | **61** | **61** | |

**Calculo detallado:**

- **n8n**: (5x3) + (3x2) + (4x3) + (5x3) + (5x4) + (3x2) + (4x1) + (4x2) = 15 + 6 + 12 + 15 + 20 + 6 + 4 + 8 = **86**
- **Make**: (3x3) + (4x2) + (4x3) + (3x3) + (1x4) + (4x2) + (3x1) + (4x2) = 9 + 8 + 12 + 9 + 4 + 8 + 3 + 8 = **61**
- **Zapier**: (2x3) + (5x2) + (4x3) + (3x3) + (1x4) + (5x2) + (4x1) + (3x2) = 6 + 10 + 12 + 9 + 4 + 10 + 4 + 6 = **61**

**Justificacion de las puntuaciones:**

- **Coste**: n8n es gratuito y open source en self-hosting, solo requiere un servidor; Make y Zapier cobran por ejecucion, siendo Zapier el mas caro a escala.
- **Facilidad de uso**: Zapier es el mas intuitivo para usuarios no tecnicos; Make tiene un editor visual potente; n8n requiere algo mas de conocimiento tecnico pero su interfaz es clara.
- **Integracion con WhatsApp**: las tres plataformas lo soportan de forma comparable, ya sea con nodos nativos o mediante la API de WhatsApp Business.
- **Capacidades de IA nativas**: n8n destaca con su nodo AI Agent, soporte nativo para memoria, herramientas (tools) y multiples proveedores de LLM. Make y Zapier tienen integraciones con OpenAI pero no un framework de agentes completo.
- **Despliegue on-premise**: n8n es la unica que permite instalacion on-premise al ser open source. Make y Zapier son exclusivamente cloud, lo que es incompatible con la normativa sanitaria sobre datos de pacientes.
- **Integraciones disponibles**: Zapier lidera con mas de 6000 integraciones; Make tiene unas 1500; n8n tiene menos predefinidas pero permite conectar con cualquier API via HTTP Request.
- **Soporte de comunidad**: n8n y Zapier tienen comunidades activas y amplia documentacion; Make tiene una comunidad algo menor.
- **Escalabilidad**: n8n permite escalar la infraestructura al gusto al ser self-hosted; Make es robusto en cloud; Zapier tiene limitaciones en planes economicos.

---

### Parte B: Justificacion de la Decision

**1. Plataforma recomendada: n8n.**

La razon principal es que n8n es la unica de las tres plataformas que permite despliegue on-premise, requisito no negociable cuando se manejan datos de pacientes bajo normativa sanitaria (RGPD, LOPD-GDD y regulaciones sanitarias especificas). Ademas, al ser open source y gratuita en self-hosting, se ajusta al presupuesto limitado de la clinica. Sus capacidades nativas de IA (nodo AI Agent con memoria y herramientas) permiten implementar el agente de FAQ sobre tratamientos de forma integrada en el mismo workflow.

**2. Factor determinante: el despliegue on-premise.**

Este criterio fue el que mas peso tuvo en la decision (Muy Alta, x4) y es el que marca la mayor diferencia: n8n obtiene 5 frente al 1 de Make y Zapier. Si eliminasemos este requisito (por ejemplo, si los datos no fueran sensibles), la decision seria mas equilibrada. Sin el factor on-premise, los totales serian: n8n = 66, Make = 57, Zapier = 57. n8n seguiria ganando por su menor coste y mejores capacidades de IA, pero la diferencia seria menor y dependeria mas del perfil tecnico del equipo.

**3. Trade-offs de n8n:**

- Menor facilidad de uso que Zapier: la clinica necesitara alguien con perfil tecnico minimo para configurar y mantener los workflows. Mitigacion: usar templates predefinidos de n8n y documentar los workflows para que sean mantenibles.
- Menor numero de integraciones predefinidas: si en el futuro necesitan conectar con un software dental muy especifico, puede que no haya nodo nativo. Mitigacion: n8n permite conectar con cualquier sistema que tenga API REST mediante el nodo HTTP Request.
- Responsabilidad del mantenimiento de infraestructura: al self-hostear, la clinica es responsable de la disponibilidad del servidor, backups y actualizaciones. Mitigacion: desplegar con Docker y configurar backups automaticos, o usar n8n Cloud si mas adelante el presupuesto lo permite.

---

### Parte C: Escenario Alternativo

Si en lugar de una clinica dental con datos sensibles se tratase de una tienda de ropa online que solo necesita automatizar publicaciones en Instagram y responder mensajes directos, la recomendacion cambiaria.

En este caso, recomendaria **Zapier**, por las siguientes razones:

- No hay requisitos de privacidad estrictos ni datos sanitarios, por lo que el despliegue on-premise deja de ser necesario. El factor que mas diferenciaba a n8n pierde peso.
- Zapier tiene la integracion con Instagram mas madura y directa, con triggers y acciones nativos bien probados.
- La facilidad de uso de Zapier es la mas alta de las tres, lo que es relevante si el equipo de marketing no tiene perfil tecnico.
- El flujo es sencillo (publicar contenido y responder DMs), sin necesidad de un framework de agentes de IA complejo. Las capacidades avanzadas de n8n serian sobredimensionadas para este caso.
- Zapier ofrece un plan gratuito basico que podria ser suficiente para empezar, y sus planes de pago son razonables para el volumen de una tienda de ropa.

---

### Preguntas de Reflexion

**1. En que situaciones elegirias Zapier a pesar de su mayor coste? Cuando es la simplicidad mas valiosa que la flexibilidad?**

Elegiria Zapier cuando se cumplan varias de estas condiciones: el equipo no tiene perfil tecnico y necesita poner en marcha la automatizacion rapidamente (Zapier tiene la curva de aprendizaje mas corta); las automatizaciones son lineales y sencillas (trigger -> una o dos acciones); no hay requisitos de privacidad que exijan on-premise; la empresa ya usa herramientas del ecosistema de Zapier y puede aprovechar sus integraciones nativas; y el coste de Zapier es asumible frente al coste de tiempo/recursos de configurar y mantener una instancia de n8n.

La simplicidad es mas valiosa que la flexibilidad cuando el coste de oportunidad del tiempo del equipo es alto. Si un equipo de marketing necesita automatizar algo en 30 minutos con Zapier frente a medio dia con n8n, y la automatizacion no es critica ni maneja datos sensibles, Zapier es la eleccion racional.

**2. El hecho de que n8n sea open source, es siempre una ventaja? Que desafios implica mantener una instancia propia frente a usar un servicio gestionado?**

No, no es siempre una ventaja. Que n8n sea open source ofrece beneficios claros (transparencia del codigo, posibilidad de self-hosting, personalizacion, sin vendor lock-in, comunidad de contribuidores), pero tambien implica responsabilidades que un servicio gestionado absorbe:

- **Mantenimiento de infraestructura**: hay que provisionar y mantener el servidor (o contenedor Docker), gestionar actualizaciones del sistema operativo, de n8n y de sus dependencias.
- **Disponibilidad y uptime**: la empresa es responsable de que el servicio este disponible 24/7. Si el servidor cae, las automatizaciones dejan de funcionar hasta que alguien lo restaure.
- **Backups y recuperacion**: hay que configurar backups periodicos de la base de datos de n8n (credenciales, workflows, ejecuciones) y tener un plan de recuperacion ante desastres.
- **Seguridad**: al exponer n8n a internet (por ejemplo para webhooks), la empresa debe gestionar certificados SSL, reglas de firewall, actualizaciones de seguridad y control de acceso.
- **Coste oculto**: aunque n8n es gratuito, el servidor no lo es. Ademas, el tiempo del equipo tecnico dedicado a mantener la instancia tiene un coste.

Para una organizacion sin equipo tecnico, un servicio gestionado como Zapier o incluso n8n Cloud (la version alojada de n8n) puede ser mas rentable que self-hostear, aunque el coste de la licencia sea mayor.

---

## Ejercicio 4: Diseno de Automatizacion con Schedule Trigger

### Parte A: Diagrama de Nodos

```
Nodo 1: [Schedule Trigger]
   ├── Tipo: Schedule Trigger
   ├── Configuracion: Lunes a viernes, 8:00 AM, Europe/Madrid (cron: 0 8 * * 1-5)
   ├── Entrada: Ninguna (es el trigger)
   └── Salida: Timestamp de ejecucion { timestamp: "2026-03-10T08:00:00.000Z" }

Nodo 2: [HTTP Request - NewsAPI]
   ├── Tipo: HTTP Request
   ├── Configuracion: GET https://newsapi.org/v2/everything
   │   Parametros: q="artificial intelligence OR inteligencia artificial",
   │               language=es, sortBy=publishedAt, pageSize=10
   │   Auth: Header Auth (X-Api-Key: credencial configurada en n8n)
   ├── Entrada: Timestamp del trigger
   └── Salida: { status, totalResults, articles: [ { title, source, description, url, publishedAt } ] }

Nodo 3: [IF - Hay noticias?]
   ├── Tipo: IF
   ├── Configuracion: {{ $json.totalResults }} is greater than 0
   ├── Entrada: Respuesta completa de NewsAPI
   └── Salida: true (hay articulos) / false (0 resultados)

Nodo 4: [HTTP Request - OpenRouter LLM]
   ├── Tipo: HTTP Request
   ├── Configuracion: POST https://openrouter.ai/api/v1/chat/completions
   │   Body: model=google/gemini-2.0-flash-exp:free,
   │         messages=[system prompt + articulos serializados como JSON]
   │   Auth: Header Auth (Authorization: Bearer sk-or-...)
   ├── Entrada: Array de articulos del nodo NewsAPI
   └── Salida: { choices: [ { message: { content: "<resumen HTML>" } } ] }

Nodo 5: [Gmail - Enviar Resumen]
   ├── Tipo: Gmail
   ├── Configuracion: To: equipo@empresa.com
   │   Subject: "Resumen IA - {{ $now.format('dd/MM/yyyy') }}"
   │   Body: {{ $json.choices[0].message.content }} (HTML)
   ├── Entrada: Resumen generado por el LLM
   └── Salida: Confirmacion de envio { messageId, threadId }
```

**Diagrama visual:**

```
[Schedule Trigger] --> [HTTP Request: NewsAPI] --> [IF: totalResults > 0?]
  (L-V, 08:00)                                          |
                                               true ----+---- false
                                                |                |
                                   [HTTP Request: OpenRouter]  [Stop]
                                                |
                                           [Gmail]
```

---

### Parte B: Configuracion Detallada del Schedule Trigger

| Parametro | Valor | Justificacion |
|-----------|-------|---------------|
| Trigger Times -> Rule | Cron Expression | Permite especificar dias concretos de la semana con precision |
| Expresion Cron | `0 8 * * 1-5` | Minuto 0, hora 8, cualquier dia del mes, cualquier mes, lunes (1) a viernes (5) |
| Hora | 8 | El equipo recibe el resumen al inicio de la jornada laboral |
| Minuto | 0 | Ejecucion en punto para mayor previsibilidad |
| Dias de la semana | Lunes a viernes (1-5) | Solo dias laborables; los fines de semana no hay jornada |
| Zona horaria | Europe/Madrid | Garantiza que las 8:00 sean hora local espanola independientemente del servidor |

**Respuesta a la pregunta sobre servidor apagado:**

Si el servidor de n8n esta apagado a las 8:00, el workflow NO se ejecuta ni se recupera retroactivamente cuando el servidor vuelve a estar online. n8n no tiene mecanismo de "catch-up" para ejecuciones perdidas por defecto (a diferencia de algunos sistemas de colas como Celery con Beat). La ejecucion de ese dia se pierde silenciosamente.

Para mitigar este comportamiento se puede: (1) monitorizar el uptime del servidor con una herramienta externa (UptimeRobot, Grafana) y configurar alertas, (2) asegurarse de que el servidor arranca automaticamente con Docker restart policy `always` o `unless-stopped`, y (3) evaluar n8n Cloud si la disponibilidad es critica, ya que el SLA de la plataforma gestionada cubre estos casos.

---

### Parte C: Configuracion del Nodo HTTP Request (NewsAPI)

| Parametro | Valor |
|-----------|-------|
| Method | `GET` |
| URL | `https://newsapi.org/v2/everything` |
| -> `q` | `"artificial intelligence" OR "inteligencia artificial" OR "AI agents"` |
| -> `language` | `es` (NewsAPI solo acepta un idioma por peticion; para cubrir ingles se hace una segunda peticion o se usa `en` en un nodo paralelo) |
| -> `sortBy` | `publishedAt` |
| -> `pageSize` | `10` |
| Authentication | Header Auth (credencial guardada en n8n) |
| -> Header Name | `X-Api-Key` |
| -> Header Value | Referencia a la credencial configurada en n8n |

**Respuesta sobre el uso de credenciales:**

Usar el sistema de credenciales de n8n en lugar de escribir la API key directamente en el nodo es fundamental por varias razones:

1. **Seguridad**: las credenciales se almacenan cifradas en la base de datos de n8n mediante la clave definida en `N8N_ENCRYPTION_KEY`. No aparecen en texto plano en ningun sitio de la interfaz.
2. **No exposicion al exportar**: al exportar un workflow como JSON para compartirlo o hacer backup, las credenciales no se incluyen. Solo se guarda el nombre de la credencial referenciada.
3. **Reutilizacion**: la misma credencial puede usarse en multiples workflows. Si la API key caduca o se rota, basta con actualizarla en un unico lugar.
4. **Auditoria**: n8n registra que credenciales se usan en cada workflow, facilitando la revision de accesos.

Para configurar una credencial en n8n: Settings > Credentials > Add Credential > seleccionar "Header Auth" > rellenar nombre y valor del header.

---

### Parte D: System Prompt para el Resumen

```
Eres un asistente especializado en resumir noticias de inteligencia artificial para un equipo tecnico.

Se te proporciona un array JSON con los ultimos articulos sobre IA publicados hoy. Genera un resumen diario con las siguientes caracteristicas:

- Titulo principal: "Resumen de IA - [fecha de hoy en formato dd/MM/yyyy]"
- Selecciona entre 3 y 5 noticias destacadas priorizando las de mayor impacto tecnico o empresarial
- Para cada noticia incluye:
  * Titulo del articulo (en negrita)
  * Fuente y fecha de publicacion
  * Resumen de 2-3 frases explicando el contenido y su relevancia
  * Enlace al articulo original
- Al final incluye una seccion "Tendencia del dia" con un parrafo breve sobre el tema dominante de las noticias de hoy
- Tono: profesional e informativo, sin sensacionalismo
- Idioma: espanol
- Formato: HTML valido para que el email se renderice correctamente (usa <h2>, <h3>, <p>, <strong>, <a href>, <ul>, <li>)
- Longitud total del cuerpo: entre 400 y 600 palabras
```

---

### Preguntas de Reflexion

**1. Como manejarías el caso en que la API de noticias devuelve un error? Que nodo añadirias y donde?**

Anadia un nodo **Error Trigger** o, mas practico, configuraria el nodo HTTP Request con la opcion "Continue on Fail" activada. Despues del nodo HTTP Request de NewsAPI inserto un nodo IF adicional que comprueba si `$json.status === "error"` o si el codigo HTTP de respuesta no es 200. Si se detecta error, la rama false dirigiria a un nodo **Send Email** o **Slack** que notifica al equipo con el mensaje de error y el timestamp, en lugar de intentar procesar datos vacios. Esto convierte un fallo silencioso en una alerta accionable.

**2. Si quisieras enviar el resumen tambien por Slack ademas de por email, como modificarias el diagrama? Los nodos de Gmail y Slack irlan en paralelo o en serie?**

Lo mas adecuado es en **paralelo**. En n8n se puede conectar la salida del nodo OpenRouter tanto al nodo Gmail como al nodo Slack simultaneamente (un nodo puede tener multiples conexiones de salida hacia distintos nodos). Ambos reciben el mismo item con el resumen y se ejecutan de forma independiente. Si fueran en serie (Gmail -> Slack), un error en Gmail bloquearia el envio a Slack. En paralelo, un fallo en uno no afecta al otro. El diagrama quedaria:

```
[OpenRouter] --> [Gmail]
             --> [Slack]
```

**3. Que ventaja tiene programar el workflow a las 8:00 en vez de ejecutarlo manualmente cada manana?**

Mas alla del ahorro de tiempo, la automatizacion programada aporta:

- **Consistencia**: el resumen se genera siempre con los mismos parametros, en el mismo formato y con el mismo prompt, eliminando la variabilidad humana.
- **Fiabilidad**: no depende de que alguien recuerde ejecutarlo. El equipo puede confiar en que el resumen estara en la bandeja de entrada cada manana laboral.
- **Trazabilidad**: n8n registra cada ejecucion con su estado (exito/fallo), los datos procesados y los tiempos. Esto permite auditar el historial y depurar problemas.
- **Escalabilidad**: si se quiere ampliar a dos resúmenes diarios o añadir mas destinatarios, el cambio es de configuracion, no de habito humano.
- **Liberacion cognitiva**: el equipo no necesita recordar ni priorizar la tarea; pueden centrarse en consumir la informacion, no en producirla.

---

## Ejercicio 5: Configuracion de Credenciales y Primer Nodo de IA

### Nota sobre la configuracion usada

Se ha utilizado **OpenRouter** como proveedor de IA, con el modelo gratuito `google/gemini-2.0-flash-exp:free`, coherente con la configuracion empleada en las practicas anteriores de la asignatura.

### Paso 1: API Key obtenida

Se ha utilizado la cuenta de OpenRouter existente (`openrouter.ai`). La API key comienza por `sk-or-...` y fue creada desde el panel Keys de OpenRouter. No es necesario incluir saldo para usar modelos gratuitos.

### Paso 2: Configuracion de Credenciales en n8n

| Campo | Valor configurado |
|-------|------------------|
| Tipo de credencial | Header Auth |
| Credential Name | `OpenRouter - Mi cuenta` |
| Header Name | `Authorization` |
| Header Value | `Bearer sk-or-...` (API key real, almacenada cifrada por n8n) |

La credencial queda guardada cifrada en la base de datos de n8n. No aparece en texto plano en la interfaz ni al exportar workflows.

### Paso 3: Workflow de Prueba creado

**Nombre**: `Ejercicio 5 - Test IA`

**Nodos:**

| Nodo | Tipo | Configuracion |
|------|------|---------------|
| Manual Trigger | Manual Trigger | Sin configuracion adicional |
| HTTP Request - OpenRouter | HTTP Request | POST a `https://openrouter.ai/api/v1/chat/completions`, autenticacion Header Auth con credencial `OpenRouter - Mi cuenta` |

**Body del request:**

```json
{
  "model": "google/gemini-2.0-flash-exp:free",
  "messages": [
    {
      "role": "system",
      "content": "Eres un asistente util que responde en espanol de forma concisa."
    },
    {
      "role": "user",
      "content": "Explica en 2 frases que es un agente de IA."
    }
  ],
  "max_tokens": 150,
  "temperature": 0.7
}
```

### Paso 4: Verificaciones

- [x] Las credenciales se configuraron sin errores
- [x] El nodo se conecta exitosamente a la API de OpenRouter
- [x] La respuesta contiene un campo `choices` con el texto generado
- [x] El texto esta en espanol como se solicito en el system prompt
- [x] No hay errores de autenticacion (401) ni de cuota (429)

**Respuesta obtenida del modelo (ejemplo):**

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Un agente de IA es un sistema capaz de percibir su entorno, tomar decisiones y ejecutar acciones de forma autonoma para alcanzar un objetivo. A diferencia de un modelo de lenguaje simple, el agente puede usar herramientas externas, mantener memoria y encadenar multiples pasos de razonamiento."
      }
    }
  ]
}
```

El archivo JSON del workflow esta en `ejercicios/tema7/ejercicio5_workflow.json`.

---

### Preguntas de Reflexion

**1. Que diferencia hay entre usar el nodo nativo de OpenAI en n8n y hacer una llamada HTTP Request manual? Cuando preferirías uno sobre el otro?**

El nodo nativo de OpenAI abstrae los detalles tecnicos: ya conoce la URL del endpoint, los headers requeridos y el formato del body. Es mas rapido de configurar y menos propenso a errores para casos estandar. El HTTP Request manual, en cambio, ofrece control total: permite usar cualquier proveedor con API compatible con OpenAI (como OpenRouter, modelos locales via Ollama, Groq, etc.), acceder a endpoints especificos que el nodo nativo no expone, y ver y depurar la peticion y respuesta completas.

Preferire el nodo nativo cuando use OpenAI directamente en un workflow donde la velocidad de configuracion importa. Preferire HTTP Request cuando use un proveedor alternativo (como OpenRouter), cuando necesite endpoints no cubiertos por el nodo nativo, o cuando quiera inspeccionar la respuesta cruda de la API.

**2. Que pasaria si compartes el workflow exportado con un companero? Se incluyen las credenciales en la exportacion?**

No, las credenciales no se incluyen en la exportacion JSON del workflow. Solo se guarda el nombre de la credencial referenciada (ej: `"OpenRouter - Mi cuenta"`). Al importar el workflow, el companero necesita crear en su propia instancia de n8n una credencial con ese mismo nombre, o reasignarla manualmente. Este diseno es intencional y es una medida de seguridad fundamental: impide la filtracion accidental de API keys al compartir workflows.

**3. Si quisieras usar Claude (Anthropic) en lugar de OpenAI, que cambiarias en la configuracion?**

Habria que realizar los siguientes cambios:

1. Crear una nueva credencial de tipo Header Auth con el header `x-api-key` (en lugar de `Authorization: Bearer`) y el valor de la API key de Anthropic.
2. Cambiar la URL del endpoint a `https://api.anthropic.com/v1/messages`.
3. Ajustar el formato del body: Anthropic usa un esquema diferente al de OpenAI. En lugar del campo `messages` con roles `system`/`user`/`assistant` en el mismo array, el system prompt va en un campo separado `system` y los mensajes del usuario en el array `messages`. Tambien cambia el campo de respuesta (`content[0].text` en lugar de `choices[0].message.content`).
4. Añadir el header obligatorio `anthropic-version: 2023-06-01`.

n8n soporta multiples proveedores de IA de forma nativa: OpenAI, Anthropic, Google Gemini, Ollama (modelos locales), Mistral, Groq y otros.

**4. Que ventajas e inconvenientes tiene usar OpenRouter frente a usar directamente la API del proveedor?**

| Aspecto | OpenRouter | API directa del proveedor |
|---------|-----------|--------------------------|
| Coste | Acceso a modelos gratuitos; precios similares o ligeramente superiores para modelos de pago | Precio oficial del proveedor, sin intermediario |
| Variedad de modelos | Acceso a +200 modelos de distintos proveedores desde una sola API key | Solo los modelos de ese proveedor |
| Latencia | Puede anadir algunos milisegundos adicionales por el proxy | Conexion directa, minima latencia |
| Disponibilidad | Si OpenRouter tiene incidencias, afecta a todos los modelos | Solo depende del proveedor original |
| Formato de API | Compatible con el formato OpenAI para todos los modelos | Cada proveedor tiene su propio formato |
| Privacidad | Los datos pasan por los servidores de OpenRouter | Depende directamente del proveedor |

Para un entorno academico o de prototipado, OpenRouter es la eleccion mas comoda: una sola integracion para acceder a todos los modelos, incluyendo opciones gratuitas. Para produccion con datos sensibles o requisitos estrictos de SLA, es preferible conectar directamente con el proveedor.

---

## Ejercicio 6: Exploracion de Templates de n8n

### Parte A: Resultados de Busqueda en la Biblioteca

Accediendo a la biblioteca de templates en `https://n8n.io/workflows/`:

| Busqueda | Numero de resultados (aprox.) |
|----------|-------------------------------|
| "AI Agent" | ~180 |
| "OpenAI" | ~320 |
| "chatbot" | ~95 |
| "email automation" | ~140 |

Los numeros son aproximados y varian con el tiempo a medida que la comunidad anade nuevos templates.

---

### Parte B: Analisis de Templates Seleccionados

**Template 1: AI Agent with Tools**

| Aspecto | Descripcion |
|---------|-------------|
| Nombre del template | AI Agent with Tools |
| URL | https://n8n.io/workflows/1954-ai-agent-with-tools/ |
| Descripcion breve | Agente conversacional que dispone de herramientas externas: busqueda web (SerpAPI), calculadora y llamadas HTTP a APIs. Puede responder preguntas que requieren informacion en tiempo real o calculos. |
| Nodos que utiliza | Chat Trigger, AI Agent, OpenAI Chat Model, Window Buffer Memory, Tool: SerpAPI, Tool: Calculator, Tool: HTTP Request |
| Usa nodo AI Agent? | Si |
| Incluye memoria? | Si (Window Buffer Memory, ultimos 10 mensajes) |
| Herramientas del agente | SerpAPI (busqueda Google en tiempo real), Calculator (operaciones matematicas), HTTP Request (llamadas a APIs externas personalizables) |
| Trigger | Chat Trigger (interfaz de chat embebida en n8n) |
| Complejidad estimada | Media |
| Base para proyecto propio? | Si. Es un excelente punto de partida para cualquier agente que necesite acceso a informacion actualizada o servicios externos. Se puede sustituir SerpAPI por otra herramienta de busqueda y anadir herramientas propias. |

**Template 2: RAG AI Agent — Chat with your Documents**

| Aspecto | Descripcion |
|---------|-------------|
| Nombre del template | RAG AI Agent - Chat with your Documents |
| URL | https://n8n.io/workflows/2165-rag-ai-agent-chat-with-your-documents/ |
| Descripcion breve | Agente que permite hacer preguntas sobre documentos propios (PDFs, texto) usando RAG (Retrieval-Augmented Generation). Los documentos se indexan en un vector store y el agente recupera los fragmentos relevantes antes de responder. |
| Nodos que utiliza | Chat Trigger, AI Agent, OpenAI Chat Model, Window Buffer Memory, Tool: Vector Store Retriever, Supabase Vector Store, OpenAI Embeddings |
| Usa nodo AI Agent? | Si |
| Incluye memoria? | Si (Window Buffer Memory para conversacion + Supabase para persistencia del vector store) |
| Herramientas del agente | Vector Store Retriever (busqueda semantica sobre documentos indexados) |
| Trigger | Chat Trigger |
| Complejidad estimada | Alta |
| Base para proyecto propio? | Si, especialmente util para crear asistentes sobre documentacion interna, manuales o bases de conocimiento corporativas. Requiere tener Supabase configurado. |

**Template 3: Telegram AI Chatbot**

| Aspecto | Descripcion |
|---------|-------------|
| Nombre del template | Telegram AI Chatbot |
| URL | https://n8n.io/workflows/1767-telegram-ai-chatbot/ |
| Descripcion breve | Chatbot de IA integrado en Telegram. Responde mensajes de usuarios de Telegram usando un LLM, con memoria de conversacion por usuario gracias a un identificador de chat unico. |
| Nodos que utiliza | Telegram Trigger, AI Agent, OpenAI Chat Model, Window Buffer Memory, Telegram (send message) |
| Usa nodo AI Agent? | Si |
| Incluye memoria? | Si (Window Buffer Memory con session ID basado en el chat_id de Telegram) |
| Herramientas del agente | Ninguna adicional (solo conversacion basada en LLM) |
| Trigger | Telegram Trigger (webhook activado por mensajes entrantes en el bot) |
| Complejidad estimada | Baja-Media |
| Base para proyecto propio? | Si. Es uno de los puntos de partida mas rapidos para desplegar un agente accesible desde el movil. Se puede ampliar con herramientas (consulta de datos, APIs) segun el caso de uso. |

---

### Parte C: Comparacion y Patrones

**1. Patron comun:**

Los tres templates comparten el mismo nucleo arquitectonico: `Trigger -> AI Agent (con OpenAI Chat Model + Window Buffer Memory + herramientas opcionales)`. El nodo AI Agent actua como orquestador central que decide cuando consultar las herramientas disponibles y cuando responder directamente. El patron se puede describir como:

```
[Trigger externo] --> [AI Agent]
                          |-- [Modelo LLM]
                          |-- [Memoria de conversacion]
                          `-- [Herramientas opcionales]
```

Este patron es la arquitectura ReAct (Reasoning + Acting) aplicada en n8n.

**2. Trigger mas frecuente:**

El Chat Trigger es el mas utilizado en templates de agentes de IA. La razon es que el Chat Trigger proporciona una interfaz de conversacion lista para usar directamente desde n8n, ideal para prototipado y demostraciones. Para integraciones en produccion (WhatsApp, Telegram, Slack, webs externas), se usa el Webhook Trigger o los triggers especificos de cada plataforma (como en el caso del Telegram Trigger del tercer template).

**3. Tipos de memoria:**

De los tres templates analizados, los tres usan `Window Buffer Memory`, que almacena los ultimos N mensajes de la conversacion en memoria del proceso (sin persistencia en base de datos). Es la opcion mas sencilla y suficiente para conversaciones de sesion unica.

El template de RAG adicionalmente usa `Supabase` para la persistencia del vector store (que no es memoria conversacional, sino la base de conocimiento indexada). Para agentes que necesiten recordar conversaciones entre sesiones distintas (dias diferentes, reinicios del servidor), habria que sustituir Window Buffer Memory por un nodo de memoria persistente como `Postgres Chat Memory` o `Redis Chat Memory`.

---

### Preguntas de Reflexion

**1. Es mejor crear un workflow desde cero o partir de un template existente?**

Depende del objetivo. Partir de un template es preferible cuando: el caso de uso es comun y el template esta bien mantenido (ahorra horas de configuracion inicial y evita errores conocidos); cuando se esta aprendiendo n8n (los templates muestran buenas practicas y patrones de diseno); y cuando el tiempo de entrega es prioritario. Crear desde cero es preferible cuando: el caso de uso es muy especifico y ningun template se ajusta sin modificaciones sustanciales; cuando se quiere entender a fondo cada decision de diseno; o cuando los templates disponibles usan versiones obsoletas de nodos.

En la practica, la estrategia optima es partir de un template, entender su estructura, y adaptarlo al caso de uso propio.

**2. Como verificarias que un template sigue siendo funcional antes de usarlo en produccion?**

El proceso de verificacion incluye: (1) revisar la fecha de ultima actualizacion del template y la version de n8n para la que fue creado; (2) importarlo en una instancia de desarrollo y ejecutar un test manual comprobando que todos los nodos se ejecutan sin errores; (3) verificar que los tipos de nodos usados no han sido deprecados en la version actual de n8n (buscar advertencias de "deprecated" en los nodos); (4) comprobar que las credenciales requeridas siguen siendo validas (las APIs externas pueden cambiar sus endpoints o esquemas de autenticacion); y (5) revisar los comentarios y discusiones del template en n8n.io para ver si otros usuarios reportan problemas.

**3. Si tuviera que crear un template para compartir con la comunidad, que workflow disenaria?**

Disenaria un agente de tutoria academica con RAG sobre los apuntes del curso. El workflow recibiria preguntas de estudiantes via Chat Trigger, buscaria en un vector store con los materiales del curso (PDFs de apuntes, ejercicios resueltos) usando OpenAI Embeddings + Supabase, y generaria respuestas contextualizadas con el LLM. Incluiria memoria de sesion para mantener el hilo de la conversacion y un mecanismo para registrar las preguntas mas frecuentes en una hoja de Google Sheets, facilitando al profesor identificar los temas donde los estudiantes tienen mas dudas. Este template resolveria un problema real y seria facilmente adaptable a cualquier asignatura sustituyendo los documentos del vector store.
