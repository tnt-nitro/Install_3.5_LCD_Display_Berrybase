#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Testprogramm für LCD Display Berrybase
# Test program for LCD Display Berrybase
# Zeigt Systeminformationen und Status auf dem LCD Display an
# Displays system information and status on the LCD display
# Run: sudo python3 /home/pi/the_programm_display_berrybase_test.py

import time
import sys
import os
import platform
import subprocess
import shutil
from datetime import datetime
from the_programm_display_utils import Display, Colors


# Konfiguration / Configuration
DISPLAY_WIDTH = 60  # Breite des Displays in Zeichen / Display width in characters
# Rahmenbreite (rechts um 1 Zeichen nach links eingerückt) / Border width (indented 1 character to the left on the right)
BORDER_WIDTH = DISPLAY_WIDTH - 1
LINE_EMPTY_BEFORE_TITLE = 2  # Freie Zeile vor Titel
LINE_TITLE = 3  # Zeile für Titel
LINE_EMPTY_AFTER_STATUS = 4  # Freie Zeile nach Status
LINE_SEPARATOR_1 = 5  # Erste Trennlinie
LINE_INFO_START = 7  # Start der Info-Bereiche
LINE_INSTALL_TIME = 8  # Zeile für Installationszeit
LINE_COUNTER = 9  # Zeile für Counter-Anzeige
LINE_DATETIME = 10  # Zeile für Datum/Zeit-Anzeige
LINE_OS = 11  # Zeile für Betriebssystem
LINE_MEMORY = 12  # Zeile für Speicher
LINE_TEMP = 13  # Zeile für Temperatur
LINE_CPU = 14  # Zeile für CPU Last
LINE_FPS = 15  # Zeile für Framerate
LINE_SD_CARD = 16  # Zeile für SD-Karte
LINE_EMPTY_1 = 17  # Freie Zeile nach SD-Karte
LINE_SEPARATOR_2 = 18  # Zweite Trennlinie
LINE_EMPTY_2 = 19  # Freie Zeile vor Display
LINE_DISPLAY_INFO = 20  # Zeile für Display-Informationen
LINE_UPTIME = 21  # Zeile für Uptime
LINE_IP = 22  # Zeile für IP-Adresse
LINE_EMPTY_AFTER_IP = 23  # Freie Zeile nach IP-Adresse
LINE_SEPARATOR_3 = 24  # Dritte Trennlinie
LINE_EMPTY_AFTER_SEPARATOR_3 = 25  # Freie Zeile nach dritter Trennlinie
# Erste Zeile für Farb-Vierecke (R G Y B mit Buchstaben)
LINE_COLOR_BLOCKS_1 = 26
# Erste zusätzliche Zeile für R G Y B (ohne Buchstaben) / First additional line for R G Y B (without letters)
LINE_COLOR_BLOCKS_1_EXTRA_1 = 27
# Zweite zusätzliche Zeile für R G Y B (ohne Buchstaben) / Second additional line for R G Y B (without letters)
LINE_COLOR_BLOCKS_1_EXTRA_2 = 28
# Freie Zeile vor M C W K / Empty line before M C W K
LINE_EMPTY_BEFORE_COLOR_BLOCKS_2 = 29
# Zweite Zeile für Farb-Vierecke (M C W K mit Buchstaben) / Second line for color blocks (M C W K with letters)
LINE_COLOR_BLOCKS_2 = 30
# Erste zusätzliche Zeile für M C W K (ohne Buchstaben) / First additional line for M C W K (without letters)
LINE_COLOR_BLOCKS_2_EXTRA_1 = 31
# Zweite zusätzliche Zeile für M C W K (ohne Buchstaben) / Second additional line for M C W K (without letters)
LINE_COLOR_BLOCKS_2_EXTRA_2 = 32
# Freie Zeile nach M C W K / Empty line after M C W K
LINE_EMPTY_AFTER_COLOR_BLOCKS_2 = 33
# Dritte Zeile für Farb-Vierecke (Dk G1 G2 G3 Lt mit Buchstaben) / Third line for color blocks (Dk G1 G2 G3 Lt with letters)
LINE_COLOR_BLOCKS_3 = 34
# Erste zusätzliche Zeile für Dk G1 G2 G3 Lt (ohne Buchstaben) / First additional line for Dk G1 G2 G3 Lt (without letters)
LINE_COLOR_BLOCKS_3_EXTRA_1 = 35
# Zweite zusätzliche Zeile für Dk G1 G2 G3 Lt (ohne Buchstaben) / Second additional line for Dk G1 G2 G3 Lt (without letters)
LINE_COLOR_BLOCKS_3_EXTRA_2 = 36
# Freie Zeile nach Grauwerten / Empty line after grayscale values
LINE_EMPTY_AFTER_COLOR_BLOCKS_3 = 37
LINE_GRAYSCALE = 38  # Zeile für Graustufen 0-100% / Line for grayscale 0-100%
UPDATE_INTERVAL = 0.1  # Aktualisierungsintervall in Sekunden / Update interval in seconds


