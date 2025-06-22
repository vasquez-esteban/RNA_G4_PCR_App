"""Clasificador de tipo de conductor"""

import gradio as gr  # type: ignore
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Cargar el modelo una sola vez al inicio
MODEL_PATH = "modelos/driver_classif.h5"
model = load_model(MODEL_PATH)

# Nombres de las clases según el modelo entrenado
CLASS_NAMES = [
    "Otras actividades",  # other_activities
    "Conducción segura",  # safe_driving
    "Hablando por teléfono",  # talking_phone
    "Escribiendo en el teléfono",  # texting_phone
    "Girando",  # turning

]
IMG_SIZE = (224, 224)  # Tamaño correcto según el modelo


def clasificar_conduccion(imagen):
    """Recibe una imagen y retorna el comportamiento de conductor"""
    if imagen is None:
        return "Por favor, carga una imagen"

    # Preprocesar la imagen
    img = image.load_img(imagen, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalización común

    # Realizar la predicción
    preds = model.predict(img_array)
    class_idx = np.argmax(preds, axis=1)[0]
    class_name = CLASS_NAMES[class_idx]
    return f"Comportamiento detectado: {class_name}"


with gr.Blocks() as clasificacion_tab:
    gr.Markdown("## Clasificación de Conducción Distractiva")
    imagen_input = gr.Image(type="filepath", label="Imagen del conductor")
    resultado_clasificacion = gr.Textbox(label="Clasificación")
    boton_clasificar = gr.Button("Clasificar")

    # Conexión del evento click
    boton_clasificar.click(
        fn=clasificar_conduccion, inputs=imagen_input, outputs=resultado_clasificacion
    )
