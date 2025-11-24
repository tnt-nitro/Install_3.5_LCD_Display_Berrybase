#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Installer Teil 1 - LCD Display Berrybase
# Installiert das 3.5" LCD Display auf dem Raspberry Pi
# Bereitet System vor, installiert Treiber und kopiert Dateien
# Run: sudo python3 install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py

import os
import sys
import time
import subprocess
import re
import shutil

print("=== LCD Display Installation - Teil 1 ===")
print("")

# ============================================================================
# HILFSFUNKTION: APT-GET MIT PROGRESSBAR
# ============================================================================


def run_apt_with_progress(command, description):
    """Führt apt-get aus und zeigt echten Progressbar mit KB-Informationen"""
    print(f"{description}")

    # Terminal-Breite für Progressbar
    try:
        terminal_size = shutil.get_terminal_size()
        terminal_width = terminal_size.columns
    except (OSError, AttributeError):
        terminal_width = 80
    bar_width = min(50, terminal_width - 30)

    # Prozess starten
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

    current_package = ""
    downloaded_kb = 0
    total_kb = 0
    last_status = ""
    line_count = 0
    last_update_time = time.time()

    # Zeilen in Echtzeit verarbeiten
    while True:
        line = process.stdout.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue

        line_count += 1
        current_time = time.time()

        # Fallback: Zeige zumindest, dass etwas passiert (alle 2 Sekunden)
        if current_time - last_update_time > 2.0 and not last_status:
            status = "Arbeite..."
            print(f"\r   {status}", end="", flush=True)
            last_status = status
            last_update_time = current_time

        # Parse "Get: X http://..." Zeilen für Downloads
        # Format: "Get:1 http://... package.deb 1234 kB"
        get_match = re.search(
            r'Get:\s+\d+\s+.*?\s+([\d.]+)\s*(B|kB|MB|GB|b|kb|mb|gb)', line, re.IGNORECASE)
        if get_match:
            size = float(get_match.group(1))
            unit = get_match.group(2).lower()

            # In KB umrechnen
            if unit == 'b':
                size_kb = size / 1024
            elif unit == 'kb':
                size_kb = size
            elif unit == 'mb':
                size_kb = size * 1024
            elif unit == 'gb':
                size_kb = size * 1024 * 1024
            else:
                size_kb = size

            total_kb += size_kb

            # Versuche Paketnamen zu extrahieren
            package_match = re.search(r'/([^/\s]+\.(deb|udeb))', line)
            if package_match:
                current_package = package_match.group(1)[:40]
            else:
                current_package = "Paket"

            status = f"Lade: {current_package} ({size_kb:.1f} KB)"
            last_update_time = current_time

            # Progressbar anzeigen
            if len(status) != len(last_status):
                print("\r" + " " * (terminal_width - 1), end="", flush=True)
            print(f"\r   {status}", end="", flush=True)
            last_status = status

        # Parse "Fetched X kB" Zeilen
        fetched_match = re.search(
            r'Fetched\s+([\d.]+)\s*(B|kB|MB|GB|b|kb|mb|gb)', line, re.IGNORECASE)
        if fetched_match:
            fetched = float(fetched_match.group(1))
            unit = fetched_match.group(2).lower()

            # In KB umrechnen
            if unit == 'b':
                fetched_kb = fetched / 1024
            elif unit == 'kb':
                fetched_kb = fetched
            elif unit == 'mb':
                fetched_kb = fetched * 1024
            elif unit == 'gb':
                fetched_kb = fetched * 1024 * 1024
            else:
                fetched_kb = fetched

            downloaded_kb = fetched_kb
            status = f"Geladen: {downloaded_kb:.1f} KB"
            last_update_time = current_time
            print(f"\r   {status}", end="", flush=True)
            last_status = status

        # Parse "Unpacking ..." Zeilen
        if "Unpacking" in line:
            unpack_match = re.search(r'Unpacking\s+(.+)', line)
            if unpack_match:
                package = unpack_match.group(1).split()[0]
                current_package = package[:40]
                status = f"Entpacke: {current_package}"
                last_update_time = current_time
                if len(status) != len(last_status):
                    print("\r" + " " * (terminal_width - 1), end="", flush=True)
                print(f"\r   {status}", end="", flush=True)
                last_status = status

        # Parse "Setting up ..." Zeilen
        if "Setting up" in line:
            setup_match = re.search(r'Setting up\s+(.+)', line)
            if setup_match:
                package = setup_match.group(1).split()[0]
                current_package = package[:40]
                status = f"Installiere: {current_package}"
                last_update_time = current_time
                if len(status) != len(last_status):
                    print("\r" + " " * (terminal_width - 1), end="", flush=True)
                print(f"\r   {status}", end="", flush=True)
                last_status = status

        # Parse "Reading package lists..." und ähnliche Statusmeldungen
        if any(keyword in line for keyword in ["Reading package lists", "Building dependency tree",
                                               "Selecting previously unselected", "Preparing to unpack",
                                               "Processing triggers"]):
            # Kürze Statusmeldung falls nötig
            status = line[:min(60, terminal_width - 5)]
            last_update_time = current_time
            if len(status) != len(last_status):
                print("\r" + " " * (terminal_width - 1), end="", flush=True)
            print(f"\r   {status}", end="", flush=True)
            last_status = status

    # Warte auf Prozess-Ende
    return_code = process.wait()

    # Letzte Zeile löschen und neue Zeile
    print("\r" + " " * (terminal_width - 1), end="", flush=True)

    if return_code == 0:
        # Zeige geladene KB (priorisiere downloaded_kb, sonst total_kb)
        final_kb = downloaded_kb if downloaded_kb > 0 else total_kb
        if final_kb > 0:
            print(f"\r   ✓ Fertig ({final_kb:.1f} KB geladen)")
        else:
            print(f"\r   ✓ Fertig")
    else:
        print(
            f"\r   ✗ FEHLER: Installation fehlgeschlagen (Code: {return_code})")
        return False

    return True


