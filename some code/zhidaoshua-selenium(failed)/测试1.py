# 使用captcha-recognizer库识别验证码
from captcha_recognizer.recognizer import Recognizer as Re
import cv2
import numpy as np

# 传入图片路径
img = 'bg.jpg'
box, confidence = Re().identify_gap(source=img, verbose=True)

print(f'缺口坐标: {box}')
print(f'可信度: {confidence}')



def remove_black_border(img):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh,  1, 2)
    x, y, w, h = cv2.boundingRect(contours[0])
    cropped_img = image[y:y+h, x:x+w]
    return cropped_img
def find_gap_position(bg_img, jigsaw_img):
    bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
    jigsaw_gray = cv2.cvtColor(jigsaw_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(bg_gray, jigsaw_gray, cv2.TM_CCOEFF_NORMED)
    _, _, _, (x, _) = cv2.minMaxLoc(result)
    return x


# 试一试

def find_gap_position(bg_img, jigsaw_img):
    img = cv2.imread('bg.jpg', cv2.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                              param1=50, param2=30, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imshow('detected circles', cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 操了


# 读取图像
image = cv2.imread('bg.jpg', cv2.IMREAD_GRAYSCALE)

# 定义模糊规则
def is_edge(pixel, threshold=200):
    # 假设“边缘”是亮度值超过阈值的像素
    return pixel > threshold

# 应用模糊规则
def detect_gaps(image, threshold=200):
    edges = np.zeros_like(image)
    for i in range(1, image.shape[0]):
        for j in range(1, image.shape[1]):
            # 检查当前像素是否为边缘
            if is_edge(image[i, j], threshold):
                # 检查周围的像素是否不是边缘
                if not is_edge(image[i-1, j], threshold) and \
                   not is_edge(image[i+1, j], threshold) and \
                   not is_edge(image[i, j-1], threshold) and \
                   not is_edge(image[i, j+1], threshold):
                    edges[i, j] = 255
    return edges


# 检测图像中的缺口
gaps = detect_gaps(image, 200)

# 显示结果
cv2.imshow('Gaps', gaps)
cv2.waitKey(0)
cv2.destroyAllWindows()
