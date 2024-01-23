# -*- coding: utf-8 -*-
"""
Creado el 01 de enero de 2023 10:38 horas
Modificado el 03 de enero de 2024 12:13 horas

@author: Carlos Ernesto Custodio Cadena
"""

import pandas as pd

datos = pd.read_csv("eficiencia_2023.csv", encoding = "unicode_escape")
datostotales = datos.groupby(["PROG_EDUC","COHORTE","EGRESADO"])["MATRICULA"].aggregate("count")
datostotales = pd.DataFrame(datostotales)
datostotales = datostotales.reset_index()
eficiencia = datostotales.pivot_table(values = "MATRICULA", index = ["PROG_EDUC","COHORTE"], columns = ["EGRESADO"], fill_value = 0).sort_values(by = ["COHORTE","PROG_EDUC"], ascending = [True, True])
#  Indice de egreso: cuantos de los inscritos de 201902S a 202301S y de 201903C a 202302C terminaron
eficiencia[("INDICE")]=round(((eficiencia[("SI")])/(eficiencia[("NO")] + eficiencia[("SI")]))*100,2)
#  crear archivo Excel con los resultados del análisis
archivo = pd.ExcelWriter("eficiencia2023.xlsx")
eficiencia.to_excel(archivo, sheet_name = "eficiencia")
datos.to_excel(archivo, sheet_name = "datos")
archivo.close()