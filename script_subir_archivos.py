import pandas as pd
import re
from exceptions_app import *

## COLUMNAS ESTANDAR
name_datos_base_cols = ['Idconce', 'Fecha', 'Sencillo', 'Indicencia','Gratuitos', 'Recargo', 'Bonobus', 'Abottes', 'Pmun', 'Otros', 'Valman','Total']
name_datos_via_cols = ['Concesion', 'Fecha', 'Nulinuser', 'Sublinea', 'Codtit', 'Coddes', 'Validaciones']
name_datos_bit_cols = ['Concesion', 'Periodo', 'Codtit', 'Subidos', 'Coddes']
name_datos_vac_app_cols = ['Concesión/Linea', 'Titulo', 'Fecha','Hora', 'Zona Validación', 'Validaciones']
name_datos_vac_val_cols = ['Fecha', 'Concesion', 'L Gestra', 'P Gestra','Corona', 'Codtit', 'Validaciones']


types_base_cols = {'Idconce':'str', 'Sencillo':"int64", 'Indicencia':"int64",'Gratuitos':"int64", 'Recargo':"int64", 'Bonobus':"int64", 'Abottes':"int64", 'Pmun':"int64", 'Otros':"int64", 'Valman':"str",'Total':"int64"}
types_via_cols = {'Concesion':'str', 'Nulinuser':"str", 'Sublinea':"str", 'Codtit':"int64", 'Coddes':"str", 'Validaciones':"int64"}
types_bit_cols = {'Concesion':'str', 'Codtit':"str", 'Subidos':"int64", 'Coddes':"str"}
types_vac_app_cols = {'Concesión/Linea':'str', 'Titulo':"str", 'Zona Validación':"str", 'Validaciones':"int64","Fecha":"datetime64[ns]"}
types_vac_val_cols = {'Concesion':'str', 'L Gestra':"str", 'P Gestra':"str",'Corona':"str", 'Codtit':"str", 'Validaciones':"int64","Fecha":"datetime64[ns]"}


def leer_archivos(diccionario_archivos):
    try:
        datos_base = pd.read_excel(diccionario_archivos["datos_base"], sheet_name="datos-base",  usecols=name_datos_base_cols, dtype= types_base_cols, date_format="%m/%Y", parse_dates=["Fecha"])
        datos_via = pd.read_excel(diccionario_archivos["datos_via"], sheet_name="datos-via", usecols=name_datos_via_cols, dtype= types_via_cols)
        datos_bit = pd.read_excel(diccionario_archivos["datos_bit"], sheet_name="datos-bit",  nrows=0)
        if "Coddes" not in datos_bit.columns:
            datos_bit = pd.read_excel(diccionario_archivos["datos_bit"], sheet_name="datos-bit",  usecols=name_datos_bit_cols[:-1], dtype= types_bit_cols, date_format="%m/%Y", parse_dates=["Periodo"])
            datos_bit["Coddes"] = ""
        else:
            datos_bit = pd.read_excel(diccionario_archivos["datos_bit"], sheet_name="datos-bit",  usecols=name_datos_bit_cols, dtype= types_bit_cols, date_format="%m/%Y", parse_dates=["Periodo"])
        datos_bit.Periodo = pd.to_datetime(datos_bit.Periodo, format="%m/%Y")
        if datos_bit.Periodo.dtypes == "datetime64[ns]":
            datos_bit.Periodo = datos_bit.Periodo.dt.to_period("M")
        datos_via.Fecha = pd.to_datetime(datos_via.Fecha, format="%d/%m/%Y").dt.date
        datos_vac_val = pd.read_excel(diccionario_archivos["datos_vac_val"], sheet_name="datos-Vval", usecols=name_datos_vac_val_cols, dtype=types_vac_val_cols , date_format="%d/%m/%Y", parse_dates=["Fecha"])
        datos_vac_app = pd.read_excel(diccionario_archivos["datos_vac_app"], sheet_name="datos-Vapp", usecols=name_datos_vac_app_cols, dtype=types_vac_app_cols , date_format="%d/%m/%Y", parse_dates=["Fecha"])
        datos_vac_app['Zona Validación'] = datos_vac_app['Zona Validación'].apply(lambda x: re.findall('\w+', x)[1])
        return datos_base, datos_via, datos_bit, datos_vac_app, datos_vac_val
    except Exception as e:
        print(str(e))
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
    try:
        datos_base = pd.read_excel(diccionario_archivos["datos_base"], sheet_name="datos-base", engine='openpyxl', nrows=0)
        datos_via = pd.read_excel(diccionario_archivos["datos_via"], sheet_name="datos-via", engine='openpyxl', nrows=0)
        datos_bit = pd.read_excel(diccionario_archivos["datos_bit"], sheet_name="datos-bit", engine='openpyxl', nrows=0)
        if "Coddes" not in datos_bit.columns:
            datos_bit["Coddes"] = ""
        datos_vac_app = pd.read_excel(diccionario_archivos["datos_vac_app"], sheet_name="datos-Vapp", engine='openpyxl', nrows=0)
        datos_vac_val = pd.read_excel(diccionario_archivos["datos_vac_val"], sheet_name="datos-Vval", engine='openpyxl', nrows=0)
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
    except Exception as e:
        raise ErrorArchivos(e)    
    

