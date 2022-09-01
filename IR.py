# -*- coding: utf-8 -*-
"""
Autor: Carlos Ernesto Custodio Cadena
Área: Estadísticas
Fecha: 30/08/2022
Hora: 12:53
Objetivo: Analizar las calificaciones de los alumnos para detectar aquellas asignaturas con mayores indices de reprobación por programa educativo.
Se toma en consideración el procentaje de alumnos reprobados por grupo.
"""
#  importar las librerias necesarias
import pandas as pd
import numpy as np
#  leer el archivo csv con los datos, codificación UNICODE y colocarlo en un DataFrame
calificaciones = pd.read_csv("calificaciones.csv", encoding = "unicode escape")
#  Eliminar los valores NaN del Dataframe y Colocar "N/A" como valor
#  En este caso hablamos de grupos que no tienen asignado salón
calificaciones.fillna("N/A", inplace = True)
#  Ordenar el DataFrame
calificaciones.sort_values(["CICLO", "MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "TURNO", "SEMESTRE", "CLAVE", "GRUPO", "DOCENTE", "MATRICULA"], inplace = True)
#  Comparar las columnas CALIF y MINIMO y determinar el estatus del alumno (Aprobado o Reprobado)
condiciones = [calificaciones["CALIF"]>calificaciones["MINIMO"],               calificaciones["CALIF"]==calificaciones["MINIMO"],               calificaciones["CALIF"]<calificaciones["MINIMO"]]
opciones = ["Aprobado","Aprobado","Reprobado"]
calificaciones["ESTATUS"] = np.select(condiciones,opciones)
#  Agrupar los datos por programa educativo, semestre, grupo contando los aprobados y los reprobados y calcular el índice de reprobación (alumnos reprobados )
indice_reprobacion = pd.pivot_table(calificaciones, values="MATRICULA",index=["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC","SEMESTRE","GRUPO","CLAVE","NOMBRE_MATERIA","DOCENTE","NOMBRE_PROFESOR","TURNO"],columns=["ESTATUS"], aggfunc="count", fill_value=0)
condiciones = [indice_reprobacion["Aprobado"]==0,indice_reprobacion["Aprobado"]>0]
opciones = [100.00,round((indice_reprobacion["Reprobado"]/(indice_reprobacion["Aprobado"]+indice_reprobacion["Reprobado"])*100),2)]
indice_reprobacion["Indice"] = np.select(condiciones, opciones)
indice_reprobacion.sort_values(["PROG_EDUC","SEMESTRE","GRUPO","CLAVE","TURNO"])
#..GENERAR ARCHIVO DE EXCEL CON LOS DATOS OBTENIDOS, SE INCLUYE DATOS FUENTE Y DATOS PROCESADOS
archivo = pd.ExcelWriter("indice_reprobacion_202201Sy202202C.xlsx")
indice_reprobacion.to_excel(archivo, sheet_name="indice_reprobacion")
calificaciones.to_excel(archivo, sheet_name="alumnos")
archivo.save()
