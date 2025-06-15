"""Módulo principal"""

import gradio as gr  # type: ignore

from src.clasificacion.interfaz import clasificacion_tab
from src.demanda.interfaz import demanda_tab
from src.recomendacion.interfaz import recomendacion_tab

demo = gr.TabbedInterface(
    interface_list=[clasificacion_tab, demanda_tab, recomendacion_tab],
    tab_names=["Clasificación", "Demanda", "Recomendación"],
)

if __name__ == "__main__":
    demo.launch()
