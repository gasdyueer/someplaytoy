import pyautogui as pg
import pyperclip as pc
import pynput
from time import sleep
# 有两个方案，一个是采用截图然后丢给umiocr识别完再拼接
# 另一个是直接用pyautogui来模拟键盘输入与鼠标点击，直接获取文本

# 这里只实现方案一


# 截图并保存到当前目录的“screenshot”文件夹下
# 先获取一个特别的坐标
left_pos = 484
height = 106
def get_screenshot_and_save(key_pos1, real_height=106):
    # 图片以时间戳命名
    import time
    now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    pg.screenshot(region=(left_pos, key_pos1.y-real_height, key_pos1.x-left_pos, real_height)).save(f"screenshot/{now}.png")


# 通过监听鼠标点击获取和返回坐标，进行两次然后做差运算，得到坐标差值
def get_mouse_click_position():


    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    with pynput.mouse.Listener(on_move=on_move,) as listener:
        listener.join()


def execute_it():
    def char(key):
        try:
            print(key.char)
            if key.char == 'j':
                pg.click()
            elif key.char == 'k':
                key_pos1 = pg.position()
                sleep(1)
                key_pos2 = pg.position()
                # 两次点击的坐标差值的绝对值
                pos_minus = abs(key_pos2.y - key_pos1.y)
                print('目前记录了两个坐标',key_pos1,'',key_pos2,'坐标差值',pos_minus)
                if pos_minus < 50:
                    print('两次点击距离过近，也就是使用默认高度')
                    get_screenshot_and_save(key_pos1, real_height=106)
                    print('截图已保存')
                else:
                    print('点击距离适中，正在进行截图')
                    get_screenshot_and_save(key_pos1, real_height=pos_minus)
                    print('截图已保存')

        except Exception as e:
            print(e)
    with pynput.keyboard.Listener(on_press=char) as listener:
        listener.join()


# get_mouse_click_position()
execute_it()
