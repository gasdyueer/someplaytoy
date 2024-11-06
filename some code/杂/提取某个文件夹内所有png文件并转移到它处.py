# 转移png文件到所在文件夹
import os
import shutil
import re

# 用户输入文件夹路径
source_path = input("\n请输入文件夹路径：")
destination_path = input("\n请输入目标文件夹路径：")
filetype = input("\n请输入文件类型：")
# 遍历文件夹，查找特定类型文件
for root, dirs, files in os.walk(source_path):
    for file in files:
        if file.endswith("." + filetype):
            # 找到png文件，将其复制到另一个文件夹
            shutil.copy(os.path.join(root, file), destination_path)
            # 打印文件路径
            print(os.path.join(root, file))

# 打印提示信息
print("文件已全部转移到所在文件夹！")
input("按任意键退出...")
