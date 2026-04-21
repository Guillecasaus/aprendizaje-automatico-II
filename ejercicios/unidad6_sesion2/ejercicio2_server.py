"""
Ejercicio 2: Servidor MCP ampliado con Resources y Prompts.
Extiende el Ejercicio 1 añadiendo dos resources y dos prompt templates.
"""

from fastmcp import FastMCP
import math
import string
import random
import json
import sys
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

mcp = FastMCP(
    name="Herramientas Básicas",
    instructions="Servidor MCP con calculadora científica, conversor de unidades, generador de contraseñas, resources de configuración/estado y prompts de análisis."
)

# ---------------------------------------------------------------------------
# Tools (del Ejercicio 1)
# ---------------------------------------------------------------------------

@mcp.tool()
def calculadora(operacion: str, a: float, b: float = 0.0) -> str:
    """Realiza operaciones matemáticas.

    Args:
        operacion: Operación a realizar. Valores posibles: suma, resta,
                   multiplicacion, division, potencia, raiz, seno, coseno, logaritmo.
        a: Primer operando (o único operando para funciones como raíz, seno, etc.).
        b: Segundo operando (opcional, necesario para suma, resta, etc.).

    Returns:
        Resultado de la operación como texto descriptivo.
    """
    try:
        operaciones = {
            "suma": lambda: a + b,
            "resta": lambda: a - b,
            "multiplicacion": lambda: a * b,
            "division": lambda: a / b if b != 0 else "Error: división por cero",
            "potencia": lambda: a ** b,
            "raiz": lambda: math.sqrt(a) if a >= 0 else "Error: raíz de número negativo",
            "seno": lambda: math.sin(math.radians(a)),
            "coseno": lambda: math.cos(math.radians(a)),
            "logaritmo": lambda: math.log(a) if a > 0 else "Error: logaritmo de número no positivo",
        }

        if operacion not in operaciones:
            return f"Operación '{operacion}' no reconocida. Operaciones válidas: {', '.join(operaciones.keys())}"

        resultado = operaciones[operacion]()
        return f"{operacion}({a}, {b}) = {resultado}"
    except Exception as e:
        return f"Error al ejecutar la operación: {str(e)}"


@mcp.tool()
def conversor_unidades(valor: float, de: str, a: str) -> str:
    """Convierte entre diferentes unidades de medida.

    Args:
        valor: Cantidad a convertir.
        de: Unidad de origen (ej: km, m, cm, kg, g, lb, celsius, fahrenheit).
        a: Unidad de destino.

    Returns:
        Resultado de la conversión con las unidades indicadas.
    """
    try:
        longitud_a_metros = {
            "km": 1000, "m": 1, "cm": 0.01, "mm": 0.001,
            "mi": 1609.34, "ft": 0.3048, "in": 0.0254
        }
        peso_a_gramos = {
            "kg": 1000, "g": 1, "mg": 0.001,
            "lb": 453.592, "oz": 28.3495
        }

        if de in longitud_a_metros and a in longitud_a_metros:
            resultado = valor * longitud_a_metros[de] / longitud_a_metros[a]
            return f"{valor} {de} = {resultado:.4f} {a}"

        if de in peso_a_gramos and a in peso_a_gramos:
            resultado = valor * peso_a_gramos[de] / peso_a_gramos[a]
            return f"{valor} {de} = {resultado:.4f} {a}"

        conversiones_temp = {
            ("celsius", "fahrenheit"): lambda v: f"{v} °C = {v * 9/5 + 32:.2f} °F",
            ("fahrenheit", "celsius"): lambda v: f"{v} °F = {(v - 32) * 5/9:.2f} °C",
            ("celsius", "kelvin"):     lambda v: f"{v} °C = {v + 273.15:.2f} K",
            ("kelvin", "celsius"):     lambda v: f"{v} K = {v - 273.15:.2f} °C",
        }
        if (de, a) in conversiones_temp:
            return conversiones_temp[(de, a)](valor)

        return f"No se puede convertir de '{de}' a '{a}'. Verifica las unidades."
    except Exception as e:
        return f"Error en la conversión: {str(e)}"