# ============================================================================
# SCHRITT 1: SYSTEM VORBEREITEN
# ============================================================================
print("1. Installiere benötigte Pakete...")
if not run_apt_with_progress("apt-get update -y", "   Aktualisiere Paketlisten..."):
    sys.exit(1)

if not run_apt_with_progress("apt-get install -y git dos2unix xserver-xorg-input-evdev", "   Installiere Pakete..."):
    sys.exit(1)

# ============================================================================
# SCHRITT 2: LCD-SHOW REPOSITORY HOLEN
# ============================================================================
print("2. Lade LCD-show Repository...")
lcd_show_dir = "/home/pi/LCD-show"
os.system(f"rm -rf {lcd_show_dir} >/dev/null 2>&1")

# Retry-Mechanismus für git clone
for attempt in range(3):
    if os.system(f"cd /home/pi && git clone https://github.com/waveshare/LCD-show.git >/dev/null 2>&1") == 0:
        if os.path.exists(lcd_show_dir):
            break
    if attempt < 2:
        time.sleep(5)

if not os.path.exists(lcd_show_dir):
    print("   ✗ FEHLER: Repository konnte nicht geladen werden!")
    sys.exit(1)
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 3: WINDOWS-ZEILENENDEN FIXEN
# ============================================================================
print("3. Fixe Zeilenenden...")
for script in ["LCD35-show", "LCD35B-show", "LCD35B-show-V2", "LCD35C-show"]:
    os.system(f"dos2unix /home/pi/LCD-show/{script} >/dev/null 2>&1")
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 4: REBOOT AUS LCD35-SHOW ENTFERNEN
# ============================================================================
print("4. Entferne Reboot aus LCD35-show...")
lcd_script = "/home/pi/LCD-show/LCD35-show"
if os.path.exists(lcd_script):
    with open(lcd_script, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("sudo reboot", "# sudo reboot # ENTFERNT")
    content = content.replace(
        'echo "reboot now"', '# echo "reboot now" # ENTFERNT')
    with open(lcd_script, "w", encoding="utf-8") as f:
        f.write(content)
    os.system(f"chmod +x {lcd_script} >/dev/null 2>&1")
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 5: LCD-TREIBER INSTALLIEREN
# ============================================================================
print("5. Installiere LCD-Treiber...")
os.system("cd /home/pi/LCD-show && ./LCD35-show lite >/dev/null 2>&1")
time.sleep(3)
os.system("sync")
print("   ✓ Fertig")

# ============================================================================
# SCHRITT 6: CONFIG.TXT FÜR ROTATION ANPASSEN
# ============================================================================
print("6. Passe config.txt an...")
CONFIG = "/boot/config.txt"
os.system("mount /boot 2>/dev/null")
time.sleep(1)

try:
    with open(CONFIG, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Alte waveshare35-Zeilen entfernen
    new_lines = [line for line in lines if not line.startswith(
        "dtoverlay=waveshare35")]

    # Rotation-Zeile hinzufügen (wenn nicht vorhanden)
    rotate_line = "dtoverlay=waveshare35a:rotate=270\n"
    if rotate_line not in new_lines:
        new_lines.append(rotate_line)

    # Zurückschreiben
    temp_file = "/tmp/config.txt"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    os.system(f"cp {temp_file} {CONFIG} >/dev/null 2>&1")
    os.system("sync")
    print("   ✓ Fertig")
except Exception as e:
    print(f"   ✗ FEHLER: {e}")
    sys.exit(1)

# ============================================================================
# SCHRITT 7: DATEIEN NACH /HOME/PI/ KOPIEREN
# ============================================================================
print("7. Kopiere Programm-Dateien...")
current_dir = os.path.dirname(os.path.abspath(__file__))
files_to_copy = [
    "install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py",
    "the_programm_main.py",
    "the_programm_display_utils.py",
    "the_programm_display_berrybase_test.py"
]

for filename in files_to_copy:
    source = os.path.join(current_dir, filename)
    target = f"/home/pi/{filename}"
    # Prüfe zuerst, ob Datei bereits in /home/pi/ existiert (z.B. nach Deinstallation)
    if os.path.exists(target):
        os.system(f"chmod +x {target} >/dev/null 2>&1")
        print(f"   ✓ {filename} (bereits vorhanden)")
    elif os.path.exists(source):
        os.system(f"cp {source} {target} >/dev/null 2>&1")
        os.system(f"chmod +x {target} >/dev/null 2>&1")
        print(f"   ✓ {filename}")
    else:
        print(f"   ✗ {filename} nicht gefunden!")

# ============================================================================
# SCHRITT 8: SERVICE FÜR ZWEITEN INSTALLER ERSTELLEN
# ============================================================================
print("8. Erstelle Service für Teil 2...")
service_file = "/etc/systemd/system/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service"
service_content = """[Unit]
Description=LCD Display Installation Teil 2
After=multi-user.target
DefaultDependencies=no

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/pi/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py
StandardOutput=journal
StandardError=journal
RemainAfterExit=yes
TimeoutStartSec=300
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
"""

with open("/tmp/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service", "w") as f:
    f.write(service_content)

os.system(
    f"mv /tmp/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service {service_file} >/dev/null 2>&1")
os.system(f"chmod 644 {service_file} >/dev/null 2>&1")
os.system("systemctl daemon-reload >/dev/null 2>&1")
os.system("systemctl enable install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service >/dev/null 2>&1")
# getty@tty1 bereits jetzt maskieren, damit es beim nächsten Boot nicht startet
os.system("systemctl mask getty@tty1.service >/dev/null 2>&1")
print("   ✓ Fertig")

print("")
print("=== Installation Teil 1 abgeschlossen ===")
print("System wird jetzt neu gestartet...")
print("")
time.sleep(2)

# ============================================================================
# SCHRITT 9: REBOOT
# ============================================================================
os.system("reboot")
