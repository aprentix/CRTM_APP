import script_generar_final as sgf
import script_subir_archivos as ssa 
import sys

def programa_final(diccionario_archivos):
    print("//////////////////////////////SCRIPT FINAL//////////////////////////////")
    ssa.comprobar_nombres_columnas(diccionario_archivos)
    print("OK NOMBRES")
    print("EMPIEZA LA CARGA DE ARCHIVOS")
    datos_base, datos_via, datos_bit, datos_vac_app, datos_vac_val = ssa.leer_archivos(diccionario_archivos)
    print("OK CARGA ARCHIVOS")
    via, bit, vac = ssa.tablas_finales_bit_via_vac(datos_via, datos_bit, datos_vac_app, datos_vac_val)
    print("OK TABLAS FINALES")
    print("VIA: ", via.shape[0], "BIT: ", bit.shape[0],"VAC: ",vac.shape[0])
    datos_VAC_OK = ssa.procesar_vac_app(datos_vac_val, datos_vac_app)
    datos_BIT_OK = ssa.procesar_bit(datos_bit)
    datos_VIA_OK = ssa.procesar_via(datos_via)
    datos_BASE_OK = ssa.proceso_base(datos_base)
    interurbanos_vcm, vacs = ssa.lista_final(datos_VIA_OK, datos_VAC_OK, datos_BIT_OK, datos_BASE_OK)
    print("interurbanos_vcm: ", interurbanos_vcm.shape[0], "vacs: ", vacs.shape[0])
    print("OK LISTAS INICIALES")
    interurbanos_vcm_decision, vacs_decision = sgf.construir_tabla_decisiones(interurbanos_vcm, vacs)
    print("OK LISTAS DECISIONES")
    tabla_final_interurbanos = sgf.contruir_tabla_final_interubanos(interurbanos_vcm_decision, via, bit)
    print("OK TABLA FINAL INTERURBANOS")
    
    tabla_final_vacs = sgf.contruir_tabla_final_vacs(vacs_decision, vac)
    print("OK TABLA FINAL VACS")
    print("tabla_final_interurbanos: ", tabla_final_interurbanos.shape[0], "tabla_final_vacs: ", tabla_final_vacs.shape[0])
    return tabla_final_interurbanos, tabla_final_vacs