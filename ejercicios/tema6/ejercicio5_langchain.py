import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI(
    model="google/gemini-2.0-flash-exp:free",
    temperature=0,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un sistema de extracción de información. Tu tarea es extraer datos
estructurados de textos no estructurados y devolver ÚNICAMENTE un JSON válido.

Reglas:
- Responde SOLO con el JSON, sin texto adicional, sin bloques de código markdown.
- Si un campo no se encuentra en el texto, usa el valor "No especificado".
- Los valores numéricos deben ser números, no strings.
- Las fechas deben estar en formato YYYY-MM-DD cuando sea posible."""),
    ("user", """Extrae la información del siguiente texto y devuelve un JSON
con este esquema: {schema}

Texto:
\"\"\"
{text}
\"\"\""""),
])

output_parser = StrOutputParser()

chain = prompt | model | output_parser

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

textos = {
    "Oferta de empleo": {
        "text": texto_empleo,
        "schema": (
            "puesto, empresa, ubicacion, salario_min, salario_max, modalidad, "
            "requisitos (lista), beneficios (lista), contacto, fecha_limite"
        ),
    },
    "Resena de producto": {
        "text": texto_resena,
        "schema": (
            "producto, puntuacion, puntuacion_maxima, precio, "
            "aspectos_positivos (lista), aspectos_negativos (lista), "
            "fecha_compra, tienda, recomendacion_general"
        ),
    },
    "Noticia": {
        "text": texto_noticia,
        "schema": (
            "empresa, tipo_evento, monto, moneda, inversores (lista), "
            "fundadores (lista), año_fundacion, sector, planes (lista)"
        ),
    },
}


for nombre, inputs in textos.items():
    print(f"\n{'='*50}")
    print(f"Procesando: {nombre}")
    print(f"{'='*50}")
    result = chain.invoke(inputs)


    content = result.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:])
        content = content.rsplit("```", 1)[0].strip()

    try:
        parsed = json.loads(content)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(f"Error al parsear JSON. Respuesta raw:\n{result}")
