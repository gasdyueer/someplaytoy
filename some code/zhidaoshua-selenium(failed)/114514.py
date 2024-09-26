# 这是一个用来学习rpa的项目
import pyautogui as pg
import time

# 在使用屏幕像素时，要像列表索引一样，比如原点坐标是(0,0)，就是从零开始的，那么右下角的坐标就是(屏幕宽度-1,屏幕高度-1)。
# size方法用于获取屏幕的尺寸，返回一个元组(width, height)。
screen_size = pg.size()
list_1 = [screen_size, 114514]
print(list_1)
print(screen_size)

# position方法用于获取鼠标的当前位置，返回一个元组(x, y)。
mouse_pos = pg.position()
print(mouse_pos)

# onScreen方法用于判断某个坐标是否在屏幕上，返回True或False。

print(pg.onScreen(1, 100))

# moveTo方法用于移动鼠标到屏幕上某个绝对坐标，可以指定移动的速度或者说持续时间。

# pg.moveTo(100, 100, duration=0.3)

# moveRel方法用于移动鼠标相对于当前位置移动，可以指定移动的速度或者说持续时间。
# 注意：如果不需要移动某个方向，可以传入0，但如果传入None则表示和另一个方向移动相同的距离。

# pg.moveRel(100, 0, duration=0.3)

# 小测试：实时返回鼠标位置
"""last = pg.position()
try:
    while True:
        current = pg.position()
        if current!= last:
            print(current)
            last = current
except KeyboardInterrupt:
    print("Exiting...")
"""

# 点击鼠标左键,不特别指定坐标x,y则默认点击当前位置
# 不特别指定次数(clicks)则默认单击一次，不特别指定interval则默认0.0秒，不特别指定button则默认左键
# pg.click(x=None, y=None, clicks=1, interval=0.0, button='left')

# 一个小程序，识别图像并点击
time.sleep(2)
# pg.screenshot('foo.png')  # 截图并保存
try:
    while True:
        caidan_pos = pg.locateOnScreen('114.png', confidence=0.9)  # 定位菜单栏
        if caidan_pos:
            break
    time.sleep(1)
    pg.moveTo(caidan_pos, duration=0.5)  # 移动鼠标到菜单栏
    pg.click(caidan_pos)  # 点击菜单栏
    time.sleep(1)
    while True:
        settings_pos = pg.locateOnScreen('shezhi.png', confidence=0.9)  # 定位设置按钮
        if settings_pos:
            break
    time.sleep(1)
    pg.moveTo(settings_pos, duration=0.5)  # 移动鼠标到菜单栏
    pg.click(settings_pos)  # 点击菜单栏
    time.sleep(1)
except pg.ImageNotFoundException:
    print("未能找到图像，请检查屏幕或调整置信度。")
print('程序结束')


