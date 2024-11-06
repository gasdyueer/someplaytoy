import pyautogui as pg
import pynput
from time import sleep
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import time
from PIL import Image, ImageTk

# 设置默认的截图保存目录
default_save_dir = "screenshot"

# 创建Tkinter应用程序窗口
root = tk.Tk()
root.title("Screenshot Taker")

# 变量来存储用户选择的截图保存目录
save_dir_var = tk.StringVar(value=default_save_dir)

# 消息框用于输出程序内的打印结果
message_box = tk.Text(root, height=10, width=50)
message_box.pack(pady=10)


def log_message(message):
    message_box.insert(tk.END, message + "\n")
    message_box.see(tk.END)  # 自动滚动到底部


# 截图并保存
def take_screenshot(key_pos1, real_height=108):
    if not os.path.exists(save_dir_var.get()):
        os.makedirs(save_dir_var.get())
    now = pg.screenshot(region=(
        left_pos, key_pos1.y - real_height, key_pos1.x - left_pos, real_height))
    filename = f"{save_dir_var.get()}/{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.png"
    now.save(filename)
    log_message(f"截图已保存到 {filename}")


# 监听键盘事件
def on_press(key):
    global crosshair_root, is_crosshair_window_open

    try:
        if key.char == 'j':
            pg.click()
        elif key.char == 'k':
            if not is_crosshair_window_open:
                # 记录第一个位置
                key_pos1 = pg.position()
                log_message(f"记录第一个位置: {key_pos1}")

                # 创建全屏窗口显示截图并绘制十字线
                create_crosshair_window(key_pos1)
                is_crosshair_window_open = True  # 标记窗口已打开
            else:
                log_message("截图窗口已打开，请先完成或取消当前截图操作。")
        elif key.char == 'l':
            if is_crosshair_window_open:
                # 关闭现有的截图窗口
                crosshair_root.destroy()
                is_crosshair_window_open = False
                log_message("取消了当前截图操作。")
            else:
                pg.click(button='right')
    except Exception as e:
        log_message(str(e))


# 创建全屏窗口显示截图并绘制十字线
def create_crosshair_window(key_pos1):
    global crosshair_root, crosshair_canvas, screenshot_photo, is_crosshair_window_open, update_crosshair_id

    # 截取屏幕内容
    screenshot = pg.screenshot()

    # 创建全屏窗口
    crosshair_root = tk.Toplevel(root)
    crosshair_root.overrideredirect(True)  # 移除窗口边框
    crosshair_root.wm_attributes('-topmost', 1)  # 确保窗口在最上层

    # 计算屏幕中心位置
    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    # 设置窗口尺寸为屏幕尺寸
    window_width = screen_width
    window_height = screen_height

    # 计算窗口左上角的位置，使其居中
    position_right = int(screen_center_x - window_width / 2)
    position_down = int(screen_center_y - window_height / 2)

    # 设置窗口位置和大小
    crosshair_root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    # 将截图转换为Tkinter兼容的格式
    screenshot_photo = ImageTk.PhotoImage(screenshot)

    # 创建Canvas并在上面放置截图
    crosshair_canvas = tk.Canvas(crosshair_root, width=screen_width,
                                 height=screen_height, highlightthickness=0)
    crosshair_canvas.pack()

    # 绘制初始截图
    crosshair_canvas.create_image(0, 0, anchor=tk.NW, image=screenshot_photo)

    # 更新十字线函数
    def update_crosshair():
        global update_crosshair_id
        if not crosshair_root or not crosshair_root.winfo_exists():
            return  # 如果窗口不存在，则不再更新十字线
        if not crosshair_canvas:
            return  # 如果Canvas不存在，则不再更新十字线
        # 获取当前鼠标位置
        x, y = crosshair_root.winfo_pointerxy()

        # 清除之前的十字线
        crosshair_canvas.delete("crosshair")

        # 绘制新的十字线
        crosshair_canvas.create_line(x, 0, x, screen_height, fill="red",
                                     tags="crosshair")
        crosshair_canvas.create_line(0, y, screen_width, y, fill="red",
                                     tags="crosshair")

        # 每隔一段时间更新十字线
        update_crosshair_id = crosshair_root.after(50, update_crosshair)

    # 开始更新十字线
    update_crosshair_id = crosshair_root.after(50, update_crosshair)

    # 记录第二个位置
    def record_second_position(event):
        global is_crosshair_window_open
        key_pos2 = (event.x, event.y)
        log_message(f"记录第二个位置: {key_pos2}")

        # 关闭全屏窗口
        crosshair_root.destroy()
        is_crosshair_window_open = False  # 重置标记

        # 清除全局变量引用
        global crosshair_canvas, screenshot_photo
        crosshair_canvas = None
        screenshot_photo = None

        # 计算高度差
        pos_minus = abs(key_pos2[1] - key_pos1.y)
        log_message(
            f"目前记录了两个坐标 {key_pos1} 和 {key_pos2}, 坐标差值 {pos_minus}")

        if pos_minus < 50:
            log_message('两次点击距离过近，使用默认高度')
            take_screenshot(key_pos1, real_height=108)
        else:
            log_message('点击距离适中，正在进行截图')
            take_screenshot(key_pos1, real_height=pos_minus)

    # 绑定鼠标点击事件
    crosshair_root.bind('<Button-1>', record_second_position)
    # 绑定鼠标右键取消截图
    crosshair_root.bind('<Button-3>', lambda e: crosshair_root.destroy())

    # 在窗口关闭时取消定时器
    crosshair_root.protocol("WM_DELETE_WINDOW", lambda: crosshair_root.after_cancel(update_crosshair_id))


