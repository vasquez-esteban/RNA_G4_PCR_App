"""Dado un usuario se recomiendan destinos para visitar"""

import gradio as gr


def recomendar_destinos(usuario_id):
    """Recibe el id del usuario y retorna los destinos"""
    return f"Destinos recomendados para el usuario {usuario_id}: [placeholder]"


with gr.Blocks() as recomendacion_tab:
    gr.Markdown("## Recomendación de Destinos de Viaje")
    with gr.Row():
        usuario_input = gr.Textbox(label="ID del Usuario")
        resultado_recomendacion = gr.Textbox(label="Destinos Recomendados")
    boton_recomendar = gr.Button("Recomendar")
    boton_recomendar.click(
        recomendar_destinos, inputs=usuario_input, outputs=resultado_recomendacion
    )
