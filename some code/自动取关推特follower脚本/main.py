# 用于删除推特关注者
from time import sleep
import pyautogui as pg


# def delete_followers(i):
#     # 识别删除按钮
#     if i == 0:
#         pos1 = pg.locateOnScreen('icon1.png', confidence=0.8)
#         if pos1:
#             pg.moveTo(pos1)
#             print(pg.position())
#             pg.moveRel(113, 97, duration=0.5)
#             last_pos = pg.position()
#             pg.click()
#             pos2 = pg.locateOnScreen('delete.png', confidence=0.8)
#             if pos2:
#                 pg.moveTo(pos2, duration=0.5)
#                 print(pg.position())
#                 pg.click()
#                 pos3 = pg.locateOnScreen('delete1.png', confidence=0.8)
#                 if pos3:
#                     pg.moveTo(pos3, duration=0.5)
#                     print(pg.position())
#                     pg.click()
#                 return True
#     else:
#         pg.moveTo(last_pos)
#         pg.moveRel(0, 96, duration=0.5)
#         last_pos = pg.position()
#         print(pg.position())
#         pg.click()
#
#         pos2 = pg.locateOnScreen('delete.png', confidence=0.8)
#         if pos2:
#             pg.moveTo(pos2, duration=0.5)
#             print(pg.position())
#             pg.click()
#             pos3 = pg.locateOnScreen('delete1.png', confidence=0.8)
#             if pos3:
#                 pg.moveTo(pos3, duration=0.5)
#                 print(pg.position())
#                 pg.click()
#             return True


def delete_followers():
    # 识别删除按钮
    pos1 = pg.locateOnScreen('icon1.png', confidence=0.8)
    if pos1:
        pg.moveTo(pos1)
        print(pg.position())
        pg.moveRel(113, 97, duration=0.5)
        pg.click()
        pos2 = pg.locateOnScreen('delete.png', confidence=0.8)
        if pos2:
            pg.moveTo(pos2, duration=0.5)
            print(pg.position())
            pg.click()
            pos3 = pg.locateOnScreen('delete1.png', confidence=0.8)
            if pos3:
                pg.moveTo(pos3, duration=0.5)
                print(pg.position())
                pg.click()
            return True
    else:
        print("未找到删除按钮")


# 监听鼠标位置
def mouse_listener():
    pos1 = pg.position()
    while True:
        pos2 = pg.position()
        if pos1 != pos2:
            print(pos2)
            pos1 = pos2


# mouse_listener()


def main():
    sleep(5)
    for i in range(90):
        delete_followers()
        print("第{i+1}次删除")
        sleep(1)
        pg.hotkey('ctrl', 'r')
        sleep(2)


if __name__ == '__main__':
    main()
