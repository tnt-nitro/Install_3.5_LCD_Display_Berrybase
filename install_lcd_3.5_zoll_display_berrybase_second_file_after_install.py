#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Installer Teil 2 - LCD Display Berrybase
# Wird nach dem Reboot automatisch ausgeführt
# Erstellt den the-programm.service und startet das Programm
# Run: sudo python3 install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py

import os
import sys
import time
import subprocess

print("=== LCD Display Installation - Teil 2 ===")
print("")

# ============================================================================
# PRÜFUNG: SERVICE BEREITS VORHANDEN?
# ============================================================================
the_programm_service = "/etc/systemd/system/the-programm.service"
if os.path.exists(the_programm_service):
    print("the-programm.service existiert bereits - Installation bereits abgeschlossen")
    print("Deaktiviere diesen Service...")
    os.system("systemctl disable install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service >/dev/null 2>&1")
    sys.exit(0)

# ============================================================================
# SCHRITT 1: PFADE SETZEN
# ============================================================================
script_dir = "/home/pi"
the_programm_path = "/home/pi/the_programm_main.py"
log_dir = "/home/pi/logs"
log_file = "/home/pi/logs/the_programm.log"

# ============================================================================
# SCHRITT 2: DATEIEN PRÜFEN
# ============================================================================
print("1. Prüfe Dateien...")
if not os.path.exists(the_programm_path):
    print(f"   ✗ FEHLER: {the_programm_path} nicht gefunden!")
    sys.exit(1)
print("   ✓ Alle Dateien vorhanden")

# ============================================================================
# SCHRITT 3: LOG-VERZEICHNIS ERSTELLEN
# ============================================================================
print("2. Erstelle Log-Verzeichnis...")
os.makedirs(log_dir, exist_ok=True)
os.system(f"chmod 777 {log_dir} >/dev/null 2>&1")
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 4: GETTY@TTY1 DAUERHAFT MASKIEREN
# ============================================================================
print("3. Maskiere getty@tty1.service...")
# Zuerst maskieren (verhindert weiteren Start), dann stoppen mit Timeout
try:
    subprocess.run(["systemctl", "mask", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Stoppen mit Timeout - ignoriere Fehler falls bereits gestoppt
    subprocess.run(["systemctl", "stop", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.TimeoutExpired:
    print("   ⚠ Warnung: getty@tty1 konnte nicht gestoppt werden (wird beim nächsten Reboot maskiert sein)")
except Exception:
    pass  # Ignoriere andere Fehler
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 5: THE-PROGRAMM.SERVICE ERSTELLEN
# ============================================================================
print("4. Erstelle the-programm.service...")
service_content = f"""[Unit]
Description=The Programm für LCD Display
After=multi-user.target
Conflicts=getty@tty1.service
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory={script_dir}
# getty@tty1 sollte bereits maskiert sein, aber sicherheitshalber nochmal maskieren
# Verwende --no-block um Zyklen zu vermeiden
ExecStartPre=/bin/bash -c 'systemctl --no-block mask getty@tty1.service 2>/dev/null || true'
ExecStartPre=/bin/bash -c 'systemctl --no-block stop getty@tty1.service 2>/dev/null || true'
ExecStartPre=/bin/sleep 2
# Bildschirm leeren BEVOR das Programm startet
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

# ============================================================================
# SCHRITT 6: SERVICE AKTIVIEREN
# ============================================================================
print("5. Aktiviere the-programm.service...")
os.system("systemctl enable the-programm.service >/dev/null 2>&1")
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 7: SERVICE STARTEN
# ============================================================================
print("6. Starte the-programm.service...")
# getty@tty1 sicher stoppen und maskieren (mit Timeout)
try:
    subprocess.run(["systemctl", "stop", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["systemctl", "mask", "getty@tty1.service"],
                   timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except (subprocess.TimeoutExpired, Exception):
    pass  # Ignoriere Fehler - mask ist bereits gesetzt
time.sleep(2)
# Bildschirm leeren (nur wenn tty1 verfügbar ist)
try:
    with open("/dev/tty1", "w") as tty:
        tty.write("\033[2J\033[H")
except Exception:
    pass  # Ignoriere Fehler falls tty1 nicht verfügbar
time.sleep(1)
# Service starten mit Timeout
try:
    subprocess.run(["systemctl", "start", "the-programm.service"],
                   timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.TimeoutExpired:
    print("   ⚠ Warnung: Service-Start dauerte länger als erwartet")
except Exception as e:
    print(f"   ⚠ Warnung: Service konnte nicht gestartet werden: {e}")
time.sleep(3)
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 8: EIGENEN SERVICE DEAKTIVIEREN
# ============================================================================
print("7. Deaktiviere Installations-Service...")
os.system("systemctl disable install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service >/dev/null 2>&1")
print("   ✓ Fertig")

print("")
print("=== Installation abgeschlossen ===")
print("the-programm läuft jetzt auf dem LCD Display!")
print("")
