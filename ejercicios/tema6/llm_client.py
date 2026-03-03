import os
from typing import Generator
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Cliente unificado para múltiples proveedores de LLMs."""

    DEFAULT_MODELS = {
        "openai": "gpt-4o-mini",
        "gemini": "gemini-1.5-flash",
        "claude": "claude-3-5-haiku-latest",
        "openrouter": "google/gemini-2.0-flash-exp:free",
    }

    def __init__(self, provider: str, model: str = None):
        """
        Inicializa el cliente del proveedor indicado.

        Args:
            provider: "openai" | "gemini" | "claude" | "openrouter"
            model:    Modelo específico. Si es None, usa el modelo por defecto.
        """
        if provider not in self.DEFAULT_MODELS:
            raise ValueError(
                f"Proveedor no soportado: '{provider}'. "
                f"Usa uno de: {list(self.DEFAULT_MODELS.keys())}"
            )

        self.provider = provider
        self.model = model or self.DEFAULT_MODELS[provider]

        if provider == "openai":
            from openai import OpenAI
            self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        elif provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self._genai = genai
            self._gemini_model = genai.GenerativeModel(self.model)

        elif provider == "claude":
            import anthropic
            self._client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        elif provider == "openrouter":
            from openai import OpenAI
            self._client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )

    def _extract_system(self, messages: list) -> tuple[str | None, list]:
        """Separa el mensaje de sistema del resto de los mensajes."""
        system_content = None
        conversation = []
        for msg in messages:
            if msg["role"] == "system":
                system_content = (system_content or "") + msg["content"] + "\n"
            else:
                conversation.append(msg)
        return system_content.strip() if system_content else None, conversation

    def _adapt_for_gemini(self, messages: list) -> tuple[str | None, list]:
        """
        Convierte mensajes al formato de Gemini.
        Gemini no tiene rol 'system' nativo: se concatena al primer mensaje de usuario.
        Además usa 'model' en lugar de 'assistant' como nombre de rol.
        """
        system_content, conversation = self._extract_system(messages)

        gemini_messages = []
        for i, msg in enumerate(conversation):
            role = "model" if msg["role"] == "assistant" else "user"
            content = msg["content"]
            if i == 0 and system_content and role == "user":
                content = f"[Instrucciones del sistema: {system_content}]\n\n{content}"
            gemini_messages.append({"role": role, "parts": [content]})

        return system_content, gemini_messages

    def chat(self, messages: list, **kwargs) -> str:
        """
        Envía mensajes al LLM y retorna la respuesta como string.

        Args:
            messages: Lista de mensajes con formato unificado
                      [{"role": "system"|"user"|"assistant", "content": "..."}]
            **kwargs: Parámetros adicionales (temperature, max_tokens, etc.)

        Returns:
            str con el texto de la respuesta.
        """
        temperature = kwargs.get("temperature", 0.7)

        if self.provider in ("openai", "openrouter"):
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                **{k: v for k, v in kwargs.items() if k != "temperature"},
            )
            return response.choices[0].message.content

        elif self.provider == "gemini":
            _, gemini_messages = self._adapt_for_gemini(messages)
            # El último mensaje es el turno actual del usuario
            history = gemini_messages[:-1]
            last_message = gemini_messages[-1]["parts"][0]
            chat_session = self._gemini_model.start_chat(history=history)
            response = chat_session.send_message(
                last_message,
                generation_config=self._genai.types.GenerationConfig(
                    temperature=temperature
                ),
            )
            return response.text

        elif self.provider == "claude":
            system_content, conversation = self._extract_system(messages)
            max_tokens = kwargs.get("max_tokens", 1024)
            create_kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": conversation,
            }
            if system_content:
                create_kwargs["system"] = system_content
            response = self._client.messages.create(**create_kwargs)
            return response.content[0].text

    def stream(self, messages: list, **kwargs) -> Generator[str, None, None]:
        """
        Envía mensajes al LLM y genera tokens/fragmentos uno a uno.

        Args:
            messages: Lista de mensajes con formato unificado.
            **kwargs: Parámetros adicionales (temperature, etc.)

        Yields:
            str: Cada fragmento de texto de la respuesta.
        """
        temperature = kwargs.get("temperature", 0.7)

        if self.provider in ("openai", "openrouter"):
            with self._client.chat.completions.stream(
                model=self.model,
                messages=messages,
                temperature=temperature,
            ) as stream:
                for text in stream.text_stream:
                    yield text

        elif self.provider == "gemini":
            _, gemini_messages = self._adapt_for_gemini(messages)
            history = gemini_messages[:-1]
            last_message = gemini_messages[-1]["parts"][0]
            chat_session = self._gemini_model.start_chat(history=history)
            response = chat_session.send_message(
                last_message,
                stream=True,
                generation_config=self._genai.types.GenerationConfig(
                    temperature=temperature
                ),
            )
            for chunk in response:
                yield chunk.text

        elif self.provider == "claude":
            system_content, conversation = self._extract_system(messages)
            max_tokens = kwargs.get("max_tokens", 1024)
            create_kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": conversation,
            }
            if system_content:
                create_kwargs["system"] = system_content
            with self._client.messages.stream(**create_kwargs) as stream:
                for text in stream.text_stream:
                    yield text
