# CHANGELOG - CMO TACTICAL VOICE ADVISOR

All notable changes to the CMO Tactical Voice Advisor project are documented here.
The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

---

## [1.2.11] - 2026-10-25

### 🛡️ Critical Bug Fixes & Combat Polish / Correcciones Críticas y Pulido de Combate
- **Filtro Estricto de Niebla de Guerra / Strict Fog of War Isolation:**
  - Corregida la fuga de inteligencia táctica y telemetría enemiga. El asesor ahora descarta al 100% cualquier línea que pertenezca explícitamente a un bando contrario al inicio del procesamiento (evitando por ejemplo que un jugador del Pacto de Varsovia escuche las detecciones de submarinos de la OTAN como *S 66 Greif* o *S 320 Narhvalen*, o fallos de misiles Exocet enemigos).
  - Blindada la función de comprobación de bandos para evitar colisiones accidentales de acrónimos (como `US` coincidiendo dentro de `USSR`).
- **Discriminación IFF en Ataques Balísticos / Combat IFF Discrimination:**
  - Los misiles lanzados por el jugador o sus aliados contra blancos enemigos (como *AIM-120 AMRAAM* atacando a un *MiG-23* o *MiG-25*) ahora se anuncian como telemetría ofensiva profesional (`🚀 [ENGAGEMENT]`), eliminando las falsas alarmas que ordenaban al jugador activar contramedidas contra sus propios misiles.
  - Las armas hostiles que amenacen a buques o aeronaves aliadas mantienen la alarma crítica de combate (`🚨 [CRÍTICO] ⚠️ [AMENAZA ENTRANTE]`).
- **Resolución de Dominio de Bombarderos y Prefijos Aéreos / Aircraft Domain Resolution:**
  - Corregido el reconocimiento aéreo para que bombarderos estratégicos (como *H-6M Badger*, *Tu-95 Bear*, etc.) y contactos bautizados como `Bomber #`, `Fighter #`, `AEW #`, `OECM #` o `Multirole #` reciban el icono aéreo (`✈️`) y la voz del Oficial de Operaciones Aéreas (Karpov) en lugar de ser tratados como buques de superficie.
- **Filtro de Cañoneo Naval y Reportes de Averías / Naval Gunfire & Subsystem Filter:**
  - Los avisos de averías internas de buques (`damage report: ... has been destroyed`) ahora se ignoran estrictamente para los Kills. El asesor ya no cantará montajes de 14.5mm, radios UHF, periscopios o tubos de torpedos de 450mm como si fueran buques enteros destruidos.
  - Las ráfagas rápidas de artillería naval (cañones de 127mm o 76mm en duelos contra lanchas torpederas Swatow o P-4) se agrupan con un enfriamiento de 30 segundos (`⚔️ [ARTILLERÍA] / [GUNFIRE]`) para evitar saturación en combates a corta distancia.
- **Filtro de Tráfico Aéreo Comercial Neutral / Neutral Airliner Filter:**
  - Ampliadas las palabras clave para que los aviones civiles de pasajeros de aerolíneas neutrales (*Boeing 777*, *Boeing 737*, *ATR-42*, *Cessna Citation*) no saturen las comunicaciones de combate.
- **Cabecera de Consola Limpia:**
  - Eliminado el número de versión visual del banner de inicio para un acabado profesional y atemporal.

---

## [1.2.1] - 2026-10-25
- Paridad con War Room: restauración de marcaciones y distancias en millas náuticas (`re_new_contact`).
- Filtro militar anti-saturación de paquetes aéreos.
- Alertas de amenazas entrantes (`re_incoming_attack`) y RWR de radar lock (`re_radar_illum`).
- Diferenciación de bajas aliadas vs kills/splashes enemigos.
- Telemetría balística de salvas y endgame (agotamiento de energía, pérdida de radar, averías).
- Control de daños y averías críticas (incendios, timón averiado, inundaciones).
- Soporte de bando 100% universal para cualquier país del mundo sin restricciones.
- Modo de prueba táctica integrado (`--test`).

---

## [1.2.0] - 2026-10-25
- Lanzamiento inicial independiente para la comunidad con soporte de voces locales neuronales Piper (Español e Inglés).
- Localizador automático de carpetas de logs de CMO (`cmo_locator.py`).
- Descargador automático de modelos ONNX (`voice_downloader.py`).
- Filtro de despegues por secciones aéreas y portaviones.
- Avisos de BDA, Bingo fuel y alertas críticas Vampire/Torpedo.
