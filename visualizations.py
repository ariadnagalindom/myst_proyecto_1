
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Proyecto Final (Analisis Fundamental)                                                       -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/ariadnagalindom/myst_proyecto_1                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def linea(df_index):
    fig = px.line(df_index, x='DateTime', y='Actual')
    return fig.show()

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
# A y AP
def autocorr(df_index):
    A = plot_acf(df_index.Actual)
    AP = plot_pacf(df_index.Actual)
    return A, AP

import statsmodels.api as sm
import data as d
# prueba heterocedasticidad
def hetero(df_index):
    fig, ax = plt.subplots(1,1, figsize=[12,6])
    a = sm.qqplot(df_index.Actual, line= 'q', fit  = True, ax = ax)

from scipy import stats
# Normalidad
def normalidad(df_index):
    print('Kursotis:', stats.kurtosis(df_index.Actual))
    print('Skewness:', stats.skew(df_index.Actual))
    print('Shapiro-Wilk: ', stats.shapiro(df_index.Actual)) # no más de 50 datos 
    print('D Agostino:', stats.normaltest(df_index.Actual))

from pylab import rcParams

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

def estacion(df_index):
    # Estacionalidad 
    rcParams['figure.figsize'] = 16, 6
    decomposition = sm.tsa.seasonal_decompose(df_index.Actual, model='additive', period=12)
    decomposition.plot()
    ## Test de DICKEY-FULLER para Estacionariedad
    df_test = adfuller(df_index.Actual)
    if df_test[1] > 0.05:
        test= print('No hay evidencia de estacionariedad')
    else:
        test= print('Hay evidencia de estacionariedad')

    return print((test,df_test[1])) ,plt.show()

# Datos Atípicos 
import seaborn as sns
def atipicos(df_index):
    ax = sns.boxplot(x='Actual', data=df_index)