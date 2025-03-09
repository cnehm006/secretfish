import cv2
import numpy as np
import pyautogui
import time

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
# Define the region (gray rectangle) where the mini-game appears.
REGION = (865, 1160, 840, 75)  # (left, top, width, height)

# HSV thresholds for detecting the cyan box.
# (The provided CYAN_RGB is (142, 252, 189). Adjust these values if needed.)
LOWER_CYAN = np.array([60, 100, 100])   # lower bound for hue, saturation, value
UPPER_CYAN = np.array([80, 255, 255])     # upper bound for cyan

# HSV thresholds for detecting the yellow bar.
# (Based on YELLOW_RGB = (255, 208, 37))
LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([30, 255, 255])

# Timing configuration
SLEEP_BETWEEN_FRAMES = 0.02   # Frame delay for near real-time processing.
POST_CLICK_WAIT = 0.1         # Pause after a click to allow for game processing.
CAST_WAIT_TIME = 7.0          # Wait time (in seconds) when no cyan is detected before casting.

def capture_region(region):
    """Capture the specified screen region and convert it to BGR (OpenCV format)."""
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

def find_largest_contour(mask):
    """Return the largest contour found in the mask, or None if no contours exist."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key=cv2.contourArea)
    return None

def get_bounding_box(contour):
    """Return the bounding rectangle (x, y, w, h) for the given contour."""
    return cv2.boundingRect(contour)

def detect_cyan_box(hsv_frame):
    """
    Detect the cyan box in the provided HSV image.
    Returns a bounding box (x, y, w, h) relative to hsv_frame if found, else None.
    """
    cyan_mask = cv2.inRange(hsv_frame, LOWER_CYAN, UPPER_CYAN)
    contour = find_largest_contour(cyan_mask)
    if contour is not None:
        return get_bounding_box(contour)
    return None

def detect_yellow_in_region(hsv_region):
    """
    Check if yellow is present in the provided HSV region.
    Returns True if the number of yellow pixels exceeds zero.
    """
    yellow_mask = cv2.inRange(hsv_region, LOWER_YELLOW, UPPER_YELLOW)
    return cv2.countNonZero(yellow_mask) > 0

def cast_rod():
    """
    Simulate casting the fishing rod.
    Modify this function if you need to click at a specific location for casting.
    """
    print("No fish detected. Casting rod.")
    pyautogui.click()  # This clicks at the current mouse location.

def main_loop():
    state = "idle"  # possible states: idle, tracking, caught
    last_cast_time = time.time()

    print("Starting auto-fishing macro. Press Ctrl+C to stop.")

    while True:
        frame = capture_region(REGION)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cyan_box = detect_cyan_box(hsv)

        if state == "idle":
            if cyan_box is not None:
                # Cyan box detected – a fish is baited. Transition to tracking.
                state = "tracking"
                print("Cyan box detected. Transitioning to tracking state.")
            else:
                print("Idle: No cyan detected.")
                # If no cyan has been detected for CAST_WAIT_TIME, cast the rod.
                if time.time() - last_cast_time >= CAST_WAIT_TIME:
                    cast_rod()
                    last_cast_time = time.time()

        elif state == "tracking":
            if cyan_box is not None:
                x, y, w, h = cyan_box
                # Calculate the center of the cyan box relative to REGION.
                cx = x + w // 2
                cy = y + h // 2
                # Convert to absolute screen coordinates.
                absolute_x = REGION[0] + cx
                absolute_y = REGION[1] + cy
                # Move the mouse cursor to the cyan box center.
                pyautogui.moveTo(absolute_x, absolute_y, duration=0)
                print(f"Tracking cyan box at ({absolute_x}, {absolute_y}) (Box: x={x}, y={y}, w={w}, h={h}).")

                # Crop the HSV image to the cyan box region.
                cyan_region = hsv[y:y+h, x:x+w]
                if detect_yellow_in_region(cyan_region):
                    print("Yellow detected inside cyan box. Clicking!")
                    # Click at the center of the cyan box.
                    pyautogui.click(absolute_x, absolute_y)
                    time.sleep(POST_CLICK_WAIT)
                    # Transition to 'caught' state to wait for the cyan box to disappear.
                    state = "caught"
                else:
                    print("No yellow detected within cyan box yet.")
            else:
                print("Lost cyan box while tracking. Reverting to idle.")
                state = "idle"

        elif state == "caught":
            # After a click, wait for the cyan box to vanish before resetting.
            if cyan_box is None:
                print("Cyan box has disappeared. Resetting to idle state.")
                state = "idle"
            else:
                print("Fish caught. Still waiting for cyan box to vanish.")

        time.sleep(SLEEP_BETWEEN_FRAMES)

if __name__ == "__main__":
    main_loop()