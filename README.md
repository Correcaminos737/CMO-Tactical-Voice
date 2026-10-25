# CMO Tactical Voice Advisor 🎙️
### Real-Time Neural Voice Advisory for Command: Modern Operations (CMO)
**Version:** 1.2.0 (Community Edition)  
**Author:** Correcaminos (Author of *Operation Absolute Resolve*, *The Hormuz Gauntlet*) & CMO War Room Community  
**Platform:** Windows 10 / 11 (64-bit)  
**License:** Community Non-Commercial & Attribution (CC BY-NC-SA 4.0 + Anti-Plagiarism)  

---

[🇬🇧 English](#-english-guide) | [🇪🇸 Guía en Español](#-guía-en-español)

---

## 🇬🇧 English Guide

### Overview
**CMO Tactical Voice Advisor** turns your computer into an authentic military Combat Information Center (CIC). Using cutting-edge, ultra-fast local neural text-to-speech (Piper ONNX), dedicated tactical watch officers narrate combat events in real time as your scenario unfolds:

- 🚨 **Urgent Alarms:** Incoming anti-ship missiles (*"Vampire! Vampire!"*), torpedoes in the water with bearings.
- 🎯 **Combat BDA & Splashes:** Real-time confirmation of destroyed targets, missile hits, and acoustic sinkings.
- 📡 **Hostile Contact Classification:** Air, naval, and submarine identifications filtered from civilian traffic.
- ✈️ **Flight Operations:** Section takeoffs, deck maintenance completion (*"Ready on deck"*), and Bingo fuel alerts.
- 🌊 **Subsurface Telemetry:** Submarine periscope BDA and acoustic sonar contacts.

> **100% Safe & Non-Invasive:** Does NOT modify CMO files, does NOT hook process memory, and uses NO compiled `.exe` files. Works purely in read-only mode by tailing CMO's native message log. Fully offline once voice models are cached.

---

### Quick Start (3 Steps)

1. **Enable Message Log in CMO:**
   - In CMO: Go to **Game** ➔ **Game Options** ➔ **Message Log** tab.
   - Check `[X] Write message log to file`. ([Detailed Guide](docs/CMO_MESSAGE_LOG_SETUP.md)).
2. **Install Dependencies (One-time):**
   - Double-click `INSTALAR_DEPENDENCIAS.bat` (or run `pip install -r requirements.txt`).
3. **Launch the Voice Advisor:**
   - Double-click **`START_VOICE_ENGLISH.bat`** (or `INICIAR_VOZ_ESPANOL.bat` for Spanish).
   - On the very first run, it will automatically download the official Piper neural models (~180 MB) directly from Hugging Face.
   - Start or unpause your CMO scenario and listen to your tactical crew!

---

### Voice Cast

| Operational Role | English Watch Officer | Spanish Watch Officer |
| :--- | :--- | :--- |
| **Tactical Air Lead / Ops (J-3)** | *Ryan* (USAF/USN Ops Lead) | *Davefx* (Karpov J-3) |
| **Intelligence Officer (J-2)** | *Lessac* (Intel Briefing Officer) | *Sharvard* (Siux J-2) |
| **Surface Warfare Officer** | *Bryce* (Tactical Action Officer) | *Claude* (Surface Action) |
| **Subsurface / Sonar Specialist** | *Alan* (Royal Navy Sonar Officer) | *Claude* (Sonar Acústico) |
| **Urgent CIC Alarms (Critical)** | *Amy* (Urgent Warning Officer) | *Davefx* (Alarma Táctica) |

---

## 🇪🇸 Guía en Español

### Descripción General
**CMO Tactical Voice Advisor** convierte tu PC en una auténtica Sala de Operaciones de Combate (CIC). Empleando síntesis neuronal local ultrarrápida (Piper ONNX), un equipo de oficiales tácticos narra los eventos de combate en tiempo real a medida que transcurre tu partida en Command: Modern Operations:

- 🚨 **Alarmas Críticas Inmediatas:** Misiles antibuque entrantes (*"¡Vampiro! ¡Vampiro!"*), torpedos en el agua con marcación.
- 🎯 **BDA y Derribos Confirmados:** Confirmación por radio de blancos destruidos, impactos directos y buques hundidos.
- 📡 **Clasificación de Contactos:** Detecciones aéreas, navales y submarinas con filtrado inteligente de tráfico civil.
- ✈️ **Operaciones Aeronavales:** Despegue de secciones en vuelo, aviso de aeronaves listas en cubierta y alerta de combustible Bingo.
- 🌊 **Guerra Submarina:** Confirmaciones acústicas por sonar y observaciones BDA por periscopio.

> **100% Seguro y No Invasivo:** NO modifica archivos de CMO, NO toca la memoria RAM del juego y NO contiene archivos `.exe` opacos. Funciona en modo solo lectura sobre el log oficial de CMO. Totalmente offline tras descargar los modelos.

---

### Inicio Rápido (3 Pasos)

1. **Activar el Message Log en CMO:**
   - En CMO: Ve a **Game** ➔ **Game Options** ➔ pestaña **Message Log**.
   - Marca la casilla `[X] Write message log to file`. ([Guía detallada](docs/CMO_MESSAGE_LOG_SETUP.md)).
2. **Instalar Dependencias (Solo la primera vez):**
   - Haz doble clic en `INSTALAR_DEPENDENCIAS.bat` (o escribe `pip install -r requirements.txt`).
3. **Iniciar el Asesor de Voz:**
   - Haz doble clic en **`INICIAR_VOZ_ESPANOL.bat`** (o `START_VOICE_ENGLISH.bat` para inglés).
   - En el primer arranque, descargará automáticamente las voces oficiales de Piper (~180 MB) desde Hugging Face.
   - ¡Despausa tu escenario en CMO y disfruta de la inmersión militar!

---

### Seguridad y Privacidad
Consulta nuestro [Manifiesto de Seguridad y Privacidad](docs/SECURITY_PRIVACY.md). El código es 100% abierto y auditable en texto plano.

---

### Créditos
Desarrollado con pasión para la comunidad de *Command: Modern Operations* por **Correcaminos** (diseñador de escenarios oficiales de la comunidad como *Operation Absolute Resolve* y *The Hormuz Gauntlet*) y el equipo de **CMO War Room**.
