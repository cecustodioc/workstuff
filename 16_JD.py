# -*- coding: utf-8 -*-
"""
Creado 08/06/2022 14:03
@author: Carlos Ernesto Custodio Cadena
Cálcular los indicadores escolares tomando como entrada archivos csv
Última revisión: 14/08/2024
Deben realizarse dos consultas las primera para los ciclos anteriores (cierre) y la segunda para los ciclos actuales (apertura), posteriormente se ejecuta este script para cada conjunto de datos cuidando actualizar el nombre del archivo de salida y los nombres de los archivos origen de datos.
Se sugiere el posfijo AN para ciclos anteriores, AC para ciclos actuales e incluir las palabras apertura y cierre según corresponda como nombre del archivo de salida (xlsx)
"""
import pandas as pd
origen = "dato/"
destino = "JD/"
nombre = "JD_III_CIERRE_2024"
#  Se leen todos los origenes de datos del informe Junta Directiva y DGESU
dinscrito = pd.read_csv(origen + "inscritoan.csv", encoding="unicode escape", index_col = False)
#  CIERRE solo alumnos vigentes, APERTURA todos los que se inscribieron inicialmente
#  Se seleccionan los alumnos que se iunscribieron y continuan inscritos a la fecha como matrícula del periodo
dinscrito = dinscrito[dinscrito["MATRICULADE"]=="CIERRE"]
dadmision = pd.read_csv(origen + "admisionan.csv", encoding="unicode escape", index_col = False)
dbaja = pd.read_csv(origen + "bajaan.csv", encoding="unicode escape", index_col = False)
ddesercion = pd.read_csv(origen + "desercionan.csv", encoding="unicode escape", index_col = False)
dcohorte = pd.read_csv(origen + "cohortean.csv", encoding="unicode escape", index_col = False)
degresado = pd.read_csv(origen + "egresadoan.csv", encoding="unicode escape", index_col = False)
dtitulado = pd.read_csv(origen + "tituladoan.csv", encoding="unicode escape", index_col = False)
dtitulado = dtitulado.fillna("NO")
dtransicion1 = pd.read_csv(origen + "transicionan.csv", encoding="unicode escape", index_col = False)
dtransicion1['PERIODO'] = 'PAS'
dtransicion2 = pd.read_csv(origen + "transicionan.csv", encoding="unicode escape", index_col = False)
dtransicion2 = dtransicion2[dtransicion2['INSCRITO']=='SI']
dtransicion2['PERIODO']='PRE'
dtransicion = pd.concat([dtransicion1,dtransicion2])
#  Se ordenan los DataFrames obtenidos
dinscrito = dinscrito.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "GRADO", "SEXO"],
    ascending=[False, True, True, True, True, True])
dadmision = dadmision.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
dbaja = dbaja.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
ddesercion = ddesercion.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
dcohorte = dcohorte.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
degresado = degresado.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
dtitulado = dtitulado.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
#  Se obtienen todas las columnas que serán el origen de los indices
iprog_educ = tuple(dinscrito["PROG_EDUC"])
idiscap = tuple(dinscrito["DISCAPACIDAD"])
isexo = tuple(dinscrito["SEXO"])
igrado = tuple(dinscrito["GRADO"])
ietnia = tuple(dinscrito["ETNIA"])
inacimiento = tuple(dinscrito["MUN_NAC"])
iprocedencia = tuple(dinscrito["MUN_PROC"])
adiscap = tuple(dadmision["DISCAPACIDAD"])
aetnia = tuple(dadmision["ETNIA"])
anacimiento = tuple(dadmision["MUN_NAC"])
aprocedencia = tuple(dadmision["MUN_PROC"])
bprog_educ = tuple(dbaja["PROG_EDUC"])
bcausa = tuple(dbaja["CAUSA"])
btipo = tuple(dbaja["TIPO"])
cprog_educ = tuple(dcohorte["PROG_EDUC"])
eprog_educ = tuple(degresado["PROG_EDUC"])
ecohorte = tuple(degresado["COHORTE"])
tprog_educ = tuple(dtitulado["PROG_EDUC"])
tcohorte = tuple(dtitulado["COHORTE"])
#  Funciones para crear los indices de Informe a la Junta Directiva y DGESU
def crea_idx(lista):
    if isinstance(lista, (tuple, list)):
        idx = []
        for elemento in lista:
            if elemento not in idx:
                idx.append(elemento)
    return idx
def indice(divisor, dividendo):
    if divisor == 0:
        return 0
    ind = round(dividendo / divisor * 100, 2)
    return ind
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
def contar_adiscap(prog_educ, discap, sex):
   prog_educ = prog_educ[prog_educ["DISCAPACIDAD"] == discap]
   prog_educ = prog_educ[prog_educ["SEXO"] == sex]
   prog_educ = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
   nadiscap = prog_educ["FOLIO_PRE"].count()
   return nadiscap
def contar_aetnia(prog_educ, etnia, sex):
   prog_educ = prog_educ[prog_educ["ETNIA"] == etnia]
   prog_educ = prog_educ[prog_educ["SEXO"] == sex]
   prog_educ = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
   naetnia = prog_educ["FOLIO_PRE"].count()
   return naetnia
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
def matr_ce_pe(prog_educ, cohorte):
    prog_educ = prog_educ[prog_educ["COHORTE"] == cohorte]
    prog_educ = prog_educ[prog_educ["EGRESADO"]=="SI"]
    m_ct = prog_educ["MATRICULA"].count()
    return m_ct
def matr_ct_pe(prog_educ, cohorte):
    prog_educ = prog_educ[prog_educ["COHORTE"] == cohorte]
    m_ct = prog_educ["MATRICULA"].count()
    return m_ct
def matr_d_pe(prog_educ, sx):
    if sx != "T":
        prog_educ = prog_educ[prog_educ["SEXO"] == sx]
    prog_educ = prog_educ[prog_educ["EGRESADO"] == "NO"]
    prog_educ = prog_educ[prog_educ["INSCRITO"] == "NO"]
    prog_educ = prog_educ[prog_educ["BAJA"] == "NO"]
    matricula_ctotal = prog_educ["MATRICULA"].count()
    return matricula_ctotal
def matr_ef_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
    prog_educ = prog_educ[prog_educ["AVANCE"] >= 100]
    prog_educ = prog_educ[prog_educ["EGRESADO"]=="SI"]
    matricula_ef = prog_educ["MATRICULA"].count()
    return matricula_ef
def matr_em_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "M"]
    prog_educ = prog_educ[prog_educ["AVANCE"] >= 100]
    prog_educ = prog_educ[prog_educ["EGRESADO"]=="SI"]
    matricula_em = prog_educ["MATRICULA"].count()
    return matricula_em
def matr_et_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["AVANCE"] >= 100]
    prog_educ = prog_educ[prog_educ["EGRESADO"]=="SI"]
    matricula_et = prog_educ["MATRICULA"].count()
    return matricula_et

