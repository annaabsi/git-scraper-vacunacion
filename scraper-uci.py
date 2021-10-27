import pandas as pd
import requests

try:
    url = "http://datos.susalud.gob.pe/sites/default/files/Camas_26-10-2021.csv"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
    req = requests.get(url, headers=headers)

    with open('camas_uci.csv', 'wb') as f:
        f.write(req.content)
    
    df=pd.read_csv('camas_uci.csv', usecols=['FECHACORTE', 'REGION', 'ZC_UCI_ADUL_CAM_TOTAL','ZC_UCI_ADUL_CAM_INOPERATIVOS', 'ZC_UCI_ADUL_CAM_TOT_OPER', 'ZC_UCI_ADUL_CAM_TOT_DISP', 'ZC_UCI_ADUL_CAM_TOT_OCUP'], sep='|')
    fecha_corte = df['FECHACORTE'].tail(1)

    df_camas_uci=df[df['FECHACORTE'] == fecha_corte.values[0]].reset_index(drop=True)
    df_camas_uci=df_camas_uci.groupby(['FECHACORTE','REGION']).sum().astype('int')
    df_camas_uci.to_csv('resultados/camas_uci.csv')

except ConnectionResetError:
    # error de peers
    pass