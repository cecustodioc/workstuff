# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:46:24 2023

@author: Carlos Ernesto Custodio Cadena

Este script toma la información de los alumnos inscritos y los clasisifca por 
municipio de nacimiento o municipio de procedencia del bachiller
"""

import pandas as pd
import numpy as np
datos = pd.read_csv('inscrito.csv', encoding = 'unicode escape')
datos = datos[datos['MATRICULADE']=='CIERRE']
datos = datos.drop(['MATRICULADE'], axis = 1)
nacimiento = pd.read_csv('inscrito.csv', encoding = 'unicode escape')
nacimiento = nacimiento[nacimiento['MATRICULADE']=='CIERRE']
nacimiento['EDO_NAC'] = np.where(nacimiento['EDO_NAC']!='TABASCO','OTRO ESTADO','TABASCO')
nacimiento = nacimiento.pivot_table(values = 'MATRICULA',
                  index = ['SISTEMA','NIVEL','PROG_EDUC'],
                  columns = ['EDO_NAC','MUN_NAC','SEXO'],
                  fill_value = 0, aggfunc = 'count')
procedencia = pd.read_csv('inscrito.csv', encoding = 'unicode escape')
procedencia = procedencia[procedencia['MATRICULADE']=='CIERRE']
procedencia['EDO_PROC'] = np.where(procedencia['EDO_PROC']!='TABASCO','OTRO ESTADO','TABASCO')
procedencia = procedencia.pivot_table(values = 'MATRICULA',
                  index = ['SISTEMA','NIVEL','PROG_EDUC'],
                  columns = ['EDO_PROC','MUN_PROC','SEXO'],
                  fill_value = 0, aggfunc = 'count')
archivo = pd.ExcelWriter('mun_nac_proc_sexo.xlsx')
nacimiento.to_excel(archivo,'lugar de nacimiento')
procedencia.to_excel(archivo,'procedencia bachiller')
datos.to_excel(archivo,'padrón')
archivo.close()