def matr_eft_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
    prog_educ = prog_educ[prog_educ["AVANCE"] >= 100]
    prog_educ = prog_educ[prog_educ["TITULADO"]=="SI"]
    matricula_ef = prog_educ["MATRICULA"].count()
    return matricula_ef
def matr_emt_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "M"]
    prog_educ = prog_educ[prog_educ["AVANCE"] >= 100]
    prog_educ = prog_educ[prog_educ["TITULADO"]=="SI"]
    matricula_em = prog_educ["MATRICULA"].count()
    return matricula_em
def matr_ett_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["AVANCE"] >= 100]
    prog_educ = prog_educ[prog_educ["TITULADO"]=="SI"]
    matricula_et = prog_educ["MATRICULA"].count()
    return matricula_et

def matr_egf_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
    prog_educ = prog_educ[prog_educ["EGRESADO"] >= "SI"]
    matricula_ef = prog_educ["MATRICULA"].count()
    return matricula_ef
def matr_egm_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["SEXO"] == "M"]
    prog_educ = prog_educ[prog_educ["EGRESADO"] >= "SI"]
    matricula_em = prog_educ["MATRICULA"].count()
    return matricula_em
def matr_egt_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["EGRESADO"] >= "SI"]
    matricula_et = prog_educ["MATRICULA"].count()
    return matricula_et
def matr_tm_pe(prog_educ):
   prog_educ = prog_educ[prog_educ["TURNO"] == "M"]
   matricula_tm = prog_educ["MATRICULA"].count()
   return matricula_tm
def matr_tv_pe(prog_educ):
   prog_educ = prog_educ[prog_educ["TURNO"] == "V"]
   matricula_tv = prog_educ["MATRICULA"].count()
   return matricula_tv
def matr_irrf_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["STATUS"] == "IRR"]
    prog_educ = prog_educ[(prog_educ["SEXO"] == "F")]
    matricula_rf = prog_educ["MATRICULA"].count()
    return matricula_rf
def matr_irrm_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["STATUS"] == "IRR"]
    prog_educ_rm = prog_educ[(prog_educ["SEXO"] == "M")]
    matricula_rm = prog_educ_rm["MATRICULA"].count()
    return matricula_rm
def matr_irr_pe(prog_educ):
    prog_educ = prog_educ[prog_educ["STATUS"] == "IRR"]
    matricula_r = prog_educ["MATRICULA"].count()
    return matricula_r
def matr_b_pe(prog_educ, tb, cb, sb):
    prog_educ = prog_educ[prog_educ["TIPO"] == tb]
    prog_educ = prog_educ[prog_educ["CAUSA"] == cb]
    prog_educ = prog_educ[prog_educ["SEXO"] == sb]
    matricula_b = prog_educ["MATRICULA"].count()
    return matricula_b
def ind_aprof_pe(prog_educ):
   prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
   if matr_t_pe(prog_educ) == 0:
       return 0
   matricula_aprof = round(prog_educ["PROM_PARC"].mean(), 2)
   #  Se homologa la escala a porcentajes ya que hay planes de 0 a 10 y de 0 a 100
   if matricula_aprof<11:
       matricula_aprof = round(matricula_aprof * 10,2)
   return matricula_aprof
def ind_aprom_pe(prog_educ):
   prog_educ = prog_educ[prog_educ["SEXO"] == "M"]
   if matr_t_pe(prog_educ) == 0:
       return 0
   matricula_aprom = round(prog_educ["PROM_PARC"].mean(), 2)
   #  Se homologa la escala a porcentajes ya que hay planes de 0 a 10 y de 0 a 100
   if matricula_aprom<11:
       matricula_aprom = round(matricula_aprom * 10,2)
   return matricula_aprom
def ind_apro_pe(prog_educ):
   if matr_t_pe(prog_educ) == 0:
       return 0
   matricula_apro = round(prog_educ["PROM_PARC"].mean(), 2)
   #  Se homologa la escala a porcentajes ya que hay planes de 0 a 10 y de 0 a 100
   if matricula_apro<11:
       matricula_apro = round(matricula_apro * 10,2)
   return matricula_apro
def contar_grado(prog_educ, grado, sex):
   prog_educ = prog_educ[prog_educ["GRADO"] == grado]
   prog_educ = prog_educ[prog_educ["SEXO"] == sex]
   ngrado = prog_educ["MATRICULA"].count()
   return ngrado
def contar_lugar_nac(prog_educ, nac):
   prog_educ = prog_educ[prog_educ["MUN_NAC"] == nac]
   n_l_n = prog_educ["MATRICULA"].count()
   return n_l_n
def contar_proc_bach(prog_educ, bac):
   prog_educ = prog_educ[prog_educ["MUN_PROC"] == bac]
   n_p_b = prog_educ["MATRICULA"].count()
   return n_p_b
def contar_alugar_nac(prog_educ, nac):
   prog_educ = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
   prog_educ = prog_educ[prog_educ["MUN_NAC"] == nac]
   n_l_n = prog_educ["MATRICULA"].count()
   return n_l_n
def contar_aproc_bach(prog_educ, bac):
   prog_educ = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
   prog_educ = prog_educ[prog_educ["MUN_PROC"] == bac]
   n_p_b = prog_educ["MATRICULA"].count()
   return n_p_b
def contar_discap(prog_educ, discap, sex):
   prog_educ = prog_educ[prog_educ["DISCAPACIDAD"] == discap]
   prog_educ = prog_educ[prog_educ["SEXO"] == sex]
   ndiscap = prog_educ["MATRICULA"].count()
   return ndiscap
def contar_etnia(prog_educ, etnia, sex):
   prog_educ = prog_educ[prog_educ["ETNIA"] == etnia]
   prog_educ = prog_educ[prog_educ["SEXO"] == sex]
   netnia = prog_educ["MATRICULA"].count()
   return netnia
def contar_t_gpo(prog_educ, grado, grupo):
   prog_educ = prog_educ[prog_educ["GRADO"] == grado]
   prog_educ = prog_educ[prog_educ["GRUPO"] == grupo]
   n_t_gpo = prog_educ["MATRICULA"].count()
   return n_t_gpo
def contar_s_gpo(prog_educ, grado, grupo, sexo):
   prog_educ = prog_educ[prog_educ["GRADO"] == grado]
   prog_educ = prog_educ[prog_educ["GRUPO"] == grupo]
   prog_educ = prog_educ[prog_educ["SEXO"] == sexo]
   n_s_gpo = prog_educ["MATRICULA"].count()
   return n_s_gpo
#  Se crean las estructuras de datos para el informe de la Junta Directiva
idx_m = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F": [],
        "M": [],
        "TOTAL": []})
idx_mreprobacion = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F_T":[],
        "M_T":[],
        "T_PE":[],
        "F": [],
        "M": [],
        "TOTAL": [],
        "IR_F": [],
        "IR_M": [],
        "IR_PROG_EDUC": []})
