import numpy as np
import pandas as pd
import zipfile
from urllib.request import urlopen, Request
import io
from datetime import date, timedelta

req = Request('https://cloud.minsa.gob.pe/s/NctBnHXDnocgWAg/download')
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')

# open and save the zip file onto computer
#url = urlopen(req)

file = zipfile.ZipFile((io.BytesIO(urlopen(req).read())))
file_name = file.namelist()[1]
#file_name
xls = pd.read_excel(file.open(file_name).read(), engine='openpyxl', index_col=0)  # <-- add .read()
xls

xls.drop(['DEBIDO A (CAUSA A)','CAUSA A (CIE-X)', 'DEBIDO A (CAUSA B)', 'CAUSA B (CIE-X)', 'DEBIDO A (CAUSA C)', 'CAUSA C (CIE-X)', 'DEBIDO A (CAUSA D)', 'CAUSA D (CIE-X)', 'DEBIDO A (CAUSA E)', 'CAUSA E (CIE-X)', 'DEBIDO A (CAUSA F)','CAUSA F (CIE-X)'], axis=1, inplace=True)

xls = xls.rename(columns={"COD# UBIGEO DOMICILIO": "UBIGEO","PAIS DOMICILIO": "PAIS","DEPARTAMENTO DOMICILIO": "DEPARTAMENTO", "PROVINCIA DOMICILIO": "PROVINCIA", "DISTRITO DOMICILIO": "DISTRITO"})

xls = xls.sort_values(by = 'FECHA')
xls['FECHA'] = pd.to_datetime(xls['FECHA'], errors='coerce', dayfirst=True)
xls['FECHA'] = pd.to_datetime(xls['FECHA'], format='%y-%m-%d', errors='ignore')
xls

xls['FECHA'].replace('SIN REGISTRO', np.nan)
xls['EDAD'].replace('SIN REGISTRO', np.nan)
xls['FECHA'].dropna()
xls['EDAD'].dropna()

start_date = "2019-01-01"
yesterday = date.today() - timedelta(days=1)
end_date = yesterday.strftime("%Y-%m-%d")
after_start_date = (xls["FECHA"] >= start_date) & (xls["FECHA"] < end_date)
filtered_dates = xls.loc[after_start_date]

xls_edad_anos = filtered_dates[filtered_dates['TIEMPO EDAD']=='AÑOS']
xls_edad_anos

xls_edad_anos.EDAD = pd.to_numeric(xls_edad_anos.EDAD, errors='coerce')
xls_edad_anos

df_total = xls_edad_anos.groupby(['FECHA', 'AÑO']).size().unstack()
df_total = df_total.rename(columns=str).reset_index()
df_total

df_total.to_csv('resultados/fallecidos_total.csv' , index=False)

bins = [17, 59, 69, 79, 130]

rs = pd.cut(xls_edad_anos['EDAD'], bins)

df = xls_edad_anos.groupby(['FECHA', rs]).size().unstack()
df = df.rename(columns=str).reset_index()
df = df.rename(columns={'(17, 59]': '18-59', '(59, 69]': '60-69', '(69, 79]': '70-79', '(79, 130]' : '80+'})
df

df.to_csv('resultados/fallecidos_edad.csv' , index=False)