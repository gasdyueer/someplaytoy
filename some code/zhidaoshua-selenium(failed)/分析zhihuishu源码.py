# 分析zhihuishu源码
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import requests as rq
from bs4 import BeautifulSoup as bs
import lxml

# 打开网页












# 分析一下这坨狗屎
with open('zhihuishunet.html', 'r', encoding='utf-8') as file:
    content = file.read()

soup = bs(content, 'lxml')
#
print(soup.prettify())
with open('zhihuishunet-prettify.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
# 输出一下右边的目录里边的视频信息

contents1 = soup.find_all('div', class_='cataloguediv-c')


for content in contents1:
    print(content.text)

