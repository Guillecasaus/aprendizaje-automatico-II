# Ejercicio 5: Diseño de Servidor MCP para Caso Real

## Caso elegido: C — Sistema de Gestión de Tickets de Soporte IT

El departamento de IT de una empresa gestiona incidencias técnicas mediante un asistente MCP
que permite crear, asignar, actualizar y analizar tickets en lenguaje natural.

---

## Paso 1: Análisis del caso

**Actores principales:**
- Técnico de soporte de nivel 1/2 (usuario principal del asistente)
- Coordinador IT (acceso a estadísticas y asignaciones masivas)
- Sistema automatizado de monitorización (creación automática de tickets)

**Acciones necesarias:**
- Crear un nuevo ticket con descripción, prioridad y categoría
- Asignar o reasignar un ticket a un técnico concreto
- Cambiar el estado de un ticket (abierto → en progreso → resuelto → cerrado)
- Buscar tickets similares ya resueltos para reutilizar soluciones
- Consultar estadísticas de resolución por técnico / categoría / período

**Fuentes de datos:**
- Base de datos relacional (PostgreSQL) con tabla `tickets`, `usuarios`, `categorias`
- Sistema de notificaciones (Slack / email)
- Directorio LDAP/AD para resolución de usuarios

---

## Paso 2: Diseño de Tools

| Herramienta | Descripción (para el LLM) | Parámetros | Retorno | Permisos necesarios |
|-------------|---------------------------|------------|---------|---------------------|
| `crear_ticket` | Abre un nuevo ticket de soporte. Úsala cuando el usuario reporte un problema nuevo que no tenga ticket previo. | `titulo: str`, `descripcion: str`, `prioridad: str` (baja/media/alta/critica), `categoria: str`, `usuario_afectado: str` (email) | JSON con `ticket_id`, `estado`, `fecha_creacion`, `url_seguimiento` | escritura |
| `consultar_ticket` | Recupera toda la información de un ticket por su ID. Úsala para verificar el estado actual antes de actualizar. | `ticket_id: int` | JSON completo del ticket (estado, asignado, historial de comentarios, SLA) | lectura |
| `actualizar_estado` | Cambia el estado de un ticket existente y añade un comentario al historial. | `ticket_id: int`, `nuevo_estado: str` (en_progreso/resuelto/cerrado/reabierto), `comentario: str` | Confirmación con estado anterior y nuevo | escritura |
| `asignar_ticket` | Asigna o reasigna un ticket a un técnico del equipo. Úsala cuando el técnico actual esté sobrecargado o no sea el experto adecuado. | `ticket_id: int`, `tecnico_email: str`, `motivo: str` | Confirmación de asignación y notificación enviada | escritura |
| `buscar_tickets_similares` | Busca en el histórico tickets resueltos parecidos al texto dado. Útil para encontrar soluciones previas antes de escalar. | `descripcion: str`, `categoria: str` (opcional), `limite: int` (default 5) | Lista de tickets similares con `ticket_id`, `titulo`, `solucion_aplicada`, `similitud_score` | lectura |
| `estadisticas_soporte` | Genera estadísticas de rendimiento del equipo de soporte. Solo para coordinadores. | `fecha_inicio: str` (ISO), `fecha_fin: str` (ISO), `agrupar_por: str` (tecnico/categoria/prioridad) | JSON con métricas: tickets_abiertos, tiempo_medio_resolución, SLA_cumplido_pct | lectura + admin |

---

## Paso 3: Diseño de Resources

| URI del Resource | Descripción | Tipo de dato | Frecuencia de actualización |
|------------------|-------------|--------------|----------------------------|
| `config://soporte/categorias` | Catálogo completo de categorías de incidencias con sus SLAs asociados (hardware, software, red, accesos, etc.) | JSON | Estático (se actualiza manualmente al añadir categorías) |
| `config://soporte/tecnicos` | Directorio de técnicos disponibles con su especialización y carga actual de tickets | JSON | Dinámico (se recalcula cada 5 minutos) |
| `status://soporte/kpis` | KPIs en tiempo real del servicio: tickets abiertos por prioridad, tickets fuera de SLA, técnico con más carga | JSON | Dinámico (tiempo real, se refresca por petición) |
| `plantillas://soporte/respuestas` | Plantillas de respuesta estándar para incidencias frecuentes (restablecimiento de contraseña, VPN, impresora) | JSON con texto markdown | Semi-estático (actualizado por el coordinador) |

---

## Paso 4: Diseño de Prompts

| Nombre del Prompt | Objetivo | Parámetros | Tools que utiliza |
|-------------------|----------|------------|-------------------|
| `triaje_incidencia` | Guía al LLM para analizar una incidencia nueva, buscar duplicados y crear el ticket con la prioridad correcta | `descripcion_usuario: str`, `usuario_afectado: str` | `buscar_tickets_similares`, `crear_ticket` |
| `informe_turno` | Genera el informe de cierre de turno para un técnico: tickets gestionados, pendientes y escalados | `tecnico_email: str`, `fecha: str` | `estadisticas_soporte`, `consultar_ticket` |
| `resolver_incidencia_conocida` | Dado un ticket abierto, busca la solución en el histórico y propone los pasos de resolución al técnico | `ticket_id: int` | `consultar_ticket`, `buscar_tickets_similares`, `actualizar_estado` |

---

## Paso 5: Seguridad y Despliegue

