# Projekt-Nutzung: Eigene Anwendungen auf dem LCD Display

## Übersicht

Diese Anleitung erklärt, wie Sie das installierte LCD Display für Ihre eigene Anwendung nutzen können. Das Projekt stellt wichtige Utilities bereit, die für eine fehlerfreie Display-Ausgabe **unbedingt verwendet werden müssen**.

## ⚠️ WICHTIG: Display-Utilities sind Pflicht!

**Die Datei `the_programm_display_utils.py` MUSS verwendet werden!**

- **Ohne diese Utilities:** Das Display flackert, die Ausgabe ist unleserlich, Farben funktionieren nicht korrekt
- **Mit diesen Utilities:** Flackerfreie, stabile Ausgabe, korrekte Farbdarstellung, präzise Cursor-Positionierung

**Auch wenn Sie:**
- Das Projekt lange nicht genutzt haben
- Fremd im Projekt sind und es zum ersten Mal sehen
- Ein bestehendes Programm anpassen möchten

**→ Die Display-Utilities MÜSSEN verwendet werden!** Diese Anleitung erklärt genau, wie.

## Warum Display-Utilities verwenden?

Das LCD Display benötigt spezielle Behandlung, um flackerfreie Ausgabe zu gewährleisten:

- **Normale `print()`-Statements** führen zu Flackern und unleserlicher Ausgabe
- **ANSI-Escape-Codes** müssen korrekt verwendet werden
- **Cursor-Positionierung** muss präzise sein
- **Zeilenaktualisierungen** müssen ohne Bildschirm-Flacker erfolgen

Die bereitgestellten `the_programm_display_utils.py` lösen alle diese Probleme automatisch.

## Projektstruktur verstehen

### Aktuelle Konfiguration

```
/home/pi/
├── the_programm_main.py                    # Wrapper, der Ihr Programm startet
├── the_programm_display_utils.py           # Display-Utilities (MUSS verwendet werden)
└── the_programm_display_berrybase_test.py  # Testprogramm (Beispiel)
```

### Service-Konfiguration

Der Service `the-programm.service` startet automatisch nach dem Boot:
- **Startet:** `/home/pi/the_programm_main.py`
- **Ausgabe:** Direkt auf `/dev/tty1` (LCD Display)
- **Logs:** `/home/pi/logs/the_programm.log`

## Methode 1: Eigene Anwendung in the_programm_main.py einbinden

### Schritt 1: Ihr Programm vorbereiten

Erstellen Sie Ihr Python-Programm und stellen Sie sicher, dass es die Display-Utilities verwendet:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ihr eigenes Programm

import sys
import os
from the_programm_display_utils import Display, Colors

