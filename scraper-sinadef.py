import subprocess
from datetime import date, timedelta

import numpy as np
import pandas as pd
from py_essentials import hashing as hs

def _execute_shell_command(command):
    with subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT
                          ) as terminal_subprocess:
        stdout, stderr = terminal_subprocess.communicate()

        return stdout, stderr

try:
    _, _ = _execute_shell_command(['wget', '-O', 'DATA_SINADEF.zip', 'https://cloud.minsa.gob.pe/s/NctBnHXDnocgWAg/download'])
    _, _ = _execute_shell_command(['md5sum', 'DATA_SINADEF.zip', '>', './resultados/hashes/hash_sinadef_downloaded.txt'])


    # hash_downloaded = hs.fileChecksum("download", "sha256")

    # Get hash hash_sinadef_downloaded
    with open('resultados/hashes/hash_sinadef_downloaded.txt') as f:
        hash_downloaded = f.readlines()[0]

    # Get hash saved
    with open('resultados/hashes/hash_sinadef.txt') as f:
        hash_saved = f.readlines()[0]

    print(hash_downloaded)
    print(hash_saved)

    if hash_saved==hash_downloaded:
        print("SAME FILE")
    else:
        print("DIFFERENT FILE")

        _, _ = _execute_shell_command(['unzip', 'DATA_SINADEF.zip'])

        xls = pd.read_excel('./DATA_SINADEF/SINADEF_DATOS_ABIERTOS.xlsx',engine='openpyxl', index_col=0)  # <-- add .read()
        # xls

        xls.drop(['DEBIDO A (CAUSA A)', 'CAUSA A (CIE-X)', 'DEBIDO A (CAUSA B)', 'CAUSA B (CIE-X)', 'DEBIDO A (CAUSA C)', 'CAUSA C (CIE-X)','DEBIDO A (CAUSA D)', 'CAUSA D (CIE-X)', 'DEBIDO A (CAUSA E)', 'CAUSA E (CIE-X)', 'DEBIDO A (CAUSA F)', 'CAUSA F (CIE-X)'], axis=1, inplace=True)

        xls = xls.rename(columns={"COD# UBIGEO DOMICILIO": "UBIGEO", "PAIS DOMICILIO": "PAIS","DEPARTAMENTO DOMICILIO": "DEPARTAMENTO", "PROVINCIA DOMICILIO": "PROVINCIA", "DISTRITO DOMICILIO": "DISTRITO"})

        xls = xls.sort_values(by='FECHA')
        xls['FECHA'] = pd.to_datetime(xls['FECHA'], errors='coerce', dayfirst=True)
        xls['FECHA'] = pd.to_datetime(xls['FECHA'], format='%y-%m-%d', errors='ignore')
        # xls

        xls['FECHA'].replace('SIN REGISTRO', np.nan)
        xls['EDAD'].replace('SIN REGISTRO', np.nan)
        xls['FECHA'].dropna()
        xls['EDAD'].dropna()

        start_date = "2019-01-01"
        yesterday = date.today() - timedelta(days=1)
        end_date = yesterday.strftime("%Y-%m-%d")
        after_start_date = (xls["FECHA"] >= start_date) & (xls["FECHA"] < end_date)
        filtered_dates = xls.loc[after_start_date]

        xls_edad_anos = filtered_dates[filtered_dates['TIEMPO EDAD'] == 'AÑOS']
        # xls_edad_anos

        xls_edad_anos.EDAD = pd.to_numeric(xls_edad_anos.EDAD, errors='coerce')
        # xls_edad_anos

        df_total = xls_edad_anos.groupby(['FECHA', 'AÑO']).size().unstack()
        df_total = df_total.rename(columns=str).reset_index()
        # df_total

        df_total.to_csv('resultados/fallecidos_total.csv', index=False)

        bins = [17, 59, 69, 79, 130]

        rs = pd.cut(xls_edad_anos['EDAD'], bins)

        df = xls_edad_anos.groupby(['FECHA', rs]).size().unstack()
        df = df.rename(columns=str).reset_index()
        df = df.rename(columns={'(17, 59]': '18-59', '(59, 69]': '60-69',
                    '(69, 79]': '70-79', '(79, 130]': '80+'})
        # df

        df.to_csv('resultados/fallecidos_edad.csv', index=False)

        _, _ = _execute_shell_command(['rm','-rf', './DATA_SINADEF/'])
        _, _ = _execute_shell_command(['rm','-f', 'download'])

        # Save new hash
        file = open('resultados/hashes/hash_sinadef.txt', 'w')
        file.write(hash_downloaded)
        file.close()

except ConnectionResetError:
    pass