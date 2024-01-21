from exceptions_app import ErrorArchivos, ErrorNombreColumnas
import script_generar_final as sgf
import script_subir_archivos as ssa 
import sys
import pandas as pd
import re
import os
from openpyxl import Workbook
import script_final as sf 

if __name__ == "__main__":
    directorios = dict()
    anyo = str(input("---- Inserte el año: "))
    mes = str(input("---- Inserte el mes: "))
    try:
        mylist = [os.path.abspath("./"+anyo+"-"+mes+"/"+x) for x in os.listdir("./"+anyo+"-"+mes+"/")]
        print(mylist)
        for file_name in mylist:
            print(file_name)
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
        print("CARGADOS\n", directorios)
        if len(directorios)==5:
            interurbanos_vcm_final, vacs_final = sf.programa_final(directorios)
            archive_name = str(input("---- Inserte el nombre del archivo: "))
            with pd.ExcelWriter("./"+anyo+"-"+mes+"/"+archive_name+".xlsx", engine="openpyxl") as writer:
                interurbanos_vcm_final.to_excel(writer, "interurbanos_vcm", index=False)
                vacs_final.to_excel(writer, "vacs", index=False)
            print("ARCHIVO CREADO")
        else:
            print("Cargue todos los archivos necesarios.")
    except FileNotFoundError:
        print("---- No existe el directorio "+anyo+"-"+mes)
    