def format_counter(seconds):
    """
    Formatiert den Counter als HH:MM:SS.FFFFFF.
    Formats the counter as HH:MM:SS.FFFFFF.

    Args:
        seconds (float): Anzahl der Sekunden / Number of seconds

    Returns:
        str: Formatierter Zeitstring / Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:09.6f}"


def get_installation_time():
    """
    Liest die Startzeit der Installation und berechnet die Installationszeit.
    Beim ersten Aufruf wird die Installationszeit berechnet und gespeichert,
    danach wird immer die gespeicherte Zeit zurückgegeben.

    Returns:
        str: Formatierte Installationszeit oder "N/A" falls nicht verfügbar
    """
    try:
        start_time_file = "/home/pi/.install_start_time"
        final_time_file = "/home/pi/.install_final_time"

        # Wenn finale Zeit bereits gespeichert ist, diese zurückgeben
        if os.path.exists(final_time_file):
            with open(final_time_file, "r") as f:
                return f.read().strip()

        # Sonst berechnen und speichern
        if os.path.exists(start_time_file):
            with open(start_time_file, "r") as f:
                start_time = float(f.read().strip())
            installation_time = time.time() - start_time
            formatted_time = format_counter(installation_time)

            # Finale Zeit speichern
            try:
                with open(final_time_file, "w") as f:
                    f.write(formatted_time)
            except Exception:
                pass

            return formatted_time
    except Exception:
        pass
    return "N/A"


def format_bytes(bytes_value):
    """
    Formatiert Bytes in lesbare Einheiten.
    Formats bytes into readable units.

    Args:
        bytes_value (int): Anzahl der Bytes / Number of bytes

    Returns:
        str: Formatierter String (z.B. "512 MB") / Formatted string (e.g. "512 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} TB"


def get_os_info():
    """Gibt Betriebssystem-Informationen zurück. / Returns operating system information."""
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    return line.split('=')[1].strip().strip('"')
        return platform.system()
    except Exception:
        return platform.system()


def get_memory_info():
    """Gibt Speicher-Informationen zurück (verfügbar/gesamt). / Returns memory information (available/total)."""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = {}
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    meminfo[parts[0].rstrip(':')] = int(parts[1])

            # KB zu Bytes / KB to bytes
            total = meminfo.get('MemTotal', 0) * 1024
            available = meminfo.get('MemAvailable', 0) * 1024
            used = total - available

            if total > 0:
                percent = (used / total) * 100
                return f"{format_bytes(used)} / {format_bytes(total)} ({percent:.1f}%)"
            return "N/A"
    except Exception:
        return "N/A"


def get_temperature():
    """Gibt CPU-Temperatur zurück. / Returns CPU temperature."""
    try:
        # Raspberry Pi Temperatur / Raspberry Pi temperature
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read().strip()) / 1000.0
            return f"{temp:.1f}°C"
    except Exception:
        try:
            # Alternative Methode / Alternative method
            result = subprocess.run(['vcgencmd', 'measure_temp'],
                                    capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                temp = result.stdout.split('=')[1].split("'")[0]
                return f"{temp}°C"
        except Exception:
            pass
    return "N/A"


def get_cpu_load():
    """Gibt CPU-Last zurück (1-Minuten-Durchschnitt). / Returns CPU load (1-minute average)."""
    try:
        with open('/proc/loadavg', 'r') as f:
            load = f.read().split()[0]
            return f"{load}"
    except Exception:
        return "N/A"


def get_uptime():
    """Gibt System-Uptime zurück. / Returns system uptime."""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.read().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
    except Exception:
        return "N/A"


def get_ip_address():
    """Gibt die IP-Adresse zurück. / Returns the IP address."""
    try:
        result = subprocess.run(['hostname', '-I'],
                                capture_output=True, text=True, timeout=1)
        if result.returncode == 0:
            ip = result.stdout.strip().split()[0]
            return ip
    except Exception:
        pass
    return "N/A"


def get_display_model():
    """Gibt das Display-Modell zurück (kompakt). / Returns the display model (compact)."""
    try:
        # Prüfe config.txt für dtoverlay / Check config.txt for dtoverlay
        config_files = ['/boot/config.txt', '/boot/firmware/config.txt']
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    for line in f:
                        line_lower = line.lower().strip()
                        if 'dtoverlay=waveshare35' in line_lower:
                            # Extrahiere Modell aus dtoverlay (kompakt) / Extract model from dtoverlay (compact)
                            if 'waveshare35a' in line_lower:
                                return "3.5\" LCD-A"
                            elif 'waveshare35b' in line_lower:
                                return "3.5\" LCD-B"
                            elif 'waveshare35c' in line_lower:
                                return "3.5\" LCD-C"
                            else:
                                return "3.5\" LCD"
    except Exception:
        pass

    return "3.5\" LCD"


def get_display_rotation():
    """Gibt die Display-Rotation zurück. / Returns the display rotation."""
    try:
        config_files = ['/boot/config.txt', '/boot/firmware/config.txt']
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    for line in f:
                        if 'rotate=' in line.lower():
                            # Extrahiere Rotationswert / Extract rotation value
                            if 'rotate=90' in line.lower():
                                return "90°"
                            elif 'rotate=180' in line.lower():
                                return "180°"
                            elif 'rotate=270' in line.lower():
                                return "270°"
                            elif 'rotate=0' in line.lower():
                                return "0°"
    except Exception:
        pass
    return "N/A"


def get_display_colors():
    """Gibt die Farbtiefe zurück. / Returns the color depth."""
    try:
        # Prüfe Framebuffer Farbtiefe / Check framebuffer color depth
        fb_bits = '/sys/class/graphics/fb0/bits_per_pixel'
        if os.path.exists(fb_bits):
            with open(fb_bits, 'r') as f:
                bits = f.read().strip()
                if bits:
                    return f"{bits} bit"
    except Exception:
        pass

    # Standard für 3.5" LCD / Default for 3.5" LCD
    return "16 bit (RGB565)"


def get_terminal_size():
    """Gibt die Terminal-Größe zurück (Zeilen x Spalten). / Returns terminal size (rows x columns)."""
    try:
        # Methode 1: stty size / Method 1: stty size
        result = subprocess.run(['stty', 'size'],
                                capture_output=True, text=True, timeout=1)
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) >= 2:
                rows = int(parts[0])
                cols = int(parts[1])
                return f"{rows}x{cols}"
    except Exception:
        pass

    try:
        # Methode 2: tput / Method 2: tput
        result_rows = subprocess.run(['tput', 'lines'],
                                     capture_output=True, text=True, timeout=1)
        result_cols = subprocess.run(['tput', 'cols'],
                                     capture_output=True, text=True, timeout=1)
        if result_rows.returncode == 0 and result_cols.returncode == 0:
            rows = result_rows.stdout.strip()
            cols = result_cols.stdout.strip()
            if rows.isdigit() and cols.isdigit():
                return f"{rows}x{cols}"
    except Exception:
        pass

    try:
        # Methode 3: os.get_terminal_size (Python) / Method 3: os.get_terminal_size (Python)
        size = shutil.get_terminal_size()
        return f"{size.lines}x{size.columns}"
    except Exception:
        pass

    # Fallback: Standard für 3.5" LCD mit typischer Terminal-Schrift
    # Fallback: Default for 3.5" LCD with typical terminal font
    # 480x320 Pixel / ~8x16 Pixel pro Zeichen ≈ 60x20 Zeichen
    # 480x320 pixels / ~8x16 pixels per character ≈ 60x20 characters
    return "20x60"


