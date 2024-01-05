import openpyxl
import pandas as pd
import numpy as np
import unicodedata

from exceptions_app import *

## COLUMNAS ESTANDAR
name_datos_base_cols = ['Idconce', 'Fecha', 'Nexpe', 'Kms', 'Sencillo', 'Indicencia',
                        'Gratuitos', 'Recargo', 'Bonobus', 'Abottes', 'Pmun', 'Otros', 'Valman',
                        'Total', 'Ingsencillo', 'Ingrecargo', 'Ingtotal', 'Fichero',
                        'Fecha Proc']
name_datos_via_cols = ['CONCESION', 'FECHA', 'NULINUSER', 'SUBLINEA', 'CODTIT', 'TITULO',
                       'IDCODIGOPERFIL', 'CODDES', 'DESCUENTO', 'VALIDACIONES', 'FICHERO','F_PROCESO']
name_datos_bit_cols = ['Operador', 'Concesion', 'Periodo', 'Codtit', 'Titulo', 'Subidos']
name_datos_vac_app_cols = ['Tipo', 'Empresa', 'Concesión/Linea', 'Titulo', 'Dscr Título', 'Fecha',
                            'Hora', 'Zona Validación', 'Validaciones']
name_datos_vac_val_cols = ['Empresa', 'Fecha', 'Concesion', 'L Gestra', 'Desclinea', 'P Gestra',
                            'Descparada', 'Corona', 'Codtit', 'Titulo', 'Validaciones']

def leer_archivos(diccionario_archivos):
    try:
        datos_base = pd.read_excel(diccionario_archivos["datos_base"], engine='openpyxl')
        datos_via = pd.read_excel(diccionario_archivos["datos_via"], sheet_name=2, engine='openpyxl')
        datos_bit = pd.read_excel(diccionario_archivos["datos_bit"], sheet_name=2, engine='openpyxl')
        datos_vac_app = pd.read_excel(diccionario_archivos["datos_vac_app"], sheet_name=0, engine='openpyxl')
        datos_vac_val = pd.read_excel(diccionario_archivos["datos_vac_val"], sheet_name=2, engine='openpyxl')
        return datos_base, datos_via, datos_bit, datos_vac_app, datos_vac_val
    except:
        raise ErrorArchivos("-------- ERROR EN LA CARGA DE ARCHIVOS --------")


def estandarizar_nombres_columnas(datos_base,datos_via, datos_bit, datos_vac_app, datos_vac_val):
    a,b = 'ÁÉÍÓÚÄËÏÖÜ', 'AEIOUAEIOU'
    trans = str.maketrans(a,b)
    datos_base = [column_name.upper().translate(trans) for column_name in datos_base]
    datos_via_cols = [column_name.upper().translate(trans) for column_name in datos_via]
    datos_bit_cols = [column_name.upper().translate(trans) for column_name in datos_bit]
    datos_vac_app_cols = [column_name.upper().translate(trans) for column_name in datos_vac_app]
    datos_vac_val_cols = [column_name.upper().translate(trans) for column_name in datos_vac_val]
    return datos_base, datos_via_cols, datos_bit_cols, datos_vac_app_cols, datos_vac_val_cols

