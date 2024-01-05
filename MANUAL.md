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

## COLUMNAS DE CADA TABLA:
BASE = ['Idconce', 'Fecha', 'Nexpe', 'Kms', 'Sencillo', 'Indicencia',
'Gratuitos', 'Recargo', 'Bonobus', 'Abottes', 'Pmun', 'Otros', 'Valman',
'Total', 'Ingsencillo', 'Ingrecargo', 'Ingtotal', 'Fichero',
'Fecha Proc']

VIA = ['CONCESION', 'FECHA', 'NULINUSER', 'SUBLINEA', 'CODTIT', 'TITULO',
'IDCODIGOPERFIL', 'CODDES', 'DESCUENTO', 'VALIDACIONES', 'FICHERO','F_PROCESO']

BIT = ['Operador', 'Concesion', 'Periodo', 'Codtit', 'Titulo', 'Subidos']

VAC_APP = ['Tipo', 'Empresa', 'Concesión/Linea', 'Titulo', 'Dscr Título', 'Fecha',
'Hora', 'Zona Validación', 'Validaciones']

VAC_VAL = ['Empresa', 'Fecha', 'Concesion', 'L Gestra', 'Desclinea', 'P Gestra',
'Descparada', 'Corona', 'Codtit', 'Titulo', 'Validaciones']


---

### AVISO: 
Es una mecanización, por ende, solo respeta procesos repetitivos y podria haber fallos si no se respetan los requisitos.

### Más info
Herramienta desarrollada para el departamento Comercial del CRTM en diciembre de 2023.
Desarrollo: Raquel DC (becaria) bajo la supervisión e instrucciones de Óscar Barrientos García.

Codigo en: https://github.com/aprentix/CRTM privado o en los archivos del Consorcio.
