# main.py
# MicroPython script for ESP32 USB Mouse Jiggler
#
# This script turns an ESP32 into a USB mouse jiggler.
# It emulates a generic USB mouse and moves the cursor slightly
# every few seconds to prevent the system from going idle.
#
# Installation:
# 1. Ensure your ESP32's MicroPython firmware supports USB HID.
# 2. Copy this code and save it as `main.py` on your ESP32's filesystem.
# 3. The script will run automatically when the ESP32 boots.

try:
    import time
    import usb_hid
    from usb_hid import Mouse
except ImportError:
    # If usb_hid is not available, try to provide a message if possible.
    # On a device without a screen, this might just cause a silent failure
    # or an error in the REPL if connected.
    print("Error: The 'usb_hid' module is not available on this MicroPython build.")
    print("Please ensure your ESP32 firmware includes USB HID support.")
    # Attempt to blink an LED or some other indication if possible,
    # otherwise, the script will just not work.
    # For simplicity, we'll just re-raise the error here.
    raise

# Attempt to enable USB HID if such a mechanism exists and is needed.
# Some MicroPython ports enable it automatically when usb_hid is imported and used.
# Others might require a specific call like:
# machine.USB_mode(hid=machine.USB_mode.HID_MOUSE) # Example, actual API may vary
# For now, we assume it's either auto-enabled or does not require explicit global enabling here.

# Define the mouse jiggle parameters
MOVE_DISTANCE_X = 5  # Pixels to move in X direction
MOVE_DISTANCE_Y = 5  # Pixels to move in Y direction
DELAY_SECONDS = 2    # Delay between jiggles

def mouse_jiggle():
    """
    Initializes the USB HID mouse and enters an infinite loop
    to jiggle the mouse cursor.
    """
    print("Starting USB Mouse Jiggler...")

    # Get the mouse device.
    # The exact way to get the mouse device can vary.
    # We'll assume `Mouse()` is the correct constructor.
    # If reports are needed, they are often implicitly handled by the Mouse class methods.
    try:
        mouse = Mouse()
    except Exception as e:
        print(f"Error initializing mouse: {e}")
        print("Please ensure the ESP32 is correctly connected and USB HID is supported.")
        return # Exit if mouse cannot be initialized

    # Small delay to ensure the USB device is ready on the host
    time.sleep(1)

    while True:
        try:
            # Move the mouse
            print(f"Jiggling mouse: move ({MOVE_DISTANCE_X}, {MOVE_DISTANCE_Y})")
            mouse.move(MOVE_DISTANCE_X, MOVE_DISTANCE_Y, 0) # dx, dy, wheel
            time.sleep(DELAY_SECONDS)

            # Move the mouse back
            print(f"Jiggling mouse: move ({-MOVE_DISTANCE_X}, {-MOVE_DISTANCE_Y})")
            mouse.move(-MOVE_DISTANCE_X, -MOVE_DISTANCE_Y, 0) # dx, dy, wheel
            time.sleep(DELAY_SECONDS)

            # Optional: small random movements
            # import random
            # rand_x = random.randint(-2, 2)
            # rand_y = random.randint(-2, 2)
            # mouse.move(rand_x, rand_y, 0)
            # time.sleep(0.1)

        except Exception as e:
            # This might happen if the USB connection is interrupted
            print(f"Error during mouse jiggle: {e}")
            # Attempt to re-initialize or simply wait and retry
            time.sleep(5)
            # Optionally, try to re-initialize mouse object here if robust error handling is needed
            # For a simple jiggler, just continuing might be okay, or it might fail persistently.

if __name__ == "__main__":
    # Check if usb_hid was successfully imported before trying to use it.
    if 'usb_hid' in globals():
        mouse_jiggle()
    else:
        print("Mouse jiggler cannot start due to missing usb_hid module.")
