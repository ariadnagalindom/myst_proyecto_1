
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Proyecto Final (Analisis Fundamental)                                                       -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/ariadnagalindom/myst_proyecto_1                                                                   -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# importamos 
import importlib 
import data as d
import pandas as pd

# importlib.reload(d)

# índicador 
# print(d.indice)
# divisa
# print(d.USD_MXN)
# reglas escenarios
escenarios = {'Escenario': ['A','B','C','D'],'Regla':['Actual>=Consensus>=Previous','Actual>=Consensus<Previous','Actual<Consensus>=Previous','Actual<Consensus<Previous']}
escenarios = pd.DataFrame(escenarios)
