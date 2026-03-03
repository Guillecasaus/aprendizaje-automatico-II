from llm_client import LLMClient

messages = [
    {
        "role": "system",
        "content": "Eres un asistente conciso. Responde en máximo 2 oraciones.",
    },
    {"role": "user", "content": "¿Qué es Python?"},
]

for provider in ["openai", "gemini", "claude"]:
    print(f"\n{'='*40}")
    print(f"Proveedor: {provider}")
    print(f"{'='*40}")

    try:
        client = LLMClient(provider)
        response = client.chat(messages, temperature=0.7)
        print(f"Respuesta: {response}")
    except Exception as e:
        print(f"Error: {e}")

modelos_openrouter = {
    "Google Gemini 2.0 Flash": "google/gemini-2.0-flash-exp:free",
    "Meta Llama 4 Scout": "meta-llama/llama-4-scout:free",
}

for nombre, modelo in modelos_openrouter.items():
    print(f"\n{'='*40}")
    print(f"OpenRouter - {nombre}")
    print(f"{'='*40}")
    try:
        client = LLMClient("openrouter", model=modelo)
        response = client.chat(messages, temperature=0.7)
        print(f"Respuesta: {response}")
    except Exception as e:
        print(f"Error: {e}")

print(f"\n{'='*40}")
print("Streaming con OpenAI")
print(f"{'='*40}")

try:
    client = LLMClient("openai")
    print("Respuesta en streaming: ", end="", flush=True)
    for token in client.stream(messages):
        print(token, end="", flush=True)
    print()
except Exception as e:
    print(f"Error: {e}")
