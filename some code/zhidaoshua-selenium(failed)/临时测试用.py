import requests as rq
import pyautogui as pg
from time import sleep
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import rpa as r
def qqocr():
    sleep(5)
    pos1 = pg.locateOnScreen('pos1.png', confidence=0.7)
    pg.moveTo(pos1)
    print(pg.position())
    print(pos1)
    pos2 = pg.locateOnScreen('pos2.png', confidence=0.7)
    pg.moveTo(pos2)
    print(pg.position())
    sleep(2)
    pg.hotkey('ctrl', 'alt', 'a')
    sleep(1)
    pg.dragTo(pos1, duration=0.5, button='left')
    sleep(1.5)
    shibie_pos = pg.locateOnScreen('shibie.png', confidence=0.7)
    pg.moveTo(shibie_pos, duration=0.5)
    pg.click()
    sleep(1)

    pg.moveTo(shibie_pos.left + 470, shibie_pos.top - 120, duration=0.5)
    pg.click(clicks=2, button='left', duration=0.1)
    pg.click(clicks=2, button='left', duration=0.1)
    sleep(1)
    pg.hotkey('ctrl', 'c')


# r.init()
# print(r.read('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[1]/div/ul[1]/div[1]/li/div[1]/div/i/span'))
# r.close()


# 测试selenium抓取图片链接
# wd_options = wd.ChromeOptions()
# wd_options.add_argument("--start-maximized")
# url = 'https://www.zhihuishu.com/'
# wd = wd.Chrome(options=wd_options)
# wd.get(url)
# wd.implicitly_wait(10)


# 图片的URL地址

image_url = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'

# 发起GET请求
response = rq.get(image_url)

# 检查请求是否成功
if response.status_code == 200:
    # 图片保存的路径
    file_path = 'downloaded_image.jpg'

    # 打开一个文件用于写入
    with open(file_path, 'wb') as file:
        # 将响应的内容写入文件
        file.write(response.content)
    print(f'图片已下载并保存为：{file_path}')
else:
    print(f'图片下载失败，状态码：{response.status_code}')
