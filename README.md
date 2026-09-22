# Procesamiento de Datos y Análisis Hidrostático

[![DOI Código](https://img.shields.io/badge/Zenodo%20Code-10.5281%2Fzenodo.XXXXXX-blue)](https://doi.org/10.5281/zenodo.22891811)
[![DOI Dataset Barométrico](https://img.shields.io/badge/Zenodo%20Dataset-10.5281%2Fzenodo.22837162-green)](https://doi.org/10.5281/zenodo.22837162)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

Este repositorio contiene el código de procesamiento de datos, análisis de incertidumbres y generación de figuras para la verificación experimental de la presión hidrostática en función de la profundidad.

---

## 📌 Descripción del Proyecto

El proyecto procesa y modela la respuesta manométrica bajo compresión de gas atrapado en un sistema hidrostático:
1. **Análisis Barométrico y Densidad:** Procesamiento de lecturas meteorológicas para obtener la media y el error estándar de la presión atmosférica, así como la densidad del agua estimada mediante la **ecuación de Tanaka**.
2. **Procesamiento Experimental:** Ajustes lineales ortogonales (ODR) con propagación de incertidumbres y generación de gráficos comparativos entre la presión experimental y el modelo teórico.

---

## 📊 Datos Utilizados

* **Datos Barométricos (Publicados):** Las mediciones de la estación meteorológica del Instituto de Astronomía y Meteorología (IAM - CUCEI) del 1 al 8 de septiembre de 2026 están archivadas de forma independiente en Zenodo:
  * **DOI:** [10.5281/zenodo.22837162](https://doi.org/10.5281/zenodo.22837162)
* **Datos Experimentales:** Mediciones directas del manómetro ($H$) y profundidades de inmersión ($h$), ubicados en `data/datos_experimentales.csv`.

---

## 📁 Estructura del Repositorio

```text
.
├── data/
│   ├── datos_barometricos_IAM.csv    # Obtenidos desde Zenodo (DOI: 10.5281/zenodo.22837162)
│   └── datos_experimentales.csv      # Mediciones de h, H y sus incertidumbres
├── scripts/
│   ├── analisis-datos-barometricos.py       # Procesa datos barométricos y densidad de Tanaka
│   └── procesamiento-datos-experimentales.py# Ajustes ODR, propagación y gráficas
├── figures/                           # Gráficas generadas automáticamente
├── requirements.txt                   # Dependencias de Python
└── README.md                          # Documentación principal
```
# 1. Clonar el repositorio
```
git clone https://github.com/TheMegaBeast99/Procesamiento-de-Datos-Presion-Hidrostatica.git
cd Procesamiento-de-Datos-Presion-Hidrostatica
```
# 2. Instalar dependencias
```
pip install -r requirements.txt
```
