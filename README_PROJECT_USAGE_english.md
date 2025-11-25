# Project Usage: Your Own Applications on the LCD Display

## Overview

This guide explains how to use the installed LCD display for your own application. The project provides important utilities that **must be used** for error-free display output.

## ⚠️ IMPORTANT: Display Utilities are Mandatory!

**The file `the_programm_display_utils.py` MUST be used!**

- **Without these utilities:** The display flickers, output is unreadable, colors don't work correctly
- **With these utilities:** Flicker-free, stable output, correct color display, precise cursor positioning

**Even if you:**
- Haven't used the project for a long time
- Are new to the project and seeing it for the first time
- Want to adapt an existing program

**→ The display utilities MUST be used!** This guide explains exactly how.

## Why Use Display Utilities?

The LCD display requires special handling to ensure flicker-free output:

- **Normal `print()` statements** cause flickering and unreadable output
- **ANSI escape codes** must be used correctly
- **Cursor positioning** must be precise
- **Line updates** must occur without screen flickering

The provided `the_programm_display_utils.py` automatically solves all these problems.

## Understanding Project Structure

### Current Configuration

```
/home/pi/
├── the_programm_main.py                    # Wrapper that starts your program
├── the_programm_display_utils.py           # Display utilities (MUST be used)
└── the_programm_display_berrybase_test.py  # Test program (example)
```

### Service Configuration

The `the-programm.service` starts automatically after boot:
- **Starts:** `/home/pi/the_programm_main.py`
- **Output:** Directly to `/dev/tty1` (LCD Display)
- **Logs:** `/home/pi/logs/the_programm.log`

## Method 1: Integrate Your Own Application into the_programm_main.py

### Step 1: Prepare Your Program

Create your Python program and make sure it uses the display utilities:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Your own program

import sys
import os
from the_programm_display_utils import Display, Colors

