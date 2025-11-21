#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Deinstaller - LCD Display Berrybase (NUR AUTOSTART)
# Entfernt alle systemd Services und Installations-Skripte
# WICHTIG: Die LCD-Display-Installation und Programm-Dateien bleiben bestehen
# Das Display funktioniert weiterhin, nur der Autostart wird entfernt
# Run: sudo python3 /home/pi/uninstall_lcd_3.5_zoll_display_berrybase_autostart.py

import os
import sys
import subprocess
import time

print("=== LCD Display Berrybase Deinstaller - NUR AUTOSTART ===")
print()
print("Hinweis: Die LCD-Display-Installation (Treiber, config.txt) bleibt bestehen.")
print("Programm-Dateien bleiben erhalten für erneute Installation.")
print("Nur die Autostart-Services werden entfernt.")
print()

# ============================================================================
# ANALYSE DER INSTALLATION:
# ============================================================================
# First File Installer erstellt:
# 1. Service: install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
#    - Datei: /etc/systemd/system/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
#    - Script: /home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py
#    - Temp: /tmp/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
#
# Second File After Install erstellt:
# 2. Service: the-programm.service
#    - Datei: /etc/systemd/system/the-programm.service
#    - Temp: /tmp/the-programm.service
#    - Logs: /home/pi/logs/ (wird NICHT entfernt, da möglicherweise andere Logs enthalten)
#
# ============================================================================

# Services die entfernt werden sollen (in der Reihenfolge wie sie erstellt wurden)
services = [
    {
        "name": "install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service",
        "file": "/etc/systemd/system/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service",
        "description": "Install LCD 3.5 Zoll Display Berrybase Second File After Install Service",
        "script": None,  # Script wird NICHT entfernt, da für erneute Installation benötigt
        "temp_file": "/tmp/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service"
    },
    {
        "name": "the-programm.service",
        "file": "/etc/systemd/system/the-programm.service",
        "description": "The Programm Service",
        "script": None,  # Script wird nicht von dieser Installation kopiert
        "temp_file": "/tmp/the-programm.service"
    }
]

# Systemd-Verzeichnisse die geprüft werden sollen
systemd_dirs = [
    "/etc/systemd/system/",
    "/etc/systemd/system/multi-user.target.wants/",
    "/lib/systemd/system/",
    "/run/systemd/system/"
]

removed_count = 0

