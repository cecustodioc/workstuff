# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:51:05 2023

@author: Carlos Ernesto Custodio Cadena
Informe DGESUI

"""
import pandas as pd
origen = "dato/"
destino = "DGESUI/"
nombre = "DGESUI_20233T"
matricula = pd.read_csv(origen+'inscrito.csv', encoding = 'unicode escape')
matricula = matricula[matricula['MATRICULADE']=='CIERRE']
#  Se crea el consolidado de la información
consolidado = matricula.groupby(['NIVEL','T_INS'])['MATRICULA'].aggregate('count')
consolidado = pd.DataFrame(consolidado)
consolidado = consolidado.pivot_table(values='MATRICULA', index = ['NIVEL'], columns = ['T_INS'], fill_value = 0).sort_values(by = ['NIVEL'], ascending = [True])
consolidado['TOT']=consolidado['NI']+consolidado['RI']
#  Se crea el detalle de la matrícula
detalle = matricula.groupby(['NIVEL','PROG_EDUC','MODALIDAD','T_INS'])['MATRICULA'].aggregate('count')
detalle = pd.DataFrame(detalle)
detalle = detalle.pivot_table(values='MATRICULA', index = ['NIVEL','PROG_EDUC','MODALIDAD'], columns = ['T_INS'], fill_value = 0).sort_values(by = ['NIVEL','MODALIDAD','PROG_EDUC'], ascending = [True, False, True])
detalle['TOT'] = detalle['NI'] + detalle['RI']
#  Crear el archivo de xlsx propio del informe
archivo = pd.ExcelWriter(destino + nombre + ".xlsx")
consolidado.to_excel(archivo,sheet_name = 'consolidado')
detalle.to_excel(archivo,sheet_name = 'detalle')
matricula.to_excel(archivo,sheet_name = 'matricula')
archivo.close()