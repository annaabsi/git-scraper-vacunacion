import numpy as np
import pandas as pd
import py7zr
import requests
import zipfile
from py_essentials import hashing as hs
from pyunpack import Archive


def summary_by_department(df):

    df=df[['FECHA_VACUNACION','DOSIS','SEXO']].groupby(['FECHA_VACUNACION','DOSIS']).count()
    df=df.reset_index()
    df=df[df['DOSIS'].isin([1,2,3])]
    df=df.pivot(index='FECHA_VACUNACION', columns='DOSIS', values='SEXO')
    df=df.rename_axis(None, axis=1)
    df.columns=['DOSIS1','DOSIS2','DOSIS3']
    df=df.fillna(0).astype('int')
    return df

def districts_by_department(df):

    df=df[['DEPARTAMENTO','DISTRITO','DOSIS','SEXO']]
    df=df[df.DOSIS == 2].groupby(['DEPARTAMENTO','DISTRITO', 'DOSIS']).count()
    df.columns=['DOSIS2']
    df = pd.merge(df, df_poblacion_distritos,  how='inner', on=['DEPARTAMENTO','DISTRITO'])
    df['INDICE']=round(df['DOSIS3']/df['POBLACION']*100,2)
    return df

# run bash script to download data
def runCommand(command):
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output

