# main.py
# CircuitPython script for USB Mouse Jiggler
#
# This script turns a CircuitPython-compatible board into a USB mouse jiggler.
# It emulates a generic USB mouse and moves the cursor slightly
# every few seconds to prevent the system from going idle.
#
# Installation:
# 1. Ensure your CircuitPython board has the `adafruit_hid` library installed
#    (e.g., in the 'lib' folder or built into the firmware).
# 2. If your board requires explicit USB HID enablement, configure `boot.py` accordingly
#    (e.g., with `usb_hid.enable((adafruit_hid.Device.MOUSE,))`).
# 3. Copy this code and save it as `main.py` or `code.py` on your CircuitPython board.
# 4. The script will run automatically when the board boots.

import time
try:
    from adafruit_hid.mouse import Mouse
    import usb_hid # Used by CircuitPython for enabling HID devices, often in boot.py
except ImportError:
    print("Error: The 'adafruit_hid.mouse' or 'usb_hid' module is not available.")
    print("Please ensure your CircuitPython board has the adafruit_hid library installed,")
    print("and that basic usb_hid functionality is present in your CircuitPython build.")
    raise

# On CircuitPython, USB HID devices are typically enabled in boot.py.
# For example, boot.py might contain:
# import usb_hid
# from adafruit_hid import Device # Corrected import for Device
# usb_hid.enable((Device.MOUSE,))
# This main.py or code.py assumes that HID mouse is already enabled via boot.py.

# Define the mouse jiggle parameters
MOVE_DISTANCE_X = 5  # Pixels to move in X direction
MOVE_DISTANCE_Y = 5  # Pixels to move in Y direction
DELAY_SECONDS = 2    # Delay between jiggles

def mouse_jiggle():
    """
    Initializes the USB HID mouse and enters an infinite loop
    to jiggle the mouse cursor.
    """
    print("Starting CircuitPython USB Mouse Jiggler...")

    try:
        mouse = Mouse()
    except Exception as e:
        print(f"Error initializing mouse: {e}")
        print("Ensure USB HID mouse is enabled (e.g., in boot.py) and adafruit_hid library is present.")
        return

    time.sleep(1) # Small delay to ensure the USB device is ready on the host

    while True:
        try:
            print(f"Jiggling mouse: move ({MOVE_DISTANCE_X}, {MOVE_DISTANCE_Y})")
            mouse.move(x=MOVE_DISTANCE_X, y=MOVE_DISTANCE_Y, wheel=0)
            time.sleep(DELAY_SECONDS)

            print(f"Jiggling mouse: move ({-MOVE_DISTANCE_X}, {-MOVE_DISTANCE_Y})")
            mouse.move(x=-MOVE_DISTANCE_X, y=-MOVE_DISTANCE_Y, wheel=0)
            time.sleep(DELAY_SECONDS)

        except Exception as e:
            print(f"Error during mouse jiggle: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if 'Mouse' in globals():
        mouse_jiggle()
    else:
        print("Mouse jiggler cannot start due to missing 'adafruit_hid.mouse.Mouse' or 'usb_hid' module.")
