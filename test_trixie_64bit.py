#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Erweiterte Version mit:
# - Logfile-Ausgabe
# - Status-Code

import platform
import subprocess
import os
import sys
import time
from datetime import datetime

LOGFILE = "trixie_test.log"


# --- Logging System --------------------------------------------------------

def write_log(message):
    """Schreibt Zeilen ins Logfile + Terminal"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {message}"

    # Terminal
    print(message)

    # Logfile
    with open(LOGFILE, "a") as log:
        log.write(line + "\n")


# --- Farben ---------------------------------------------------------------

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


# --- Formatierte Ausgabe ---------------------------------------------------

def print_header(text):
    bar = "=" * 60
    write_log(f"{Colors.BOLD}{Colors.BLUE}{bar}{Colors.RESET}")
    write_log(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    write_log(f"{Colors.BOLD}{Colors.BLUE}{bar}{Colors.RESET}")


def print_test(text):
    write_log(f"{Colors.BOLD}→ {text}{Colors.RESET}")


def print_success(text):
    write_log(f"{Colors.GREEN}   ✓ {text}{Colors.RESET}")


def print_error(text):
    write_log(f"{Colors.RED}   ✗ {text}{Colors.RESET}")


def print_warning(text):
    write_log(f"{Colors.YELLOW}   ⚠ {text}{Colors.RESET}")


# --- OS Detection ----------------------------------------------------------

def detect_os():
    result = {
        "codename": "unknown",
        "arch": "unknown",
        "config_path": "/boot/config.txt",
        "kms_active": False,
        "display_overlay": "unknown"
    }

    try:
        codename = subprocess.check_output(
            ["lsb_release", "-cs"]).decode().strip()
        result["codename"] = codename
    except:
        # fallback
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if "VERSION_CODENAME" in line:
                        result["codename"] = line.split(
                            "=")[1].strip().strip('"')
                        break
        except:
            pass

    result["arch"] = platform.machine()

    if os.path.exists("/boot/firmware/config.txt"):
        result["config_path"] = "/boot/firmware/config.txt"

    try:
        with open(result["config_path"]) as f:
            for line in f:
                if "dtoverlay=vc4-kms-v3d" in line and not line.strip().startswith("#"):
                    result["kms_active"] = True
                    break
    except:
        pass

    if result["codename"] in ["buster", "bullseye"]:
        result["display_overlay"] = "waveshare35a:rotate=270"
    elif result["codename"] in ["bookworm", "trixie"]:
        result["display_overlay"] = "vc4-kms-dsi-waveshare-panel-v2"

    return result


# --- Tests ----------------------------------------------------------------

def test_1_framebuffer_path():
    print_test("Test 1: Framebuffer Path")

    framebuffers = []
    for fb in ["/dev/fb0", "/dev/fb1", "/dev/fb2"]:
        if os.path.exists(fb):
            try:
                with open(fb, "rb") as f:
                    f.read(1)
                print_success(f"{fb} readable")
                framebuffers.append(fb)
            except Exception as e:
                print_warning(f"{fb} exists but unreadable ({e})")

    if not framebuffers:
        print_error("No framebuffer found")
        return None

    if "/dev/fb0" in framebuffers:
        print_success("/dev/fb0 expected for KMS (good)")
        return "/dev/fb0"

    print_warning(f"Unexpected framebuffer: {framebuffers[0]}")
    return framebuffers[0]


def test_2_kms_active(info):
    print_test("Test 2: KMS status")

    if info["kms_active"]:
        print_success("KMS enabled (vc4-kms-v3d found)")
        print_warning("LCD-show incompatible with KMS")
        return True
    else:
        print_warning("KMS disabled (unexpected for Trixie)")
        return False


def test_3_python_tty_output(fb):
    print_test("Test 3: Text output to TTY")

    try:
        with open("/dev/tty1", "w") as tty:
            tty.write("\033[2J\033[H")
            tty.write("Python TTY Test OK\n")
        print_success("TTY output works")
        return True
    except Exception as e:
        print_error(f"TTY output failed ({e})")
        return False


def test_4_rotation(info):
    print_test("Test 4: Rotation handling")

    bad_overlay = False

    try:
        with open(info["config_path"]) as f:
            for line in f:
                if "waveshare35" in line and not line.startswith("#"):
                    print_error("waveshare35 overlay found → CRASH risk")
                    bad_overlay = True
                if "rotate" in line and not line.startswith("#"):
                    print_warning("rotate= in config.txt (ignored by KMS)")
    except:
        pass

    if bad_overlay:
        return False

    if info["kms_active"]:
        print_success("Rotation handled by KMS")
        return True
    else:
        print_warning("Rotation may be incorrect (no KMS)")
        return False


# --- Main -----------------------------------------------------------------

def main():
    # Logfile Reset
    if os.path.exists(LOGFILE):
        os.remove(LOGFILE)

    print_header("Trixie 64-bit LCD Compatibility Test")

    info = detect_os()
    write_log(f"Detected OS: {info['codename']}")
    write_log(f"Architecture: {info['arch']}")
    write_log(f"Config path: {info['config_path']}")
    write_log(f"KMS active: {info['kms_active']}")
    write_log(f"Overlay expected: {info['display_overlay']}")

    # Tests
    fb = test_1_framebuffer_path()
    kms = test_2_kms_active(info)
    tty = test_3_python_tty_output(fb)
    rot = test_4_rotation(info)

    # Zusammenfassung
    print_header("Summary")

    ok = True

    if fb is None:
        print_error("No framebuffer available")
        ok = False

    if not tty:
        print_error("Cannot write to TTY")
        ok = False

    if not rot:
        print_warning("Rotation problem detected")
        ok = False

    if info["codename"] != "trixie":
        print_warning("Not running Trixie")
    if info["arch"] != "aarch64":
        print_warning("Not 64-bit")

    print_header("Final Result")

    if ok:
        print_success("Display *might* work on Trixie 64-bit")
        write_log("EXIT CODE 0")
        sys.exit(0)
    else:
        print_error("Display incompatible with Trixie 64-bit")
        write_log("EXIT CODE 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
