# Avance de la Vacunación contra la Covid-19 en Perú

[![scraper-daily](https://github.com/annaabsi/git-scraper-vacunacion/actions/workflows/main.yml/badge.svg)](https://github.com/annaabsi/git-scraper-vacunacion/actions/workflows/main.yml)


## Instalación


### Linux (Probado en python 3.8.1+)
```
# Instala requerimientos de python
pip3 install -r requirements.txt
# Instala dependencias de scraper de Tableau
bash setup_scraper-tableau.bash
```


## Descripción

El programa consta de dos scripts separados: 
- scraper: obtiene datos de "Datos Abiertos Perú".
- scraper-tableau: obtiene datos del CMP sobre médicos vacunados.

### *scraper.py*

Genera 3 distintas tablas de salida con sus respetivas columnas que se encuentran dentro de la carpeta `resultados/`

1. `departamentos.csv`: FECHA_CORTE, DEPARTAMENTO, DOSIS1, DOSIS2
2. `dosis1.csv`: FECHA_CORTE, FECHA_VACUNACION, DOSIS, TOTAL, ACUMULADO
3. `dosis2.csv`: FECHA_CORTE, FECHA_VACUNACION, DOSIS, TOTAL, ACUMULADO

Dónde: 

- `FECHA_CORTE`: Fecha hasta la cuál se ha realizado el conteo.
- `DEPARTAMENTO`: Subregión del país, nivel 2.
- `DOSIS1`: Cantidad de vacunas aplicadas en un `DEPARTAMENTO` específico, hasta la `FECHA_CORTE`
- `DOSIS2`: Cantidad de vacunas aplicadas en un `DEPARTAMENTO` específico, hasta la `FECHA_CORTE`
- `FECHA_VACUNACION`: Fecha de vacunación de la dosis.
- `DOSIS`: Nº de dosis aplicada.
- `TOTAL`: Número de personas vacunadas el día `FECHA_VACUNACION`
- `ACUMULADO`: Número de personas vacunadas hasta el día `FECHA_CORTE`

### *scraper-tableau.py*

Este scraper simula abrir una ventana de Chrome con la librería `selenium` y obtiene una captura de pantalla. Luego, se extrae el texto de la imagen con `tesseract`.
