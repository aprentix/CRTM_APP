# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['your_program.py'],
    pathex=[],
    binaries=[],
    datas=[('images/CRTM_LOGO.png', 'assets'), ('MANUAL.md', 'assets'), ('script_generar_final.py', 'assets'), ('script_subir_archivos.py', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='your_program',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='C:\\Users\\ray\\AppData\\Local\\Temp\\277e4bcf-3790-457f-9e61-4257f093c33f',
)
