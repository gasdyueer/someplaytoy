import os

# 字母表
alphabet = 'abcdefghijklmnopqrstuvwxyz'
def number_to_alpha(number):
    thenum = number

    # 结果字符串
    result = ''
    while number > 0:
        number, remainder = divmod(number, 26)
        result = alphabet[remainder] + result

    return result, thenum


def fix_alpha(thealpha, thenum, length=3):
    # 根据字母表修改一下
    char_list = [thealpha[i] for i in range(len(thealpha))]
    result = ''
    if thenum % 26 == 0:
        for res in char_list:
            result = result + alphabet[alphabet.index(res) - 1]
    else:
        result = thealpha
        result = result[:-1] + alphabet[alphabet.index(char_list[-1]) - 1]

    if len(result) != 3:
        result = 'a' * (length - len(result)) + result
    return result



def rename_files_in_directory(directory):
    # 获取目录中的所有文件和子文件夹
    for root, dirs, files in os.walk(directory):
        # 对文件进行排序（可选，如果需要按某种顺序处理）
        files.sort()

        # 重命名文件
        for i, old_name in enumerate(files, start=1):
            new_name = fix_alpha(number_to_alpha(i)[0], i) + os.path.splitext(old_name)[1]
            old_path = os.path.join(root, old_name)
            new_path = os.path.join(root, new_name)

            # 重命名文件
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")


# 使用示例
directory_path = r"E:\about-create\saki MAD\manga\92_source - 副本"  # 替换为你的目录路径
rename_files_in_directory(directory_path)