@mcp.tool()
def generar_contrasena(longitud: int = 16, incluir_simbolos: bool = True) -> str:
    """Genera una contraseña aleatoria segura.

    Args:
        longitud: Longitud de la contraseña (entre 8 y 128 caracteres).
        incluir_simbolos: Si es True, incluye caracteres especiales (!@#$%...).

    Returns:
        Contraseña generada aleatoriamente con indicador de fortaleza.
    """
    if longitud < 8:
        return "Error: la longitud mínima es 8 caracteres."
    if longitud > 128:
        return "Error: la longitud máxima es 128 caracteres."

    caracteres = string.ascii_letters + string.digits
    if incluir_simbolos:
        caracteres += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))

    tiene_mayusculas = any(c.isupper() for c in contrasena)
    tiene_minusculas = any(c.islower() for c in contrasena)
    tiene_numeros = any(c.isdigit() for c in contrasena)
    tiene_especiales = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in contrasena)

    fortaleza_score = sum([tiene_mayusculas, tiene_minusculas, tiene_numeros, tiene_especiales])
    fortaleza = {1: "Débil", 2: "Media", 3: "Fuerte", 4: "Muy fuerte"}.get(fortaleza_score, "Débil")

    return f"Contraseña: {contrasena}\nLongitud: {longitud}\nFortaleza: {fortaleza}"


@mcp.tool()
def consultar_hora(zona_horaria: str = "Europe/Madrid") -> str:
    """Devuelve la fecha y hora actual en la zona horaria especificada.

    Args:
        zona_horaria: Nombre de la zona horaria IANA (ej: Europe/Madrid, America/New_York).

    Returns:
        Fecha y hora actual formateada en la zona horaria solicitada.
    """
    try:
        tz = ZoneInfo(zona_horaria)
        ahora = datetime.now(tz)
        return (
            f"Zona horaria: {zona_horaria}\n"
            f"Fecha y hora: {ahora.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"UTC offset: {ahora.strftime('%z')}"
        )
    except ZoneInfoNotFoundError:
        return f"Error: zona horaria '{zona_horaria}' no encontrada."
    except Exception as e:
        return f"Error al consultar la hora: {str(e)}"


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

@mcp.resource("config://servidor")
def obtener_configuracion() -> str:
    """Configuración actual del servidor MCP y sus capacidades."""
    config = {
        "nombre": "Herramientas Básicas",
        "version": "1.0.0",
        "herramientas_disponibles": [
            "calculadora",
            "conversor_unidades",
            "generar_contrasena",
            "consultar_hora",
        ],
        "unidades_soportadas": {
            "longitud": ["km", "m", "cm", "mm", "mi", "ft", "in"],
            "peso": ["kg", "g", "mg", "lb", "oz"],
            "temperatura": ["celsius", "fahrenheit", "kelvin"],
        },
        "operaciones_calculadora": [
            "suma", "resta", "multiplicacion", "division",
            "potencia", "raiz", "seno", "coseno", "logaritmo",
        ],
    }
    return json.dumps(config, indent=2, ensure_ascii=False)


@mcp.resource("status://servidor")
def obtener_estado() -> str:
    """Estado actual del servidor incluyendo timestamp y métricas básicas."""
    estado = {
        "estado": "activo",
        "timestamp": datetime.now().isoformat(),
        "uptime_info": "Servidor funcionando correctamente",
        "version_python": sys.version,
        "modulos_cargados": ["math", "string", "random", "json", "datetime", "zoneinfo"],
    }
    return json.dumps(estado, indent=2, ensure_ascii=False)


