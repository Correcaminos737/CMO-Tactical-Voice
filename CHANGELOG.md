# CHANGELOG - CMO TACTICAL VOICE ADVISOR

All notable changes to the CMO Tactical Voice Advisor project are documented here.
The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

---

## [1.2.1] - 2026-10-25

### 🚀 Nuevas Características y Paridad con War Room / New Features & War Room Parity
- **Detección de Contactos con Marcaciones y Distancias en Millas Náuticas (`re_new_contact`):**
  - El sistema vuelve a cantar marcaciones y distancias estimadas (ej. *"Bogey 12 contacto, al 245, a 30 millas"* / *"Bogey 12 contact, bearing 245, at 30 miles"*).
  - Incluye filtro anti-saturación militar: si se detectan 3 o más trazas aéreas simultáneas (paquete enemigo en aproximación), la radio consolida el aviso automáticamente (ej. *"Detección múltiple: paquete de 4 trazas aéreas aproximándose al 240"*).
- **Avisos de Ataques Entrantes e Intercepciones (`re_incoming_attack`):**
  - Alerta inmediata de combate cuando un arma hostil (misil o torpedo) inicia trayectoria de ataque contra un buque o aeronave aliada (ej. *"¡Alerta táctica! Silkworm atacando a Sterett"*).
- **Alerta RWR de Iluminación de Guiado Radar Hostil (`re_radar_illum`):**
  - Detección de lock-on / iluminación por radar de dirección de tiro enemigo sobre unidades del jugador con aviso de alerta electrónica.
- **Diferenciación de Bajas Aliadas vs Derribos Enemigos:**
  - Si una aeronave o buque del jugador es derribado o hundido, se emite una alarma crítica de pérdida en combate (*"¡Atención sala de operaciones! Baja aliada confirmada"*).
  - Si la unidad destruida es enemiga, se emite la confirmación de impacto/splash (*"¡Impacto definitivo confirmado! Blanco destruido"*).
- **Telemetría Balística de Salvas y Endgame:**
  - Informes de agotamiento cinético de misiles (*"Agotó energía cinética fuera de envolvente"*), pérdida de guiado radar (*"Misil ciego por pérdida de radar"*), fallos de motor o tiros fallidos consolidados.
- **Control de Daños y Subsistemas Críticos:**
  - Alerta de averías en buques aliados: incendios a bordo, vías de agua / inundaciones, timón averiado o metralla en cabina.
- **Soporte de Bando 100% Universal:**
  - Eliminada cualquier restricción que atara el asesor a bandos OTAN o EE.UU. Ahora se puede jugar con cualquier país del mundo (Etiopía, Irán, Unión Soviética, Suecia, etc.) y el asesor detecta y sincroniza automáticamente las comunicaciones del bando activo del jugador sin perder eventos.
- **Modo de Prueba Táctica Integrado (`--test`):**
  - Permite ejecutar `python cmo_tactical_voice.py --test --lang es` o `--lang en` para escuchar una secuencia completa de combate simulada sin necesidad de arrancar el juego.

### 🐛 Correcciones de Errores / Bug Fixes
- **Corrección de Regex de Clasificación de Contactos:**
  - Corregido el bug donde los modelos de contacto se cortaban en la primera letra (`Y` en vez de `Yak-38`, `C` en vez de `Cargo`, `P` en vez de `Patrol Craft`). Ahora se extrae el nombre completo del modelo.
- **Filtro de Tráfico Mercante y Civil Restablecido:**
  - Al resolverse el nombre completo del modelo, los buques civiles (`Cargo`, `Tanker`, `Fishing`) quedan correctamente filtrados y silenciados, evitando la saturación por tráfico neutral.
- **Aislamiento de Detecciones Enemigas:**
  - Evitada la fuga de detecciones del bando contrario en las comunicaciones aliadas.

---

## [1.2.0] - 2026-10-25
- Lanzamiento inicial independiente para la comunidad con soporte de voces locales neuronales Piper (Español e Inglés).
- Localizador automático de carpetas de logs de CMO (`cmo_locator.py`).
- Descargador automático de modelos ONNX (`voice_downloader.py`).
- Filtro de despegues por secciones aéreas y portaviones.
- Avisos de BDA, Bingo fuel y alertas críticas Vampire/Torpedo.
