#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Haupt-Installer für LCD Display Berrybase
# Startet den Installationsprozess für das 3.5" LCD Display
# Run: sudo python3 /home/pi/main.py

import subprocess
import sys
import os

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

    # Installationsskript starten (mit stdin weiterleiten für interaktive Eingabe)
    print("Starte install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py")
    subprocess.run([sys.executable, script_path], stdin=sys.stdin)
