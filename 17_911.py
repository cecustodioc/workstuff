# -*- coding: utf-8 -*-
"""
Creado 05/09/2022 09:16
@author: Carlos Ernesto Custodio Cadena
Cálcular los indicadores escolares tomando como entrada archivos csv
Última revisión: 14/11/2023
"""
#  Se importan las librerias que nos permitiran manipular los datos de los archivos csv
import pandas as pd
#  import numpy as np
#  Se crean los DataFrames con los datos de las consultas SQL guardadas en archivos csv
dadmision = pd.read_csv("dato/admision.csv", encoding = "unicode escape", index_col = False)
dadmision = dadmision[dadmision['ESTATUS'] == 'ACEPTADO']
dadmisionanual = pd.read_csv("dato/admisionanual.csv", encoding = "unicode escape", index_col = False)
ddatocarrera = pd.read_csv("dato/datocarrera.csv", encoding="unicode escape", index_col = False)
degresadoanual = pd.read_csv("dato/egresadoanual.csv", encoding="unicode escape", index_col = False)
dinscrito = pd.read_csv("dato/inscrito.csv", encoding = "unicode escape", index_col = False)
dinscrito = dinscrito[dinscrito['MATRICULADE']=='CIERRE']
dtituladoanual = pd.read_csv("dato/tituladoanual.csv", encoding="unicode escape", index_col = False)

