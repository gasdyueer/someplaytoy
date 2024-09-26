# 知到刷课脚本
import os
import time
import webbrowser
import pyautogui as ptg
import pyperclip as pc
from bs4 import BeautifulSoup as b
import lxml
import random
import rpa as r
import requests as rq
import json

# 打开知到刷课网页
os.system('openchrome.bat')
url = 'https://www.zhihuishu.com/'
webbrowser.open(url)
time.sleep(1)
ptg.hotkey('alt', 'f4')
time.sleep(1)


# 然后浏览器最大化
# 有时候已经最大化了

# 登录模块（包含点击与手动滑块验证）
def login():

    try:
        signin_pos = ptg.locateCenterOnScreen('signin.png', confidence=0.7)
    except ptg.ImageNotFoundException:
        pass
    else:
        ptg.click(signin_pos, duration=0.5)
        time.sleep(1)

    signinanniu = ptg.locateCenterOnScreen('signinanniu.png', confidence=0.7)
    ptg.click(signinanniu, duration=0.5)
    time.sleep(1)
    # 滑块验证 技术上可能有点难度，转人工
    OKma = 0
    while True:
        if not OKma:
            print('请手动完成滑块验证')
            OKma = input()

        else:
            print('好了，可以继续了')
            break


# 判断是否需要登录
def is_login():
    try:
        ptg.locateCenterOnScreen('yidenglu.png', confidence=0.7)
        return True
    except ptg.ImageNotFoundException:
        login()
        return True


if is_login():
    print('已经登录')

# 进入同步课堂

try:
    wodexuetang_pos = ptg.locateCenterOnScreen('wodexuetang.png', confidence=0.7)
except ptg.ImageNotFoundException:
    pass
else:
    ptg.click(wodexuetang_pos, duration=0.5)
time.sleep(3)


# 选择课程


def choose_course():
    # 首先大雾
    dawu_pos = ptg.locateCenterOnScreen('dawu.png', confidence=0.7)
    ptg.click(dawu_pos, duration=0.5)
    time.sleep(1)


choose_course()
time.sleep(3)
# 获取当前视频的时长
# 首先获取网址
shoucang_pos = ptg.locateCenterOnScreen('wangzhilan.png', confidence=0.7)
ptg.click(shoucang_pos.x - 30, shoucang_pos.y, duration=0.5)
ptg.hotkey('ctrl', 'c')
url_wangke = pc.paste()
time.sleep(1)


# 然后获取视频时长
# 利用qq识别模块


def qq_ocr():
    time.sleep(2)
    ptg.moveTo(x=1983, y=997, duration=0.5)

    time.sleep(1)
    ptg.hotkey('ctrl', 'alt', 'a')
    time.sleep(1)
    ptg.dragTo(x=2084, y=1022, duration=0.5, button='left')
    time.sleep(1.5)
    shibie_pos = ptg.locateOnScreen('shibie.png', confidence=0.7)
    ptg.moveTo(shibie_pos, duration=0.5)
    ptg.click()
    time.sleep(1)
    ptg.moveTo(shibie_pos.left + 470, shibie_pos.top - 120, duration=0.5)

    ptg.click(clicks=2, button='left', duration=0.1)
    ptg.click(clicks=2, button='left', duration=0.1)
    time.sleep(1)
    ptg.hotkey('ctrl', 'c')

    ptg.hotkey('alt', 'f4')
    return pc.paste()


print(qq_ocr())