idx_mdesercion = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "CA_F":[],
        "CA_M":[],
        "CA_T":[],
        "NRI_F": [],
        "NRI_M": [],
        "NRI_T": [],
        "ID_F": [],
        "ID_M": [],
        "ID_P_E": []})
idx_maprovechamiento = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F": [],
        "M": [],
        "TOTAL": []})
idx_mdiscap = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "DISCAP": [],
        "SEXO": [],
        "CANT": []})
idx_metnia = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "ETNIA": [],
        "SEXO": [],
        "CANT": []})
idx_mnacimiento = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "LUGAR_NAC": [],
        "CANT": []})
idx_mprocedencia = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "PROC_BACH": [],
        "CANT": []})
idx_mturno = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "MATUTINO": [],
        "VESPERTINO": [],
        "TOTAL": []})
idx_ni = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "NIF": [],
        "NIM": [],
        "NIT": []})
idx_atn_dmda = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "SOF": [],
        "SOM": [],
        "SOT": [],
        "ADF": [],
        "ADM": [],
        "ADT": [],
        "IADF": [],
        "IADM": [],
        "IADT": []})
idx_adiscap = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "DISCAP": [],
        "SEXO": [],
        "CANT": []})
idx_aetnia = pd.DataFrame({
        "MODALIDAD":[],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "ETNIA": [],
        "SEXO": [],
        "CANT": []})
idx_anacimiento = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "LUGAR_NAC": [],
        "CANT": []})
idx_aprocedencia = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "PROC_BACH": [],
        "CANT": []})
idx_nidiscap = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "DISCAP": [],
        "SEXO": [],
        "CANT": []})
idx_nietnia = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "ETNIA": [],
        "SEXO": [],
        "CANT": []})
idx_ninacimiento = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "LUGAR_NAC": [],
        "CANT": []})
idx_niprocedencia = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "PROC_BACH": [],
        "CANT": []})
idx_bajadef = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F": [],
        "M": [],
        "TOTAL": [],
        "IB_F": [],
        "IB_M": [],
        "IB_PROG_EDUC": []})
idx_bajatemp = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F": [],
        "M": [],
        "TOTAL": [],
        "IB_F": [],
        "IB_M": [],
        "IB_PROG_EDUC": []})
idx_bajacyt = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "TIPO": [],
        "CAUSA": [],
        "SEXO": [],
        "CANT": []})
idx_egresado = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F": [],
        "M": [],
        "TOTAL": []})
idx_egresado_cohorte = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "COHORTE": [],
        "CANT": []})
idx_titulado = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F": [],
        "M": [],
        "TOTAL": []})
idx_titulado_cohorte = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "COHORTE": [],
        "CANT": []})
idx_cohorte = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "NI_F": [],
        "NI_M": [],
        "NI_PE": [],
        "EG_F": [],
        "EG_M": [],
        "EG_PE": [],
        "EFIC_F": [],
        "EFIC_M": [],
        "EFIC_PE": []})
idx_cohorte_titulado = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "EG_F": [],
        "EG_M": [],
        "EG_PE": [],
        "TI_F": [],
        "TI_M": [],
        "TI_PE": [],
        "EFIC_F": [],
        "EFIC_M": [],
        "EFIC_PE": []})

