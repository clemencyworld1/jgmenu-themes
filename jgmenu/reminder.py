import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
import datetime
import threading
import os

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder App")
        self.reminders = {}

        self.calendar = Calendar(root, selectmode='day', year=2024, month=7, day=12)
        self.calendar.pack(pady=20)

        self.select_btn = tk.Button(root, text="Select Date", command=self.select_date)
        self.select_btn.pack(pady=10)

        self.reminder_text = tk.Entry(root, width=50)
        self.reminder_text.pack(pady=10)

        self.set_reminder_btn = tk.Button(root, text="Set Reminder", command=self.set_reminder)
        self.set_reminder_btn.pack(pady=10)

        self.alarm_file_path = None
        self.select_alarm_btn = tk.Button(root, text="Select Alarm Sound", command=self.select_alarm_sound)
        self.select_alarm_btn.pack(pady=10)

    def select_date(self):
        selected_date = self.calendar.get_date()
        self.reminder_text.delete(0, tk.END)
        self.reminder_text.insert(0, f"Reminder for {selected_date}")

    def set_reminder(self):
        selected_date = self.calendar.get_date()
        reminder_message = self.reminder_text.get()
        if reminder_message:
            self.reminders[selected_date] = reminder_message
            messagebox.showinfo("Reminder Set", f"Reminder set for {selected_date}")
            if self.alarm_file_path:
                # Set reminder time to 9 AM on the selected date
                reminder_time = datetime.datetime.strptime(selected_date, "%m/%d/%y").replace(hour=9, minute=0, second=0)
                delay = (reminder_time - datetime.datetime.now()).total_seconds()
                if delay > 0:
                    threading.Timer(delay, self.show_reminder, args=(selected_date, reminder_message)).start()
                    threading.Timer(delay, self.play_alarm).start()
        else:
            messagebox.showerror("Error", "Please enter a reminder message")

    def select_alarm_sound(self):
        self.alarm_file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
        if self.alarm_file_path:
            messagebox.showinfo("Alarm Sound Selected", f"Selected alarm sound: {self.alarm_file_path}")

    def show_reminder(self, date, message):
        messagebox.showinfo(f"Reminder for {date}", message)

    def play_alarm(self):
        if self.alarm_file_path:
            os.system(f"aplay {self.alarm_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
