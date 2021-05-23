import pandas as pd

df=pd.read_csv('https://cloud.minsa.gob.pe/s/ZgXoXqK2KLjRLxD/download', usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_VACUNACION', 'DOSIS', 'DEPARTAMENTO'],parse_dates=['FECHA_VACUNACION'])
#df=pd.read_csv('vacunas_covid.csv', usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_VACUNACION', 'DOSIS', 'DEPARTAMENTO'], parse_dates=['FECHA_VACUNACION'])
fecha_corte=df['FECHA_CORTE'].drop_duplicates().set_axis(['fecha_corte'])
fecha_corte.to_json("/resultados/fecha_corte.json")

#DIARIO DOSIS 1 Y DOSIS 2
df_ambas_dosis=df[['FECHA_VACUNACION','DOSIS','SEXO']].groupby(['FECHA_VACUNACION','DOSIS']).count()
df_ambas_dosis=df_ambas_dosis.reset_index()
df_ambas_dosis=df_ambas_dosis.pivot(index='FECHA_VACUNACION', columns='DOSIS', values='SEXO')
df_ambas_dosis=df_ambas_dosis.rename_axis(None, axis=1)
df_ambas_dosis.columns=['DOSIS1','DOSIS2']
df_ambas_dosis=df_ambas_dosis.fillna(0).astype('int')
df_ambas_dosis

#ACUMULADO DOSIS 1 Y DOSIS 2
df_ambas_dosis_cum=df_ambas_dosis.cumsum()
df_ambas_dosis_cum

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

# ACUMULADO POR DEPARTAMENTO (DOSIS 2 - VACUNACION COMPLETA)
df_ambas_dosis_departamento=df[['DEPARTAMENTO','DOSIS','SEXO']].groupby(['DEPARTAMENTO', 'DOSIS']).count()
df_ambas_dosis_departamento=df_ambas_dosis_departamento.reset_index()
df_ambas_dosis_departamento=df_ambas_dosis_departamento.pivot(index='DEPARTAMENTO', columns='DOSIS', values='SEXO')
df_ambas_dosis_departamento.columns=['DOSIS1','DOSIS2']
df_ambas_dosis_departamento['POBLACION']=col_poblacion
df_ambas_dosis_departamento['INDICE']=round(df_ambas_dosis_departamento['DOSIS2']/(df_ambas_dosis_departamento['POBLACION']/100000)).astype('int')
df_ambas_dosis_departamento

# ACUMULADO POR GRUPO ETARIO (DOSIS 2 - VACUNACION COMPLETA)
bins = [18,20,30,40,50,60,70,80,df['EDAD'].max()+1]
labels = ['18 a 19 años','20 a 29 años','30 a 39 años','40 a 49 años','50 a 59 años','60 a 69 años','70 a 79 años','80 años a más']
poblacion_por_grupo_etario = [900000,5700000,5300000,4400000,3300000,2300000,1300000,700000] 
df_edades = df
df_edades['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
df_edades = df_edades[df_edades.DOSIS == 2].groupby(['GRUPO_ETARIO'])["DOSIS"].count().reset_index()
df_edades.rename(columns = {'DOSIS':'DOSIS2'}, inplace = True)
df_edades['POBLACION']=poblacion_por_grupo_etario
df_edades['PORCENTAJE']=round(df_edades['DOSIS2']/df_edades['POBLACION']*100,2)
df_edades=df_edades.set_index('GRUPO_ETARIO')
df_edades

df_ambas_dosis.to_csv('resultados/dosis1y2.csv')
df_ambas_dosis_cum.to_csv('resultados/acumulados1y2.csv')
df_ambas_dosis_departamento.to_csv('resultados/departamentos.csv')
df_edades.to_csv('resultados/dosis2_por_edades.csv')