#  Se crean todos los indices para las consultas
diprog_educ = crea_idx(iprog_educ)
didiscap = crea_idx(idiscap)
disexo = crea_idx(isexo)
digrado = crea_idx(igrado)
dietnia = crea_idx(ietnia)
dinacimiento = crea_idx(inacimiento)
diprocedencia = crea_idx(iprocedencia)
dadiscap = crea_idx(adiscap)
daetnia = crea_idx(aetnia)
danacimiento = crea_idx(anacimiento)
daprocedencia = crea_idx(aprocedencia)
dbprog_educ = crea_idx(bprog_educ)
dbcausa = crea_idx(bcausa)
dbtipo = crea_idx(btipo)
dcprog_educ = crea_idx(cprog_educ)
deprog_educ = crea_idx(eprog_educ)
decohorte = crea_idx(ecohorte)
decohorte.sort()
dtprog_educ = crea_idx(tprog_educ)
dtcohorte = crea_idx(tcohorte)
dtcohorte.sort()
#  Se realiza el ciclo para obtener todos los indicadores del ciclo actual
for p in diprog_educ:
    itemp = dinscrito[dinscrito["PROG_EDUC"] == p]
    itemp = itemp[itemp["MATRICULADE"] == "CIERRE"]
    #  Evita que se presenten datos de alumnos que se dieron de baja en el informe
    atemp = dadmision[dadmision["PROG_EDUC"] == p]
    dtemp = ddesercion[ddesercion["PROG_EDUC"] == p]
    #dtemp = dtemp[dtemp['BAJA']=='NO']
    #dtemp = dtemp[dtemp['EGRESADO']=='NO']
    #  Contiene información de alumnos de NI ciclo actual
    itempadm = dinscrito[dinscrito["PROG_EDUC"]==p]
    itempadm = itempadm[itempadm["T_INS"] == "NI"]
    itempadm = itempadm[itempadm["E_EXT"] == "ADM"]
    itempadm = itempadm[itempadm["E_INT"] == "ADM"]
    #  ----------------- INDICADORES INSCRITOS CICLO ACTUAL
    #  Matrícula
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "F": matr_f_pe(itemp),
            "M": matr_m_pe(itemp),
            "TOTAL": matr_t_pe(itemp)}, index=[len(idx_m)])
    idx_m = pd.concat([idx_m, idx_tmp])
    #  Matrícula x turno
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "MATUTINO": matr_tm_pe(itemp),
            "VESPERTINO": matr_tv_pe(itemp),
            "TOTAL": matr_t_pe(itemp)}, index=[len(idx_mturno)])
    idx_mturno = pd.concat([idx_mturno, idx_tmp])
    #  Índice reprobación
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "F_T":matr_f_pe(itemp),
            "M_T":matr_m_pe(itemp),
            "T_PE":matr_t_pe(itemp),
            "F": matr_irrf_pe(itemp),
            "M": matr_irrm_pe(itemp),
            "TOTAL": matr_irr_pe(itemp),
            "IR_F": indice(matr_f_pe(itemp), matr_irrf_pe(itemp)),
            "IR_M": indice(matr_m_pe(itemp), matr_irrm_pe(itemp)),
            "IR_PROG_EDUC": indice(matr_t_pe(itemp), matr_irr_pe(itemp))}, index=[len(idx_mreprobacion)])
    if matr_irr_pe(itemp)!=0:
        idx_mreprobacion = pd.concat([idx_mreprobacion,idx_tmp])
    #  Índice de aprovechamiento
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "F": ind_aprof_pe(itemp),
            "M": ind_aprom_pe(itemp),
            "TOTAL": ind_apro_pe(itemp)}, index=[len(idx_maprovechamiento)])
    idx_maprovechamiento = pd.concat([idx_maprovechamiento,idx_tmp])
    #  Matrícula con discapacidad
    for d in didiscap:
        if d not in ("NINGUNA", "Ninguna"):
            for s in disexo:
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": itemp["MODALIDAD"].max(),
                        "NIVEL": itemp["NIVEL"].max(),
                        "SISTEMA": itemp["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itemp["PLAN"].max(),
                        "DIVISION": itemp["DIVISION"].max(),
                        "DISCAP": d,
                        "SEXO": s,
                        "CANT": contar_discap(itemp, d, s)}, index=[len(idx_mdiscap)])
                idx_mdiscap = pd.concat([idx_mdiscap, idx_tmp])
    #  Matrícula por etnia
    for e in dietnia:
        if e != "NINGUNA" and d != "Ninguna":
            for s in disexo:
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": itemp["MODALIDAD"].max(),
                        "NIVEL": itemp["NIVEL"].max(),
                        "SISTEMA": itemp["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itemp["PLAN"].max(),
                        "DIVISION": itemp["DIVISION"].max(),
                        "ETNIA": e,
                        "SEXO": s,
                        "CANT": contar_etnia(itemp, e, s)}, index=[len(idx_metnia)])
                idx_metnia = pd.concat([idx_metnia, idx_tmp])
    #  Matrícula por lugar de nacimiento
    for ln in dinacimiento:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itemp["MODALIDAD"].max(),
                "NIVEL": itemp["NIVEL"].max(),
                "SISTEMA": itemp["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itemp["PLAN"].max(),
                "DIVISION": itemp["DIVISION"].max(),
                "LUGAR_NAC": ln,
                "CANT": contar_lugar_nac(itemp, ln)}, index=[len(idx_mnacimiento)])
        idx_mnacimiento = pd.concat([idx_mnacimiento, idx_tmp])
    #  Matrícula por lugar de procedencia bachiller
    for pb in diprocedencia:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itemp["MODALIDAD"].max(),
                "NIVEL": itemp["NIVEL"].max(),
                "SISTEMA": itemp["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itemp["PLAN"].max(),
                "DIVISION": itemp["DIVISION"].max(),
                "PROC_BACH": pb,
                "CANT": contar_proc_bach(itemp, pb)}, index=[len(idx_mprocedencia)])
        idx_mprocedencia = pd.concat([idx_mprocedencia, idx_tmp])
    #  -----INDICADORES NUEVO INGRESO CICLO ACTUAL
    #  Matrícula de nuevo ingreso
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itempadm["MODALIDAD"].max(),
            "NIVEL": itempadm["NIVEL"].max(),
            "SISTEMA": itempadm["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itempadm["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "NIF": matr_f_pe(itempadm),
            "NIM": matr_m_pe(itempadm),
            "NIT": matr_t_pe(itempadm)}, index=[len(idx_ni)])
    if matr_t_pe(itempadm)!=0:
        idx_ni = pd.concat([idx_ni, idx_tmp])
    #  Matrícula por discapacidad nuevo ingreso
    for d in didiscap:
        if d not in ("NINGUNA", "Ninguna"):
            for s in disexo:
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": itempadm["MODALIDAD"].max(),
                        "NIVEL": itempadm["NIVEL"].max(),
                        "SISTEMA": itempadm["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itempadm["PLAN"].max(),
                        "DIVISION": itempadm["DIVISION"].max(),
                        "DISCAP": d,
                        "SEXO": s,
                        "CANT": contar_discap(itempadm, d, s)}, index=[len(idx_nidiscap)])
                idx_nidiscap = pd.concat([idx_nidiscap, idx_tmp])
    #  Matrícula por etnia nuevo ingreso
    for e in dietnia:
        if e != "NINGUNA" and d != "Ninguna":
            for s in disexo:
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": itempadm["MODALIDAD"].max(),
                        "NIVEL": itempadm["NIVEL"].max(),
                        "SISTEMA": itempadm["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itempadm["PLAN"].max(),
                        "DIVISION": itempadm["DIVISION"].max(),
                        "ETNIA": e,
                        "SEXO": s,
                        "CANT": contar_etnia(itempadm, e, s)}, index=[len(idx_nietnia)])
                idx_nietnia = pd.concat([idx_nietnia, idx_tmp])
    #  Matrícula por lugar de nacimiento nuevo ingreso
    for ln in dinacimiento:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itempadm["MODALIDAD"].max(),
                "NIVEL": itempadm["NIVEL"].max(),
                "SISTEMA": itempadm["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itempadm["PLAN"].max(),
                "DIVISION": itempadm["DIVISION"].max(),
                "LUGAR_NAC": ln,
                "CANT": contar_lugar_nac(itempadm, ln)}, index=[len(idx_ninacimiento)])
        idx_ninacimiento = pd.concat([idx_ninacimiento, idx_tmp])
    #  Matrícula por procedencia de bachiller nuevo ingreso
    for pb in diprocedencia:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itempadm["MODALIDAD"].max(),
                "NIVEL": itempadm["NIVEL"].max(),
                "SISTEMA": itempadm["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itempadm["PLAN"].max(),
                "DIVISION": itempadm["DIVISION"].max(),
                "PROC_BACH": pb,
                "CANT": contar_proc_bach(itempadm, pb)}, index=[len(idx_niprocedencia)])
        idx_niprocedencia = pd.concat([idx_niprocedencia, idx_tmp])
    # ------INDICADORES ADMISION CICLO ACTUAL
    #  Atención a la demanda nuevo ingreso
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "SOF": fol_sf_pe(atemp),
            "SOM": fol_sm_pe(atemp),
            "SOT": fol_st_pe(atemp),
            "ADF": fol_af_pe(atemp),
            "ADM": fol_am_pe(atemp),
            "ADT": fol_at_pe(atemp),
            "IADF": indice(fol_sf_pe(atemp), fol_af_pe(atemp)),
            "IADM": indice(fol_sm_pe(atemp), fol_am_pe(atemp)),
            "IADT": indice(fol_st_pe(atemp), fol_at_pe(atemp))}, index=[len(idx_atn_dmda)])
    #  Discapacidad de aspirantes
    if indice(fol_st_pe(atemp), fol_at_pe(atemp))!=0:  #  Lo agrega si > 0
        idx_atn_dmda = pd.concat([idx_atn_dmda, idx_tmp])
    for d in dadiscap:
        if d not in ("NINGUNA", "Ninguna"):
            for s in disexo:
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": itemp["MODALIDAD"].max(),
                        "NIVEL": itemp["NIVEL"].max(),
                        "SISTEMA": itemp["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itemp["PLAN"].max(),
                        "DIVISION": itemp["DIVISION"].max(),
                        "DISCAP": d,
                        "SEXO": s,
                        "CANT": contar_adiscap(atemp, d, s)}, index=[len(idx_adiscap)])
                idx_adiscap = pd.concat([idx_adiscap, idx_tmp])
    #  Etnia  de aspirantes
    for e in daetnia:
        if e != "NINGUNA" and d != "Ninguna":
            for s in disexo:
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": itemp["MODALIDAD"].max(),
                        "NIVEL": itemp["NIVEL"].max(),
                        "SISTEMA": itemp["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itemp["PLAN"].max(),
                        "DIVISION": itemp["DIVISION"].max(),
                        "ETNIA": e,
                        "SEXO": s,
                        "CANT": contar_aetnia(atemp, e, s)}, index=[len(idx_aetnia)])
                idx_aetnia = pd.concat([idx_aetnia, idx_tmp])
    #  Lugar de nacimiento aspirantes
    for ln in danacimiento:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itemp["MODALIDAD"].max(),
                "NIVEL": itemp["NIVEL"].max(),
                "SISTEMA": itemp["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itemp["PLAN"].max(),
                "DIVISION": itemp["DIVISION"].max(),
                "LUGAR_NAC": ln,
                "CANT": contar_alugar_nac(atemp, ln)}, index=[len(idx_anacimiento)])
        idx_anacimiento = pd.concat([idx_anacimiento, idx_tmp])
    #  Procedencia bachiller aspirantes
    for pb in daprocedencia:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itemp["MODALIDAD"].max(),
                "NIVEL": itemp["NIVEL"].max(),
                "SISTEMA": itemp["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itemp["PLAN"].max(),
                "DIVISION": itemp["DIVISION"].max(),
                "PROC_BACH": pb,
                "CANT": contar_aproc_bach(atemp, pb)}, index=[len(idx_aprocedencia)])
        idx_aprocedencia = pd.concat([idx_aprocedencia, idx_tmp])
    #  ------------------INDICADORES DESERCION CICLO ACTUAL
    #  Deserción: PCT INSCRITOS CICLO ANTERIOR QUE NO SE REINSCRIBIERON
    idx_tmp = pd.DataFrame({
            "MODALIDAD": dtemp["MODALIDAD"].max(),
            "NIVEL": dtemp["NIVEL"].max(),
            "SISTEMA": dtemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": dtemp["PLAN"].max(),
            "DIVISION": dtemp["DIVISION"].max(),
            "CA_F": matr_f_pe(dtemp),
            "CA_M": matr_m_pe(dtemp),
            "CA_T": matr_t_pe(dtemp),
            "NRI_F": matr_d_pe(dtemp,"F"),
            "NRI_M": matr_d_pe(dtemp,"M"),
            "NRI_T": matr_d_pe(dtemp,"T"),
            "ID_F": round(indice(matr_f_pe(dtemp), matr_d_pe(dtemp,"F")), 2),
            "ID_M": round(indice(matr_m_pe(dtemp), matr_d_pe(dtemp,"M")), 2),
            "ID_P_E": indice(matr_t_pe(dtemp), matr_d_pe(dtemp,"T"))},index = [len(idx_mdesercion)])
    if matr_t_pe(dtemp) !=0:
        idx_mdesercion = pd.concat([idx_mdesercion, idx_tmp])
