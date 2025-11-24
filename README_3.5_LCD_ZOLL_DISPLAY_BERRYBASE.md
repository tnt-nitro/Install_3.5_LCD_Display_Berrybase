# Installation 3.5" LCD Display Berrybase

## Übersicht

Dieses Installationsskript richtet ein 3.5" LCD Display (Waveshare 35B) auf einem Raspberry Pi ein und macht es fehlerfrei nutzbar. Die Installation erfolgt in zwei Schritten mit automatischem Reboot dazwischen.

**Zweck des Projekts:**

- Installation und Konfiguration des 3.5" LCD Displays für fehlerfreie Nutzung
- Bereitstellung von Display-Utilities (`the_programm_display_utils.py`) für flackerfreie Ausgabe
- Automatischer Start des Zielprogramms (`the_programm_main.py`) nach dem Boot
- Einfache Integration eigener Projekte

**📖 Wichtige Dokumentation:**

- **Diese Datei:** Installationsanleitung
- **`README_PROJEKT_NUTZUNG.md`:** Ausführliche Anleitung zur Nutzung eigener Projekte und zur Verwendung der Display-Utilities

**Kompatibilität:**

- Raspberry Pi 3 B
- **Raspberry Pi OS Buster Lite (32-bit) - Image: 2023-05-03-raspios-buster-armhf-lite.img.xz**
- **WICHTIG:** Nur dieses spezifische Image wurde erfolgreich getestet.
- Waveshare 3.5" LCD (B) Display

## ❗ Kompatibilitätshinweis

**Dieses LCD-Display ist ein Legacy-SPI-Display und funktioniert nicht unter Raspberry Pi OS Bookworm oder Trixie (weder 32-bit noch 64-bit).**

**Nur Raspberry Pi OS Buster (32-bit, Legacy) wird vollständig unterstützt.**

## Voraussetzungen

1. **Raspberry Pi OS Image (WICHTIG - Nur dieses Image funktioniert!):**
   - **2023-05-03-raspios-buster-armhf-lite.img.xz**
   - Raspberry Pi OS Buster Lite (32-bit)
   - **Hinweis:** Andere Images (Bookworm, Bullseye, neuere Versionen) wurden ausführlich getestet und funktionieren **nicht** mit dieser Installation
   - **Download:** Das Image kann von der offiziellen Raspberry Pi Website heruntergeladen werden (Legacy Images / Buster)
   - Image auf SD-Karte geschrieben

2. **Hardware:**
   - Raspberry Pi 3 B
   - Waveshare 3.5" LCD (B) Display
   - SD-Karte mit installiertem OS

3. **Zugriff:**
   - SSH-Zugriff ODER
   - Tastatur und HDMI-Monitor für die Installation

## Installationsablauf

### Schritt 1: Dateien auf den Raspberry Pi kopieren

Kopieren Sie alle Dateien aus diesem Verzeichnis auf den Raspberry Pi, z.B. nach `/home/pi/Install_3.5_LCD_Display_Berrybase/`

### Schritt 2: Installation starten

```bash
cd /home/pi/Install_3.5_LCD_Display_Berrybase
sudo python3 main.py
```

### Schritt 3: Automatischer Ablauf

Die Installation läuft vollautomatisch ab:

1. **main.py** startet **install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py**
   - System wird vorbereitet (apt-get update, git, dos2unix)
   - LCD-show Repository wird von GitHub geclont
   - Windows-Zeilenenden werden korrigiert
   - LCD35-show Treiber wird installiert (lite-Version)
   - config.txt wird für Rotation angepasst (270°)
   - Service für second_file wird eingerichtet
   - **System startet automatisch neu**

2. **Nach dem Reboot:**
   - **install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py** wird automatisch gestartet
   - The Programm Service wird eingerichtet (the-programm.service)
   - Installation ist abgeschlossen

### Schritt 4: Installation testen

Nach erfolgreicher Installation startet das Programm automatisch nach dem Boot. Sie können es auch manuell starten:

```bash
sudo python3 /home/pi/the_programm_main.py
```

**Hinweis:**

- Das Hauptprogramm (`the_programm_main.py`) startet standardmäßig das Testprogramm (`the_programm_display_berrybase_test.py`)
- Um ein eigenes Projekt zu nutzen, siehe `README_PROJEKT_NUTZUNG.md`

## Dateistruktur

```
Install_3.5_LCD_Display_Berrybase/
├── main.py                                          # Startet die Installation
├── install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py    # Installation Schritt 1
├── install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py  # Installation Schritt 2
├── the_programm_main.py                             # Hauptprogramm-Wrapper (startet Zielprogramm)
├── the_programm_display_utils.py                    # Display-Utilities für flackerfreie Ausgabe
├── the_programm_display_berrybase_test.py          # Testprogramm (wird von the_programm_main.py gestartet)
├── uninstall_lcd_3.5_zoll_display_berrybase_complete.py      # Vollständige Deinstallation
├── uninstall_lcd_3.5_zoll_display_berrybase_autostart.py     # Deinstallation nur Autostart
├── README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE.md         # Diese Datei (Installationsanleitung)
└── README_PROJEKT_NUTZUNG.md                        # Anleitung zur Nutzung eigener Projekte
```

