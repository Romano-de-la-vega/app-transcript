# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# === Point d'entrée ===
ENTRYPOINT = "main_gui.py"   # ou "main.py" si besoin

# === BASE robuste (emplacement du .spec) ===
try:
    BASE = Path(__file__).parent.resolve()
except NameError:
    BASE = Path(os.getcwd()).resolve()

# === Données à EMBARQUER dans l'exe ===
datas = []
for src in ["templates", "static", "assets"]:
    p = BASE / src
    if p.exists():
        # (source_absolue, chemin_relatif_dans_le_bundle)
        datas.append((str(p), src))

# Assets internes de faster_whisper (silero_vad.onnx, etc.)
datas += collect_data_files("faster_whisper", includes=["assets/*"])

# === Binaries optionnels (ffmpeg) ===
binaries = []
for exe in ["ffmpeg.exe", "ffprobe.exe"]:
    p = BASE / exe
    if p.exists():
        binaries.append((str(p), "."))

# === Imports cachés utiles ===
hiddenimports = [
    "uvicorn", "httptools", "websockets", "anyio", "starlette", "jinja2",
    "ctranslate2", "onnxruntime", "tokenizers", "huggingface_hub",
    "orjson", "ujson", "httpx", "pydantic",
]
hiddenimports += collect_submodules("uvicorn")
hiddenimports += collect_submodules("starlette")
hiddenimports += collect_submodules("anyio")
try:
    hiddenimports += collect_submodules("webview")  # pour main_gui.py
except Exception:
    pass

block_cipher = None

a = Analysis(
    [ENTRYPOINT],
    pathex=[str(BASE)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,                   # <- important pour one-file
    name="TranscripteurWhisper",
    icon=str(BASE / "icon.ico") if (BASE / "icon.ico").exists() else None,
    version=str(BASE / "version.rc") if (BASE / "version.rc").exists() else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                 # évite certains soucis sur Windows
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,             # mets True pour voir la console en debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