#  ---------------------INDICADORES BAJAS PERIODO ACTUAL
for p in dbprog_educ:
    btemp = dbaja[dbaja["PROG_EDUC"] == p]
    itemp = dinscrito[dinscrito["PROG_EDUC"] == p]
    #  Baja definitiva
    bdtemp = btemp[btemp["TIPO"] == "DEFINITIVA"]
    idx_tmp = pd.DataFrame({
            "MODALIDAD": btemp["MODALIDAD"].max(),
            "NIVEL": btemp["NIVEL"].max(),
            "SISTEMA": btemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": btemp["PLAN"].max(),
            "DIVISION": btemp["DIVISION"].max(),
            "F": matr_f_pe(bdtemp),
            "M": matr_m_pe(bdtemp),
            "TOTAL": matr_t_pe(bdtemp),
            "IB_F": indice(matr_f_pe(itemp), matr_f_pe(bdtemp)),
            "IB_M": indice(matr_m_pe(itemp), matr_m_pe(bdtemp)),
            "IB_PROG_EDUC": indice(matr_t_pe(itemp), matr_t_pe(bdtemp))}, index=[len(idx_bajadef)])
    #if indice(matr_f_pe(itemp), matr_f_pe(bdtemp))!=0 or  indice(matr_m_pe(itemp), matr_m_pe(bdtemp))!=0:
    idx_bajadef = pd.concat([idx_bajadef, idx_tmp])
    #  Baja temporal
    bttemp = btemp[btemp["TIPO"] == "TEMPORAL"]
    idx_tmp = pd.DataFrame({
            "MODALIDAD": btemp["MODALIDAD"].max(),
            "NIVEL": btemp["NIVEL"].max(),
            "SISTEMA": btemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": btemp["PLAN"].max(),
            "DIVISION": btemp["DIVISION"].max(),
            "F": matr_f_pe(bttemp),
            "M": matr_m_pe(bttemp),
            "TOTAL": matr_t_pe(bttemp),
            "IB_F": indice(matr_f_pe(itemp), matr_f_pe(bttemp)),
            "IB_M": indice(matr_m_pe(itemp), matr_m_pe(bttemp)),
            "IB_PROG_EDUC": indice(matr_t_pe(itemp), matr_t_pe(bttemp))}, index = [len(idx_bajatemp)])
    #if indice(matr_f_pe(itemp), matr_f_pe(bttemp))!=0 or indice(matr_m_pe(itemp), matr_m_pe(bttemp))!=0:
    idx_bajatemp = pd.concat([idx_bajatemp, idx_tmp])
    #  Conteo de las causas de baja por tipo y causa
    for dbt in dbtipo:
        for dbc in dbcausa:
            for dis in disexo:
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": btemp["MODALIDAD"].max(),
                        "NIVEL": btemp["NIVEL"].max(),
                        "SISTEMA": btemp["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": btemp["PLAN"].max(),
                        "DIVISION": btemp["DIVISION"].max(),
                        "TIPO": dbt,
                        "CAUSA": dbc,
                        "SEXO": dis,
                        "CANT": matr_b_pe(btemp, dbt, dbc, dis)}, index = [len(idx_bajacyt)])
                idx_bajacyt = pd.concat([idx_bajacyt, idx_tmp])
    #  Bajas definitivas
    idx_bajacytdef = idx_bajacyt[idx_bajacyt["TIPO"] == "DEFINITIVA"]
    #  Bajas temporales
    idx_bajacyttemp = idx_bajacyt[idx_bajacyt["TIPO"] == "TEMPORAL"]
