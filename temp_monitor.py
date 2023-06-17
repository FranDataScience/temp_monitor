import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_echarts import st_echarts
import time
import sqlite3
from sqlalchemy import create_engine
import time
import datetime
from streamlit.components.v1 import html

#CONFIGURACION DE LA PÁGINA
st.set_page_config(
     page_title = 'CoolProData',
     page_icon = 'Logo CoolProData trans color.png',
     layout = 'wide')


#CARGAR DATOS
# df = pd.read_csv('tablon_datos.csv', sep = ',', parse_dates = ['fecha']).set_index('fecha')

# Información de conexión a la base de datos
host = 'auth-db928.hstgr.io'
user = 'u953770621_tempuser'
password = 'nlpBi=NgX;9'
database = 'u953770621_tempdata'

# Crear la cadena de conexión usando SQLAlchemy
connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"

# Configurar la página de Streamlit
st.title("Últimos registros")

# Mostrar el logo de CoolProData en el sidebar
st.sidebar.image('Logo CoolProData trans color 400x293.png')

# Agregar el icono de termómetro utilizando el componente html
html_code = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<span style="display: inline-flex; align-items: center;">
    <i class="fa fa-thermometer-full" style="margin-right: 5px;"></i>
    <h2 style="margin: 0; margin-left: 10px;">Real Time DATA</h2>
