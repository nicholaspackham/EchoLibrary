# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['/Users/nicholaspackham/_Projects/EchoLibrary'],
    binaries=[],
    datas=[('/Library/Tcl/tkdnd2.8', 'tkdnd2.8'), ('images/echo-library-icon.png', 'images')],
    hiddenimports=['tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Echo Library',
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
    icon=['images/echo-library-icon.png'],
)
app = BUNDLE(
    exe,
    name='Echo Library.app',
    icon='images/echo-library-icon.png',
    bundle_identifier=None,
)
