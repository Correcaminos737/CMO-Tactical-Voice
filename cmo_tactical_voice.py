#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMO Tactical Voice Advisor - Community Edition
Version: 1.2.0
Author: Correcaminos & CMO War Room Community
Project: https://github.com/Correcaminos737/CMO-Tactical-Voice

Real-time Tactical Voice Advisory for Command: Modern Operations (CMO).
100% Non-invasive, read-only telemetry parser with local neural Piper ONNX voices.
Zero cloud dependencies, zero game modification, zero telemetry.
"""

import sys
import os
import time
import re
import queue
import threading
import ctypes
import io
import wave
import argparse
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple

# Ensure safe UTF-8 console output across all Windows codepages
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Import local helper modules
from cmo_locator import detect_cmo_logs_dir, save_cmo_path
from voice_downloader import ensure_voices_available

__version__ = "1.2.0"

# =============================================================================
# 1. VOICE CONFIGURATION & CATALOG
# =============================================================================

VOICE_DIR = os.path.join(os.path.dirname(__file__), "voices")

VOICE_CONFIG_ES = {
    "AIR": {
        "model": os.path.join(VOICE_DIR, "es", "es_ES", "davefx", "medium", "es_ES-davefx-medium.onnx"),
        "role": "Karpov (J-3 Ops Aire)",
        "speed": 1.05
    },
    "SURFACE": {
        "model": os.path.join(VOICE_DIR, "es", "es_MX", "claude", "high", "es_MX-claude-high.onnx"),
        "role": "Oficial de Superficie",
        "speed": 1.0
    },
    "SUB": {
        "model": os.path.join(VOICE_DIR, "es", "es_MX", "claude", "high", "es_MX-claude-high.onnx"),
        "role": "Oficial Sonar / ASW",
        "speed": 0.98
    },
    "INTEL": {
        "model": os.path.join(VOICE_DIR, "es", "es_ES", "sharvard", "medium", "es_ES-sharvard-medium.onnx"),
        "role": "Siux (J-2 Inteligencia)",
        "speed": 1.02
    },
    "CRITICAL": {
        "model": os.path.join(VOICE_DIR, "es", "es_ES", "davefx", "medium", "es_ES-davefx-medium.onnx"),
        "role": "Alarma CIC (Vampire/Torpedo)",
        "speed": 1.10
    },
    "BDA": {
        "model": os.path.join(VOICE_DIR, "es", "es_ES", "sharvard", "medium", "es_ES-sharvard-medium.onnx"),
        "role": "Argos (J-5 BDA)",
        "speed": 1.02
    }
}

VOICE_CONFIG_EN = {
    "AIR": {
        "model": os.path.join(VOICE_DIR, "en", "en_US", "ryan", "medium", "en_US-ryan-medium.onnx"),
        "role": "Tactical Air Ops Lead",
        "speed": 1.05
    },
    "SURFACE": {
        "model": os.path.join(VOICE_DIR, "en", "en_US", "bryce", "medium", "en_US-bryce-medium.onnx"),
        "role": "Surface Warfare Officer",
        "speed": 1.0
    },
    "SUB": {
        "model": os.path.join(VOICE_DIR, "en", "en_GB", "alan", "medium", "en_GB-alan-medium.onnx"),
        "role": "Subsurface Sonar Officer (RN)",
        "speed": 0.98
    },
    "INTEL": {
        "model": os.path.join(VOICE_DIR, "en", "en_US", "lessac", "medium", "en_US-lessac-medium.onnx"),
        "role": "Intelligence Officer (J-2)",
        "speed": 1.02
    },
    "CRITICAL": {
        "model": os.path.join(VOICE_DIR, "en", "en_US", "amy", "medium", "en_US-amy-medium.onnx"),
        "role": "Urgent CIC Alarms",
        "speed": 1.10
    },
    "BDA": {
        "model": os.path.join(VOICE_DIR, "en", "en_US", "ryan", "medium", "en_US-ryan-medium.onnx"),
        "role": "Strike Evaluation (BDA)",
        "speed": 1.02
    }
}

# Priorities
PRIORITY_CRITICAL = 1   # Vampires, torpedos, fatal hits (Interrupts)
PRIORITY_HIGH = 2       # Bandits, Kills, Splashes, Sunk ships, Bingo fuel
PRIORITY_NORMAL = 3     # Bogey, Skunk, flight ops, damage control

# Civil traffic filter (completely muted to prevent tactical spam)
CIVILIAN_KEYWORDS = (
    "CIVILIAN", "MERCHANT", "TANKER", "CRUDE OIL TANKER", "CARGO", "CONTAINER",
    "FISHING", "DHOW", "TRAWLER", "SURVEILLANCE", "AIRLINER", "COMMERCIAL",
    "BIOLOGIC", "WHALE", "NEUTRAL", "NON-COMBATANT", "UNCLASSIFIED CIVILIAN",
    "PASSENGER", "PLEASURE CRAFT", "BULK CARRIER"
)

MILITARY_KEYWORDS = (
    "BANDIT", "HOSTILE", "UNFRIENDLY", "BOGHAMMAR", "COMBATTANTE", "SILKWORM",
    "F-4", "F-14", "SU-24", "MIG-", "CORVETTE", "FRIGATE", "DESTROYER",
    "CRUISER", "SUBMARINE", "SSK", "SSN", "MISSILE BOAT", "PATROL CRAFT",
    "SAM", "BATTERY", "FIGHTER", "ATTACK", "BOMBER", "TORPEDO", "VAMPIRE",
    "WARSHIP", "FAC", "GUNBOAT"
)


def acquire_single_instance_lock():
    """Ensures only a single instance runs to prevent echo/sound collisions."""
    try:
        import subprocess
        my_pid = os.getpid()
        # Automatically terminate any orphan advisor instance to prevent duplicate audio
        kill_cmd = f'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object {{ $_.ProcessId -ne {my_pid} -and ($_.CommandLine -like \'*tactical_voice*\' -or $_.CommandLine -like \'*cmo_tactical_voice*\') }} | ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }}"'
        try:
            subprocess.run(kill_cmd, shell=True, capture_output=True, timeout=4)
            time.sleep(0.5)
        except Exception:
            pass

        kernel32 = ctypes.windll.kernel32
        mutex_name = "Global\\CMO_Tactical_Voice_Advisor_Mutex"
        mutex = kernel32.CreateMutexW(None, False, mutex_name)
        last_error = kernel32.GetLastError()
        ERROR_ALREADY_EXISTS = 183
        if last_error == ERROR_ALREADY_EXISTS:
            return None
        return mutex
    except Exception:
        return True


@dataclass(order=True)
class VoiceAlert:
    priority: int
    timestamp: float = field(compare=False)
    domain: str = field(compare=False)
    text_display: str = field(compare=False)
    text_speech: str = field(compare=False)
    ttl_seconds: float = field(compare=False, default=12.0)
    interrupt_current: bool = field(compare=False, default=False)
    is_radio: bool = field(compare=False, default=False)


# =============================================================================
# 2. PHONETIC HELPERS & MILITARY BREVITY
# =============================================================================

class PhoneticHelper:
    """Cleans technical CMO strings into natural military radio brevity."""

    @classmethod
    def clean_name(cls, raw: str) -> str:
        if not raw:
            return ""
        # 1. Strip bracketed system IDs first: [S-75M Volkhov], [5N69]
        text = re.sub(r'\[.*?\]', '', raw)
        # 2. If it has parentheses with a designation like (SA-2f Guideline), blend nicely
        m_par = re.search(r'\(([^)]+)\)', text)
        if m_par:
            inner = m_par.group(1).strip()
            outer = re.sub(r'\(.*?\)', '', text).strip()
            if any(w in outer.lower() for w in ["sam", "battery", "radar", "site", "bn", "airbase"]):
                text = f"{outer} {inner}"
            elif inner and len(inner) > 2:
                text = inner
            else:
                text = outer
        text = re.sub(r'\b(DDG-\d+|CG-\d+|SSN-\d+|SSK-\d+|FFG-\d+|CVN-\d+|USS|HMS)\b', '', text, flags=re.IGNORECASE)
        text = text.replace('#', ' ').replace('_', ' ')
        cleaned = re.sub(r'\s+', ' ', text).strip()
        if cleaned in (")", "(", "#", "-", "/", "No cargo"):
            return ""
        return cleaned

    @classmethod
    def clean_base(cls, raw: str) -> str:
        if not raw:
            return "su base"
        b = str(raw).strip()
        b = re.sub(r'\s+and\s+is\s+waiting\s+for\s+orders.*$', '', b, flags=re.IGNORECASE).strip()
        b = re.sub(r'\(.*?\)', '', b)
        b = re.sub(r'\[.*?\]', '', b)
        return re.sub(r'\s+', ' ', b).strip()

    @classmethod
    def clean_unit_callsign(cls, raw: str) -> str:
        """Translates unit strings like 'Strike Ftr #5 (F/A-18C Hornet)' to 'Hornet 5'."""
        if not raw:
            return ""
        text = re.sub(r"^\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*-\s*", "", raw)
        text = re.sub(r"^\[.*?\]\s*", "", text).strip()

        m_call = re.search(r'\[([A-Z\s0-9]+)\]', text)
        callsign = m_call.group(1).strip() if m_call else ""

        m_model = re.search(r'\(([^)]+)\)', text)
        model = m_model.group(1).strip() if m_model else ""

        m_num = re.search(r'#(\d+)', text)
        num_str = f" {m_num.group(1)}" if m_num else ""

        m_up = (model + " " + text).upper()
        if "HORNET" in m_up or "F/A-18" in m_up or "F-18" in m_up:
            base_name = f"Hornet{num_str}"
        elif "TOMCAT" in m_up or "F-14" in m_up:
            base_name = f"Tomcat{num_str}"
        elif "EAGLE" in m_up or "F-15" in m_up:
            base_name = f"F-15{num_str}"
        elif "VIPER" in m_up or "F-16" in m_up or "FALCON" in m_up:
            base_name = f"F-16{num_str}"
        elif "LIGHTNING" in m_up or "F-35" in m_up:
            base_name = f"F-35{num_str}"
        elif "RAPTOR" in m_up or "F-22" in m_up:
            base_name = f"F-22{num_str}"
        elif "TYPHOON" in m_up or "EUROFIGHTER" in m_up:
            base_name = f"Eurofighter{num_str}"
        elif "RAFALE" in m_up:
            base_name = f"Rafale{num_str}"
        elif "HARRIER" in m_up or "AV-8" in m_up:
            base_name = f"Harrier{num_str}"
        elif "HAWKEYE" in m_up or "E-2" in m_up:
            base_name = f"Hawkeye{num_str}"
        elif "SENTRY" in m_up or "E-3" in m_up:
            base_name = f"AWACS Sentry{num_str}"
        elif "PROWLER" in m_up or "EA-6" in m_up:
            base_name = f"Prowler{num_str}"
        elif "GROWLER" in m_up or "EA-18" in m_up:
            base_name = f"Growler{num_str}"
        elif "CORSAIR" in m_up or "A-7" in m_up:
            base_name = f"Corsair{num_str}"
        elif "INTRUDER" in m_up or "A-6" in m_up:
            base_name = f"Intruder{num_str}"
        elif "WARTHOG" in m_up or "A-10" in m_up:
            base_name = f"A-10{num_str}"
        elif "PHANTOM" in m_up or "F-4" in m_up:
            base_name = f"Phantom{num_str}"
        elif model:
            base_name = f"{model}{num_str}"
        else:
            base_name = cls.clean_name(text)

        if callsign:
            return f"{callsign.title()} ({base_name})"
        return base_name

    @classmethod
    def clean_weapon(cls, raw: str) -> str:
        if not raw:
            return ""
        clean = raw.split('#')[0].split('[')[0].strip()
        clean = re.sub(r'\b(Mod\s*\d+|LWT|ER|SARH|IR|ASM|AAM|SAM)\b', '', clean, flags=re.IGNORECASE).strip()
        return clean


# =============================================================================
# 3. TACTICAL VOICE ADVISOR CORE ENGINE
# =============================================================================

class CmoTacticalVoiceAdvisor:
    def __init__(self, lang: str = "es", debug: bool = True):
        self.lang = lang.lower() if lang.lower() in ("es", "en") else "es"
        self.debug = debug
        self.voice_config = VOICE_CONFIG_ES if self.lang == "es" else VOICE_CONFIG_EN
        self.alert_queue: queue.PriorityQueue[VoiceAlert] = queue.PriorityQueue()
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self._piper_cache: Dict[str, Any] = {}
        self.player_side: Optional[str] = None
        self.known_contacts: set = set()
        self.is_baseline_sync = False
        self.baseline_start_time = 0.0
        self.baseline_contacts_count = 0

        # Departure Section / Strike Package Batching
        self.departure_buffer: Dict[str, List[Dict[str, Any]]] = {}
        self.departure_lock = threading.Lock()
        self.departure_timer: Optional[threading.Timer] = None
        self.recent_flight_ops: Dict[str, float] = {}

    def notify_departure(self, unit_raw: str, base_raw: str):
        """Batches multi-ship takeoffs within 1.8s into a single military radio announcement."""
        now = time.time()
        c_unit = PhoneticHelper.clean_unit_callsign(unit_raw)
        c_base = PhoneticHelper.clean_base(base_raw)

        with self.departure_lock:
            if c_base not in self.departure_buffer:
                self.departure_buffer[c_base] = []
            self.departure_buffer[c_base].append({"raw": unit_raw, "clean": c_unit, "time": now})

            if self.departure_timer:
                self.departure_timer.cancel()
            self.departure_timer = threading.Timer(1.8, self._flush_departure_buffer)
            self.departure_timer.daemon = True
            self.departure_timer.start()

    def _flush_departure_buffer(self):
        with self.departure_lock:
            buffer_copy = {k: list(v) for k, v in self.departure_buffer.items()}
            self.departure_buffer.clear()
            self.departure_timer = None

        now = time.time()
        for base_name, items in buffer_copy.items():
            if not items:
                continue
            is_carrier = any(c in base_name.lower() for c in ["carrier", "portaaviones", "cvn", "cv", "lha", "lhd"])

            if self.lang == "es":
                caller = "Control de vuelo"
                if len(items) == 1:
                    u = items[0]["clean"]
                    disp = f"VUELO: {u} en el aire desde {base_name}."
                    speech = f"{caller}: {u} en el aire desde {base_name}."
                elif len(items) == 2:
                    u1 = items[0]["clean"]
                    disp = f"VUELO EN SECCIÓN: 2x aeronaves ({u1}) en el aire desde {base_name}."
                    speech = f"{caller}: Sección de dos aeronaves en el aire desde {base_name}."
                else:
                    count = len(items)
                    u_type = items[0]["clean"].split()[0]
                    disp = f"LANZAMIENTO EN PAQUETE: {count}x {u_type} en el aire desde {base_name}."
                    speech = f"{caller}: Paquete de {count} {u_type} en el aire desde {base_name}."
            else:
                caller = "Flight operations"
                if len(items) == 1:
                    u = items[0]["clean"]
                    disp = f"FLIGHT OPS: {u} airborne from {base_name}."
                    speech = f"{caller}: {u} airborne from {base_name}."
                elif len(items) == 2:
                    u1 = items[0]["clean"]
                    disp = f"SECTION DEPARTURE: 2-ship flight ({u1}) airborne from {base_name}."
                    speech = f"{caller}: 2-ship flight airborne from {base_name}."
                else:
                    count = len(items)
                    u_type = items[0]["clean"].split()[0]
                    disp = f"STRIKE PACKAGE: {count}x {u_type} airborne from {base_name}."
                    speech = f"{caller}: Strike package of {count} {u_type} airborne from {base_name}."

            self.alert_queue.put(VoiceAlert(
                priority=PRIORITY_NORMAL,
                timestamp=now,
                domain="AIR",
                text_display=disp,
                text_speech=speech,
                ttl_seconds=15.0
            ))

    def preload_voices(self):
        """Preloads Piper ONNX neural models into RAM for ultra-fast 150ms synthesis."""
        loaded = 0
        for dom, cfg in self.voice_config.items():
            model_path = cfg.get("model")
            if model_path and model_path not in self._piper_cache:
                voice = self._load_piper_model(model_path)
                if voice:
                    loaded += 1
        if self.debug and loaded > 0:
            lbl = "modelos neuronales locales precargados en memoria RAM." if self.lang == "es" else "local neural voice models preloaded into RAM."
            print(f"🎙️  {loaded} {lbl}")

    def _load_piper_model(self, model_path: str):
        if not model_path or not os.path.exists(model_path):
            return None
        if model_path in self._piper_cache:
            return self._piper_cache[model_path]

        config_path = f"{model_path}.json"
        if os.path.exists(model_path) and os.path.exists(config_path):
            try:
                from piper import PiperVoice
                voice = PiperVoice.load(model_path, config_path=config_path)
                self._piper_cache[model_path] = voice
                return voice
            except Exception as e:
                if self.debug:
                    print(f"⚠️ Piper load error ({os.path.basename(model_path)}): {e}")
        return None

    def start(self):
        self.running = True
        self.worker_thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self.worker_thread.start()

    def _dispatch_loop(self):
        while self.running:
            try:
                alert: VoiceAlert = self.alert_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            now = time.time()
            if now - alert.timestamp > alert.ttl_seconds:
                self.alert_queue.task_done()
                continue

            domain_icons = {
                "AIR": "✈️", "SURFACE": "🚢", "SUB": "🌊",
                "INTEL": "📡", "CRITICAL": "🚨", "BDA": "🎯"
            }
            icon = domain_icons.get(alert.domain, "🔊")
            prefix = "[CRÍTICO]" if alert.priority == PRIORITY_CRITICAL else "[TÁCTICO]"
            print(f"\n{icon} {prefix} {alert.text_display}")

            self._synthesize_and_play(alert)
            self.alert_queue.task_done()

    def _synthesize_and_play(self, alert: VoiceAlert):
        import winsound
        conf = self.voice_config.get(alert.domain, self.voice_config["AIR"])
        model_path = conf.get("model")
        voice = self._load_piper_model(model_path)

        if not voice:
            return

        try:
            mem_buf = io.BytesIO()
            with wave.open(mem_buf, "wb") as wav_mem:
                voice.synthesize_wav(alert.text_speech, wav_mem)

            mem_buf.seek(0)
            with wave.open(mem_buf, "rb") as r:
                sample_rate = r.getframerate()
                speech_bytes = r.readframes(r.getnframes())

            # Optional radio DSP processing (pedalboard)
            final_pcm = speech_bytes
            try:
                import numpy as np
                from pedalboard import Pedalboard, HighpassFilter, LowpassFilter, Compressor, Gain
                audio_float = np.frombuffer(speech_bytes, dtype=np.int16).astype(np.float32) / 32767.0

                if alert.is_radio:
                    dsp = Pedalboard([
                        HighpassFilter(cutoff_frequency_hz=350.0),
                        LowpassFilter(cutoff_frequency_hz=3200.0),
                        Compressor(threshold_db=-14.0, ratio=4.0),
                        Gain(gain_db=2.0)
                    ])
                else:
                    dsp = Pedalboard([
                        HighpassFilter(cutoff_frequency_hz=180.0),
                        Compressor(threshold_db=-10.0, ratio=2.0)
                    ])

                out_float = dsp(audio_float, sample_rate)
                clipped = np.clip(out_float * 32767.0, -32768.0, 32767.0).astype(np.int16)
                final_pcm = clipped.tobytes()
            except ImportError:
                pass

            final_buf = io.BytesIO()
            with wave.open(final_buf, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(sample_rate)
                w.writeframes(final_pcm)

            winsound.PlaySound(final_buf.getvalue(), winsound.SND_MEMORY)

        except Exception as e:
            if self.debug:
                print(f"⚠️ Audio playback error: {e}")


# =============================================================================
# 4. LOG PROCESSING & STREAMING DISPATCHER
# =============================================================================

def get_latest_cmo_log(log_dir: str) -> Optional[str]:
    if not log_dir or not os.path.exists(log_dir):
        return None
    candidates = []
    for f in os.listdir(log_dir):
        if f.endswith(".txt") and not f.startswith("ExceptionLog") and not f.startswith("LuaHistory"):
            full_path = os.path.join(log_dir, f)
            try:
                candidates.append((os.path.getmtime(full_path), full_path))
            except OSError:
                pass
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def detect_player_side(log_path: str) -> Optional[str]:
    if not log_path or not os.path.exists(log_path):
        return None
    last_side = None
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "Switched side to:" in line:
                    parts = line.split("Switched side to:")
                    if len(parts) > 1:
                        cand = parts[1].strip()
                        if cand:
                            last_side = cand
    except Exception:
        pass
    return last_side


US_SIDE_ALIASES = {
    "USN", "US NAVY", "U.S. NAVY", "UNITED STATES NAVY",
    "USAF", "US AIR FORCE", "U.S. AIR FORCE", "UNITED STATES AIR FORCE",
    "USA", "U.S.A.", "U.S.", "US", "UNITED STATES", "UNITED STATES OF AMERICA",
    "USMC", "US MARINE CORPS", "U.S. MARINES", "US MARINES",
    "BLUE", "NATO", "ALLIES", "ISRAEL", "IDF"
}

def is_player_side(line_side: Optional[str], player_side: Optional[str]) -> bool:
    """Verifies if an event's side belongs to the player or allied forces."""
    if not line_side or not player_side:
        return True
    ls = line_side.strip().upper()
    ps = player_side.strip().upper()
    if ls == ps:
        return True
    if ls in US_SIDE_ALIASES and ps in US_SIDE_ALIASES:
        return True
    if ls in ps or ps in ls:
        return True
    return False


