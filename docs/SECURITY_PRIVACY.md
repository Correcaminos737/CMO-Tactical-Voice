# Security & Privacy Manifest
# Manifiesto de Seguridad y Privacidad

**Version:** 1.2.0  
**Project:** CMO Tactical Voice Advisor  
**Author:** Correcaminos & CMO War Room Community  

---

## English

### 1. Zero Game Modification (100% Read-Only)
- This tool does **NOT** inject DLLs, does **NOT** read or hook game process memory, and does **NOT** modify any game executable or scenario file.
- It operates strictly in **read-only mode**, monitoring the standard text log file (`.txt`) that CMO natively writes to your local disk when `Write message log to file` is enabled.
- Your game installation, steam integrity checks, and multiplayer compatibility remain 100% untouched.

### 2. 100% Offline & Local AI (Zero Telemetry)
- Once the initial neural voice models (`.onnx`) are cached from Hugging Face on the first run, the tool works completely **offline**.
- No external server connections are ever opened during gameplay.
- No player data, logs, or analytics are collected, transmitted, or stored outside your own computer.

### 3. Open Source & Transparent
- All code is distributed in plain text (`.py` and `.bat`).
- There are no compiled, obfuscated `.exe` binaries.
- Anyone can inspect every single line of code with Notepad before running.

---

## Español

### 1. Cero Modificación del Juego (100% Solo Lectura)
- Esta herramienta **NO** inyecta DLLs, **NO** lee ni intercepta la memoria RAM de CMO y **NO** modifica ningún archivo ejecutable ni escenario.
- Opera estrictamente en **modo solo lectura**, monitorizando el archivo de texto estándar (`.txt`) que CMO escribe de forma nativa en disco cuando activas la casilla `Write message log to file`.
- La integridad de tu juego en Steam o Matrix Games permanece intacta.

### 2. 100% Local y Sin Conexión (Cero Telemetría)
- Una vez descargadas las voces neuronales oficiales (`.onnx`) desde Hugging Face en el primer arranque, la herramienta funciona completamente **offline**.
- No realiza conexiones a ningún servidor externo durante tus partidas.
- No se recopila ni envía ningún dato, log o estadística fuera de tu PC.

### 3. Código Abierto y Totalmente Transparente
- Todo el código se distribuye en texto plano (`.py` y `.bat`).
- No contiene archivos binarios ejecutables opacos (`.exe`).
- Cualquier usuario puede abrir y revisar cada línea de código con el Bloc de Notas antes de ejecutarlo.
