# Installation 3.5" LCD Display Berrybase

## Overview

This installation script sets up a **3.5" SPI LCD display** (GoodTFT/XPT2046-based) on a Raspberry Pi and makes it usable without errors. The installation is performed in two steps with an automatic reboot in between.

**Important:** This project supports **GoodTFT/XPT2046-based 3.5" displays** (also known as "3.5 inch RPi Display" or "3.5 inch RPi LCD"). These displays do **NOT** use the Waveshare overlay. Waveshare ≠ GoodTFT.

**Project Purpose:**

- Installation and configuration of the 3.5" LCD display for error-free use
- Provision of display utilities (`the_programm_display_utils.py`) for flicker-free output
- Automatic startup of the target program (`the_programm_main.py`) after boot
- Easy integration of your own projects

**📖 Important Documentation:**

- **This file:** Installation guide
- **`README_PROJECT_USAGE_english.md`:** Detailed guide for using your own projects and using the display utilities

**Compatibility:**

- Raspberry Pi 3 B
- **Raspberry Pi Zero 2 W** (tested and works flawlessly)
- **3.5" SPI LCD Display** (GoodTFT/XPT2046-based)
  - Touch Controller: **XPT2046** (sometimes misprinted as XP12046)
  - Manufacturers: GoodTFT / KeDei / MHS
  - Also known as: "3.5 inch RPi Display" / "3.5 inch RPi LCD"
  - **IMPORTANT:** These displays do **NOT** use the Waveshare overlay
- **Raspberry Pi OS Buster Lite (32-bit) - Image: 2023-05-03-raspios-buster-armhf-lite.img.xz**
- **IMPORTANT:** Only this specific 32-bit Buster image is supported.
- **64-bit versions have been tested and are NOT supported** - no further attempts needed.

## Prerequisites

1. **Raspberry Pi OS Image (IMPORTANT - Only this image works!):**
   - **2023-05-03-raspios-buster-armhf-lite.img.xz**
   - Raspberry Pi OS Buster Lite (32-bit)
   - **IMPORTANT:** Only 32-bit Buster is supported!
   - **Note:** Other images (64-bit, Bookworm, Bullseye, newer versions) have been extensively tested and do **not** work with this installation
   - **64-bit versions are NOT supported anymore** - no further attempts needed.
   - **Download:** The image can be downloaded from the official Raspberry Pi website (Legacy Images / Buster)
   - Image written to SD card

2. **Hardware:**
   - Raspberry Pi 3 B
   - **Raspberry Pi Zero 2 W** (tested and works flawlessly)
   - **3.5" SPI LCD Display** (GoodTFT/XPT2046-based)
     - Touch Controller: XPT2046
     - Manufacturers: GoodTFT / KeDei / MHS
   - SD card with installed OS

3. **Access:**
   - SSH access OR
   - Keyboard and HDMI monitor for installation

## Installation Process

### Step 1: Copy Files to Raspberry Pi

Copy all files from this directory to the Raspberry Pi, e.g., to `/home/pi/Install_3.5_LCD_Display_Berrybase/`

### Step 2: Start Installation

```bash
cd /home/pi/Install_3.5_LCD_Display_Berrybase
sudo python3 main.py
```

### Step 3: Automatic Process

The installation runs fully automatically:

1. **main.py** starts **install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py**
   - System is prepared (apt-get update, git, dos2unix)
   - LCD-show repository is cloned from GitHub
   - Windows line endings are corrected
   - LCD35-show driver is installed (lite version)
   - config.txt is adjusted for rotation (270°)
   - Service for second_file is set up
   - **System automatically reboots**

2. **After Reboot:**
   - **install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py** is automatically started
   - The Programm Service is set up (the-programm.service)
   - Installation is complete

### Step 4: Test Installation

**Installation Time:** The initial installation typically takes **5-15 minutes**, depending on internet connection and SD card speed. The installation time is displayed in the test program after installation is complete.

After successful installation, the program starts automatically after boot. You can also start it manually:

```bash
sudo python3 /home/pi/the_programm_main.py
```

**Note:**

- The main program (`the_programm_main.py`) starts the test program (`the_programm_display_berrybase_test.py`) by default
- To use your own project, see `README_PROJECT_USAGE_english.md`

## File Structure

```
Install_3.5_LCD_Display_Berrybase/
├── main.py                                          # Starts the installation
├── install_lcd_3.5_zoll_display_berrybase_first_file_the_installer.py    # Installation step 1
├── install_lcd_3.5_zoll_display_berrybase_second_file_after_install.py  # Installation step 2
├── the_programm_main.py                             # Main program wrapper (starts target program)
├── the_programm_display_utils.py                    # Display utilities for flicker-free output
├── the_programm_display_berrybase_test.py          # Test program (started by the_programm_main.py)
├── uninstall_lcd_3.5_zoll_display_berrybase_complete.py      # Complete uninstallation
├── uninstall_lcd_3.5_zoll_display_berrybase_autostart.py     # Uninstall autostart only
├── README_3.5_LCD_ZOLL_DISPLAY_BERRYBASE_english.md         # This file (installation guide)
└── README_PROJECT_USAGE_english.md                        # Guide for using your own projects
```