def comprobar_nombres_columnas(diccionario_archivos):
    ## cargamos las columnas de los archivos
    mensaje_error = ""
    datos_base = pd.read_excel(diccionario_archivos["datos_base"], engine="openpyxl", nrows=0)
    datos_via = pd.read_excel(diccionario_archivos["datos_via"], sheet_name=2, header=0, engine='openpyxl', nrows=0)
    datos_bit = pd.read_excel(diccionario_archivos["datos_bit"], sheet_name=2, header=0,  engine='openpyxl', nrows=0)
    datos_vac_app = pd.read_excel(diccionario_archivos["datos_vac_app"], sheet_name=0, header=0,  engine='openpyxl', nrows=0)
    datos_vac_val = pd.read_excel(diccionario_archivos["datos_vac_val"], sheet_name=2, header=0,  engine='openpyxl', nrows=0)

    datos_base_cols, datos_via_cols, datos_bit_cols, datos_vac_app_cols, datos_vac_val_cols = estandarizar_nombres_columnas(datos_base, datos_via, datos_bit, datos_vac_app, datos_vac_val)
    name_datos_base_cols_OK, name_datos_via_cols_OK, name_datos_bit_cols_OK, name_datos_vac_app_cols_OK, name_datos_vac_val_cols_OK = estandarizar_nombres_columnas(name_datos_base_cols, name_datos_via_cols, name_datos_bit_cols, name_datos_vac_app_cols, name_datos_vac_val_cols)

    print("COMPROBANDO LAS DIFERENCIAS ENTRE LAS COLUMNAS: ")
    print("__________________________________________________________\n")
    cols_data_base = [col for col in name_datos_base_cols_OK if col not in datos_base_cols]
    if cols_data_base == []:
        print("CORRECTO, LOS CAMPOS DE LAS COLUMNAS DEL datos_base COINCIDEN.")
    else:
        print("CORREGIR CAMPOS datos_via: ")
        print("Su fichero contiene las columnas: ", datos_base.columns)
        print("El fichero deseado contiene las columnas: ", name_datos_base_cols)
        print("Corrija las siguientes columnas: ", cols_data_base)
        mensaje_error+="\nBASE columnas a revisar: "+str(cols_data_base)
    print("__________________________________________________________\n")
    cols_data_via = [col for col in name_datos_via_cols_OK if col not in datos_via_cols]
    if cols_data_via == []:
        print("CORRECTO, LOS CAMPOS DE LAS COLUMNAS DEL datos_via COINCIDEN.")
    else:
        print("CORREGIR CAMPOS datos_via: ")
        print("Su fichero contiene las columnas: ", datos_via.columns)
        print("El fichero deseado contiene las columnas: ", name_datos_via_cols)
        print("Corrija las siguientes columnas: ", cols_data_via)
        mensaje_error+="\nVIA columnas a revisar: "+str(cols_data_via)
    print("__________________________________________________________\n")
    cols_data_bit = [col for col in name_datos_bit_cols_OK if col not in datos_bit_cols]
    if cols_data_bit == []:
        print("CORRECTO, LOS CAMPOS DE LAS COLUMNAS DEL datos_bit COINCIDEN.")
    else:
        print("CORREGIR CAMPOS cols_data_bit: ")
        print("Su fichero contiene las columnas: ", datos_bit.columns)
        print("El fichero deseado contiene las columnas: ", name_datos_bit_cols)
        print("Corrija las siguientes columnas: ", cols_data_bit)
        mensaje_error+="\nBIT columnas a revisar: "+str(cols_data_bit)
    print("__________________________________________________________\n")
    cols_data_vac_app = [col for col in name_datos_vac_app_cols_OK if col not in datos_vac_app_cols]
    if cols_data_vac_app == []:
        print("CORRECTO, LOS CAMPOS DE LAS COLUMNAS DEL datos_vac_app COINCIDEN.")
    else:
        print("CORREGIR CAMPOS datos_vac_app: ")
        print("Su fichero contiene las columnas: ", datos_vac_app.columns)
        print("El fichero deseado contiene las columnas: ", name_datos_vac_app_cols)
        print("Corrija las siguientes columnas: ", cols_data_vac_app)
        mensaje_error+="\nVAC_app columnas a revisar: "+str(cols_data_vac_app)
    print("__________________________________________________________\n")
    cols_data_vac_val = [col for col in name_datos_vac_val_cols_OK if col not in datos_vac_val_cols]
    if cols_data_vac_val == []:
        print("CORRECTO, LOS CAMPOS DE LAS COLUMNAS DEL datos_vac_val COINCIDEN.")
    else:
        print("CORREGIR CAMPOS datos_vac_val: ")
        print("Su fichero contiene las columnas: ", datos_vac_val.columns)
        print("El fichero deseado contiene las columnas: ", name_datos_vac_val_cols)
        print("Corrija las siguientes columnas: ", cols_data_vac_val)
        mensaje_error+="\nVAC_val columnas a revisar: "+str(cols_data_vac_val)
    if mensaje_error!="":
        raise ErrorNombreColumnas(mensaje_error)

## procesamos el VAC
### VAC_VAL y VAC_APP
def procesar_vac_app(datos_vac_val, datos_vac_app):
    day_datos_vac_val_export = datos_vac_val.groupby(["Concesion", "Fecha", "Codtit"])["Validaciones"].sum().reset_index(name="Total_VAC")
    day_datos_vac_app_export = datos_vac_app.groupby(["Concesión/Linea", "Fecha", "Titulo"])["Validaciones"].sum().reset_index(name="Total_VAC")
    day_datos_vac_app_export.rename({"Concesión/Linea":"Concesion", "Titulo":"Codtit"}, axis=1, inplace=True)
    day_datos_vac_export = pd.concat([day_datos_vac_val_export, day_datos_vac_app_export], axis=0)
    month_datos_vac_export = day_datos_vac_export
    if month_datos_vac_export.Fecha.dtypes == "datetime64[ns]":
        month_datos_vac_export.Fecha = day_datos_vac_export.Fecha.dt.to_period("M")
    month_datos_vac_export.rename({"CONCESION":"Concesion", "Fecha":"Mes","Total_VAC":"Total"}, axis=1, inplace=True)
    return month_datos_vac_export.groupby(["Concesion", "Mes"])["Total"].sum().reset_index(name="Total_VAC")
## procesamos el BIT
def procesar_bit(datos_bit):
    month_datos_bit_export = datos_bit.groupby(["Concesion", "Periodo", "Codtit"])["Subidos"].sum().reset_index(name="Total_BIT")
    month_datos_bit_export.Periodo = pd.to_datetime(month_datos_bit_export.Periodo, format="%m/%Y")
    if month_datos_bit_export.Periodo.dtypes == "datetime64[ns]":
        month_datos_bit_export.Periodo = month_datos_bit_export.Periodo.dt.to_period("M")
    month_datos_bit_export.columns
    month_datos_bit_export.rename({"CONCESION":"Concesion", "Periodo":"Mes", "Total_BIT":"Total"}, axis=1, inplace=True)
    return month_datos_bit_export.groupby(["Concesion", "Mes"])["Total"].sum().reset_index(name="Total_BIT")
