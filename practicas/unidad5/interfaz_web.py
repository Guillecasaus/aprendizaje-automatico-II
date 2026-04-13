# interfaz_web.py (bonificación)
import gradio as gr
from asistente import cargar_base_vectorial, crear_cadena_rag

vectorstore = cargar_base_vectorial()
cadena, _ = crear_cadena_rag(vectorstore)

def responder(pregunta, historial):
    respuesta = cadena.invoke(pregunta)
    historial.append({"role": "user", "content": pregunta})
    historial.append({"role": "assistant", "content": respuesta})
    return "", historial

with gr.Blocks(title="Asistente TechCorp") as demo:
    gr.Markdown("# Asistente RAG - TechCorp")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Escribe tu pregunta...")
    msg.submit(responder, [msg, chatbot], [msg, chatbot])

demo.launch()