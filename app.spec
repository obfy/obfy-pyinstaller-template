# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for an obfy-protected app.
#
# This spec points at the PROTECTED tree in ./protected (produced by `obfy build`),
# NOT at ./src. Run `obfy build` first, then `pyinstaller app.spec`.
# (./dist is PyInstaller's own output dir, so the obfy mirror lives in ./protected.)

a = Analysis(
    ['protected/run.py'],            # protected entry-point stub (was src/run.py)
    pathex=[],
    binaries=[],
    datas=[('./protected/', './')],  # ship the whole mirror: stubs, __obfy__/, runtime
    hiddenimports=['obfy_runtime'],  # the native loader is imported dynamically
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
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
