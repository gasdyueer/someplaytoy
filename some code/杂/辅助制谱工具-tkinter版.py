import tkinter as tk
from tkinter import filedialog, messagebox
import time
from datetime import datetime
from pynput.keyboard import Listener as KeyboardListener
from pygame import mixer

class AudioKeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Key Logger")
        self.root.geometry("400x300")

        # GUI Components
        self.audio_path_var = tk.StringVar()
        self.output_folder_var = tk.StringVar()

        # Variables
        self.keys_pressed = []
        self.start_time = None
        self.log_file_path = None
        self.recording = False  # 添加 recording 属性

        self.create_widgets()
        self.setup_key_listener()
        self.initialize_mixer()

        # 绑定鼠标点击事件以失去焦点
        self.root.bind("<Button-1>", self.on_click)

    def create_widgets(self):
        # Audio File Input
        tk.Label(self.root, text="Audio File:").pack(pady=5)
        self.audio_path_entry = tk.Entry(self.root, textvariable=self.audio_path_var, width=50)
        self.audio_path_entry.pack(pady=5)

        # Output Folder Input
        tk.Label(self.root, text="Output Folder:").pack(pady=5)
        self.output_folder_entry = tk.Entry(self.root, textvariable=self.output_folder_var, width=50)
        self.output_folder_entry.pack(pady=5)

        # Browse Buttons
        self.browse_audio_button = tk.Button(self.root, text="Browse Audio", command=self.browse_audio)
        self.browse_audio_button.pack(pady=5)

        self.browse_output_button = tk.Button(self.root, text="Browse Output", command=self.browse_output)
        self.browse_output_button.pack(pady=5)

        # Play Button
        self.play_button = tk.Button(self.root, text="Play", command=self.play_audio)
        self.play_button.pack(pady=10)

        # Log Display
        self.log_label = tk.Label(self.root, text="Keyboard Log:", anchor='w', justify='left')
        self.log_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def browse_audio(self):
        audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg")])
        if audio_file:
            self.audio_path_var.set(audio_file)
        self.root.focus()  # 设置焦点到根窗口

    def browse_output(self):
        output_folder = filedialog.askdirectory()
        if output_folder:
            self.output_folder_var.set(output_folder)
        self.root.focus()  # 设置焦点到根窗口

    def setup_key_listener(self):
        self.listener = KeyboardListener(on_press=self.on_key_press)
        self.listener.start()

    def initialize_mixer(self):
        mixer.init()

    def play_audio(self):
        audio_file = self.audio_path_var.get()
        if not audio_file:
            messagebox.showerror("Error", "Please select an audio file.")
            return

        self.keys_pressed = []
        self.start_time = time.time()
        self.recording = True  # 开始录音时设置 recording 为 True

        # Set up the log file path
        output_folder = self.output_folder_var.get() or "."
        self.log_file_path = f"{output_folder}/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        # Clear previous logs
        self.update_log_display("")

        # Load and play the audio
        try:
            mixer.music.load(audio_file)
            mixer.music.play()
            self.check_audio_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {e}")

    def check_audio_status(self):
        if mixer.music.get_busy():
            self.root.after(1000, self.check_audio_status)  # 每秒检查一次
        else:
            self.finish_recording()

    def on_key_press(self, key):
        if self.recording and hasattr(key, 'char') and key.char in 'dfjk':
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            key_info = (key.char, elapsed_time)
            self.keys_pressed.append(key_info)
            self.update_log_display(f"Key: {key.char}, Time: {elapsed_time:.2f}s\n")

    def update_log_display(self, log_text):
        current_text = self.log_label.cget("text")
        self.log_label.config(text=current_text + log_text, anchor='nw', justify='left')

    def finish_recording(self):
        self.recording = False  # 结束录音时设置 recording 为 False
        with open(self.log_file_path, 'w') as f:
            for key, t in self.keys_pressed:
                f.write(f"{key},{t:.2f}\n")
        self.update_log_display("Recording finished. Log saved.\n")

    def on_click(self, event):
        # 如果点击的是 Entry 小部件，则不改变焦点
        if not isinstance(event.widget, tk.Entry):
            self.root.focus()  # 设置焦点到根窗口

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioKeyLoggerApp(root)
    root.mainloop()