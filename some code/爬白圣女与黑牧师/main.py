import requests as rq
from bs4 import BeautifulSoup as bs
import re
import lxml
from time import sleep
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

# 老样子，爬个源代码看看
manga_page_url = 'http://www.92mh.com/manhua/382/{}.html'
manga_dirpage = 'http://www.92mh.com/manhua/381/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def get_max_page(url):
    options = wd.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--start-maximized')  # 最大化窗口
    driver = wd.Chrome(options=options)
    driver.get(url)  # 替换为你需要访问的网址
    driver.implicitly_wait(10)  # 等待10秒，直到页面加载完毕
    sleep(1)  # 等待1秒，等待图片加载完毕
    # 获取最大页数
    pic1 = driver.page_source
    driver.quit()
    pic_soup1 = bs(pic1, 'lxml')
    max_page = pic_soup1.find('select')
    values = []
    if max_page:
        for option in max_page.find_all('option'):
            values.append(option.get('value'))
    return values, pic_soup1

def download_image(img_url, img_name, j):
    while True:
        try:
            _, soup1 = get_max_page(img_url)
            img1_url = soup1.find('div', id='images')
            src = img1_url.img.get('src')
            print(f"{img_name}的第{j}页链接为{img_url}")
            print(f"{img_name}的第{j}页图片链接为{src}")
            # 下载图片
            img_content = rq.get(src, headers=headers, timeout=10)
            with open(f"{j}.jpg", 'wb') as f:
                f.write(img_content.content)
            # 校验图片是否下载成功
            if os.stat(f"{j}.jpg").st_size == 0:
                os.remove(f"{j}.jpg")
                continue
            # 转移到指定文件夹
            if not os.path.exists(f"{img_name}/{j}.jpg"):
                shutil.move(f"{j}.jpg", f"{img_name}/{j}.jpg")
            print(f"{img_name}的第{j}页图片保存成功")
        except Exception as e:
            print(f"图片{img_name}链接获取失败，错误信息: {e}")
        else:
            break

def main():
    content_list = rq.get(manga_dirpage, headers=headers)
    content_soup = bs(content_list.content, 'lxml')
    links = content_soup.find_all('a', href=re.compile(r'http://www.92mh.com/manhua/381/\d+.html'))

    for i in range(len(links)):
        # if i < 4:
        #     continue
        print(f'正在爬第{i+1}话')
        page_url = links[i].get('href')
        img_name = links[i].text.strip()
        # 新建文件夹
        if not os.path.exists(img_name):
            os.mkdir(img_name)

        # 先用selenium获取页数列表
        while True:
            suffix, _ = get_max_page(page_url)
            print(suffix)
            if suffix:
                break
            else:
                print("获取页数失败，正在重试")

        # 使用线程池并行下载图片
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for j in range(1, len(suffix) + 1):
                img_url = f"{page_url}?p={j}"
                futures.append(executor.submit(download_image, img_url, img_name, j))

            for future in as_completed(futures):
                future.result()

if __name__ == "__main__":
    main()
    