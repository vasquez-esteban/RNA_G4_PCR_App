---
title: Rna G4 Trabajo3
emoji: 🐨
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.34.0
app_file: app.py
pinned: false
license: mit
short_description: Este proyecto implementa un sistema inteligente basado en RN
---

# Sistema Inteligente para Transporte

Este proyecto implementa una aplicación web construida con [Gradio](https://www.gradio.app/) que sirve como interfaz para un sistema inteligente desarrollado con aprendizaje profundo, diseñado para una empresa de transporte. El sistema resuelve tres retos clave:

1. **Predicción de demanda de rutas** (series de tiempo)
2. **Clasificación de conducción distractiva** (imágenes)
3. **Recomendación de destinos personalizados** (sistemas de recomendación)

El despliegue de la aplicación se realiza automáticamente mediante **GitHub Actions** cada vez que se hace un push al repositorio.

---

## Estructura del Proyecto

```
.
├── app.py               # Aplicación principal con interfaz Gradio
├── requirements.txt     # Dependencias necesarias para correr la app
├── src/                 # Código fuente para cada uno de los módulos
│   ├── demanda/         # Predicción de demanda de transporte
│   ├── clasificacion/   # Clasificación de imágenes de conducción
│   └── recomendacion/   # Sistema de recomendación de destinos
├── .github/
│   └── workflows/
│       └── deploy.yml   # Workflow para CI/CD con GitHub Actions
└── README.md            # Este archivo
```

---

## Guía Rápida de Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/vasquez-esteban/RNA_G4_PCR_App
cd RNA_G4_PCR_App
```

### 2. Configurar entorno Python (Linux/macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
source setup.sh
```

#### En Windows:

```bash
python3 -m venv .venv
.venv\Scripts\activate
setup.bat
```

---

## Ejecutar la aplicación web

```bash
python3 app.py
```

---

## ⚙️ Despliegue Automático con GitHub Actions

Este repositorio incluye un flujo de trabajo de GitHub Actions en `.github/workflows/deploy.yml` que automatiza:

- Despliegue automático al entorno de producción [Hugging Face Spaces](https://huggingface.co/spaces)

### 🔐 Variables de entorno necesarias

Agrega las siguientes _GitHub Secrets_ si usas Hugging Face Spaces:

- `HF_TOKEN`: Token de autenticación personal de Hugging Face
- `SPACE_ID`: Nombre del espacio (por ejemplo, `usuario/nombre_del_space`)

---

## 🧪 Requisitos

- Python 3.9+

Consulta `requirements.txt` para más detalles.

## 📄 Licencia

Distribuido bajo la [Licencia MIT](LICENSE).

## Referencias

Este proyecto forma parte del repositorio principal del equipo, que contiene todos los módulos de predicción, clasificación y recomendación, así como los modelos y reportes técnicos:

[Repositorio Principal](vasquez-esteban/RNA_G4_Prediccion_Clasificacion_Recomendacion)
