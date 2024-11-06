import pyautogui as pg
from time import sleep
import pyperclip


def get_mouse_position():
    pos1 = pg.position()
    while True:
        pos2 = pg.position()
        if pos1 != pos2:
            print(pos2)
            pos1 = pos2

def match_image():
    # 循环匹配图片直到找到完成信息
    while True:
        try:
            if pg.locateCenterOnScreen("D:\\my Code\\py\\测试各种东西\\测试代码\\正在ASR.png", confidence=0.8):
                print('正在ASR')
                sleep(240)
            elif pg.locateCenterOnScreen("D:\\my Code\\py\\测试各种东西\\测试代码\\ASR完成.png", confidence=0.8):
                print('翻译完成')
                return True
        except Exception as e:
            print(e)
            pass



def execute_translation(num):
    # 改路径
    pg.click(627, 691, duration=0.5)
    pg.click()
    pg.click()
    pg.click()
    sleep(1)

    pg.hotkey('delete')
    pg.typewrite('E:\AI\GPT-SoVITS\GPT-SoVITS-v2-240807\output\slicer_opt sort\group_'+str(num))

    pg.click(2087,826, duration=0.5)

sleep(2)
for i in range(24):
    print('第'+str(i+1)+'组')
    i += 4
    execute_translation(i)
    sleep(250)
    print('翻译完成')



