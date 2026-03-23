# Documentación Práctica Unidad 4
## Agente de IA con n8n — Caso 1: Atención al Cliente eCommerce

**Autor:** Guillermo Casaus
**Fecha:** Marzo 2026
**Caso elegido:** Caso 1 — Agente de Atención al Cliente para eCommerce

---

## 1. Descripción del Agente

Se ha construido **TechBot**, un agente de atención al cliente para la tienda ficticia **TechStore**, especializada en accesorios y periféricos tecnológicos. El agente es capaz de:

- Consultar el inventario real desde Google Sheets
- Informar sobre disponibilidad, stock y precios de productos
- Responder sobre las políticas de la tienda (envíos, devoluciones, garantía)
- Rechazar inventar productos que no existan en el catálogo
- Mantener el contexto de la conversación gracias a la memoria

---

## 2. Arquitectura del Workflow

El workflow sigue el patrón fundamental de agente de IA:

```
[Chat Trigger] → [AI Agent]
                      ├── [OpenAI Chat Model - gpt-4o-mini]  (ai_languageModel)
                      ├── [Window Buffer Memory - 10 msgs]   (ai_memory)
                      └── [Google Sheets - Inventario]        (ai_tool)
```

| Nodo | Tipo | Función |
|------|------|---------|
| Chat Trigger | `@n8n/n8n-nodes-langchain.chatTrigger` | Recibe los mensajes del usuario |
| AI Agent | `@n8n/n8n-nodes-langchain.agent` | Orquesta el LLM, la memoria y las herramientas |
| OpenAI Chat Model | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | Modelo gpt-4o-mini como motor de razonamiento |
| Window Buffer Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | Recuerda los últimos 10 mensajes de la conversación |
| Google Sheets | `n8n-nodes-base.googleSheetsTool` | Consulta el inventario de productos en tiempo real |

> **Captura del workflow completo:**
> *(Añadir aquí captura limpia del editor de n8n con todos los nodos visibles)*

---

## 3. Inventario de Productos (Google Sheets)

La hoja `Inventario` contiene 10 productos con las columnas: ID, Nombre, Descripción, Precio (€), Stock, Categoría.

| ID | Nombre | Precio (€) | Stock | Categoría |
|----|--------|-----------|-------|-----------|
| 001 | Auriculares Bluetooth ProSound X1 | 89.99 | 15 | Audio |
| 002 | Auriculares Gaming RGB | 59.99 | 8 | Gaming |
| 003 | Altavoz Portátil WaveBox | 49.99 | **0** | Audio |
| 004 | Teclado Mecánico TactilePro | 74.99 | 22 | Periféricos |
| 005 | Ratón Ergonómico ErgoClick | 39.99 | 5 | Periféricos |
| 006 | Hub USB-C 7en1 | 34.99 | 12 | Conectividad |
| 007 | Cámara Webcam 4K StreamPro | 109.99 | **0** | Imagen |
| 008 | Soporte Monitor Articulado | 44.99 | 7 | Accesorios |
| 009 | Cable USB-C Trenzado 2m | 14.99 | 50 | Conectividad |
| 010 | Alfombrilla XL DeskMate | 24.99 | 18 | Accesorios |

---

## 4. System Prompt del Agente

> **Captura del System Prompt:**
> *(Añadir aquí captura del campo System Message en el nodo AI Agent)*

```
# Rol
Eres TechBot, el asistente virtual de atención al cliente de TechStore, una tienda online
especializada en accesorios y periféricos tecnológicos. Tu objetivo es ayudar a los clientes
de forma amable, honesta y profesional.

# Tareas
- Cuando un cliente pregunte por productos, usa SIEMPRE la herramienta de Google Sheets
  para consultar el inventario actualizado antes de responder
- Informa sobre disponibilidad (stock), precios y características de los productos
- Ayuda al cliente a encontrar el producto más adecuado para sus necesidades
- Responde sobre las políticas de la tienda cuando se te pregunte

# Restricciones
- NUNCA inventes productos que no aparezcan en el inventario
- NUNCA afirmes que un producto está disponible si su stock es 0
- NO modifiques los precios ni la información del inventario
- Si un producto no existe en el catálogo, dilo honestamente y ofrece alternativas reales
- No hagas promesas de entrega o disponibilidad futura que no puedas garantizar

# Políticas de la tienda
- Envíos: Envío gratuito en pedidos superiores a 50€. Entrega estimada: 3-5 días laborables
- Devoluciones: 30 días naturales para devoluciones sin necesidad de justificación,
  producto en buen estado
- Garantía: 2 años de garantía oficial en todos los productos
- Pago: Tarjeta bancaria, PayPal y transferencia bancaria
- Atención: Lunes a viernes de 9h a 18h en soporte@techstore.es

# Formato de respuesta
- Tono amable, cercano y profesional
- Cuando listes productos, muestra: nombre, precio y disponibilidad (unidades o "Agotado")
- Respuestas concisas, máximo 250 palabras
- Si el cliente duda entre varios productos, ayúdale a elegir con preguntas sobre su uso
```