def get_display_resolution():
    """Gibt die Display-Auflösung zurück. / Returns the display resolution."""
    try:
        # Prüfe Framebuffer / Check framebuffer
        fb_info = '/sys/class/graphics/fb0/virtual_size'
        if os.path.exists(fb_info):
            with open(fb_info, 'r') as f:
                size = f.read().strip()
                if ',' in size:
                    width, height = size.split(',')
                    return f"{width}x{height}"
    except Exception:
        pass

    try:
        # Prüfe über fbset / Check via fbset
        result = subprocess.run(['fbset', '-s'],
                                capture_output=True, text=True, timeout=1)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'geometry' in line.lower():
                    parts = line.split()
                    if len(parts) >= 3:
                        return f"{parts[1]}x{parts[2]}"
    except Exception:
        pass

    # Standard für 3.5" LCD / Default for 3.5" LCD
    return "480x320"


def get_display_info():
    """Gibt eine Zusammenfassung der Display-Informationen zurück (kompakt). / Returns a summary of display information (compact)."""
    model = get_display_model()
    resolution = get_display_resolution()
    rotation = get_display_rotation()
    terminal_size = get_terminal_size()

    # Kompakte Darstellung: Modell Res Terminal-Größe
    # Compact representation: Model Res Terminal size
    info = f"{model} {resolution} {terminal_size}"
    if rotation != "N/A" and rotation != "0°":
        info += f" R{rotation.replace('°', '')}"
    return info


