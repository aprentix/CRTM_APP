from exceptions_app import ErrorArchivos, ErrorNombreColumnas
import script_generar_final as sgf
import script_subir_archivos as ssa 
import sys
import pandas as pd
import re
import os


def programa_final(diccionario_archivos):
    print("//////////////////////////////PRUEBAS DE SCRIPT FINAL//////////////////////////////")
    try:
        ssa.comprobar_nombres_columnas(diccionario_archivos)
    except ErrorNombreColumnas as e:
        print("Revise los nombres de las columnas: ")
        print(e)
        return -1
    print("OK NOMBRES")
    print("EMPIEZA LA CARGA DE ARCHIVOS")
    try:
        datos_base, datos_via, datos_bit, datos_vac_app, datos_vac_val = ssa.leer_archivos(diccionario_archivos)
    except ErrorArchivos as e:
        print(e)
        return -1
    print("OK CARGA ARCHIVOS")

    datos_VAC_OK = ssa.procesar_vac_app(datos_vac_val, datos_vac_app)
    print("OK VAC")
    datos_BIT_OK = ssa.procesar_bit(datos_bit)
    print("OK BIT")
    datos_VIA_OK = ssa.procesar_via(datos_via)
    print("OK VIA")
    datos_BASE_OK = ssa.proceso_base(datos_base)
    print("OK BASE")
    interurbanos_vcm, interurbanos_vac, vacs = ssa.lista_final(datos_VIA_OK, datos_VAC_OK, datos_BIT_OK, datos_BASE_OK)
    print("OK LISTAS INICIALES")
    interurbanos_vcm_decision, interurbanos_vac_decision, vacs_decision = sgf.construir_tabla_decisiones(interurbanos_vcm, interurbanos_vac, vacs)
    print("OK LISTAS DECISIONES")

    return interurbanos_vcm_decision, interurbanos_vac_decision, vacs_decision

if __name__ == "__main__":
    # directorios = {
    #     "datos_base":"./2023-09/2023-09 DATOS_BASE.xlsx",
    #     "datos_via":"./2023-09/2023-09 DATOS_VIA.xlsx",
    #     "datos_bit":"./2023-09/2023-09 InformeBIT.xlsx",
    #     "datos_vac_app":"./2023-09/2023-09Vac_app.xlsx",
    #     "datos_vac_val":"./2023-09/2023-09Vac_val.xlsx"
    # }
    directorios = dict()
    for file_name in sys.argv:
        if re.search(r".*BIT.*",file_name) != None:
            directorios['datos_bit']=os.path.abspath(file_name)
        elif re.search(r".*BASE.*",file_name) != None:
            directorios['datos_base']=os.path.abspath(file_name)
        elif re.search(r".*VIA.*",file_name) != None:
            directorios['datos_via']=os.path.abspath(file_name)
        elif re.search(r".*Vac_app.*",file_name) != None:
            directorios['datos_vac_app']=os.path.abspath(file_name)
        elif re.search(r".*Vac_val.*",file_name) != None:
            directorios['datos_vac_val']=os.path.abspath(file_name)
    if len(directorios)==5:
        interurbanos_vcm_decision, interurbanos_vac_decision, vacs_decision = programa_final(directorios)
        archive_name = str(input("---- Inserte el nombre del archivo: "))
        with pd.ExcelWriter("./"+archive_name+".xlsx") as writer:
            interurbanos_vcm_decision.to_excel(writer, "interurbanos_vcm")
            interurbanos_vac_decision.to_excel(writer, "interurbanos_vac")
            vacs_decision.to_excel(writer, "vacs")
        print("ARCHIVO CREADO")