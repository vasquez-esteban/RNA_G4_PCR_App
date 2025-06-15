"""Modelo de series de tiempo"""

import gradio as gr


def predecir_demanda(ruta):
    """Dada una ruta retorna la demanda"""
    return f"Demanda estimada para {ruta}: [placeholder] pasajeros"


with gr.Blocks() as demanda_tab:
    gr.Markdown("## Predicción de Demanda de Transporte")
    with gr.Row():
        ruta_input = gr.Textbox(label="Ruta")
        resultado_demanda = gr.Textbox(label="Predicción de Demanda")
    boton_predecir = gr.Button("Predecir")
    boton_predecir.click(predecir_demanda, inputs=ruta_input, outputs=resultado_demanda)