</span>
'''
st.sidebar.markdown(html_code, unsafe_allow_html=True)


# Obtener y mostrar las temperaturas en el sidebar
sidebar_temp = st.sidebar.empty()

# Definir la función de transformación para Tª
def transform_bits_T(B):
    if B <= 1187:
        return 0.0000000103224*B**3 + -0.0000349642182*B**2 + 0.0698133944850*B + -35.8794110121062
    elif B > 1187 and B <= 2535:
        return 0.0000000027044*B**3 + -0.0000128640904*B**2 + 0.0482934758650*B + -28.8457090426883
    elif B > 2535:
        return -0.0000000056532*B**3 + 0.0000488967642*B**2 + -0.1016331415578*B + 90.1890811324308
    else:
        return B
    
# Definir la función de transformación para Presión
def transform_bits_P(B):
    return 0.0030380736*B -1.70948139


# Obtener y mostrar las temperaturas en el sidebar
while True:
    # Crear el objeto de conexión SQLAlchemy
    engine = create_engine(connection_string)

    # Consulta SQL para obtener el registro más reciente
    query = "SELECT * FROM DataSensors1 ORDER BY id DESC LIMIT 1"
    
    num_registros = 500  # Número de registros a obtener
    query2 = f"SELECT * FROM DataSensors1 ORDER BY id DESC LIMIT {num_registros};"

    # Ejecutar la consulta y cargar los datos en un DataFrame
    df = pd.read_sql(query, engine)
    df2 = pd.read_sql(query2, engine)
    
    # Establece la columna 'fecha' como índice
    df.set_index('fecha', inplace=True)
    df2.set_index('fecha', inplace=True)
    # Seleccionar las columnas deseadas
    df = df[['DAT1','DAT2','DAT3','DAT4','DAT5','DAT6','DAT7','DAT8','DAT10','DAT11','XHT1T']].copy()
    df.dropna(inplace = True)
    df2 = df2[['DAT1','DAT2','DAT3','DAT4','DAT5','DAT6','DAT7','DAT8','DAT10','DAT11','XHT1T']].copy()
    df2.dropna(inplace = True)
    # Cambiamos nombres de las variables
    df.columns = ['t_air_ee','t_air_se','t_ext','t_cam','t_cond','t_air_sc','t_air_ec','t_evap','pb','pa','temp']
    df2.columns = ['t_air_ee','t_air_se','t_ext','t_cam','t_cond','t_air_sc','t_air_ec','t_evap','pb','pa','temp']
    # Convertimos temp en float
    df['temp'] = round(df['temp'].astype(float),1)
    df2['temp'] = round(df2['temp'].astype(float),1)
    
    # Transformar BITS a unidades de medida
    df['t_air_ee'] = round(df['t_air_ee'].apply(transform_bits_T),1)
    df['t_air_se'] = round(df['t_air_se'].apply(transform_bits_T),1)
    df['t_evap'] = round(df['t_evap'].apply(transform_bits_T),1)
    df['t_cam'] = round(df['t_cam'].apply(transform_bits_T),1)
    df['t_cond'] = round(df['t_cond'].apply(transform_bits_T),1)
    df['t_air_sc'] = round(df['t_air_sc'].apply(transform_bits_T),1)
    df['t_air_ec'] = round(df['t_air_ec'].apply(transform_bits_T),1)
    df['t_ext'] = round(df['t_ext'].apply(transform_bits_T),1)
    df['pb'] = round(df['pb'].apply(transform_bits_P),2)
    df['pa'] = round(df['pa'].apply(transform_bits_P),2)
    
    df2['t_air_ee'] = round(df2['t_air_ee'].apply(transform_bits_T),1)
    df2['t_air_se'] = round(df2['t_air_se'].apply(transform_bits_T),1)
    df2['t_evap'] = round(df2['t_evap'].apply(transform_bits_T),1)
    df2['t_cam'] = round(df2['t_cam'].apply(transform_bits_T),1)
    df2['t_cond'] = round(df2['t_cond'].apply(transform_bits_T),1)
    df2['t_air_sc'] = round(df2['t_air_sc'].apply(transform_bits_T),1)
    df2['t_air_ec'] = round(df2['t_air_ec'].apply(transform_bits_T),1)
    df2['t_ext'] = round(df2['t_ext'].apply(transform_bits_T),1)
    df2['pb'] = round(df2['pb'].apply(transform_bits_P),2)
    df2['pa'] = round(df2['pa'].apply(transform_bits_P),2)

    # Cerrar la conexión
    engine.dispose()

    # Obtener los valores de temperatura de las columnas
    fecha = df.index[0]  
    t_air_ee = df.iloc[0, 0]  
    t_air_se = df.iloc[0, 1]  
    t_ext = df.iloc[0, 2]
    t_cam = df.iloc[0, 3]
    t_cond = df.iloc[0, 4]
    t_air_sc = df.iloc[0, 5]
    t_air_ec = df.iloc[0, 6]
    t_evap = df.iloc[0, 7]
    pb = df.iloc[0, 8]
    t_air_sc = df.iloc[0, 9]
    temp = df.iloc[0, 10]
    
    
    
    # Mostrar las temperaturas en el sidebar  
     
    with st.sidebar:
        # Crear los marcadores vacíos para los valores
        fecha_marker = st.empty()
        t_evap_marker = st.empty()
        t_cam_marker = st.empty()
        t_cond_marker = st.empty()
        t_ext_marker = st.empty()
    
        # Actualizar los marcadores con los nuevos valores
        fecha_marker.markdown(f"**Fecha:** {fecha}")
        t_evap_marker.info(f"Tª evaporación: **{t_evap} ºC**")
        t_cam_marker.info(f"Tª cámara: **{t_cam} ºC**")
        t_cond_marker.info(f"Tª condensación: **{t_cond} ºC**")
        t_ext_marker.info(f"Tª exterior: **{t_ext} ºC**")
    

    #Creación de las dos columnas
    col1, col2 = st.columns(2)



    #Tabla datos
    with col1:
        st.write(df2[['t_evap','t_cam','t_cond','t_ext','temp','t_air_ee','t_air_se']])
               
    

    # Monitor 1
    with col2:
        df3 = df2.sort_index(ascending=True).copy()
        fig, ax = plt.subplots(figsize=(8, 4))
        df3[['t_air_ee','t_air_se','t_evap','t_cond']].plot(ax=ax, fontsize=10)
        ax.set_ylabel('T (ºC)', fontsize=10)
        ax.set_xlabel('Fecha', fontsize=10)
        ax.set_title('Monitor variables', fontsize=10)
        ax.tick_params(axis='x', rotation=45)  # Rotar etiquetas de fecha en el eje x
        fig.set_size_inches(8, 4)
        st.pyplot(fig, use_column_width=True)
         
   
    # Esperar 5 segundos antes de la siguiente actualización
    time.sleep(5)
    
    st.experimental_rerun()

if __name__ == '__main__':
    main()

    


