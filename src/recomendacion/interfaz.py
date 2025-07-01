"""Dado un usuario se recomiendan destinos para visitar"""
import numpy as np
import gradio as gr
import pandas as pd
import os
import pickle
from tensorflow.keras.models import load_model
import calendar

CSV_PATH = os.path.join(os.path.dirname(__file__), "df_ready_for_training.csv")
df = pd.read_csv(CSV_PATH)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "modelos", "modelo_recomendador_destinos.h5")
modelo = load_model(MODEL_PATH, compile=False)
MAPPER_PATH = os.path.join(os.path.dirname(__file__), "destination_name_mapper.pkl")
with open(MAPPER_PATH, "rb") as f:
    destination_name_mapper = pickle.load(f)

num_cols = [
    'NumberOfAdults', 'NumberOfChildren', 'Popularity',
    'Adventure', 'Beaches', 'City', 'Historical', 'Nature',
    'Month_sin', 'Month_cos',
    'Gender_Female', 'Gender_Male',
    'Type_Adventure', 'Type_Beach', 'Type_City', 'Type_Historical', 'Type_Nature'
]

# Lista de meses en español (enero a diciembre)
MESES_ES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

def get_month_name_es(month_sin, month_cos):
    """
    Recupera el nombre del mes en español a partir de Month_sin y Month_cos.
    """
    angle = np.arctan2(month_sin, month_cos)
    month_number = int(np.round((angle / (2 * np.pi) * 12))) % 12 + 1
    return MESES_ES[month_number]

def preparar_inputs(X):
    """
    Prepara los inputs del modelo en formato de diccionario para alimentar a la red neuronal.

    Parámetro:
    - X: DataFrame con las columnas necesarias

    Retorna:
    - Diccionario con entradas nombradas según las capas del modelo.
    """
    return {
        "user_input": np.array(X["UserID"]),
        "dest_input": np.array(X["DestinationID"]),
        "numeric_input": np.array(X[
            [
                "NumberOfAdults", "NumberOfChildren", "Popularity",
                "Adventure", "Beaches", "City", "Historical", "Nature",
                "Type_Adventure", "Type_Beach", "Type_City", "Type_Historical", "Type_Nature",
                "Gender_Female", "Gender_Male",
                "Month_sin", "Month_cos"
            ]
        ])
    }

def obtener_perfil_usuario(user_id, df):
    user_data = df[df["UserID"] == user_id]
    if user_data.empty:
        return df[num_cols].mean(), False, None
    return user_data[num_cols].mean(), True, user_data

def recomendar_destinos_para_usuario(user_id, df, modelo, top_n=5):
    destinos_unicos = df["DestinationID"].unique()
    perfil, user_found, user_data = obtener_perfil_usuario(user_id, df)

    # Si el usuario no existe, usa un UserID válido (por ejemplo, el primero del dataset)
    if not user_found:
        valid_user_id = df["UserID"].iloc[0]
        user_id_for_model = valid_user_id
    else:
        user_id_for_model = user_id

    user_df = pd.DataFrame({
        "UserID": [user_id_for_model] * len(destinos_unicos),
        "DestinationID": destinos_unicos
    })

    for col in num_cols:
        user_df[col] = perfil[col]

    inputs = preparar_inputs(user_df)
    predicciones = predict_with_clipping(modelo, inputs).flatten()
    user_df["PredictedRating"] = predicciones

    recomendaciones = user_df.sort_values(by="PredictedRating", ascending=False).head(top_n)
    recomendaciones["DestinationName"] = recomendaciones["DestinationID"].map(destination_name_mapper)
    recomendaciones = recomendaciones.reset_index(drop=True)
    return recomendaciones, user_found, user_data

def predict_with_clipping(model, inputs, min_rating=1, max_rating=5):
    """
    Realiza una predicción con el modelo y asegura que los valores estén dentro del rango deseado.

    Parámetros:
    - model: modelo entrenado de Keras.
    - inputs: diccionario con los datos de entrada.
    - min_rating: valor mínimo permitido en la predicción (default=1).
    - max_rating: valor máximo permitido (default=5).

    Retorna:
    - Las predicciones ajustadas (clipped) al rango definido.
    """
    pred = model.predict(inputs, verbose=0)
    return np.clip(pred, min_rating, max_rating)

def recomendar_destinos_wrapper(user_id):
    if not str(user_id).strip().isdigit():
        return "Please enter a valid numeric User ID."
    recomendaciones, user_found, user_data = recomendar_destinos_para_usuario(int(user_id), df, modelo)
    intro = ""
    if user_found and user_data is not None:
        row = user_data.iloc[0]
        gender = "femenino" if row.get("Gender_Female", 0) > row.get("Gender_Male", 0) else "masculino"
        n_children = int(round(row.get("NumberOfChildren", 0)))
        n_adults = int(round(row.get("NumberOfAdults", 0)))
        month_sin = row.get("Month_sin", 0)
        month_cos = row.get("Month_cos", 1)
        month = get_month_name_es(month_sin, month_cos)
        # Tipo de viaje preferido
        type_cols = ["Type_Adventure", "Type_Beach", "Type_City", "Type_Historical", "Type_Nature"]
        type_names = {
            "Type_Adventure": "aventureros",
            "Type_Beach": "playeros",
            "Type_City": "urbanos",
            "Type_Historical": "históricos",
            "Type_Nature": "naturales"
        }
        preferred_type_col = max(type_cols, key=lambda col: row.get(col, 0))
        preferred_type = type_names[preferred_type_col]
        intro = (
            f"Teniendo en cuenta que el usuario es de género {gender}, "
            f"viaja con {n_children} niñ{'o' if n_children==1 else 'os'} y {n_adults} adult{'o' if n_adults==1 else 'os'}, "
            f"le gustan los destinos {preferred_type}, "
            f"y usualmente viaja en el mes de  {month}, "
            f"le recomendamos los siguientes destinos:\n\n"
        )
    elif not user_found:
        intro = "Usuario no registrado en el sistema. Mostrando recomendaciones promedio\n\n"

    lines = [
        f"Recomendación {i+1}: {row['DestinationName']} con calificación {row['PredictedRating']:.1f}"
        for i, row in recomendaciones.iterrows()
    ]
    result = intro + "\n".join(lines)
    return result

with gr.Blocks() as recomendacion_tab:
    gr.Markdown("## Recomendación de Destinos de Viaje")
    with gr.Row():
        usuario_input = gr.Textbox(label="ID del Usuario")
        resultado_recomendacion = gr.Textbox(label="Destinos Recomendados", value="")
    boton_recomendar = gr.Button("Recomendar")
    boton_recomendar.click(
        recomendar_destinos_wrapper, inputs=usuario_input, outputs=resultado_recomendacion
    )
