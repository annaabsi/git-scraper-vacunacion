import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
import datetime
import json
from urllib.request import urlopen

st.title("Dashboard")
st.write("My description")
x=0

###############################################################
df_departamentos=pd.read_csv("resultados/departamentos.csv")

fecha_corte= datetime.datetime.strptime(str(df_departamentos['FECHA_CORTE'][0]), '%Y%m%d').date()

st.header(f"1. Dosis por departamento [{fecha_corte}]")

col1, col2, col3 = st.beta_columns(3)
with col1:
    if st.button('Dosis 1'):
        x=1
    else:
        pass

with col2:
    if st.button('Dosis 2'):
        x=2
    else:
        pass

with col3:
    if st.button('Ambas Dosis'):
        x=3
    else:
        pass


if x==1:
    fig_dosis1_departamento = px.bar(df_departamentos, x='DEPARTAMENTO', y='DOSIS1')
    st.plotly_chart(fig_dosis1_departamento)

if x==2:
    fig_dosis2_departamento = px.bar(df_departamentos, x='DEPARTAMENTO', y='DOSIS2')
    st.plotly_chart(fig_dosis2_departamento)

if x==3 or x==0:
    fig_ambasdosis_departamento = px.bar(df_departamentos, x='DEPARTAMENTO', y=['DOSIS1','DOSIS2'])
    st.plotly_chart(fig_ambasdosis_departamento)

###############################################################
st.header(f"2. Dosis 1: diarias y totales [{fecha_corte}]")

df_dosis1 = pd.read_csv('resultados/dosis1.csv')

df_dosis1['FECHA_VACUNACION']=pd.to_datetime(df_dosis1['FECHA_VACUNACION'],format='%Y%m%d')

# st.write(df_dosis1)
fig_dosis1 = px.line(df_dosis1, x='FECHA_VACUNACION', y=['TOTAL','ACUMULADO']) # title='Time Series with Range Slider and Selectors'

fig_dosis1.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

st.plotly_chart(fig_dosis1)

###############################################################

st.header(f"3. Dosis 2: diarias y totales [{fecha_corte}]")

df_dosis2 = pd.read_csv('resultados/dosis2.csv')

df_dosis2['FECHA_VACUNACION']=pd.to_datetime(df_dosis2['FECHA_VACUNACION'],format='%Y%m%d')

# st.write(df_dosis1)
fig_dosis2 = px.line(df_dosis2, x='FECHA_VACUNACION', y=['TOTAL','ACUMULADO']) # title='Time Series with Range Slider and Selectors'

fig_dosis2.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

st.plotly_chart(fig_dosis1)


######################################################################
st.header(f"4. Mapa al [{fecha_corte}]")

with urlopen('https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_departamental_simple.geojson') as response:
    departamentos = json.load(response)

fig = px.choropleth(df_departamentos, geojson=departamentos, locations='DEPARTAMENTO', color='DOSIS1',
                    color_continuous_scale="Viridis",
                    featureidkey="properties.NOMBDEP",
                    range_color=(0, 12),
                    scope="south america",
                    labels={'DOSIS1':'Dosis 1'}
                    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


######################################################################
st.header(f"5. Avance por región [{fecha_corte}]")

st.write(df_departamentos[['DEPARTAMENTO','DOSIS1','DOSIS2']])
