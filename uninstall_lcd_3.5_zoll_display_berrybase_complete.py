#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Deinstaller - LCD Display Berrybase (VOLLSTÄNDIG)
# Entfernt: Services, LCD-Treiber, config.txt-Änderungen
# BEHÄLT: Programm-Dateien und Logs (für erneute Installation)
# WICHTIG: Diese Deinstallation setzt die LCD-Installation zurück
# Run: sudo python3 /home/pi/uninstall_lcd_3.5_zoll_display_berrybase_complete.py

import os
import sys
import subprocess
import time

print("=== LCD Display Berrybase VOLLSTÄNDIGER Deinstaller ===")
print()
print("WARNUNG: Diese Deinstallation setzt die LCD-Installation zurück!")
print("Entfernt werden:")
print("  - Alle Services und Autostart")
print("  - LCD-Treiber (/home/pi/LCD-show/)")
print("  - config.txt Änderungen (dtoverlay)")
print()
print("BEHALTEN werden (für erneute Installation):")
print("  - Programm-Dateien (/home/pi/the_programm_*.py)")
print("  - Installations-Skripte (/home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py)")
print("  - Log-Verzeichnis und Log-Dateien (/home/pi/logs/)")
print()
print("Das Display wird nach dieser Deinstallation NICHT mehr funktionieren (weißer Bildschirm)!")
print("Eine erneute Installation mit main.py ist möglich.")
print()
response = input("Möchten Sie wirklich fortfahren? (ja/nein): ")
if response.lower() not in ["ja", "j", "yes", "y"]:
    print("Deinstallation abgebrochen.")
    sys.exit(0)
print()

# ============================================================================
# ANALYSE DER INSTALLATION:
# ============================================================================
# First File Installer erstellt:
# 1. Service: install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
#    - Datei: /etc/systemd/system/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
#    - Script: /home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py
#    - Temp: /tmp/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
# 2. /home/pi/LCD-show/ (LCD-Treiber)
# 3. /boot/config.txt (dtoverlay=waveshare35a:rotate=270)
# 4. Installierte Pakete: git, dos2unix, xserver-xorg-input-evdev
#
# Second File After Install erstellt:
# 5. Service: the-programm.service
#    - Datei: /etc/systemd/system/the-programm.service
#    - Temp: /tmp/the-programm.service
#    - Logs: /home/pi/logs/
# 6. Log-Datei: /home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.log
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
        "script": None,
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
print("=== 1. SERVICES ENTFERNEN ===")
print()
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
print("=== 2. KOPIERTE DATEIEN ENTFERNEN ===")
print()

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

# Log-Dateien werden NICHT entfernt, da sie für Diagnosezwecke nützlich sein können
# Log-Datei: /home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.log bleibt erhalten

print()

# ============================================================================
# LCD-TREIBER ENTFERNEN
# ============================================================================
print("=== 3. LCD-TREIBER ENTFERNEN ===")
print()

