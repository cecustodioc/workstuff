# -*- coding: utf-8 -*-
"""
Creado 08/06/2022 14:03
@author: Carlos Ernesto Custodio Cadena
Cálcular los indicadores escolares tomando como entrada csv
Última revisión: 21/06/2022
"""
import pandas as pd

#  Se leen todos los origenes de datos del informe Junta Directiva y DGESU
dinscrito = pd.read_csv("inscrito.csv", encoding="unicode escape")
#  CIERRE solo alumnos vigentes, APERTURA todos los que se inscribieron inicialmente
#  para el informe DGESU y 911 la matricula de interés es la de CIERRE para los
#  informes de la JD en ocasiones es de interés la matrícula de APERTURA
dinscrito = dinscrito[dinscrito["MATRICULADE"]=="CIERRE"]
dadmision = pd.read_csv("admision.csv", encoding="unicode escape")
dabandono = pd.read_csv("abandono.csv", encoding="unicode escape")
dbaja = pd.read_csv("baja.csv", encoding="unicode escape")
ddesercion = pd.read_csv("desercion.csv", encoding="unicode escape")
dcohorte = pd.read_csv("cohorte.csv", encoding="unicode escape")
degresado = pd.read_csv("egresado.csv", encoding="unicode escape")
dtitulado = pd.read_csv("titulado.csv", encoding="unicode escape")

#  Se ordenan los DataFrames obtenidos
dinscrito = dinscrito.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "GRADO", "SEXO"],
    ascending=[False, True, True, True, True, True])
dadmision = dadmision.sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC", "SEXO"],
    ascending=[False, True, True, True, True])
dabandono = dabandono.sort_values(
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
inacimiento = tuple(dinscrito["LUGAR_NAC"])
iprocedencia = tuple(dinscrito["PROC_BACH"])
adiscap = tuple(dadmision["DISCAPACIDAD"])
aetnia = tuple(dadmision["ETNIA"])
anacimiento = tuple(dadmision["LUGAR_NAC"])
aprocedencia = tuple(dadmision["PROC_BACH"])
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


def matr_regf_pe(prog_educ, sem):
    prog_educ = prog_educ[prog_educ["SEXO"] == "F"]
    prog_educ = prog_educ[prog_educ["INSCRITO"] == "SI"]
    prog_educ = prog_educ[prog_educ["GRADO"] == sem]
    matricula_cf = prog_educ["MATRICULA"].count()
    return matricula_cf


def matr_regm_pe(prog_educ, sem):
    prog_educ = prog_educ[prog_educ["SEXO"] == "M"]
    prog_educ = prog_educ[prog_educ["INSCRITO"] == "SI"]
    prog_educ = prog_educ[prog_educ["GRADO"] == sem]
    matricula_cm = prog_educ["MATRICULA"].count()
    return matricula_cm


def matr_regt_pe(prog_educ, sem):
    prog_educ = prog_educ[prog_educ["INSCRITO"] == "SI"]
    prog_educ = prog_educ[prog_educ["GRADO"] == sem]
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
   prog_educ = prog_educ[prog_educ["LUGAR_NAC"] == nac]
   n_l_n = prog_educ["MATRICULA"].count()
   return n_l_n


def contar_proc_bach(prog_educ, bac):
   prog_educ = prog_educ[prog_educ["PROC_BACH"] == bac]
   n_p_b = prog_educ["MATRICULA"].count()
   return n_p_b


def contar_alugar_nac(prog_educ, nac):
   prog_educ = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
   prog_educ = prog_educ[prog_educ["LUGAR_NAC"] == nac]
   n_l_n = prog_educ["MATRICULA"].count()
   return n_l_n


def contar_aproc_bach(prog_educ, bac):
   prog_educ = prog_educ[prog_educ["ESTATUS"] == "ACEPTADO"]
   prog_educ = prog_educ[prog_educ["PROC_BACH"] == bac]
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
        "NI_F":[],
        "NI_M":[],
        "NI_T":[],
        "F": [],
        "M": [],
        "TOTAL": [],
        "ID_F": [],
        "ID_M": [],
        "ID_PROG_EDUC": []})

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

idx_mgrado = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "GRADO": [],
        "SEXO": [],
        "CANT": []})