---

## 5. Conversaciones de Prueba

### Caso 1 — Consulta de productos disponibles por categoría

**Objetivo:** Verificar que el agente consulta el inventario real y filtra por categoría correctamente.

**Conversación:**
> **Usuario:** Hola, ¿qué auriculares tenéis disponibles?

**Respuesta del agente:**
El agente consultó automáticamente el inventario vía Google Sheets y devolvió los dos auriculares disponibles en catálogo con su precio y stock:
- **Auriculares Bluetooth ProSound X1** — 89.99€ — 15 unidades en stock
- **Auriculares Gaming RGB** — 59.99€ — 8 unidades en stock

Además ofreció ayuda para elegir según el uso (gaming, trabajo, etc.).

**Resultado:** Correcto. El agente consultó el inventario, filtró por categoría Audio/Gaming y mostró solo productos reales con disponibilidad.

![Caso 1 - Consulta de auriculares disponibles](./caso_1.png)

---

### Caso 2 — Producto agotado y oferta de alternativas

**Objetivo:** Verificar que el agente identifica correctamente un producto con stock=0 y no afirma disponibilidad falsa.

**Conversación:**
> **Usuario:** *(Continuación del caso anterior)* Me interesa el Altavoz Portátil WaveBox, ¿lo tenéis?

**Respuesta del agente:**
El agente indicó claramente que el Altavoz Portátil WaveBox está **agotado** (sin stock disponible) y ofreció proactivamente alternativas similares del catálogo, sin inventar disponibilidad futura.

**Resultado:** Correcto. El agente respetó la restricción de no confirmar disponibilidad cuando stock=0 y orientó al usuario hacia alternativas reales.

![Caso 2 - Producto agotado](./caso_2.png)

---

### Caso 3 — Políticas de la tienda

**Objetivo:** Verificar que el agente responde sobre políticas sin necesidad de consultar el inventario.

**Conversación:**
> **Usuario:** ¿Quiero comprar el Altavoz Portátil WaveBox, ¿lo tenéis?
> **Usuario:** ¿Cuál es la política de devoluciones?

**Respuesta del agente:**
Tras confirmar de nuevo que el WaveBox está agotado, respondió la pregunta sobre devoluciones detallando:
- 30 días naturales para devoluciones
- Producto debe estar en buen estado y con todos sus accesorios
- Proceso de contacto con el servicio de atención al cliente

**Resultado:** Correcto. El agente combinó información de inventario (producto agotado) con políticas de tienda (devoluciones) en la misma conversación, sin mezclar ni confundir datos.

![Caso 3 - Políticas de devolución](./caso_3.png)

---

### Caso 4 — Producto inexistente: honestidad y alternativas reales

**Objetivo:** Verificar que el agente no inventa productos que no están en el catálogo.

**Conversación:**
> **Usuario:** ¿Tenéis monitores gaming?

**Respuesta del agente:**
El agente consultó el inventario, no encontró monitores y respondió honestamente: *"Lo siento, actualmente no tenemos monitores gaming en nuestro inventario"*. A continuación ofreció productos relacionados disponibles:
- Auriculares Gaming RGB — 59.99€ — 8 unidades
- Teclado Mecánico TactilePro — 74.99€ — 22 unidades
- Ratón Ergonómico ErgoClick — 39.99€ — 5 unidades

En los logs se puede observar la llamada a Google Sheets retornando el inventario completo antes de formular la respuesta.

**Resultado:** Correcto. El agente no inventó ningún monitor, comunicó la ausencia honestamente y ofreció alternativas reales del catálogo.

![Caso 4 - Producto inexistente](./caso_4.png)