# 开始监听
def start_listening():
    global listener
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()


# 停止监听
def stop_listening():
    if 'listener' in globals():
        listener.stop()


# 选择截图保存目录
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_dir_var.set(directory)
        log_message(f"截图保存目录已设置为: {directory}")


# 显示帮助信息
def show_help():
    help_text = """
    使用说明：
    1. 点击“开始”按钮启动键盘监听。
    2. 按下 'j' 键进行鼠标左键点击,确定截图
    3. 按下 'k' 键记录当前鼠标位置，并创建一个全屏窗口显示截图并绘制十字线。
       - 在全屏窗口中，你可以通过移动鼠标来查看十字线的位置。
       - 单击鼠标左键（<Button-1>）记录第二个位置，并根据两次点击的位置差值决定截图的高度，然后截取屏幕区域并保存。
       - 单击鼠标右键（<Button-3>）或按下 'l' 键取消截图操作。
    4. 可以通过“选择保存目录”按钮更改截图保存路径。
    5. 点击“停止”按钮结束键盘监听。

    注意事项：
    - 请确保在运行时没有其他程序干扰鼠标和键盘操作。
    - 如果需要更改默认的截图宽度，请修改代码中的 `left_pos` 变量。
    - 截图会自动保存到指定的目录中，文件名包含时间戳。
    - 如果两次点击的距离过近（小于50像素），则使用默认高度108像素进行截图。
    """
    messagebox.showinfo("帮助", help_text)

# 添加使用说明标签
help_label = tk.Label(root, text="点击帮助按钮查看使用说明", fg="blue", cursor="hand2")
help_label.pack(pady=10)
help_label.bind("<Button-1>", lambda e: show_help())

# Tkinter UI元素
start_button = tk.Button(root, text="开始", command=start_listening)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(root, text="停止", command=stop_listening)
stop_button.pack(side=tk.RIGHT, padx=10)

select_dir_button = tk.Button(root, text="选择保存目录",
                              command=select_directory)
select_dir_button.pack(side=tk.BOTTOM, pady=10)

# 初始化屏幕尺寸和鼠标位置
screen_width, screen_height = pg.size()
left_pos = 484

# 初始化变量
key_pos1 = None
key_pos2 = None
is_crosshair_window_open = False  # 标记截图窗口是否已打开
update_crosshair_id = None  # 用于存储定时器ID
crosshair_canvas = None  # 用于存储Canvas引用
screenshot_photo = None  # 用于存储截图引用

# 运行Tkinter主循环
root.mainloop()