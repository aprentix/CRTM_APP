# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app_CRTM.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\images\\CRTM_LOGO.png', '.\\images'), ('.\\MANUAL.md', '.')],
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
    name='app_CRTM',
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
    version='C:\\Users\\ray\\AppData\\Local\\Temp\\adec1bbc-d83c-4974-86b5-5f45df0c4e2a',
    icon=['images\\CRTM_LOGO.png'],
)
