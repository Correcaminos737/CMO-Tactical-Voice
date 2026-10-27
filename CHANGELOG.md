# CHANGELOG - CMO TACTICAL VOICE ADVISOR



All notable changes to the CMO Tactical Voice Advisor project are documented here.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.



---



## [1.2.14] - 2026-10-28

### 🛡️ Auto-Instalación de Dependencias y Clarificación de Configuración / Auto-Dependency Healing & Setup Polish
- **Auto-Comprobación y Auto-Instalación de Piper-TTS (Zero-Setup Definitivo):**
  - Implementado pre-flight check en `START_VOICE_ENGLISH.bat` e `INICIAR_VOZ_ESPANOL.bat` que detecta si el motor de voz neuronal (`piper-tts`) está instalado en el entorno de Python activo. Si no lo está, lo instala automáticamente vía `pip` en el primer arranque.
  - Implementada función auto-sanadora `ensure_dependencies()` directamente en `cmo_tactical_voice.py` para garantizar que incluso si el script se lanza desde terminal o IDE sin pasar por los lanzadores `.bat`, las dependencias requeridas se resuelvan limpiamente en vez de arrojar `No module named 'piper'`.
- **Clarificación de Configuración del Message Log de CMO:**
  - Corregida y actualizada la documentación en `README.md` y `docs/CMO_MESSAGE_LOG_SETUP.md`: se eliminó la instrucción obsoleta de buscar la casilla *"Write message log to file"* (propia del viejo CMANO) y se sustituyó por una guía visual y detallada explicando que el guardado a disco en CMO es nativo y automático, requiriendo únicamente marcar las casillas deseadas en la columna **"Show on Message Log"**.

---

## [1.2.13] - 2026-10-27



### 🎙️ Diccionario Fonético Militar DB3000 y Pronunciación Neural Bilingüe / Full DB3000 Phonetic Lexicon

- **Barrido Completo de la Base de Datos DB3000 (27.000+ Entidades):**

  - Incorporado léxico fonético militar precompilado (`phonetic_lexicon.json`) con más de 27.000 entradas bilingües (Español e Inglés) cubriendo la totalidad de aeronaves, buques, submarinos, sensores, instalaciones y armamento de CMO.

  - Carga y búsqueda en memoria RAM en tiempo O(1) (menos de 10 microsegundos), sin latencia ni impacto en el rendimiento.

  - Zero-setup para el usuario final: incluido directamente en el archivo ZIP, listo para usar sin requerir extracciones de bases de datos ni configuración previa.

- **Normalización Fonética Militar para Síntesis Neural (Piper TTS):**

  - Pronunciación fluida y natural: términos militares como `BOGEY` se leen "Boguey" (eliminando la jota dura en español), `HARM` con aspiración suave, `AMRAAM` natural ("Amram"), `AWACS`/`AEWC` ("Aguacs"), `SEAD` ("Siad"), y siglas de misiles (`RIM-66`, `AIM-120`) pronunciados con sus nombres militares en lugar de deletrearse letra a letra.

  - Traducción táctica de clasificaciones y sufijos (`Multirole` -> "caza polivalente", `GuidedWeapon` -> "arma guiada", `#10` -> "número 10", `FFG` -> "fragata", `DDG` -> "destructor").

- **Limpieza de Radares, Emplazamientos y Detectores:**

  - Los nombres técnicos de bases y radares (`Skiros AN/TPS-43F Site`, `Mount Hymettus S-743D Site`) se sintetizan de forma limpia y natural (`Radar de Skiros`, `Radar de Monte Himeto`).

  - Identificación clara de plataformas de alerta temprana aérea (`AWACS Erieye`, `AWACS Wedgetail`).

- **Limpieza de Misiles y Lotes de Producción:**

  - Eliminación de sufijos de ingeniería y lotes de producción innecesarios para comunicaciones de radio (`P3I.3`, `Blk VIB`, etc.) y corrección de truncamientos en nombres de armas.

- **Pipeline de Audio en Memoria Reparado:**

  - Corregido el buffer de canales de audio (`# channels not specified`), garantizando reproducción de voz cristalina e instantánea en todos los canales tácticos.



### 🚀 Facilidad de Instalación, Auto-Detección y Kills Confirmados / Installation & Detection Polish

- **Detección Automática de Python y Protección de Versión (Python 3.12):**

  - Los lanzadores ahora buscan automáticamente Python en AppData (`%LOCALAPPDATA%\Programs\Python`) por si el usuario olvidó marcar la casilla del PATH.

  - Añadida comprobación de compatibilidad que detecta Python 3.13+ y muestra un enlace directo oficial al instalador de Python 3.12 (evitando el error de falta de binarios de `piper-phonemize` en Python 3.13).

- **Auto-Detección Relativa en Carpeta de CMO / Root Folder Discovery:**

  - `cmo_locator.py` ahora comprueba si la carpeta del asesor está descomprimida directamente dentro de la instalación de Command: Modern Operations (`..\Logs`), garantizando enlace instantáneo sin configuración para cualquier instalación en discos secundarios o rutas personalizadas.

- **Soporte Completo en Inglés / Dedicated English Installer:**

  - Añadido `INSTALL_DEPENDENCIES.bat` en inglés junto a `INSTALAR_DEPENDENCIAS.bat`.

  - Los scripts `.bat` ahora detectan tanto `python` como el launcher oficial `py -3` de Windows, ofreciendo mensajes de error limpios y enlaces de ayuda si Python no está presente.

- **Reordenamiento de Kills y Niebla de Guerra / Enemy Splashes vs Fog of War:**

  - El evaluador de bajas enemigas ahora se procesa antes de aislar la telemetría hostil. CMO etiqueta los derribos enemigos bajo el bando de la víctima (`[Russia] ... destroyed!`), por lo que ahora los derribos y buques hundidos se anuncian inmediatamente como Kills confirmados antes de bloquear los radares y sensores enemigos.

- **Instrucciones Claras en README y Foro:**

  - Clarificado que el asesor funciona como una Consola de Radio Táctica ultraligera en segundo plano (terminal sin GUI pesada) y simplificada la guía de instalación a 3 pasos directos con enlace directo a Python 3.12.



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