```
SEGURIDAD:
- Autenticación: JWT con OAuth2 Client Credentials Flow. El auth server es el
  mismo Active Directory de la empresa via OIDC. Tokens con TTL de 1 hora.
- Autorización: Mixta por roles + por herramienta.
  · Rol "tecnico": puede usar crear_ticket, consultar_ticket, actualizar_estado,
    asignar_ticket, buscar_tickets_similares.
  · Rol "coordinador": acceso total incluyendo estadisticas_soporte.
  · El claim "allowed_tools" del JWT restringe herramientas por usuario.
- Datos sensibles: descripciones de tickets (pueden contener contraseñas en claro
  por error del usuario), datos personales del usuario_afectado → cifrado AES-256
  en base de datos, enmascaramiento en logs.
- Validación de inputs: ticket_id debe ser un entero positivo existente en BD;
  tecnico_email debe pertenecer al dominio corporativo (@empresa.com);
  fechas en formato ISO 8601; prioridad sólo acepta enum definido;
  longitud máxima de descripcion: 4000 caracteres.
- Logging: registrar OBLIGATORIAMENTE: creación/modificación de tickets (quién,
  cuándo, qué cambió), asignaciones, accesos a estadísticas, errores de
  autenticación/autorización. Retención 1 año (auditoría GDPR).

DESPLIEGUE:
- Transporte: Streamable HTTP (permite múltiples clientes concurrentes y
  despliegue como servicio REST estándar; stdio solo válido para uso local).
- Infraestructura: Contenedor Docker detrás de nginx como reverse proxy TLS.
  Desplegado en el clúster Kubernetes corporativo en namespace "soporte-it".
  ConfigMap para variables de entorno, Secret para credenciales de BD.
- Escalabilidad: Horizontal Pod Autoscaler (HPA) en Kubernetes basado en
  CPU > 70% o latencia p95 > 2s. La sesión es stateless (JWT), por lo que
  cualquier réplica puede atender cualquier request. Pool de conexiones PgBouncer
  para la BD.
- Monitorización: Prometheus + Grafana. Métricas clave: latencia por tool,
  tasa de error, tokens JWT rechazados, tickets creados/min. Alertas si
  latencia p99 > 5s o tasa de error > 5%.
- Backup y recuperación: Snapshots diarios de la BD PostgreSQL a S3 corporativo
  con retención 30 días. RTO objetivo: 4h. RPO: 24h. Playbook de recuperación
  documentado en Confluence.
```

---

## Diagrama de Arquitectura

```
                    ┌──────────────────┐
                    │   Auth Server    │
                    │   (OIDC/AD)      │
                    └────────┬─────────┘
                             │ JWT
                             ▼
┌─────────────┐    HTTPS    ┌──────────────────────────────────────────┐
│  Claude /   │ ──────────► │  nginx (TLS termination + rate limit)    │
│  LLM Client │             └──────────────┬───────────────────────────┘
└─────────────┘                            │ HTTP interno
                                           ▼
                             ┌─────────────────────────┐
                             │   Servidor MCP           │
                             │   (FastMCP + Python)     │
                             │                          │
                             │  Tools:                  │
                             │   crear_ticket           │
                             │   consultar_ticket       │
                             │   actualizar_estado      │
                             │   asignar_ticket         │
                             │   buscar_similares       │
                             │   estadisticas_soporte   │
                             │                          │
                             │  Resources:              │
                             │   config://soporte/...   │
                             │   status://soporte/kpis  │
                             │   plantillas://...       │
                             └──────┬──────────┬────────┘
                                    │          │
                         ┌──────────▼──┐  ┌────▼──────────┐
                         │ PostgreSQL   │  │ Slack / Email  │
                         │ (tickets BD) │  │ (notificaciones│
                         └─────────────┘  └────────────────┘
```

---

## Diagrama de Secuencia — Flujo completo: Triaje de incidencia

```
Técnico IT          LLM (Claude)        Servidor MCP         Base de Datos
    │                    │                    │                    │
    │  "Tengo un         │                    │                    │
    │  problema con      │                    │                    │
    │  la VPN"           │                    │                    │
    │ ──────────────────►│                    │                    │
    │                    │                    │                    │
    │                    │ [Decide usar       │                    │
    │                    │  prompt triaje]    │                    │
    │                    │                    │                    │
    │                    │ tool_use:          │                    │
    │                    │ buscar_similares   │                    │
    │                    │ ("problema VPN")   │                    │
    │                    │ ──────────────────►│                    │
    │                    │                    │ SELECT similares   │
    │                    │                    │ ──────────────────►│
    │                    │                    │ [{id:142,          │
    │                    │                    │  solucion:...}]    │
    │                    │                    │ ◄──────────────────│
    │                    │ [3 tickets         │                    │
    │                    │  similares         │                    │
    │                    │  encontrados]      │                    │
    │                    │ ◄──────────────────│                    │
    │                    │                    │                    │
    │                    │ [Solución conocida │                    │
    │                    │  → crear ticket    │                    │
    │                    │  con prioridad     │                    │
    │                    │  media]            │                    │
    │                    │                    │                    │
    │                    │ tool_use:          │                    │
    │                    │ crear_ticket(...)  │                    │
    │                    │ ──────────────────►│                    │
    │                    │                    │ INSERT ticket      │
    │                    │                    │ ──────────────────►│
    │                    │                    │ {id:501, url:...}  │
    │                    │                    │ ◄──────────────────│
    │                    │ ticket_id: 501     │                    │
    │                    │ ◄──────────────────│                    │
    │                    │                    │                    │
    │  "Ticket #501      │                    │                    │
    │  creado. Solución  │                    │                    │
    │  sugerida: reinicia│                    │                    │
    │  el cliente VPN    │                    │                    │
    │  y borra caché"    │                    │                    │
    │ ◄──────────────────│                    │                    │
```
