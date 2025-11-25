# Install 3.5" LCD Display Berrybase

Installationsskript für das **Waveshare 3.5" LCD (B) Display** auf Raspberry Pi.  
Das Projekt richtet das Display vollständig ein, installiert Treiber, setzt die richtige Rotation,  
und startet danach automatisch dein eigenes Programm über `the_programm_main.py`.

## 📌 Unterstützte Hardware / Software

- **Raspberry Pi 3 B**  
- **Raspberry Pi Zero 2 W** (getestet und funktioniert fehlerfrei)
- **Waveshare 3.5" LCD (B)**  
- **Raspberry Pi OS Buster Lite (2023-05-03 – 32-bit)**  
  → **WICHTIG:** Dieses Projekt funktioniert **NUR** mit diesem 32-bit Buster Image.
  → 64-bit Versionen wurden getestet und werden **nicht unterstützt** - keine weiteren Versuche nötig.

## 📘 Dokumentation

Die vollständige Dokumentation befindet sich in zwei separaten Readmes:

- **Installationsanleitung**  
  → [README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE.md](README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE.md)

- **Nutzung eigener Programme & Display-Utilities**  
  → [README_PROJEKT_NUTZUNG.md](README_PROJEKT_NUTZUNG.md)

## 🚀 Schnellstart

```bash
cd /home/pi/Install_3.5_LCD_Display_Berrybase
sudo python3 main.py
```

Nach dem Reboot startet automatisch der zweite Installationsschritt  
und danach dein Programm (`the_programm_main.py`).

## 📂 Projektstruktur

```text
Install_3.5_LCD_Display_Berrybase/
├── main.py
├── install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py
├── install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py
├── the_programm_main.py
├── the_programm_display_utils.py
├── the_programm_display_berrybase_test.py
├── uninstall_lcd_3.5_zoll_display_berrybase_complete.py
├── uninstall_lcd_3.5_zoll_display_berrybase_autostart.py
├── README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE.md
└── README_PROJEKT_NUTZUNG.md
```

## ⏱️ Installationszeit

Die Erstinstallation dauert typischerweise **5-15 Minuten**, abhängig von:
- Internetverbindung (für Git-Clone und Paket-Downloads)
- SD-Karten-Geschwindigkeit
- Systemleistung

Die Installationszeit wird nach Abschluss der Installation im Testprogramm angezeigt.

## ℹ️ Hinweis

Dieses Projekt wurde speziell für das **Waveshare 3.5" LCD (B) Display**  
und das OS-Image **2023-05-03-raspios-buster-armhf-lite** entwickelt.  
- **Nur 32-bit Buster wird unterstützt** - andere Images (64-bit, Bookworm, Bullseye) funktionieren nicht.
- 64-bit Versionen wurden ausführlich getestet und werden **nicht mehr unterstützt**.
