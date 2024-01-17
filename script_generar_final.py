import pandas as pd
import math
### INTERURBANOS VCM
# BASE-VIA = BASE-VIA
# %DIF/BASE = ((BASE-VIA)/BASE)
# %BIT/VIA = (BIT/VIA)
# %BIT/BASE = (BIT/BASE)
# BASE-BIT = BASE-BIT

'''  INTERURBANOS VCM
UNO BLANCO - 0.995<BASE/VIA<1.005
DOS AMARILLO - not 0.995<BASE/VIA<1.005
A VERDE - 0.995<BIT/VIA<1.005
B BLANCO - not 0.995<BIT/VIA<1.005
X MORADO - 0.995<BIT/BASE<1.005
Y BLANCO - not 0.995<BIT/BASE<1.005
'''
# "BASE-VIA" "%DIF/BASE" "BASE-BIT" "%BIT/BASE" "%BIT/VIA"
def assign_categorie_interurbanos_vcm(x): 
    resultado = ["ERROR", "ERROR"]
    if 0.995<x["BASE/VIA"]<1.005: # (UNO BLANCO)
        if 0.995<x["%BIT/VIA"]<1.005: # (UNO BLANCO, A VERDE)
            if x["BASE-VIA"]>0:
                resultado = ["VIA+Reg. Base", "OK+Regulariza[BASE-VIA]"]
            elif x["BASE-VIA"]<=0:
                resultado = ["VIA", "OK"]
        elif not 0.995<x["%BIT/VIA"]<1.005: # (UNO BLANCO, B BLANCO)
            if x["BASE-VIA"]>0:
                resultado = ["VIA+Reg. Base", "Dif. BIT-VIA"]
            elif x["BASE-VIA"]<=0:
                resultado = ["VIA", "Dif. BIT-VIA"]
    elif not 0.995<x["BASE/VIA"]<1.005: # (DOS AMARILLO)
        if 0.995<x["%BIT/VIA"]<1.005: # (DOS AMARILLO, A VERDE)
            if x["BASE-VIA"]>0:
                resultado = ["VIA+Reg. Base", "Analizar BASE"]
            elif x["BASE-VIA"]<0:
                resultado = ["VIA", "Analizar BASE"]
        elif not 0.995<x["%BIT/VIA"]<1.005: # (DOS AMARILLO, B BLANCO)
            if 0.995<x["%BIT/BASE"]<1.005:
                if x["BASE-BIT"]>0:
                    resultado = ["BIT+Reg. Base", "VIA erroneo-Analizar base"]
                elif x["BASE-BIT"]<=0:
                    resultado = ["BIT", "VIA erroneo-Analizar base"]
            elif not 0.995<x["%BIT/BASE"]<1.005:
                if x["BASE-BIT"]>0 or x["BASE-BIT"]<0:
                    resultado = ["no coincide nada", "No coincide nada"]
    return pd.Series(resultado)

### VACs
# BASE-VAC = BASE-VAC
# %BASE/VAC = (BASE/VAC)
# %BIT/VAC = (BIT/VAC)
''' 
BLANCO - SIN BASE
UNO NARANJA - 0.995<BASE/VAC<1.005
DOS AZUL - not 0.995<BASE/VAC<1.005
A VERDE - 0.995<BIT/VAC<1.005
B ROJO - not 0.995<BIT/VAC<1.005
'''
## "BASE-VAC" "%BASE/VAC" "%BIT/VAC"
def assign_categorie_vacs(x):
    resultado = ["ERROR", "ERROR"]
    if math.isnan(x["BASE"]): # (BLANCO)
        resultado = ["VAC", "Sin dato BASE"]
    else:
        if 0.995<x["%BASE/VAC"]<1.005: # (UNO NARANJA)
            if x["BASE-VAC"]>0:
                resultado = ["VAC+Reg. Base", "OK+Regulariza[BASE-VAC]"]
            elif x["BASE-VAC"]<=0:
                resultado = ["VAC", "OK"]
        elif not 0.995<x["%BASE/VAC"]<1.005: # (DOS AZUL)
            if 0.995<x["%BIT/VAC"]<1.005: # (DOS AZUL, A VERDE)
                resultado = ["VAC", "Error en BASE"]
            elif not 0.995<x["%BIT/VAC"]<1.005: # (DOS AZUL, B ROJO)
                resultado = ["VAC", "No coincide nada"]
    return pd.Series(resultado)

