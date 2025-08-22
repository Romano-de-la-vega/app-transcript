# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

ENTRYPOINT = "main_gui.py"   # ou "main.py"

try:
    BASE = Path(__file__).parent.resolve()
except NameError:
    BASE = Path(os.getcwd()).resolve()

datas = []
for src in ["templates", "static", "assets"]:
    p = BASE / src
    if p.exists():
        datas.append((str(p), src))

# assets Silero inclus avec faster_whisper
datas += collect_data_files("faster_whisper", includes=["assets/*"])

binaries = []
for exe in ["ffmpeg.exe", "ffprobe.exe"]:
    p = BASE / exe
    if p.exists():
        binaries.append((str(p), "."))

hiddenimports = [
    "uvicorn", "httptools", "websockets", "anyio", "starlette", "jinja2",
    "ctranslate2", "onnxruntime", "tokenizers", "huggingface_hub",
    "orjson", "ujson", "httpx", "pydantic",
]
hiddenimports += collect_submodules("uvicorn")
hiddenimports += collect_submodules("starlette")
hiddenimports += collect_submodules("anyio")
try:
    hiddenimports += collect_submodules("webview")
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

# chemins propres pour icon & version
icon_path = BASE / "static" / "icon.ico"
version_path = BASE / "version.rc"

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="TranscripteurWhisper",
    icon=str(icon_path) if icon_path.exists() else None,
    version=str(version_path) if version_path.exists() else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