#  Solo los PE con matrícula vigente matrícula
carreras = dinscrito["PROG_EDUC"].drop_duplicates()
#..Datos de las carreras con alumnos inscritos para el informe 911
datocarrera = ddatocarrera
#  Admision anual
admisionanual = dadmisionanual
admisionanual = admisionanual[admisionanual["ESTATUS"] == "ACEPTADO"]
admisionanual = admisionanual.pivot_table(values = "MATRICULA", index=["PROG_EDUC"], columns = ["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(admisionanual)>1:
    admisionanual["TOTAL"] = admisionanual["F"] + admisionanual["M"]
#  Egresado anual
egresadoanual = degresadoanual
egresadoanual = egresadoanual.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(egresadoanual)>1:
    egresadoanual["TOTAL"] = egresadoanual["F"] + egresadoanual["M"]
#  Egresados discapacidad
egresadodiscapacidad = degresadoanual[degresadoanual["DISCAPACIDAD"]!="NINGUNA"]
egresadodiscapacidad = egresadodiscapacidad.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(egresadodiscapacidad)>1:
    egresadodiscapacidad["TOTALD"] = egresadodiscapacidad["F"] + egresadodiscapacidad["M"]
#  Egresados indigenas
egresadoindigena = degresadoanual[degresadoanual["ETNIA"]!="NINGUNA"]
egresadoindigena = egresadoindigena.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(egresadoindigena)>1:
    egresadoindigena["TOTALI"] = egresadoindigena["F"] + egresadoindigena["M"]
#  Egresados por edades
egresadoanualedad = degresadoanual
egresadoanualedad = egresadoanualedad.pivot_table(values = "MATRICULA", index =  ["PROG_EDUC", "EDAD"], columns = ["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(egresadoanualedad)>1:
    egresadoanualedad["TOTAL"] = egresadoanualedad["F"] + egresadoanualedad["M"]
#  Titulado anual
tituladoanual = dtituladoanual[dtituladoanual["PROG_EDUC"].isin(carreras)]
tituladoanual = tituladoanual.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns = ["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(tituladoanual)>1:
    tituladoanual["TOTAL"] = tituladoanual["F"] + tituladoanual["M"]
#  Titulados discapacidad
tituladodiscapacidad = dtituladoanual[dtituladoanual["DISCAPACIDAD"]!="NINGUNA"]
tituladodiscapacidad = tituladodiscapacidad.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(tituladodiscapacidad)>1:
    tituladodiscapacidad["TOTALD"] = tituladodiscapacidad["F"] + tituladodiscapacidad["M"]
#  Titulados indigenas
tituladoindigena = dtituladoanual[dtituladoanual["ETNIA"]!="NINGUNA"]
tituladoindigena = tituladoindigena.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(tituladoindigena)>1:
    tituladoindigena["TOTALI"] = tituladoindigena["F"] + tituladoindigena["M"]
#  Titulados por edades
tituladoanualedad = dtituladoanual[dtituladoanual["PROG_EDUC"].isin(carreras)]
tituladoanualedad = tituladoanualedad.pivot_table(values = "MATRICULA", index = ["PROG_EDUC","EDAD"], columns = ["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(tituladoanualedad)>1:
    tituladoanualedad["TOTAL"] = tituladoanualedad["F"] + tituladoanualedad["M"]
#  Primer ingreso (ADMISION - Lugares Ofertados)
#  Datos de admision alumnos ACEPTADOS por PE ciclo actual
#  Lugares ofertados
admisioncicloactual = dadmision
admisioncicloactual = admisioncicloactual.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(admisioncicloactual)>1:
    admisioncicloactual["TOTAL"] = admisioncicloactual["F"] + admisioncicloactual["M"]
#  Admision discapacidad
admisiondiscapacidad = dadmision[dadmision["DISCAPACIDAD"]!="NINGUNA"]
admisiondiscapacidad = admisiondiscapacidad.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(admisiondiscapacidad)>1:
    admisiondiscapacidad["TOTALD"] = admisiondiscapacidad["F"] + admisiondiscapacidad["M"]
#  Admision indigenas
admisionindigena = dadmision[dadmision["ETNIA"]!="NINGUNA"]
admisionindigena = admisionindigena.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(admisionindigena)>1:
    admisionindigena["TOTALI"] = admisionindigena["F"] + admisionindigena["M"]
#  Primer ingreso (INSCRITOS)
#  Inscrito
inscritocicloactual = dinscrito[dinscrito["T_INS"]=="NI"]
inscritocicloactual = inscritocicloactual.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(inscritocicloactual)>1:
    inscritocicloactual["TOTAL"] = inscritocicloactual["F"] + inscritocicloactual["M"]
#  Inscrito discapacidad
inscritodiscapacidad = dinscrito[dinscrito["T_INS"]=="NI"]
inscritodiscapacidad = inscritodiscapacidad[inscritodiscapacidad["DISCAPACIDAD"]!="NINGUNA"]
inscritodiscapacidad = inscritodiscapacidad.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(inscritodiscapacidad)>1:
    inscritodiscapacidad["TOTALD"] = inscritodiscapacidad["F"] + inscritodiscapacidad["M"]
#  Inscrito indigenas
inscritoindigena = dinscrito[dinscrito["T_INS"]=="NI"]
inscritoindigena = inscritoindigena[inscritoindigena["ETNIA"]!="NINGUNA"]
inscritoindigena = inscritoindigena.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(inscritoindigena)>1:
    inscritoindigena["TOTALI"] = inscritoindigena["F"] + inscritoindigena["M"]
#  Inscritos por nacimiento (Estado)
inscritoestado = dinscrito[dinscrito["T_INS"]=="NI"]
inscritoestado = inscritoestado.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "EDO_NAC"], columns =["SEXO"], aggfunc = "count", fill_value=0, sort = True)
if len(inscritoestado)>1:
    inscritoestado["TOTALE"] = inscritoestado["F"] + inscritoestado["M"]
#  Inscritos por procedencia (Bachiller)
inscritobachiller = dinscrito[dinscrito["T_INS"]=="NI"]
inscritobachiller = inscritobachiller.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "EDO_PROC"], columns =["SEXO"], aggfunc = "count", fill_value=0, sort = True)
if len(inscritobachiller)>1:
    inscritobachiller["TOTALE"] = inscritobachiller["F"] + inscritobachiller["M"]
#  Matrícula total
#  InscritoGrado
matriculacicloactual = dinscrito
matriculacicloactual = matriculacicloactual.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "GRADO"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(matriculacicloactual)>1:
    matriculacicloactual["TOTAL"] = matriculacicloactual["F"] + matriculacicloactual["M"]
#  Inscrito discapacidad
matriculadiscapacidad = dinscrito
matriculadiscapacidad = matriculadiscapacidad[matriculadiscapacidad["DISCAPACIDAD"]!="NINGUNA"]
matriculadiscapacidad = matriculadiscapacidad.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "GRADO"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(matriculadiscapacidad)>1:
    matriculadiscapacidad["TOTALD"] = matriculadiscapacidad["F"] + matriculadiscapacidad["M"]
#  Inscrito indigenas
matriculaindigena = dinscrito
matriculaindigena = matriculaindigena[matriculaindigena["ETNIA"]!="NINGUNA"]
matriculaindigena = matriculaindigena.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "GRADO"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(matriculaindigena)>1:
    matriculaindigena["TOTALI"] = matriculaindigena["F"] + matriculaindigena["M"]
#  Inscritos por nacimiento y grado (Estado)
matriculagradonacimiento = dinscrito
matriculagradonacimiento = matriculagradonacimiento.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "GRADO","EDO_NAC"], columns =["SEXO"], aggfunc = "count", fill_value=0, sort = True)
if len(matriculagradonacimiento)>1:
    matriculagradonacimiento["TOTALNG"] = matriculagradonacimiento["F"] + matriculagradonacimiento["M"]
#  Inscritos por nacimiento (Estado)
matriculanacimiento = dinscrito
matriculanacimiento = matriculanacimiento.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "EDO_NAC"], columns =["SEXO"], aggfunc = "count", fill_value=0, sort = True)
if len(matriculanacimiento)>1:
    matriculanacimiento["TOTALE"] = matriculanacimiento["F"] + matriculanacimiento["M"]