lcd_show_dir = "/home/pi/LCD-show"
if os.path.exists(lcd_show_dir):
    print(f"Entferne LCD-Treiber: {lcd_show_dir}")
    result = subprocess.run(
        ["sudo", "rm", "-rf", lcd_show_dir],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  LCD-Treiber entfernt.")
    else:
        print(f"  Warnung beim Entfernen: {result.stderr}")
else:
    print(f"LCD-Treiber nicht gefunden: {lcd_show_dir}")

print()

# ============================================================================
# CONFIG.TXT ÄNDERUNGEN ENTFERNEN
# ============================================================================
print("=== 4. CONFIG.TXT ÄNDERUNGEN ENTFERNEN ===")
print()

# Prüfen ob /boot gemountet ist
CONFIG = "/boot/config.txt"
if not os.path.exists(CONFIG):
    # Versuche /boot/firmware/config.txt (neue Raspberry Pi OS Versionen)
    CONFIG = "/boot/firmware/config.txt"

if not os.path.exists(CONFIG):
    print(f"WARNUNG: config.txt nicht gefunden!")
    print("  Erwartet: /boot/config.txt oder /boot/firmware/config.txt")
else:
    print(f"Bearbeite: {CONFIG}")

    # Prüfen ob /boot gemountet ist (read-only)
    # Versuche zu mounten falls nötig
    if not os.access(CONFIG, os.W_OK):
        print("  /boot ist read-only, versuche zu mounten...")
        result = subprocess.run(
            ["sudo", "mount", "-o", "remount,rw", "/boot"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # Versuche /boot/firmware
            result = subprocess.run(
                ["sudo", "mount", "-o", "remount,rw", "/boot/firmware"],
                capture_output=True,
                text=True
            )

    try:
        # config.txt lesen
        with open(CONFIG, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # dtoverlay-Zeilen entfernen
        new_lines = []
        removed_lines = []
        for line in lines:
            if line.startswith("dtoverlay=waveshare35"):
                removed_lines.append(line.strip())
                continue
            new_lines.append(line)

        if removed_lines:
            print(f"  Entferne dtoverlay-Zeilen: {', '.join(removed_lines)}")

            # Zurückschreiben
            temp_config = "/tmp/config.txt"
            with open(temp_config, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            result = subprocess.run(
                ["sudo", "cp", temp_config, CONFIG],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  config.txt erfolgreich aktualisiert.")
                os.system("sync")
            else:
                print(f"  FEHLER beim Aktualisieren: {result.stderr}")
        else:
            print(f"  Keine dtoverlay-Zeilen gefunden (bereits entfernt?).")

    except Exception as e:
        print(f"  FEHLER beim Bearbeiten von config.txt: {e}")

print()

# ============================================================================
# LOG-VERZEICHNIS BEHALTEN
# ============================================================================
print("=== 5. LOG-VERZEICHNIS ===")
print()

log_dir = "/home/pi/logs"
if os.path.exists(log_dir):
    print(f"Log-Verzeichnis bleibt erhalten: {log_dir}")
    print("  (Logs werden für Diagnosezwecke behalten)")
else:
    print(f"Log-Verzeichnis nicht gefunden: {log_dir}")

print()

# ============================================================================
# GETTY@TTY1 WIEDERHERSTELLEN
# ============================================================================
print("=== 6. GETTY@TTY1 WIEDERHERSTELLEN ===")
print()

# getty@tty1 unmasken und starten, damit Login wieder funktioniert
print("Stelle getty@tty1 wieder her...")
try:
    result = subprocess.run(
        ["sudo", "systemctl", "unmask", "getty@tty1.service"],
        timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    result = subprocess.run(
        ["sudo", "systemctl", "enable", "getty@tty1.service"],
        timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    result = subprocess.run(
        ["sudo", "systemctl", "start", "getty@tty1.service"],
        timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    print("  getty@tty1 wiederhergestellt.")
except Exception:
    print("  Warnung: getty@tty1 konnte nicht wiederhergestellt werden.")

print()

# ============================================================================
# INSTALLIERTE PAKETE ENTFERNEN (OPTIONAL)
# ============================================================================
print("=== 7. INSTALLIERTE PAKETE ENTFERNEN (OPTIONAL) ===")
print()
print("Die folgenden Pakete wurden während der Installation installiert:")
print("  - git")
print("  - dos2unix")
print("  - xserver-xorg-input-evdev")
print()
response = input("Möchten Sie diese Pakete auch entfernen? (ja/nein): ")
if response.lower() in ["ja", "j", "yes", "y"]:
    packages = ["git", "dos2unix", "xserver-xorg-input-evdev"]
    for package in packages:
        print(f"Entferne Paket: {package}")
        result = subprocess.run(
            ["sudo", "apt-get", "remove", "-y", package],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  {package} entfernt.")
        else:
            print(f"  Warnung beim Entfernen: {result.stderr}")
    print()
else:
    print("Pakete bleiben installiert.")
    print()

# ============================================================================
# SYSTEMD NEU LADEN
# ============================================================================
if removed_count > 0:
    print("=== 8. SYSTEMD NEU LADEN ===")
    print()
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
print("=== 9. FINALE PRÜFUNG ===")
print()
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
print("=== VOLLSTÄNDIGE DEINSTALLATION ABGESCHLOSSEN ===")
print()
print(f"{removed_count} Service(s) wurden erfolgreich entfernt.")
print()
print("Entfernt wurden:")
print("  - Service-Dateien in /etc/systemd/system/")
print("  - Symlinks in systemd-Verzeichnissen")
print("  - Temporäre Service-Dateien in /tmp/")
print("  - /home/pi/LCD-show/ (LCD-Treiber)")
print("  - dtoverlay-Zeilen aus /boot/config.txt")
print()
print("NICHT entfernt (für erneute Installation erhalten):")
print("  - /home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py (Installations-Skript)")
print("  - /home/pi/the_programm_main.py (Programm-Dateien)")
print("  - /home/pi/the_programm_display_utils.py")
print("  - /home/pi/the_programm_display_berrybase_test.py")
print("  - /home/pi/logs/ (Log-Verzeichnis)")
print("  - Log-Dateien")
print()
print("Hinweis: Die LCD-Display-Installation wurde zurückgesetzt.")
print("Das Display funktioniert nach dem Reboot NICHT mehr (weißer Bildschirm).")
print("Programm-Dateien und Logs bleiben erhalten für erneute Installation.")
print("Eine erneute Installation mit main.py ist möglich.")
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
