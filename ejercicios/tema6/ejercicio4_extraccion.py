"""
Ejercicio 4: Extracción Estructurada
Unidad 3, Sesión 2 - Acceso Programático a LLMs

Extrae datos estructurados en JSON a partir de textos libres,
con validación y lógica de reintentos ante JSON inválido.
Requiere OPENROUTER_API_KEY en el archivo .env
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Opción B - OpenRouter (gratuito)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
MODEL = "google/gemini-2.0-flash-exp:free"

SYSTEM_PROMPT = """Eres un sistema de extracción de información. Tu tarea es extraer datos
estructurados de textos no estructurados y devolver ÚNICAMENTE un JSON válido.

Reglas:
- Responde SOLO con el JSON, sin texto adicional, sin bloques de código markdown.
- Si un campo no se encuentra en el texto, usa el valor "No especificado".
- Los valores numéricos deben ser números, no strings.
- Las fechas deben estar en formato YYYY-MM-DD cuando sea posible.
"""

# ---------------------------------------------------------------------------
# Textos de entrada
# ---------------------------------------------------------------------------

texto_empleo = """
Unete a nuestro equipo! Buscamos Desarrollador Senior Python para nuestra
oficina en Madrid. Ofrecemos salario de 45.000-55.000€ brutos anuales,
teletrabajo 3 días por semana y seguro médico privado. Requisitos: 5 años
de experiencia, conocimientos en Django y PostgreSQL. Incorporación inmediata.
Enviar CV a empleo@techcorp.es antes del 15 de marzo de 2025.
"""

texto_resena = """
Compré el portátil UltraBook X15 hace 2 semanas. La pantalla de 15 pulgadas
es espectacular y la batería dura unas 10 horas reales. Sin embargo, el
teclado es un poco incómodo para escribir largo rato y se calienta bastante
con tareas pesadas. Por el precio de 1.299€ creo que está bien, pero no es
perfecto. Le doy un 7 de 10. Lo compré en Amazon el 20 de enero de 2025.
"""

texto_noticia = """
La empresa española de inteligencia artificial, NovaTech, anunció hoy una
ronda de financiación Serie B por valor de 30 millones de euros, liderada
por el fondo Sequoia Capital con participación de Telefónica Ventures.
La compañía, fundada en 2021 por María García y Carlos López, planea usar
los fondos para expandirse a Latinoamérica y contratar a 50 ingenieros
antes de fin de año. NovaTech ha desarrollado un modelo de lenguaje
especializado en el sector legal.
"""

# ---------------------------------------------------------------------------
# Función principal de extracción
# ---------------------------------------------------------------------------

def extract_json(text: str, schema_description: str, max_retries: int = 3):
    """
    Extrae datos estructurados de un texto libre.

    Args:
        text: Texto del cual extraer información.
        schema_description: Descripción del esquema JSON esperado.
        max_retries: Número máximo de reintentos si el JSON es inválido.

    Returns:
        dict con los datos extraídos, o None si se agotaron los reintentos.
    """
    user_prompt = (
        f"Extrae la información del siguiente texto y devuelve un JSON\n"
        f"con este esquema:\n\n{schema_description}\n\n"
        f'Texto:\n"""\n{text}\n"""\n'
    )

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
            )

            content = response.choices[0].message.content.strip()

            # Eliminar posibles bloques de código markdown (```json ... ```)
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:])
                content = content.rsplit("```", 1)[0].strip()

            result = json.loads(content)
            print(f"  [Extraccion exitosa en intento {attempt + 1}]")
            print(f"  [Tokens usados: {response.usage.total_tokens}]")
            return result

        except json.JSONDecodeError as e:
            print(f"  [Intento {attempt + 1}/{max_retries}] JSON invalido: {e}")
            if attempt < max_retries - 1:
                print("  Reintentando...")
            else:
                print("  Se agotaron los reintentos.")
                return None


# ---------------------------------------------------------------------------
# Definición de textos y esquemas
# ---------------------------------------------------------------------------

schemas = {
    "Oferta de empleo": {
        "text": texto_empleo,
        "schema": """{
    "puesto": "string - título del puesto",
    "empresa": "string - nombre de la empresa",
    "ubicacion": "string - ciudad/lugar",
    "salario_min": "number - salario mínimo en euros",
    "salario_max": "number - salario máximo en euros",
    "modalidad": "string - presencial/remoto/híbrido",
    "requisitos": ["lista de requisitos"],
    "beneficios": ["lista de beneficios"],
    "contacto": "string - email o forma de contacto",
    "fecha_limite": "string - formato YYYY-MM-DD"
}""",
    },
    "Resena de producto": {
        "text": texto_resena,
        "schema": """{
    "producto": "string - nombre del producto",
    "puntuacion": "number - nota dada",
    "puntuacion_maxima": "number - nota máxima posible",
    "precio": "number - precio en euros",
    "aspectos_positivos": ["lista de aspectos positivos"],
    "aspectos_negativos": ["lista de aspectos negativos"],
    "fecha_compra": "string - formato YYYY-MM-DD",
    "tienda": "string - donde se compro",
    "recomendacion_general": "string - positiva/neutra/negativa"
}""",
    },
    "Noticia": {
        "text": texto_noticia,
        "schema": """{
    "empresa": "string - nombre de la empresa",
    "tipo_evento": "string - tipo de evento",
    "monto": "number - cantidad en millones",
    "moneda": "string - EUR, USD, etc.",
    "inversores": ["lista de inversores"],
    "fundadores": ["lista de fundadores"],
    "año_fundacion": "number",
    "sector": "string - sector de la empresa",
    "planes": ["lista de planes futuros"]
}""",
    },
}

# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------

resultados = {}
for nombre, data in schemas.items():
    print(f"\n{'='*50}")
    print(f"Procesando: {nombre}")
    print(f"{'='*50}")
    resultado = extract_json(data["text"], data["schema"])
    if resultado:
        resultados[nombre] = resultado
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
