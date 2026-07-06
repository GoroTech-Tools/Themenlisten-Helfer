# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

ROOT_DIR = Path(os.getcwd()).resolve()
SRC_DIR = ROOT_DIR / 'src'


a = Analysis(
    [str(SRC_DIR / 'ThemenlistenHelfer_GUI.py')],
    pathex=[str(SRC_DIR)],
    binaries=[],
    datas=[
        (str(ROOT_DIR / 'assets' / 'icons' / 'Themenlistenhelfer256.ico'), '.'),
        (str(ROOT_DIR / 'data' / 'Themenlisten-Vorlagen'), 'data/Themenlisten-Vorlagen'),
        (str(ROOT_DIR / 'output' / 'Themenlisten'), 'output/Themenlisten'),
        (str(ROOT_DIR / 'data' / 'Auswahl Teilnehmende zu Lernbereichen.xlsx'), 'data'),
        (str(ROOT_DIR / 'assets' / 'images' / 'Themenlistenhelfer.png'), 'assets/images'),
        (str(SRC_DIR / 'version.txt'), 'src'),
    ],
    hiddenimports=[],
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
    name='ThemenlistenHelfer',
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
    icon=[str(ROOT_DIR / 'assets' / 'icons' / 'Themenlistenhelfer256.ico')],
)
