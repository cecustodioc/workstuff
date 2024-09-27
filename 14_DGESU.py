# -*- coding: utf-8 -*-
"""
Creado 08/06/2022 14:03
@author: Carlos Ernesto Custodio Cadena
Cálcular informe DGESU con archivos csv
Última revisión: 09/07/2024
"""
import pandas as pd
#  Se leen todos los origenes de datos del informe Junta Directiva y DGESU
dinscrito = pd.read_csv("dato/inscrito.csv", encoding="unicode escape", index_col = False)
origen = "dato/"
destino = "DGESU/"
nombre = "DGESU_20242T"
#  CIERRE solo alumnos vigentes, APERTURA todos los que se inscribieron inicialmente
#  para el informe DGESU la matricula de interés es la de CIERRE
dinscrito = dinscrito[dinscrito["MATRICULADE"]=="CIERRE"]
dadmision = pd.read_csv(origen + "admision.csv", encoding="unicode escape", index_col = False)
#  Se ordenan los DataFrames obtenidos
dinscrito = dinscrito.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "GRADO", "SEXO"],
    ascending=[False, True, True, True, True, True])
dadmision = dadmision.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
#  Se obtienen todas las columnas que serán el origen de los indices
iprog_educ = tuple(dinscrito["PROG_EDUC"])
#  Funciones para crear los indices de Informe a la Junta Directiva y DGESU
def crea_idx(lista):
    if isinstance(lista, (tuple, list)):
        idx = []
        for elemento in lista:
            if elemento not in idx:
                idx.append(elemento)
    return idx
def fol_sf_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
    admision_sf = prog_educ["FOLIO_PRE"].count()
    return admision_sf
def fol_sm_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "M"]
    admision_sm = prog_educ["FOLIO_PRE"].count()
    return admision_sm
def fol_st_pe(prog_educ):
    admision_st = prog_educ["FOLIO_PRE"].count()
    return admision_st
def fol_af_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
    prog_educ = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
    admision_af = prog_educ["FOLIO_PRE"].count()
    return admision_af
def fol_am_pe(prog_educ):
    prog_educ_am = prog_educ[prog_educ["SEXO"] == "M"]
    prog_educ_am = prog_educ_am[prog_educ_am["ESTATUS"] == "ACEPTADO"]
    admision_am = prog_educ_am["FOLIO_PRE"].count()
    return admision_am
def fol_at_pe(prog_educ):
    prog_educ_at = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
    admision_at = prog_educ_at["FOLIO_PRE"].count()
    return admision_at
def matr_f_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
    m_f = prog_educ["MATRICULA"].count()
    return m_f
def matr_m_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "M"]
    m_m = prog_educ["MATRICULA"].count()
    return m_m
def matr_t_pe(prog_educ):
    m_t = prog_educ["MATRICULA"].count()
    return m_t
#  Se crean las estructuras de datos para el informe de la Junta Directiva
idx_dgesu = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "ADF": [],
        "ADM": [],
        "ADT": [],
        "NIF": [],
        "NIM": [],
        "NIT": [],
        "RIF": [],
        "RIM": [],
        "RIT": [],
        "MTF": [],
        "MTM": [],
        "MT": []})
#  Se crean todos los indices para las consultas
diprog_educ = crea_idx(iprog_educ)
#  Se realiza el ciclo para obtener todos los indicadores del ciclo actual
for p in diprog_educ:
    itemp = dinscrito[dinscrito["PROG_EDUC"] == p]
    atemp = dadmision[dadmision["PROG_EDUC"] == p]
    #  Contiene información de alumnos de NI ciclo actual
    itempadm = dinscrito[dinscrito["PROG_EDUC"]==p]
    itempadm = itempadm[itempadm["T_INS"] == "NI"]
    itempadm = itempadm[itempadm["E_EXT"] == "ADM"]
    itempadm = itempadm[itempadm["E_INT"] == "ADM"]
    #  ----------------INFORME DGESU
    #  Reporte de Aspirantes/Nuevo ingreso/reingreso del ciclo
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "ADF": fol_af_pe(atemp),
            "ADM": fol_am_pe(atemp),
            "ADT": fol_at_pe(atemp),
            "NIF": matr_f_pe(itempadm),
            "NIM": matr_m_pe(itempadm),
            "NIT": matr_t_pe(itempadm),
            "RIF": matr_f_pe(itemp) - matr_f_pe(itempadm),
            "RIM": matr_m_pe(itemp) - matr_m_pe(itempadm),
            "RIT": matr_t_pe(itemp) - matr_t_pe(itempadm),
            "MTF": matr_f_pe(itemp),
            "MTM": matr_m_pe(itemp),
            "MT": matr_t_pe(itemp)}, index=[len(idx_dgesu)])
    idx_dgesu = pd.concat([idx_dgesu, idx_tmp])
#  Se crea el archivo de Excel para el informe DGESU
writer = pd.ExcelWriter(destino + nombre + ".xlsx")
idx_dgesu.to_excel(writer, sheet_name = nombre)
dinscrito.to_excel(writer, sheet_name="inscrito")
dadmision.to_excel(writer, sheet_name="admision")
writer.close()
