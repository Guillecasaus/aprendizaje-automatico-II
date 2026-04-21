from fastmcp import FastMCP
import math
import string
import random
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

mcp = FastMCP(
    name="Herramientas Básicas",
    instructions="Servidor MCP con calculadora científica, conversor de unidades y generador de contraseñas."
)


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

        if de == "celsius" and a == "fahrenheit":
            return f"{valor} °C = {valor * 9/5 + 32:.2f} °F"
        if de == "fahrenheit" and a == "celsius":
            return f"{valor} °F = {(valor - 32) * 5/9:.2f} °C"
        if de == "celsius" and a == "kelvin":
            return f"{valor} °C = {valor + 273.15:.2f} K"
        if de == "kelvin" and a == "celsius":
            return f"{valor} K = {valor - 273.15:.2f} °C"

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
        zona_horaria: Nombre de la zona horaria IANA (ej: Europe/Madrid, America/New_York, Asia/Tokyo).

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
        return f"Error: zona horaria '{zona_horaria}' no encontrada. Usa nombres IANA como 'Europe/Madrid'."
    except Exception as e:
        return f"Error al consultar la hora: {str(e)}"


if __name__ == "__main__":
    mcp.run()
