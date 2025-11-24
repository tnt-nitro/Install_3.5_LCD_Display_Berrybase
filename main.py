#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Haupt-Installer für LCD Display Berrybase
# Startet den Installationsprozess für das 3.5" LCD Display
# Run: sudo python3 /home/pi/main.py

import subprocess
import sys
import os
import time

if __name__ == "__main__":
    # ============================================================================
    # HAUPT-INSTALLER
    # ============================================================================

    # Pfad zum Installationsskript bestimmen
    script_path = os.path.join(os.path.dirname(
        __file__), "install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py")

    # Prüfen ob die Datei existiert
    if not os.path.exists(script_path):
        print(f"Fehler: {script_path} nicht gefunden!")
        sys.exit(1)

    # Startzeitpunkt speichern
    start_time_file = "/home/pi/.install_start_time"
    try:
        with open(start_time_file, "w") as f:
            f.write(str(time.time()))
    except Exception as e:
        print(f"Warnung: Konnte Startzeit nicht speichern: {e}")

    # Installationsskript starten (mit stdin weiterleiten für interaktive Eingabe)
    print("Starte install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py")
    subprocess.run([sys.executable, script_path], stdin=sys.stdin)
