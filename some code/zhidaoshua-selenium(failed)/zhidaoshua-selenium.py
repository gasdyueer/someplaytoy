# 使用selenium进行自动化测试
import requests as rq
import random as r
import pyperclip as pc
import cv2
import numpy as np
from time import sleep
import ddddocr as ddd
import pyautogui as pg
import selenium as se
from selenium import webdriver as wd
from selenium.webdriver.common.by import By

# 最大化打开浏览器与网页

wd_options = wd.ChromeOptions()
wd_options.add_argument("--start-maximized")
url = 'https://www.zhihuishu.com/'
wd = wd.Chrome(options=wd_options)
wd.get(url)
wd.implicitly_wait(10)

# 进入登录界面
login_elements = wd.find_element(By.CSS_SELECTOR, '[href="https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin"]')
login_elements.click()


# 输入用户名密码
phonenumber = ''
password = ''
phonenumber_element = wd.find_element(By.ID, 'lUsername')
phonenumber_element.send_keys(phonenumber)
sleep(1)
password_element = wd.find_element(By.ID, 'lPassword')
password_element.send_keys(password)
sleep(1)

# 点击登录按钮
login_button = wd.find_element(By.CSS_SELECTOR, '.wall-sub-btn')
login_button.click()

sleep(2)


# 先是下载图片模块


def download_img(url1, filename):
    response = rq.get(url1)
    with open(filename, 'wb') as f1:
        f1.write(response.content)
    print('图片保存成功')


targetimgname = 'target.jpg'
targetimgurl = wd.find_element(By.CSS_SELECTOR, '[alt="验证码滑块"]').get_attribute('src')
bgimgname = 'bg.jpg'
bgimgurl = wd.find_element(By.CSS_SELECTOR, '[alt="验证码背景"]').get_attribute('src')
download_img(bgimgurl, bgimgname)
download_img(targetimgurl, targetimgname)
# 滑块验证-得到滑块缺口的位置
det = ddd.DdddOcr(det=False, ocr=False)

with open(targetimgname, 'rb') as f:
    target_bytes = f.read()

with open(bgimgname, 'rb') as f:
    background_bytes = f.read()

res = det.slide_match(target_bytes, background_bytes)
print(res)
x1, y1, x2, y2 = res['target']
# 然后定位需要移动的滑块位置


def move_slider():
    sleep(2)
    slider = 'slider.png'
    slider_pos = pg.locateOnScreen(slider, confidence=0.7)
    pg.moveTo(slider_pos, duration=0.5)
    sleep(2)


move_slider()
# 确定缺口准确位置
def judge_random(x):
    if 0 < x < 100:
        randomnum = r.randint(20, 30)
        return randomnum
    if 100 < x < 200:
        randomnum = r.randint(130, 140)
        return randomnum
    if 200 < x < 320:
        randomnum = r.randint(110, 120)
        return randomnum
randomnum = judge_random(x1)
real_x = x1 - 30
print(x1, randomnum, real_x)
# 自制高斯补间函数


def interpolate(value):
    """
    补间函数，根据输入值返回处理后的结果。

    参数:
    value -- 输入的浮点数值

    返回:
    处理后的浮点数值。
    """

    # 定义变化幅度
    amplitude = 0.1
    print('输入值：', value)
    # 检查输入值是否为0.0或1.0
    if value in [0.0, 1.0]:
        return value
    else:
        # 对于0.1到0.9之间的值，进行随机处理
        # 生成一个 [-amplitude, amplitude] 范围内的随机浮点数
        random_offset = np.random.uniform(-amplitude, amplitude)
        # 计算处理后的值，并确保它在0.0到1.0之间
        processed_value = value + random_offset
        processed_value = max(0.0, min(processed_value, 1.0))
        print('处理后的值：', processed_value)
        return processed_value


# 开始模拟拖动滑块
pg.dragRel(real_x, 0, duration=2, tween=interpolate)

# 检测成功没
count = 0
while True:
    if count < 3:
        try:
            pg.locateCenterOnScreen('check1.png', confidence=0.7)
        except Exception:
            print('未检测到登录成功,正在重试')
            move_slider()
            pg.dragRel(real_x, 0, duration=3, tween=interpolate)

        else:
            print('登录成功,美美刷课了家人们')
            break
        count += 1
    else:
        print('请手动进行滑块验证，完成后请输入1继续')
        wc = input('输入1继续\n')
        if wc == '1':
            break







# 草泥马，终于可以写其他模块了
# 选择课程
class_name = wd.find_element(By.CSS_SELECTOR, '#sharingClassed > div:nth-child(2) > ul > div > dl > dt > div.item-left-course > div.courseName')
classname = class_name.text
viwepocess = wd.find_element(By.CSS_SELECTOR, '.processNum').text
print(f"当前课程：{classname}，当前进度：{viwepocess}")
print(f"正在进入{classname}课程")
class_name.click()
# 检测是否有神必的学前导读弹窗


def check_guidepopwin():
    try:
        pos = pg.locateCenterOnScreen('popup window1.png', confidence=0.7)
    except pg.ImageNotFoundException:
        print('未检测到弹窗')
        return False
    else:
        pg.moveTo(pos, duration=0.5)
        pg.moveRel(272, 225, duration=0.5)
        pg.click()
        check_guidepopwin()
        return True

sleep(4)
if check_guidepopwin():
    print('检测到傻卵弹窗，已击毙')
    pg.click()

# 时间累计模块
current_total_time = 0
def time_accumulation(time):
    # 提取当前视频的总时长
    total_time = wd.find_element(By.CSS_SELECTOR, '.totalTime').text


input('输点东西关闭')