def main():
    # Display initialisieren (WICHTIG!)
    display = Display(max_rows=30)
    display.init()
    
    try:
        # Ihr Programm-Code hier
        display.update_line(1, "Willkommen zu meinem Programm!")
        display.update_line(2, f"{Colors.GREEN}Status: Bereit{Colors.RESET}")
        
        # Beispiel: Endlosschleife
        counter = 0
        while True:
            counter += 1
            display.update_line(3, f"Counter: {counter}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        # Display aufräumen (WICHTIG!)
        display.cleanup()

if __name__ == "__main__":
    main()
```

### Schritt 2: the_programm_main.py anpassen

Öffnen Sie `/home/pi/the_programm_main.py` und ändern Sie den Pfad:

```python
# Ändern Sie diese Zeile:
script_path = os.path.join(os.path.dirname(__file__), "the_programm_display_berrybase_test.py")

# Zu Ihrem Programm:
script_path = "/pfad/zu/ihrem/programm.py"
```

**Beispiel:**
```python
script_path = "/home/pi/mein_programm.py"
```

### Schritt 3: Service neu starten

```bash
sudo systemctl restart the-programm.service
```

## Methode 2: Projekt duplizieren für andere Programme

**Wann verwenden?**
- Sie möchten das Display in einem anderen Programm nutzen
- Sie möchten mehrere Projekte parallel betreiben
- Sie möchten das Original-Projekt unverändert lassen

**Wichtig:** Wenn Sie das Display in einem anderen Programm nutzen möchten, duplizieren Sie das Projekt und ersetzen Sie `the_programm_main.py` durch die Startdatei Ihrer Wunschanwendung.

Wenn Sie mehrere Projekte haben oder das Original-Projekt behalten möchten:

### Schritt 1: Projekt-Verzeichnis erstellen

```bash
mkdir -p /home/pi/mein_projekt
cd /home/pi/mein_projekt
```

### Schritt 2: Display-Utilities kopieren

```bash
cp /home/pi/the_programm_display_utils.py /home/pi/mein_projekt/
```

**WICHTIG:** Die `the_programm_display_utils.py` MUSS im gleichen Verzeichnis wie Ihr Programm sein oder im Python-Pfad verfügbar sein. **Diese Datei ist essentiell für fehlerfreie Display-Ausgabe und MUSS verwendet werden!**

### Schritt 3: Ihr Programm erstellen ODER bestehendes Programm anpassen

**Falls Sie ein neues Programm erstellen:**

Erstellen Sie `mein_programm.py` in `/home/pi/mein_projekt/`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ihr Programm

import sys
import os
import time

# Display-Utils importieren (aus gleichem Verzeichnis)
from the_programm_display_utils import Display, Colors

def main():
    # Display initialisieren
    display = Display(max_rows=30)
    display.init()
    
    try:
        # Ihr Programm-Code
        display.update_line(1, f"{Colors.BOLD}Mein Programm{Colors.RESET}")
        display.update_line(2, f"{Colors.GREEN}Läuft...{Colors.RESET}")
        
        # Beispiel-Logik
        for i in range(10):
            display.update_line(3, f"Schritt {i+1}/10")
            time.sleep(1)
            
    except KeyboardInterrupt:
        display.update_line(3, f"{Colors.YELLOW}Beendet{Colors.RESET}")
    finally:
        display.cleanup()

if __name__ == "__main__":
    main()
```

**Falls Sie ein bestehendes Programm nutzen:**

1. Kopieren Sie Ihr bestehendes Programm nach `/home/pi/mein_projekt/`
2. **WICHTIG:** Passen Sie Ihr Programm an, um die Display-Utilities zu verwenden:
   - Importieren Sie `from the_programm_display_utils import Display, Colors`
   - Ersetzen Sie alle `print()`-Statements durch `display.update_line()`
   - Initialisieren Sie das Display mit `display.init()` am Anfang
   - Räumen Sie mit `display.cleanup()` im `finally`-Block auf

**Beispiel-Anpassung:**

```python
# VORHER (normales Programm):
print("Hallo Welt!")
print(f"Status: {status}")

# NACHHER (mit Display-Utils):
from the_programm_display_utils import Display, Colors

display = Display(max_rows=30)
display.init()
try:
    display.update_line(1, "Hallo Welt!")
    display.update_line(2, f"Status: {status}")
finally:
    display.cleanup()
```

### Schritt 4: the_programm_main.py anpassen ODER Service anpassen

**Option A: the_programm_main.py anpassen (einfach)**

```python
script_path = "/home/pi/mein_projekt/mein_programm.py"
```

**Option B: Service direkt anpassen (für mehrere Projekte)**

Wenn Sie mehrere Projekte haben, können Sie auch den Service direkt anpassen:

```bash
sudo nano /etc/systemd/system/the-programm.service
```

Ändern Sie die `ExecStart`-Zeile:

```ini
ExecStart=/bin/bash -c 'cd /home/pi/mein_projekt && /usr/bin/python3 -u /home/pi/mein_projekt/mein_programm.py 2>&1 | tee -a /home/pi/logs/the_programm.log'
```

Dann:

```bash
sudo systemctl daemon-reload
```

### Schritt 5: Service neu starten

```bash
sudo systemctl restart the-programm.service
```

## Display-Utilities: Detaillierte Anleitung

### Display-Klasse

Die `Display`-Klasse ist das Herzstück für flackerfreie Ausgabe.

#### Initialisierung

```python
from the_programm_display_utils import Display

# Erstellen Sie ein Display-Objekt
display = Display(max_rows=30)  # 30 Zeilen (Standard für 3.5" LCD)

# Initialisieren Sie das Display (löscht Bildschirm, versteckt Cursor)
display.init()
```

#### Wichtige Methoden

##### `update_line(row, text)`
Aktualisiert eine Zeile flackerfrei:

```python
# Zeile 1 aktualisieren
display.update_line(1, "Hallo Welt!")

# Mit Farben
display.update_line(2, f"{Colors.GREEN}Status: OK{Colors.RESET}")
```

**Wichtig:**
- `row` beginnt bei 1 (nicht 0)
- Der Text wird automatisch auf die Zeile gesetzt
- Alte Inhalte werden automatisch gelöscht

##### `clear_screen()`
Löscht den gesamten Bildschirm:

```python
display.clear_screen()
```

##### `clear_full_screen()`
Löscht den Bildschirm und füllt alle Zeilen mit Leerzeichen:

```python
display.clear_full_screen()
```

##### `move_cursor(row, col)`
Bewegt den Cursor zu einer bestimmten Position:

```python
display.move_cursor(5, 10)  # Zeile 5, Spalte 10
```

##### `print_border(width, char='#')`
Zeichnet einen Rahmen um das Display:

```python
display.print_border(width=60, char='#')
```

##### `update_line_with_border(row, text, width, border_char='#')`
Aktualisiert eine Zeile, während der Rahmen erhalten bleibt:

```python
display.update_line_with_border(5, "Mein Text", width=60, border_char='#')
```

##### `cleanup()`
Räumt das Display auf (zeigt Cursor wieder):

```python
display.cleanup()
```

**WICHTIG:** Rufen Sie `cleanup()` immer im `finally`-Block auf!

### Colors-Klasse

Die `Colors`-Klasse stellt ANSI-Farbcodes bereit.

#### Vordergrundfarben

```python
from the_programm_display_utils import Colors

# Verfügbare Farben:
Colors.RED      # Rot
Colors.GREEN    # Grün
Colors.YELLOW   # Gelb
Colors.BLUE     # Blau
Colors.MAGENTA  # Magenta
Colors.CYAN     # Cyan
Colors.PURPLE   # Lila
Colors.WHITE    # Weiß
Colors.BLACK    # Dunkelgrau
Colors.RESET    # Zurücksetzen
Colors.BOLD     # Fett
```

#### Verwendung

```python
# Text in Farbe ausgeben
text = f"{Colors.GREEN}Erfolg!{Colors.RESET}"
display.update_line(1, text)

# Kombinationen
text = f"{Colors.BOLD}{Colors.RED}FEHLER!{Colors.RESET}"
display.update_line(2, text)
```

**WICHTIG:** Verwenden Sie immer `Colors.RESET` nach farbigem Text!

#### Hintergrundfarben

```python
# Verfügbare Hintergrundfarben:
Colors.BG_BLACK
Colors.BG_RED
Colors.BG_GREEN
Colors.BG_YELLOW
Colors.BG_BLUE
Colors.BG_MAGENTA
Colors.BG_CYAN
Colors.BG_WHITE

# Spezielle Farben:
Colors.BG_ORANGE
Colors.BG_BROWN
Colors.BG_PINK
Colors.BG_LIME
Colors.BG_VIOLET

# Graustufen:
Colors.BG_GRAY_DARK
Colors.BG_GRAY_1
Colors.BG_GRAY_2
Colors.BG_GRAY_3
Colors.BG_GRAY_LIGHT
```

#### Gefüllte Vierecke

```python
# Gefülltes Viereck in einer Farbe
block = display.print_colored_block(width=20, bg_color=Colors.BG_RED, label="Status: ")
display.update_line(5, block)
```

#### Graustufen für Prozentwerte

```python
# Graustufe für einen Prozentwert (0-100)
color = display.get_grayscale_color(percent=75)  # 75% = hellgrau
block = display.print_colored_block(width=50, bg_color=color)
display.update_line(6, block)
```

### Hilfsfunktion: strip_ansi_codes()

Entfernt ANSI-Codes aus einem String (für Längenberechnung):

```python
from the_programm_display_utils import strip_ansi_codes

text = f"{Colors.GREEN}Hallo{Colors.RESET}"
length_with_codes = len(text)  # Länge mit ANSI-Codes
length_without_codes = len(strip_ansi_codes(text))  # Tatsächliche Textlänge
```

## Vollständiges Beispiel

Hier ist ein vollständiges Beispiel, das alle wichtigen Konzepte zeigt:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Beispiel-Programm für LCD Display

import time
import sys
from the_programm_display_utils import Display, Colors

def main():
    # Display initialisieren
    display = Display(max_rows=30)
    display.init()
    
    try:
        # Titel
        display.update_line(1, f"{Colors.BOLD}{Colors.CYAN}=== Mein Programm ==={Colors.RESET}")
        
        # Status
        display.update_line(3, f"{Colors.GREEN}Status: Bereit{Colors.RESET}")
        
        # Rahmen zeichnen
        display.print_border(width=60, char='=')
        
        # Hauptbereich
        counter = 0
        while True:
            counter += 1
            
            # Counter anzeigen
            display.update_line(5, f"Counter: {counter}")
            
            # Farbige Status-Bar
            percent = (counter % 100)
            color = display.get_grayscale_color(percent)
            bar = display.print_colored_block(width=percent//2, bg_color=color, label="Fortschritt: ")
            display.update_line(7, bar)
            
            # Zeit anzeigen
            from datetime import datetime
            now = datetime.now().strftime("%H:%M:%S")
            display.update_line(9, f"Zeit: {now}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        display.update_line(3, f"{Colors.YELLOW}Status: Beendet{Colors.RESET}")
        time.sleep(2)
    finally:
        # WICHTIG: Display aufräumen
        display.cleanup()

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Immer Display initialisieren und aufräumen

```python
display = Display(max_rows=30)
display.init()

try:
    # Ihr Code
    pass
finally:
    display.cleanup()  # IMMER aufräumen!
```

### 2. Farben immer zurücksetzen

```python
# RICHTIG:
text = f"{Colors.GREEN}Text{Colors.RESET}"

# FALSCH:
text = f"{Colors.GREEN}Text"  # Farbe bleibt aktiv!
```

### 3. Zeilen nicht überschreiben ohne update_line()

```python
# RICHTIG:
display.update_line(1, "Neuer Text")

# FALSCH:
print("Neuer Text")  # Führt zu Flackern!
```

### 4. Lange Texte kürzen

```python
text = "Sehr langer Text der nicht auf das Display passt..."
if len(text) > 60:  # Display-Breite prüfen
    text = text[:57] + "..."
display.update_line(1, text)
```

### 5. ANSI-Codes bei Längenberechnung berücksichtigen

```python
from the_programm_display_utils import strip_ansi_codes

text = f"{Colors.GREEN}Hallo{Colors.RESET}"
actual_length = len(strip_ansi_codes(text))  # Korrekte Länge
```

## Fehlerbehebung

### Problem: Display flackert

**Lösung:** Verwenden Sie immer `display.update_line()` statt `print()`.

### Problem: Farben funktionieren nicht

**Lösung:** Stellen Sie sicher, dass Sie `Colors.RESET` nach farbigem Text verwenden.

### Problem: Cursor ist sichtbar

**Lösung:** Rufen Sie `display.init()` am Anfang auf und `display.cleanup()` am Ende.

### Problem: Zeilen werden nicht aktualisiert

**Lösung:** Verwenden Sie `display.update_line(row, text)` mit korrekter Zeilennummer (1-basiert).

### Problem: Programm startet nicht nach Boot

**Lösung:** Prüfen Sie die Service-Status:

```bash
sudo systemctl status the-programm.service
sudo journalctl -u the-programm.service -n 50
```

## Service-Verwaltung

### Service neu starten

```bash
sudo systemctl restart the-programm.service
```

### Service stoppen

```bash
sudo systemctl stop the-programm.service
```

### Service starten

```bash
sudo systemctl start the-programm.service
```

### Service-Status prüfen

```bash
sudo systemctl status the-programm.service
```

### Logs anzeigen

```bash
# Letzte 50 Zeilen
sudo journalctl -u the-programm.service -n 50

# Live-Logs
sudo journalctl -u the-programm.service -f

# Log-Datei
tail -f /home/pi/logs/the_programm.log
```

## Zusammenfassung

1. **Display-Utilities verwenden:** Die `the_programm_display_utils.py` MUSS verwendet werden für fehlerfreie Ausgabe
2. **Display initialisieren:** `display.init()` am Anfang
3. **Display aufräumen:** `display.cleanup()` im `finally`-Block
4. **update_line() verwenden:** Nie `print()` direkt, immer `display.update_line()`
5. **Farben zurücksetzen:** Immer `Colors.RESET` nach farbigem Text
6. **the_programm_main.py anpassen:** Pfad zu Ihrem Programm eintragen
7. **Service neu starten:** Nach Änderungen `sudo systemctl restart the-programm.service`

Bei Fragen oder Problemen prüfen Sie die Logs und stellen Sie sicher, dass Sie die Display-Utilities korrekt verwenden.