#  -------------------INDICADORES EGRESADOS CICLO ANTERIOR
for p in deprog_educ:
    etemp = degresado[degresado["PROG_EDUC"] == p]
    #  Egresados del ciclo
    idx_tmp = pd.DataFrame({
        "MODALIDAD": etemp["MODALIDAD"].max(),
        "NIVEL": etemp["NIVEL"].max(),
        "SISTEMA": etemp["SISTEMA"].max(),
        "PROG_EDUC": p,
        "PLAN": etemp["PLAN"].max(),
        "DIVISION": etemp["DIVISION"].max(),
        "F": matr_egf_pe(etemp),
        "M": matr_egm_pe(etemp),
        "TOTAL": matr_egt_pe(etemp)}, index = [len(idx_egresado)])
    if matr_egt_pe(etemp)!=0:
        idx_egresado = pd.concat([idx_egresado, idx_tmp])
    #  Egresados del ciclo por cohorte
    for c in decohorte:
        idx_tmp = pd.DataFrame({
            "MODALIDAD": etemp["MODALIDAD"].max(),
            "NIVEL": etemp["NIVEL"].max(),
            "SISTEMA": etemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": etemp["PLAN"].max(),
            "DIVISION": etemp["DIVISION"].max(),
            "COHORTE": c,
            "CANT": matr_ce_pe(etemp, c)
            }, index = [len(idx_egresado_cohorte)])
        idx_egresado_cohorte = pd.concat([idx_egresado_cohorte, idx_tmp])
for p in dtprog_educ:
    ttemp = dtitulado[dtitulado["PROG_EDUC"] == p]
    #  Titulados del ciclo
    idx_tmp = pd.DataFrame({
        "MODALIDAD": ttemp["MODALIDAD"].max(),
        "NIVEL": ttemp["NIVEL"].max(),
        "SISTEMA": ttemp["SISTEMA"].max(),
        "PROG_EDUC": p,
        "PLAN": ttemp["PLAN"].max(),
        "DIVISION": ttemp["DIVISION"].max(),
        "F": matr_f_pe(ttemp),
        "M": matr_m_pe(ttemp),
        "TOTAL": matr_t_pe(ttemp)}, index = [len(idx_titulado)])
    if matr_t_pe(ttemp)!=0:
        idx_titulado = pd.concat([idx_titulado, idx_tmp])
    #  Titulados del ciclo por cohorte
    for c in dtcohorte:
        idx_tmp = pd.DataFrame({
            "MODALIDAD": ttemp["MODALIDAD"].max(),
            "NIVEL": ttemp["NIVEL"].max(),
            "SISTEMA": ttemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": ttemp["PLAN"].max(),
            "DIVISION": ttemp["DIVISION"].max(),
            "COHORTE": c,
            "CANT": matr_ct_pe(ttemp, c)
            }, index = [len(idx_titulado_cohorte)])
        idx_titulado_cohorte = pd.concat([idx_titulado_cohorte, idx_tmp])
#  Titulados por modalidad
idx_titulado_modalidad = dtitulado.groupby(["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC","C_EXAM","SEXO"])["MATRICULA"].aggregate("count")
idx_titulado_modalidad = pd.DataFrame(idx_titulado_modalidad)
idx_titulado_modalidad = idx_titulado_modalidad.pivot_table(values = "MATRICULA", index = ["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC"], columns = ["C_EXAM","SEXO"], fill_value = 0).sort_values(by = ["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC"], ascending = [False, True, True, True])
#  ------------------INDICADORES COHORTE CICLO ANTERIOR
for p in dcprog_educ:
    #  Egresados de la cohorte correspondiente a los egresos del ciclo vs NI cohorte
    ctemp = dcohorte[dcohorte["PROG_EDUC"] == p]
    idx_tmp = pd.DataFrame({
            "MODALIDAD": ctemp["MODALIDAD"].max(),
            "NIVEL": ctemp["NIVEL"].max(),
            "SISTEMA": ctemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": ctemp["PLAN"].max(),
            "DIVISION": ctemp["DIVISION"].max(),
            "NI_F": matr_f_pe(ctemp),
            "NI_M": matr_m_pe(ctemp),
            "NI_PE": matr_t_pe(ctemp),
            "EG_F": matr_ef_pe(ctemp),
            "EG_M": matr_em_pe(ctemp),
            "EG_PE": matr_et_pe(ctemp),
            "EFIC_F": indice(matr_f_pe(ctemp), matr_ef_pe(ctemp)),
            "EFIC_M": indice(matr_m_pe(ctemp), matr_em_pe(ctemp)),
            "EFIC_PE": indice(matr_t_pe(ctemp), matr_et_pe(ctemp))}, index=[len(idx_cohorte)])
    if indice(matr_t_pe(ctemp), matr_et_pe(ctemp))!=0:
        idx_cohorte = pd.concat([idx_cohorte, idx_tmp])
    # Egresados de la cohorte que ya se titularon vs egresados de la cohorte
    ctemp = dcohorte[dcohorte["PROG_EDUC"] == p]
    ctemp = ctemp[ctemp['EGRESADO']=='SI']
    idx_tmp = pd.DataFrame({
            "MODALIDAD": ctemp["MODALIDAD"].max(),
            "NIVEL": ctemp["NIVEL"].max(),
            "SISTEMA": ctemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": ctemp["PLAN"].max(),
            "DIVISION": ctemp["DIVISION"].max(),
            "EG_F": matr_f_pe(ctemp),
            "EG_M": matr_m_pe(ctemp),
            "EG_PE": matr_t_pe(ctemp),
            "TI_F": matr_eft_pe(ctemp),
            "TI_M": matr_emt_pe(ctemp),
            "TI_PE": matr_ett_pe(ctemp),
            "EFIC_F": indice(matr_f_pe(ctemp), matr_eft_pe(ctemp)),
            "EFIC_M": indice(matr_m_pe(ctemp), matr_emt_pe(ctemp)),
            "EFIC_PE": indice(matr_t_pe(ctemp), matr_ett_pe(ctemp))}, index=[len(idx_cohorte)])
#    if indice(matr_t_pe(ctemp), matr_ett_pe(ctemp))!=0:
    idx_cohorte_titulado = pd.concat([idx_cohorte_titulado, idx_tmp])
#  ------------------INDICADORES DE TRANSICION POR MODALIDAD Y NIVEL
#  Transición Planes Semestrales (LICENCIATURA)
#  Ciclo anterior semestres 1,3,5,7
#  Ciclo actual semestres 2,4,6,8
dtransicionsem = dtransicion[dtransicion["MODALIDAD"]=="SEMESTRE"]
dtransicionsem = dtransicionsem[dtransicionsem["GRADO"]!=8]
dtransicionsem = dtransicionsem.pivot_table(values = 'MATRICULA', index = ['MODALIDAD','NIVEL','SISTEMA','PROG_EDUC'], columns = ['PERIODO','GRADO'], aggfunc = 'count', fill_value = 0, sort = [False, True, True, True])

