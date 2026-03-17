# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# ── Collect everything needed ─────────────────────────────────
streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all('streamlit')
altair_datas, altair_binaries, altair_hiddenimports         = collect_all('altair')
pandas_datas, pandas_binaries, pandas_hiddenimports         = collect_all('pandas')
pydeck_datas, pydeck_binaries, pydeck_hiddenimports         = collect_all('pydeck')
docx_datas, docx_binaries, docx_hiddenimports               = collect_all('docx')
reportlab_datas, reportlab_binaries, reportlab_hiddenimports = collect_all('reportlab')
qrcode_datas, qrcode_binaries, qrcode_hiddenimports         = collect_all('qrcode')
PIL_datas, PIL_binaries, PIL_hiddenimports                   = collect_all('PIL')
openpyxl_datas, openpyxl_binaries, openpyxl_hiddenimports   = collect_all('openpyxl')

# ── Your app files ────────────────────────────────────────────
app_datas = [
    ('app.py',                  '.'),
    ('generate_cards.py',       '.'),
    ('generate_cards_docx.py',  '.'),
]

all_datas = (
    app_datas +
    streamlit_datas +
    altair_datas +
    pandas_datas +
    pydeck_datas +
    docx_datas +
    reportlab_datas +
    qrcode_datas +
    PIL_datas +
    openpyxl_datas
)

all_binaries = (
    streamlit_binaries +
    altair_binaries +
    pandas_binaries +
    pydeck_binaries +
    docx_binaries +
    reportlab_binaries +
    qrcode_binaries +
    PIL_binaries +
    openpyxl_binaries
)

all_hiddenimports = (
    streamlit_hiddenimports +
    altair_hiddenimports +
    pandas_hiddenimports +
    pydeck_hiddenimports +
    docx_hiddenimports +
    reportlab_hiddenimports +
    qrcode_hiddenimports +
    PIL_hiddenimports +
    openpyxl_hiddenimports + [
    'streamlit',
    'streamlit.web',
    'streamlit.web.cli',
    'streamlit.web.server',
    'streamlit.runtime',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.components.v1',
    'pandas',
    'PIL',
    'PIL.Image',
    'reportlab',
    'docx',
    'qrcode',
    'openpyxl',
    'altair',
    'pydeck',
    'pkg_resources.py2_warn',
    'pkg_resources._vendor',
])

# ── Analysis ──────────────────────────────────────────────────
a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
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
    name='TentCardGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # No terminal window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ── Mac .app bundle ───────────────────────────────────────────
app = BUNDLE(
    exe,
    name='TentCardGenerator.app',
    icon=None,
    bundle_identifier='com.tentcard.generator',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleShortVersionString': '1.0.0',
    },
)
