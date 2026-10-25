# Matrix Games Forum Release Post Kit
## Ready to copy & paste to the CMO General or Modding Subforum

**Suggested Thread Title:**  
`[TOOL / RELEASE] CMO Tactical Voice Advisor v1.2 (Real-Time Neural Radio & CIC Watch Officers - 100% Free & Open Source)`

---

### English Post (For Matrix Games / Slitherine Forum)

Hi everyone,

As a fellow CMO scenario author (*Operation Absolute Resolve*, *The Hormuz Gauntlet*) and long-time player, I’ve always felt that one of the things missing in *Command: Modern Operations* is the immersion of hearing your Combat Information Center (CIC) and tactical watch team communicating over military radio in real time.

Today, I’m releasing **CMO Tactical Voice Advisor (v1.2 Community Edition)** — a 100% free, open-source, non-invasive tactical voice tool powered by local neural AI voices (Piper ONNX).

---

### 🎙️ What does it do?
The advisor runs alongside CMO and gives you a dedicated team of watch officers who narrate combat events as they unfold:

- 🚨 **Urgent Tactical Alarms:** Immediate warnings for incoming anti-ship missiles (*"Vampire! Vampire!"*) and torpedos in the water with bearings.
- 🎯 **Combat BDA & Splashes:** Instant radio reports when missiles hit, targets are destroyed, or ships are confirmed sunk.
- 📡 **Contact Classification:** Positive identification of hostile bandits, surface combatants, and subsurface threats (smartly filtering out civilian dhows, fishing trawlers, and airliners).
- ✈️ **Flight Operations:** Advisories when sections launch, when maintenance turnaround completes (*"Ready on deck"*), and when aircraft hit Bingo fuel and return to base.
- 🌊 **Submarine Telemetry:** Periscope observations and acoustic BDA updates from your subs.
- 📻 **Military Radio FX:** Built-in VHF/UHF tactical radio filtering and authentic intercom DSP.

---

### 🛡️ Safety, Security & Zero Bloat (Read Before Running)
I know the CMO community takes cybersecurity seriously (as we all should). This tool was built with strict safety principles:
1. **Zero Game Modification (100% Read-Only):** Does **NOT** inject DLLs, does **NOT** hook process memory, and does **NOT** alter game files. It simply reads the text log that CMO already writes to disk when you enable the native Message Log.
2. **Zero Compiled Binaries:** No opaque `.exe` files. Everything is plain-text Python (`.py`) and transparent 3-line `.bat` launchers that you can inspect in Notepad.
3. **100% Offline & Private:** Once the official public voice models are downloaded from Hugging Face on the first run, the tool runs completely offline. Zero telemetry, zero external connections.

---

### 🚀 Quick Start Guide (3 Simple Steps)

1. **Enable Message Log in CMO (10 seconds):**
   - Open CMO ➔ **Game** ➔ **Game Options** ➔ **Message Log** tab.
   - Check `[X] Write message log to file`.
2. **Install dependencies (Only once):**
   - Double-click `INSTALAR_DEPENDENCIAS.bat` (or run `pip install -r requirements.txt`).
3. **Run the Advisor:**
   - For English: Double-click **`START_VOICE_ENGLISH.bat`**
   - For Spanish: Double-click **`INICIAR_VOZ_ESPANOL.bat`**
   - The tool will automatically locate your CMO installation across your Steam or Matrix Games drives, preload the neural models into RAM, and start narrating.

---

### 📦 Download & Source Code
- **GitHub Repository:** [https://github.com/Correcaminos737/CMO-Tactical-Voice](https://github.com/Correcaminos737/CMO-Tactical-Voice)
- **VirusTotal Clean Report:** *(100% Clean / 0 detections on release zip)*

Feedback, bug reports, and suggestions are welcome! I hope this adds as much immersion and adrenaline to your CMO battles as it has to mine.

Good hunting, Commanders!

**Correcaminos**  
*CMO War Room Community*
