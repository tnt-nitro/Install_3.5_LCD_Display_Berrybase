#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Display-Utilities-Modul für LCD Display Berrybase
# Display utilities module for LCD Display Berrybase
# Wiederverwendbares Modul für flackerfreie Display-Ausgabe
# Reusable module for flicker-free display output

import re


def strip_ansi_codes(text):
    """
    Entfernt ANSI-Escape-Codes aus einem String, um die tatsächliche Textlänge zu berechnen.
    Removes ANSI escape codes from a string to calculate the actual text length.

    Args:
        text (str): Text mit möglichen ANSI-Codes / Text with possible ANSI codes

    Returns:
        str: Text ohne ANSI-Codes / Text without ANSI codes
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class Colors:
    # Vordergrundfarben / Foreground colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    PURPLE = '\033[35m'  # Lila/Purple
    WHITE = '\033[97m'
    # Dunkelgrau (schwarz ist schwer sichtbar) / Dark gray (black is hard to see)
    BLACK = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CLEAR = '\033[2J'  # Bildschirm löschen / Clear screen
    HOME = '\033[H'    # Cursor nach oben links / Cursor to top left
    ERASE_LINE = '\033[K'  # Zeile bis zum Ende löschen / Erase line to end
    HIDE_CURSOR = '\033[?25l'  # Cursor ausblenden / Hide cursor
    SHOW_CURSOR = '\033[?25h'  # Cursor einblenden / Show cursor

    # Hintergrundfarben (für gefüllte Vierecke) / Background colors (for filled rectangles)
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Zusätzliche 8-bit Farben / Additional 8-bit colors
    BG_ORANGE = '\033[48;5;208m'  # Orange
    BG_BROWN = '\033[48;5;130m'   # Braun / Brown
    BG_PINK = '\033[48;5;218m'    # Pink
    BG_LIME = '\033[48;5;154m'    # Lime (Gelbgrün) / Lime (yellow-green)
    BG_VIOLET = '\033[48;5;129m'  # Violett (knallig) / Violet (bright)

    # Grauwerte (8-bit Farben) / Grayscale values (8-bit colors)
    BG_GRAY_DARK = '\033[48;5;232m'    # Sehr dunkel / Very dark
    BG_GRAY_1 = '\033[48;5;238m'       # Dunkelgrau 1 / Dark gray 1
    BG_GRAY_2 = '\033[48;5;244m'       # Mittelgrau / Medium gray
    BG_GRAY_3 = '\033[48;5;250m'       # Hellgrau / Light gray
    BG_GRAY_LIGHT = '\033[48;5;255m'   # Sehr hell / Very light


class Display:
    """Klasse für flackerfreie Display-Ausgabe / Class for flicker-free display output"""

    def __init__(self, max_rows=30):
        """
        Initialisiert das Display-Objekt.
        Initializes the display object.

        Args:
            max_rows (int): Maximale Anzahl der Zeilen auf dem Display (Standard: 30) / Maximum number of rows on the display (default: 30)
        """
        self.initialized = False
        self.max_rows = max_rows

    def init(self):
        """Display initialisieren (Bildschirm löschen, Cursor ausblenden) / Initialize display (clear screen, hide cursor)"""
        try:
            print(Colors.CLEAR + Colors.HOME +
                  Colors.HIDE_CURSOR, end='', flush=True)
            self.initialized = True
        except Exception as e:
            # Fehler beim Initialisieren ignorieren, um Robustheit zu gewährleisten
            # Ignore initialization errors to ensure robustness
            pass

    def clear_screen(self):
        """Kompletten Screen löschen (kann mehrfach aufgerufen werden) / Clear entire screen (can be called multiple times)"""
        try:
            print(Colors.CLEAR + Colors.HOME, end='', flush=True)
        except Exception:
            pass

    def clear_full_screen(self):
        """Löscht den gesamten Bildschirm und füllt ihn mit Leerzeichen. / Clears the entire screen and fills it with spaces."""
        try:
            print(Colors.CLEAR + Colors.HOME, end='', flush=True)
            # Fülle den gesamten Bildschirm mit Leerzeichen, um sicherzustellen, dass alles weg ist
            # Fill the entire screen with spaces to ensure everything is cleared
            for i in range(1, self.max_rows + 1):
                self.update_line(i, "")
            # Cursor wieder nach oben links / Cursor back to top left
            print(Colors.HOME, end='', flush=True)
        except Exception:
            # Fehler beim Löschen ignorieren / Ignore errors when clearing
            pass

    def move_cursor(self, row, col):
        """
        Cursor zu bestimmter Position bewegen.
        Move cursor to specified position.

        Args:
            row (int): Zeilennummer (1-basiert) / Row number (1-based)
            col (int): Spaltennummer (1-basiert) / Column number (1-based)
        """
        try:
            print(f'\033[{row};{col}H', end='', flush=True)
        except Exception:
            pass

    def update_line(self, row, text):
        """
        Eine Zeile komplett überschreiben (flackerfrei).
        Completely overwrite a line (flicker-free).

        Args:
            row (int): Zeilennummer (1-basiert) / Row number (1-based)
            text (str): Text der angezeigt werden soll / Text to be displayed
        """
        try:
            self.move_cursor(row, 1)
            print(f"{text}{Colors.ERASE_LINE}", end='', flush=True)
        except Exception:
            pass

    def cleanup(self):
        """Display aufräumen (Cursor wieder einblenden) / Cleanup display (show cursor again)"""
        try:
            print(Colors.SHOW_CURSOR, end='', flush=True)
            self.initialized = False
        except Exception:
            pass

    def print_colored_block(self, width, bg_color, label=""):
        """
        Gibt ein gefülltes Viereck in einer bestimmten Farbe aus.
        Outputs a filled rectangle in a specific color.

        Args:
            width (int): Breite des Vierecks in Zeichen / Width of rectangle in characters
            bg_color (str): ANSI-Hintergrundfarbe / ANSI background color
            label (str): Optionales Label vor dem Viereck / Optional label before rectangle

        Returns:
            str: Formatierter String mit gefülltem Viereck / Formatted string with filled rectangle
        """
        try:
            block = ' ' * width  # Leerzeichen als Füllung
            if label:
                return f"{label}{bg_color}{block}{Colors.RESET}"
            else:
                return f"{bg_color}{block}{Colors.RESET}"
        except Exception:
            return ""

    def get_grayscale_color(self, percent):
        """
        Gibt eine Graustufen-Hintergrundfarbe für einen Prozentwert zurück.
        Returns a grayscale background color for a percentage value.

        Args:
            percent (int): Prozentwert von 0 (schwarz) bis 100 (weiß) / Percentage value from 0 (black) to 100 (white)

        Returns:
            str: ANSI-Hintergrundfarbe-Code / ANSI background color code
        """
        try:
            # Begrenze auf 0-100% / Limit to 0-100%
            percent = max(0, min(100, percent))

            # Konvertiere Prozent in 256-Farben-Palette (232-255 sind Graustufen)
            # Convert percentage to 256-color palette (232-255 are grayscale)
            # 232 = sehr dunkel (0%), 255 = weiß (100%)
            # 232 = very dark (0%), 255 = white (100%)
            # 24 Graustufen verfügbar, auf 21 Schritte (0-100% in 5% Schritten) verteilen
            # 24 grayscale values available, distributed over 21 steps (0-100% in 5% steps)
            gray_value = 232 + int((percent / 100.0) * 23)
            return f'\033[48;5;{gray_value}m'
        except Exception:
            return Colors.BG_BLACK

    def print_border(self, width, char='#'):
        """
        Zeichnet einen Rahmen um das gesamte Display.
        Draws a border around the entire display.

        Args:
            width (int): Breite des Displays in Zeichen / Display width in characters
            char (str): Zeichen für den Rahmen (Standard: '#') / Character for border (default: '#')
        """
        try:
            # Obere Rahmenlinie (Zeile 1) / Top border line (row 1)
            top_border = char * width
            self.update_line(1, top_border)

            # Untere Rahmenlinie (Zeile max_rows) / Bottom border line (row max_rows)
            bottom_border = char * width
            self.update_line(self.max_rows, bottom_border)

            # Seitenränder für alle Zeilen dazwischen / Side borders for all rows in between
            for row in range(2, self.max_rows):
                # Erstelle Zeile mit Rahmenzeichen am Anfang und Ende
                # Create line with border characters at start and end
                side_border = char + ' ' * (width - 2) + char
                self.update_line(row, side_border)
        except Exception:
            pass

    def update_line_with_border(self, row, text, width, border_char='#'):
        """
        Aktualisiert eine Zeile mit Text, während der Rahmen erhalten bleibt.
        Updates a line with text while preserving the border.

        Args:
            row (int): Zeilennummer (1-basiert) / Row number (1-based)
            text (str): Text der angezeigt werden soll / Text to be displayed
            width (int): Breite des Displays in Zeichen / Display width in characters
            border_char (str): Zeichen für den Rahmen (Standard: '#') / Character for border (default: '#')
        """
        try:
            # Stelle sicher, dass der Text nicht zu lang ist
            # Ensure text is not too long
            # Minus 2 für die Rahmenzeichen, minus 1 für das Leerzeichen nach dem linken Rahmenzeichen
            # Minus 2 for border characters, minus 1 for space after left border character
            max_text_width = width - 3

            # Berechne die tatsächliche Textlänge ohne ANSI-Codes
            # Calculate actual text length without ANSI codes
            text_without_ansi = strip_ansi_codes(text)
            actual_text_length = len(text_without_ansi)

            # Kürze den Text, wenn er zu lang ist (behalte ANSI-Codes)
            # Truncate text if too long (keep ANSI codes)
            if actual_text_length > max_text_width:
                # Finde die Position, an der der Text gekürzt werden muss
                # Find position where text needs to be truncated
                # Wir müssen durch den String gehen und ANSI-Codes überspringen
                # We need to go through the string and skip ANSI codes
                ansi_escape = re.compile(
                    r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                pos = 0
                visible_chars = 0
                while pos < len(text) and visible_chars < max_text_width:
                    match = ansi_escape.match(text, pos)
                    if match:
                        pos = match.end()
                    else:
                        pos += 1
                        visible_chars += 1
                text = text[:pos]

            # Erstelle Zeile mit Rahmenzeichen, Leerzeichen, Text und Rahmenzeichen
            # Create line with border characters, spaces, text and border characters
            # Berechne die benötigte Auffüllung basierend auf der tatsächlichen Textlänge
            # Calculate required padding based on actual text length
            text_without_ansi_final = strip_ansi_codes(text)
            padding_needed = max_text_width - len(text_without_ansi_final)
            line_with_border = border_char + ' ' + text + ' ' * padding_needed + border_char
            self.update_line(row, line_with_border)
        except Exception:
            pass
