#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

# Define the path to the brightness file
BRIGHTNESS_FILE = '/sys/class/backlight/intel_backlight/brightness'
MAX_BRIGHTNESS_FILE = '/sys/class/backlight/intel_backlight/max_brightness'

def read_brightness():
    """Read the current brightness value from the file."""
    try:
        with open(BRIGHTNESS_FILE, 'r') as file:
            return int(file.read().strip())
    except IOError as e:
        messagebox.showerror("Error", f"Unable to read brightness: {e}")
        return 0

def read_max_brightness():
    """Read the maximum brightness value from the file."""
    try:
        with open(MAX_BRIGHTNESS_FILE, 'r') as file:
            return int(file.read().strip())
    except IOError as e:
        messagebox.showerror("Error", f"Unable to read max brightness: {e}")
        return 100

def set_brightness(value):
    """Set the brightness to the specified value."""
    try:
        with open(BRIGHTNESS_FILE, 'w') as file:
            file.write(str(int(value)))
    except IOError as e:
        messagebox.showerror("Error", f"Unable to set brightness: {e}")

def update_brightness(value):
    """Update the brightness based on the slider value."""
    set_brightness(int(float(value)))

def set_xrandr_brightness(value):
    brightness = float(value) / 100
    subprocess.call(['xrandr', '--output', 'eDP-1', '--brightness', str(brightness)])

def debounce(func, wait):
    from threading import Timer
    def debounced(*args, **kwargs):
        def call_it():
            func(*args, **kwargs)
        if hasattr(debounced, '_timer'):
            debounced._timer.cancel()
        debounced._timer = Timer(wait, call_it)
        debounced._timer.start()
    return debounced

# Initialize gamma values
gamma_r, gamma_g, gamma_b = 1.0, 1.0, 1.0

def apply_gamma():
    subprocess.call(['xrandr', '--output', 'eDP-1', '--gamma', f'{gamma_r}:{gamma_g}:{gamma_b}'])

debounced_apply_gamma = debounce(apply_gamma, 0.1)

def set_gamma_r(value):
    global gamma_r
    gamma_r = float(value)
    debounced_apply_gamma()

def set_gamma_g(value):
    global gamma_g
    gamma_g = float(value)
    debounced_apply_gamma()

def set_gamma_b(value):
    global gamma_b
    gamma_b = float(value)
    debounced_apply_gamma()

# Exit application when focus is lost
def on_focus_out(event):
    root.quit()

# Center the window on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Create the main application window
root = tk.Tk()
root.title("Brightness and Gamma Controller")

# Apply a modern theme
style = ttk.Style(root)
style.configure('TFrame', background='#2E2E2E')
style.configure('TLabel', background='#2E2E2E', foreground='white', font=('Helvetica', 12))
style.configure('TButton', background='#2E2E2E', foreground='white', font=('Helvetica', 12), relief='flat', padding=(10, 5))
style.configure('TScale', background='#2E2E2E')
style.map('TButton', background=[('active', '#5E5E5E')])

# Remove window borders
root.overrideredirect(True)

# Exit on lose focus
root.bind("<FocusOut>", on_focus_out)

# Read the current and maximum brightness levels
current_brightness = read_brightness()
max_brightness = read_max_brightness()

# Create a frame for the sliders and labels
frame = ttk.Frame(root, padding=(20, 20, 20, 20))
frame.pack(pady=20, padx=20)

# Create sliders and labels
def create_slider(frame, label_text, from_, to, command, initial_value):
    row_frame = ttk.Frame(frame)
    row_frame.pack(fill='x', pady=10)
    
    label = ttk.Label(row_frame, text=label_text)
    label.pack(side='left', padx=10)
    
    slider = ttk.Scale(row_frame, from_=from_, to=to, orient=tk.HORIZONTAL, length=300, command=command)
    slider.set(initial_value)
    slider.pack(side='right')
    
    return slider

# Brightness slider (File)
create_slider(frame, "Brightness (File)", 0, max_brightness, update_brightness, current_brightness)

# Brightness slider (xrandr)
create_slider(frame, "Brightness (xrandr)", 0, 100, set_xrandr_brightness, 100)

# Gamma sliders
create_slider(frame, "Gamma Red", 0.1, 3.0, set_gamma_r, 1.0)
create_slider(frame, "Gamma Green", 0.1, 3.0, set_gamma_g, 1.0)
create_slider(frame, "Gamma Blue", 0.1, 3.0, set_gamma_b, 1.0)

# Create an Exit button
exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

# Center the window on the screen
center_window(root)

# Start the GUI event loop
root.mainloop()