## procesamos el VAC
### VAC_VAL y VAC_APP
def procesar_vac_app(datos_vac_val, datos_vac_app):
    datos_vac_val["Fecha"] = pd.to_datetime(datos_vac_val.Fecha, format="mixed", dayfirst=True)
    datos_vac_app["Fecha"] = pd.to_datetime(datos_vac_app.Fecha, format="mixed", dayfirst=True)
    print("VAC_VAL:\n", datos_vac_val.dtypes)
    print("VAC_APP:\n", datos_vac_app.dtypes)
    day_datos_vac_val_export = datos_vac_val.groupby(["Concesion", "Fecha", "Codtit"])["Validaciones"].sum().reset_index(name="Total_VAC")
    day_datos_vac_app_export = datos_vac_app.groupby(["Concesion", "Fecha", "Codtit"])["Validaciones"].sum().reset_index(name="Total_VAC")
    day_datos_vac_export = pd.concat([day_datos_vac_val_export, day_datos_vac_app_export], axis=0)
    month_datos_vac_export = day_datos_vac_export
    if month_datos_vac_export.Fecha.dtypes == "datetime64[ns]":
        month_datos_vac_export.Fecha = day_datos_vac_export.Fecha.dt.to_period("M")
    month_datos_vac_export.rename({"CONCESION":"Concesion", "Fecha":"Mes","Total_VAC":"Total"}, axis=1, inplace=True)
    return month_datos_vac_export.groupby(["Concesion", "Mes"])["Total"].sum().reset_index(name="Total_VAC")
## procesamos el BIT
def procesar_bit(datos_bit):
    month_datos_bit_export = datos_bit.groupby(["Concesion", "Fecha", "Codtit"])["Validaciones"].sum().reset_index(name="Total_BIT")
    #month_datos_bit_export.Fecha = pd.to_datetime(month_datos_bit_export.Fecha, format="%m/%Y")
    if month_datos_bit_export.Fecha.dtypes == "datetime64[ns]":
        month_datos_bit_export.Fecha = month_datos_bit_export.Fecha.dt.to_period("M")
    month_datos_bit_export.columns
    month_datos_bit_export.rename({"Fecha":"Mes", "Total_BIT":"Total"}, axis=1, inplace=True)
    return month_datos_bit_export.groupby(["Concesion", "Mes"])["Total"].sum().reset_index(name="Total_BIT")
## procesamos el VIA
def procesar_via(datos_via):
    datos_via.Validaciones = datos_via.Validaciones.astype('int64')
    day_datos_via_export = datos_via.groupby(["Concesion", "Fecha", "Codtit"])["Validaciones"].sum().reset_index(name="Total_VIA")
    day_datos_via_export.Fecha = pd.to_datetime(day_datos_via_export.Fecha, format="%d/%m/%Y")
    month_datos_via_export = day_datos_via_export
    ## sustituyo la fecha a mes
    if month_datos_via_export.Fecha.dtypes == "datetime64[ns]":
        month_datos_via_export.Fecha = pd.to_datetime(month_datos_via_export.Fecha)
        month_datos_via_export.Fecha = day_datos_via_export.Fecha.dt.to_period("M")
    ## agrupo por mes y hago la suma total de los totales
    month_datos_via_export.rename({"Fecha":"Mes", "Total_VIA":"Total"}, axis=1, inplace=True)
    return month_datos_via_export.groupby(["Concesion", "Mes"])["Total"].sum().reset_index(name="Total_VIA")
## proceso el BASE
def proceso_base(datos_base):
    datos_base.Fecha = datos_base.Fecha.dt.to_period("M")
    datos_base.rename(columns={"Idconce":"Concesion","Fecha":"Mes","Total":"Total_BASE"}, inplace=True)
    return datos_base[["Concesion","Mes","Total_BASE"]]

