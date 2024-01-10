# INSTRUCCIONES APLICACIÓN GENERACIÓN ARCHIVOS EXCEL

## REQUISITOS:
- Los archivos tienen que tener el nombre original de descarga y no han de tener las hojas en orden modificado. Todos han de pertenecer al mismo mes. 
- Ejemplo para el mes 09 :
    - BASE: "2023-09 DATOS_BASE.xlsx"
    - VIA: "2023-09 DATOS_VIA.xlsx"
    - BIT: "2023-09 InformeBIT.xlsx"
    - VAC_APP: "2023-09Vac_app.xlsx"
    - VAC_VAL: "2023-09Vac_val.xlsx"
- Las columnas de cada archivo:

## ADVERTENCIA:
El programa puede llegar a tardar 10 minutos en cargar los datos, una vez cargados tiene que pulsar en descargar archivo y guardarlo en el directorio que guste.

## NOMBRES OBLIGATORIOS DE LAS HOJAS A CARGAR
- BASE = "datos-base"
- VIA = "datos-via"
- BIT = "datos-bit"
- VAC_APP = "datos-Vapp"
- VAC_VAL = "datos-Vval"

## COLUMNAS OBLIGATORIAS DE CADA TABLA:
BASE = ['Idconce', 'Fecha', 'Sencillo', 'Indicencia','Gratuitos', 'Recargo', 'Bonobus', 'Abottes', 'Pmun', 'Otros', 'Valman','Total']

VIA = ['CONCESION', 'FECHA', 'NULINUSER', 'SUBLINEA', 'CODTIT', 'CODDES','VALIDACIONES']

BIT = ['Concesion', 'Periodo', 'Codtit', 'Subidos'] (Coddes)

VAC_APP = ['Concesión/Linea', 'Titulo', 'Fecha','Hora', 'Zona Validación', 'Validaciones']

VAC_VAL = ['Fecha', 'Concesion', 'L Gestra', 'P Gestra','Corona', 'Codtit', 'Validaciones']

## COLUMNAS TABLA FINAL
[Concesion, Fecha, Codtit, Validaciones, Coddes, Corona]

---

### AVISO: 
Es una mecanización, por ende, solo respeta procesos repetitivos y podria haber fallos si no se respetan los requisitos.

### Más info
Herramienta desarrollada para el departamento Comercial del CRTM en diciembre de 2023.
Desarrollo: Raquel DC (becaria) bajo la supervisión e instrucciones de Óscar Barrientos García.

Codigo en: https://github.com/aprentix/CRTM privado o en los archivos del Consorcio.
