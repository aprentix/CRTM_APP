## Día 14/12/2023
- [x] Tablas de lista_totales generadas correctamente.
> Falta que salgan los numeros en excel con separador decimal y lo detecte con formato numérico.
## Día 15/12/2023
> ¿Hay que hacer el apartado 4?
- [x] Poner en la tabla el Dif/Base, Bit/Via, Bit/Base
> Estamos en el punto 5 de la hoja, apartado "Análisis de la comparación de datos"
- [x] Entender la lógica de la aplicación a partir de las tablas.
- [x] Implementar la lógica básica.
## Día [18,19]/12/2023
- [x] Estudiar las diferentes opciones para hacer el front de la APP con Python. (y elegir una)
- [x] Aprender cómo funciona FLET
- [x] Comenzar con una interfaz básica
## Día 20/12/2023
- [x] Diseño de la app y ver que sea intuituitiva
## Día 21/12/2023
- [x] Hacer el manual de usuario de la app
- [x] Estudiar requisitos
- [x] Poner columna a parte del CE
## Día 22/12/2023
- [x] Hacer que se abra el menu de instrucciones markdown https://flet.dev/docs/controls/markdown/ 
- [x] Hacer el script base
## Día 26/12/2023
- [x] Separar los interurbanos en VCM y VAC (con los codigos que me ha enviado)
- [x] Ver cómo modificar los archivos que carga el usuario desde pyhton.
- [x] Hacer que funcione por cosola de comandos y genere correctamente el excel final por ahora.
- [x] Corregir fallos en la lógica del programa
- [x] Analizar las columnas antes de cargar el archivo
## Día [27, 28]/12/2023
- [x] Retocar la APP
- [x] Hacer que funcione la app y retorne los excel
- [x] Hacer que la app funcione
- [x] Hacer el manual de instrucciones de usuario.
- [x] Sacar mensajes de error al usuario
    - [x] Cuando los archivos no tienen los nombres de columnas que necesita.
    - [x] Cuando falta algún archivo.
    - [x] Cuando sobra algún archivo (solo opera con los que le interesa).
## Día 29/12/2023
- [+|-] Retocar la lógica
- [x] Separar las tablas interurbanos
- [x] Mejorar la interfaz para hacerla más visual
## Día 02/01/2024
- [x] Poner todas las tablas en un excel y que el usuario pueda nombrarlo.
- [x] Capturar cualquier error que se produzca
- [x] Hacer más interactiva la app para que el usuario vea los errores
- [x] Continuar con el manual de usuario
## Día [03/04/05]/01/2024
- [x] Hacer script independiente.
- [x] Corregir errores en los nombres de las columnas de la alerta al usuario.
## OTROS
- [x] Solucionar problemas de ejecucion del archivo Python en ordenadores del consorcio [llamar al equipo técnico, Ann]
- [ ] Empezar con la parte de descuentos???

## Corregir
- [ ] Corregir lo de los interurbanos que aparezcan sow
## Apuntes:
Para generar el ejecutable:
> flet pack app_CRTM.py --add-data ".\images\CRTM_LOGO.png;.\images" --add-data ".\MANUAL.md;." --icon ".\images\CRTM_LOGO.png"