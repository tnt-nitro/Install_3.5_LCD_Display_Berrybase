# Install 3.5" LCD Display Berrybase

---

## 🇩🇪 Deutsch

Installationsskript für **3.5" SPI LCD Displays** (GoodTFT/XPT2046-basiert) auf Raspberry Pi.  
Das Projekt richtet das Display vollständig ein, installiert Treiber, setzt die richtige Rotation,  
und startet danach automatisch dein eigenes Programm über `the_programm_main.py`.

**Wichtig:** Dieses Projekt unterstützt **GoodTFT/XPT2046-basierte 3.5" Displays** (auch bekannt als "3.5 inch RPi Display" oder "3.5 inch RPi LCD"). Diese Displays nutzen **NICHT** das Waveshare-Overlay.

### 📌 Unterstützte Hardware / Software

- **Raspberry Pi 3 B**  
- **Raspberry Pi Zero 2 W** (getestet und funktioniert fehlerfrei)
- **3.5" SPI LCD Display** (GoodTFT/XPT2046-basiert)
  - Touch-Controller: **XPT2046** (manchmal als XP12046 falsch gedruckt)
  - Hersteller: GoodTFT / KeDei / MHS
  - Auch bekannt als: "3.5 inch RPi Display" / "3.5 inch RPi LCD"
- **Raspberry Pi OS Buster Lite (2023-05-03 – 32-bit)**  
  → **WICHTIG:** Dieses Projekt funktioniert **NUR** mit diesem 32-bit Buster Image.
  → 64-bit Versionen wurden getestet und werden **nicht unterstützt** - keine weiteren Versuche nötig.

### 📘 Dokumentation

Die vollständige Dokumentation befindet sich in zwei separaten Readmes:

- **Installationsanleitung**  
  → [README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE.md](README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE.md)

- **Nutzung eigener Programme & Display-Utilities**  
  → [README_PROJEKT_NUTZUNG.md](README_PROJEKT_NUTZUNG.md)

### 🚀 Schnellstart

```bash
cd /home/pi/Install_3.5_LCD_Display_Berrybase
sudo python3 main.py
```

Nach dem Reboot startet automatisch der zweite Installationsschritt  
und danach dein Programm (`the_programm_main.py`).

### 📂 Projektstruktur

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

### ⏱️ Installationszeit

Die Erstinstallation dauert typischerweise **5-15 Minuten**, abhängig von:

- Internetverbindung (für Git-Clone und Paket-Downloads)
- SD-Karten-Geschwindigkeit
- Systemleistung

Die Installationszeit wird nach Abschluss der Installation im Testprogramm angezeigt.

### ℹ️ Technische Informationen

**Display-Typ:**

- **GoodTFT/XPT2046-basierte 3.5" SPI Displays**
- Diese Displays nutzen **NICHT** das Waveshare-Overlay
- Waveshare ≠ GoodTFT
- Genau deshalb funktionieren sie auf Pi 5 unter 64-bit **NICHT** ohne Anpassungen

**Treiber:**

- fbtft, MHS35, rpi-fbcp
- Touch: XPT2046

**OS-Kompatibilität:**

- Dieses Projekt wurde speziell für das OS-Image **2023-05-03-raspios-buster-armhf-lite** entwickelt
- **Nur 32-bit Buster wird unterstützt** - andere Images (64-bit, Bookworm, Bullseye) funktionieren nicht
- 64-bit Versionen wurden ausführlich getestet und werden **nicht mehr unterstützt**

### 🔗 Referenzen

- [Install 3.5" LCD Display Berrybase - Dieses Projekt](https://github.com/tnt-nitro/Install_3.5_LCD_Display_Berrybase)
- [LCD-show GitHub Repository](https://github.com/goodtft/LCD-show)

---

## 🇬🇧 English

Installation script for **3.5" SPI LCD Displays** (GoodTFT/XPT2046-based) on Raspberry Pi.  
The project fully sets up the display, installs drivers, sets the correct rotation,  
and then automatically starts your own program via `the_programm_main.py`.

**Important:** This project supports **GoodTFT/XPT2046-based 3.5" displays** (also known as "3.5 inch RPi Display" or "3.5 inch RPi LCD"). These displays do **NOT** use the Waveshare overlay.

### 📌 Supported Hardware / Software

- **Raspberry Pi 3 B**  
- **Raspberry Pi Zero 2 W** (tested and works flawlessly)
- **3.5" SPI LCD Display** (GoodTFT/XPT2046-based)
  - Touch Controller: **XPT2046** (sometimes misprinted as XP12046)
  - Manufacturers: GoodTFT / KeDei / MHS
  - Also known as: "3.5 inch RPi Display" / "3.5 inch RPi LCD"
- **Raspberry Pi OS Buster Lite (2023-05-03 – 32-bit)**  
  → **IMPORTANT:** This project works **ONLY** with this 32-bit Buster image.
  → 64-bit versions have been tested and are **not supported** - no further attempts needed.

### 📘 Documentation

Complete documentation is available in two separate readmes:

- **Installation Guide**  
  → [README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE_english.md](README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE_english.md)

- **Using Your Own Programs & Display Utilities**  
  → [README_PROJECT_USAGE_english.md](README_PROJECT_USAGE_english.md)

### 🚀 Quick Start

```bash
cd /home/pi/Install_3.5_LCD_Display_Berrybase
sudo python3 main.py
```

After reboot, the second installation step starts automatically  
and then your program (`the_programm_main.py`).

### 📂 Project Structure

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
├── README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE_english.md
└── README_PROJECT_USAGE_english.md
```

### ⏱️ Installation Time

The initial installation typically takes **5-15 minutes**, depending on:

- Internet connection (for Git clone and package downloads)
- SD card speed
- System performance

The installation time is displayed in the test program after installation is complete.

### ℹ️ Technical Information

**Display Type:**

- **GoodTFT/XPT2046-based 3.5" SPI Displays**
- These displays do **NOT** use the Waveshare overlay
- Waveshare ≠ GoodTFT
- This is exactly why they do **NOT** work on Pi 5 under 64-bit without modifications

**Drivers:**

- fbtft, MHS35, rpi-fbcp
- Touch: XPT2046

**OS Compatibility:**

- This project was specifically developed for the OS image **2023-05-03-raspios-buster-armhf-lite**
- **Only 32-bit Buster is supported** - other images (64-bit, Bookworm, Bullseye) do not work
- 64-bit versions have been extensively tested and are **no longer supported**

### 🔗 References

- [Install 3.5" LCD Display Berrybase - This Project](https://github.com/tnt-nitro/Install_3.5_LCD_Display_Berrybase)
- [LCD-show GitHub Repository](https://github.com/goodtft/LCD-show)
