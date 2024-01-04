import pandas as pd
import numpy as np

def construir_tabla_decisiones(interurbanos_vcm, interurbanos_vac, vacs):
    interurbanos_vcm.rename({"Concesion":"CONCESION", "Total_VIA":"VIA","Total_BIT":"BIT","Total_BASE":"BASE"}, axis=1 , inplace=True)
    interurbanos_vac.rename({"Concesion":"CONCESION", "Total_VIA":"VIA","Total_BIT":"BIT","Total_BASE":"BASE", "Total_VAC":"VAC"}, axis=1 , inplace=True)
    vacs.rename({"Concesion":"CONCESION","Total_VIA":"VIA", "Total_VAC":"VAC","Total_BIT":"BIT","Total_BASE":"BASE"}, axis=1 , inplace=True)
    
    ### INTERURBANOS VCM
    # BASE-VIA = BASE-VIA
    # %DIF/BASE = ((BASE-VIA)/BASE)*100
    # BIT-BASE = BIT-BASE
    # %BIT/BASE = (BIT/BASE)*100
    # %BIT/VIA = (BIT/VIA)*100

    ### INTERURBANOS VAC
    # BASE-VIA = BASE-VIA
    # %DIF/BASE = (BASE-VIA)/BASE
    # VAC-BASE = VAC-BASE
    # VAC/VIA = VAC/VIA
    '''  INTERURBANOS VCM
    Los filtros de colores indican:
    amarillo si %DIF/BASE => -0.005<val<0.005 # val not in
    morado si %BIT/BASE => 0.995<val<1.005 # val in
    verde si %BIT/VIA => 0.995<val<1005 # val in
    '''
    '''  INTERURBANOS VCM
    'CONCESION', 'VIA', 'BIT', 'BASE', 'BASE-VIA', '%DIF/BASE', 'BIT-BASE',
    '%BIT/BASE', '%BIT/VIA', 'DECISION'
    '''
    '''  INTERURBANOS VCM
    amarillo: not -0.005<x["%DIF/BASE"]<0.005
    verde: entre 0.995<x["%BIT/VIA"]<1005
    morado: entre 0.995<x["%BIT/BASE"]<1.005
    '''
    ## para las interurbano_VCM
    def assign_categorie_interurbanos_vcm(x): 
        if -0.005<x["%DIF/BASE"]<0.005: ## (UNO BLANCO)
            if 0.995<x["%BIT/VIA"]<1005: ## (UNO BLANCO, A VERDE)
                return pd.Series(["VIA", ""])
            elif not 0.995<x["%BIT/VIA"]<1005: ## (UNO BLANCO, B BLANCO)
                if not -0.005<x["%DIF/BASE"]<0.005: ## DOS AMARILLO
                    if 0.995<x["%BIT/VIA"]<1005: ## (DOS AMARILLO, A VERDE)
                        return pd.Series(["VIA", "CE"])
                    elif not 0.995<x["%BIT/VIA"]<1005: ## (DOS AMARILLO, B BLANCO)
                        if 0.995<x["%BIT/BASE"]<1.005: ## (DOS AMARILLO, B BLANCO, X MORADO)
                            return pd.Series(["BIT", "CE"])
                        else:
                            return pd.Series(["SIN CRITERIO 1",""])
        elif not -0.005<x["%DIF/BASE"]<0.005: ## DOS AMARILLO
            if 0.995<x["%BIT/VIA"]<1005: ## (DOS AMARILLO, A VERDE)
                return pd.Series(["VIA", "CE"])
            elif not 0.995<x["%BIT/VIA"]<1005: ## (DOS AMARILLO, B BLANCO)
                if 0.995<x["%BIT/BASE"]<1.005: ## (DOS AMARILLO, B BLANCO, X MORADO)
                    return pd.Series(["BIT", "CE"])
                else:
                    return pd.Series(["SIN CRITERIO",""])
        else:
            return pd.Series(["CE",""])
        
    '''  INTERURBANOS VAC
    Los filtros:
    1. No tiene Base en la columna decisión => VAC, ""
    2. else:
        2.1. if 0.005<VAC/BASE<1.005
            2.1.1 if 0.005>BIT/VAC>1.005 => VAC, ""
            2.1.2 else => VAC, "error BIT"
        2.2. else
            2.2.1 0.005<BIT/VAC<1.005 => VAC, "error BASE"
            2.2.2 else => BIT, "Sin criterio"

    '''
    '''  INTERURBANOS VAC
    'VAC/BASE', 'BIT/VAC'
    '''
    ## para las interurbano_VACS
    def assign_categorie_interurbanos_vacs(x): 
        if x["BASE"]==0:
            return pd.Series(["VAC", ""])
        else:
            if 0.005<x["VAC/BASE"]<1.005:
                if 0.005>x["BIT/VAC"]>1.005:
                    return pd.Series(["VAC", ""])
                else:
                    return pd.Series(["VAC", "error BIT"])
            else:
                if 0.005<x["BIT/VAC"]<1.005:
                    return pd.Series(["VAC", "error BASE"])
                else:
                    return pd.Series(["BIT", "Sin criterio"])

    ### VACs
    # BASE-VIA = BASE-VIA
    # %DIF/BASE = (BASE-VIA)/BASE
    # VAC-BASE = VAC-BASE
    # VAC/VIA = VAC/VIA
    ''' 
    amarillo: not -0.005<x["%DIF/BASE"]<0.005
    verde: entre 0.995<x["%VAC/VIA"]<1.005
    morado: entre x["VAC"]*0.99<x["BIT"]<x["VAC"]*1.01
    '''
    def assign_categorie_vacs(x):
        if x["VIA"]==0:
            return pd.Series(["VAC",""])
        elif -0.005<x["%DIF/BASE"]<0.005: ## (UNO BLANCO)
            if 0.995<x["%VAC/VIA"]<1.005: ## (UNO BLANCO, A VERDE)
                return pd.Series(["VAC",""])
            elif not 0.995<x["%VAC/VIA"]<1.005: ## (UNO BLANCO, B BLANCO)
                if x["VAC"]*0.99<x["BIT"]<x["VAC"]*1.01: ## (UNO BLANCO, B BLANCO, X MORADO)
                    return pd.Series(["ANALIZAR VIA/VAC",""])
                else:
                    return pd.Series(["ANALIZAR DATOS",""])
        elif not -0.005<x["%DIF/BASE"]<0.005: ## (DOS AMARILLO)
            if 0.995<x["%VAC/VIA"]<1.005: ## (DOS AMARILLO, A VERDE)
                return pd.Series(["VAC", "CE"])
            elif not 0.995<x["%VAC/VIA"]<1.005: ## (DOS AMARILLO, B BLANCO)
                if x["VAC"]*0.99<x["BIT"]<x["VAC"]*1.01: ## (DOS AMARILLO, B BLANCO, X MORADO)
                    return pd.Series(["VAC", "CE"])
                else:
                    return pd.Series(["SIN CRITERIO",""])
        else:
            return pd.Series(["CE","CE"])

    interurbanos_vcm["BASE-VIA"] = interurbanos_vcm["BASE"]-interurbanos_vcm["VIA"]
    interurbanos_vcm["%DIF/BASE"] = (interurbanos_vcm["BASE-VIA"]/interurbanos_vcm["BASE"])*100
    interurbanos_vcm["BIT-BASE"] = interurbanos_vcm["BIT"]-interurbanos_vcm["BASE"]
    interurbanos_vcm["%BIT/BASE"] = (interurbanos_vcm["BIT"]/interurbanos_vcm["BASE"])*100
    interurbanos_vcm["%BIT/VIA"] = (interurbanos_vcm["BIT"]/interurbanos_vcm["VIA"])*100
    interurbanos_vcm[["DECISION","ACCION"]] = interurbanos_vcm.apply(assign_categorie_interurbanos_vcm, axis=1)

    '''  INTERURBANOS VAC
    'VAC/BASE', 'BIT/VAC'
    '''
    interurbanos_vac['VAC/BASE'] = interurbanos_vac["VAC"]/interurbanos_vac["BASE"]
    interurbanos_vac['BIT/VAC'] = interurbanos_vac["BIT"]/interurbanos_vac["VAC"]
    
    interurbanos_vac[["DECISION","ACCION"]] = interurbanos_vac.apply(assign_categorie_interurbanos_vacs, axis=1)

    ### VACs
    # BASE-VIA = BASE-VIA
    # %DIF/BASE = (BASE-VIA)/BASE
    # VAC-BASE = VAC-BASE
    # VAC/VIA = VAC/VIA

    vacs["BASE-VIA"] = vacs["BASE"]-vacs["VIA"]
    vacs["%DIF/BASE"] = (vacs["BASE-VIA"]/vacs["BASE"])*100
    vacs["VAC-BASE"] = vacs["VAC"]-vacs["BASE"]
    vacs["%VAC/VIA"] = (vacs["VAC"]/vacs["VIA"])*100
    vacs[["DECISION","ACCION"]] = vacs.apply(assign_categorie_vacs, axis=1)

    print("////// INTERURBANOS VCM /// ", interurbanos_vcm.columns)
    print("////// INTERURBANOS VAC /// ", interurbanos_vac.columns)
    print("////// VACs /// ", vacs.columns)
    return interurbanos_vcm, interurbanos_vac, vacs