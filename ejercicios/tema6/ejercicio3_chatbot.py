"""
Ejercicio 3: Chatbot con Memoria
Unidad 3, Sesión 2 - Acceso Programático a LLMs

Implementa un tutor de Python con historial de conversación y recorte
automático cuando se supera MAX_MESSAGES.
Requiere OPENROUTER_API_KEY en el archivo .env
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
MODEL = "google/gemini-2.0-flash-exp:free"

SYSTEM_PROMPT = """Eres PyTutor, un tutor de Python amigable y paciente.

Tu personalidad:
- Explicas conceptos de forma clara y con ejemplos prácticos
- Usas analogías cuando un concepto es complejo
- Siempre incluyes un pequeño ejemplo de código cuando es relevante
- Animas al estudiante y celebras su progreso
- Si el estudiante comete un error conceptual, lo corriges con amabilidad

Reglas:
- Responde siempre en español
- Mantén las respuestas concisas (máximo 200 palabras)
- Siempre ofrece una pregunta de seguimiento o sugerencia de qué explorar después
"""

MAX_MESSAGES = 10


def create_initial_messages():
    """Crea la lista inicial de mensajes con el system prompt."""
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def trim_history(messages):
    """
    Recorta el historial si excede MAX_MESSAGES.
    Mantiene siempre el system prompt (primer mensaje)
    y los últimos MAX_MESSAGES mensajes de conversación.
    """
    if len(messages) - 1 > MAX_MESSAGES:
        messages = [messages[0]] + messages[-MAX_MESSAGES:]
    return messages


def get_response(messages):
    """Envía los mensajes a la API y retorna el objeto response completo."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )
    return response


def summarize_and_trim(messages):
    """
    Bonus: en lugar de simplemente recortar, resume los mensajes antiguos
    y los añade como contexto adicional antes de los mensajes recientes.
    """
    if len(messages) - 1 > MAX_MESSAGES:
        old_messages = messages[1:-MAX_MESSAGES]

        conversation_text = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in old_messages
        )

        summary_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Resume la siguiente conversación en 2-3 oraciones, "
                        "capturando los temas principales discutidos."
                    ),
                },
                {"role": "user", "content": conversation_text},
            ],
            temperature=0,
        )

        summary = summary_response.choices[0].message.content

        messages = (
            [messages[0]]
            + [
                {
                    "role": "system",
                    "content": f"Resumen de la conversación anterior: {summary}",
                }
            ]
            + messages[-MAX_MESSAGES:]
        )

    return messages


def chat():
    """Bucle principal del chatbot."""
    messages = create_initial_messages()
    print("=" * 50)
    print("  Tutor de Python - Escribe 'salir' para terminar")
    print("=" * 50)
    print()

    while True:
        user_input = input("Tu: ").strip()

        if user_input.lower() == "salir":
            print("\nHasta pronto! Sigue practicando Python.")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        messages = trim_history(messages)

        response = get_response(messages)

        assistant_message = response.choices[0].message.content

        messages.append({"role": "assistant", "content": assistant_message})

        print(f"\nTutor: {assistant_message}")
        print(
            f"  [Tokens - Prompt: {response.usage.prompt_tokens}, "
            f"Respuesta: {response.usage.completion_tokens}, "
            f"Total: {response.usage.total_tokens}]"
        )
        print(f"  [Mensajes en historial: {len(messages) - 1}]")
        print()


if __name__ == "__main__":
    chat()
