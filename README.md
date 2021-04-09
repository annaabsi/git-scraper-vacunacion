# Resumidor de vacunación

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


<!-- Anna Bananna -->