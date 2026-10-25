#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piper Voice Model Downloader for CMO Tactical Voice Advisor
Version: 1.2.0
Author: Correcaminos / CMO War Room Community

Safely downloads official Piper neural voice models directly from Hugging Face
(rhasspy/piper-voices) into the local voices/ directory on first launch.
100% transparent, uses standard Python urllib with progress reporting.
"""

import os
import sys
import shutil
import urllib.request
from typing import Dict, List, Tuple

# Ensure safe console output across all Windows codepages
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_HF_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/"

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


def _download_with_progress(url: str, dest_file: str, description: str):
    """Downloads a file via HTTP with a clean in-console progress bar."""
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    temp_file = dest_file + ".tmp"

    print(f"📥 {description}...")
    headers = {"User-Agent": "CMO-Tactical-Voice-Downloader/1.2"}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response, open(temp_file, "wb") as out_file:
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        block_size = 65536  # 64 KB blocks

        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            downloaded += len(buffer)
            out_file.write(buffer)

            if total_size > 0:
                percent = downloaded / total_size * 100.0
                mb_curr = downloaded / (1024 * 1024)
                mb_tot = total_size / (1024 * 1024)
                bar_len = 25
                filled = int(bar_len * downloaded // total_size)
                bar = "=" * filled + ">" + " " * (bar_len - filled - 1) if filled < bar_len else "=" * bar_len
                sys.stdout.write(f"\r   [{bar}] {percent:5.1f}% ({mb_curr:4.1f}/{mb_tot:4.1f} MB)")
                sys.stdout.flush()

    sys.stdout.write("\n")
    if os.path.exists(dest_file):
        os.remove(dest_file)
    os.rename(temp_file, dest_file)


def ensure_voices_available(lang: str = "es", base_voices_dir: str = None) -> bool:
    """
    Checks if all required Piper voices for the specified language are present.
    If missing, downloads both the .onnx model and .onnx.json config from Hugging Face.
    """
    if base_voices_dir is None:
        base_voices_dir = os.path.join(os.path.dirname(__file__), "voices")

    # Filter catalog for the selected language
    target_voices = {k: v for k, v in VOICE_CATALOG.items() if v["lang"] == lang.lower()}
    if not target_voices:
        print(f"⚠️ Unsupported language code: '{lang}'. Defaulting to 'es'.")
        target_voices = {k: v for k, v in VOICE_CATALOG.items() if v["lang"] == "es"}

    missing_items = []
    for key, info in target_voices.items():
        onnx_local = os.path.join(base_voices_dir, info["rel_path"])
        json_local = f"{onnx_local}.json"
        if not os.path.exists(onnx_local) or not os.path.exists(json_local):
            missing_items.append((key, info, onnx_local, json_local))

    # Fast check: If missing, can we import existing files from ../../tools/voices during development?
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
    print(f"🎙️ PRIMERA EJECUCIÓN: DESCARGANDO VOCES TÁCTICAS [{lang.upper()}]")
    print("Repositorio oficial: Hugging Face (rhasspy/piper-voices)")
    print("Esta descarga (~180 MB) solo se realiza una vez.")
    print("=" * 70)

    try:
        for idx, (key, info, onnx_local, json_local) in enumerate(missing_items, 1):
            onnx_url = BASE_HF_URL + info["hf_subpath"]
            json_url = f"{onnx_url}.json"
            desc = f"[{idx}/{len(missing_items)}] Descargando {info['role']} ({os.path.basename(onnx_local)})"

            _download_with_progress(onnx_url, onnx_local, desc)
            _download_with_progress(json_url, json_local, f"   Configuración {os.path.basename(json_local)}")

        print("\n✅ Todas las voces neuronales se han descargado e instalado correctamente.")
        print("=" * 70 + "\n")
        return True

    except Exception as e:
        print(f"\n❌ Error al descargar voces de Hugging Face: {e}")
        print("Por favor verifica tu conexión a internet o intenta de nuevo.")
        return False


if __name__ == "__main__":
    lang_to_test = sys.argv[1] if len(sys.argv) > 1 else "es"
    print(f"Testing voice availability for '{lang_to_test}'...")
    success = ensure_voices_available(lang_to_test)
    print("Success:", success)