## tabla union de todos los totales VIA, VAC, BIT
def lista_final(month_datos_via_export, month_datos_vac_export, month_datos_bit_export, datos_base_ok):
    # print("VIA:\n", month_datos_via_export.dtypes)
    # print("VAC:\n", month_datos_vac_export.dtypes)
    # print("BIT:\n", month_datos_bit_export.dtypes)
    # print("BASE:\n", datos_base_ok.dtypes)
    lista_concat = ['Concesion', 'Mes']
    lista_interubanos_vcm = ['U0058', 'URCM-005',
    'URCM-013', 'URCM-014', 'URCM-148', 'URCM-152', 
    'URCM-161', 'VCM-101', 'VCM-102', 'VCM-103', 
    'VCM-200', 'VCM-201', 'VCM-202', 'VCM-203', 
    'VCM-204', 'VCM-301', 'VCM-302', 'VCM-303', 
    'VCM-401', 'VCM-402', 'VCM-403', 'VCM-404', 
    'VCM-500', 'VCM-501', 'VCM-502', 'VCM-503', 
    'VCM-504', 'VCM-600', 'VCM-601', 'VCM-602', 
    'VCM-603', 'VCM-604', 'VCM-605', 'VCM-606', 
    'VCM-607', 'VCM-701', 'VCM-702']
    lista_vacs_interurbano = ['V5805','VAC-023',
    'VAC-051','VAC-063','VAC-082','VAC-087',
    'VAC-093','VAC-152','VAC-158','VAC-221',
    'VAC-226','VAC-231','VAC-243','VAC-249']
    lista_totales_union_INTERURBANOS = pd.merge(pd.merge(month_datos_via_export, month_datos_bit_export, on=lista_concat, how="outer"),datos_base_ok, on=lista_concat, how="outer")
    lista_totales_union_INTERURBANOS.rename({"Total_x":"Total_via", "Total_y":"Total_bit", "Total":"Total_BASE"}, axis=1, inplace=True)
    lista_totales_union_INTERURBANOS.drop(["Mes"], axis=1, inplace=True)

    lista_totales_union_VACs = pd.merge(pd.merge(pd.merge(month_datos_vac_export, month_datos_bit_export, on=lista_concat, how="outer"),datos_base_ok, on=lista_concat, how="outer"), month_datos_via_export, on=lista_concat, how="outer")
    lista_totales_union_VACs.rename({"Total_x":"Total_via", "Total_y":"Total_bit", "Total":"Total_BASE"}, axis=1, inplace=True)
    lista_totales_union_VACs.drop(["Mes"], axis=1, inplace=True)

    lista_totales_union_INTERURBANOS = lista_totales_union_INTERURBANOS[(lista_totales_union_INTERURBANOS.Concesion != "-") & (lista_totales_union_INTERURBANOS.Concesion != "97")]
    lista_totales_union_VACs = lista_totales_union_VACs[(lista_totales_union_VACs.Concesion != "-") & (lista_totales_union_VACs.Concesion != "97")]
    
    lista_totales_union_VACs = lista_totales_union_VACs[lista_totales_union_VACs['Concesion'].isin(lista_vacs_interurbano)]
    lista_totales_union_INTERURBANOS_VCM = lista_totales_union_INTERURBANOS[lista_totales_union_INTERURBANOS['Concesion'].isin(lista_interubanos_vcm)]

    print("////// INTERURBANOS VCM/// ", lista_totales_union_INTERURBANOS_VCM.columns)
    print("////// VACs /// ", lista_totales_union_VACs.columns)
    return lista_totales_union_INTERURBANOS_VCM, lista_totales_union_VACs

def tablas_finales_bit_via_vac(datos_via, datos_bit, datos_vac_app, datos_vac_val):
    columnas_finales_vcm = ['Concesion', 'Fecha', 'Codtit', 'Validaciones', 'Coddes']
    columnas_vacs = ['Concesion','Fecha', 'Corona', 'Codtit', 'Validaciones']
    datos_bit.rename({'Periodo':"Fecha", 'Subidos':'Validaciones'}, inplace=True, axis='columns')
    if 'Coddes' not  in datos_bit.columns:
        datos_bit["Coddes"]=""
    datos_vac_app.rename({'Concesión/Linea':"Concesion",'Titulo':"Codtit", 'Zona Validación':"Corona"}, inplace=True, axis='columns')
    
    vacs = pd.concat([datos_vac_app[columnas_vacs], datos_vac_val[columnas_vacs]], axis=0)
    datos_bit["Origen"] = ""
    datos_via["Origen"] = ""
    vacs["Origen"] = ""
    vacs.Fecha = pd.to_datetime(vacs.Fecha, format="mixed").dt.strftime("%d/%m/%Y")
    return datos_via[columnas_finales_vcm], datos_bit[columnas_finales_vcm], vacs[columnas_vacs]
