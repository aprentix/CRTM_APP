# INSTRUCCIONES APLICACIÓN GENERACIÓN ARCHIVOS EXCEL

## REQUISITOS:
- Los archivos tienen que tener el nombre original de descarga y no han de tener las hojas en orden modificado. Todos han de pertenecer al mismo mes. 

## NOMBRES DE LAS HOJAS A CARGAR
- BASE = "DATOS_BASE"
- VIA = "DATOS_VIA"
- BIT = "BIT"
- VAC_APP = "Vac_app"
- VAC_VAL = "Vac_val"

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

VIA = ['Concesion', 'Fecha', 'Nulinuser', 'Sublinea', 'Codtit', 'Coddes', 'Validaciones']

BIT = ['Concesion', 'Periodo', 'Codtit', 'Subidos', 'Coddes']

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
Manual usuario APP: https://docs.google.com/document/d/1OxDYcsYn9UWq-GU2fweTsBBJ5eM-45skSWKJ__kvl0s/edit?usp=sharing