def get_disk_usage():
    """Gibt SD-Karten-Speicherplatz-Informationen zurück (verwendet/gesamt). / Returns SD card storage information (used/total)."""
    try:
        # Verwende statvfs für bessere Kompatibilität / Use statvfs for better compatibility
        stat = os.statvfs('/')

        # Berechne Speicherplatz / Calculate storage space
        total_bytes = stat.f_frsize * stat.f_blocks
        free_bytes = stat.f_frsize * stat.f_bavail
        used_bytes = total_bytes - free_bytes

        if total_bytes > 0:
            percent = (used_bytes / total_bytes) * 100
            return f"{format_bytes(used_bytes)} / {format_bytes(total_bytes)} ({percent:.1f}%)"
        return "N/A"
    except Exception:
        try:
            # Alternative: df -h verwenden / Alternative: use df -h
            result = subprocess.run(['df', '-h', '/'],
                                    capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        used = parts[2]
                        total = parts[1]
                        percent = parts[4]
                        return f"{used} / {total} ({percent})"
        except Exception:
            pass
    return "N/A"


def center_text(text, width=BORDER_WIDTH):
    """
    Zentriert einen Text innerhalb der angegebenen Breite (ohne Rahmen).
    Centers text within the specified width (without border).

    Args:
        text (str): Der zu zentrierende Text / Text to center
        width (int): Die Breite des Rahmens (ohne Rahmen) / Border width (without border)

    Returns:
        str: Zentrierter Text / Centered text
    """
    # Berücksichtige den Rahmen: Breite minus 2 für die Rahmenzeichen, minus 1 für das Leerzeichen nach dem linken Rahmenzeichen
    # Consider border: width minus 2 for border characters, minus 1 for space after left border character
    inner_width = width - 3
    return text.center(inner_width)


def update_line_with_border(display, row, text):
    """
    Aktualisiert eine Zeile mit Text, während der Rahmen erhalten bleibt.
    Updates a line with text while preserving the border.

    Args:
        display (Display): Display-Objekt / Display object
        row (int): Zeilennummer (1-basiert) / Row number (1-based)
        text (str): Text der angezeigt werden soll / Text to be displayed
    """
    # Bestimme die Rahmenbreite basierend auf der Zeilennummer
    # Determine border width based on row number
    # Für Zeilen Laufzeit bis SD-Karte: Rahmen rechts um 14 Zeichen nach links eingerückt
    # For rows runtime to SD card: border indented 14 characters to the left on the right
    # Für Zeile Display: Rahmen rechts um 4 Zeichen nach links eingerückt
    # For display line: border indented 4 characters to the left on the right
    # Für Zeile Uptime: Rahmen rechts um 10 Zeichen nach links eingerückt
    # For uptime line: border indented 10 characters to the left on the right
    # Für Zeile IP-Adresse: Rahmen rechts um 4 Zeichen nach links eingerückt
    # For IP address line: border indented 4 characters to the left on the right
    if LINE_COUNTER <= row <= LINE_SD_CARD:
        border_width = BORDER_WIDTH - 0  # 14 Zeichen nach links eingerückt
    elif row == LINE_DISPLAY_INFO:
        border_width = BORDER_WIDTH - 0  # 4 Zeichen nach links eingerückt
    elif row == LINE_UPTIME:
        border_width = BORDER_WIDTH - 0  # 10 Zeichen nach links eingerückt
    elif row == LINE_IP:
        border_width = BORDER_WIDTH - 0  # 4 Zeichen nach links eingerückt
    else:
        border_width = BORDER_WIDTH

    display.update_line_with_border(row, text, border_width, '#')


def print_extended_border_lines(display):
    """
    Zeichnet den breiteren Rahmen für spezielle Zeilenbereiche neu.
    Redraws the wider border for special line areas.

    Args:
        display (Display): Display-Objekt / Display object
    """
    try:
        # Rahmenbreiten für verschiedene Bereiche (nach links eingerückt)
        # Border widths for different areas (indented to the left)
        # Für Laufzeit bis SD-Karte (14 Zeichen eingerückt)
        # For runtime to SD card (indented 14 characters)
        reduced_width_counter = BORDER_WIDTH - 14
        # Für Uptime (10 Zeichen eingerückt)
        # For uptime (indented 10 characters)
        reduced_width_uptime = BORDER_WIDTH - 10
        # Für Display und IP-Adresse (4 Zeichen eingerückt)
        # For display and IP address (indented 4 characters)
        reduced_width_display_ip = BORDER_WIDTH - 4
        char = '#'

        # Zeilen Laufzeit bis SD-Karte / Rows runtime to SD card
        for row in range(LINE_COUNTER, LINE_SD_CARD + 1):
            side_border = char + ' ' * (reduced_width_counter - 2) + char
            display.update_line(row, side_border)

        # Zeile Display (4 Zeichen eingerückt) / Display line (indented 4 characters)
        side_border = char + ' ' * (reduced_width_display_ip - 2) + char
        display.update_line(LINE_DISPLAY_INFO, side_border)

        # Zeile Uptime (10 Zeichen eingerückt) / Uptime line (indented 10 characters)
        side_border = char + ' ' * (reduced_width_uptime - 2) + char
        display.update_line(LINE_UPTIME, side_border)

        # Zeile IP-Adresse (4 Zeichen eingerückt) / IP address line (indented 4 characters)
        side_border = char + ' ' * (reduced_width_display_ip - 2) + char
        display.update_line(LINE_IP, side_border)
    except Exception:
        pass


def print_separator(display, line, char='-'):
    """
    Gibt eine Trennlinie aus (ohne Leerzeichen nach dem linken Rahmenzeichen).
    Outputs a separator line (without space after left border character).

    Args:
        display (Display): Display-Objekt / Display object
        line (int): Zeilennummer / Row number
        char (str): Zeichen für die Trennlinie / Character for separator line
    """
    try:
        # Trennlinie ohne Leerzeichen: Breite minus 2 für die Rahmenzeichen
        # Separator line without spaces: width minus 2 for border characters
        inner_width = BORDER_WIDTH - 2
        separator = '#' + char * inner_width + '#'
        display.update_line(line, separator)
    except Exception:
        pass


def print_header(display):
    """
    Gibt den Header mit Titel und Status aus.
    Outputs the header with title and status.

    Args:
        display (Display): Display-Objekt / Display object
    """
    try:
        # Freie Zeile vor Titel (Rahmen wird automatisch gezeichnet)
        # Empty line before title (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_BEFORE_TITLE, "")

        # Titel und Status in einer Zeile zentriert
        title_status = center_text("LCD Display System Status: Aktiv / Active")
        update_line_with_border(display, LINE_TITLE, title_status)

        # Freie Zeile nach Titel/Status (Rahmen wird automatisch gezeichnet)
        update_line_with_border(display, LINE_EMPTY_AFTER_STATUS, "")

        # Trennlinie / Separator line
        print_separator(display, LINE_SEPARATOR_1)
    except Exception:
        pass


def print_color_blocks(display):
    """
    Gibt gefüllte Vierecke in verschiedenen Farben über 3 Zeilen aus.
    Outputs filled rectangles in various colors over 3 lines.

    Args:
        display (Display): Display-Objekt / Display object
    """
    try:
        # Zeile 1: Grundfarben / Line 1: Basic colors
        color_blocks_1 = [
            ("R", Colors.BG_RED),
            ("G", Colors.BG_GREEN),
            ("Y", Colors.BG_YELLOW),
            ("B", Colors.BG_BLUE),
            ("O", Colors.BG_ORANGE),  # Orange
            ("V", Colors.BG_VIOLET),  # Violett (knallig) / Violet (bright)
        ]

        # Zeile 2: Erweiterte Farben / Line 2: Extended colors
        color_blocks_2 = [
            ("M", Colors.BG_MAGENTA),
            ("C", Colors.BG_CYAN),
            ("W", Colors.BG_WHITE),
            ("K", Colors.BG_BLACK),
            ("P", Colors.BG_PINK),   # Pink
            ("L", Colors.BG_LIME),   # Lime (Gelbgrün) / Lime (yellow-green)
        ]

        # Zeile 3: Grauwerte / Line 3: Grayscale values
        color_blocks_3 = [
            ("Dk", Colors.BG_GRAY_DARK),
            ("G1", Colors.BG_GRAY_1),
            ("G2", Colors.BG_GRAY_2),
            ("G3", Colors.BG_GRAY_3),
            ("Lt", Colors.BG_GRAY_LIGHT),
            # Absolutes Weiß (6. Graukarte) / Absolute white (6th gray card)
            ("Wt", Colors.BG_WHITE),
        ]

        block_width = 6  # Breite jedes Vierecks / Width of each rectangle

        # Zeile 1 ausgeben (mit Buchstaben) - Leerzeichen vor Buchstaben für Ausrichtung mit Graukarten
        # Output line 1 (with letters) - spaces before letters for alignment with gray cards
        color_line_1 = ""
        for label, bg_color in color_blocks_1:
            block = display.print_colored_block(
                # Leerzeichen vor Buchstaben / Space before letter
                block_width, bg_color, " " + label)
            color_line_1 += block + " "  # Abstand zwischen Vierecken / Space between rectangles
        update_line_with_border(display, LINE_COLOR_BLOCKS_1, color_line_1)

        # Zwei zusätzliche Zeilen für R G Y B O V ohne Buchstaben
        # Two additional lines for R G Y B O V without letters
        color_line_1_extra_1 = ""
        for label, bg_color in color_blocks_1:
            block = display.print_colored_block(
                block_width, bg_color, "")  # Ohne Label / Without label
            # Zwei Leerzeichen vor Farbe für Ausrichtung mit Zeile mit Buchstaben
            # Two spaces before color for alignment with line with letters
            color_line_1_extra_1 += "  " + block + " "
        update_line_with_border(
            display, LINE_COLOR_BLOCKS_1_EXTRA_1, color_line_1_extra_1)

        color_line_1_extra_2 = ""
        for label, bg_color in color_blocks_1:
            block = display.print_colored_block(
                block_width, bg_color, "")  # Ohne Label / Without label
            # Zwei Leerzeichen vor Farbe für Ausrichtung mit Zeile mit Buchstaben
            # Two spaces before color for alignment with line with letters
            color_line_1_extra_2 += "  " + block + " "
        update_line_with_border(
            display, LINE_COLOR_BLOCKS_1_EXTRA_2, color_line_1_extra_2)

        # Freie Zeile vor M C W K (Rahmen wird automatisch gezeichnet)
        # Empty line before M C W K (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_BEFORE_COLOR_BLOCKS_2, "")

        # Zeile 2 ausgeben (mit Buchstaben) - Leerzeichen vor Buchstaben für Ausrichtung mit Graukarten
        # Output line 2 (with letters) - spaces before letters for alignment with gray cards
        color_line_2 = ""
        for label, bg_color in color_blocks_2:
            block = display.print_colored_block(
                # Leerzeichen vor Buchstaben / Space before letter
                block_width, bg_color, " " + label)
            color_line_2 += block + " "  # Abstand zwischen Vierecken / Space between rectangles
        update_line_with_border(display, LINE_COLOR_BLOCKS_2, color_line_2)

        # Zwei zusätzliche Zeilen für M C W K P L ohne Buchstaben
        # Two additional lines for M C W K P L without letters
        color_line_2_extra_1 = ""
        for label, bg_color in color_blocks_2:
            block = display.print_colored_block(
                block_width, bg_color, "")  # Ohne Label / Without label
            # Zwei Leerzeichen vor Farbe für Ausrichtung mit Zeile mit Buchstaben
            # Two spaces before color for alignment with line with letters
            color_line_2_extra_1 += "  " + block + " "
        update_line_with_border(
            display, LINE_COLOR_BLOCKS_2_EXTRA_1, color_line_2_extra_1)

        color_line_2_extra_2 = ""
        for label, bg_color in color_blocks_2:
            block = display.print_colored_block(
                block_width, bg_color, "")  # Ohne Label / Without label
            # Zwei Leerzeichen vor Farbe für Ausrichtung mit Zeile mit Buchstaben
            # Two spaces before color for alignment with line with letters
            color_line_2_extra_2 += "  " + block + " "
        update_line_with_border(
            display, LINE_COLOR_BLOCKS_2_EXTRA_2, color_line_2_extra_2)

        # Freie Zeile nach M C W K (Rahmen wird automatisch gezeichnet)
        # Empty line after M C W K (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_AFTER_COLOR_BLOCKS_2, "")

        # Zeile 3 ausgeben (Grauwerte mit Buchstaben)
        # Output line 3 (grayscale values with letters)
        color_line_3 = ""
        for label, bg_color in color_blocks_3:
            block = display.print_colored_block(block_width, bg_color, label)
            color_line_3 += block + " "  # Abstand zwischen Vierecken / Space between rectangles
        update_line_with_border(display, LINE_COLOR_BLOCKS_3, color_line_3)

        # Zwei zusätzliche Zeilen für Dk G1 G2 G3 Lt Wt ohne Buchstaben
        # Two additional lines for Dk G1 G2 G3 Lt Wt without letters
        color_line_3_extra_1 = ""
        for label, bg_color in color_blocks_3:
            block = display.print_colored_block(
                block_width, bg_color, "")  # Ohne Label / Without label
            # Drei Leerzeichen vor Farbe für Ausrichtung mit Zeile mit Buchstaben (alle Labels haben 2 Buchstaben)
            # Three spaces before color for alignment with line with letters (all labels have 2 letters)
            color_line_3_extra_1 += "  " + block + " "
        update_line_with_border(
            display, LINE_COLOR_BLOCKS_3_EXTRA_1, color_line_3_extra_1)

        color_line_3_extra_2 = ""
        for label, bg_color in color_blocks_3:
            block = display.print_colored_block(
                block_width, bg_color, "")  # Ohne Label / Without label
            # Drei Leerzeichen vor Farbe für Ausrichtung mit Zeile mit Buchstaben (alle Labels haben 2 Buchstaben)
            # Three spaces before color for alignment with line with letters (all labels have 2 letters)
            color_line_3_extra_2 += "  " + block + " "
        update_line_with_border(
            display, LINE_COLOR_BLOCKS_3_EXTRA_2, color_line_3_extra_2)

        # Freie Zeile nach Grauwerten (Rahmen wird automatisch gezeichnet)
        # Empty line after grayscale values (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_AFTER_COLOR_BLOCKS_3, "")
    except Exception:
        pass


def print_grayscale_line(display):
    """
    Gibt eine Zeile mit Graustufen von 0% bis 100% in 5% Schritten aus.
    Outputs a line with grayscale from 0% to 100% in 5% steps.

    Args:
        display (Display): Display-Objekt / Display object
    """
    try:
        # Berechne Anzahl der Blöcke (0%, 5%, 10%, ..., 100% = 21 Blöcke)
        # Calculate number of blocks (0%, 5%, 10%, ..., 100% = 21 blocks)
        num_blocks = 21
        # Berücksichtige den Rahmen: Breite minus 2 für die Rahmenzeichen, minus 1 für das Leerzeichen nach dem linken Rahmenzeichen, minus 10 für Labels
        # Consider border: width minus 2 for border characters, minus 1 for space after left border character, minus 10 for labels
        # Etwas Platz für Labels lassen / Leave some space for labels
        total_width = BORDER_WIDTH - 3 - 10
        # Mindestens 2 Zeichen pro Block / At least 2 characters per block
        block_width = max(2, total_width // num_blocks)

        grayscale_line = ""

        # Erstelle Blöcke von 0% bis 100% in 5% Schritten
        # Create blocks from 0% to 100% in 5% steps
        for i in range(num_blocks):
            percent = i * 5  # 0, 5, 10, ..., 100
            bg_color = display.get_grayscale_color(percent)

            # Verwende "*" als Füllung / Use "*" as fill
            block = '*' * block_width
            grayscale_line += f"{bg_color}{block}{Colors.RESET}"

        update_line_with_border(display, LINE_GRAYSCALE, grayscale_line)
    except Exception:
        pass


def print_static_info(display):
    """
    Gibt statische Informationen aus.
    Outputs static information.

    Args:
        display (Display): Display-Objekt / Display object
    """
    try:
        # Info-Bereich Titel / Info section title
        info_title = "System-Informationen / System Information"
        update_line_with_border(display, LINE_INFO_START, info_title)

        # Labels für dynamische Daten
        update_line_with_border(
            display, LINE_INSTALL_TIME, "Installationszeit / Install Time:")
        update_line_with_border(display, LINE_COUNTER, "Laufzeit / Runtime:")
        update_line_with_border(display, LINE_DATETIME,
                                "Aktuelle Zeit / Time:")
        update_line_with_border(display, LINE_OS, "Betriebssystem / OS:")
        update_line_with_border(display, LINE_MEMORY, "Speicher / Memory:")
        update_line_with_border(
            display, LINE_TEMP, "Temperatur / Temperature:")
        update_line_with_border(display, LINE_CPU, "CPU Last / CPU Load:")
        update_line_with_border(display, LINE_FPS, "Framerate:")
        update_line_with_border(display, LINE_SD_CARD, "SD-Karte / SD Card:")

        # Freie Zeile nach SD-Karte (Rahmen wird automatisch gezeichnet)
        # Empty line after SD card (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_1, "")

        # Zweite Trennlinie / Second separator line
        print_separator(display, LINE_SEPARATOR_2)

        # Freie Zeile vor Display (Rahmen wird automatisch gezeichnet)
        # Empty line before display (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_2, "")

        # Weitere Labels / Additional labels
        update_line_with_border(display, LINE_DISPLAY_INFO, "Display:")
        update_line_with_border(display, LINE_UPTIME, "Uptime:")
        update_line_with_border(display, LINE_IP, "IP-Adresse / IP Address:")

        # Freie Zeile nach IP-Adresse (Rahmen wird automatisch gezeichnet)
        # Empty line after IP address (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_AFTER_IP, "")

        # Dritte Trennlinie / Third separator line
        print_separator(display, LINE_SEPARATOR_3)

        # Freie Zeile nach dritter Trennlinie (Rahmen wird automatisch gezeichnet)
        # Empty line after third separator (border is drawn automatically)
        update_line_with_border(display, LINE_EMPTY_AFTER_SEPARATOR_3, "")

        # Farb-Vierecke / Color blocks
        print_color_blocks(display)

        # Graustufen-Zeile / Grayscale line
        print_grayscale_line(display)

        sys.stdout.flush()
    except Exception:
        pass


def main():
    """Hauptfunktion des Testprogramms. / Main function of the test program."""
    start_time = time.time()
    display = None
    frame_count = 0
    fps_start_time = time.time()
    os_info = get_os_info()  # Statisch, nur einmal laden / Static, load only once
    # Statisch, nur einmal laden / Static, load only once
    display_info = get_display_info()

    try:
        # Display initialisieren (flackerfrei) - max_rows erhöht für zusätzliche Zeilen
        # Initialize display (flicker-free) - max_rows increased for additional lines
        display = Display(max_rows=40)

        # Screen komplett löschen um alle Boot-Meldungen zu entfernen
        # Clear screen completely to remove all boot messages
        display.clear_full_screen()
        time.sleep(0.2)

        # Display initialisieren / Initialize display
        display.init()
        time.sleep(0.3)

        # Rahmen um das Display zeichnen (rechts um 1 Zeichen nach links eingerückt)
        # Draw border around display (indented 1 character to the left on the right)
        display.print_border(BORDER_WIDTH, '#')

        # Breiteren Rahmen für spezielle Zeilenbereiche zeichnen
        # Draw wider border for special line areas
        print_extended_border_lines(display)

        # Statische Inhalte einmalig ausgeben
        # Output static content once
        print_header(display)
        print_static_info(display)

        # Hauptschleife für dynamische Updates
        # Main loop for dynamic updates
        while True:
            try:
                loop_start = time.time()

                # Installationszeit aktualisieren (flackerfrei)
                install_time_str = get_installation_time()
                install_time_text = f"Installationszeit / Install Time: {Colors.BOLD}{install_time_str}{Colors.RESET}"
                update_line_with_border(
                    display, LINE_INSTALL_TIME, install_time_text)

                # Counter-Zeile aktualisieren (flackerfrei)
                # Update counter line (flicker-free)
                elapsed = time.time() - start_time
                counter_str = format_counter(elapsed)
                counter_text = f"Laufzeit / Runtime: {Colors.BOLD}{counter_str}{Colors.RESET}"
                update_line_with_border(display, LINE_COUNTER, counter_text)

                # Datum/Zeit-Zeile aktualisieren (flackerfrei)
                # Update date/time line (flicker-free)
                now = datetime.now()
                datetime_str = now.strftime("%Y-%m-%d  %H:%M:%S")
                datetime_text = f"Aktuelle Zeit / Time: {Colors.BOLD}{datetime_str}{Colors.RESET}"
                update_line_with_border(display, LINE_DATETIME, datetime_text)

                # Betriebssystem (statisch, aber für Konsistenz)
                # Operating system (static, but for consistency)
                os_text = f"Betriebssystem / OS: {Colors.BOLD}{os_info}{Colors.RESET}"
                update_line_with_border(display, LINE_OS, os_text)

                # Speicher-Informationen / Memory information
                memory_info = get_memory_info()
                memory_text = f"Speicher / Memory: {Colors.BOLD}{memory_info}{Colors.RESET}"
                update_line_with_border(display, LINE_MEMORY, memory_text)

                # Temperatur / Temperature
                temp_info = get_temperature()
                temp_text = f"Temperatur / Temperature: {Colors.BOLD}{temp_info}{Colors.RESET}"
                update_line_with_border(display, LINE_TEMP, temp_text)

                # CPU Last / CPU load
                cpu_load = get_cpu_load()
                cpu_text = f"CPU Last / CPU Load: {Colors.BOLD}{cpu_load}{Colors.RESET}"
                update_line_with_border(display, LINE_CPU, cpu_text)

                # Framerate berechnen / Calculate framerate
                frame_count += 1
                fps_elapsed = time.time() - fps_start_time
                if fps_elapsed >= 1.0:  # Alle 1 Sekunde aktualisieren / Update every 1 second
                    fps = frame_count / fps_elapsed
                    frame_count = 0
                    fps_start_time = time.time()
                else:
                    fps = frame_count / fps_elapsed if fps_elapsed > 0 else 0
                fps_text = f"Framerate: {Colors.BOLD}{fps:.1f} FPS{Colors.RESET}"
                update_line_with_border(display, LINE_FPS, fps_text)

                # SD-Karte Speicherplatz / SD card storage space
                disk_info = get_disk_usage()
                disk_text = f"SD-Karte / SD Card: {Colors.BOLD}{disk_info}{Colors.RESET}"
                update_line_with_border(display, LINE_SD_CARD, disk_text)

                # Uptime
                uptime_info = get_uptime()
                uptime_text = f"Uptime: {Colors.BOLD}{uptime_info}{Colors.RESET}"
                update_line_with_border(display, LINE_UPTIME, uptime_text)

                # Display-Informationen (statisch, aber für Konsistenz)
                # Display information (static, but for consistency)
                display_text = f"Display: {Colors.BOLD}{display_info}{Colors.RESET}"
                update_line_with_border(
                    display, LINE_DISPLAY_INFO, display_text)

                # IP-Adresse / IP address
                ip_info = get_ip_address()
                ip_text = f"IP-Adresse / IP Address: {Colors.BOLD}{ip_info}{Colors.RESET}"
                update_line_with_border(display, LINE_IP, ip_text)

                # Pause für flüssige, aber nicht zu schnelle Aktualisierung
                # Pause for smooth but not too fast updates
                time.sleep(UPDATE_INTERVAL)

            except KeyboardInterrupt:
                raise  # Weiterleiten an äußeren Handler / Forward to outer handler
            except Exception:
                # Bei Fehlern in der Update-Schleife kurz warten und weitermachen
                # On errors in update loop, wait briefly and continue
                time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        if display:
            display.cleanup()
        print(f"\n{Colors.RESET}Programm beendet. / Program terminated.")
    except Exception as e:
        # Fehlerbehandlung für unerwartete Fehler
        # Error handling for unexpected errors
        if display:
            display.cleanup()
        print(f"\n{Colors.RED}Fehler: {e} / Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
