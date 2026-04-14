"""
Asistente RAG para documentación de empresa.
Recupera información relevante y genera respuestas contextualizadas.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Cargar variables de entorno
load_dotenv()

def cargar_base_vectorial(ruta_db: str = "./chroma_db"):
    """Carga la base vectorial existente."""
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = Chroma(
        persist_directory=ruta_db,
        embedding_function=embeddings,
        collection_name="empresa_docs"
    )
    print(f"Base vectorial cargada: {vectorstore._collection.count()} vectores")
    return vectorstore

# Almacén de historiales por sesión (en memoria, dura lo que dura el proceso)
_store: dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]


def crear_cadena_rag(vectorstore):
    """Crea la cadena RAG con LCEL y memoria conversacional en sesión."""

    # Configurar retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    # Configurar modelo
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )

    # Prompt template con historial de conversación
    template = ChatPromptTemplate.from_messages([
        ("system", """Eres el asistente virtual de TechCorp, especializado en responder
preguntas sobre la documentación interna de la empresa.

INSTRUCCIONES:
- Responde SOLO con información que esté en el contexto proporcionado.
- Si la información no está en el contexto, responde: "No dispongo de información
  sobre ese tema en la documentación de la empresa. Te recomiendo contactar con
  el departamento correspondiente."
- NO inventes políticas, procedimientos ni datos.
- Sé claro, conciso y profesional.
- Cuando sea posible, indica de qué documento proviene la información.

CONTEXTO DE DOCUMENTOS INTERNOS:
{context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    # Función para formatear documentos recuperados
    def formatear_docs(docs):
        return "\n\n---\n\n".join(
            f"[Fuente: {doc.metadata.get('source', 'desconocida')}]\n{doc.page_content}"
            for doc in docs
        )

    # Construir cadena con LCEL (input como dict)
    cadena = (
        {
            "context": (lambda x: x["question"]) | retriever | formatear_docs,
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", [])
        }
        | template
        | llm
        | StrOutputParser()
    )

    # Envolver con gestión automática del historial
    cadena_con_memoria = RunnableWithMessageHistory(
        cadena,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history"
    )

    return cadena_con_memoria, retriever

def main():
    """Ejecuta el asistente en modo interactivo por CLI."""
    print("=" * 50)
    print("ASISTENTE RAG - TechCorp")
    print("=" * 50)
    print("Escribe tu pregunta sobre la documentación de la empresa.")
    print("Escribe 'salir' para terminar.\n")

    # Cargar base vectorial
    vectorstore = cargar_base_vectorial()

    # Crear cadena RAG
    cadena, retriever = crear_cadena_rag(vectorstore)

    while True:
        pregunta = input("\nTú: ").strip()

        if pregunta.lower() in ["salir", "exit", "quit", "q"]:
            print("\n¡Hasta luego!")
            break

        if not pregunta:
            print("Por favor, escribe una pregunta.")
            continue

        try:
            # Mostrar documentos recuperados (para depuración)
            docs_recuperados = retriever.invoke(pregunta)
            print(f"\n[Documentos recuperados: {len(docs_recuperados)}]")
            for i, doc in enumerate(docs_recuperados, 1):
                fuente = doc.metadata.get("source", "desconocida")
                print(f"  {i}. {fuente} - {doc.page_content[:80]}...")

            # Generar respuesta (con memoria de sesión)
            respuesta = cadena.invoke(
                {"question": pregunta},
                config={"configurable": {"session_id": "cli"}}
            )
            print(f"\nAsistente: {respuesta}")

        except Exception as e:
            print(f"\nError al procesar la pregunta: {e}")

if __name__ == "__main__":
    main()