#  Transición Planes Cuatrimestrales
#  Ciclo anterior semestres 1,3,5,7,9,11
#  Ciclo actual semestres 2,4,6,8,10,12
dtransicioncuatrim = dtransicion[dtransicion["MODALIDAD"]=="CUATRIMESTRE"]
dtransicioncuatrim = dtransicioncuatrim[dtransicioncuatrim["GRADO"]!=12]
dtransicioncuatrim = dtransicioncuatrim.pivot_table(values = 'MATRICULA', index = ['MODALIDAD','NIVEL','SISTEMA','PROG_EDUC'], columns = ['PERIODO','GRADO'], aggfunc = 'count', fill_value = 0, sort = [False, True, True, True])

#  Creación de las tablas finales para Excel de la información de grado, discapacidades, etnias, nacimiento, procedencia
idx_grupo = dinscrito.groupby(["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "GRADO", "GRUPO"])["MATRICULA"].aggregate("count")
idx_grupo = pd.DataFrame(idx_grupo)
idx_grupo = idx_grupo.pivot_table(values="MATRICULA", index = ["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC","GRUPO"],columns=["GRADO"],fill_value=0).sort_values(by=["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC","GRUPO"], ascending=[False, True, True, True, True])
idx_mdiscap = idx_mdiscap.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["DISCAP", "SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_metnia = idx_metnia.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["ETNIA", "SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_mnacimiento = idx_mnacimiento.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["LUGAR_NAC"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_mprocedencia = idx_mprocedencia.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["PROC_BACH"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_nidiscap = idx_nidiscap.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["DISCAP", "SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_nietnia = idx_nietnia.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["ETNIA", "SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_ninacimiento = idx_ninacimiento.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["LUGAR_NAC"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_niprocedencia = idx_niprocedencia.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["PROC_BACH"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_adiscap = idx_adiscap.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["DISCAP", "SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_aetnia = idx_aetnia.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["ETNIA", "SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_anacimiento = idx_anacimiento.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["LUGAR_NAC"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_aprocedencia = idx_aprocedencia.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["PROC_BACH"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_bajacytdef = idx_bajacytdef.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["CAUSA","SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_bajacyttemp = idx_bajacyttemp.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["CAUSA","SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_egresado_cohorte = idx_egresado_cohorte.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["COHORTE"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_titulado_cohorte = idx_titulado_cohorte.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["COHORTE"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])
idx_egresado_cohorte_sexo = degresado.groupby(["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC","COHORTE","SEXO"])["MATRICULA"].aggregate("count")
idx_egresado_cohorte_sexo = pd.DataFrame(idx_egresado_cohorte_sexo)
idx_egresado_cohorte_sexo = idx_egresado_cohorte_sexo.pivot_table(values = "MATRICULA", index = ["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"], columns=["COHORTE", "SEXO"], fill_value = 0).sort_values(by = ["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"], ascending = [False, True, True, True])
#  Crear tabla de grupos por turno y semestre
idx_grupo_turno_semestre = dinscrito.groupby(["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC","GRUPO","TURNO","GRADO"])["MATRICULA"].aggregate("count")
idx_grupo_turno_semestre = pd.DataFrame(idx_grupo_turno_semestre)
idx_grupo_turno_semestre = idx_grupo_turno_semestre.pivot_table(values = "MATRICULA", index = ["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC","GRUPO"], columns=["TURNO", "GRADO"], fill_value = 0).sort_values(by = ["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC","GRUPO"], ascending = [False, True, True, True, True])
#  Crear tabla de grupos por semestre y sexos
idx_grupo_semestre_sexo = dinscrito.groupby(["MODALIDAD","NIVEL","SISTEMA","PROG_EDUC","GRUPO","GRADO","SEXO"])["MATRICULA"].aggregate("count")
idx_grupo_semestre_sexo = pd.DataFrame(idx_grupo_semestre_sexo)
idx_grupo_semestre_sexo = idx_grupo_semestre_sexo.pivot_table(values = "MATRICULA", index = ["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC","GRUPO"], columns=["GRADO", "SEXO"], fill_value = 0).sort_values(by = ["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC","GRUPO"], ascending = [False, True, True, True, True])
##########  GRAFICOS DEL INFORME  ##########
#  MATRICULA
g = idx_m[idx_m["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Matricula_Sem.png",dpi=300,bbox_inches='tight')
g = idx_m[idx_m["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Matrícula_Cuatim.png",dpi=300,bbox_inches='tight')
#  TURNO
g = idx_mturno[idx_mturno["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["MATUTINO", "VESPERTINO"],
        color = ["skyblue", "orange"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Turno Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Turno_Sem.png",dpi=300,bbox_inches='tight')
g = idx_mturno[idx_mturno["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["MATUTINO", "VESPERTINO"],
        color = ["skyblue", "orange"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Turno Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Turno_Cuatrim.png",dpi=300,bbox_inches='tight')
#  NUEVO INGRESO
g = idx_ni[idx_ni["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["NIF", "NIM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Nuevo Ingreso Semestral",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0,35),
        fontsize=7).get_figure().savefig(destino + nombre + "_NI_Sem.png",dpi=300,bbox_inches='tight')
g = idx_ni[idx_ni["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["NIF", "NIM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Nuevo Ingreso Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        # ylim = (0,30),
        fontsize=7).get_figure().savefig(destino + nombre + "_NI_Cuatrim.png",dpi=300,bbox_inches='tight')
#  APROVECHAMIENTO
g = idx_maprovechamiento[idx_maprovechamiento["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Aprovechamiento Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig(destino + nombre + "_Aprovechamiento_Sem.png",dpi=300,bbox_inches='tight')
g = idx_maprovechamiento[idx_maprovechamiento["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Aprovechamiento Cuatrimestral",
        xlabel="",
        ylim = (0, 100),
        ylabel="Porcentaje",
        fontsize=7).get_figure().savefig(destino + nombre + "_Aprovechamiento_Cuatrim.png",dpi=300,bbox_inches='tight')
#  REPROBACION
g = idx_mreprobacion[idx_mreprobacion["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Reprobación Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Reprobación_Sem.png",dpi=300,bbox_inches='tight')
g = idx_mreprobacion[idx_mreprobacion["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Reprobación Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        # ylim = (0, 25),
        fontsize=7).get_figure().savefig(destino + nombre + "_Reprobación_Cuatrim.png",dpi=300,bbox_inches='tight')
#  DESERCION
g = idx_mdesercion[idx_mdesercion["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["NRI_F", "NRI_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Deserción Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Deserción_Sem.png",dpi=300,bbox_inches='tight')
g = idx_mdesercion[idx_mdesercion["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["NRI_F", "NRI_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Deserción Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Deserción_Cuatrim.png",dpi=300,bbox_inches='tight')
#  BAJAS TEMPORALES
g = idx_bajatemp [idx_bajatemp["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Temporal Semestral",
        xlabel="",
        ylim = (0, 10),
        ylabel="Porcentaje",
        fontsize=7).get_figure().savefig(destino + nombre + "_Baja_Temp_Sem.png",dpi=300,bbox_inches='tight')
g = idx_bajatemp[idx_bajatemp["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Temporal Cuatrimestral",
        xlabel="",
        ylim = (0, 10),
        ylabel="Porcentaje",
        fontsize=7).get_figure().savefig(destino + nombre + "_Baja_Temp_Cuatrim.png",dpi=300,bbox_inches='tight')
#  BAJAS DEFINITIVA
g = idx_bajadef [idx_bajadef["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Definitiva Semestral",
        xlabel="",
        #ylim = (0, 10),
        ylabel="Porcentaje",
        fontsize=7).get_figure().savefig(destino + nombre + "_Baja_Defin_Sem.png",dpi=300,bbox_inches='tight')
g = idx_bajadef[idx_bajadef["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Definitiva Cuatrimestral",
        xlabel="",
        ylim = (0, 10),
        ylabel="Porcentaje",
        fontsize=7).get_figure().savefig(destino + nombre + "_Baja_Defin_Cuatrim.png",dpi=300,bbox_inches='tight')
#  EGRESADOS
g = idx_egresado [idx_egresado["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Egreso Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Egresados_Sem.png",dpi=300,bbox_inches='tight')
g = idx_egresado[idx_egresado["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Egreso Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Egresados_Cuatrim.png", dpi=300, bbox_inches='tight')
#  TITULADOS
g = idx_titulado [idx_titulado["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Titulación Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig(destino + nombre + "_Titulados_Sem.png",dpi=300,bbox_inches='tight')
g = idx_titulado[idx_titulado["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Titulación Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        #ylim = (0, 25),
        fontsize=7).get_figure().savefig(destino + nombre + "_Titulados_Cuatrim.png",dpi=300,bbox_inches='tight')
#  Eliminar columnas innecesarias para los archivos de Excel
idx_m.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_mturno.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_mreprobacion.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_maprovechamiento.drop(["DIVISION", "PLAN"], axis="columns",inplace=True)
idx_cohorte.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_cohorte_titulado.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_atn_dmda.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_ni.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_egresado.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_titulado.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_bajatemp.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_bajadef.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_mdesercion.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
#  se crea la tabla de etnias por P.E. sin sexo
etniape = dinscrito[dinscrito["MATRICULADE"]=="CIERRE"]
etniape = etniape[etniape['ETNIA']!='NINGUNA']
etniape = etniape.groupby(['MODALIDAD','NIVEL','SISTEMA','PROG_EDUC','ETNIA'])['MATRICULA'].aggregate('count')
etniape = pd.DataFrame(etniape)
etniape = etniape.pivot_table(values='MATRICULA', index= ['MODALIDAD','NIVEL','SISTEMA','PROG_EDUC'],columns=['ETNIA'],fill_value=0).sort_values(by=['MODALIDAD','NIVEL','SISTEMA','PROG_EDUC'],ascending=[False,True,True,True])
#  Se crea el archivo de Excel para el informe a la J. D.
writer = pd.ExcelWriter(destino + nombre + ".xlsx")
#  Análisis de la matrícula escolar periodo actual
idx_m.to_excel(writer, sheet_name="matricula")
idx_mturno.to_excel(writer, sheet_name="turno")
idx_mdiscap.to_excel(writer, sheet_name="discap")
etniape.to_excel(writer, sheet_name='etniape')
idx_metnia.to_excel(writer, sheet_name="etnia")
idx_mnacimiento.to_excel(writer, sheet_name = "lugar_nac")
idx_mprocedencia.to_excel(writer, sheet_name = "proc_bach")
idx_grupo_semestre_sexo.to_excel(writer, sheet_name="gpo_sem_sex")
idx_grupo_turno_semestre.to_excel(writer, sheet_name="gpo_turno_sem")
#  Análisis de la matrícula de nuevo ingreso periodo actual
idx_ni.to_excel(writer, sheet_name= "NI")
idx_nidiscap.to_excel(writer, sheet_name = "discap_NI")
idx_nietnia.to_excel(writer, sheet_name = "etnia_NI")
idx_ninacimiento.to_excel(writer, sheet_name = "lugar_nac_NI")
idx_niprocedencia.to_excel(writer, sheet_name = "proc_bach_NI")
#  Análisis de la matrícula actual en el periodo inmediato anterior
idx_maprovechamiento.to_excel(writer, sheet_name = "aprovechamiento")
idx_mreprobacion.to_excel(writer, sheet_name = "reprobación")
idx_mdesercion.to_excel(writer, sheet_name = "deserción")
#  Análisis del proceso de admisión periodo actual
idx_atn_dmda.to_excel(writer, sheet_name = "atn_demanda")
idx_adiscap.to_excel(writer, sheet_name = "discap_aspirante")
idx_aetnia.to_excel(writer, sheet_name = "etnia_aspirante")
idx_anacimiento.to_excel(writer, sheet_name = "lugar_nac_aspirantes")
idx_aprocedencia.to_excel(writer, sheet_name = "proc_bach_aspirantes")
#  Transicion programas educativos
dtransicionsem.to_excel(writer, sheet_name = "trans_sem")
dtransicioncuatrim.to_excel(writer, sheet_name = "trans_cuatrim")
#  Análisis de las bajas periodo solicitado
if len(idx_bajacyttemp)!=0:
    idx_bajatemp.to_excel(writer, sheet_name = "ind_baja_temp")
if len(idx_bajadef)!=0:
    idx_bajadef.to_excel(writer, sheet_name = "ind_baja_def")
if len(idx_bajacyttemp)!=0:
    idx_bajacyttemp.to_excel(writer, sheet_name = "clasif_baja_temp")
if len(idx_bajacytdef)!=0:
    idx_bajacytdef.to_excel(writer, sheet_name = "clasif_baja_def")
#  Análisis de la matrícula de egresados ciclo inmediato anterior
idx_egresado.to_excel(writer, sheet_name = "egresado_PE")
idx_egresado_cohorte.to_excel(writer, sheet_name = "egresado_cohorte")
idx_egresado_cohorte_sexo.to_excel(writer, sheet_name = "egresado_cohorte_sexo")
#  Análisis de la matrícula de titulados periodo solicitado
idx_titulado.to_excel(writer, sheet_name = "titulado_PE")
idx_titulado_cohorte.to_excel(writer, sheet_name = "titulado_cohorte")
idx_titulado_modalidad.to_excel(writer, sheet_name = "titulado_modalidad")
#  Análisis de la cohorte ciclo inmediato anterior
idx_cohorte.to_excel(writer, sheet_name = "efic_terminal")
idx_cohorte_titulado.to_excel(writer, sheet_name = "efic_terminal_vs_titulados")
#  Datos origen indicadores
dinscrito.to_excel(writer, sheet_name="inscrito")
dadmision.to_excel(writer, sheet_name="admision")
ddesercion.to_excel(writer, sheet_name="desercion")
dbaja.to_excel(writer, sheet_name="baja")
degresado.to_excel(writer, sheet_name="egresado")
dtitulado.to_excel(writer, sheet_name="titulado")
dcohorte.to_excel(writer, sheet_name="cohorte")
writer.close()
