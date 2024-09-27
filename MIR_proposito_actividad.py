# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:39:52 2024

@author: Carlos Ernesto Custodio Cadena

Actualización de los valores reportados a MIR en la proyecciòn inicial 
Indicadores Propósito (Eficiencia terminal anual) y Actividad 1.1 (atención a la demanda anual)
Los ciclos que se consideran son los del año en análisis ejemplos: 
    Para 2024 en el propósito son los ciclos de las cohortes que egresan en 202401, 202402 y 202403
    Para 2024 en la actividad 1.1 los ciclos que se considean para el año 2024 son los NI de 202401, 202402 y 202403
"""

import pandas as pd
# Se obtienen los datos de los ciclos de interés periodo actual y periodo anterior
dproposito = pd.read_csv('eficiencia_anual_2024.csv', encoding = 'unicode escape')
dactividad1_1 = pd.read_csv('atencion_a_la_demanda_2024.csv', encoding = 'unicode escape')
# se pivotean los datos para obtener las sumatorias de los datos y calcular los índices
# se contabiliza cuantos de los miembros del cohorte han egresado a la fecha y se cálculo el índice al momento.
iproposito = dproposito.pivot_table(values = 'MATRICULA',
                                    index = ['ANIO'],
                                    columns = ['EGRESADO'],
                                    fill_value =0,
                                    aggfunc = 'count')
iproposito['TOTAL'] = iproposito['NO']+iproposito['SI']
iproposito['INDICE'] = round(iproposito['SI']/iproposito['TOTAL']*100,2)


# se contabiliza cuantos de los solicitantes fueron aceptados y se cálculo el índice al momento.
# se debe seleccionar el año de interés y si se quiere calcular los dos hacerlo por separado (podrìa implementarse un ciclo por año)
dactividad1_1 = dactividad1_1[dactividad1_1['ESTATUS']!='PRE-REGISTRO']
dactividad1_1 = dactividad1_1[dactividad1_1['ANIO']==2024]
iactividad1_1 = dactividad1_1.pivot_table(values = 'MATRICULA',
                                    index = ['TRIMESTRE'],
                                    columns = ['ESTATUS'],
                                    fill_value =0,
                                    aggfunc = 'count')
iactividad1_1['TOTAL'] = iactividad1_1['PENDIENTE']+iactividad1_1['ACEPTADO']
iactividad1_1['INDICE'] = round(iactividad1_1['TOTAL']/iactividad1_1['TOTAL'].sum()*100,2)
# se guardan los cálculos en un archivo xlsx
archivo = pd.ExcelWriter('indicadores_mir.xlsx')
iproposito.to_excel(archivo, sheet_name = 'proposito')
iactividad1_1.to_excel(archivo, sheet_name = 'actividad_1_1')
archivo.close()