import pandas as pd
import pandasql as ps

URL_DATA='https://cloud.minsa.gob.pe/s/ZgXoXqK2KLjRLxD/download'
df=pd.read_csv(URL_DATA)


# Delete all not wanted columns
df.drop(['UUID', 'GRUPO_RIESGO', 'EDAD','SEXO','FABRICANTE','DIRESA','PROVINCIA','DISTRITO'], axis=1, inplace=True)

# Please write the full query on one line
# ACUMULADO DOSIS 1
query_dosis1="""select FECHA_CORTE, FECHA_VACUNACION, DOSIS, count (rowid) as TOTAL, sum(count (rowid)) over (order by FECHA_VACUNACION) as ACUMULADO from df where "DOSIS" = 1 group by FECHA_VACUNACION """
result_query_dosis1=ps.sqldf(query_dosis1,locals())
print(ps.sqldf(query_dosis1,locals()))

# Please write the full query on one line
# ACUMULADO DOSIS 2
query_dosis2="""select FECHA_CORTE, FECHA_VACUNACION, DOSIS, count (rowid) as TOTAL, sum(count (rowid)) over (order by FECHA_VACUNACION) as ACUMULADO from df where "DOSIS" = 2 group by FECHA_VACUNACION"""
result_query_dosis2=ps.sqldf(query_dosis2,locals())
print(ps.sqldf(query_dosis2,locals()))

# Please write the full query on one line
# ACUMULADO DEPARTAMENTOS
query_departamentos="""select FECHA_CORTE, DEPARTAMENTO, count (case when DOSIS = 1 then 1 end) as DOSIS1, count (case when DOSIS = 2 then 1 end) as DOSIS2 from df group by DEPARTAMENTO"""
result_query_departamentos=ps.sqldf(query_departamentos,locals())
print(ps.sqldf(query_departamentos,locals()))

col_poblacion=[379384,
1083519,
405759,
1382730,
616176,
1341012,
994494,
1205527,
347639,
721047,
850765,
1246038,
1778080,
1197260,
9485405,
883510,
141070,
174863,
254065,
1856809,
1172697,
813381,
329332,
224863,
496459]

result_query_departamentos['POBLACION']=col_poblacion

result_query_departamentos['INDICE1']=round(result_query_departamentos['DOSIS1']/(result_query_departamentos['POBLACION']/100000)).astype('int')
result_query_departamentos['INDICE2']=round(result_query_departamentos['DOSIS2']/(result_query_departamentos['POBLACION']/100000)).astype('int')

result_query_dosis1.to_csv('resultados/dosis1.csv')
result_query_dosis2.to_csv('resultados/dosis2.csv')
result_query_departamentos.to_csv('resultados/departamentos.csv')


print('Anna Bananna----------------------------------------------')
