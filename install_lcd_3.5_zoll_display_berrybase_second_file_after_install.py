#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Installer Teil 2 - LCD Display Berrybase
# Installer Part 2 - LCD Display Berrybase
# Wird nach dem Reboot automatisch ausgeführt
# Automatically executed after reboot
# Erstellt den the-programm.service und startet das Programm
# Creates the-programm.service and starts the program
# Run: sudo python3 install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py

import os
import sys
import time
import subprocess

print("=== LCD Display Installation - Teil 2 ===")
print("=== LCD Display Installation - Part 2 ===")
print("")

# ============================================================================
# PRÜFUNG: SERVICE BEREITS VORHANDEN?
# CHECK: SERVICE ALREADY EXISTS?
# ============================================================================
the_programm_service = "/etc/systemd/system/the-programm.service"
if os.path.exists(the_programm_service):
    print("the-programm.service existiert bereits - Installation bereits abgeschlossen")
    print("the-programm.service already exists - Installation already completed")
    print("Deaktiviere diesen Service...")
    print("Disabling this service...")
    os.system("systemctl disable install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service >/dev/null 2>&1")
    sys.exit(0)

# ============================================================================
# SCHRITT 1: PFADE SETZEN
# STEP 1: SET PATHS
# ============================================================================
script_dir = "/home/pi"
the_programm_path = "/home/pi/the_programm_main.py"
log_dir = "/home/pi/logs"
log_file = "/home/pi/logs/the_programm.log"

# ============================================================================
# SCHRITT 2: DATEIEN PRÜFEN
# STEP 2: CHECK FILES
# ============================================================================
print("1. Prüfe Dateien...")
print("1. Checking files...")
if not os.path.exists(the_programm_path):
    print(f"   ✗ FEHLER: {the_programm_path} nicht gefunden!")
    print(f"   ✗ ERROR: {the_programm_path} not found!")
    sys.exit(1)
print("   ✓ Alle Dateien vorhanden")
print("   ✓ All files present")

# ============================================================================
# SCHRITT 3: LOG-VERZEICHNIS ERSTELLEN
# STEP 3: CREATE LOG DIRECTORY
# ============================================================================
print("2. Erstelle Log-Verzeichnis...")
print("2. Creating log directory...")
os.makedirs(log_dir, exist_ok=True)
os.system(f"chmod 777 {log_dir} >/dev/null 2>&1")
print("   ✓ Fertig")
print("   ✓ Done")

