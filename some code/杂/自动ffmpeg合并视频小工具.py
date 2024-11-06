import os
import subprocess
from tkinter import *
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar
from tqdm import tqdm


class VideoProcessor:
    def __init__(self, master):
        self.master = master
        self.master.title("视频处理器")

        # 文件夹选择按钮
        self.select_folder_button = Button(master, text="选择文件夹",
                                           command=self.select_folder)
        self.select_folder_button.pack()

        # 显示文件列表的文本框
        self.files_textbox = Text(master, height=10, width=50)
        self.files_textbox.pack()

        # 进度条
        self.progress = Progressbar(master, orient=HORIZONTAL, length=300,
                                    mode='determinate')
        self.progress.pack()

        # 执行f1命令按钮
        self.convert_button = Button(master, text="转换视频 (f1)",
                                     command=self.convert_videos)
        self.convert_button.pack()

        # 生成file_list.txt按钮
        self.generate_filelist_button = Button(master, text="生成文件列表",
                                               command=self.generate_filelist)
        self.generate_filelist_button.pack()

        # 显示file_list.txt内容的文本框
        self.filelist_textbox = scrolledtext.ScrolledText(master, height=10,
                                                          width=50)
        self.filelist_textbox.pack()

        # 更新file_list.txt按钮
        self.update_filelist_button = Button(master, text="更新文件列表",
                                             command=self.update_filelist)
        self.update_filelist_button.pack()

        # 执行f2命令按钮
        self.concat_button = Button(master, text="合并视频 (f2)",
                                    command=self.concat_videos)
        self.concat_button.pack()

        self.folder_path = ""
        self.files = []

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.files = [f for f in os.listdir(self.folder_path) if
                          f.endswith(('.mp4', '.avi', '.mkv'))]
            self.files_textbox.delete(1.0, END)
            self.files_textbox.insert(END, "\n".join(self.files))

    def convert_videos(self):
        if not self.files:
            messagebox.showwarning("警告", "没有文件需要处理。")
            return

        total_files = len(self.files)
        self.progress['maximum'] = total_files
        self.progress['value'] = 0

        for i, file_name in enumerate(self.files, start=1):
            input_path = os.path.join(self.folder_path, file_name)
            output_path = os.path.join(self.folder_path, f"temp{i}.mp4")
            command = f'ffmpeg -i "{input_path}" -vf "scale=1920:1080,fps=fps=30" -c:v h264_nvenc -c:a copy "{output_path}"'
            subprocess.run(command, shell=True)
            self.progress['value'] = i
            self.master.update_idletasks()

    def generate_filelist(self):
        filelist_path = os.path.join(self.folder_path, "file_list.txt")
        with open(filelist_path, 'w') as f:
            for i in range(len(self.files)):
                f.write(f"file 'temp{i + 1}.mp4'\n")
        self.update_filelist_textbox(filelist_path)

    def update_filelist_textbox(self, path):
        with open(path, 'r') as f:
            content = f.read()
        self.filelist_textbox.delete(1.0, END)
        self.filelist_textbox.insert(END, content)

    def update_filelist(self):
        filelist_path = os.path.join(self.folder_path, "file_list.txt")
        with open(filelist_path, 'w') as f:
            f.write(self.filelist_textbox.get(1.0, END))

    def concat_videos(self):
        filelist_path = os.path.join(self.folder_path, "file_list.txt")
        output_path = os.path.join(self.folder_path, "output.mp4")
        command = f'ffmpeg -f concat -safe 0 -i "{filelist_path}" -c copy "{output_path}"'
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    root = Tk()
    app = VideoProcessor(root)
    root.mainloop()