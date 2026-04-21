"""
Ejercicio 4: Cliente MCP con Streamlit.
Interfaz web que se conecta a un servidor MCP local y permite
interactuar en lenguaje natural. El LLM decide cuándo invocar tools.

Uso:
    streamlit run ejercicio4_app.py

Requiere:
    pip install streamlit mcp anthropic python-dotenv
    ANTHROPIC_API_KEY en .env o en variables de entorno
"""

import streamlit as st
import asyncio
import os
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

st.set_page_config(
    page_title="Cliente MCP",
    page_icon="🔧",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Cliente MCP
# ---------------------------------------------------------------------------

class MCPClient:
    """Gestiona la conexión con un servidor MCP local y el ciclo tool-calling."""

    def __init__(self):
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.available_tools: list[dict] = []

    async def connect(self, server_script_path: str) -> list[dict]:
        """Conecta con un servidor MCP local vía stdio y descubre sus herramientas."""
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
        )
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        read_stream, write_stream = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()

        response = await self.session.list_tools()
        self.available_tools = [
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]
        return self.available_tools

    async def process_message(self, user_message: str, message_history: list) -> str:
        """Procesa un mensaje del usuario con el ciclo agentic tool-calling."""
        message_history.append({"role": "user", "content": user_message})

        response = self.anthropic.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=(
                "Eres un asistente útil con acceso a herramientas MCP. "
                "Usa las herramientas disponibles cuando sea apropiado "
                "para responder a las preguntas del usuario. "
                "Responde siempre en español."
            ),
            tools=self.available_tools,
            messages=message_history,
        )

        result_text = ""
        while response.stop_reason == "tool_use":
            assistant_content = response.content
            message_history.append({"role": "assistant", "content": assistant_content})

            tool_results = []
            for block in assistant_content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_args = block.input

                    # Log en sidebar
                    st.sidebar.markdown(f"**🔧 Tool call:** `{tool_name}`")
                    st.sidebar.json(tool_args)

                    tool_response = await self.session.call_tool(tool_name, tool_args)

                    result_str = str(tool_response.content)
                    st.sidebar.markdown(f"**📤 Resultado:** `{result_str[:200]}{'...' if len(result_str) > 200 else ''}`")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_str,
                    })

            message_history.append({"role": "user", "content": tool_results})
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=(
                    "Eres un asistente útil con acceso a herramientas MCP. "
                    "Usa las herramientas disponibles cuando sea apropiado. "
                    "Responde siempre en español."
                ),
                tools=self.available_tools,
                messages=message_history,
            )

        for block in response.content:
            if hasattr(block, "text"):
                result_text += block.text

        message_history.append({"role": "assistant", "content": result_text})
        return result_text

    async def disconnect(self):
        await self.exit_stack.aclose()


# ---------------------------------------------------------------------------
# Helpers asyncio <-> Streamlit
# ---------------------------------------------------------------------------

def run_async(coro):
    """Ejecuta una coroutine en el event loop gestionado por Streamlit."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
    except RuntimeError:
        pass
    return asyncio.run(coro)


# ---------------------------------------------------------------------------
# Interfaz Streamlit
# ---------------------------------------------------------------------------

st.title("🔧 Cliente MCP con Streamlit")
st.markdown("Conecta con un servidor MCP local y chatea usando lenguaje natural.")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuración")
    server_path = st.text_input(
        "Ruta al servidor MCP",
        value="ejercicio1_server.py",
        help="Ruta relativa o absoluta al archivo Python del servidor MCP",
    )
    connect_button = st.button("🔌 Conectar al servidor", use_container_width=True)
    if st.button("🗑️ Limpiar chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Estado de sesión ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "connected" not in st.session_state:
    st.session_state.connected = False
if "tools" not in st.session_state:
    st.session_state.tools = []
if "mcp_client" not in st.session_state:
    st.session_state.mcp_client = None
if "history" not in st.session_state:
    st.session_state.history = []

# --- Conectar ---
if connect_button:
    if not os.path.exists(server_path):
        st.sidebar.error(f"No se encuentra el archivo: {server_path}")
    else:
        with st.sidebar:
            with st.spinner("Conectando..."):
                try:
                    client = MCPClient()
                    tools = run_async(client.connect(server_path))
                    st.session_state.mcp_client = client
                    st.session_state.tools = tools
                    st.session_state.connected = True
                    st.session_state.history = []
                    st.success("✅ Conectado")
                except Exception as e:
                    st.error(f"Error al conectar: {e}")

# --- Mostrar herramientas ---
if st.session_state.connected:
    with st.sidebar:
        st.subheader("🛠️ Herramientas disponibles")
        for tool in st.session_state.tools:
            with st.expander(f"🔧 {tool['name']}"):
                st.write(tool["description"])
        st.divider()
        st.subheader("📋 Log de tool calls")

# --- Historial de chat ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Input usuario ---
if prompt := st.chat_input("Escribe tu mensaje..."):
    if not st.session_state.connected:
        st.warning("⚠️ Primero conecta con un servidor MCP usando el panel lateral.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Procesando..."):
                try:
                    response = run_async(
                        st.session_state.mcp_client.process_message(
                            prompt,
                            st.session_state.history,
                        )
                    )
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error al procesar el mensaje: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
