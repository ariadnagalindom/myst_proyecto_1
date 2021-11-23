
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Proyecto Final (Analisis Fundamental)                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: ariadnagalindom                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/ariadnagalindom/myst_proyecto_1                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import MetaTrader5 as mt
import pytz

# leer índice económico
indice = pd.read_csv(r'C:\Users\ariad\OneDrive\Documentos\GitHub\myst_proyecto_1\files\API Weekly Crude Oil Stock - United States.txt')
# Consensus y Revised estan vacias 
indice.Previous.isna().sum() #solo tenemos el último valor de Previous vacio 
# Si un renglón no tiene "Previous", asígnale el "Actual" del renglón anterior.
indice.Previous.iloc[-1] = indice.Actual.iloc[-1]
# Si un renglón no tiene "Consensus", asígnale el "Previous" del mismo renglón. (arreglamos eso)
indice.Consensus = indice.Previous
indice = indice.drop('Revised',axis=1)
#indice = indice.sort_values('DateTime')

# Quitamos los valores de los años anteriores a lo que necesitamos 
df_index = {}
for i in range(len(indice)):
    indice.DateTime = pd.to_datetime(indice.DateTime)
    if indice.DateTime[i]  >= datetime.datetime(2019,1,1):
        df_index = indice.iloc[:i+1,:]
# extraemos y renombramos 
indice = df_index

# descargamos un par de divisas relacionadas de los últimos dos años 
# date_format = "%Y-%m-%d"
# start =datetime.datetime.strptime('2018-11-01', date_format).date()
# end = datetime.datetime.today().date()
# USD_GBP = yf.download('USDGBP=X', start=start, end=end, interval='1d') #solo se puede una semana 

# generamos lista cada 7 dias en intervalo de tiempo
#d = start
#step = datetime.timedelta(days=6)
#dict = []
#while d < end:
#    dict.append(d.strftime(date_format))
#    d += step
# descargamos por cada step de tiempo     
#USD_GBP = pd.DataFrame()
#for i in range(len(dict)-1):
#    temp = yf.download('USDGBP=X', start= dict[i], end= dict[i+1], interval='1m') #marca error si es más alejado de 30 dias
#    temp = pd.DataFrame(temp)
#    USD_GBP.append(temp)

# USD_GBP = pd.DataFrame(USD_GBP)

# Cargamos divisas 
EUR_AUD_2019 = pd.read_csv(r'C:\Users\ariad\OneDrive\Documentos\GitHub\myst_proyecto_1\files\EURAUD_M1_2019.csv')
EUR_AUD_2020 = pd.read_csv(r'C:\Users\ariad\OneDrive\Documentos\GitHub\myst_proyecto_1\files\EURAUD_M1_2020.csv')
EUR_AUD_2021 = pd.read_csv(r'C:\Users\ariad\OneDrive\Documentos\GitHub\myst_proyecto_1\files\EURAUD_M1_2021.csv')

EUR_AUD = EUR_AUD_2019.append(EUR_AUD_2020)
EUR_AUD = EUR_AUD_2019.append(EUR_AUD_2021)

def historico(ticker, date_from, date_to):
#del archivo donde estan los datos de inicio de sesión
    param_archivo = pd.read_csv(r'C:\Users\ariad\OneDrive\Documentos\GitHub\myst_proyecto_1\files\cuentas.csv')
    Names = list(param_archivo['Name'])
    Users = list(param_archivo['Account'])
    Passwords = list(param_archivo['Password'])
    
    #iniciar conexión con MT5
    mt.initialize(login=Users[0], server='FxPro-MT5',password=Passwords[0])
    # obtenemos las barras 
    rates = mt.copy_rates_range(ticker, mt.TIMEFRAME_M1, date_from, date_to)  
    # finalizamos la conexión 
    # mt.shutdown()
    # creamos un DataFrame de los datos obtenidos
    rates_frame = pd.DataFrame(rates)
    # convertimos la hora en segundos al formato datetime
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame

# divisa = historico('EURUSD', datetime.datetime(2020,1,1), datetime.datetime(2020,1,2))

# rates = mt.copy_rates_range('EURUSD', mt.TIMEFRAME_M1, datetime.datetime(2020,1,1), datetime.datetime(2020,1,2)) 