def run_tactical_voice(lang: str = "es", side_override: str = ""):
    mutex = acquire_single_instance_lock()
    if not mutex:
        print("\n" + "=" * 70)
        if lang == "es":
            print("⚠️ [AVISO DE INSTANCIA PREVIA EN EJECUCIÓN]")
            print("Ya existe una ventana de la Voz Táctica abierta en este equipo.")
            print("Para evitar colisiones de audio, cierra la otra ventana antes de abrir una nueva.")
        else:
            print("⚠️ [PREVIOUS INSTANCE RUNNING]")
            print("An instance of CMO Tactical Voice Advisor is already running.")
            print("Please close the existing window to prevent overlapping audio.")
        print("=" * 70)
        try:
            input("\nPresiona ENTER / Press ENTER to exit...")
        except Exception:
            time.sleep(4)
        return

    banner_lang = "ESPAÑOL" if lang == "es" else "ENGLISH"
    print("=" * 70)
    print(f"🎙️  CMO TACTICAL VOICE ADVISOR - v{__version__} (Community Edition)")
    print(f"🎖️  IDIOMA / LANGUAGE: {banner_lang} | AUTOR: Correcaminos")
    print("=" * 70)

    # 1. Ensure voice models are ready
    if not ensure_voices_available(lang):
        print("❌ Cannot proceed without voice models. Aborting.")
        return

    # 2. Auto-locate CMO Logs directory
    log_dir = detect_cmo_logs_dir()
    if not log_dir or not os.path.exists(log_dir):
        print("\n⚠️ No se detectó automáticamente la carpeta de Logs de CMO.")
        print("   CMO Logs directory was not automatically detected.")
        prompt_txt = "Introduce la ruta de CMO Logs (ej: C:\\...\\Command - Modern Operations\\Logs): " if lang == "es" else "Enter CMO Logs path: "
        try:
            user_input = input(prompt_txt).strip().strip('"').strip("'")
            if user_input and os.path.exists(user_input):
                save_cmo_path(user_input)
                log_dir = detect_cmo_logs_dir()
        except Exception:
            pass

    if not log_dir or not os.path.exists(log_dir):
        print("❌ Error: No se puede conectar con CMO sin la carpeta de Logs.")
        input("Presiona ENTER para salir...")
        return

    print(f"📂 Carpeta de Logs enlazada: {log_dir}")

    # Initialize advisor
    advisor = CmoTacticalVoiceAdvisor(lang=lang, debug=True)
    advisor.preload_voices()
    advisor.start()

    # Welcome announcement
    if lang == "es":
        welcome_txt = "Sala de operaciones en línea. Modo inmersivo activado. Buena caza, Comandante."
        welcome_dsp = "Enlace táctico establecido con CMO (Español)."
    else:
        welcome_txt = "Tactical Operations Center online. Immersion mode active. Good hunting, Commander."
        welcome_dsp = "Tactical link established with CMO (English)."

    advisor.alert_queue.put(VoiceAlert(
        priority=PRIORITY_HIGH,
        timestamp=time.time(),
        domain="AIR",
        text_display=welcome_dsp,
        text_speech=welcome_txt,
        ttl_seconds=15.0
    ))

    active_log = get_latest_cmo_log(log_dir)
    if active_log:
        print(f"📄 Archivo de log activo: {os.path.basename(active_log)}")
    else:
        print(f"⏳ Esperando inicio de partida o creación de log en {log_dir}...")

    current_log = active_log
    file_pos = os.path.getsize(current_log) if current_log and os.path.exists(current_log) else 0
    if file_pos == 0:
        advisor.is_baseline_sync = True
        advisor.baseline_start_time = time.time()
        advisor.baseline_contacts_count = 0

    if side_override:
        advisor.player_side = side_override.strip()
        print(f"🎖️ Bando forzado: {advisor.player_side}")
    elif active_log:
        advisor.player_side = detect_player_side(active_log)
        if advisor.player_side:
            print(f"🎖️ Bando detectado: {advisor.player_side}")

    # Regex definitions
    re_side_switch = re.compile(r"Switched side to:\s*([^:\n\r]+)", re.IGNORECASE)
    re_line_side = re.compile(r"^\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*-\s*\[(.*?)\]\s*(.*)$")
    re_timestamp_prefix = re.compile(r"^\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*-\s*")
    re_vampire = re.compile(r"(?:VAMPIRE|Missile inbound).*?(?:at\s*(\d+)deg)?", re.IGNORECASE)
    re_torpedo = re.compile(r"Torpedo\s*(?:inbound|detected).*?(?:at\s*(\d+)deg)?", re.IGNORECASE)
    re_classified = re.compile(r"Contact:\s*([^:\n]+?)\s*has been (?:positively identified|classified|type-classified) as:\s*([^:\n]+?)(?:\s*-\s*Determined as:\s*([A-Za-z]+))?", re.IGNORECASE)
    re_hit = re.compile(r"Weapon:\s*([^:\n]+?)\s*(?:has impacted|has detonated near)\s*([^:\(\n]+)", re.IGNORECASE)
    re_destroyed = re.compile(r"(?:Unit:\s*)?([A-Za-z0-9\-\s,#\(\)\'\"\[\]\.]+?)\s+has (?:been destroyed|sunk|run out of fuel and crashed)", re.IGNORECASE)
    re_bingo = re.compile(r"Unit:\s*([^:\n]+?)\s*is BINGO FUEL", re.IGNORECASE)
    re_departed = re.compile(r"([A-Za-z0-9\-\s,#\(\)\'\"\[\]\.]+?\([^)]+\))\s+departed\s+([^.\n]+?)(?:\s+and\s+is\s+waiting\s+for\s+orders)?\.", re.IGNORECASE)
    re_rtb = re.compile(r"([A-Za-z0-9\-\s,#\(\)\'\"\[\]\.]+?\([^)]+\))\s+is returning to base\s*\(([^)]+)\)", re.IGNORECASE)
    re_bda_report = re.compile(
        r"([A-Za-z0-9\-\s,#\(\)\'\"\[\]\.]+?)\s+reports BDA status change on contact:\s*(.*?)\s+-\s+((?:Light|Medium|Moderate|Heavy|Minor|Severe|No)?\s*(?:damage|fire|destroyed|sunk|undamaged).*)$",
        re.IGNORECASE
    )

    print("\n🟢 Sistema activo. Despausa o avanza el tiempo en CMO (1x o Barra Espaciadora).")
    print("Para apagar el asesor, simplemente cierra esta ventana.\n")

    try:
        while True:
            latest = get_latest_cmo_log(log_dir)
            if latest and latest != current_log:
                print(f"\n🔄 Detectado nuevo log / escenario: {os.path.basename(latest)}")
                current_log = latest
                file_pos = 0
                if not side_override:
                    advisor.player_side = detect_player_side(current_log)
                advisor.is_baseline_sync = True
                advisor.baseline_start_time = time.time()
                advisor.baseline_contacts_count = 0
                advisor.known_contacts.clear()

            # Baseline absorption phase completion check
            if advisor.is_baseline_sync and (time.time() - advisor.baseline_start_time) > 4.5:
                advisor.is_baseline_sync = False
                if advisor.baseline_contacts_count > 0:
                    if lang == "es":
                        b_dsp = f"LÍNEA BASE DEL TEATRO: {advisor.baseline_contacts_count} trazas registradas en sector."
                        b_sp = f"Línea base establecida: {advisor.baseline_contacts_count} trazas registradas en el sector. A la escucha de nuevas amenazas."
                    else:
                        b_dsp = f"THEATER BASELINE: {advisor.baseline_contacts_count} tracks registered in sector."
                        b_sp = f"Theater baseline established: {advisor.baseline_contacts_count} tracks registered in sector. Standing by for new threats."

                    advisor.alert_queue.put(VoiceAlert(
                        priority=PRIORITY_NORMAL,
                        timestamp=time.time(),
                        domain="AIR",
                        text_display=b_dsp,
                        text_speech=b_sp,
                        ttl_seconds=15.0
                    ))

            if current_log and os.path.exists(current_log):
                curr_size = os.path.getsize(current_log)
                if curr_size < file_pos:
                    file_pos = 0
                if curr_size > file_pos:
                    with open(current_log, "r", encoding="utf-8", errors="ignore") as f:
                        f.seek(file_pos)
                        lines = f.readlines()
                        file_pos = f.tell()

                    for raw_line in lines:
                        raw_s = raw_line.strip()
                        if not raw_s:
                            continue

                        # Detect side switch events
                        m_sw = re_side_switch.search(raw_s)
                        if m_sw:
                            cand_side = m_sw.group(1).strip()
                            if cand_side:
                                advisor.player_side = cand_side
                                print(f"🎖️ Bando de operaciones activo: {advisor.player_side}")
                            continue

                        # Parse side prefix [Side] if present
                        m_side = re_line_side.match(raw_s)
                        if m_side:
                            line_side = m_side.group(1).strip()
                            line = m_side.group(2).strip()
                        else:
                            line_side = None
                            line = re_timestamp_prefix.sub("", raw_s).strip()

                        if not line:
                            continue

                        # 1. Vampire / Missile Inbound (Only against player/allies!)
                        m_vamp = re_vampire.search(line)
                        if m_vamp:
                            if is_player_side(line_side, advisor.player_side):
                                bearing = m_vamp.group(1)
                                if lang == "es":
                                    b_msg = f" con marcación {bearing}" if bearing else ""
                                    sp = f"¡Alerta Vampire! ¡Misil antibuque entrante{b_msg}!"
                                    dp = f"ALERTA VAMPIRE: Misil entrante{b_msg}."
                                else:
                                    b_msg = f" bearing {bearing}" if bearing else ""
                                    sp = f"Warning: Vampire! Missile inbound{b_msg}!"
                                    dp = f"VAMPIRE WARNING: Missile inbound{b_msg}."

                                advisor.alert_queue.put(VoiceAlert(
                                    priority=PRIORITY_CRITICAL,
                                    timestamp=time.time(),
                                    domain="CRITICAL",
                                    text_display=dp,
                                    text_speech=sp,
                                    ttl_seconds=14.0,
                                    interrupt_current=True,
                                    is_radio=True
                                ))
                            continue

                        # 2. Torpedo Inbound (Only against player/allies!)
                        m_torp = re_torpedo.search(line)
                        if m_torp:
                            if is_player_side(line_side, advisor.player_side):
                                bearing = m_torp.group(1)
                                if lang == "es":
                                    b_msg = f" por marcación {bearing}" if bearing else ""
                                    sp = f"¡Torpedo en el agua{b_msg}! ¡Maniobra evasiva inmediata!"
                                    dp = f"ALERTA TORPEDO: Torpedo en el agua{b_msg}."
                                else:
                                    b_msg = f" bearing {bearing}" if bearing else ""
                                    sp = f"Warning: Torpedo in the water{b_msg}! Initiate evasive action!"
                                    dp = f"TORPEDO WARNING: Inbound torpedo{b_msg}."

                                advisor.alert_queue.put(VoiceAlert(
                                    priority=PRIORITY_CRITICAL,
                                    timestamp=time.time(),
                                    domain="CRITICAL",
                                    text_display=dp,
                                    text_speech=sp,
                                    ttl_seconds=14.0,
                                    interrupt_current=True,
                                    is_radio=True
                                ))
                            continue

                        # 3. Unit Destroyed / Sunk
                        m_dest = re_destroyed.search(line)
                        if m_dest:
                            raw_unit = m_dest.group(1).strip()
                            clean_target = PhoneticHelper.clean_name(raw_unit)
                            if clean_target and clean_target not in (")", "(", "#", "-", "/", "No cargo") and len(clean_target) > 1:
                                is_sunk = "sunk" in line.lower()
                                domain = "SUB" if is_sunk else "BDA"

                                if lang == "es":
                                    verb = "hundido" if is_sunk else "destruido"
                                    sp = f"¡Impacto definitivo confirmado! Blanco {clean_target} {verb}."
                                    dp = f"KILL / SPLASH CONFIRMADO: {clean_target} {verb}."
                                else:
                                    verb = "sunk" if is_sunk else "destroyed"
                                    sp = f"Splash confirmed! Target {clean_target} {verb}."
                                    dp = f"KILL / SPLASH CONFIRMED: {clean_target} {verb}."

                                advisor.alert_queue.put(VoiceAlert(
                                    priority=PRIORITY_HIGH,
                                    timestamp=time.time(),
                                    domain=domain,
                                    text_display=dp,
                                    text_speech=sp,
                                    ttl_seconds=15.0
                                ))
                            continue

                        # 4. Weapon Hit
                        m_hit = re_hit.search(line)
                        if m_hit:
                            w_raw = m_hit.group(1).strip()
                            t_raw = m_hit.group(2).strip()
                            w_clean = PhoneticHelper.clean_weapon(w_raw)
                            t_clean = PhoneticHelper.clean_name(t_raw)

                            if lang == "es":
                                sp = f"Impacto confirmado en {t_clean} con {w_clean}."
                                dp = f"IMPACTO DIRECTO: {t_clean} alcanzado por {w_clean}."
                            else:
                                sp = f"Direct hit confirmed on {t_clean} with {w_clean}."
                                dp = f"DIRECT HIT: {t_clean} hit by {w_clean}."

                            advisor.alert_queue.put(VoiceAlert(
                                priority=PRIORITY_NORMAL,
                                timestamp=time.time(),
                                domain="BDA",
                                text_display=dp,
                                text_speech=sp,
                                ttl_seconds=12.0
                            ))
                            continue

                        # 5. Contact Classification
                        m_class = re_classified.search(line)
                        if m_class:
                            c_id = m_class.group(1).strip()
                            c_type = m_class.group(2).strip()
                            c_host = m_class.group(3).strip() if m_class.group(3) else "Hostile"

                            # Skip civilian traffic
                            if any(k in c_type.upper() for k in CIVILIAN_KEYWORDS):
                                continue

                            c_key = f"{c_id}:{c_type}"
                            if c_key in advisor.known_contacts:
                                continue
                            advisor.known_contacts.add(c_key)

                            # If in initial baseline sync (scenario start), absorb silently
                            if advisor.is_baseline_sync:
                                advisor.baseline_contacts_count += 1
                                continue

                            domain = "AIR" if any(a in c_type.upper() for a in ("FIGHTER", "BOMBER", "ATTACK", "AIRCRAFT")) else "SURFACE"

                            if lang == "es":
                                sp = f"Contacto {c_id} identificado positivamente como {c_type}."
                                dp = f"CONTACTO IDENTIFICADO: {c_id} -> {c_type} ({c_host})."
                            else:
                                sp = f"Contact {c_id} identified as {c_type}."
                                dp = f"CONTACT IDENTIFIED: {c_id} -> {c_type} ({c_host})."

                            advisor.alert_queue.put(VoiceAlert(
                                priority=PRIORITY_HIGH if c_host.upper() in ("HOSTILE", "UNFRIENDLY") else PRIORITY_NORMAL,
                                timestamp=time.time(),
                                domain=domain,
                                text_display=dp,
                                text_speech=sp,
                                ttl_seconds=15.0
                            ))
                            continue

                        # 6. Bingo Fuel
                        m_bingo = re_bingo.search(line)
                        if m_bingo:
                            u_name = PhoneticHelper.clean_name(m_bingo.group(1).strip())
                            if lang == "es":
                                sp = f"Aviso logístico: {u_name} en combustible Bingo. Regresando a base."
                                dp = f"LOGÍSTICA: {u_name} en combustible Bingo (RTB)."
                            else:
                                sp = f"Logistics advisory: {u_name} at Bingo fuel. Returning to base."
                                dp = f"LOGISTICS: {u_name} at Bingo fuel (RTB)."

                            advisor.alert_queue.put(VoiceAlert(
                                priority=PRIORITY_HIGH,
                                timestamp=time.time(),
                                domain="AIR",
                                text_display=dp,
                                text_speech=sp,
                                ttl_seconds=12.0
                            ))
                            continue

                        # 7. Section Departed (Takeoff - Only player/allied units)
                        m_dep = re_departed.search(line)
                        if m_dep:
                            if is_player_side(line_side, advisor.player_side):
                                advisor.notify_departure(unit_raw=m_dep.group(1).strip(), base_raw=m_dep.group(2).strip())
                            continue

                        # 8. Return to Base (RTB - Only player/allied units)
                        m_rtb = re_rtb.search(line)
                        if m_rtb:
                            if is_player_side(line_side, advisor.player_side):
                                c_unit = PhoneticHelper.clean_unit_callsign(m_rtb.group(1).strip())
                                c_base = PhoneticHelper.clean_base(m_rtb.group(2).strip())
                                now = time.time()
                                if (now - advisor.recent_flight_ops.get(c_unit, 0.0)) > 45.0:
                                    advisor.recent_flight_ops[c_unit] = now
                                    if lang == "es":
                                        sp = f"Control de vuelo: {c_unit} regresando a {c_base}."
                                        dp = f"REGRESO A BASE: {c_unit} regresa a {c_base}."
                                    else:
                                        sp = f"Flight operations: {c_unit} returning to {c_base}."
                                        dp = f"RTB: {c_unit} returning to {c_base}."

                                    advisor.alert_queue.put(VoiceAlert(
                                        priority=PRIORITY_NORMAL,
                                        timestamp=now,
                                        domain="AIR",
                                        text_display=dp,
                                        text_speech=sp,
                                        ttl_seconds=12.0
                                    ))
                            continue

                        # 9. BDA Report (Battle Damage Assessment)
                        m_bda = re_bda_report.search(line)
                        if m_bda:
                            raw_obs = m_bda.group(1).strip()
                            observer = PhoneticHelper.clean_name(raw_obs)
                            c_id = PhoneticHelper.clean_name(m_bda.group(2).strip())
                            bda_desc = m_bda.group(3).strip()

                            is_sub = any(s in raw_obs.lower() for s in ["sub", "ssn", "ssk", "submarine"])
                            domain = "SUB" if is_sub else "BDA"

                            if lang == "es":
                                desc_es = bda_desc
                                desc_es = re.sub(r'\bLight damage\b', 'daños ligeros', desc_es, flags=re.IGNORECASE)
                                desc_es = re.sub(r'\bMedium damage\b|\bModerate damage\b', 'daños moderados', desc_es, flags=re.IGNORECASE)
                                desc_es = re.sub(r'\bHeavy damage\b|\bHeavily damaged\b', 'daños graves', desc_es, flags=re.IGNORECASE)
                                desc_es = re.sub(r'\bNo Fire\b', 'sin fuego', desc_es, flags=re.IGNORECASE)
                                desc_es = re.sub(r'\bMinor fire\b', 'con fuego leve', desc_es, flags=re.IGNORECASE)
                                desc_es = re.sub(r'\bMajor fire\b', 'con incendios graves', desc_es, flags=re.IGNORECASE)
                                desc_es = re.sub(r'\bDestroyed\b', 'destruido', desc_es, flags=re.IGNORECASE)

                                if is_sub:
                                    sp = f"Informe de submarino {observer}: BDA en contacto {c_id}, {desc_es}."
                                    dp = f"ASW / BDA SUBMARINA: {observer} sobre {c_id} -> {desc_es}."
                                else:
                                    sp = f"Evaluación de ataque de {observer}: Blanco {c_id}, {desc_es}."
                                    dp = f"INFORME BDA: {observer} sobre {c_id} -> {desc_es}."
                            else:
                                if is_sub:
                                    sp = f"Submarine report from {observer}: BDA on contact {c_id}, {bda_desc}."
                                    dp = f"ASW / SUB BDA: {observer} on {c_id} -> {bda_desc}."
                                else:
                                    sp = f"Strike evaluation from {observer}: Target {c_id}, {bda_desc}."
                                    dp = f"BDA REPORT: {observer} on {c_id} -> {bda_desc}."

                            advisor.alert_queue.put(VoiceAlert(
                                priority=PRIORITY_HIGH,
                                timestamp=time.time(),
                                domain=domain,
                                text_display=dp,
                                text_speech=sp,
                                ttl_seconds=15.0
                            ))
                            continue

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n🛑 Asesor de voz detenido por el usuario.")
    finally:
        advisor.running = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"CMO Tactical Voice Advisor v{__version__}")
    parser.add_argument("--lang", choices=["es", "en"], default="es", help="Language: 'es' (Spanish) or 'en' (English)")
    parser.add_argument("--side", type=str, default="", help="Force player operational side (e.g. USN, NATO, Blue)")
    args = parser.parse_args()

    run_tactical_voice(lang=args.lang, side_override=args.side)
