"""Modelo de series de tiempo"""

import gradio as gr
import os

# Opciones de rutas
RUTAS = [
    "Goa Beaches",
    "Jaipur City",
    "Kerala Backwaters",
    "Leh Ladakh",
    "Taj Mahal",
]

# Mapeo de rutas a imágenes
IMAGES_DIR = "src/demanda/images"
ROUTE_IMAGE_MAP = {
    "Goa Beaches": os.path.join(IMAGES_DIR, "per_route_pred_vs_real_Goa_Beaches.png"),
    "Jaipur City": os.path.join(IMAGES_DIR, "per_route_pred_vs_real_Jaipur_City.png"),
    "Kerala Backwaters": os.path.join(IMAGES_DIR, "per_route_pred_vs_real_Kerala_Backwaters.png"),
    "Leh Ladakh": os.path.join(IMAGES_DIR, "per_route_pred_vs_real_Leh_Ladakh.png"),
    "Taj Mahal": os.path.join(IMAGES_DIR, "per_route_pred_vs_real_Taj_Mahal.png"),
    # Agrega más rutas e imágenes aquí si es necesario
}


def predecir_demanda(ruta):
    """Dada una ruta retorna la imagen correspondiente"""
    imagen = ROUTE_IMAGE_MAP.get(ruta, None)
    return imagen


with gr.Blocks() as demanda_tab:
    gr.Markdown("## Predicción de Demanda de Transporte")
    with gr.Row():
        ruta_input = gr.Dropdown(choices=RUTAS, label="Ruta")
    imagen_prediccion = gr.Image(
        label=None,
        visible=True,
        height=400,
        container=True
    )
    # Elimina el botón y conecta el evento de cambio del dropdown
    ruta_input.change(
        predecir_demanda,
        inputs=ruta_input,
        outputs=imagen_prediccion,
    )
