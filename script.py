import time
import tkinter as tk
import pyautogui
REGION = (865, 1160, 840, 75)
CYAN_RGB = (34, 166, 133)
YELLOW_RGB = (255, 208, 37)
COLOR_TOLERANCE = 40
WAIT_FOR_CYAN_TIMEOUT = 15
SLEEP_BETWEEN_CHECKS = 0.00001   # smaller => more frequent scanning but higher CPU usage. Put a bigger value if your computer is on the lower end.
POST_CLICK_WAIT = 0.05
SKIP = 1
pyautogui.PAUSE = 0.0
def show_region_outline(region, outline_duration=None):
    left, top, width, height = region
    root = tk.Tk()
    root.title("Region Outline")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.attributes("-alpha", 0.3)
    geometry_str = f"{width}x{height}+{left}+{top}"
    root.geometry(geometry_str)
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    canvas.create_rectangle(0, 0, width, height, outline="red", width=2)
    def on_key(event):
        if event.keysym == 'Escape':
            root.destroy()
    canvas.bind_all("<Key>", on_key)
    if outline_duration is not None:
        root.after(int(outline_duration * 1000), root.destroy)
    root.mainloop()
def color_is_close(pixel_color, target_color, tolerance=20):
    return (
        abs(pixel_color[0] - target_color[0]) <= tolerance and
        abs(pixel_color[1] - target_color[1]) <= tolerance and
        abs(pixel_color[2] - target_color[2]) <= tolerance
    )
def find_color_box_center_in_region(target_color, region, tolerance=20, skip=1):
    left, top, width, height = region
    screenshot = pyautogui.screenshot(region=region)
    min_x, min_y = width, height
    max_x, max_y = 0, 0
    found_any = False
    for y in range(0, height, skip):
        for x in range(0, width, skip):
            pixel = screenshot.getpixel((x, y))
            if color_is_close(pixel, target_color, tolerance):
                found_any = True
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y
    if found_any:
        abs_min_x = left + min_x
        abs_min_y = top + min_y
        abs_max_x = left + max_x
        abs_max_y = top + max_y
        cx = (abs_min_x + abs_max_x) // 2
        cy = (abs_min_y + abs_max_y) // 2
        return (cx, cy, abs_min_x, abs_max_x, abs_min_y, abs_max_y)
    else:
        return None
def scan_region_for_color(region, target_color, tolerance=20, skip=1):
    left, top, width, height = region
    screenshot = pyautogui.screenshot(region=region)
    for y in range(0, height, skip):
        for x in range(0, width, skip):
            pixel = screenshot.getpixel((x, y))
            if color_is_close(pixel, target_color, tolerance):
                return True
    return False
def cast_fishing_rod():
    print("Casting fishing rod...")
    pyautogui.click()
def wait_for_cyan(timeout=15):
    start_time = time.time()
    while time.time() - start_time < timeout:
        box_info = find_color_box_center_in_region(
            CYAN_RGB, REGION, tolerance=COLOR_TOLERANCE, skip=SKIP
        )
        if box_info:
            return box_info
        time.sleep(SLEEP_BETWEEN_CHECKS)
    return None
def still_has_cyan():
    res = find_color_box_center_in_region(CYAN_RGB, REGION, tolerance=COLOR_TOLERANCE, skip=SKIP)
    return (res is not None)
def main_fishing_loop():
    print("Starting fishing macro. Press Ctrl+C to stop.")
    while True:
        cast_fishing_rod()
        print("Waiting 3s for cast animation...")
        time.sleep(3)
        first_cyan = wait_for_cyan(timeout=WAIT_FOR_CYAN_TIMEOUT)
        if not first_cyan:
            print("No cyan -> recasting.\n")
            continue
        while True:
            if not still_has_cyan():
                print("No more cyan -> fish caught.\n")
                break
            stage_done = False
            while True:
                if not still_has_cyan():
                    print("Cyan vanished -> end or next stage.\n")
                    break
                box_info = find_color_box_center_in_region(
                    CYAN_RGB, REGION, tolerance=COLOR_TOLERANCE, skip=SKIP
                )
                if not box_info:
                    print("No bounding box found this iteration.\n")
                    break
                cx, cy, min_x, max_x, min_y, max_y = box_info
                w = (max_x - min_x) + 1
                h = (max_y - min_y) + 1
                print(f"Tracking cyan -> center=({cx},{cy}), bounding=({min_x},{min_y})-({max_x},{max_y}).")
                if w <= 0 or h <= 0:
                    print("Invalid bounding box. Breaking.\n")
                    break
                pyautogui.moveTo(cx, cy, duration=0)
                margin = 5
                expanded_min_x = max(0, min_x - margin)
                expanded_min_y = max(0, min_y - margin)
                expanded_w = w + (margin * 2)
                expanded_h = h + (margin * 2)
                bounding_region = (expanded_min_x, expanded_min_y, expanded_w, expanded_h)  
                found_yellow = False
                attempts = 0
                max_attempts = 3
                while attempts < max_attempts and not found_yellow:
                    found_yellow = scan_region_for_color(
                        bounding_region, YELLOW_RGB, tolerance=COLOR_TOLERANCE, skip=SKIP
                    )
                    if not found_yellow:
                        time.sleep(SLEEP_BETWEEN_CHECKS)
                    attempts += 1
                if found_yellow:
                    print("Detected YELLOW! Clicking once...")
                    pyautogui.click()
                    time.sleep(POST_CLICK_WAIT)
                    print("Clicked. Next stage...\n")
                    stage_done = True
                    break
                else:
                    time.sleep(SLEEP_BETWEEN_CHECKS)
            if stage_done:
                continue
            else:
                break
if __name__ == "__main__":
    print("Showing region outline; close it (Esc or X) when ready.")
    show_region_outline(REGION)
    print("Outline closed. Starting in 3s...")
    time.sleep(3)
    main_fishing_loop()