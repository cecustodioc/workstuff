# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:31:48 2024

@author: Carlos Ernesto Custodio Cadena
"""
# importar las librerias de trabajo
import pandas as pd
import cx_Oracle
# crear la estructura de almacenamiento de los datos
resultado = pd.DataFrame({
    'NO': [],
    'NOMBRE': [],
    'MATRICULA': [],
    'CARRERA': [],
    'ESTATUS': []
    })
# configurar la conexión a Oracle
servidor = '999.999.999.999'
puerto = 9999
identificador = 'xxxxxxxx'
usuario = input('Usuario: ')
contrasena = input('Password: ')
midsn = cx_Oracle.makedsn(host = servidor, port = puerto, sid = identificador)
# leer el archivo con los datos
datos = pd.read_excel('archivo_origen.xlsx')
# obtener las matrículas a consultar
matriculas = datos['MATRICULA']
# fijar el ciclo de la consulta
ciclo = "202401"
# inicializar la variable de las matrículas
matricula = ""
# hacer el ciclo de las consultas
for d in matriculas:
    matricula = d
    itemp = datos[datos['MATRICULA']==d]
    conn = cx_Oracle.connect(user = usuario, password = contrasena, dsn = midsn)
    c = conn.cursor()
    consulta = "select case esta_inscrito(a.matricula, a.plan, a.tipoplan, '" + ciclo + "') when 1 then 'Inscrito' else 'No inscrito' end || ' ' || case es_regular(a.matricula) when 1 then 'regular' else 'irregular' end || ' ' || case plan_completo(a.matricula, a.plan) when 1 then 'egresado' || ' el ' || cc.termina else '' end || case a.status when 4 then 'baja' else '' end as estado from alumnos a inner join carreras c on c.carrera = a.carrera left join ciclos cc on cc.ciclo=periodo_ultimo(a.matricula,a.plan) and cc.tipoplan=a.tipoplan where matricula = '" + matricula + "'"
    c.execute(consulta)
    for r in c:
        # localizar la fila de la matricula en datos y crear una nueva tabla con los resultados de la consulta a la base de datos
        idx_tmp = pd.DataFrame({
            'NO': itemp['NO'].max(),
            'NOMBRE': itemp['NOMBRE'].max(),
            'MATRICULA': matricula,
            'CARRERA': itemp['CARRERA'].max(),
            'ESTATUS': str(r[0])
          }, index=[len(resultado)])
        resultado = pd.concat([resultado, idx_tmp])
    conn.close()
# quitar el índice a los resultados
resultado = resultado.set_index('NO')
# guardar los resultados en un nuevo archivo formato xslx
archivo = pd.ExcelWriter('archivo_salida.xlsx')
resultado.to_excel(archivo,'becados')
archivo.close()
