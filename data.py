
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

# leer índice económico
indice = pd.read_csv(r'C:\Users\ariad\OneDrive\Documentos\GitHub\myst_proyecto_1\files\API Weekly Crude Oil Stock - United States.txt')
# Consensus y Revised estan vacias 
indice.Previous.isna().sum() #solo tenemos el último valor de Previous vacio 
# Si un renglón no tiene "Previous", asígnale el "Actual" del renglón anterior.
indice.Previous.iloc[-1] = indice.Actual.iloc[-1]
# Si un renglón no tiene "Consensus", asígnale el "Previous" del mismo renglón. (arreglamos eso)
indice.Consensus = indice.Previous
indice = indice.drop('Revised',axis=1)

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



