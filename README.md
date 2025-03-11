<<<<<<< HEAD
# capture_name_image
=======
# Capture Image Tool

A screen capture application that can capture selected areas with a 2-second delay, allowing cursor movement and precise image capture.

## Features

- Selective screen area capture
- 2-second countdown before capturing
- Ability to move the mouse after initial area selection
- Automatic image saving with filename based on window title and timestamp
- Custom save directory option

## Installation

### Requirements

- Python 3.6 or higher
- Required libraries:
  - pyautogui
  - pynput
  - Tkinter (usually pre-installed with Python)

### How to Install

1. Clone or download the source code
2. Install required libraries:

```bash
pip install pyautogui pynput
```

## How to Use

1. Run the application by opening a terminal and typing:
   ```bash
   python capture.py
   ```

2. The application interface will appear with the following options:
   - **Choose folder save**: Select the folder to save screenshots
   - **Capture**: Start the screen capture process

3. Screen capture process:
   - Click the **Capture** button
   - The application window will hide
   - Press and drag with the left mouse button to select the initial area
   - Release the mouse button to finish the area selection
   - A 2-second countdown timer will appear
   - During this time, you can move the mouse to a new position
   - After the countdown ends, the application will capture the image from the starting point to the final mouse position
   - The image will be saved to the selected folder

4. A notification with the saved image path will appear after a successful capture

## Customization

Parameters that can be customized in the source code:
- Countdown time (currently 2 seconds)
- Default save directory (currently "screenshots")
- Filename format

## Building a Standalone Application

You can package the application into an .exe file to run without Python installation:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the .exe file:
   ```bash
   pyinstaller --onefile --windowed --icon=icon.ico capture.py
   ```
   (Add an icon.ico file to the folder if you want a custom icon)

3. The .exe file will be created in the "dist" folder

## Notes

- If the default save directory doesn't exist, the application will create it automatically
- Make sure you have write permissions to the selected save directory
>>>>>>> e1d8780 (Complete Project)
