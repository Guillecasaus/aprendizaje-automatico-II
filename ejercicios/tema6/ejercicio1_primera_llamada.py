import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
MODEL = "google/gemini-2.0-flash-exp:free"

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "¿Qué es el machine learning? Responde en 3 oraciones."}
    ],
    temperature=0.7
)

print("Respuesta:", response.choices[0].message.content)
print("Modelo:", response.model)
print("Prompt tokens:", response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)

print("\n" + "=" * 60)
print("Experimentando con temperature")
print("=" * 60)

temperaturas = [0, 0.7, 1.5]

for temp in temperaturas:
    print(f"\n--- temperature = {temp} ---")
    for ejecucion in range(1, 3):
        r = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "¿Qué es el machine learning? Responde en 3 oraciones."}
            ],
            temperature=temp
        )
        print(f"  Ejecucion {ejecucion}: {r.choices[0].message.content}")
        if r.usage:
            print(f"  Tokens usados: {r.usage.total_tokens}")
