# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Workarea\\Python\\Passwords_2\\Passwords\\Psswd.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Workarea\\Python\\Passwords_2\\Passwords\\information.json', '.'), ('C:\\Workarea\\Python\\Passwords_2\\Passwords\\key.key', '.'), ('C:\\Workarea\\Python\\Passwords_2\\Passwords\\passwords.enc', '.')],
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
    [],
    exclude_binaries=True,
    name='Psswd',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    name='Psswd',
)