---

### Caso 5 — Conversación con contexto y combinación de inventario + políticas

**Objetivo:** Verificar la memoria conversacional y la capacidad de combinar datos del inventario con las políticas de envío.

**Conversación:**
> **Usuario:** Si compro el Hub USB-C, ¿el envío es gratis?

**Respuesta del agente:**
El agente consultó el inventario para confirmar el precio del Hub USB-C 7en1 (34.99€, 12 unidades en stock) y luego aplicó la política de envíos (gratuito en pedidos superiores a 50€), concluyendo que la compra del Hub solo **no alcanza el mínimo** para envío gratuito. Proactivamente sugirió combinaciones de productos del catálogo para superar los 50€:
- Alfombrilla XL DeskMate — 24.99€ — 18 unidades
- Ratón Ergonómico ErgoClick — 39.99€ — 5 unidades
- Cable USB-C Trenzado 2m — 14.99€ — 50 unidades

Calculó que Hub + Cable = 49.98€, aún insuficiente, y ofreció seguir ayudando a encontrar la combinación óptima.

**Resultado:** Correcto. El agente razonó combinando datos reales del inventario (precio del Hub) con las reglas de negocio (umbral de envío gratuito), demostrando capacidad de razonamiento contextualizado.

![Caso 5 - Envío gratuito y contexto encadenado](./caso_5.png)

---

## 6. Resumen de Resultados

| Caso | Objetivo | Resultado |
|------|----------|-----------|
| 1 | Consulta de productos por categoría | Correcto |
| 2 | Producto agotado (stock=0) | Correcto |
| 3 | Políticas de la tienda | Correcto |
| 4 | Producto inexistente, sin inventar | Correcto |
| 5 | Combinación inventario + políticas + contexto | Correcto |

En todos los casos el agente:
- Consultó el inventario antes de responder sobre productos
- Respetó las restricciones definidas en el System Prompt
- Mantuvo un tono profesional y orientado a la solución

---

## 7. Reflexión Personal

**¿Qué caso práctico elegiste y por qué?**

Elegí el Caso 1 de atención al cliente para eCommerce porque representa uno de los casos de uso más frecuentes y tangibles de los agentes de IA en entornos reales. La combinación de una herramienta externa (Google Sheets como inventario) con una LLM y memoria conversacional permite construir un sistema funcional con muy poco código, lo cual ilustra perfectamente el potencial de n8n como plataforma de automatización con IA.

**¿Qué dificultades encontraste durante el desarrollo?**

La principal dificultad fue la configuración correcta del nodo de Google Sheets como herramienta del agente (conexión vía `ai_tool` en lugar de la conexión `main` habitual). Al principio el agente no consultaba el inventario porque la conexión no estaba bien tipada. También fue importante redactar el System Prompt de forma precisa: instrucciones demasiado vagas hacían que el agente no siempre usara la herramienta antes de responder sobre productos.

**¿Qué mejoras añadirías si tuvieras más tiempo?**

- **Memoria persistente** con PostgreSQL o Supabase, para que el historial de conversación no se pierda entre sesiones
- **Integración con Telegram** para que los clientes puedan usar el agente desde un canal de mensajería real
- **Herramienta de búsqueda semántica** en lugar de cargar todo el inventario, más eficiente con catálogos grandes
- **Nodo de escalado a agente humano** cuando el agente detecte una queja o situación compleja que no sabe resolver

**¿Cómo aplicarías este tipo de agentes en un contexto profesional real?**

Este patrón (LLM + herramienta de datos + memoria) es directamente aplicable en cualquier empresa con catálogo de productos, base de conocimiento o FAQ. Sin necesidad de desarrollar una aplicación desde cero, n8n permite conectar un modelo de lenguaje con los sistemas existentes (ERP, CRM, Google Sheets, bases de datos) y desplegar el agente en canales como Telegram, WhatsApp Business o una web. El valor principal está en la reducción de carga sobre el equipo de soporte para consultas repetitivas, liberando tiempo humano para casos complejos.

---

## 8. Archivos Entregados

| Archivo | Descripción |
|---------|-------------|
| `Agente Atención al Cliente - TechStore.json` | Workflow exportado desde n8n |
| `inventario_techstore.csv` | Datos del inventario importados en Google Sheets |
| `documentacion_practica_unidad4.md` | Este documento |
