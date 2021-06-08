[![scraper-daily](https://github.com/annaabsi/git-scraper-vacunacion/actions/workflows/main.yml/badge.svg)](https://github.com/annaabsi/git-scraper-vacunacion/actions/workflows/main.yml)

<!-- PROJECT HEADER -->
<br />
<p align="center">
  <a href="#">
    <img src="https://data.larepublica.pe/avance-vacunacion-covid-19-peru/logo.png" alt="Logo" width="30%" >
  </a>

  <h3 align="center">Avance de la vacunación contra la Covid-19 en Perú</h3>

  <p align="center">
    <a href="https://data.larepublica.pe/avance-vacunacion-covid-19-peru">Publicación</a>
  </p>
</p>

<hr>

## Instalación 

### Linux (Probado en Python 3.8.1+)

Automatizado con [Github Actions](.github/workflows/main.yml)

Instalación
```bash
# Instala requerimientos de Python
pip3 install -r requirements.txt
# Instala dependencias de scraper de Tableau
bash setup_scraper-tableau.bash
```

Obtener resultados
```bash
# Obtener tablas resumen de datos abiertos
python3 scraper.py
# Obtener cifras de dashboards externos
python3 scraper-tableau.py
# Finalmente realizar commit
```


## Descripción

El programa consta de dos scripts separados: 
- scraper: obtiene [datos de "Datos Abiertos Perú"](https://www.datosabiertos.gob.pe/dataset/vacunaci%C3%B3n-contra-covid-19-ministerio-de-salud-minsa) sobre Vacunación contra COVID-19 - MINSA.
- scraper-tableau: obtiene [datos del CMP](https://www.cmp.org.pe/vacunometro-cmp/) sobre médicos vacunados.

### *scraper.py*

Genera 3 distintas tablas de salida con sus respetivas columnas que se encuentran dentro de la carpeta [resultados/](resultados/)

1. [departamentos.csv](resultados/departamentos.csv): DEPARTAMENTO,DOSIS1,DOSIS2,POBLACION,INDICE
2. [dosis1y2.csv](resultados/dosis1y2.csv): FECHA_VACUNACION,DOSIS1,DOSIS2
3. [acumulados1y2.csv](resultados/acumulados1y2.csv): FECHA_VACUNACION,DOSIS1,DOSIS2
4. [dosis2_por_edades.csv](resultados/dosis2_por_edades.csv): GRUPO_ETARIO,DOSIS2,POBLACION,PORCENTAJE
5. [fecha_corte.json](resultados/fecha_corte.json): fecha_corte

Dónde: 

- `fecha_corte`: Fecha hasta la cuál se ha realizado el conteo.
- `DEPARTAMENTO`: Subregión del país, nivel 2.
- `DOSIS1`: Cantidad de vacunas aplicadas en un `DEPARTAMENTO` específico, hasta la `FECHA_CORTE`
- `DOSIS2`: Cantidad de vacunas aplicadas en un `DEPARTAMENTO` específico, hasta la `FECHA_CORTE`
- `FECHA_VACUNACION`: Fecha de vacunación de la dosis.
<!-- - `DOSIS`: Nº de dosis aplicada. -->
<!-- - `TOTAL`: Número de personas vacunadas el día `FECHA_VACUNACION`
- `ACUMULADO`: Número de personas vacunadas hasta el día `FECHA_CORTE` -->
- `POBLACION`: Población por departamento según el "Estado de la población peruana 2020" - [INEI](https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1743/Libro.pdf)
- `INDICE1`: Índice de vacunación por 100 000 hab para Dosis 1 = (`DOSIS1`/(`POBLACION`/100000))
- `INDICE2`: Índice de vacunación por 100 000 hab para Dosis 2 = (`DOSIS2`/(`POBLACION`/100000))

### *scraper-tableau.py*

Este scraper simula abrir una ventana de Chrome con la librería `selenium` y obtiene una captura de pantalla. Luego, se extrae el texto de la imagen con `tesseract` y guarda los números en el archivo [ambas_dosis.json](resultados/ambas_dosis.json)