# ============================================================================
# SERVICES ENTFERNEN
# ============================================================================
for service in services:
    service_name = service["name"]
    service_file = service["file"]
    service_description = service["description"]
    script_file = service["script"]
    temp_file = service["temp_file"]

    print(f"--- {service_description} ---")

    # Prüfen ob Service existiert
    if not os.path.exists(service_file):
        print(f"Service-Datei nicht gefunden: {service_file}")
        print(f"Der {service_name} ist möglicherweise bereits entfernt.")
        print()
        continue

    print(f"Service-Datei gefunden: {service_file}")

    # Service maskieren ZUERST (verhindert Neustart bei Restart=always)
    # WICHTIG: Maskieren muss VOR dem Löschen der Datei passieren!
    print(f"Maskiere {service_name} (verhindert Neustart)...")
    result = subprocess.run(
        ["sudo", "systemctl", "mask", service_name],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  {service_name} maskiert.")
    else:
        # Wenn mask fehlschlägt (z.B. Datei existiert nicht), ignorieren
        if "already exists" not in result.stderr.lower() and "does not exist" not in result.stderr.lower():
            print(f"  Warnung beim Maskieren: {result.stderr}")

    # Service stoppen (mehrfach versuchen bei Restart=always)
    print(f"Stoppe {service_name}...")
    max_attempts = 3
    for attempt in range(max_attempts):
        result = subprocess.run(
            ["sudo", "systemctl", "stop", service_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Prüfen ob Service wirklich gestoppt ist
            time.sleep(1)
            check_result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True
            )
            if check_result.stdout.strip() == "inactive":
                print(f"  {service_name} gestoppt.")
                break
            else:
                if attempt < max_attempts - 1:
                    print(
                        f"  Service läuft noch, versuche erneut... (Versuch {attempt + 2}/{max_attempts})")
                else:
                    print(f"  WARNUNG: Service läuft möglicherweise noch!")
        else:
            if attempt < max_attempts - 1:
                print(
                    f"  Warnung beim Stoppen, versuche erneut... (Versuch {attempt + 2}/{max_attempts})")
            else:
                print(f"  Warnung beim Stoppen: {result.stderr}")

    # Service deaktivieren
    print(f"Deaktiviere {service_name}...")
    result = subprocess.run(
        ["sudo", "systemctl", "disable", service_name],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  {service_name} deaktiviert.")
    else:
        print(f"  Warnung beim Deaktivieren: {result.stderr}")

    # Service-Datei löschen
    print(f"Lösche Service-Datei...")
    result = subprocess.run(
        ["sudo", "rm", "-f", service_file],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  Service-Datei gelöscht: {service_file}")
        removed_count += 1
    else:
        print(f"  Fehler beim Löschen: {result.stderr}")

    # Symlinks in allen systemd-Verzeichnissen entfernen
    for systemd_dir in systemd_dirs:
        symlink_path = os.path.join(systemd_dir, service_name)
        if os.path.exists(symlink_path) or os.path.islink(symlink_path):
            print(f"  Entferne Symlink: {symlink_path}")
            result = subprocess.run(
                ["sudo", "rm", "-f", symlink_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"    Symlink entfernt.")
            else:
                print(
                    f"    Warnung beim Entfernen des Symlinks: {result.stderr}")

    # Service-Datei in allen systemd-Verzeichnissen suchen und entfernen
    for systemd_dir in systemd_dirs:
        service_file_path = os.path.join(systemd_dir, service_name)
        if os.path.exists(service_file_path) and service_file_path != service_file:
            print(f"  Entferne Service-Datei: {service_file_path}")
            result = subprocess.run(
                ["sudo", "rm", "-f", service_file_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"    Service-Datei entfernt.")
            else:
                print(f"    Warnung beim Entfernen: {result.stderr}")

    # Verifizieren dass Datei wirklich gelöscht wurde
    if os.path.exists(service_file):
        print(f"  WARNUNG: Service-Datei existiert noch: {service_file}")
        print("  Versuche erneut zu löschen...")
        result = subprocess.run(
            ["sudo", "rm", "-f", service_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and not os.path.exists(service_file):
            print(f"    Service-Datei erfolgreich gelöscht.")
        else:
            print(f"    FEHLER: Service-Datei konnte nicht gelöscht werden!")

    # Service-Maske entfernen (falls vorhanden, nach dem Löschen der Datei)
    mask_path = f"/etc/systemd/system/{service_name}"
    if os.path.exists(mask_path) and os.path.islink(mask_path):
        try:
            link_target = os.readlink(mask_path)
            if link_target == "/dev/null":
                print(f"  Entferne Service-Maske: {mask_path}")
                result = subprocess.run(
                    ["sudo", "systemctl", "unmask", service_name],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"    Service-Maske entfernt.")
                else:
                    print(
                        f"    Warnung beim Entfernen der Maske: {result.stderr}")
        except Exception:
            pass

    print()

# ============================================================================
# KOPIERTE DATEIEN ENTFERNEN
# ============================================================================
print("--- Kopierte Dateien entfernen ---")

for service in services:
    script_file = service["script"]
    temp_file = service["temp_file"]

    # Script-Dateien entfernen
    if script_file and os.path.exists(script_file):
        print(f"Entferne Script: {script_file}")
        result = subprocess.run(
            ["sudo", "rm", "-f", script_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  Script entfernt.")
        else:
            print(f"  Warnung beim Entfernen: {result.stderr}")

    # Temporäre Service-Dateien entfernen
    if temp_file and os.path.exists(temp_file):
        print(f"Entferne temporäre Datei: {temp_file}")
        result = subprocess.run(
            ["sudo", "rm", "-f", temp_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  Temporäre Datei entfernt.")
        else:
            print(f"  Warnung beim Entfernen: {result.stderr}")

# Programm-Dateien werden NICHT entfernt, da sie für eine erneute Installation benötigt werden
# Diese Dateien bleiben erhalten:
# - /home/pi/the_programm_main.py
# - /home/pi/the_programm_display_utils.py
# - /home/pi/the_programm_display_berrybase_test.py

# Log-Datei des Installationsskripts entfernen
log_file = "/home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.log"
if os.path.exists(log_file):
    print(f"Entferne Log-Datei: {log_file}")
    result = subprocess.run(
        ["sudo", "rm", "-f", log_file],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  Log-Datei entfernt.")
    else:
        print(f"  Warnung beim Entfernen: {result.stderr}")

print()

# ============================================================================
# SYSTEMD NEU LADEN
# ============================================================================
if removed_count > 0:
    print("--- systemd neu laden ---")
    result = subprocess.run(
        ["sudo", "systemctl", "daemon-reload"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("systemd neu geladen.")
    else:
        print(f"Warnung beim Neuladen: {result.stderr}")
    print()

# ============================================================================
# FINALE PRÜFUNG
# ============================================================================
print("--- Finale Prüfung ---")
found_remaining = False
for systemd_dir in systemd_dirs:
    if os.path.exists(systemd_dir):
        for service in services:
            service_name = service["name"]
            check_path = os.path.join(systemd_dir, service_name)
            if os.path.exists(check_path) or os.path.islink(check_path):
                print(f"WARNUNG: Noch vorhanden: {check_path}")
                found_remaining = True
                # Versuche nochmal zu löschen
                result = subprocess.run(
                    ["sudo", "rm", "-f", check_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"  -> Erfolgreich entfernt")
                else:
                    print(f"  -> FEHLER: Konnte nicht entfernt werden!")

if not found_remaining:
    print("Alle Service-Dateien und Symlinks wurden erfolgreich entfernt.")
print()

# ============================================================================
# ZUSAMMENFASSUNG
# ============================================================================
print("=== Deinstallation abgeschlossen ===")
print()
print(f"{removed_count} Service(s) wurden erfolgreich entfernt.")
print("Der Autostart ist jetzt deaktiviert.")
print()
print("Entfernt wurden:")
print("  - Service-Dateien in /etc/systemd/system/")
print("  - Symlinks in systemd-Verzeichnissen")
print("  - Temporäre Service-Dateien in /tmp/")
print()
print("NICHT entfernt (für erneute Installation erhalten):")
print("  - /home/pi/LCD-show/ (LCD-Treiber)")
print("  - /boot/config.txt (dtoverlay=waveshare35a:rotate=270)")
print("  - Installierte Pakete (git, dos2unix, xserver-xorg-input-evdev)")
print("  - /home/pi/logs/ (Log-Verzeichnis)")
print("  - /home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py (Installations-Skript)")
print("  - /home/pi/the_programm_main.py (Programm-Dateien)")
print("  - /home/pi/the_programm_display_utils.py")
print("  - /home/pi/the_programm_display_berrybase_test.py")
print()
print("Hinweis: Die LCD-Display-Installation und Programm-Dateien bleiben bestehen.")
print("Das Display funktioniert weiterhin, nur der Autostart ist deaktiviert.")
print("Eine erneute Installation ist ohne erneutes Kopieren der Dateien möglich.")
print()
print("=== Starte Reboot in 5 Sekunden ===")
print("Drücken Sie Ctrl+C zum Abbrechen...")
try:
    for i in range(5, 0, -1):
        print(f"Reboot in {i} Sekunden...", end='\r')
        time.sleep(1)
    print("\nReboot wird jetzt durchgeführt...")
    # Reboot mit subprocess für bessere Zuverlässigkeit
    subprocess.run(["sudo", "reboot"], check=False)
except KeyboardInterrupt:
    print("\nReboot abgebrochen.")
    sys.exit(0)
except Exception as e:
    print(f"\nFehler beim Reboot: {e}")
    print("Bitte manuell rebooten: sudo reboot")
    sys.exit(1)
