#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Haupt-Installer für LCD Display Berrybase
# Main installer for LCD Display Berrybase
# Startet den Installationsprozess für das 3.5" LCD Display
# Starts the installation process for the 3.5" LCD Display
# Run: sudo python3 /home/pi/main.py

import subprocess
import sys
import os
import time

if __name__ == "__main__":
    # ============================================================================
    # HAUPT-INSTALLER
    # MAIN INSTALLER
    # ============================================================================

    # Pfad zum Installationsskript bestimmen
    # Determine path to installation script
    script_path = os.path.join(os.path.dirname(
        __file__), "install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py")

    # Prüfen ob die Datei existiert
    # Check if the file exists
    if not os.path.exists(script_path):
        print(f"Fehler: {script_path} nicht gefunden!")
        print(f"Error: {script_path} not found!")
        sys.exit(1)

    # Startzeitpunkt speichern
    start_time_file = "/home/pi/.install_start_time"
    try:
        with open(start_time_file, "w") as f:
            f.write(str(time.time()))
    except Exception as e:
        print(f"Warnung: Konnte Startzeit nicht speichern: {e}")

    # Installationsskript starten (mit stdin weiterleiten für interaktive Eingabe)
    # Start installation script (with stdin forwarding for interactive input)
    print("Starte install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py")
    print("Starting install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py")
    subprocess.run([sys.executable, script_path], stdin=sys.stdin)