## What Gets Installed?

### LCD Display Driver

- LCD-show repository is installed (compatible with GoodTFT/XPT2046 displays)
- LCD35-show driver (lite version)
- Rotation: 270° (portrait mode)
- Touch functionality is set up (XPT2046 controller)
- Drivers: fbtft, MHS35, rpi-fbcp

### Systemd Services

- `install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service` - Starts second_file after reboot
- `the-programm.service` - Set up by second_file (starts the_programm_main.py)

### Config.txt Changes

- `dtoverlay=waveshare35a:rotate=270` is added
- Old waveshare35* entries are removed

## Uninstallation

There are two uninstallation options:

### Option 1: Remove Autostart Only (LCD Remains Functional)

```bash
sudo python3 /home/pi/uninstall_lcd_3.5_zoll_display_berrybase_autostart.py
```

This removes:

- `install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service`
- `the-programm.service`

**Note:** The LCD display installation itself remains. Only the autostart services are removed.

### Option 2: Complete Uninstallation (LCD is Deactivated)

```bash
sudo python3 /home/pi/uninstall_lcd_3.5_zoll_display_berrybase_complete.py
```

This removes:

- All services and autostart
- LCD driver (`/home/pi/LCD-show/`)
- `config.txt` changes (dtoverlay)

**Note:** After this uninstallation, the display no longer works (white screen). A reinstallation with `main.py` is possible.

**Manual Check After Uninstallation:**

```bash
# Check if service files still exist
ls -la /etc/systemd/system/ | grep -E "install_lcd|the-programm"

# If files still exist, delete manually:
sudo rm -f /etc/systemd/system/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
sudo rm -f /etc/systemd/system/the-programm.service

# Remove symlinks (if present)
sudo rm -f /etc/systemd/system/multi-user.target.wants/install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
sudo rm -f /etc/systemd/system/multi-user.target.wants/the-programm.service

# Reload systemd
sudo systemctl daemon-reload
```

## Troubleshooting

### Display Shows Nothing

1. Check the connection between Raspberry Pi and display
2. Check `/boot/config.txt`:

   ```bash
   sudo nano /boot/config.txt
   ```

   Should contain: `dtoverlay=waveshare35a:rotate=270`

### Installation Hangs

- Check internet connection (Git clone requires internet)
- Check logs: `journalctl -u install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service`

### Touch Doesn't Work

- Check if `xserver-xorg-input-evdev` is installed
- Check the touch cable connection

### Service Doesn't Start

```bash
# Check service status
sudo systemctl status install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service

# Start service manually
sudo systemctl start install_lcd_3.5_zoll_display_berrybase_second_file_after_install.service
```

## Manual Config.txt Editing

If you need to manually edit the config.txt:

```bash
# For Raspberry Pi OS Buster (this image):
sudo nano /boot/config.txt
```

**Note:** In Raspberry Pi OS Buster, the config.txt is located directly in `/boot/config.txt`, not in `/boot/firmware/`.

**Important Entries:**

```
dtoverlay=waveshare35a:rotate=270
```

## References

- [Install 3.5" LCD Display Berrybase - This Project](https://github.com/tnt-nitro/Install_3.5_LCD_Display_Berrybase)
- [LCD-show GitHub Repository](https://github.com/goodtft/LCD-show)
- [Waveshare Wiki - 3.5" LCD (B)](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)#Screen_orientation_settings)
- [Waveshare LCD-show GitHub](https://github.com/waveshare/LCD-show)

## Technical Information

**Display Type:**

- **GoodTFT/XPT2046-based 3.5" SPI Displays**
- These displays do **NOT** use the Waveshare overlay
- Waveshare ≠ GoodTFT
- This is exactly why they do **NOT** work on Pi 5 under 64-bit without modifications

**Drivers:**

- fbtft, MHS35, rpi-fbcp
- Touch: XPT2046

## Main Program

The main program (`the_programm_main.py`) is a wrapper that starts the actual target program. By default, it starts the test program (`the_programm_display_berrybase_test.py`).

**Important:** To use your own project, see the detailed guide in `README_PROJECT_USAGE_english.md`.

### Display Utilities

The file `the_programm_display_utils.py` contains important utilities for flicker-free display output:

- **Display Class:** For flicker-free line updates
- **Colors Class:** ANSI color codes for colored output
- **Functions:** `strip_ansi_codes()` for correct text length calculation

**These utilities MUST be used** to ensure error-free display output. See `README_PROJECT_USAGE_english.md` for details.

## Support

If you have problems, check:

1. The logs: `journalctl -u <service-name>`
2. The config.txt: `/boot/config.txt` or `/boot/firmware/config.txt`
3. The service status: `sudo systemctl status <service-name>`
