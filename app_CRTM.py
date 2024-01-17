import flet as ft
import flet
import re
import script_final as sf
import os
import sys
import pandas as pd
from exceptions_app import *

from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

from script_subir_archivos import ErrorArchivos, ErrorNombreColumnas, UserCancel

def main(page: Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    interurbanos_vcm_decision, interurbanos_vac_decision, vacs_decision = None, None, None
    directorios = {}
    page.window_width = 800
    manual_path = os.path.join(base_path, 'MANUAL.md')
    with open(manual_path, 'r', encoding="utf-8") as f:
        markdown_string = f.read()   
    table = markdown_string
    page.title = "Herramienta para el departamento de Comercio"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    texto_alert = ft.Text(
            value=str("ERROR")
    )
    def close_bs(e):
        snack_bar.open = False
        snack_bar.update()
        try:
            raise UserCancel()
        except UserCancel as e:
            raise

    snack_bar = ft.BottomSheet(
        ft.Container(
            ft.Row(
                [
                    ft.Text("Subiendo los archivos ..."),
                    ft.ElevatedButton("Cancelar", on_click=close_bs),
                ], alignment=ft.MainAxisAlignment.CENTER,
                tight=True,
            ),
            padding=10,
        ),dismissible=False,
        open=False,
    )
    page.overlay.append(snack_bar)
    # Pick files dialog
    def pick_files_result(e: FilePickerResultEvent):
        global decision_interurbanos_vcm, decision_interurbanos_vac, decision_vacs
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Suba los archivos!"
        )
        selected_files.update()
        for file_info in e.files:
            file_name = file_info.name
            if re.search(r".*BIT.*",file_name) != None:
                directorios['datos_bit']=file_info.path
            elif re.search(r".*BASE.*",file_name) != None:
                directorios['datos_base']=file_info.path
            elif re.search(r".*VIA.*",file_name) != None:
                directorios['datos_via']=file_info.path
            elif re.search(r".*Vac_app.*",file_name) != None:
                directorios['datos_vac_app']=file_info.path
            elif re.search(r".*Vac_val.*",file_name) != None:
                directorios['datos_vac_val']=file_info.path
        if len(directorios) == 5:
            try:
                boton_activado_.disabled = True
                boton_activado_.update()
                page.banner.open = False
                snack_bar.open = True
                page.update()
                decision_interurbanos_vcm, decision_vacs = sf.programa_final(directorios)
                snack_bar.open = False
                boton_activado_.disabled = False
                boton_activado_.update()
                page.update()
            except ErrorNombreColumnas as e:
                snack_bar.open = False
                print(e)
                texto_alert.value = str(e)
                texto_alert.update()
                page.banner.open = True
                page.update()
        else:
            try:
                raise ErrorArchivos("Faltan archivos, ha subido: ", str(selected_files))
            except ErrorArchivos as e:
                print(e)
                texto_alert.value = str(e)
                texto_alert.update()
                page.banner.open = True
                page.update()
            

    def click_boton(e):
        save_file_dialog.save_file()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()
    boton_activado_ = ft.ElevatedButton(content=ft.Text("GENERAR ARCHIVO", size=15), 
                                        height=70, on_click=click_boton, disabled=True,
                                        style=ft.ButtonStyle(
                            shape=ft.ContinuousRectangleBorder(radius=40),
                        ))

    # Save file dialog
    def save_file_result(e: FilePickerResultEvent):
        global decision_interurbanos_vcm, decision_interurbanos_vac, decision_vacs
        file_path = e.path+".xlsx"
        print(str(file_path))
        try:
            if file_path:
                directory_path = os.path.dirname(file_path)
                save_file_path.value = directory_path if e.path else "Descarga cancelada"
                os.makedirs(directory_path, exist_ok=True)
                with pd.ExcelWriter(file_path) as writer:
                    decision_interurbanos_vcm.to_excel(writer, "interurbanos_vcm", index_label=None)
                    decision_vacs.to_excel(writer, "vacs")
                print("ARCHIVOS CREADOS")
            else:
                print("NO PATH SELECTED")  
            save_file_path.update()
        except Exception as e:
            raise

    save_file_dialog = FilePicker(on_result=save_file_result)
    save_file_path = Text()

    page.overlay.extend([pick_files_dialog, save_file_dialog])

    image_path = os.path.join(base_path, 'images', 'CRTM_LOGO.png')
    img = ft.Image(
        src=image_path,
        height=150,
    )
   
    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [ft.Markdown(
                table,
                selectable=True,
                extension_set="gitHubWeb",
                code_theme="atom-one-dark",
                code_style=ft.TextStyle(font_family="Roboto Mono"),
                on_tap_link=lambda e: page.launch_url(e.data),
                )],scroll=ft.ScrollMode.ALWAYS,
        ),
        actions=[
            ft.TextButton("OK", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Dismissed"),
    )
    

    def open_dlg(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()
    
    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=texto_alert,
        content_padding=20,
        actions=[
            ft.TextButton("OK", on_click=close_banner),
        ],
    )

    page.add(
        ft.ResponsiveRow(
            [
            ft.Row(
                [img],
                alignment=ft.MainAxisAlignment.CENTER, spacing=50,
            ),ft.Divider(thickness=150, opacity=0.0),
            ft.Row(
                [
                    ElevatedButton(
                        content=ft.Column(
                                [
                                    ft.Row([ft.Icon(icons.UPLOAD_FILE, size=70),], 
                                        alignment=ft.MainAxisAlignment.CENTER,),
                                    ft.Row([ft.Text("Seleccione los archivos DATOS_VIA, DATOS_BASE, InformeBIT, Vac_app y Vac_val")],
                                        alignment=ft.MainAxisAlignment.CENTER,),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                        height=200,
                        width=700,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=True
                        ),
                        style=ft.ButtonStyle(
                            
                            shape=ft.ContinuousRectangleBorder(radius=40),
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,spacing=50,
            ),
            ft.Row([selected_files], alignment=ft.MainAxisAlignment.CENTER, spacing=50,),
            ft.Column(
                [ft.Row([ft.Column([boton_activado_], alignment=ft.MainAxisAlignment.CENTER, spacing=50,
                    ),
                ],alignment=ft.MainAxisAlignment.CENTER,spacing=50),
                ft.Row(
                    [save_file_path], alignment=ft.MainAxisAlignment.CENTER, spacing=50,),
                ], alignment=ft.MainAxisAlignment.CENTER,)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=50,
        ),
        ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.INFO, size=40)], alignment="center", spacing=5
        ), opacity=0.5, on_click=open_dlg,
    )
    )


app = flet.app(target=main)