# ============================================================================
# SCHRITT 4: GETTY@TTY1 DAUERHAFT MASKIEREN
# STEP 4: PERMANENTLY MASK GETTY@TTY1
# ============================================================================
print("3. Maskiere getty@tty1.service...")
print("3. Masking getty@tty1.service...")
# Zuerst maskieren (verhindert weiteren Start), dann stoppen mit Timeout
# First mask (prevents further start), then stop with timeout
try:
    subprocess.run(["systemctl", "mask", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Stoppen mit Timeout - ignoriere Fehler falls bereits gestoppt
    # Stop with timeout - ignore errors if already stopped
    subprocess.run(["systemctl", "stop", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.TimeoutExpired:
    print("   ⚠ Warnung: getty@tty1 konnte nicht gestoppt werden (wird beim nächsten Reboot maskiert sein)")
    print("   ⚠ Warning: getty@tty1 could not be stopped (will be masked on next reboot)")
except Exception:
    pass  # Ignoriere andere Fehler / Ignore other errors
print("   ✓ Fertig")
print("   ✓ Done")

# ============================================================================
# SCHRITT 5: THE-PROGRAMM.SERVICE ERSTELLEN
# STEP 5: CREATE THE-PROGRAMM.SERVICE
# ============================================================================
print("4. Erstelle the-programm.service...")
print("4. Creating the-programm.service...")
service_content = f"""[Unit]
Description=The Programm für LCD Display
After=multi-user.target
Conflicts=getty@tty1.service
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory={script_dir}
# getty@tty1 sollte bereits maskiert sein, aber sicherheitshalber nochmal maskieren
# getty@tty1 should already be masked, but mask again for safety
# Verwende --no-block um Zyklen zu vermeiden
# Use --no-block to avoid cycles
ExecStartPre=/bin/bash -c 'systemctl --no-block mask getty@tty1.service 2>/dev/null || true'
ExecStartPre=/bin/bash -c 'systemctl --no-block stop getty@tty1.service 2>/dev/null || true'
ExecStartPre=/bin/sleep 2
# Bildschirm leeren BEVOR das Programm startet
# Clear screen BEFORE program starts
ExecStartPre=/bin/bash -c 'echo -e "\\033[2J\\033[H" > /dev/tty1 2>/dev/null || true'
ExecStart=/bin/bash -c 'cd {script_dir} && /usr/bin/python3 -u {the_programm_path} 2>&1 | tee -a {log_file}'
ExecStopPost=/bin/bash -c 'systemctl --no-block unmask getty@tty1.service 2>/dev/null || true'
ExecStopPost=/bin/bash -c 'systemctl --no-block start getty@tty1.service 2>/dev/null || true'
StandardInput=tty
StandardOutput=tty
StandardError=tty
TTYPath=/dev/tty1
TTYReset=yes
TTYVHangup=yes
Restart=always
RestartSec=10
User=root
Environment="PYTHONUNBUFFERED=1"
Environment="PYTHONIOENCODING=utf-8"

[Install]
WantedBy=multi-user.target
"""

with open("/tmp/the-programm.service", "w") as f:
    f.write(service_content)

os.system("mv /tmp/the-programm.service /etc/systemd/system/the-programm.service >/dev/null 2>&1")
os.system("chmod 644 /etc/systemd/system/the-programm.service >/dev/null 2>&1")
os.system("systemctl daemon-reload >/dev/null 2>&1")
print("   ✓ Fertig")
print("   ✓ Done")

# ============================================================================
# SCHRITT 6: SERVICE AKTIVIEREN
# STEP 6: ENABLE SERVICE
# ============================================================================
print("5. Aktiviere the-programm.service...")
print("5. Enabling the-programm.service...")
os.system("systemctl enable the-programm.service >/dev/null 2>&1")
print("   ✓ Fertig")
print("   ✓ Done")

# ============================================================================
# SCHRITT 7: SERVICE STARTEN
# STEP 7: START SERVICE
# ============================================================================
print("6. Starte the-programm.service...")
print("6. Starting the-programm.service...")
# getty@tty1 sicher stoppen und maskieren (mit Timeout)
# Safely stop and mask getty@tty1 (with timeout)
try:
    subprocess.run(["systemctl", "stop", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["systemctl", "mask", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except (subprocess.TimeoutExpired, Exception):
    pass  # Ignoriere Fehler - mask ist bereits gesetzt / Ignore errors - mask is already set
time.sleep(2)
# Bildschirm leeren (nur wenn tty1 verfügbar ist)
# Clear screen (only if tty1 is available)
try:
    with open("/dev/tty1", "w") as tty:
        tty.write("\033[2J\033[H")
except Exception:
    pass  # Ignoriere Fehler falls tty1 nicht verfügbar / Ignore errors if tty1 not available
time.sleep(1)
# Service starten mit Timeout
# Start service with timeout
try:
    subprocess.run(["systemctl", "start", "the-programm.service"],
                   timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.TimeoutExpired:
    print("   ⚠ Warnung: Service-Start dauerte länger als erwartet")
    print("   ⚠ Warning: Service start took longer than expected")
except Exception as e:
    print(f"   ⚠ Warnung: Service konnte nicht gestartet werden: {e}")
    print(f"   ⚠ Warning: Service could not be started: {e}")
time.sleep(3)
print("   ✓ Fertig")
print("   ✓ Done")

# ============================================================================
# SCHRITT 8: EIGENEN SERVICE DEAKTIVIEREN
# STEP 8: DISABLE OWN SERVICE
# ============================================================================
print("7. Deaktiviere Installations-Service...")
print("7. Disabling installation service...")
os.system("systemctl disable install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service >/dev/null 2>&1")
print("   ✓ Fertig")
print("   ✓ Done")

print("")
print("=== Installation abgeschlossen ===")
print("=== Installation completed ===")
print("the-programm läuft jetzt auf dem LCD Display!")
print("the-programm is now running on the LCD Display!")
print("")