def construir_tabla_decisiones(interurbanos_vcm, vacs):
    interurbanos_vcm.rename({"Concesion":"CONCESION", "Total_VIA":"VIA","Total_BIT":"BIT","Total_BASE":"BASE"}, axis=1 , inplace=True)
    vacs.rename({"Concesion":"CONCESION","Total_VIA":"VIA", "Total_VAC":"VAC","Total_BIT":"BIT","Total_BASE":"BASE"}, axis=1 , inplace=True)
### INTERURBANOS VCM
# BASE-VIA = BASE-VIA
# %DIF/BASE = ((BASE-VIA)/BASE)
# %BIT/VIA = (BIT/VIA)
# %BIT/BASE = (BIT/BASE)
# BASE-BIT = BASE-BIT
    interurbanos_vcm["BASE-VIA"] = interurbanos_vcm["BASE"]-interurbanos_vcm["VIA"]
    interurbanos_vcm["BASE/VIA"] = interurbanos_vcm["BASE"]/interurbanos_vcm["VIA"]
    #interurbanos_vcm["%DIF/BASE"] = (interurbanos_vcm["BASE-VIA"]/interurbanos_vcm["BASE"])
    interurbanos_vcm["BASE-BIT"] = interurbanos_vcm["BASE"]-interurbanos_vcm["BIT"]
    interurbanos_vcm["%BIT/BASE"] = (interurbanos_vcm["BIT"]/interurbanos_vcm["BASE"])
    interurbanos_vcm["%BIT/VIA"] = (interurbanos_vcm["BIT"]/interurbanos_vcm["VIA"])
    interurbanos_vcm[["DECISION","ACCION"]] = interurbanos_vcm.apply(assign_categorie_interurbanos_vcm, axis=1)
    print("------------------ INTERURBANOS VCM /// ")
### VACs
# BASE-VAC = BASE-VAC
# %BASE/VAC = (BASE/VAC)
# %BIT/VAC = (BIT/VAC)
    vacs["BASE-VAC"] = vacs["BASE"]-vacs["VAC"]
    vacs["%BASE/VAC"] = (vacs["BASE"]/vacs["VAC"])
    vacs["%BIT/VAC"] = (vacs["BIT"]/vacs["VAC"])
    vacs[["DECISION","ACCION"]] = vacs.apply(assign_categorie_vacs, axis=1)
    print("------------- VACs /// ", vacs.columns)
    print("////// INTERURBANOS VCM /// ", interurbanos_vcm.columns)
    print("////// VACs /// ", vacs.columns)
    return interurbanos_vcm, vacs

