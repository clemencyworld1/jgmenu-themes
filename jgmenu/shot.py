#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess
from datetime import datetime

# Create the Tkinter app
class ScreenshotApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x300")
        self.window.resizable(0, 0)
        self.window.title("Screenshot App")

        # Apply a modern theme
        style = ttk.Style(self.window)
        style.configure('TFrame', background='#2E2E2E')
        style.configure('TLabel', background='#2E2E2E', foreground='white', font=('Helvetica', 12))
        style.configure('TButton', background='#2E2E2E', foreground='white', font=('Helvetica', 12), relief='flat', padding=(10, 5))
        style.configure('TScale', background='#2E2E2E')
        style.map('TButton', background=[('active', '#5E5E5E')])

        self.create_ui()

    def create_ui(self):
        frame = ttk.Frame(self.window, padding="20 20 20 20")
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        label = ttk.Label(frame, text="Custom Filename (optional):")
        label.pack(pady=10)

        self.filename_entry = ttk.Entry(frame)
        self.filename_entry.pack(pady=10, padx=20, fill=tk.X)

        button = ttk.Button(frame, text="Take Screenshot", command=self.take_screenshot)
        button.pack(pady=20)

    def take_screenshot(self):
        pictures_dir = os.path.expanduser("~/Pictures")
        if not os.path.exists(pictures_dir):
            os.makedirs(pictures_dir)

        custom_filename = self.filename_entry.get().strip()
        if custom_filename:
            filename = os.path.join(pictures_dir, custom_filename + ".png")
        else:
            timestamp = datetime.now().strftime('%I:%M:%S_grim.png')
            filename = os.path.join(pictures_dir, timestamp)

        command = f"import {filename}"

        try:
            subprocess.run(command, shell=True, check=True)
            self.show_message(f"Screenshot saved as {filename}", "Success")
        except subprocess.CalledProcessError as e:
            self.show_message(f"Error taking screenshot: {e}", "Error")

    def show_message(self, message, title):
        messagebox.showinfo(title, message)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ScreenshotApp()
    app.run()
