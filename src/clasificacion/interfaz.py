"""Clasificador de tipo de conductor"""

import gradio as gr  # type: ignore


def clasificar_conduccion(imagen):
    """Recibe una imagen y retorna el comportamiento de conductor"""
    if imagen is None:
        return "Por favor, carga una imagen"

    return "Comportamiento detectado: Safe Driving"


with gr.Blocks() as clasificacion_tab:
    gr.Markdown("## Clasificación de Conducción Distractiva")
    imagen_input = gr.Image(type="filepath", label="Imagen del conductor")
    resultado_clasificacion = gr.Textbox(label="Clasificación")
    boton_clasificar = gr.Button("Clasificar")

    # Conexión del evento click
    boton_clasificar.click(
        fn=clasificar_conduccion, inputs=imagen_input, outputs=resultado_clasificacion
    )
