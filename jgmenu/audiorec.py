import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

class AudioScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio and Screen Recorder")
        self.root.geometry("400x250")
        
        # Variables for record settings
        self.filename = tk.StringVar(value="recording")
        self.audio_format = tk.StringVar(value="wav")
        self.video_format = tk.StringVar(value="mkv")
        self.record_mode = tk.StringVar(value="audio")  # Variable to select between audio and screen recording
        
        # UI Elements
        self.create_widgets()
        
        # Recording process
        self.recording_process = None
        
    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TCombobox', font=('Arial', 12))
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Filename entry
        ttk.Label(frame, text="Filename:", style='TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.filename, width=30).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Audio format dropdown
        ttk.Label(frame, text="Audio Format:", style='TLabel').grid(row=1, column=0, sticky=tk.W)
        ttk.Combobox(frame, textvariable=self.audio_format, values=["wav", "mp3", "ogg", "flac", "aac"], width=27, state="readonly").grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Video format dropdown
        ttk.Label(frame, text="Video Format:", style='TLabel').grid(row=2, column=0, sticky=tk.W)
        ttk.Combobox(frame, textvariable=self.video_format, values=["mkv", "mp4", "avi", "mov"], width=27, state="readonly").grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Record mode dropdown
        ttk.Label(frame, text="Mode:", style='TLabel').grid(row=3, column=0, sticky=tk.W)
        ttk.Combobox(frame, textvariable=self.record_mode, values=["audio", "screen"], width=27, state="readonly").grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Record button
        self.record_button = ttk.Button(frame, text="Record", style='TButton', command=self.toggle_recording)
        self.record_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Configure grid
        frame.columnconfigure(1, weight=1)
        
    def toggle_recording(self):
        if self.recording_process:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        filename = self.filename.get()
        audio_format_option = self.audio_format.get()
        video_format_option = self.video_format.get()
        
        if self.record_mode.get() == "audio":
            audio_filename = f"{filename}_audio.{audio_format_option}"
            
            # Use ffmpeg to record audio from default ALSA device
            audio_command = [
                "ffmpeg", "-y",
                "-f", "alsa", "-ac", "2", "-i", "default",  # Record from default ALSA device (stereo)
                "-vn", "-acodec", "copy", audio_filename  # Copy audio codec directly
            ]
            self.recording_process = subprocess.Popen(audio_command)
            self.record_button.config(text="Stop", style='TButton')
        
        elif self.record_mode.get() == "screen":
            audio_filename = f"{filename}_audio.{audio_format_option}"
            video_filename = f"{filename}_video.{video_format_option}"
            combined_filename = f"{filename}.{video_format_option}"
            
            # Record audio from default ALSA device
            audio_command = [
                "ffmpeg", "-y",
                "-f", "alsa", "-ac", "2", "-i", "default",  # Record from default ALSA device (stereo)
                "-vn", "-acodec", "copy", audio_filename  # Copy audio codec directly
            ]
            self.recording_process = subprocess.Popen(audio_command)
            
            # Record screen using ffmpeg
            video_command = [
                "ffmpeg", "-y",
                "-video_size", "1920x1080", "-framerate", "25",
                "-f", "x11grab", "-i", ":0.0", video_filename
            ]
            self.recording_process = subprocess.Popen(video_command)
            
            self.record_button.config(text="Stop", style='TButton')
            
            self.audio_filename = audio_filename
            self.video_filename = video_filename
            self.combined_filename = combined_filename
    
    def stop_recording(self):
        if self.recording_process:
            self.recording_process.terminate()
            self.recording_process = None
        
        if self.record_mode.get() == "screen":
            # Combine audio and video using ffmpeg
            combine_command = [
                "ffmpeg", "-y",
                "-i", self.video_filename,
                "-i", self.audio_filename,
                "-c:v", "copy", "-c:a", "aac",
                self.combined_filename
            ]
            subprocess.run(combine_command)
            os.remove(self.audio_filename)
            os.remove(self.video_filename)
            messagebox.showinfo("Info", f"Recording saved as {self.combined_filename}")
        
        else:
            messagebox.showinfo("Info", f"Recording saved as {self.filename.get()}_{self.record_mode.get()}.{self.audio_format.get()}")
        
        self.record_button.config(text="Record", style='TButton')

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioScreenRecorderApp(root)
    root.mainloop()