def main():
    # Initialize display (IMPORTANT!)
    display = Display(max_rows=30)
    display.init()
    
    try:
        # Your program code here
        display.update_line(1, "Welcome to my program!")
        display.update_line(2, f"{Colors.GREEN}Status: Ready{Colors.RESET}")
        
        # Example: Infinite loop
        counter = 0
        while True:
            counter += 1
            display.update_line(3, f"Counter: {counter}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up display (IMPORTANT!)
        display.cleanup()

if __name__ == "__main__":
    main()
```

### Step 2: Modify the_programm_main.py

Open `/home/pi/the_programm_main.py` and change the path:

```python
# Change this line:
script_path = os.path.join(os.path.dirname(__file__), "the_programm_display_berrybase_test.py")

# To your program:
script_path = "/path/to/your/program.py"
```

**Example:**
```python
script_path = "/home/pi/my_program.py"
```

### Step 3: Restart Service

```bash
sudo systemctl restart the-programm.service
```

## Method 2: Duplicate Project for Other Programs

**When to use?**
- You want to use the display in another program
- You want to run multiple projects in parallel
- You want to keep the original project unchanged

**Important:** If you want to use the display in another program, duplicate the project and replace `the_programm_main.py` with the startup file of your desired application.

If you have multiple projects or want to keep the original project:

### Step 1: Create Project Directory

```bash
mkdir -p /home/pi/my_project
cd /home/pi/my_project
```

### Step 2: Copy Display Utilities

```bash
cp /home/pi/the_programm_display_utils.py /home/pi/my_project/
```

**IMPORTANT:** The `the_programm_display_utils.py` MUST be in the same directory as your program or available in the Python path. **This file is essential for error-free display output and MUST be used!**

### Step 3: Create Your Program OR Adapt Existing Program

**If you're creating a new program:**

Create `my_program.py` in `/home/pi/my_project/`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Your program

import sys
import os
import time

# Import display utils (from same directory)
from the_programm_display_utils import Display, Colors

def main():
    # Initialize display
    display = Display(max_rows=30)
    display.init()
    
    try:
        # Your program code
        display.update_line(1, f"{Colors.BOLD}My Program{Colors.RESET}")
        display.update_line(2, f"{Colors.GREEN}Running...{Colors.RESET}")
        
        # Example logic
        for i in range(10):
            display.update_line(3, f"Step {i+1}/10")
            time.sleep(1)
            
    except KeyboardInterrupt:
        display.update_line(3, f"{Colors.YELLOW}Stopped{Colors.RESET}")
    finally:
        display.cleanup()

if __name__ == "__main__":
    main()
```

**If you're using an existing program:**

1. Copy your existing program to `/home/pi/my_project/`
2. **IMPORTANT:** Adapt your program to use the display utilities:
   - Import `from the_programm_display_utils import Display, Colors`
   - Replace all `print()` statements with `display.update_line()`
   - Initialize the display with `display.init()` at the beginning
   - Clean up with `display.cleanup()` in the `finally` block

**Example Adaptation:**

```python
# BEFORE (normal program):
print("Hello World!")
print(f"Status: {status}")

# AFTER (with display utils):
from the_programm_display_utils import Display, Colors

display = Display(max_rows=30)
display.init()
try:
    display.update_line(1, "Hello World!")
    display.update_line(2, f"Status: {status}")
finally:
    display.cleanup()
```

### Step 4: Modify the_programm_main.py OR Adapt Service

**Option A: Modify the_programm_main.py (simple)**

```python
script_path = "/home/pi/my_project/my_program.py"
```

**Option B: Adapt Service Directly (for multiple projects)**

If you have multiple projects, you can also adapt the service directly:

```bash
sudo nano /etc/systemd/system/the-programm.service
```

Change the `ExecStart` line:

```ini
ExecStart=/bin/bash -c 'cd /home/pi/my_project && /usr/bin/python3 -u /home/pi/my_project/my_program.py 2>&1 | tee -a /home/pi/logs/the_programm.log'
```

Then:

```bash
sudo systemctl daemon-reload
```

### Step 5: Restart Service

```bash
sudo systemctl restart the-programm.service
```

## Display Utilities: Detailed Guide

### Display Class

The `Display` class is the core for flicker-free output.

#### Initialization

```python
from the_programm_display_utils import Display

# Create a display object
display = Display(max_rows=30)  # 30 rows (standard for 3.5" LCD)

# Initialize the display (clears screen, hides cursor)
display.init()
```

#### Important Methods

##### `update_line(row, text)`
Updates a line without flickering:

```python
# Update line 1
display.update_line(1, "Hello World!")

# With colors
display.update_line(2, f"{Colors.GREEN}Status: OK{Colors.RESET}")
```

**Important:**
- `row` starts at 1 (not 0)
- Text is automatically set to the line
- Old content is automatically cleared

##### `clear_screen()`
Clears the entire screen:

```python
display.clear_screen()
```

##### `clear_full_screen()`
Clears the screen and fills all lines with spaces:

```python
display.clear_full_screen()
```

##### `move_cursor(row, col)`
Moves the cursor to a specific position:

```python
display.move_cursor(5, 10)  # Row 5, column 10
```

##### `print_border(width, char='#')`
Draws a border around the display:

```python
display.print_border(width=60, char='#')
```

##### `update_line_with_border(row, text, width, border_char='#')`
Updates a line while preserving the border:

```python
display.update_line_with_border(5, "My Text", width=60, border_char='#')
```

##### `cleanup()`
Cleans up the display (shows cursor again):

```python
display.cleanup()
```

**IMPORTANT:** Always call `cleanup()` in the `finally` block!

### Colors Class

The `Colors` class provides ANSI color codes.

#### Foreground Colors

```python
from the_programm_display_utils import Colors

# Available colors:
Colors.RED      # Red
Colors.GREEN    # Green
Colors.YELLOW   # Yellow
Colors.BLUE     # Blue
Colors.MAGENTA  # Magenta
Colors.CYAN     # Cyan
Colors.PURPLE   # Purple
Colors.WHITE    # White
Colors.BLACK    # Dark gray
Colors.RESET    # Reset
Colors.BOLD     # Bold
```

#### Usage

```python
# Output text in color
text = f"{Colors.GREEN}Success!{Colors.RESET}"
display.update_line(1, text)

# Combinations
text = f"{Colors.BOLD}{Colors.RED}ERROR!{Colors.RESET}"
display.update_line(2, text)
```

**IMPORTANT:** Always use `Colors.RESET` after colored text!

#### Background Colors

```python
# Available background colors:
Colors.BG_BLACK
Colors.BG_RED
Colors.BG_GREEN
Colors.BG_YELLOW
Colors.BG_BLUE
Colors.BG_MAGENTA
Colors.BG_CYAN
Colors.BG_WHITE

# Special colors:
Colors.BG_ORANGE
Colors.BG_BROWN
Colors.BG_PINK
Colors.BG_LIME
Colors.BG_VIOLET

# Grayscale:
Colors.BG_GRAY_DARK
Colors.BG_GRAY_1
Colors.BG_GRAY_2
Colors.BG_GRAY_3
Colors.BG_GRAY_LIGHT
```

#### Filled Rectangles

```python
# Filled rectangle in a color
block = display.print_colored_block(width=20, bg_color=Colors.BG_RED, label="Status: ")
display.update_line(5, block)
```

#### Grayscale for Percentage Values

```python
# Grayscale for a percentage value (0-100)
color = display.get_grayscale_color(percent=75)  # 75% = light gray
block = display.print_colored_block(width=50, bg_color=color)
display.update_line(6, block)
```

### Helper Function: strip_ansi_codes()

Removes ANSI codes from a string (for length calculation):

```python
from the_programm_display_utils import strip_ansi_codes

text = f"{Colors.GREEN}Hello{Colors.RESET}"
length_with_codes = len(text)  # Length with ANSI codes
length_without_codes = len(strip_ansi_codes(text))  # Actual text length
```

## Complete Example

Here is a complete example showing all important concepts:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Example program for LCD Display

import time
import sys
from the_programm_display_utils import Display, Colors

def main():
    # Initialize display
    display = Display(max_rows=30)
    display.init()
    
    try:
        # Title
        display.update_line(1, f"{Colors.BOLD}{Colors.CYAN}=== My Program ==={Colors.RESET}")
        
        # Status
        display.update_line(3, f"{Colors.GREEN}Status: Ready{Colors.RESET}")
        
        # Draw border
        display.print_border(width=60, char='=')
        
        # Main area
        counter = 0
        while True:
            counter += 1
            
            # Show counter
            display.update_line(5, f"Counter: {counter}")
            
            # Colored status bar
            percent = (counter % 100)
            color = display.get_grayscale_color(percent)
            bar = display.print_colored_block(width=percent//2, bg_color=color, label="Progress: ")
            display.update_line(7, bar)
            
            # Show time
            from datetime import datetime
            now = datetime.now().strftime("%H:%M:%S")
            display.update_line(9, f"Time: {now}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        display.update_line(3, f"{Colors.YELLOW}Status: Stopped{Colors.RESET}")
        time.sleep(2)
    finally:
        # IMPORTANT: Clean up display
        display.cleanup()

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Always Initialize and Clean Up Display

```python
display = Display(max_rows=30)
display.init()

try:
    # Your code
    pass
finally:
    display.cleanup()  # ALWAYS clean up!
```

### 2. Always Reset Colors

```python
# CORRECT:
text = f"{Colors.GREEN}Text{Colors.RESET}"

# WRONG:
text = f"{Colors.GREEN}Text"  # Color remains active!
```

### 3. Don't Overwrite Lines Without update_line()

```python
# CORRECT:
display.update_line(1, "New Text")

# WRONG:
print("New Text")  # Causes flickering!
```

### 4. Truncate Long Texts

```python
text = "Very long text that doesn't fit on the display..."
if len(text) > 60:  # Check display width
    text = text[:57] + "..."
display.update_line(1, text)
```

### 5. Consider ANSI Codes in Length Calculation

```python
from the_programm_display_utils import strip_ansi_codes

text = f"{Colors.GREEN}Hello{Colors.RESET}"
actual_length = len(strip_ansi_codes(text))  # Correct length
```

## Troubleshooting

### Problem: Display Flickers

**Solution:** Always use `display.update_line()` instead of `print()`.

### Problem: Colors Don't Work

**Solution:** Make sure you use `Colors.RESET` after colored text.

### Problem: Cursor is Visible

**Solution:** Call `display.init()` at the beginning and `display.cleanup()` at the end.

### Problem: Lines Are Not Updated

**Solution:** Use `display.update_line(row, text)` with correct row number (1-based).

### Problem: Program Doesn't Start After Boot

**Solution:** Check the service status:

```bash
sudo systemctl status the-programm.service
sudo journalctl -u the-programm.service -n 50
```

## Service Management

### Restart Service

```bash
sudo systemctl restart the-programm.service
```

### Stop Service

```bash
sudo systemctl stop the-programm.service
```

### Start Service

```bash
sudo systemctl start the-programm.service
```

### Check Service Status

```bash
sudo systemctl status the-programm.service
```

### View Logs

```bash
# Last 50 lines
sudo journalctl -u the-programm.service -n 50

# Live logs
sudo journalctl -u the-programm.service -f

# Log file
tail -f /home/pi/logs/the_programm.log
```

## Summary

1. **Use display utilities:** The `the_programm_display_utils.py` MUST be used for error-free output
2. **Initialize display:** `display.init()` at the beginning
3. **Clean up display:** `display.cleanup()` in the `finally` block
4. **Use update_line():** Never use `print()` directly, always use `display.update_line()`
5. **Reset colors:** Always use `Colors.RESET` after colored text
6. **Modify the_programm_main.py:** Enter the path to your program
7. **Restart service:** After changes `sudo systemctl restart the-programm.service`

If you have questions or problems, check the logs and make sure you're using the display utilities correctly.

