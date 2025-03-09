# Fishing Macro

A **Python-based** fishing macro that automates a mini-game by detecting colors on the screen and clicking at the correct time.

> **Disclaimer**: Game automation may violate your game’s Terms of Service (TOS).  
> Use this script **at your own risk**.

## Features

- Continuously detects a **cyan** mini-game background and a **yellow** moving bar.
- Tracks and **clicks** automatically when conditions are met.
- Allows **configuration** for screen regions, color tolerance, and detection speed.

## Prerequisites

1. **Operating System**:
   - Script has been tested on **Windows 10/11**. May also work on macOS/Linux with some adjustments.
2. **Python**:
   - Python 3.7+ is recommended.
   - Download from [python.org](https://www.python.org/) if you don’t have it installed.

## Installation

1. **Clone or Download** the Repository
   - Click the green “Code” button on GitHub, then choose “Download ZIP”
     or run `git clone https://github.com/cnehm006/secretfish.git` in your terminal.

2. **Open a Terminal or Command Prompt**
   - Navigate to the folder where you cloned/downloaded the files.

3. **Install Dependencies**
   - Run the following commands one at a time to install the required Python libraries:
     ```bash
     pip install pyautogui
     ```
     ```bash
     pip install pillow
     ```

## Usage

1. **Tweak CPU Usage**
   - Look for line 9:
     ```python
     SLEEP_BETWEEN_CHECKS = 0.0001
     ```
     Increase this value (e.g., `0.05` or `0.1`) to **lower** CPU usage (but slower detection), or decrease it to **speed up** detection (but higher CPU usage).

2. **Run the Script**
   - In your terminal, from the project folder, type:
     ```bash
     python script.py
     ```

3. **Switch to Your Game Window**
   - When the script starts, it may display a semi-transparent rectangle outlining the detection region. Close it when you’re ready.
   - The script will cast, detect the mini-game (cyan), and click on the yellow bar automatically.

## Troubleshooting

- **Not Detecting Anything**
  - Increase `COLOR_TOLERANCE` in the script if your game’s colors vary.
  - Make sure the `REGION` matches the exact on-screen location.

- **Too Slow or High CPU Usage**
  - Increase sleeps (`SLEEP_BETWEEN_CHECKS`) or use pixel-skipping (`SKIP`).

- **False Positives**
  - Make the bounding box smaller or refine the color/tolerance settings to avoid background detections.

## Contributing

1. **Fork** this repository.
2. **Create a Feature Branch** (`git checkout -b feature/awesome-improvement`).
3. **Commit Your Changes** (`git commit -m 'Add some awesome improvement'`).
4. **Push to the Branch** (`git push origin feature/awesome-improvement`).
5. **Open a Pull Request**.

## Disclaimer

This software is provided **“as is”**, without warranty of any kind. Usage of game automation scripts may violate your game’s TOS. Always check before using.

---

Happy fishing – and **use responsibly**!