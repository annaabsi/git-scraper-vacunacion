import pandas as pd

try:
    url = "http://datos.susalud.gob.pe/node/548/download"
    df=pd.read_csv(url, usecols=['FECHACORTE', 'REGION', 'ZC_UCI_ADUL_CAM_TOTAL','ZC_UCI_ADUL_CAM_INOPERATIVOS', 'ZC_UCI_ADUL_CAM_TOT_OPER', 'ZC_UCI_ADUL_CAM_TOT_DISP', 'ZC_UCI_ADUL_CAM_TOT_OCUP'], sep='|')
    fecha_corte = df['FECHACORTE'].tail(1)

    df_camas_uci=df[df['FECHACORTE'] == fecha_corte.values[0]].reset_index(drop=True)
    df_camas_uci=df_camas_uci.groupby(['FECHACORTE','REGION']).sum().astype('int')
    df_camas_uci.to_csv('resultados/camas_uci.csv')

except ConnectionResetError:
    # error de peers
    pass
