# How to Enable the Message Log in Command: Modern Operations (CMO)
# Cómo Activar el Message Log en Command: Modern Operations

To allow the Tactical Voice Advisor to narrate combat in real time, CMO must write its event log to disk. This is a built-in feature of CMO and takes only 10 seconds to configure.

Para que el Asesor Táctico por Voz pueda narrar el combate en tiempo real, CMO debe escribir su registro de eventos en disco. Esta es una función nativa oficial de CMO y se configura en 10 segundos.

---

### Step-by-Step Instructions / Instrucciones Paso a Paso

1. Open **Command: Modern Operations**.
   *Abre Command: Modern Operations.*

2. In the top menu bar, click on **Game** ➔ **Game Options** (or press `Alt + O`).
   *En el menú superior, haz clic en **Game** ➔ **Game Options** (o pulsa `Alt + O`).*

3. Go to the **Message Log** tab.
   *Entra en la pestaña **Message Log**.*

4. Make sure the following checkbox is **CHECKED / ACTIVADO**:
   - `[X] Write message log to file` (Escribir registro de mensajes en archivo)

5. (Recommended) Ensure message types you care about are active (Contacts, Air Operations, Weapons End-game, Battle Damage Assessment).
   *(Recomendado) Asegúrate de que los tipos de mensajes principales estén marcados (Contactos, Operaciones aéreas, Resultados de armas, BDA).*

6. Click **OK** to save.
   *Haz clic en **OK** para guardar.*

---

```text
  +-------------------------------------------------------+
  |  CMO - Game Options                                  |
  |  [ General ]  [ Message Log ]  [ Sound ]  [ Map ]    |
  |                                                       |
  |   [X] Write message log to file                       |
  |   [X] Major events only / All events                  |
  |                                                       |
  |                        [ OK ]      [ Cancel ]         |
  +-------------------------------------------------------+
```

That's it! When you start any scenario, CMO will automatically create a `.txt` log file in your `Logs/` folder, and the Tactical Voice Advisor will immediately begin narrating.

¡Listo! Cuando inicies cualquier escenario, CMO creará automáticamente un archivo de texto en tu carpeta `Logs/` y el Asesor Táctico comenzará a hablar de inmediato.
