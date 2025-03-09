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
     or run `git clone https://github.com/<your-username>/<your-repo>.git` in your terminal.

2. **Open a Terminal or Command Prompt**
   - Navigate to the folder where you cloned/downloaded the files.

3. **Install Dependencies**
   - Run the following command to install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```
   - Or, if you want to install them manually:
     ```bash
     pip install pyautogui
     pip install pillow
     ```
     *(Adjust if your script requires additional packages like tkinter or opencv-python.)*

4. **Verify Installation**
   - In the same terminal, run:
     ```bash
     python --version
     pip freeze
     ```
   - Confirm Python is **3.7+** and that you see the required libraries (pyautogui, etc.) in the installed packages list.

## Usage

1. **Configure the Script**
   - Open the main Python file (e.g., `fishing_macro.py`) in a text editor.
   - Adjust the `REGION`, color values (`CYAN_RGB`, `YELLOW_RGB`), and detection settings (`COLOR_TOLERANCE`, etc.) to match your game’s on-screen positions and colors.

2. **Run the Script**
   - In your terminal, from the project folder, type:
     ```bash
     python fishing_macro.py
     ```
   - (Replace `fishing_macro.py` with the actual script name if different.)

3. **Switch to Your Game Window**
   - When the script starts, it may display a semi-transparent rectangle outlining the detection region. Close it when you’re ready.
   - The script will cast, detect the mini-game (cyan), and click on the yellow bar automatically.

## Troubleshooting

- **Not Detecting Anything**
  - Increase `COLOR_TOLERANCE` in the script if your game’s colors vary.
  - Make sure the `REGION` matches the exact on-screen location.

- **Too Slow or High CPU Usage**
  - Increase sleeps (`SLEEP_BETWEEN_CHECKS`) or use pixel-skipping (if supported in the script).
  - Use smaller detection regions if your screen is large.

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