## Was wird installiert?

### LCD Display Treiber

- Waveshare LCD-show Repository wird installiert
- LCD35-show Treiber (lite-Version)
- Rotation: 270° (Hochformat)
- Touch-Funktionalität wird eingerichtet

### Systemd Services

- `install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service` - Startet second_file nach Reboot
- `the-programm.service` - Wird von second_file eingerichtet (startet the_programm_main.py)

### Config.txt Änderungen

- `dtoverlay=waveshare35a:rotate=270` wird hinzugefügt
- Alte waveshare35*-Einträge werden entfernt

## Deinstallation

Es gibt zwei Deinstallationsoptionen:

### Option 1: Nur Autostart entfernen (LCD bleibt funktionsfähig)

```bash
sudo python3 /home/pi/uninstall_lcd_3.5_zoll_display_berrybase_autostart.py
```

Dies entfernt:

- `install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service`
- `the-programm.service`

**Hinweis:** Die LCD-Display-Installation selbst bleibt bestehen. Nur die Autostart-Services werden entfernt.

### Option 2: Vollständige Deinstallation (LCD wird deaktiviert)

```bash
sudo python3 /home/pi/uninstall_lcd_3.5_zoll_display_berrybase_complete.py
```

Dies entfernt:

- Alle Services und Autostart
- LCD-Treiber (`/home/pi/LCD-show/`)
- `config.txt` Änderungen (dtoverlay)

**Hinweis:** Nach dieser Deinstallation funktioniert das Display nicht mehr (weißer Bildschirm). Eine erneute Installation mit `main.py` ist möglich.

**Manuelle Prüfung nach Deinstallation:**

```bash
# Prüfen ob Service-Dateien noch existieren
ls -la /etc/systemd/system/ | grep -E "install_lcd|the-programm"

# Falls Dateien noch existieren, manuell löschen:
sudo rm -f /etc/systemd/system/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
sudo rm -f /etc/systemd/system/the-programm.service

# Symlinks entfernen (falls vorhanden)
sudo rm -f /etc/systemd/system/multi-user.target.wants/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
sudo rm -f /etc/systemd/system/multi-user.target.wants/the-programm.service

# systemd neu laden
sudo systemctl daemon-reload
```

## Troubleshooting

### Display zeigt nichts an

1. Prüfen Sie die Verbindung zwischen Raspberry Pi und Display
2. Prüfen Sie `/boot/config.txt`:

   ```bash
   sudo nano /boot/config.txt
   ```

   Sollte enthalten: `dtoverlay=waveshare35a:rotate=270`

### Installation hängt

- Prüfen Sie die Internetverbindung (Git-Clone benötigt Internet)
- Prüfen Sie die Logs: `journalctl -u install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service`

### Touch funktioniert nicht

- Prüfen Sie ob `xserver-xorg-input-evdev` installiert ist
- Prüfen Sie die Verbindung des Touch-Kabels

### Service startet nicht

```bash
# Service-Status prüfen
sudo systemctl status install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service

# Service manuell starten
sudo systemctl start install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
```

## Manuelle Config.txt Bearbeitung

Falls Sie die config.txt manuell bearbeiten müssen:

```bash
# Für Raspberry Pi OS Buster (dieses Image):
sudo nano /boot/config.txt
```

**Hinweis:** Bei Raspberry Pi OS Buster liegt die config.txt direkt in `/boot/config.txt`, nicht in `/boot/firmware/`.

**Wichtige Einträge:**

```
dtoverlay=waveshare35a:rotate=270
```

## Referenzen

- [Waveshare Wiki - 3.5" LCD (B)](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)#Screen_orientation_settings)
- [Waveshare LCD-show GitHub](https://github.com/waveshare/LCD-show)

## Hauptprogramm

Das Hauptprogramm (`the_programm_main.py`) ist ein Wrapper, der das eigentliche Zielprogramm startet. Standardmäßig startet es das Testprogramm (`the_programm_display_berrybase_test.py`).

**Wichtig:** Um ein eigenes Projekt zu nutzen, siehe die ausführliche Anleitung in `README_PROJEKT_NUTZUNG.md`.

### Display-Utilities

Die Datei `the_programm_display_utils.py` enthält wichtige Utilities für die flackerfreie Display-Ausgabe:

- **Display-Klasse:** Für flackerfreie Zeilenaktualisierungen
- **Colors-Klasse:** ANSI-Farbcodes für farbige Ausgabe
- **Funktionen:** `strip_ansi_codes()` für korrekte Textlängenberechnung

**Diese Utilities MÜSSEN verwendet werden**, um eine fehlerfreie Display-Ausgabe zu gewährleisten. Siehe `README_PROJEKT_NUTZUNG.md` für Details.

## Support

Bei Problemen prüfen Sie:

1. Die Logs: `journalctl -u <service-name>`
2. Die config.txt: `/boot/config.txt` oder `/boot/firmware/config.txt`
3. Die Service-Status: `sudo systemctl status <service-name>`
