# 读图片
import pyautogui as pg
import time
pic = '114.png'
while True:
    try:
        nm = pg.locateOnScreen(pic, confidence=0.5)
        if nm:
            print('找到了')
            pg.moveTo(nm, duration=0.5)
            pg.click()
            time.sleep(1)
            break
        else:
            print('没找到')

    except Exception:
        print('出错了')

        break


