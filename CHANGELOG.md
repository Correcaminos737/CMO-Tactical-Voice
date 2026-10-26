# CHANGELOG - CMO TACTICAL VOICE ADVISOR

All notable changes to the CMO Tactical Voice Advisor project are documented here.
The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

---

## [1.2.11] - 2026-10-26

### 🚀 Facilidad de Instalación, Auto-Detección y Kills Confirmados / Installation & Detection Polish
- **Auto-Detección Relativa en Carpeta de CMO / Root Folder Discovery:**
  - `cmo_locator.py` ahora comprueba si la carpeta del asesor está descomprimida directamente dentro de la instalación de Command: Modern Operations (`..\Logs`), garantizando enlace instantáneo sin configuración para cualquier instalación en discos secundarios o rutas personalizadas.
- **Soporte Completo en Inglés / Dedicated English Installer:**
  - Añadido `INSTALL_DEPENDENCIES.bat` en inglés junto a `INSTALAR_DEPENDENCIAS.bat`.
  - Los scripts `.bat` ahora detectan tanto `python` como el launcher oficial `py -3` de Windows, ofreciendo mensajes de error limpios y enlaces de ayuda si Python no está presente.
- **Reordenamiento de Kills y Niebla de Guerra / Enemy Splashes vs Fog of War:**
  - El evaluador de bajas enemigas ahora se procesa antes de aislar la telemetría hostil. CMO etiqueta los derribos enemigos bajo el bando de la víctima (`[Russia] ... destroyed!`), por lo que ahora los derribos y buques hundidos se anuncian inmediatamente como Kills confirmados antes de bloquear los radares y sensores enemigos.
- **Instrucciones Claras en README y Foro:**
  - Clarificado que el asesor funciona como una Consola de Radio Táctica ultraligera en segundo plano (terminal sin GUI pesada) y simplificada la guía de instalación a 3 pasos directos.

---

## [1.2.1] - 2026-10-25

### 🛡️ Optimización de Voz, Supresión de AAA y Debounce / Combat Audio Polish
- **Supresión de Spam de AAA, Balas y Proyectiles:**
  - Se eliminan por completo los avisos continuos de ráfagas de ametralladoras, cañones y proyectiles antiaéreos (AAA de 12.7mm, 23mm, 37mm, 57mm, Vulcan, etc.). No más interrupciones repetitivas ni falsos positivos de "fuego naval" sobre tierra.
  - La confirmación de derribos e impactos definitivos (Kills/Splashes y Bajas Aliadas) se mantiene intacta al 100%.
  - Las alertas críticas de misiles guiados (SAM, AAM, Vampire, Torpedo) y RWR continúan teniendo prioridad inmediata.
- **Deduplicación y Filtro Anti-Rebote (Debounce Multi-Bando):**
  - Incorporada caché de supresión de duplicados: 30 segundos en bajas aliadas, 20 segundos en derribos de blancos hostiles y 15 segundos en informes BDA.
  - Evita que un avión derribado se cante dos o tres veces consecutivas cuando CMO registra el evento bajo varios bandos (`[USN]`, `[USAF]`, `[Downed Pilots]`).
- **Corrección de Identificación de Cazas (Regex Word Boundaries):**
  - Blindada la clasificación de aeronaves con límites de palabra (`\b`) en `clean_unit_callsign`.
  - Resuelto el error donde escuadrones navales históricos como `VF-154` eran interpretados erróneamente como cazas `F-15`. Ahora se traducen limpiamente como `Phantom 5`, `Skyhawk`, `Thunderchief`, etc.
- **Filtro Estricto de Niebla de Guerra / Strict Fog of War Isolation:**
  - Corregida la fuga de inteligencia táctica y telemetría enemiga. El asesor ahora descarta al 100% cualquier línea que pertenezca explícitamente a un bando contrario al inicio del procesamiento.
- **Discriminación IFF en Ataques Balísticos / Combat IFF Discrimination:**
  - Los misiles lanzados por el jugador o sus aliados contra blancos enemigos ahora se anuncian como telemetría ofensiva profesional (`🚀 [ENGAGEMENT]`), eliminando las falsas alarmas que ordenaban al jugador activar contramedidas contra sus propios misiles.
- **Resolución de Dominio de Bombarderos y Prefijos Aéreos / Aircraft Domain Resolution:**
  - Corregido el reconocimiento aéreo para bombarderos estratégicos y prefijos de misión.
- **Filtro de Cañoneo Naval y Reportes de Averías / Naval Gunfire & Subsystem Filter:**
  - Ignorados los reportes de averías internas de buques para no confundirlos con hundimientos, y throttled el fuego continuo de cañones.
- **Filtro de Tráfico Aéreo Comercial Neutral / Neutral Airliner Filter:**
  - Silenciados los aviones comerciales de pasajeros durante el combate.
- **Cabecera de Consola Limpia:**
  - Eliminado el número de versión visual del banner de inicio para un acabado profesional.
