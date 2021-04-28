# Avance de la vacunación contra la Covid-19 en Perú

[![scraper-daily](https://github.com/annaabsi/git-scraper-vacunacion/actions/workflows/main.yml/badge.svg)](https://github.com/annaabsi/git-scraper-vacunacion/actions/workflows/main.yml)


## Instalación


### Linux (Probado en Python 3.8.1+)
```
# Instala requerimientos de Python
pip3 install -r requirements.txt
# Instala dependencias de scraper de Tableau
bash setup_scraper-tableau.bash
```


## Descripción

El programa consta de dos scripts separados: 
- scraper: obtiene [datos de "Datos Abiertos Perú"](https://www.datosabiertos.gob.pe/dataset/vacunaci%C3%B3n-contra-covid-19-ministerio-de-salud-minsa) sobre Vacunación contra COVID-19 - MINSA.
- scraper-tableau: obtiene [datos del CMP](https://www.cmp.org.pe/vacunometro-cmp/) sobre médicos vacunados.

### *scraper.py*

Genera 3 distintas tablas de salida con sus respetivas columnas que se encuentran dentro de la carpeta [resultados/](resultados/)

1. [departamentos.csv](departamentos.csv): FECHA_CORTE, DEPARTAMENTO, DOSIS1, DOSIS2, POBLACION, INDICE1, INDICE2
2. [dosis1.csv](dosis1.csv): FECHA_CORTE, FECHA_VACUNACION, DOSIS, TOTAL, ACUMULADO
3. [dosis2.csv](dosis2.csv): FECHA_CORTE, FECHA_VACUNACION, DOSIS, TOTAL, ACUMULADO

Dónde: 

- `FECHA_CORTE`: Fecha hasta la cuál se ha realizado el conteo.
- `DEPARTAMENTO`: Subregión del país, nivel 2.
- `DOSIS1`: Cantidad de vacunas aplicadas en un `DEPARTAMENTO` específico, hasta la `FECHA_CORTE`
- `DOSIS2`: Cantidad de vacunas aplicadas en un `DEPARTAMENTO` específico, hasta la `FECHA_CORTE`
- `FECHA_VACUNACION`: Fecha de vacunación de la dosis.
- `DOSIS`: Nº de dosis aplicada.
- `TOTAL`: Número de personas vacunadas el día `FECHA_VACUNACION`
- `ACUMULADO`: Número de personas vacunadas hasta el día `FECHA_CORTE`
- `POBLACION`: Población por departamento según el "Estado de la población peruana 2020" - [INEI](https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1743/Libro.pdf)
- `INDICE1`: Índice de vacunación por 100 000 hab para DOSIS1 = (DOSIS1/(POBLACION/100000))
- `INDICE2`: Índice de vacunación por 100 000 hab para DOSIS2 = (DOSIS2/(POBLACION/100000))

### *scraper-tableau.py*

Este scraper simula abrir una ventana de Chrome con la librería `selenium` y obtiene una captura de pantalla. Luego, se extrae el texto de la imagen con `tesseract`.
