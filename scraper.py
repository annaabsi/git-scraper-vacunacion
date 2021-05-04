import pandas as pd
import pandasql as ps

URL_DATA='https://cloud.minsa.gob.pe/s/ZgXoXqK2KLjRLxD/download'
df=pd.read_csv(URL_DATA)


# Delete all not wanted columns
df.drop(['UUID', 'GRUPO_RIESGO', 'EDAD','SEXO','FABRICANTE','DIRESA','PROVINCIA','DISTRITO'], axis=1, inplace=True)

# Please write the full query on one line
# DOSIS 1 y 2
query_dosis="""select FECHA_CORTE, FECHA_VACUNACION, count (case when DOSIS = 1 then 1 end) as DOSIS1, count (case when DOSIS = 2 then 1 end) as DOSIS2 from df group by FECHA_VACUNACION """
result_query_dosis=ps.sqldf(query_dosis,locals())
print(ps.sqldf(query_dosis,locals()))

# Please write the full query on one line
# ACUMULADOS DOSIS 1 Y 2
query_acumulados="""select FECHA_CORTE, FECHA_VACUNACION, sum(count (case when DOSIS = 1 then 1 end)) over (order by FECHA_VACUNACION) as ACUMULADO1, sum(count (case when DOSIS = 2 then 1 end)) over (order by FECHA_VACUNACION) as ACUMULADO2 from df group by FECHA_VACUNACION"""
result_query_acumulados=ps.sqldf(query_acumulados,locals())
print(ps.sqldf(query_acumulados,locals()))

# Please write the full query on one line
# ACUMULADO DEPARTAMENTOS
query_departamentos="""select FECHA_CORTE, DEPARTAMENTO, count (case when DOSIS = 1 then 1 end) as DOSIS1, count (case when DOSIS = 2 then 1 end) as DOSIS2 from df group by DEPARTAMENTO"""
result_query_departamentos=ps.sqldf(query_departamentos,locals())
print(ps.sqldf(query_departamentos,locals()))

col_poblacion=[426806,
1180638,
430736,
1497438,
668213,
1453711,
1129854,
1357075,
365317,
760267,
975182,
1361467,
2016771,
1310785,
10628470,
1027559,
173811,
192740,
271904,
2047954,
1237997,
899648,
370974,
251521,
589110]

result_query_departamentos['POBLACION']=col_poblacion

result_query_departamentos['INDICE1']=round(result_query_departamentos['DOSIS1']/(result_query_departamentos['POBLACION']/100000)).astype('int')
result_query_departamentos['INDICE2']=round(result_query_departamentos['DOSIS2']/(result_query_departamentos['POBLACION']/100000)).astype('int')

result_query_dosis.to_csv('resultados/dosis1y2.csv')
result_query_acumulados.to_csv('resultados/acumulados1y2.csv')
result_query_departamentos.to_csv('resultados/departamentos.csv')
