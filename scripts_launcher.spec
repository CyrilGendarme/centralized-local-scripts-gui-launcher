# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for building the Scripts Launcher executable.

Build command:
    pyinstaller scripts_launcher.spec

Or use the build script:
    python build.py
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('theme.py', '.'),
    ],
    hiddenimports=['tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
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
    name='ScriptsLauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app (no console window)
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Set to your icon path if desired
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScriptsLauncher',
)
