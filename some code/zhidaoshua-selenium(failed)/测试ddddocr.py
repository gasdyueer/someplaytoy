# 测试ddddocr
import ddddocr
import cv2

det = ddddocr.DdddOcr(det=False, ocr=False)

with open('target.jpg', 'rb') as f:
    target_bytes = f.read()

with open('bg.jpg', 'rb') as f:
    background_bytes = f.read()

res = det.slide_match(target_bytes, background_bytes)

image = cv2.imread('bg.jpg')
cv2.rectangle(image, (res['target'][0], res['target'][1]), (res['target'][2], res['target'][3]), (0, 0, 255), 2)
cv2.imwrite('bg-rect1.jpg', image)
print(res)
