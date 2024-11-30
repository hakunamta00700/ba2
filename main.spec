# -*- mode: python ; coding: utf-8 -*-

import os
import glob

block_cipher = None

# Windows DLL 경로 찾기
system32_path = os.path.join(os.environ['SystemRoot'], 'System32')
ucrt_dlls = glob.glob(os.path.join(system32_path, 'api-ms-win-*.dll'))
extra_binaries = []
for dll in ucrt_dlls:
    if os.path.exists(dll):
        extra_binaries.append((os.path.basename(dll), dll, 'BINARY'))

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=extra_binaries,
    datas=[],
    hiddenimports=['babel.numbers', 'tzdata', 'tkcalendar'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