@mcp.resource("conversion://{de}/{a}")
def tabla_conversion(de: str, a: str) -> str:
    """Tabla de factores de conversión entre dos unidades del mismo tipo.

    Args:
        de: Unidad de origen.
        a:  Unidad de destino.

    Returns:
        JSON con la tabla de conversión para valores representativos.
    """
    longitud_a_metros = {
        "km": 1000, "m": 1, "cm": 0.01, "mm": 0.001,
        "mi": 1609.34, "ft": 0.3048, "in": 0.0254,
    }
    peso_a_gramos = {
        "kg": 1000, "g": 1, "mg": 0.001,
        "lb": 453.592, "oz": 28.3495,
    }

    valores_muestra = [1, 5, 10, 50, 100, 500, 1000]
    tabla = []

    for familia in (longitud_a_metros, peso_a_gramos):
        if de in familia and a in familia:
            for v in valores_muestra:
                tabla.append({
                    "origen": f"{v} {de}",
                    "destino": f"{v * familia[de] / familia[a]:.4f} {a}",
                })
            return json.dumps({"conversion": f"{de} → {a}", "tabla": tabla}, indent=2, ensure_ascii=False)

    return json.dumps({"error": f"No se puede generar tabla para '{de}' → '{a}'"}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

@mcp.prompt()
def analizar_conversion(valor: float, unidad_origen: str, contexto: str = "general") -> str:
    """Prompt para analizar una conversión de unidades en contexto.

    Args:
        valor: Valor numérico a analizar.
        unidad_origen: Unidad del valor proporcionado.
        contexto: Contexto de uso (ej: cocina, ingeniería, ciencia, viaje).
    """
    return f"""Eres un experto en unidades de medida y conversiones.

Se te proporciona el siguiente valor: {valor} {unidad_origen}

Contexto de uso: {contexto}

Por favor:
1. Convierte este valor a las 3 unidades más relevantes para el contexto indicado.
   Usa la herramienta 'conversor_unidades' para cada conversión.
2. Explica en qué situaciones prácticas del contexto '{contexto}' se usaría cada unidad.
3. Indica si el valor proporcionado está dentro de rangos habituales para ese contexto.

Responde de forma clara y estructurada."""


@mcp.prompt()
def generar_informe_seguridad(
    longitud_minima: int = 12,
    num_contrasenas: int = 5,
) -> str:
    """Prompt para generar un informe de seguridad de contraseñas.

    Args:
        longitud_minima: Longitud mínima de las contraseñas a evaluar.
        num_contrasenas: Número de contraseñas a generar para el análisis.
    """
    return f"""Eres un experto en ciberseguridad y gestión de contraseñas.

Realiza las siguientes tareas:

1. Genera {num_contrasenas} contraseñas usando la herramienta 'generar_contrasena':
   - 2 contraseñas de {longitud_minima} caracteres SIN símbolos
   - 2 contraseñas de {longitud_minima} caracteres CON símbolos
   - 1 contraseña de {longitud_minima + 8} caracteres CON símbolos

2. Para cada contraseña generada, analiza:
   - Fortaleza reportada por la herramienta
   - Tiempo estimado de cracking por fuerza bruta
   - Vulnerabilidades potenciales

3. Elabora un informe con:
   - Tabla comparativa de las contraseñas
   - Recomendaciones de mejores prácticas
   - Política de contraseñas sugerida para una organización

Presenta el informe de forma profesional y estructurada."""


@mcp.prompt()
def analisis_completo(tema: str) -> str:
    """Prompt que combina las tres herramientas para un análisis multidimensional.

    Args:
        tema: Tema o escenario sobre el que realizar el análisis (ej: 'planificación de un viaje a EEUU').
    """
    return f"""Eres un asistente analítico con acceso a calculadora, conversor de unidades y generador de contraseñas.

Tema del análisis: {tema}

Realiza un análisis completo que incluya:

1. **Cálculos relevantes**: Usa 'calculadora' para al menos 2 operaciones matemáticas útiles en este contexto.
2. **Conversiones útiles**: Usa 'conversor_unidades' para convertir al menos 3 magnitudes relevantes para el tema.
3. **Seguridad**: Usa 'generar_contrasena' para crear credenciales seguras si el tema involucra accesos digitales.

Estructura tu respuesta con secciones claramente diferenciadas y explica por qué cada herramienta es relevante para el tema propuesto."""


if __name__ == "__main__":
    mcp.run()
