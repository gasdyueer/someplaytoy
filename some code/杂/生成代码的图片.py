import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
import io

def select_input_file():
    file_path = filedialog.askopenfilename(
        title="选择Python文件",
        filetypes=(("Python files", "*.py"), ("All files", "*.*"))
    )
    if file_path:
        input_file_var.set(file_path)

def select_output_dir():
    dir_path = filedialog.askdirectory(
        title="选择图片导出路径"
    )
    if dir_path:
        output_dir_var.set(dir_path)

def convert_to_image():
    input_file = input_file_var.get()
    output_dir = output_dir_var.get()

    if not input_file or not output_dir:
        messagebox.showwarning("警告", "请先选择输入文件和输出目录！")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    formatter = ImageFormatter(style='default', line_numbers=True, font_name='DejaVu Math TeX Gyre')
    image_data = pygments.highlight(code, PythonLexer(), formatter)

    # 将图片数据加载到 PIL 图像对象
    image = Image.open(io.BytesIO(image_data))

    # 保存图片
    output_file = f"{output_dir}/{input_file.split('/')[-1].replace('.py', '.png')}"
    image.save(output_file)

    messagebox.showinfo("成功", f"代码图片已生成：{output_file}")

# 创建主窗口
root = tk.Tk()
root.title("Python代码转图片工具")

# 设置样式
style = ttk.Style(root)
style.theme_use('clam')

# 输入文件路径
input_file_var = tk.StringVar(value="")
ttk.Label(root, text="选择Python文件:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=input_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(root, text="浏览...", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

# 输出目录路径
output_dir_var = tk.StringVar(value="")
ttk.Label(root, text="选择图片导出路径:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=output_dir_var, width=50).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(root, text="浏览...", command=select_output_dir).grid(row=1, column=2, padx=5, pady=5)

# 转换按钮
ttk.Button(root, text="转换为图片", command=convert_to_image).grid(row=2, column=0, columnspan=3, pady=10)

# 启动GUI
root.mainloop()
