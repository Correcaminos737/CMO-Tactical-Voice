# CMO Tactical Voice Advisor 🎙️
### Real-Time Neural Voice Advisory for Command: Modern Operations (CMO)
**Version:** (Community Edition)  
**Author:** Correcaminos (Author of *Operation Absolute Resolve*, *The Hormuz Gauntlet* , and other CMO scenarios)
**Platform:** Windows 10 / 11 (64-bit)  
**License:** Community Non-Commercial & Attribution 

---

[🇬🇧 English](#-english-guide) | [🇪🇸 Guía en Español](#-guía-en-español)

---

## 🇬🇧 English Guide

### Overview
**CMO Tactical Voice Advisor** turns your computer into an authentic military Combat Information Center (CIC). Using cutting-edge, ultra-fast local neural text-to-speech (Piper ONNX), dedicated tactical watch officers narrate combat events in real time as your scenario unfolds:

- 🚨 **Urgent Alarms:** Incoming anti-ship missiles (*"Vampire! Vampire!"*), torpedoes in the water with bearings.
- 🎯 **Combat BDA & Splashes:** Real-time confirmation of destroyed targets, missile hits, and acoustic sinkings.
- 📡 **Hostile Contact Classification:** Air, naval, and submarine identifications filtered from civilian traffic.
- ✈️ **Flight Operations:** Section takeoffs, strike package departures, Bingo fuel alerts, and return-to-base (RTB) approach calls.
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

### 🎛️ Total Customization: Control What the Voices Say!
You have 100% control over which tactical events are narrated without touching a single line of code:
- **Test with everything active:** When trying out the advisor, go to CMO **Game Options** ➔ **Message Log** and check all event types to experience the full immersion of an authentic military operations room.
- **Tailor to your taste:** If you only want critical combat alerts (Missiles, Torpedoes, BDA, Splashes) and prefer not to hear routine flight takeoffs or contact detections, simply **uncheck** those categories in CMO's Message Log tab.
- The advisor only narrates what you choose to log in CMO!

---

### 🧠 How It Works & Anti-Saturation Architecture
To deliver an authentic military radio atmosphere without turning your speakers into an overwhelming wall of noise, the advisor operates on several smart tactical principles:

- ⏱️ **Real-Time Log Tailing (No Historical Spam):**  
  When you launch the advisor with an ongoing game, it immediately jumps to the end of CMO's active log. It will **not** replay events from past hours—it only narrates what happens live from the exact second you unpause.

- 🛡️ **Theater Baseline Sync (Scenario Startup):**  
  When a new scenario begins at `00:00:00`, CMO dumps dozens of pre-existing map contacts at once (coastal radars, known airbases, initial patrols). Instead of machine-gunning you with 40 consecutive voice alerts, the advisor absorbs them silently during the first 4.5 seconds and broadcasts a single consolidated brevity report:  
  *"Theater baseline established: X tracks registered in sector. Standing by for new threats."*  
  From that moment on, any **new** contact detected during the mission is announced individually in real time.

- 🚢 **Civilian & Neutral Traffic Filter:**  
  Combat radio nets prioritize military threats. Commercial airliners, crude oil tankers, cargo freighters, fishing trawlers, and biological acoustic returns (whales) are automatically silenced.

- 🧠 **Smart Deduplication & Lag-Free TTL Queue:**  
  Radars constantly refresh tracks; the advisor remembers identified units and avoids repeating the same contact classification every few seconds. In massive battles, queued alerts expire after 15 seconds so you never experience audio lag behind the actual game state.

- 🧹 **Pro-Tip: CMO Logs Maintenance:**  
  If you play with all Message Log categories enabled, CMO creates a `.txt` log file for each mission that can grow over long sessions. We recommend occasionally clearing old `.txt` files from your CMO `Logs/` folder to save disk space and keep your simulator tidy!

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
- ✈️ **Operaciones Aeronavales:** Despegue de secciones en vuelo, lanzamientos en paquete, avisos de regreso a base (RTB) y alerta de combustible Bingo.
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

### 🎛️ Personalización Total: ¡Tú Decides Qué Quieres Escuchar!
Tienes control absoluto sobre qué avisos canta la radio militar sin tener que tocar código:
- **Prueba marcándolo todo:** Para tus primeras partidas de prueba, entra en CMO a **Game Options** ➔ pestaña **Message Log** y marca todas las categorías de eventos para vivir la experiencia inmersiva completa de una Sala de Operaciones táctica.
- **Filtra a tu gusto:** Si más adelante prefieres una radio más silenciosa centrada solo en combate crítico (Vampires, Torpedos, BDA y Derribos) y no quieres avisos rutinarios de despegues o contactos, simplemente **desmarca** esas casillas en el Message Log de CMO.
- ¡El Asesor solo narrará lo que tú decidas tener activado en tu simulador!

---

### 🧠 Cómo Funciona y Sistema Anti-Saturación
Para ofrecer una experiencia de radio militar realista sin convertir tus altavoces en una saturación de avisos caótica, el asesor sigue una serie de principios tácticos inteligentes:

- ⏱️ **Lectura en Tiempo Real (Sin Repetir el Pasado):**  
  Si abres el asesor con una partida ya en curso, el sistema salta directamente al final del archivo de log activo. **No reproducirá eventos pasados** de hace 20 minutos; solo narrará lo que ocurra en vivo desde el momento en que despauses o avances el tiempo en CMO.

- 🛡️ **Línea Base del Teatro (Arranque de Escenario):**  
  Al iniciar un escenario nuevo en el segundo `00:00:00`, CMO vuelca de golpe decenas de contactos preexistentes en el mapa (radares de costa, bases aéreas enemigas, patrullas fijas). En lugar de ametrallarte con 40 avisos consecutivos, el asesor los absorbe en silencio durante los primeros 4,5 segundos para registrarlos en su radar y emite un único reporte consolidado:  
  *«Línea base establecida: X trazas registradas en el sector. A la escucha de nuevas amenazas.»*  
  A partir de ese instante, cualquier **nuevo** contacto que aparezca o detecten tus radares durante la misión sí se anunciará individualmente.

- 🚢 **Filtro Estricto de Tráfico Civil y Neutral:**  
  La red de combate militar prioriza amenazas tácticas. Buques mercantes, petroleros, cargueros, barcos pesqueros, aviones comerciales y contactos biológicos (fauna marina / ballenas) son filtrados y silenciados automáticamente para mantener la frecuencia limpia.

- 🧠 **Deduplicación Inteligente y Cola sin Retraso (TTL):**  
  Tus sensores refrescan las trazas continuamente; el asesor recuerda qué unidades ya han sido cantadas para no repetir el mismo contacto cada 10 segundos. Si en un combate masivo coinciden decenas de eventos a la vez, las alertas en espera caducan tras 15 segundos para que la radio jamás acumule retraso respecto al juego.

- 🧹 **Consejo Útil: Mantenimiento de la Carpeta Logs de CMO:**  
  Si juegas con todas las casillas del Message Log activadas, CMO genera un archivo `.txt` por cada sesión que puede llegar a ocupar bastante espacio tras muchas horas de juego. Te recomendamos vaciar periódicamente los archivos `.txt` antiguos de la carpeta `Command - Modern Operations\Logs` para mantener tu disco limpio y el simulador ágil.

---

### Seguridad y Privacidad
Consulta nuestro [Manifiesto de Seguridad y Privacidad](docs/SECURITY_PRIVACY.md). El código es 100% abierto y auditable en texto plano.

---

### Créditos
Desarrollado con pasión para la comunidad de *Command: Modern Operations* por **Correcaminos** (diseñador de escenarios oficiales de la comunidad como *Operation Absolute Resolve* y *The Hormuz Gauntlet*) y el equipo de **CMO War Room**.
