#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Hauptprogramm-Wrapper für LCD Display Berrybase
# Main program wrapper for LCD Display Berrybase
# Startet das eigentliche Hauptprogramm (aktuell Testprogramm)
# Starts the actual main program (currently test program)
# Run: sudo python3 /home/pi/the_programm_main.py

import subprocess
import sys
import os

if __name__ == "__main__":
    # ============================================================================
    # HAUPTPROGRAMM-WRAPPER
    # MAIN PROGRAM WRAPPER
    # ============================================================================

    # TODO: Hier später den Pfad zum eigentlichen Hauptprogramm eintragen
    # TODO: Enter path to actual main program here later
    # Beispiel: script_path = "/pfad/zum/eigentlichen/programm.py"
    # Example: script_path = "/path/to/actual/program.py"

    # Aktuell: Testprogramm verwenden
    # Currently: Use test program
    script_path = os.path.join(os.path.dirname(
        __file__), "the_programm_display_berrybase_test.py")

    # Prüfen ob die Datei existiert
    # Check if the file exists
    if not os.path.exists(script_path):
        print(f"Fehler: Hauptprogramm nicht gefunden!")
        print(f"Error: Main program not found!")
        print(f"Erwartet: {script_path}")
        print(f"Expected: {script_path}")
        sys.exit(1)

    # Hauptprogramm starten (mit stdin weiterleiten für interaktive Eingabe)
    # Start main program (with stdin forwarding for interactive input)
    print(f"Starte {os.path.basename(script_path)}")
    print(f"Starting {os.path.basename(script_path)}")
    subprocess.run([sys.executable, script_path], stdin=sys.stdin)
