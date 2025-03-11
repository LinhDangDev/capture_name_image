import pyautogui
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import datetime
from pynput import mouse
import time
import threading
import ctypes
import os

SAVE_DIR = "screenshots"
DRAGGING = False
START_X, START_Y = 0, 0
END_X, END_Y = 0, 0
listener = None  # Biến toàn cục để lưu listener
countdown_window = None

def choose_directory():
    global SAVE_DIR
    SAVE_DIR = filedialog.askdirectory()
    if SAVE_DIR:
        status_label.config(text=f"Thư mục lưu: {SAVE_DIR}")
    else:
        status_label.config(text="Chưa chọn thư mục")

def on_click(x, y, button, pressed):
    global DRAGGING, START_X, START_Y
    if pressed:
        DRAGGING = True
        START_X, START_Y = x, y
    else:
        DRAGGING = False
        start_countdown()
        listener.stop()  # Dừng listener sau khi chọn vùng

def start_countdown():
    global countdown_window
    countdown_window = tk.Toplevel()
    countdown_window.attributes('-topmost', True)
    countdown_window.overrideredirect(True)

    # Đặt cửa sổ đếm ngược ở góc dưới bên phải màn hình
    screen_width = countdown_window.winfo_screenwidth()
    screen_height = countdown_window.winfo_screenheight()
    countdown_window.geometry(f"150x100+{screen_width-170}+{screen_height-120}")

    countdown_label = tk.Label(countdown_window, text="3", font=("Arial", 48), bg="black", fg="white")
    countdown_label.pack(fill=tk.BOTH, expand=True)

    threading.Thread(target=countdown_thread, args=(countdown_label,)).start()

def countdown_thread(label):
    for i in range(2, 0, -1):
        label.config(text=str(i))
        time.sleep(1)

    countdown_window.destroy()
    # Lấy vị trí hiện tại để chụp ảnh
    global END_X, END_Y
    END_X, END_Y = pyautogui.position()
    take_screenshot()

def start_dragging():
    global listener
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    root.withdraw()  # Ẩn cửa sổ khi bắt đầu kéo vùng chụp

def get_active_window_title():
    """Get the title of the currently active window using Windows API directly"""
    if os.name == 'nt':  # Windows
        try:
            user32 = ctypes.windll.user32
            h_wnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(h_wnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(h_wnd, buf, length + 1)
            return buf.value
        except Exception:
            return "Untitled"
    else:  # For non-Windows platforms
        try:
            return pyautogui.getActiveWindow().title
        except:
            return "Untitled"

def take_screenshot():
    try:
        # Get window title using the new function instead of pyautogui.getActiveWindow()
        window_title = get_active_window_title()

        # Use a default title if we couldn't get one
        if not window_title:
            window_title = "Screenshot"

        filename_part = window_title.split(" - ")[0].strip() if " - " in window_title else window_title

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in filename_part)
        filename = f"{sanitized_name}_{timestamp}.png"

        # Ensure SAVE_DIR exists
        Path(SAVE_DIR).mkdir(exist_ok=True)

        # Chụp màn hình vùng từ điểm bắt đầu đến vị trí cuối cùng sau 3 giây
        width = abs(END_X - START_X)
        height = abs(END_Y - START_Y)
        capture_x = min(START_X, END_X)
        capture_y = min(START_Y, END_Y)

        img = pyautogui.screenshot(region=(capture_x, capture_y, width, height))
        save_path = Path(SAVE_DIR) / filename
        img.save(str(save_path))

        # Hiện lại cửa sổ và thông báo
        root.deiconify()
        status_label.config(text=f"Đã chụp và lưu tại: {save_path}", fg="green")
    except Exception as e:
        root.deiconify()
        status_label.config(text=f"Lỗi: {str(e)}", fg="red")

# Cấu hình giao diện
root = tk.Tk()
root.title("Capture Image")
root.geometry("400x300")
root.resizable(True, True)  # Cho phép kéo thả và thay đổi kích thước

# Canvas (giữ lại nhưng không dùng để vẽ trong quá trình chụp)
canvas = tk.Canvas(root, bg="gray", width=400, height=200)
canvas.pack(pady=10)

# Nút chọn thư mục
browse_btn = tk.Button(root, text="Choose folder save", command=choose_directory)
browse_btn.pack(pady=5)

# Nút bắt đầu kéo
start_drag_btn = tk.Button(root, text="Capture", command=start_dragging, bg="lightblue", font=("Arial", 12))
start_drag_btn.pack(pady=5)

# Hiển thị thông báo
status_label = tk.Label(root, text=f"Default Folder: {SAVE_DIR}", fg="blue")
status_label.pack()

root.mainloop()