def contruir_tabla_final_interubanos(decision_interurbanos, via, bit):
    try:
        finaldf = pd.DataFrame(columns=["Concesion","Fecha","Codtit","Coddes","Validaciones"])
        via["Fecha"] = pd.to_datetime(via["Fecha"])
        for registro in decision_interurbanos.iterrows():
            registro = registro[1]
            if registro["DECISION"] == "VIA":
                finaldf = pd.concat([finaldf, via[via["Concesion"]==registro["CONCESION"]]], axis=0)
                finaldf.Fecha = pd.to_datetime(finaldf.Fecha, format="mixed").dt.strftime("%d/%m/%Y")
            elif registro["DECISION"] == "BIT":
                bit.rename(columns={"Periodo":"Fecha","Subidos":"Validaciones"}, inplace=True, errors="ignore")
                finaldf = pd.concat([finaldf, bit[bit["Concesion"]==registro["CONCESION"]]], axis=0)
                finaldf.Fecha = pd.to_datetime(finaldf.Fecha, format="mixed").dt.strftime("%d/%m/%Y")
            elif registro["DECISION"] == "VIA+Reg. Base":
                new_df = pd.DataFrame(columns=["Concesion","Fecha","Codtit","Validaciones","Coddes"])
                new_df = via[via["Concesion"]==registro["CONCESION"]]
                decision_inter = decision_interurbanos[decision_interurbanos["CONCESION"]==registro["CONCESION"]]
                new_df = pd.concat([new_df, via[via["Concesion"]==registro["CONCESION"]]], axis=0)
                new_df.Fecha = pd.to_datetime(new_df.Fecha).dt.strftime("%d/%m/%Y")
                line = pd.DataFrame({"Concesion":registro["CONCESION"], "Fecha":via["Fecha"].dt.strftime("%m/%Y"), "Codtit":"Regulariza", "Validaciones":decision_inter["BASE-VIA"], "Coddes":"Regulariza"}, index=[0])
                new_df = pd.concat([new_df, line], axis=0)
                finaldf = pd.concat([finaldf, new_df], axis=0)
            elif registro["DECISION"] == "BIT+Reg. Base":
                bit.rename(columns={"Periodo":"Fecha","Subidos":"Validaciones"}, inplace=True, errors="ignore")
                new_df = pd.DataFrame(columns=["Concesion","Fecha","Codtit","Validaciones","Coddes"])
                new_df = bit[bit["Concesion"]==registro["CONCESION"]]
                decision_inter = decision_interurbanos[decision_interurbanos["CONCESION"]==registro["CONCESION"]]
                new_df = pd.concat([new_df, bit[bit["Concesion"]==registro["CONCESION"]]], axis=0)
                new_df.Fecha = pd.to_datetime(new_df.Fecha).dt.strftime("%d/%m/%Y")
                line = pd.DataFrame({"Concesion":registro["CONCESION"], "Fecha":bit["Fecha"].dt.strftime("%m/%Y"), "Codtit":"Regulariza", "Validaciones":decision_inter["BASE-VIA"], "Coddes":"Regulariza"}, index=[0])
                new_df = pd.concat([new_df, line], axis=0)
                finaldf = pd.concat([finaldf, new_df], axis=0)
        return finaldf
    except Exception as e:
        print(e)
        raise e

def contruir_tabla_final_vacs(vacs_decision, vacs):
    try:
        finaldf = pd.DataFrame(columns=["Concesion","Fecha","Codtit","Coddes","Validaciones"])
        for registro in vacs_decision.iterrows():
            registro = registro[1]
            if registro["DECISION"] == "VIA":
                finaldf = pd.concat([finaldf, vacs[vacs["Concesion"]==registro["CONCESION"]]], axis=0)
                finaldf.Fecha = pd.to_datetime(finaldf.Fecha, format="mixed").dt.strftime("%d/%m/%Y")
            elif registro["DECISION"] == "VIA+Reg. Base":
                new_df = pd.DataFrame(columns=["Concesion","Fecha","Codtit","Validaciones","Coddes"])
                new_df = vacs[vacs["Concesion"]==registro["CONCESION"]]
                decision_inter = vacs_decision[vacs_decision["CONCESION"]==registro["CONCESION"]]
                new_df = pd.concat([new_df, vacs[vacs["Concesion"]==registro["CONCESION"]]], axis=0)
                new_df.Fecha = pd.to_datetime(new_df.Fecha).dt.strftime("%d/%m/%Y")
                line = pd.DataFrame({"Concesion":registro["CONCESION"], "Fecha":vacs["Fecha"].dt.strftime("%m/%Y"), "Codtit":"Regulariza", "Validaciones":decision_inter["BASE-VIA"], "Coddes":"Regulariza"}, index=[0])
                new_df = pd.concat([new_df, line], axis=0)
                finaldf = pd.concat([finaldf, new_df], axis=0)
        return finaldf
    except Exception as e:
        print(e)
        raise e