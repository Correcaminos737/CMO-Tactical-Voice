#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMO Combat Log Auditor & Offline Test Harness
==============================================
Audita masivamente todos los logs reales de Command: Modern Operations
para verificar la robustez del parser, clasificaciones y código Brevity
sin necesidad de jugar en vivo ni gastar tokens.

Uso:
    python tools\\audit_cmo_logs.py
    python tools\\audit_cmo_logs.py --max-files 5
    python tools\\audit_cmo_logs.py --verbose
"""

import os
import sys
import glob
import re
import time
import argparse

# Configurar salida UTF-8 para consola de Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DEFAULT_LOG_DIRS = [
    r"S:\SteamLibrary\steamapps\common\Command - Modern Operations\Logs",
    r"C:\SteamLibrary\steamapps\common\Command - Modern Operations\Logs",
    r"C:\Program Files (x86)\Steam\steamapps\common\Command - Modern Operations\Logs",
]

def find_log_dir() -> str:
    for d in DEFAULT_LOG_DIRS:
        if os.path.isdir(d):
            return d
    return ""

def main():
    parser = argparse.ArgumentParser(description="CMO Combat Log Auditor & Offline Test Harness")
    parser.add_argument("--dir", default="", help="Ruta a la carpeta Logs de CMO")
    parser.add_argument("--max-files", type=int, default=0, help="Limitar a los N logs más recientes (0 = todos)")
    parser.add_argument("--verbose", action="store_true", help="Mostrar detalle de cada evento procesado")
    args = parser.parse_args()

    log_dir = args.dir or find_log_dir()
    if not log_dir or not os.path.isdir(log_dir):
        print(f"❌ Error: No se encontró la carpeta Logs de CMO en las rutas habituales.")
        sys.exit(1)

    print("=" * 72)
    print("   CMO COMBAT LOG AUDITOR & OFFLINE TEST HARNESS")
    print("   Doctrina Brevity y Validación Masiva de Telemetría Táctica")
    print("=" * 72)
    print(f"📁 Directorio de Logs: {log_dir}")

    all_files = glob.glob(os.path.join(log_dir, "*.txt"))
    # Filtrar logs de excepción del motor de CMO y logs puros de Lua
    scenario_files = [
        f for f in all_files 
        if not os.path.basename(f).startswith(("ExceptionLog", "LuaHistory"))
    ]
    scenario_files.sort(key=os.path.getmtime, reverse=True)

    if args.max_files > 0:
        scenario_files = scenario_files[:args.max_files]

    print(f"📊 Archivos de escenario encontrados para auditar: {len(scenario_files)}")
    print("-" * 72)

    # Regex definitions conformes con v1.2.17
    re_timestamp_prefix = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*-\s*")
    re_line_side = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*-\s*\[(.*?)\]\s*(.*)$")

    re_destroyed = re.compile(r"(?:Unit:\s*)?([A-Za-z0-9\-\s,#\(\)\'\"\[\]\.]+?)\s+has (?:been destroyed|sunk|run out of fuel and crashed)", re.IGNORECASE)
    re_incoming_attack = re.compile(r"(?:Weapon:\s*)?([^:\n]+?)\s+is attacking\s+(.+?)(?:\s+with\b|\s*\.\s*$|$)", re.IGNORECASE)
    re_bda_report = re.compile(r"([A-Za-z0-9\-\s,#\(\)\'\"\[\]\.]+?)\s+reports BDA status change on contact:\s*(.*?)\s+-\s+((?:Light|Medium|Moderate|Heavy|Minor|Severe|No|Major|Critical|Conflagration)?\s*(?:damage|fire|flooding|destroyed|sunk|undamaged|capsizing).*)$", re.IGNORECASE)
    re_classified = re.compile(r"Contact:\s*([^:\n]+?)\s*has been (?:positively identified|classified|type-classified) as:\s*(.+?)(?:\s*-\s*Determined as:\s*([A-Za-z]+))?(?:\s*\((?:ID|Classification)\s+by:.*?\))?\s*$", re.IGNORECASE)
    re_departed = re.compile(r"([A-Za-z0-9\-\s,#\(\)\'\"\[\]\.]+?\([^)]+\))\s+departed\s+([^.\n]+?)(?:\s+and\s+is\s+waiting\s+for\s+orders)?\.", re.IGNORECASE)

    stats = {
        'total_lines': 0,
        'attacks_missile': 0,
        'attacks_torpedo': 0,
        'attacks_gun_silenced': 0,
        'kills_valid': 0,
        'damage_reports_silenced': 0,
        'bda_reports': 0,
        'contacts_id': 0,
        'departures': 0,
        'anomalies_bracket': 0,
        'anomalies_sensor_leak': 0,
    }

    anomalies = []
    t_start = time.time()

    for idx, fpath in enumerate(scenario_files, 1):
        fname = os.path.basename(fpath)
        file_lines = 0
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            for lnum, line in enumerate(fp, 1):
                raw = line.strip()
                if not raw:
                    continue
                file_lines += 1
                stats['total_lines'] += 1

                content = re_timestamp_prefix.sub("", raw).strip()
                m_s = re_line_side.match(raw)
                if m_s:
                    side = m_s.group(1).strip()
                    content = m_s.group(2).strip()
                else:
                    side = None

                # 1. Silenciado de subsistemas internos
                if "damage report:" in content.lower():
                    stats['damage_reports_silenced'] += 1
                    continue

                # 2. Destrucciones y bajas
                m_dest = re_destroyed.search(content)
                if m_dest:
                    tgt = m_dest.group(1).strip()
                    # Sanitize target prefixes
                    tgt_clean = tgt.strip()
                    if ']' in tgt_clean and tgt_clean.find(']') < len(tgt_clean)//2 and not tgt_clean.startswith(('Unit:', 'Contact:')):
                        tgt_clean = re.sub(r'^\s*\[?[^\]\n]*\]\s*', '', tgt_clean)
                    tgt_clean = re.sub(r'^\s*\[TARGET\[\s*', '', tgt_clean, flags=re.IGNORECASE)
                    tgt_clean = re.sub(r'^[\s\]\[/]+', '', tgt_clean).strip()
                    u_up = tgt_clean.upper()
                    # Check internal components
                    if any(comp in u_up for comp in ("MOUNT", "MAGAZINE", "TURRET", "TT", "RADAR", "ENGINE", "RADIO", "SONAR", "BURST", "DIRECTOR")):
                        stats['damage_reports_silenced'] += 1
                        continue
                    stats['kills_valid'] += 1
                    if tgt_clean.count('[') != tgt_clean.count(']'):
                        stats['anomalies_bracket'] += 1
                        anomalies.append((fname, lnum, "Paréntesis desbalanceados en Kill", tgt_clean))
                    if any(x in tgt_clean.lower() for x in ("id by:", "classification by:", "sensor:")):
                        stats['anomalies_sensor_leak'] += 1
                        anomalies.append((fname, lnum, "Fuga de sensor en Kill", tgt_clean))

                # 3. Intercambio balístico de armas
                m_atk = re_incoming_attack.search(content)
                if m_atk:
                    weapon = m_atk.group(1).strip()
                    target = m_atk.group(2).strip()
                    w_up = weapon.upper()
                    is_gun = any(g in w_up for g in (
                        "MM", "CAL", "GUN", "BURST", "SALVO", "CANNON", "SHELL", "HOWITZER",
                        "AK-", "MK-", "MK15", "PHALANX", "CIWS", "GOALKEEPER", "BOFORS", "OTO"
                    )) and not any(m in w_up for m in ("AIM", "RIM", "SAM", "MISSILE", "TORPEDO", "AGM"))
                    is_torp = "TORPEDO" in w_up or "45-36" in w_up or "53-65" in w_up or "SET-" in w_up
                    
                    if is_gun:
                        stats['attacks_gun_silenced'] += 1
                    elif is_torp:
                        stats['attacks_torpedo'] += 1
                    else:
                        stats['attacks_missile'] += 1

                    if target.count('[') != target.count(']'):
                        stats['anomalies_bracket'] += 1
                        anomalies.append((fname, lnum, "Paréntesis desbalanceados en Blanco", target))

                # 4. BDA de combate
                m_bda = re_bda_report.search(content)
                if m_bda:
                    stats['bda_reports'] += 1
                    c_tgt = m_bda.group(2).strip()
                    if c_tgt.count('[') != c_tgt.count(']'):
                        stats['anomalies_bracket'] += 1
                        anomalies.append((fname, lnum, "Paréntesis desbalanceados en BDA", c_tgt))

                # 5. Identificaciones de contacto
                m_id = re_classified.search(content)
                if m_id:
                    stats['contacts_id'] += 1

                # 6. Despegues
                m_dep = re_departed.search(content)
                if m_dep:
                    stats['departures'] += 1

        if args.verbose:
            print(f"  [{idx:02d}/{len(scenario_files):02d}] {fname} -> {file_lines} líneas procesadas.")

    duration = time.time() - t_start

    print("\n" + "=" * 72)
    print(f"✅ AUDITORÍA COMPLETADA EN {duration:.2f} SEGUNDOS")
    print("=" * 72)
    print(f"  • Total de líneas de combate escaneadas : {stats['total_lines']:,}")
    print(f"  • Contactos navales/aéreos identificados: {stats['contacts_id']:,}")
    print(f"  • Despegues y operaciones de vuelo     : {stats['departures']:,}")
    print(f"  • Ataques con misiles guiados          : {stats['attacks_missile']:,}")
    print(f"  • Carreras de torpedos en combate      : {stats['attacks_torpedo']:,}")
    print(f"  • Ráfagas de cañón/metralla silenciadas: {stats['attacks_gun_silenced']:,}")
    print(f"  • Bajas enemigas y aliadas validadas   : {stats['kills_valid']:,}")
    print(f"  • Averías internas y pañoles silenciados: {stats['damage_reports_silenced']:,}")
    print(f"  • Reportes de daños BDA procesados     : {stats['bda_reports']:,}")
    print("-" * 72)
    print(f"  • Anomalías de formato / corchetes     : {stats['anomalies_bracket']}")
    print(f"  • Fugas de texto técnico de sensores   : {stats['anomalies_sensor_leak']}")

    if anomalies:
        print("\n⚠️ Anomalías detectadas para pulir:")
        for a in anomalies[:10]:
            print(f"    [{a[0]}:{a[1]}] {a[2]} -> '{a[3]}'")
    else:
        print("\n🎉 ¡TODAS LAS LÍNEAS DE COMBATE CUMPLEN LA DOCTRINA BREVITY SIN ERRORES!")

    print("=" * 72)

if __name__ == "__main__":
    main()
