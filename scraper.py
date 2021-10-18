import pandas as pd
import py7zr
import requests
from py_essentials import hashing as hs

try:
    url = "https://cloud.minsa.gob.pe/s/To2QtqoNjKqobfw/download"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
    req = requests.get(url, headers=headers)

    with open('vacunas_covid.7z', 'wb') as f:
        f.write(req.content)

    hash_downloaded = hs.fileChecksum("vacunas_covid.7z", "sha256")

    # Get hash saved
    with open('resultados/hashes/hash_scraper.txt') as f:
        hash_saved = f.readlines()[0]

    if hash_saved==hash_downloaded:
        print("SAME FILE")
    else:
        print("DIFFERENT FILE")

        with py7zr.SevenZipFile('vacunas_covid.7z', mode='r') as z:
            z.extractall()

        df=pd.read_csv('vacunas_covid.csv', usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_VACUNACION', 'DOSIS', 'DEPARTAMENTO', 'FABRICANTE'],parse_dates=['FECHA_VACUNACION'])
        print(df.head(10))
        #df=pd.read_csv('vacunas_covid.csv', usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_VACUNACION', 'DOSIS', 'DEPARTAMENTO', 'FABRICANTE'], parse_dates=['FECHA_VACUNACION'])
        fecha_corte=df['FECHA_CORTE'].drop_duplicates().set_axis(['fecha_corte'])
        fecha_corte.to_json("resultados/fecha_corte.json")

        # DIARIO DOSIS 1 Y DOSIS 2
        df_ambas_dosis=df[['FECHA_VACUNACION','DOSIS','SEXO']].groupby(['FECHA_VACUNACION','DOSIS']).count()
        df_ambas_dosis=df_ambas_dosis.reset_index()
        df_ambas_dosis=df_ambas_dosis.pivot(index='FECHA_VACUNACION', columns='DOSIS', values='SEXO')
        df_ambas_dosis=df_ambas_dosis.rename_axis(None, axis=1)
        df_ambas_dosis.columns=['DOSIS1','DOSIS2','DOSIS3']
        df_ambas_dosis=df_ambas_dosis.fillna(0).astype('int')
        df_ambas_dosis

        # ACUMULADO DOSIS 1 Y DOSIS 2
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
        df_ambas_dosis_departamento.columns=['DOSIS1','DOSIS2','DOSIS3']
        df_ambas_dosis_departamento['POBLACION']=col_poblacion
        df_ambas_dosis_departamento['INDICE']=round(df_ambas_dosis_departamento['DOSIS2']/(df_ambas_dosis_departamento['POBLACION']/100000)).astype('int')
        df_ambas_dosis_departamento=df_ambas_dosis_departamento.fillna(0).astype('int')
        df_ambas_dosis_departamento

        # ACUMULADO POR GRUPO ETARIO (DOSIS 2 - VACUNACION COMPLETA)
        bins = [18,30,40,50,60,70,80,df['EDAD'].max()+1]
        labels = ['18 a 29 años','30 a 39 años','40 a 49 años','50 a 59 años','60 a 69 años','70 a 79 años','80 años a más']
        poblacion_por_grupo_etario = [6303670,5031117,4183174,3277134,2221241,1271842,647355] 
        df_edades = df
        df_edades['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
        df_edades = df_edades[df_edades.DOSIS == 2].groupby(['GRUPO_ETARIO'])["DOSIS"].count().reset_index()
        df_edades.rename(columns = {'DOSIS':'DOSIS2'}, inplace = True)
        df_edades['POBLACION']=poblacion_por_grupo_etario
        df_edades['PORCENTAJE']=round(df_edades['DOSIS2']/df_edades['POBLACION']*100,2)
        df_edades=df_edades.set_index('GRUPO_ETARIO')
        df_edades

        # DIARIO POR FABRICANTE
        df_fabricante=df[['FECHA_VACUNACION','FABRICANTE','SEXO']].groupby(['FECHA_VACUNACION','FABRICANTE']).count()
        df_fabricante=df_fabricante.reset_index()
        df_fabricante=df_fabricante.pivot(index='FECHA_VACUNACION', columns='FABRICANTE', values='SEXO')
        df_fabricante=df_fabricante.rename_axis(None, axis=1)
        df_fabricante=df_fabricante.fillna(0).astype('int')
        df_fabricante

        # ACUMULADO POR FABRICANTE
        df_fabricante_cum=df_fabricante.cumsum()
        df_fabricante_cum

        # DATA PONGO EL HOMBRO
        from requests_html import HTMLSession
        session = HTMLSession()
        r = session.get('https://www.gob.pe/pongoelhombro#contador-de-vacunados')
        scrap_contador_vacunados = r.html.find('.font-bold.text-3xl')
        d = []
        for number in scrap_contador_vacunados:
            d.append(number.text)
        contador_vacunados = pd.Series(d,index=['total_dosis1', 'total_dosis2','ayer_dosis1','ayer_dosis2','total_dosis','ayer_total_dosis','vacunacion_completa'])
        contador_vacunados.to_json('resultados/pongo_el_hombro.json')

        # DIARIO DOSIS 1 Y DOSIS 2: TACNA
        df_tacna=df[df['DEPARTAMENTO'] == 'TACNA']
        df_diario_tacna=df_tacna[['FECHA_VACUNACION','DOSIS','SEXO']].groupby(['FECHA_VACUNACION','DOSIS']).count()
        df_diario_tacna=df_diario_tacna.reset_index()
        df_diario_tacna=df_diario_tacna.pivot(index='FECHA_VACUNACION', columns='DOSIS', values='SEXO')
        df_diario_tacna=df_diario_tacna.rename_axis(None, axis=1)
        df_diario_tacna.columns=['DOSIS1','DOSIS2']
        df_diario_tacna=df_diario_tacna.fillna(0).astype('int')
        df_diario_tacna

        # TOTAL DE 11 A 16 AÑOS
        bins = [11,12,13,14,15,16,17]
        labels = ['11 años','12 años','13 años','14 años','15 años','16 años'] 
        df_11_16 = df
        df_11_16['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
        df_11_16 = df_11_16[df_11_16.DOSIS == 2].groupby(['GRUPO_ETARIO'])["DOSIS"].count().reset_index()
        df_11_16.rename(columns = {'DOSIS':'DOSIS2'}, inplace = True)
        df_11_16=df_11_16.set_index('GRUPO_ETARIO')
        df_11_16

        # ACUMULADO DE 11 A 16 AÑOS
        df_11_16_diario = df
        df_11_16_diario = df[df['EDAD'].isin([11,12,13,14,15,16])]
        df_11_16_diario = df_11_16_diario[df_11_16_diario.DOSIS == 2].groupby(['FECHA_VACUNACION'])["DOSIS"].count().reset_index()
        df_11_16_diario = df_11_16_diario.set_index('FECHA_VACUNACION')
        df_11_16_diario.rename(columns = {'DOSIS':'DOSIS2'}, inplace = True)
        df_11_16_diario_cum = df_11_16_diario.cumsum()
        df_11_16_diario_cum

        df_ambas_dosis.to_csv('resultados/dosis1y2.csv')
        df_ambas_dosis_cum.to_csv('resultados/acumulados1y2.csv')
        df_ambas_dosis_departamento.to_csv('resultados/departamentos.csv')
        df_edades.to_csv('resultados/dosis2_por_edades.csv')
        df_fabricante.to_csv('resultados/diario_por_fabricante.csv')
        df_fabricante_cum.to_csv('resultados/acumulado_por_fabricante.csv')
        df_diario_tacna.to_csv('resultados/tacna.csv')
        df_11_16.to_csv('resultados/11_a_16_anios.csv')
        df_11_16_diario_cum.to_csv('resultados/acumulado_11_a_16_anios.csv')

        # Save new hash
        file = open('resultados/hashes/hash_scraper.txt', 'w')
        file.write(hash_downloaded)
        file.close()

except ConnectionResetError:
    # error de peers
    pass
