import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

prompt = "Explica qué es la recursividad en programación. Incluye un ejemplo en Python."

modelos = {
    "Google Gemini 2.0 Flash": "google/gemini-2.0-flash-exp:free",
    "DeepSeek R1": "deepseek/deepseek-r1-0528:free",
    "Meta Llama 4 Scout": "meta-llama/llama-4-scout:free",
}

resultados = {}

for nombre, modelo in modelos.items():
    print(f"\n{'='*40}")
    print(f"Modelo: {nombre} ({modelo})")
    print(f"{'='*40}")

    start = time.time()
    response = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    elapsed = time.time() - start

    contenido = response.choices[0].message.content
    print(contenido)
    print(f"\nTiempo: {elapsed:.2f}s")

    tokens_total = None
    if response.usage:
        tokens_total = response.usage.total_tokens
        print(f"Tokens: {tokens_total}")

    resultados[nombre] = {
        "tiempo": elapsed,
        "tokens": tokens_total,
        "longitud": len(contenido) if contenido else 0,
    }

print(f"\n{'='*60}")
print("TABLA RESUMEN")
print(f"{'='*60}")
print(f"{'Metrica':<35} {'Gemini':>10} {'DeepSeek':>10} {'Llama':>10}")
print("-" * 70)

nombres = list(modelos.keys())

for metrica in ["tiempo", "tokens", "longitud"]:
    fila = f"{metrica:<35}"
    for nombre in nombres:
        valor = resultados[nombre][metrica]
        if valor is None:
            fila += f"{'N/A':>10}"
        elif metrica == "tiempo":
            fila += f"{valor:>9.2f}s"
        else:
            fila += f"{valor:>10}"
    print(fila)
