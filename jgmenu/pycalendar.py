import tkinter as tk
from tkcalendar import Calendar

def on_ok():
    root.destroy()

root = tk.Tk()
root.title("Simple Calendar")

# Set the predefined position (e.g., 300x300) and size (e.g., 400x400)
root.geometry("250x270+1650+760")

# Remove window borders
root.overrideredirect(True)

# Create the calendar widget with minimized padding
cal = Calendar(root, selectmode='day', year=2024, month=7, day=12, borderwidth=0, highlightthickness=0)
cal.pack(fill="both", expand=True)

# Create the OK button with no border
ok_button = tk.Button(root, text="OK", command=on_ok, borderwidth=0, highlightthickness=0)
ok_button.pack(fill="x")

root.mainloop()