idx_mgrupo = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "GRADO": [],
        "GRUPO": [],
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

idx_mabandono = pd.DataFrame({
        "MODALIDAD": [],
        "NIVEL": [],
        "SISTEMA": [],
        "PROG_EDUC": [],
        "PLAN": [],
        "DIVISION": [],
        "F": [],
        "M": [],
        "TOTAL": [],
        "I_AB_FEM": [],
        "I_AB_MASC": [],
        "I_AB_PE": []})

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
    #  itemp = itemp[itemp["MATRICULADE"] == "CIERRE"] #  Evita que se presenten datos de alumnos que se dieron de baja en el informe
    atemp = dadmision[dadmision["PROG_EDUC"] == p]
    abtemp = dabandono[dabandono["PROG_EDUC"] == p]
    dtemp = ddesercion[ddesercion["PROG_EDUC"] == p]
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
    #  Matrícula por grado
    for g in digrado:
        for s in disexo:
            idx_tmp = pd.DataFrame({
                    "MODALIDAD": itemp["MODALIDAD"].max(),
                    "NIVEL": itemp["NIVEL"].max(),
                    "SISTEMA": itemp["SISTEMA"].max(),
                    "PROG_EDUC": p,
                    "PLAN": itemp["PLAN"].max(),
                    "DIVISION": itemp["DIVISION"].max(),
                    "GRADO": g,
                    "SEXO": s,
                    "CANT": contar_grado(itemp, g, s)}, index=[len(idx_mgrado)])
            idx_mgrado = pd.concat([idx_mgrado,idx_tmp])
    #  Matrícula por grupo
    for d in digrado:
        mgrupo = itemp[itemp["GRADO"] == d]
        imgrupo = tuple(mgrupo["GRUPO"])
        dimgrupo = crea_idx(imgrupo)
        if dimgrupo != []:
            for g in dimgrupo:
                t_a_gpo = contar_t_gpo(itemp, d, g)
                for s in disexo:
                    if s == "F":
                        t_f_gpo = contar_s_gpo(itemp, d, g, s)
                    else:
                        t_m_gpo = contar_s_gpo(itemp, d, g, s)
                idx_tmp = pd.DataFrame({
                        "MODALIDAD": itemp["MODALIDAD"].max(),
                        "NIVEL": itemp["NIVEL"].max(),
                        "SISTEMA": itemp["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itemp["PLAN"].max(),
                        "DIVISION": itemp["DIVISION"].max(),
                        "GRADO": d,
                        "GRUPO": g,
                        "F": t_f_gpo,
                        "M": t_m_gpo,
                        "TOTAL": t_a_gpo}, index=[len(idx_mgrupo)])
                idx_mgrupo = pd.concat([idx_mgrupo, idx_tmp])
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
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
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
                        "MODALIDAD": itemp["MODALIDAD"].max(),
                        "NIVEL": itemp["NIVEL"].max(),
                        "SISTEMA": itemp["SISTEMA"].max(),
                        "PROG_EDUC": p,
                        "PLAN": itemp["PLAN"].max(),
                        "DIVISION": itemp["DIVISION"].max(),
                        "DISCAP": d,
                        "SEXO": s,
                        "CANT": contar_discap(itempadm, d, s)}, index=[len(idx_nidiscap)])
                idx_nidiscap = pd.concat([idx_nidiscap, idx_tmp])
    #  Matrícula por etnia nuevo ingreso
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
                        "CANT": contar_etnia(itempadm, e, s)}, index=[len(idx_nietnia)])
                idx_nietnia = pd.concat([idx_nietnia, idx_tmp])
    #  Matrícula por lugar de nacimiento nuevo ingreso
    for ln in dinacimiento:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itemp["MODALIDAD"].max(),
                "NIVEL": itemp["NIVEL"].max(),
                "SISTEMA": itemp["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itemp["PLAN"].max(),
                "DIVISION": itemp["DIVISION"].max(),
                "LUGAR_NAC": ln,
                "CANT": contar_lugar_nac(itempadm, ln)}, index=[len(idx_ninacimiento)])
        idx_ninacimiento = pd.concat([idx_ninacimiento, idx_tmp])
    #  Matrícula por procedencia de bachiller nuevo ingreso
    for pb in diprocedencia:
        idx_tmp = pd.DataFrame({
                "MODALIDAD": itemp["MODALIDAD"].max(),
                "NIVEL": itemp["NIVEL"].max(),
                "SISTEMA": itemp["SISTEMA"].max(),
                "PROG_EDUC": p,
                "PLAN": itemp["PLAN"].max(),
                "DIVISION": itemp["DIVISION"].max(),
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

    #  ------------------INDICADORES ABANDONO CICLO ACTUAL
    #  Abandono: alumnos inscritos ciclo anterior no reinscritos al actual
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "F": matr_f_pe(abtemp),
            "M": matr_m_pe(abtemp),
            "TOTAL": matr_t_pe(abtemp),
            "I_AB_FEM": indice(matr_f_pe(itemp), matr_f_pe(abtemp)),
            "I_AB_MASC": indice(matr_m_pe(itemp), matr_m_pe(abtemp)),
            "I_AB_PE": indice(matr_t_pe(itemp), matr_t_pe(abtemp))}, index=[len(idx_mabandono)])
    if indice(matr_f_pe(itemp), matr_f_pe(abtemp))!=0 or indice(matr_m_pe(itemp), matr_m_pe(abtemp))!=0:
        idx_mabandono = pd.concat([idx_mabandono, idx_tmp])

    #  ------------------INDICADORES DESERCION CICLO ACTUAL
    #  Deserción: Alumnos NI año anterior no inscritos en 3ro ciclo actual
    if itemp["MODALIDAD"].max() == "CUATRIMESTRE":
        sem = 4
    else:
        sem = 3
    idx_tmp = pd.DataFrame({
            "MODALIDAD": itemp["MODALIDAD"].max(),
            "NIVEL": itemp["NIVEL"].max(),
            "SISTEMA": itemp["SISTEMA"].max(),
            "PROG_EDUC": p,
            "PLAN": itemp["PLAN"].max(),
            "DIVISION": itemp["DIVISION"].max(),
            "NI_F": matr_f_pe(dtemp),
            "NI_M": matr_m_pe(dtemp),
            "NI_T": matr_t_pe(dtemp),
            "F": matr_f_pe(dtemp) - matr_regf_pe(dtemp, sem),
            "M": matr_m_pe(dtemp) - matr_regm_pe(dtemp, sem),
            "TOTAL": matr_t_pe(dtemp) - matr_regt_pe(dtemp, sem),
            "ID_F": round(indice(matr_f_pe(dtemp), matr_f_pe(dtemp) - matr_regf_pe(dtemp, sem)), 2),
            "ID_M": round(indice(matr_m_pe(dtemp), matr_m_pe(dtemp) - matr_regm_pe(dtemp, sem)), 2),
            "ID_PROG_EDUC": indice(matr_t_pe(dtemp), matr_t_pe(dtemp) - matr_regt_pe(dtemp, sem))},index = [len(idx_mdesercion)])
    if matr_t_pe(dtemp) !=0:
        idx_mdesercion = pd.concat([idx_mdesercion, idx_tmp])
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
    if indice(matr_f_pe(itemp), matr_f_pe(bdtemp))!=0 or  indice(matr_m_pe(itemp), matr_m_pe(bdtemp))!=0:
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
    if indice(matr_f_pe(itemp), matr_f_pe(bttemp))!=0 or indice(matr_m_pe(itemp), matr_m_pe(bttemp))!=0:
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
    #  En caso de que la JD solicite solo los que tienen titulo en mano
    #  ttemp = ttemp[ttemp["TITU_ENTREGA"]!="NO"]
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