## procesamos el VIA
def procesar_via(datos_via):
    day_datos_via_export = datos_via.groupby(["CONCESION", "FECHA", "CODTIT"])["VALIDACIONES"].sum().reset_index(name="Total_VIA")
    day_datos_via_export.FECHA = pd.to_datetime(day_datos_via_export.FECHA, format="%d/%m/%Y")
    month_datos_via_export = day_datos_via_export
    ## sustituyo la fecha a mes
    if month_datos_via_export.FECHA.dtypes == "datetime64[ns]":
        month_datos_via_export.FECHA = pd.to_datetime(month_datos_via_export.FECHA)
        month_datos_via_export.FECHA = day_datos_via_export.FECHA.dt.to_period("M")
    ## agrupo por mes y hago la suma total de los totales
    month_datos_via_export.rename({"CONCESION":"Concesion", "FECHA":"Mes", "Total_VIA":"Total"}, axis=1, inplace=True)
    return month_datos_via_export.groupby(["Concesion", "Mes"])["Total"].sum().reset_index(name="Total_VIA")
## proceso el BASE
def proceso_base(datos_base):
    datos_base.rename(columns={"Idconce":"Concesion","Fecha":"Mes","Total":"Total_BASE"}, inplace=True)
    datos_base_ok = datos_base[["Concesion","Mes","Total_BASE"]]
    datos_base_ok.Mes = pd.to_datetime(datos_base_ok.Mes, format="%m/%Y")
    if datos_base_ok.Mes.dtypes == "datetime64[ns]":
        datos_base_ok.Mes = pd.to_datetime(datos_base_ok.Mes)
        datos_base_ok.Mes = datos_base_ok.Mes.dt.to_period("M")
    return datos_base_ok

## tabla union de todos los totales VIA, VAC, BIT
def lista_final(month_datos_via_export, month_datos_vac_export, month_datos_bit_export, datos_base_ok):
    lista_concat = ['Concesion', 'Mes']
    lista_vacs_interurbano = ['V5805','VAC-023',
    'VAC-051','VAC-063','VAC-082','VAC-087',
    'VAC-093','VAC-152','VAC-158','VAC-221',
    'VAC-226','VAC-231','VAC-243','VAC-249']
    lista_totales_union_INTERURBANOS = pd.merge(pd.merge(month_datos_via_export, month_datos_bit_export, on=lista_concat, how="left"),datos_base_ok, on=lista_concat, how="left")
    lista_totales_union_INTERURBANOS.rename({"Total_x":"Total_via", "Total_y":"Total_bit", "Total":"Total_BASE"}, axis=1, inplace=True)
    lista_totales_union_INTERURBANOS.drop(["Mes"], axis=1, inplace=True)

    lista_totales_union_VACs = pd.merge(pd.merge(pd.merge(month_datos_vac_export, month_datos_bit_export, on=lista_concat, how="left"),datos_base_ok, on=lista_concat, how="left"), month_datos_via_export, on=lista_concat, how="left")
    lista_totales_union_VACs.rename({"Total_x":"Total_via", "Total_y":"Total_bit", "Total":"Total_BASE"}, axis=1, inplace=True)
    lista_totales_union_VACs.drop(["Mes"], axis=1, inplace=True)

    lista_totales_union_INTERURBANOS = lista_totales_union_INTERURBANOS[(lista_totales_union_INTERURBANOS.Concesion != "-") & (lista_totales_union_INTERURBANOS.Concesion != "97")]
    lista_totales_union_VACs = lista_totales_union_VACs[(lista_totales_union_VACs.Concesion != "-") & (lista_totales_union_VACs.Concesion != "97")]
    
    lista_totales_union_INTERURBANOS_VCM = lista_totales_union_INTERURBANOS[~lista_totales_union_INTERURBANOS['Concesion'].isin(lista_vacs_interurbano)]
    lista_totales_union_INTERURBANOS_VAC = lista_totales_union_INTERURBANOS[lista_totales_union_INTERURBANOS['Concesion'].isin(lista_vacs_interurbano)]

    lista_totales_union_INTERURBANOS_VAC = pd.merge(lista_totales_union_INTERURBANOS_VAC, lista_totales_union_VACs, how="left")
    print("////// INTERURBANOS VCM/// ", lista_totales_union_INTERURBANOS_VCM.columns)
    print("////// INTERURBANOS VAC/// ", lista_totales_union_INTERURBANOS_VAC.columns)

    print("////// VACs /// ", lista_totales_union_VACs.columns)

    return lista_totales_union_INTERURBANOS_VCM, lista_totales_union_INTERURBANOS_VAC, lista_totales_union_VACs