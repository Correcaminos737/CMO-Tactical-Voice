#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMO Locator - Universal Path Detector for Command: Modern Operations
Version: 1.2.13
Author: Correcaminos / CMO War Room Community

Safely auto-detects the Command: Modern Operations installation and Logs folder
across all Windows drives, Steam libraries (via libraryfolders.vdf), and 
Matrix Games / Slitherine standalone registry entries.
"""

import os
import sys
import re
import string
import winreg
from typing import Optional, List

# Ensure safe console output across all Windows codepages (cp1252, cp437, etc.)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def get_all_windows_drives() -> List[str]:
    """Returns a list of all existing drive roots on this Windows PC (e.g. ['C:\\', 'D:\\', ...])."""
    drives = []
    for letter in string.ascii_uppercase:
        drive_path = f"{letter}:\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    return drives


def get_steam_library_folders() -> List[str]:
    """
    Parses Steam's registry and libraryfolders.vdf to find all Steam library locations
    configured by the user across multiple disks (C:, D:, E:, S:, etc.).
    """
    steam_roots = []
    for root_key in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for subkey in (r"Software\Valve\Steam", r"Software\WOW6432Node\Valve\Steam"):
            try:
                with winreg.OpenKey(root_key, subkey) as k:
                    val, _ = winreg.QueryValueEx(k, "SteamPath")
                    if val and os.path.exists(val):
                        steam_roots.append(os.path.normpath(val))
            except Exception:
                pass

    all_steam_libs = set(steam_roots)
    for sr in steam_roots:
        vdf_path = os.path.join(sr, "steamapps", "libraryfolders.vdf")
        if os.path.exists(vdf_path):
            try:
                with open(vdf_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        m = re.search(r'"path"\s+"([^"]+)"', line)
                        if m:
                            p = os.path.normpath(m.group(1).replace("\\\\", "\\"))
                            if os.path.exists(p):
                                all_steam_libs.add(p)
            except Exception:
                pass

    return list(all_steam_libs)


def detect_cmo_logs_dir(custom_path_override: Optional[str] = None) -> Optional[str]:
    """
    Locates the active 'Logs' folder of Command: Modern Operations.
    Order of discovery:
    1. Direct override parameter or local cmo_path.txt file
    2. Steam installation libraries (Registry + libraryfolders.vdf)
    3. Matrix Games / Slitherine Standalone Registry keys
    4. Fast drive-sweep across common default paths
    """
    # 1. Direct parameter override
    if custom_path_override and os.path.exists(custom_path_override):
        if os.path.basename(custom_path_override).lower() == "logs":
            return os.path.normpath(custom_path_override)
        sub_log = os.path.join(custom_path_override, "Logs")
        if os.path.exists(sub_log):
            return os.path.normpath(sub_log)

    # 1b. Check local config file override (cmo_path.txt)
    cfg_file = os.path.join(os.path.dirname(__file__), "cmo_path.txt")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                saved = f.read().strip()
                if saved and os.path.exists(saved):
                    if os.path.basename(saved).lower() == "logs":
                        return os.path.normpath(saved)
                    sub_log = os.path.join(saved, "Logs")
                    if os.path.exists(sub_log):
                        return os.path.normpath(sub_log)
        except Exception:
            pass

    # 1c. Check if placed directly inside CMO root directory (e.g. Command - Modern Operations/CMO-Tactical-Voice)
    parent_logs = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "Logs"))
    if os.path.exists(parent_logs) and os.path.isdir(parent_logs):
        return parent_logs

    local_logs = os.path.normpath(os.path.join(os.path.dirname(__file__), "Logs"))
    if os.path.exists(local_logs) and os.path.isdir(local_logs):
        return local_logs

    candidates = []

    # 2. Check Steam libraries
    steam_libs = get_steam_library_folders()
    for lib in steam_libs:
        cmo_log = os.path.join(lib, "steamapps", "common", "Command - Modern Operations", "Logs")
        if os.path.exists(cmo_log):
            candidates.append(os.path.normpath(cmo_log))

    # 3. Check Matrix Games / Slitherine standalone registry
    standalone_registry_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Matrix Games\Command Modern Operations"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Matrix Games\Command Modern Operations"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Slitherine\Command Modern Operations"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Slitherine\Command Modern Operations"),
        (winreg.HKEY_CURRENT_USER, r"Software\Matrix Games\Command Modern Operations"),
        (winreg.HKEY_CURRENT_USER, r"Software\WOW6432Node\Matrix Games\Command Modern Operations"),
    ]
    for root_k, subkey in standalone_registry_keys:
        try:
            with winreg.OpenKey(root_k, subkey) as k:
                for val_name in ("Path", "InstallPath", "TargetDir", "Folder"):
                    try:
                        val, _ = winreg.QueryValueEx(k, val_name)
                        if val and os.path.exists(val):
                            sub_logs = os.path.join(val, "Logs")
                            if os.path.exists(sub_logs):
                                candidates.append(os.path.normpath(sub_logs))
                    except Exception:
                        pass
        except Exception:
            pass

    # 4. Sweep common folders across all active Windows drives
    drives = get_all_windows_drives()
    common_subpaths = [
        r"SteamLibrary\steamapps\common\Command - Modern Operations\Logs",
        r"Program Files (x86)\Steam\steamapps\common\Command - Modern Operations\Logs",
        r"Program Files\Steam\steamapps\common\Command - Modern Operations\Logs",
        r"Steam\steamapps\common\Command - Modern Operations\Logs",
        r"Games\Command - Modern Operations\Logs",
        r"Games\Matrix Games\Command Modern Operations\Logs",
        r"Matrix Games\Command Modern Operations\Logs",
        r"Command - Modern Operations\Logs",
    ]
    for drive in drives:
        for sub in common_subpaths:
            full = os.path.normpath(os.path.join(drive, sub))
            if os.path.exists(full) and full not in candidates:
                candidates.append(full)

    if candidates:
        return candidates[0]
    return None


def save_cmo_path(path: str) -> None:
    """Saves a verified CMO path to cmo_path.txt for future zero-detection runs."""
    cfg_file = os.path.join(os.path.dirname(__file__), "cmo_path.txt")
    try:
        with open(cfg_file, "w", encoding="utf-8") as f:
            f.write(path.strip())
    except Exception:
        pass


if __name__ == "__main__":
    print("🔍 Testing CMO Auto-Locator v1.2...")
    found = detect_cmo_logs_dir()
    if found:
        print(f"✅ CMO Logs Directory Found:\n   {found}")
    else:
        print("❌ CMO Logs Directory not found automatically.")
