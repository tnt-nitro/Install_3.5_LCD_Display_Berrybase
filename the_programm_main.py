#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Hauptprogramm-Wrapper für LCD Display Berrybase
# Startet das eigentliche Hauptprogramm (aktuell Testprogramm)
# Run: sudo python3 /home/pi/the_programm_main.py

import subprocess
import sys
import os

if __name__ == "__main__":
    # ============================================================================
    # HAUPTPROGRAMM-WRAPPER
    # ============================================================================
    
    # TODO: Hier später den Pfad zum eigentlichen Hauptprogramm eintragen
    # Beispiel: script_path = "/pfad/zum/eigentlichen/programm.py"
    
    # Aktuell: Testprogramm verwenden
    script_path = os.path.join(os.path.dirname(
        __file__), "the_programm_display_berrybase_test.py")

    # Prüfen ob die Datei existiert
    if not os.path.exists(script_path):
        print(f"Fehler: Hauptprogramm nicht gefunden!")
        print(f"Erwartet: {script_path}")
        sys.exit(1)

    # Hauptprogramm starten (mit stdin weiterleiten für interaktive Eingabe)
    print(f"Starte {os.path.basename(script_path)}")
    subprocess.run([sys.executable, script_path], stdin=sys.stdin)
