
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Proyecto Final (Analisis Fundamental)                                                       -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/ariadnagalindom/myst_proyecto_1                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
from pandas.core.indexes.base import Index
import data as d 
import pandas as pd 
import numpy as np 


#clasificacion de escenarios del indice 
def clas_esc(df_indice):
    df_indice['Escenario'] = ''
    for i in range(len(df_indice)):
        if df_indice.Actual[i] >= df_indice.Consensus[i] and df_indice.Consensus[i] >= df_indice.Previous[i]:
            df_indice.Escenario.iloc[i] = 'A'
        elif df_indice.Actual[i] >= df_indice.Consensus[i] and df_indice.Consensus[i] < df_indice.Previous[i]:
            df_indice.Escenario.iloc[i] = 'B'
        elif df_indice.Actual[i] < df_indice.Consensus[i] and df_indice.Consensus[i] >= df_indice.Previous[i]:
            df_indice.Escenario.iloc[i] = 'C'
        elif df_indice.Actual[i] < df_indice.Consensus[i] and df_indice.Consensus[i] < df_indice.Previous[i]:
            df_indice.Escenario.iloc[i] = 'D'
        
    return df_indice

df_indice = d.indice
df_divisas = d.USD_GBP

def get_metricas(df_indice, df_divisas):
    '''
    calcular las siguientes 4 métricas cada que sucede uno de los escenarios: 
    1.- (Dirección) Signo*(Close (t_30) - Open(t_0))
    2.- (Pips Alcistas) High(t_0 : t_30) – Open(t_0) 
    3.- (Pips Bajistas) Open(t_0) – Low(t_0 : t_30) 
    4.- (Volatilidad) High(t_-30 : t_30) ,  - mínimo low (t_-30:t_30) 
    '''
    tiempo = pd.Timedelta('30min') #seccionamos el tiempo
    # aseguramos el tipo de datos sea datetime
    df_divisas.index = pd.to_datetime(df_divisas.index)
    df_indice.DateTime = pd.to_datetime(df_indice.DateTime)
    # ordenamos las fechas del indice 
    df_indice = df_indice.sort_values('DateTime')


    