#  Inscritos por procedencia (Bachiller)
matriculaprocedencia = dinscrito
matriculaprocedencia = matriculaprocedencia.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "EDO_PROC"], columns =["SEXO"], aggfunc = "count", fill_value=0, sort = True)
if len(matriculaprocedencia)>1:
    matriculaprocedencia["TOTALP"] = matriculaprocedencia["F"] + matriculaprocedencia["M"]
#  Sexo, edad, grado (matricula total)
matriculaedadgradosexo = dinscrito
matriculaedadgradosexo = matriculaedadgradosexo.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "EDAD"], columns =["T_INS", "GRADO", "SEXO"], aggfunc = "count", fill_value=0, sort = True)
# Detalle discapacidad
matriculadiscapacidaddetalle = dinscrito
matriculadiscapacidaddetalle = matriculadiscapacidaddetalle[matriculadiscapacidaddetalle["DISCAPACIDAD"]!="NINGUNA"]
matriculadiscapacidaddetalle = matriculadiscapacidaddetalle.pivot_table(values = "MATRICULA", index = ["PROG_EDUC", "DISCAPACIDAD"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(matriculadiscapacidaddetalle)>1:
    matriculadiscapacidaddetalle["TOTALDD"] = matriculadiscapacidaddetalle["F"] + matriculadiscapacidaddetalle["M"]
#  Inscrito indigenas totales
matriculaindigenatotal = dinscrito
matriculaindigenatotal = matriculaindigenatotal[matriculaindigenatotal["ETNIA"]!="NINGUNA"]
matriculaindigenatotal = matriculaindigenatotal.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(matriculaindigenatotal)>1:
    matriculaindigenatotal["TOTALIT"] = matriculaindigenatotal["F"] + matriculaindigenatotal["M"]
#  Inscrito indigenas totales con discapacidad
matriculaindigenatotaldiscapacidad = dinscrito
matriculaindigenatotaldiscapacidad = matriculaindigenatotaldiscapacidad[matriculaindigenatotaldiscapacidad["ETNIA"]!="NINGUNA"]
matriculaindigenatotaldiscapacidad = matriculaindigenatotaldiscapacidad[matriculaindigenatotaldiscapacidad["DISCAPACIDAD"]!="NINGUNA"]
matriculaindigenatotaldiscapacidad = matriculaindigenatotaldiscapacidad.pivot_table(values = "MATRICULA", index = ["PROG_EDUC"], columns=["SEXO"], aggfunc = "count", fill_value = 0, sort = [True])
if len(matriculaindigenatotaldiscapacidad)>1:
    matriculaindigenatotaldiscapacidad["TOTALITD"] = matriculaindigenatotaldiscapacidad["F"] + matriculaindigenatotaldiscapacidad["M"]
#  Resetear los indices para poder hacer selecciones
datocarrera.drop(columns=["PLAN","DIVISION"], inplace = True)
admisionanual.reset_index(inplace = True)
egresadoanual.reset_index(inplace = True)
egresadoindigena.reset_index(inplace = True)
egresadodiscapacidad.reset_index(inplace = True)
egresadoanualedad.reset_index(inplace = True)
tituladoanual.reset_index(inplace = True)
tituladodiscapacidad.reset_index(inplace = True)
tituladoindigena.reset_index(inplace = True)
tituladoanualedad.reset_index(inplace = True)
admisioncicloactual.reset_index(inplace = True)
admisiondiscapacidad.reset_index(inplace = True)
admisionindigena.reset_index(inplace = True)
inscritocicloactual.reset_index(inplace = True)
inscritodiscapacidad.reset_index(inplace = True)
inscritoindigena.reset_index(inplace = True)
inscritoestado.reset_index(inplace = True)
inscritobachiller.reset_index(inplace = True)
matriculacicloactual.reset_index(inplace = True)
matriculadiscapacidad.reset_index(inplace = True)
matriculaindigena.reset_index(inplace = True)
matriculagradonacimiento.reset_index(inplace = True)
matriculanacimiento.reset_index(inplace = True)
matriculaprocedencia.reset_index(inplace = True)
matriculaedadgradosexo.reset_index(inplace = True)
matriculadiscapacidaddetalle.reset_index(inplace = True)
matriculaindigenatotal.reset_index(inplace = True)
matriculaindigenatotaldiscapacidad.reset_index(inplace = True)
for d in carreras:
    #  Para armar cada xlsx ya obtenido todas las tablas de datos.
    datocarrera911 = datocarrera[datocarrera["PROG_EDUC"] == d]
    admisionanual911 = admisionanual[admisionanual["PROG_EDUC"] == d]
    egresadoanual911 = egresadoanual[egresadoanual["PROG_EDUC"] == d]
    egresadodiscapacidad911 = egresadodiscapacidad[egresadodiscapacidad["PROG_EDUC"] == d]
    egresadoindigena911 = egresadoindigena[egresadoindigena["PROG_EDUC"] == d]
    egresadoanualedad911 = egresadoanualedad[egresadoanualedad["PROG_EDUC"] == d]
    tituladoanual911 = tituladoanual[tituladoanual["PROG_EDUC"] == d]
    tituladodiscapacidad911 = tituladodiscapacidad[tituladodiscapacidad["PROG_EDUC"] == d]
    tituladoindigena911 = tituladoindigena[tituladoindigena["PROG_EDUC"] == d]
    tituladoanualedad911 = tituladoanualedad[tituladoanualedad["PROG_EDUC"] == d]
    admisioncicloactual911 = admisioncicloactual[admisioncicloactual["PROG_EDUC"] == d]
    admisiondiscapacidad911 = admisiondiscapacidad[admisiondiscapacidad["PROG_EDUC"] == d]
    admisionindigena911 = admisionindigena[admisionindigena["PROG_EDUC"] == d]
    inscritocicloactual911 = inscritocicloactual[inscritocicloactual["PROG_EDUC"] == d]
    inscritodiscapacidad911 = inscritodiscapacidad[inscritodiscapacidad["PROG_EDUC"] == d]
    inscritoindigena911 = inscritoindigena[inscritoindigena["PROG_EDUC"] == d]
    inscritoestado911 = inscritoestado[inscritoestado["PROG_EDUC"] == d]
    inscritobachiller911 = inscritobachiller[inscritobachiller["PROG_EDUC"] == d]
    matriculacicloactual911 = matriculacicloactual[matriculacicloactual["PROG_EDUC"] == d]
    matriculadiscapacidad911 = matriculadiscapacidad[matriculadiscapacidad["PROG_EDUC"] == d]
    matriculaindigena911 = matriculaindigena[matriculaindigena["PROG_EDUC"] == d]
    matriculagradonacimiento911 = matriculagradonacimiento[matriculagradonacimiento["PROG_EDUC"] == d]
    matriculanacimiento911 = matriculanacimiento[matriculanacimiento["PROG_EDUC"] == d]
    matriculaprocedencia911 = matriculaprocedencia[matriculaprocedencia["PROG_EDUC"] == d]
    matriculaedadgradosexo911 = matriculaedadgradosexo[matriculaedadgradosexo["PROG_EDUC"] == d]
    matriculadiscapacidaddetalle911 = matriculadiscapacidaddetalle[matriculadiscapacidaddetalle["PROG_EDUC"] == d]
    matriculaindigenatotal911 = matriculaindigenatotal[matriculaindigenatotal["PROG_EDUC"] == d]
    matriculaindigenatotaldiscapacidad911 = matriculaindigenatotaldiscapacidad[matriculaindigenatotaldiscapacidad["PROG_EDUC"] == d]
    #  Grabar el xlsx
    archivo = pd.ExcelWriter("911/" + d + ".xlsx")
    datocarrera911.to_excel(archivo, sheet_name = "1_2")
    admisionanual911.to_excel(archivo, sheet_name = "II_2")
    egresadoanual911.to_excel(archivo, sheet_name = "III_1")
    egresadodiscapacidad911.to_excel(archivo, sheet_name = "III_1a")
    egresadoindigena911.to_excel(archivo, sheet_name = "III_1b")
    tituladoanual911.to_excel(archivo, sheet_name = "III_2")
    tituladodiscapacidad911.to_excel(archivo, sheet_name = "III_2a")
    tituladoindigena911.to_excel(archivo, sheet_name = "III_2b")
    egresadoanualedad911.to_excel(archivo, sheet_name = "III_3a")
    tituladoanualedad911.to_excel(archivo, sheet_name = "III_3b")
    admisioncicloactual911.to_excel(archivo, sheet_name = "V_2y3")
    admisiondiscapacidad911.to_excel(archivo, sheet_name = "V_3a")
    admisionindigena911.to_excel(archivo, sheet_name = "V_3b")
    inscritocicloactual911.to_excel(archivo, sheet_name = "V_4")
    inscritodiscapacidad911.to_excel(archivo, sheet_name = "V_4a")
    inscritoindigena911.to_excel(archivo, sheet_name = "V_4b")
    inscritobachiller911.to_excel(archivo, sheet_name = "V_5a_b")
    inscritoestado911.to_excel(archivo, sheet_name = "V_6")
    matriculacicloactual911.to_excel(archivo, sheet_name = "VI_1")
    matriculadiscapacidad911.to_excel(archivo, sheet_name = "VI_1a")
    matriculagradonacimiento911.to_excel(archivo, sheet_name = "VI_1b")
    matriculaindigena911.to_excel(archivo, sheet_name = "VI_1c")
    matriculaprocedencia911.to_excel(archivo, sheet_name = "VI_2a")
    matriculanacimiento911.to_excel(archivo, sheet_name = "VI_2b")
    matriculaedadgradosexo911.to_excel(archivo, sheet_name = "VI_3")
    matriculadiscapacidaddetalle911.to_excel(archivo, sheet_name = "VI_4")
    matriculaindigenatotal911.to_excel(archivo, sheet_name = "VI_5")
    matriculaindigenatotaldiscapacidad911.to_excel(archivo, sheet_name = "VI_5a")
    archivo.close()