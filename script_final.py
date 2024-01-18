import script_generar_final as sgf
import script_subir_archivos as ssa 
import sys

# diccionario_archivos = {
#         "datos_base":"./2023-09/2023-09 DATOS_BASE.xlsx",
#         "datos_via":"./2023-09/2023-09 DATOS_VIA.xlsx",
#         "datos_bit":"./2023-09/2023-09 InformeBIT.xlsx",
#         "datos_vac_app":"./2023-09/2023-09Vac_app.xlsx",
#         "datos_vac_val":"./2023-09/2023-09Vac_val.xlsx"
# }

def programa_final(diccionario_archivos):
    print("//////////////////////////////PRUEBAS DE SCRIPT FINAL//////////////////////////////")
    ssa.comprobar_nombres_columnas(diccionario_archivos)
    print("OK NOMBRES")
    print("EMPIEZA LA CARGA DE ARCHIVOS")
    datos_base, datos_via, datos_bit, datos_vac_app, datos_vac_val = ssa.leer_archivos(diccionario_archivos)
    print("OK CARGA ARCHIVOS")
    via, bit, vac = ssa.tablas_finales_bit_via_vac(datos_via, datos_bit, datos_vac_app, datos_vac_val)
    via.to_excel("./pruebas_out_app/via_ind.xlsx")
    bit.to_excel("./pruebas_out_app/bit_ind.xlsx")
    vac.to_excel("./pruebas_out_app/vac_ind.xlsx")
    print("OK TABLAS FINALES")
    datos_VAC_OK = ssa.procesar_vac_app(datos_vac_val, datos_vac_app)
    print("OK VAC")
    datos_BIT_OK = ssa.procesar_bit(datos_bit)
    print("OK BIT")
    datos_VIA_OK = ssa.procesar_via(datos_via)
    print("OK VIA")
    datos_BASE_OK = ssa.proceso_base(datos_base)
    print("OK BASE")
    interurbanos_vcm, vacs = ssa.lista_final(datos_VIA_OK, datos_VAC_OK, datos_BIT_OK, datos_BASE_OK)
    print("OK LISTAS INICIALES")
    interurbanos_vcm_decision, vacs_decision = sgf.construir_tabla_decisiones(interurbanos_vcm, vacs)
    print("OK LISTAS DECISIONES")
    tabla_final_interurbanos = sgf.contruir_tabla_final_interubanos(interurbanos_vcm_decision, via, bit)

    interurbanos_vcm_decision.to_excel("./pruebas_out_app/interurbanos_vcm_decision.xlsx")
    tabla_final_interurbanos.to_excel("./pruebas_out_app/tabla_final_interurbanos.xlsx")
    print("OK TABLA FINAL INTERURBANOS")
    
    tabla_final_vacs = sgf.contruir_tabla_final_vacs(vacs_decision, vac)
    vacs_decision.to_excel("./pruebas_out_app/vacs_decision.xlsx")
    tabla_final_vacs.to_excel("./pruebas_out_app/tabla_final_vacs.xlsx")
    print("OK TABLA FINAL VACS")
    return tabla_final_interurbanos, tabla_final_vacs