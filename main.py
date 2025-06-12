import time
import random # Import the random module for generating random numbers

try:
    from adafruit_hid.mouse import Mouse
    import usb_hid # Needed to access usb_hid.devices for the Mouse constructor
    from adafruit_hid import Device # This is needed for boot.py, but good to have if debugging
except ImportError:
    print("Error: The 'adafruit_hid.mouse' or 'usb_hid' module is not available.")
    print("Please ensure your CircuitPython board has the adafruit_hid library installed,")
    print("and that basic usb_hid functionality is present in your CircuitPython build.")
    raise

# Define the range for random mouse jiggle
# These values define the minimum and maximum pixels the mouse will move
# in a single jiggle in both X and Y directions.
# Using a range like -5 to 5 will allow movement in all directions from a central point.
MIN_MOVE_DISTANCE = 5
MAX_MOVE_DISTANCE = 10
DELAY_SECONDS = 2    # Delay between jiggles

def mouse_jiggle():
    """
    Initializes the USB HID mouse and enters an infinite loop
    to jiggle the mouse cursor.
    """
    print("Jello is jiggling...")

    try:
        # Pass usb_hid.devices to the Mouse constructor.
        # This tells the Mouse object which USB HID device to control.
        mouse = Mouse(usb_hid.devices)
    except Exception as e:
        print(f"Error initializing mouse: {e}")
        print("Ensure USB HID mouse is enabled (e.g., in boot.py) and adafruit_hid library is present.")
        return

    # Small delay to allow the USB device to fully enumerate on the host computer.
    # This can prevent initial errors where the host isn't yet ready for HID input.
    time.sleep(1)

    while True:
        try:
            # Generate random movement distances for X and Y
            # random.randint(a, b) returns a random integer N such that a <= N <= b.
            # We multiply by random.choice([-1, 1]) to randomly choose a positive or negative direction.
            move_x = random.randint(MIN_MOVE_DISTANCE, MAX_MOVE_DISTANCE) * random.choice([-1, 1])
            move_y = random.randint(MIN_MOVE_DISTANCE, MAX_MOVE_DISTANCE) * random.choice([-1, 1])

            print(f"Jiggling mouse: move ({move_x}, {move_y})")
            # Move the mouse by the specified X and Y distances.
            # wheel=0 indicates no scroll wheel movement.
            mouse.move(x=move_x, y=move_y, wheel=0)
            time.sleep(DELAY_SECONDS) # Wait for the specified delay

            # No need to explicitly move back now, as the next jiggle will be random
            # and could naturally move it back or in another direction.
            # If you wanted it to return to a central point after each jiggle,
            # you would uncomment and adjust the following lines, but for pure jiggling,
            # continuous random movement is more effective.
            # print(f"Jiggling mouse: move ({-move_x}, {-move_y})")
            # mouse.move(x=-move_x, y=-move_y, wheel=0)
            # time.sleep(DELAY_SECONDS)

        except Exception as e:
            # If an error occurs during jiggling (e.g., USB disconnected),
            # print the error and wait longer before retrying to prevent rapid error cycling.
            print(f"Error during mouse jiggle: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # This check ensures that mouse_jiggle() is only called if the necessary
    # HID modules were successfully imported at the beginning of the script.
    if 'Mouse' in globals():
        mouse_jiggle()
    else:
        # This part of the error message should ideally not be reached if
        # the initial ImportError block correctly raises an exception.
        # It's kept as a fallback for clarity.
        print("Mouse jiggler cannot start due to missing 'adafruit_hid.mouse.Mouse' or 'usb_hid' module.")