if __name__ == '__main__':
    try:
        # url = "https://drive.minsa.gob.pe/s/qioYn4FDbsJ62Mw/download"
        # headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
        # req = requests.get(url, headers=headers)
        # print("Downloaded")

        # with open('vacunas_covid.7z', 'wb') as f:
        #     f.write(req.content)

        with py7zr.SevenZipFile('vacunas_covid.7z', mode='r') as z:
            z.extractall()

        # with zipfile.ZipFile('vacunas_covid.zip', 'r') as zip_ref:
        #     zip_ref.extractall()

        # Archive('vacunas_covid.7z').extractall('.')

        runCommand('bash process.sh')

        # chunks = [] # List to keep filtered chunk dataframes.

        # for chunked_data in pd.read_csv('vacunas_covid.csv',
        #  usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_VACUNACION', 'DOSIS', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'FABRICANTE'],
        #  parse_dates=['FECHA_VACUNACION'],
        #  chunksize = 1e7
        #  ):
        
        #     chunked_data=reduce_mem_usage(chunked_data)
        #     chunks.append(chunked_data)

        # df = pd.concat(chunks)
        # chunks=[]
        df=pd.read_csv('vacunas_covid.csv',
        usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_VACUNACION', 'DOSIS', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'FABRICANTE'],
        parse_dates=['FECHA_VACUNACION'],
        dtype={'FECHA_CORTE': 'str', 
                'EDAD': 'Int16',
                'SEXO': 'boolean',
                'FECHA_VACUNACION': 'str',
                'DOSIS': 'Int8',
                'DEPARTAMENTO': 'str',
                'PROVINCIA': 'str',
                'DISTRITO': 'str',
                'FABRICANTE': 'str',},
        on_bad_lines="warn",
        # na_values={
        #     'FECHA_CORTE': '',
        #     'EDAD': 0,
        #     'SEXO': 0,
        #     'FECHA_VACUNACION': '',
        #     'DOSIS': 0,
        #     'DEPARTAMENTO': '',
        #     'PROVINCIA': '',
        #     'DISTRITO': '',
        #     'FABRICANTE': '',
        # },
        # true_values=[1],
        # false_values=[0],
        low_memory=False,
        )

        print(df.head(10))
        print(df.info())
        #df=pd.read_csv('vacunas_covid.csv', usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_VACUNACION', 'DOSIS', 'DEPARTAMENTO', 'FABRICANTE'], parse_dates=['FECHA_VACUNACION'])
        fecha_corte=df['FECHA_CORTE'].drop_duplicates().set_axis(['fecha_corte'])
        fecha_corte.to_json("resultados/fecha_corte.json")
        df_poblacion_distritos=pd.read_csv('poblacion_distritos.csv')
        df_poblacion_provincias=pd.read_csv('poblacion_provincias.csv')

        # DIARIO DOSIS 1 Y DOSIS 2
        df_ambas_dosis=df[['FECHA_VACUNACION','DOSIS','SEXO']].groupby(['FECHA_VACUNACION','DOSIS']).count()
        df_ambas_dosis=df_ambas_dosis.reset_index()
        df_ambas_dosis=df_ambas_dosis[df_ambas_dosis['DOSIS'].isin([1,2,3])]
        df_ambas_dosis=df_ambas_dosis.pivot(index='FECHA_VACUNACION', columns='DOSIS', values='SEXO')
        df_ambas_dosis=df_ambas_dosis.rename_axis(None, axis=1)
        df_ambas_dosis.columns=['DOSIS1','DOSIS2','DOSIS3']
        df_ambas_dosis=df_ambas_dosis.fillna(0).astype('int')
        df_ambas_dosis

        # ACUMULADO DOSIS 1 Y DOSIS 2
        df_ambas_dosis_cum=df_ambas_dosis.cumsum()
        df_ambas_dosis_cum

        col_poblacion=[452125,
        1189403,
        440629,
        1488247,
        658081,
        1528904,
        1090990,
        1392648,
        414882,
        823560,
        889916,
        1340064,
        1955991,
        1325269,
        10741923,
        1096407,
        170503,
        190442,
        283946,
        1966703,
        1221523,
        920842,
        365771,
        235194,
        597287]

        # ACUMULADO POR DEPARTAMENTO (DOSIS 3 - DOSIS REFUERZO)
        df_ambas_dosis_departamento=df[['DEPARTAMENTO','DOSIS','SEXO']].groupby(['DEPARTAMENTO', 'DOSIS']).count()
        df_ambas_dosis_departamento=df_ambas_dosis_departamento.reset_index()
        df_ambas_dosis_departamento=df_ambas_dosis_departamento[df_ambas_dosis_departamento['DOSIS'].isin([1,2,3])]
        df_ambas_dosis_departamento=df_ambas_dosis_departamento.pivot(index='DEPARTAMENTO', columns='DOSIS', values='SEXO')
        df_ambas_dosis_departamento.columns=['DOSIS1','DOSIS2','DOSIS3']
        df_ambas_dosis_departamento['POBLACION']=col_poblacion
        df_ambas_dosis_departamento['INDICE']=round(df_ambas_dosis_departamento['DOSIS3']/(df_ambas_dosis_departamento['POBLACION']/100000)).astype('int')
        df_ambas_dosis_departamento=df_ambas_dosis_departamento.fillna(0).astype('int')
        df_ambas_dosis_departamento

        # ACUMULADO POR GRUPO ETARIO (DOSIS 3 - DOSIS REFUERZO)
        bins = [5,12,18,30,40,50,60,80,df['EDAD'].max()+1]
        labels = ['5 a 11 años','12 a 17 años','18 a 29 años','30 a 39 años','40 a 49 años','50 a 59 años','60 a 79 años','80 años a más']
        poblacion_por_grupo_etario = [4201842,3614488,6788969,5382481,4604711,3524112,3851743,812904]
        df_edades = df
        df_edades['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
        df_edades = df_edades[df_edades.DOSIS == 3].groupby(['GRUPO_ETARIO'])["DOSIS"].count().reset_index()
        df_edades.rename(columns = {'DOSIS':'DOSIS3'}, inplace = True)
        df_edades['POBLACION']=poblacion_por_grupo_etario
        df_edades['PORCENTAJE']=round(df_edades['DOSIS3']/df_edades['POBLACION']*100,2)
        df_edades=df_edades.set_index('GRUPO_ETARIO')
        df_edades

        # ACUMULADO POR GRUPO ETARIO (DOSIS 1)
        df_edades_1 = df
        df_edades_1['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
        df_edades_1 = df_edades_1[df_edades_1.DOSIS == 1].groupby(['GRUPO_ETARIO'])["DOSIS"].count().reset_index()
        df_edades_1.rename(columns = {'DOSIS':'DOSIS1'}, inplace = True)
        df_edades_1['POBLACION']=poblacion_por_grupo_etario
        df_edades_1['PORCENTAJE']=round(df_edades_1['DOSIS1']/df_edades_1['POBLACION']*100,2)
        df_edades_1=df_edades_1.set_index('GRUPO_ETARIO')
        df_edades_1

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

        # # DATA PONGO EL HOMBRO
        # from requests_html import HTMLSession
        # session = HTMLSession()
        # r = session.get('https://www.gob.pe/pongoelhombro#contador-de-vacunados')
        # scrap_contador_vacunados = r.html.find('.font-bold.text-3xl')
        # d = []
        # for number in scrap_contador_vacunados:
        #     d.append(number.text)
        d = [df_ambas_dosis_cum['DOSIS1'][-1], df_ambas_dosis_cum['DOSIS2'][-1], df_ambas_dosis_cum['DOSIS3'][-1], df_ambas_dosis['DOSIS1'][-1], df_ambas_dosis['DOSIS2'][-1], df_ambas_dosis_cum.iloc[-1].sum(), df_ambas_dosis.iloc[-1].sum(), df_ambas_dosis_cum['DOSIS2'][-1]]
        d = list(map(str,d))
        contador_vacunados = pd.Series(d,index=['total_dosis1','total_dosis2','total_dosis3','ayer_dosis1','ayer_dosis2','total_dosis','ayer_total_dosis','vacunacion_completa'])
        contador_vacunados.to_json('resultados/pongo_el_hombro.json')

        # DIARIO POR DEPARTAMENTO
        list_departamentos = ["AMAZONAS",
                        "ANCASH",
                        "APURIMAC",
                        "AREQUIPA",
                        "AYACUCHO",
                        "CAJAMARCA",
                        "CALLAO",
                        "CUSCO",
                        "HUANCAVELICA",
                        "HUANUCO",
                        "ICA",
                        "JUNIN",
                        "LA LIBERTAD",
                        "LAMBAYEQUE",
                        "LIMA",
                        "LORETO",
                        "MADRE DE DIOS",
                        "MOQUEGUA",
                        "PASCO",
                        "PIURA",
                        "PUNO",
                        "SAN MARTIN",
                        "TACNA",
                        "TUMBES",
                        "UCAYALI"]

        for department_name in list_departamentos:
            df_by_department=df[df['DEPARTAMENTO'] == department_name]
            df_filtered=summary_by_department(df_by_department)
            df_filtered.to_csv(f"resultados/departamentos/{department_name.lower()}.csv")

        # PROVINCIAS CRITICAS
        df_ambas_dosis_provincia=df[['PROVINCIA','DOSIS','SEXO']].groupby(['PROVINCIA', 'DOSIS']).count()
        df_ambas_dosis_provincia=df_ambas_dosis_provincia.reset_index()
        df_ambas_dosis_provincia=df_ambas_dosis_provincia[df_ambas_dosis_provincia['DOSIS'].isin([1,2,3])]
        df_ambas_dosis_provincia=df_ambas_dosis_provincia.pivot(index='PROVINCIA', columns='DOSIS', values='SEXO')
        df_ambas_dosis_provincia.columns=['DOSIS1','DOSIS2','DOSIS3']
        df_ambas_dosis_provincia = pd.merge(df_ambas_dosis_provincia, df_poblacion_provincias,  how='inner', on=['PROVINCIA'])
        df_ambas_dosis_provincia['INDICE']=round(df_ambas_dosis_provincia['DOSIS3']/df_ambas_dosis_provincia['POBLACION']*100,2)
        df_ambas_dosis_provincia=df_ambas_dosis_provincia.fillna(0)
        df_ambas_dosis_provincia

        # DISTRITOS POR DEPARTAMENTOS CRITICOS
        list_departamentos_criticos = ["AMAZONAS",
                    "AYACUCHO",
                    "HUANCAVELICA",
                    "HUANUCO",
                    "JUNIN",
                    "LAMBAYEQUE",
                    "LORETO",
                    "MADRE DE DIOS",
                    "PIURA",
                    "PUNO",
                    "UCAYALI"]

        for department_name in list_departamentos_criticos:
            df_by_department=df[df['DEPARTAMENTO'] == department_name]
            df_filtered=districts_by_department(df_by_department)
            df_filtered.to_csv(f"resultados/distritos_por_departamento/{department_name.lower()}.csv")
        
        # # TOTAL DE 11 A 16 AÑOS
        # bins = [11,12,13,14,15,16,17]
        # labels = ['11 años','12 años','13 años','14 años','15 años','16 años'] 
        # df_11_16 = df
        # df_11_16['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
        # df_11_16 = df_11_16[df_11_16.DOSIS == 2].groupby(['GRUPO_ETARIO'])["DOSIS"].count().reset_index()
        # df_11_16.rename(columns = {'DOSIS':'DOSIS2'}, inplace = True)
        # df_11_16=df_11_16.set_index('GRUPO_ETARIO')
        # df_11_16

        # # ACUMULADO DE 11 A 16 AÑOS
        # df_11_16_diario = df
        # df_11_16_diario = df[df['EDAD'].isin([11,12,13,14,15,16])]
        # df_11_16_diario = df_11_16_diario[df_11_16_diario.DOSIS == 2].groupby(['FECHA_VACUNACION'])["DOSIS"].count().reset_index()
        # df_11_16_diario = df_11_16_diario.set_index('FECHA_VACUNACION')
        # df_11_16_diario.rename(columns = {'DOSIS':'DOSIS2'}, inplace = True)
        # df_11_16_diario_cum = df_11_16_diario.cumsum()
        # df_11_16_diario_cum

        df_ambas_dosis.to_csv('resultados/dosis1y2.csv')
        df_ambas_dosis_cum.to_csv('resultados/acumulados1y2.csv')
        df_ambas_dosis_departamento.to_csv('resultados/departamentos.csv')
        df_ambas_dosis_provincia.to_csv('resultados/provincias_criticas.csv')
        df_edades.to_csv('resultados/dosis2_por_edades.csv')
        df_edades_1.to_csv('resultados/dosis1_por_edades.csv')
        df_fabricante.to_csv('resultados/diario_por_fabricante.csv')
        df_fabricante_cum.to_csv('resultados/acumulado_por_fabricante.csv')

        # df_11_16.to_csv('resultados/11_a_16_anios.csv')
        # df_11_16_diario_cum.to_csv('resultados/acumulado_11_a_16_anios.csv')

        # Save new hash
        # file = open('resultados/hashes/hash_scraper.txt', 'w')
        # file.write(hash_downloaded)
        # file.close()

    except ConnectionResetError:
        # error de peers
        pass
