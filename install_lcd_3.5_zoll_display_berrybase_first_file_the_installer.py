#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Installer Teil 1 - LCD Display Berrybase
# Installiert das 3.5" LCD Display auf dem Raspberry Pi
# Bereitet System vor, installiert Treiber und kopiert Dateien
# Run: sudo python3 install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py

import os
import sys
import time

print("=== LCD Display Installation - Teil 1 ===")
print("")

# ============================================================================
# SCHRITT 1: SYSTEM VORBEREITEN
# ============================================================================
print("1. Installiere benötigte Pakete...")
os.system("apt-get update -y >/dev/null 2>&1")
os.system("apt-get install -y git dos2unix xserver-xorg-input-evdev >/dev/null 2>&1")
print("   ✓ Fertig")

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
