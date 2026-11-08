#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piper Voice Model Downloader for CMO Tactical Voice Advisor
Version: 1.2.17
Author: Correcaminos / CMO War Room Community

Safely downloads official Piper neural voice models directly from Hugging Face
(rhasspy/piper-voices) into the local voices/ directory on first launch.
Features:
- Resumable chunked downloads (HTTP Range) to survive socket drops (WinError 10054).
- Automatic reconnection and retries (up to 5 attempts).
- Auto-detection of user zip extraction locations (voices/voices/ or root en/es).
- Clear bilingual status output (EN/ES).
"""

import os
import sys
import shutil
import time
import ssl
import urllib.request
import urllib.error
from typing import Dict, List, Tuple

# Ensure safe console output across all Windows codepages
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_HF_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
GITHUB_RELEASES_URL = "https://github.com/Correcaminos737/CMO-Tactical-Voice/releases"

VOICE_CATALOG: Dict[str, Dict[str, str]] = {
    # SPANISH VOICES
    "es_davefx": {
        "lang": "es",
        "role": "J-3 Ops Officer (Karpov) / Critical Alarms",
        "rel_path": os.path.join("es", "es_ES", "davefx", "medium", "es_ES-davefx-medium.onnx"),
        "hf_subpath": "es/es_ES/davefx/medium/es_ES-davefx-medium.onnx"
    },
    "es_sharvard": {
        "lang": "es",
        "role": "J-2 Intel Officer (Siux) / J-5 BDA (Argos)",
        "rel_path": os.path.join("es", "es_ES", "sharvard", "medium", "es_ES-sharvard-medium.onnx"),
        "hf_subpath": "es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx"
    },
    "es_claude": {
        "lang": "es",
        "role": "Surface Warfare / Sonar Acoustic Officer",
        "rel_path": os.path.join("es", "es_MX", "claude", "high", "es_MX-claude-high.onnx"),
        "hf_subpath": "es/es_MX/claude/high/es_MX-claude-high.onnx"
    },
    # ENGLISH VOICES
    "en_ryan": {
        "lang": "en",
        "role": "Tactical Operations Officer / Air Ops Lead",
        "rel_path": os.path.join("en", "en_US", "ryan", "medium", "en_US-ryan-medium.onnx"),
        "hf_subpath": "en/en_US/ryan/medium/en_US-ryan-medium.onnx"
    },
    "en_lessac": {
        "lang": "en",
        "role": "Intelligence Officer (J-2) / Recon & ESM",
        "rel_path": os.path.join("en", "en_US", "lessac", "medium", "en_US-lessac-medium.onnx"),
        "hf_subpath": "en/en_US/lessac/medium/en_US-lessac-medium.onnx"
    },
    "en_bryce": {
        "lang": "en",
        "role": "Surface Warfare / Weapons Officer",
        "rel_path": os.path.join("en", "en_US", "bryce", "medium", "en_US-bryce-medium.onnx"),
        "hf_subpath": "en/en_US/bryce/medium/en_US-bryce-medium.onnx"
    },
    "en_alan": {
        "lang": "en",
        "role": "Subsurface / Sonar Acoustic Specialist (Royal Navy)",
        "rel_path": os.path.join("en", "en_GB", "alan", "medium", "en_GB-alan-medium.onnx"),
        "hf_subpath": "en/en_GB/alan/medium/en_GB-alan-medium.onnx"
    },
    "en_amy": {
        "lang": "en",
        "role": "Urgent CIC Alarms (Vampire, Torpedo inbound)",
        "rel_path": os.path.join("en", "en_US", "amy", "medium", "en_US-amy-medium.onnx"),
        "hf_subpath": "en/en_US/amy/medium/en_US-amy-medium.onnx"
    }
}


def _fix_extracted_voice_folders(base_voices_dir: str):
    """
    Quality-of-life helper: If a user manually extracts voices zip into the wrong
    subfolder (e.g., voices/voices/en or root/en), automatically move them into place.
    """
    root_dir = os.path.dirname(base_voices_dir)

    # 1. Check if user extracted inside voices/ creating voices/voices/
    nested_voices = os.path.join(base_voices_dir, "voices")
    if os.path.exists(nested_voices) and os.path.isdir(nested_voices):
        for item in os.listdir(nested_voices):
            src = os.path.join(nested_voices, item)
            dst = os.path.join(base_voices_dir, item)
            if not os.path.exists(dst):
                try:
                    shutil.move(src, dst)
                except Exception:
                    pass
        try:
            os.rmdir(nested_voices)
        except Exception:
            pass

    # 2. Check if user extracted into mod root creating root/en or root/es
    for lang_code in ("en", "es"):
        root_lang = os.path.join(root_dir, lang_code)
        target_lang = os.path.join(base_voices_dir, lang_code)
        if os.path.exists(root_lang) and os.path.isdir(root_lang) and not os.path.exists(target_lang):
            os.makedirs(base_voices_dir, exist_ok=True)
            try:
                shutil.move(root_lang, target_lang)
            except Exception:
                pass


def _download_with_progress(url: str, dest_file: str, description: str, lang: str = "es", max_retries: int = 5):
    """
    Downloads a file via HTTP with a clean in-console progress bar,
    supporting HTTP Range resume and automatic retries against connection drops (WinError 10054).
    """
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    temp_file = dest_file + ".tmp"

    headers_base = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    try:
        ssl_ctx = ssl.create_default_context()
    except Exception:
        ssl_ctx = ssl._create_unverified_context()

    print(f"📥 {description}...")

    for attempt in range(1, max_retries + 1):
        try:
            downloaded = os.path.getsize(temp_file) if os.path.exists(temp_file) else 0
            req_headers = dict(headers_base)
            if downloaded > 0:
                req_headers["Range"] = f"bytes={downloaded}-"

            req = urllib.request.Request(url, headers=req_headers)

            try:
                response = urllib.request.urlopen(req, context=ssl_ctx, timeout=30)
            except ssl.SSLError:
                response = urllib.request.urlopen(req, context=ssl._create_unverified_context(), timeout=30)

            with response:
                status = getattr(response, "status", 200)
                content_len = response.headers.get("Content-Length")

                if status == 206:
                    # Resumed download
                    total_size = downloaded + int(content_len) if content_len else 0
                    mode = "ab"
                else:
                    # Full download
                    total_size = int(content_len) if content_len else 0
                    downloaded = 0
                    mode = "wb"

                block_size = 131072  # 128 KB
                with open(temp_file, mode) as out_file:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        downloaded += len(buffer)
                        out_file.write(buffer)

                        if total_size > 0:
                            percent = min(100.0, downloaded / total_size * 100.0)
                            mb_curr = downloaded / (1024 * 1024)
                            mb_tot = total_size / (1024 * 1024)
                            bar_len = 25
                            filled = int(bar_len * downloaded // total_size)
                            filled = min(bar_len, max(0, filled))
                            bar = "=" * filled + ">" + " " * (bar_len - filled - 1) if filled < bar_len else "=" * bar_len
                            sys.stdout.write(f"\r   [{bar}] {percent:5.1f}% ({mb_curr:4.1f}/{mb_tot:4.1f} MB)")
                            sys.stdout.flush()

            # Verify downloaded size if total_size was known
            actual_size = os.path.getsize(temp_file)
            if total_size > 0 and actual_size < total_size:
                raise OSError(f"Incomplete download: {actual_size}/{total_size} bytes")

            sys.stdout.write("\n")
            if os.path.exists(dest_file):
                os.remove(dest_file)
            os.rename(temp_file, dest_file)
            return

        except Exception as exc:
            if attempt < max_retries:
                retry_msg = (
                    f"\n   ⚠️ Connection interrupted: {exc}. Resuming in 2s (Attempt {attempt}/{max_retries})..."
                    if lang == "en" else
                    f"\n   ⚠️ Conexión interrumpida: {exc}. Reanudando en 2s (Intento {attempt}/{max_retries})..."
                )
                print(retry_msg)
                time.sleep(2)
            else:
                sys.stdout.write("\n")
                raise


def ensure_voices_available(lang: str = "es", base_voices_dir: str = None) -> bool:
    """
    Checks if all required Piper voices for the specified language are present.
    If missing, downloads both the .onnx model and .onnx.json config from Hugging Face.
    """
    if base_voices_dir is None:
        base_voices_dir = os.path.join(os.path.dirname(__file__), "voices")

    # Auto-repair misplaced extraction if applicable
    _fix_extracted_voice_folders(base_voices_dir)

    target_lang = lang.lower() if lang else "es"
    target_voices = {k: v for k, v in VOICE_CATALOG.items() if v["lang"] == target_lang}
    if not target_voices:
        print(f"⚠️ Unsupported language code: '{lang}'. Defaulting to 'es'.")
        target_lang = "es"
        target_voices = {k: v for k, v in VOICE_CATALOG.items() if v["lang"] == "es"}

    missing_items = []
    for key, info in target_voices.items():
        onnx_local = os.path.join(base_voices_dir, info["rel_path"])
        json_local = f"{onnx_local}.json"
        if not os.path.exists(onnx_local) or not os.path.exists(json_local):
            missing_items.append((key, info, onnx_local, json_local))

    # Fast check: If missing, can we import existing files from dev workspace?
    dev_fallback = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "tools", "voices"))
    if os.path.exists(dev_fallback) and missing_items:
        still_missing = []
        for key, info, onnx_local, json_local in missing_items:
            dev_onnx = os.path.join(dev_fallback, info["rel_path"])
            dev_json = f"{dev_onnx}.json"
            if os.path.exists(dev_onnx) and os.path.exists(dev_json):
                os.makedirs(os.path.dirname(onnx_local), exist_ok=True)
                shutil.copy2(dev_onnx, onnx_local)
                shutil.copy2(dev_json, json_local)
                print(f"📦 Imported local model for {key} from dev workspace.")
            else:
                still_missing.append((key, info, onnx_local, json_local))
        missing_items = still_missing

    if not missing_items:
        return True

    print("=" * 70)
    if target_lang == "en":
        print("🎙️ FIRST LAUNCH: DOWNLOADING TACTICAL NEURAL VOICES [ENGLISH]")
        print("Official repository: Hugging Face (rhasspy/piper-voices)")
        print("This one-time download (~315 MB total) only runs once on initial setup.")
    else:
        print(f"🎙️ PRIMERA EJECUCIÓN: DESCARGANDO VOCES TÁCTICAS [{target_lang.upper()}]")
        print("Repositorio oficial: Hugging Face (rhasspy/piper-voices)")
        print("Esta descarga (~180 MB) solo se realiza una vez.")
    print("=" * 70)

    try:
        for idx, (key, info, onnx_local, json_local) in enumerate(missing_items, 1):
            onnx_url = BASE_HF_URL + info["hf_subpath"]
            json_url = f"{onnx_url}.json"

            if target_lang == "en":
                desc_onnx = f"[{idx}/{len(missing_items)}] Downloading {info['role']} ({os.path.basename(onnx_local)})"
                desc_json = f"   Config {os.path.basename(json_local)}"
            else:
                desc_onnx = f"[{idx}/{len(missing_items)}] Descargando {info['role']} ({os.path.basename(onnx_local)})"
                desc_json = f"   Configuración {os.path.basename(json_local)}"

            _download_with_progress(onnx_url, onnx_local, desc_onnx, lang=target_lang)
            _download_with_progress(json_url, json_local, desc_json, lang=target_lang)

        print("\n" + "=" * 70)
        if target_lang == "en":
            print("✅ All tactical neural voice models downloaded and verified successfully.")
        else:
            print("✅ Todas las voces neuronales se han descargado e instalado correctamente.")
        print("=" * 70 + "\n")
        return True

    except Exception as e:
        zip_asset_name = f"voices-{target_lang}.zip"
        print("\n" + "!" * 70)
        if target_lang == "en":
            print(f"❌ Error downloading voices from Hugging Face: {e}")
            print("\n💡 MANUAL DOWNLOAD OPTION:")
            print("   If your Antivirus, Firewall, or ISP connection drops large downloads,")
            print("   you can manually download the voice models directly as a single ZIP file:")
            print(f"   👉 {GITHUB_RELEASES_URL}")
            print(f"   Download '{zip_asset_name}' and extract it into your mod folder.")
        else:
            print(f"❌ Error al descargar voces de Hugging Face: {e}")
            print("\n💡 OPCIÓN DE DESCARGA MANUAL:")
            print("   Si tu antivirus, cortafuegos o proveedor de internet interrumpe descargas grandes,")
            print("   puedes descargar las voces directamente en un único archivo ZIP:")
            print(f"   👉 {GITHUB_RELEASES_URL}")
            print(f"   Descarga '{zip_asset_name}' y descomprímelo dentro de la carpeta del mod.")
        print("!" * 70 + "\n")
        return False


if __name__ == "__main__":
    lang_to_test = sys.argv[1] if len(sys.argv) > 1 else "es"
    print(f"Testing voice availability for '{lang_to_test}'...")
    success = ensure_voices_available(lang_to_test)
    print("Success:", success)