#  ------------------INDICADORES COHORTE CICLO ANTERIOR
for p in dcprog_educ:
    ctemp = dcohorte[dcohorte["PROG_EDUC"] == p]
    #  Egresados de la cohorte correspondiente a los egresos del ciclo
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

#  Creación de las tablas finales para Excel de la información de grado, discapacidades, etnias, nacimiento, procedencia
idx_mgrado = idx_mgrado.pivot_table(
    values="CANT",
    index=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    columns=["GRADO", "SEXO"]).sort_values(
    by=["MODALIDAD", "NIVEL", "SISTEMA", "PROG_EDUC"],
    ascending=[False, True, True, True])

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

#  MATRICULA
g = idx_m[idx_m["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Escolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_MESem.png",dpi=300,bbox_inches='tight')

g = idx_m[idx_m["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Semiescolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_MSS.png",dpi=300,bbox_inches='tight')

g= idx_m[idx_m["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula SemiEscolarizado Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_MSC.png",dpi=300,bbox_inches='tight')

g = idx_m[idx_m["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Posgrado",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_MP.png",dpi=300,bbox_inches='tight')

#  TURNO
g = idx_mturno[idx_mturno["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["MATUTINO", "VESPERTINO"],
        color = ["skyblue", "orange"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Turno Escolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_MTES.png",dpi=300,bbox_inches='tight')

g = idx_mturno[idx_mturno["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["MATUTINO", "VESPERTINO"],
        color = ["skyblue", "orange"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Turno Semiescolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_MTSS.png",dpi=300,bbox_inches='tight')

g= idx_mturno[idx_mturno["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["MATUTINO", "VESPERTINO"],
        color = ["skyblue", "orange"],
        kind="bar",
        figsize=(8, 5),
        title="Matrícula Turno Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_MTSC.png",dpi=300,bbox_inches='tight')

g = idx_mturno[idx_mturno["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["MATUTINO", "VESPERTINO"],
        color = ["skyblue", "orange"],
        kind = "bar",
        figsize = (8, 5),
        title = "Matrícula Turno Posgrado",
        xlabel = "",
        ylabel = "Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_MTP.png",dpi=300,bbox_inches='tight')

#  NUEVO INGRESO
g = idx_ni[idx_ni["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
       x="PLAN",
       y=["NIF", "NIM"],
       color = ["hotpink", "deepskyblue"],
       kind="bar",
       figsize=(8, 5),
       title="Nuevo Ingreso Escolarizado Semestral",
       xlabel="",
       ylabel="Matrícula",
       fontsize=7).get_figure().savefig("2022_2T_NIES.png",dpi=300,bbox_inches='tight')

g = idx_ni[idx_ni["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["NIF", "NIM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Nuevo Ingreso Semiescolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de pocos datos
        fontsize=7).get_figure().savefig("2022_2T_NISS.png",dpi=300,bbox_inches='tight')

g= idx_ni[idx_ni["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["NIF", "NIM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Nuevo Ingreso SemiEscolarizado Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 25),  #  Activar si la gráfica es de pocos datos
        fontsize=7).get_figure().savefig("2022_2T_NISC.png",dpi=300,bbox_inches='tight')

g = idx_ni[idx_ni["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["NIF", "NIM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Nuevo Ingreso Posgrado",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_NIP.png",dpi=300,bbox_inches='tight')

#  ATENCION A LA DEMANDA
g = idx_atn_dmda[idx_atn_dmda["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
       x="PLAN",
       y=["IADF", "IADM"],
       color = ["hotpink", "deepskyblue"],
       kind="bar",
       figsize=(8, 5),
       title="Atención a la Demanda Escolarizado Semestral",
       xlabel="",
       ylabel="Matrícula",
       fontsize=7).get_figure().savefig("2022_2T_ADES.png",dpi=300,bbox_inches='tight')

g = idx_atn_dmda[idx_atn_dmda["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IADF", "IADM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Atención a la Demanda Semiescolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        #  ylim = (0, 5),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_ADSS.png",dpi=300,bbox_inches='tight')

g= idx_atn_dmda[idx_atn_dmda["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IADF", "IADM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Atención a la Demanda SemiEscolarizado Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_ADSC.png",dpi=300,bbox_inches='tight')

g = idx_atn_dmda[idx_atn_dmda["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IADF", "IADM"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Atención a la Demanda Posgrado",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_ADP.png",dpi=300,bbox_inches='tight')

#  APROVECHAMIENTO
g = idx_maprovechamiento[idx_maprovechamiento["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Aprovechamiento Escolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_AES.png",dpi=300,bbox_inches='tight')

g = idx_maprovechamiento[idx_maprovechamiento["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Aprovechamiento Semiescolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_ASS.png",dpi=300,bbox_inches='tight')

g= idx_maprovechamiento[idx_maprovechamiento["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Aprovechamiento Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_ASC.png",dpi=300,bbox_inches='tight')

g = idx_maprovechamiento[idx_maprovechamiento["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
       x="PLAN",
       y=["F", "M"],
       color = ["hotpink", "deepskyblue"],
       kind="bar",
       figsize=(8, 5),
       title="Aprovechamiento Posgrado",
       xlabel="",
       ylabel="Porcentaje",
       ylim = (0, 100),
       fontsize=7).get_figure().savefig("2022_2T_AP.png",dpi=300,bbox_inches='tight')

#  REPROBACION
g = idx_mreprobacion[idx_mreprobacion["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IR_F", "IR_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Reprobación Escolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_RES.png",dpi=300,bbox_inches='tight')

g = idx_mreprobacion[idx_mreprobacion["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IR_F", "IR_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Reprobación Semiescolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_RSS.png",dpi=300,bbox_inches='tight')

g= idx_mreprobacion[idx_mreprobacion["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IR_F", "IR_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Reprobación Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_RSC.png",dpi=300,bbox_inches='tight')

g = idx_mreprobacion[idx_mreprobacion["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IR_F", "IR_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Reprobación Posgrado",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_RP.png",dpi=300,bbox_inches='tight')

#  DESERCION
g = idx_mdesercion[idx_mdesercion["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["ID_F", "ID_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Deserción Escolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_DES.png",dpi=300,bbox_inches='tight')

g = idx_mdesercion[idx_mdesercion["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["ID_F", "ID_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Deserción Semiescolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_DSS.png",dpi=300,bbox_inches='tight')

g= idx_mdesercion[idx_mdesercion["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["ID_F", "ID_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Deserción Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_DSC.png",dpi=300,bbox_inches='tight')

g = idx_mdesercion[idx_mdesercion["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["ID_F", "ID_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Deserción Posgrado",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_DP.png",dpi=300,bbox_inches='tight')

#  ABANDONO
g = idx_mabandono[idx_mabandono["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["I_AB_FEM", "I_AB_MASC"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Abandono Escolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_ABES.png",dpi=300,bbox_inches='tight')

g = idx_mabandono[idx_mabandono["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["I_AB_FEM", "I_AB_MASC"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Abandono Semiescolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_ABSS.png",dpi=300,bbox_inches='tight')

g= idx_mabandono[idx_mabandono["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["I_AB_FEM", "I_AB_MASC"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Abandono Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_ABSC.png",dpi=300,bbox_inches='tight')

g = idx_mabandono[idx_mabandono["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["I_AB_FEM", "I_AB_MASC"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Abandono Posgrado",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_ABP.png",dpi=300,bbox_inches='tight')

#  BAJAS TEMPORALES
g = idx_bajatemp [idx_bajatemp["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Temporal Escolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_BTES.png",dpi=300,bbox_inches='tight')

g = idx_bajatemp[idx_bajatemp["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Temporal Semiescolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_BTSS.png",dpi=300,bbox_inches='tight')

g= idx_bajatemp[idx_bajatemp["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Temporal Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_BTSC.png",dpi=300,bbox_inches='tight')

g = idx_bajatemp[idx_bajatemp["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Temporal Posgrado",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_BTP.png",dpi=300,bbox_inches='tight')

#  BAJAS DEFINITIVA
g = idx_bajadef [idx_bajadef["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Definitiva Escolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_BDES.png",dpi=300,bbox_inches='tight')

g = idx_bajadef[idx_bajadef["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
       x="PLAN",
       y=["IB_F", "IB_M"],
       color = ["hotpink", "deepskyblue"],
       kind="bar",
       figsize=(8, 5),
       title="Baja Definitiva Semiescolarizado Semestral",
       xlabel="",
       ylabel="Porcentaje",
       ylim = (0, 100),
       fontsize=7).get_figure().savefig("2022_2T_BDSS.png",dpi=300,bbox_inches='tight')

g= idx_bajadef[idx_bajadef["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Definitiva Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_BDSC.png",dpi=300,bbox_inches='tight')

g = idx_bajadef[idx_bajadef["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["IB_F", "IB_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Baja Definitiva Posgrado",
        xlabel="",
        ylabel="Porcentaje",
        ylim = (0, 100),
        fontsize=7).get_figure().savefig("2022_2T_BDP.png",dpi=300,bbox_inches='tight')

#  EGRESADOS
g = idx_egresado [idx_egresado["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Egreso Escolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_EGES.png",dpi=300,bbox_inches='tight')

g = idx_egresado[idx_egresado["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
       x="PLAN",
       y=["F", "M"],
       color = ["hotpink", "deepskyblue"],
       kind="bar",
       figsize=(8, 5),
       title="Egreso Semiescolarizado Semestral",
       xlabel="",
       ylabel="Matrícula",
       ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
       fontsize=7).get_figure().savefig("2022_2T_EGSS.png",dpi=300,bbox_inches='tight')

g= idx_egresado[idx_egresado["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Egreso Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        fontsize=7).get_figure().savefig("2022_2T_EGSC.png",dpi=300,bbox_inches='tight')

g = idx_egresado[idx_egresado["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Egreso Posgrado",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_EGP.png",dpi=300,bbox_inches='tight')

#  TITULADOS
g = idx_titulado [idx_titulado["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Titulación Escolarizado Semestral",
        xlabel="",
        ylabel="Matrícula",
        #  ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_TES.png",dpi=300,bbox_inches='tight')

g = idx_titulado[idx_titulado["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
       x="PLAN",
       y=["F", "M"],
       color = ["hotpink", "deepskyblue"],
       kind="bar",
       figsize=(8, 5),
       title="Titulación Semiescolarizado Semestral",
       xlabel="",
       ylabel="Matrícula",
       ylim = (0, 5),  #  Activar si la gráfica es de menos de 5 datos
       fontsize=7).get_figure().savefig("2022_2T_TSS.png",dpi=300,bbox_inches='tight')

g= idx_titulado[idx_titulado["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Titulación Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Matrícula",
        #  ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_TSC.png",dpi=300,bbox_inches='tight')

g = idx_titulado[idx_titulado["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["F", "M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Titulación Posgrado",
        xlabel="",
        ylabel="Matrícula",
        ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_TP.png",dpi=300,bbox_inches='tight')

#  EFICIENCIA TERMINAL
g = idx_cohorte [idx_cohorte["SISTEMA"] == "ESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["EFIC_F", "EFIC_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Eficiencia Terminal Escolarizado Semestral",
        xlabel="",
        ylabel="Porcentaje",
        fontsize=7).get_figure().savefig("2022_2T_ETES.png",dpi=300,bbox_inches='tight')

g = idx_cohorte[idx_cohorte["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "SEMESTRE"]
if len(g)!=0:
    g.plot(
       x="PLAN",
       y=["EFIC_F", "EFIC_M"],
       color = ["hotpink", "deepskyblue"],
       kind="bar",
       figsize=(8, 5),
       title="Eficiencia Terminal Semiescolarizado Semestral",
       xlabel="",
       ylabel="Porcentaje",
       fontsize=7).get_figure().savefig("2022_2T_ETSS.png",dpi=300,bbox_inches='tight')

g= idx_cohorte[idx_cohorte["SISTEMA"] == "SEMIESCOLARIZADO"]
g = g[g["NIVEL"] == "LICENCIATURA"]
g = g[g["MODALIDAD"] == "CUATRIMESTRE"]
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["EFIC_F", "EFIC_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Eficiencia Terminal Semiescolarizado Cuatrimestral",
        xlabel="",
        ylabel="Porcentaje",
        #  ylim = (0, 10),  #  Activar si la gráfica es de menos de 5 datos
        fontsize=7).get_figure().savefig("2022_2T_ETSC.png",dpi=300,bbox_inches='tight')

g = idx_cohorte[idx_cohorte["NIVEL"] == "MAESTRIA"]  #  Se grafican juntos por ser pocos
if len(g)!=0:
    g.plot(
        x="PLAN",
        y=["EFIC_F", "EFIC_M"],
        color = ["hotpink", "deepskyblue"],
        kind="bar",
        figsize=(8, 5),
        title="Eficiencia Terminal Posgrado",
        xlabel="",
        ylabel="Porcentaje",
        fontsize=7).get_figure().savefig("2022_2T_ETP.png",dpi=300,bbox_inches='tight')

#  Eliminar columnas innecesarias para los archivos de Excel
idx_m.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_mturno.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_mreprobacion.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_maprovechamiento.drop(["DIVISION", "PLAN"], axis="columns",inplace=True)
idx_mgrupo.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_cohorte.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_mabandono.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_atn_dmda.drop(["DIVISION", "PLAN"],axis="columns", inplace=True)
idx_dgesu.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_ni.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_egresado.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_titulado.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_bajatemp.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_bajadef.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)
idx_mdesercion.drop(["DIVISION", "PLAN"], axis="columns", inplace=True)

#  Se crea el archivo de Excel para el informe DGESU e informe a la J. D.
writer = pd.ExcelWriter("2022_2T_DGESU_JD.xlsx")

#  Análisis de la matrícula escolar periodo actual
idx_m.to_excel(writer, sheet_name="matricula")
idx_mgrado.to_excel(writer, sheet_name="grado")
idx_mgrupo.to_excel(writer, sheet_name="grupo")
idx_mturno.to_excel(writer, sheet_name="turno")
idx_mdiscap.to_excel(writer, sheet_name="discapacidad")
idx_metnia.to_excel(writer, sheet_name="etnia")
idx_mnacimiento.to_excel(writer, sheet_name = "lugar_nac")
idx_mprocedencia.to_excel(writer, sheet_name = "procedencia_bach")
#  Análisis de la matrícula de nuevo ingreso periodo actual
idx_ni.to_excel(writer, sheet_name= "nuevo_ingreso")
idx_nidiscap.to_excel(writer, sheet_name = "discapacidad_NI")
idx_nietnia.to_excel(writer, sheet_name = "etnia_NI")
idx_ninacimiento.to_excel(writer, sheet_name = "lugar_nac_NI")
idx_niprocedencia.to_excel(writer, sheet_name = "procedencia_bach_NI")
#  Análisis de la matrícula actual en el periodo inmediato anterior
idx_maprovechamiento.to_excel(writer, sheet_name = "aprovechamiento")
idx_mreprobacion.to_excel(writer, sheet_name = "reprobación")
idx_mdesercion.to_excel(writer, sheet_name = "deserción")
idx_mabandono.to_excel(writer, sheet_name = "abandono_escolar")
#  Análisis del proceso de admisión periodo actual
idx_atn_dmda.to_excel(writer, sheet_name = "atencion_demanda")
idx_adiscap.to_excel(writer, sheet_name = "discap_aspirante")
idx_aetnia.to_excel(writer, sheet_name = "etnia_aspirante")
idx_anacimiento.to_excel(writer, sheet_name = "lugar_nac_aspirantes")
idx_aprocedencia.to_excel(writer, sheet_name = "procedencia_bach_aspirantes")
#  Análisis de las bajas periodo solicitado
idx_bajatemp.to_excel(writer, sheet_name = "indice_baja_temporal")
idx_bajadef.to_excel(writer, sheet_name = "indice_baja_definitiva")
idx_bajacyttemp.to_excel(writer, sheet_name = "clasif_bajas_temp")
idx_bajacytdef.to_excel(writer, sheet_name = "clasif_bajas_def")
#  Análisis de la matrícula de egresados ciclo inmediato anterior
idx_egresado.to_excel(writer, sheet_name = "egresado_PE")
idx_egresado_cohorte.to_excel(writer, sheet_name = "egresado_cohorte")
#  Análisis de la matrícula de titulados periodo solicitado
idx_titulado.to_excel(writer, sheet_name = "titulado_PE")
idx_titulado_cohorte.to_excel(writer, sheet_name = "titulado_cohorte")
#  Análisis de la cohorte ciclo inmediato anterior
idx_cohorte.to_excel(writer, sheet_name = "eficiencia_terminal")
#  Informe DGESU periodo actual
idx_dgesu.to_excel(writer, sheet_name="DGESU")
#  Datos origen de los 911, DGESU e indicadores
dinscrito.to_excel(writer, sheet_name="inscrito")
dadmision.to_excel(writer, sheet_name="admision")
#  Datos origen para indicadores
ddesercion.to_excel(writer, sheet_name="desercion")
dabandono.to_excel(writer, sheet_name="abandono")
dbaja.to_excel(writer, sheet_name="baja")
degresado.to_excel(writer, sheet_name="egresado")
dtitulado.to_excel(writer, sheet_name="titulado")
dcohorte.to_excel(writer, sheet_name="cohorte")
writer.save()