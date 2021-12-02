
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
import datetime

#clasificacion de escenarios del indice 
def clas_esc(df_indice):
    # clasificación de escenarios: A, B, C, D
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
    # tipo: compra o venta 
    df_indice['Operacion']= ''
    for i in range(len(df_indice)):
        if df_indice.Escenario[i] == 'A' or df_indice.Escenario[i] == 'B':
            df_indice.Operacion[i] = 'Sell'
        else:
            df_indice.Operacion[i] = 'Buy'  

    return df_indice.drop(['index'], axis=1)
    


df_indice = d.indice
df_divisas = d.EUR_AUD

def get_metricas(df_index, df_divisas):
    '''
    calcular las siguientes 4 métricas cada que sucede uno de los escenarios: 
    1.- (Dirección) Signo*(Close (t_30) - Open(t_0))
    2.- (Pips Alcistas) High(t_0 : t_30) – Open(t_0) 
    3.- (Pips Bajistas) Open(t_0) – Low(t_0 : t_30) 
    4.- (Volatilidad) High(t_-30 : t_30) ,  - mínimo low (t_-30:t_30) 
    '''
    fechas = []
    actual = []
    prevision = []
    anterior = [] 
    escenario = []
    direccion = []
    pip_alcista = []
    pip_bajista = []
    volatilidad = []
    for i in range(len(df_divisas)):
        for j in range(len(df_index)):
            if df_index['DateTime'][j]==df_divisas.time[i]:
                fechas.append(df_index.DateTime[j])
                actual.append(df_index.Actual[j])
                prevision.append(df_index.Consensus[j])
                anterior.append(df_index.Previous[j])
                escenario.append(df_index.Escenario[j])
                # dirección 
                if df_index['Operacion'][j] == 'Sell':
                    direccion.append(-1)

                elif df_index['Operacion'][j] == 'Buy':
                    direccion.append(1)
                # pips Alcistas
                pip_alcista.append(abs(np.round((df_divisas.high[i-15]-df_divisas.high[i+15])-df_divisas.open[i-15])))
                # pips Bajistas
                pip_bajista.append(abs(np.round((df_divisas.open[i-15]-df_divisas.low[i+15])*1000)))
                # volatilidad 
                volatilidad.append(np.round(abs((df_divisas.high[i-15]- df_divisas.high[i+15])-(df_divisas.low[i-15]- df_divisas.low[i+15]))*10000))  
    return fechas, escenario, direccion, pip_bajista, pip_alcista, volatilidad
    

def escenarios(fechas, escenario, direccion, pip_alcista,pip_bajista, volatilidad):
    df = pd.DataFrame()
    df['TimeStamp'] = fechas
    df['escenario'] = escenario
    df['direccion'] = direccion
    df['pip_alcista'] = pip_alcista
    df['pip_bajista'] = pip_bajista
    df['volatilidad'] = volatilidad

    return df

def entrenamiento(df):
    df_test = {}
    df_train = {}
    for i in range(len(df)):
        df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
        if df['TimeStamp'][i]  <= datetime.datetime(2019,2,1):
            df_train = df.iloc[:i+1,:]
        else:
            df_test = df.iloc[i:,:]
    return df_test,df_train


def decisiones(df):
    # nos aseguramos del tipo 
    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
    # tomamos solo el rango de fechas 
    df2 = df.loc[df["TimeStamp"].between('2019-02-1', '2020-02-1')]
    df_decisiones = pd.DataFrame()
    df_decisiones['escenario'] = df2.escenario
    operacion = []
    for i in range(len(df2)):
        if df.direccion[i] > 0:
            operacion.append('Buy')
        else:
            operacion.append('Sell')
    tiempo = df2['TimeStamp']
    df_decisiones['operacion'] = operacion
    df_decisiones['SL'] = 20
    df_decisiones['TP'] = 30 
    df_decisiones['volumen'] = 100   
    df_decisiones = df_decisiones.reset_index()
    return df_decisiones.drop(['index'], axis=1), tiempo



def backtest(df_decisiones,divisa, tiempo):
    capital = 100000
    df_backtest = pd.DataFrame()
    df_backtest['DateTime'] = tiempo
    a = list(df_decisiones.escenario)
    df_backtest['escenario'] = a
    a = list(df_decisiones.operacion)
    df_backtest['operacion'] = a
    df_backtest['volumen'] = 1000
    df_backtest = df_backtest.reset_index()
    df_backtest = df_backtest.drop(['index'], axis=1)

    resultado = []
    pips = []
    pips1 = 0.0001
    pips3 = 0
    cont_capital = []
    capital_acum = []
    TP = .2
    SL = 0.2
    for i in range(len(divisa)):
        for j in range(len(df_backtest)):
            if divisa.time[i] == df_backtest.DateTime[j]:
                if df_backtest.operacion[j] == 'Buy':
                    for k in range(len(divisa)):
                        
                        if divisa.close[i] + TP <= divisa.close[k]:
                            resultado.append('ganada')
                            pips2=pips1*df_backtest.volumen[j]
                            pips3 = pips3+pips2
                            pips.append(pips3)

                            lana =(pips1/divisa.close[k])*100
                            cont_capital.append(lana)
                            lana_acum = capital+lana
                            capital_acum.append(lana_acum)
                        else:
                        #elif divisa.close[i] - SL >= divisa.close[k]:
                            resultado.append('perdida')
                            pips2=(pips1*df_backtest.volumen[j]) * -1
                            pips3 = pips3+pips2
                            pips.append(pips3)

                            lana =((pips1/divisa.close[k])*100) * -1
                            cont_capital.append(lana)
                            lana_acum = capital+lana
                            capital_acum.append(lana_acum)
                        break 
                else:
                    for k in range(len(divisa)):
                        if divisa.close[i] - TP <= divisa.close[k]:
                            resultado.append('ganada')
                            pips2=pips1*df_backtest.volumen[j]
                            pips3 = pips3+pips2
                            pips.append(pips3)

                            lana =(pips1/divisa.close[k])*100
                            cont_capital.append(lana)
                            lana_acum = capital+lana
                            capital_acum.append(lana_acum)

                        elif divisa.close[i] + SL >= divisa.close[k]:
                            resultado.append('perdida')
                            pips2=(pips1*df_backtest.volumen[j]) * -1
                            pips3 = pips3+pips2
                            pips.append(pips3)

                            lana =((pips1/divisa.close[k])*100) * -1
                            cont_capital.append(lana)
                            lana_acum = capital+lana
                            capital_acum.append(lana_acum)
                        break
    df_backtest['resultado'] = resultado
    df_backtest['pips'] = pips
    df_backtest['capital'] = cont_capital
    df_backtest['capital_acm'] = capital_acum

    return df_backtest
