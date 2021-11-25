'''自定义扩展工具方法'''
import platform
from collections import Counter
import hashlib

if platform.system() == "Windows":
    separator = "\\"
else:
    separator = "/"


def adjust_path_separator(path_name):
    """转换不同系统下的分隔符"""
    if platform.system() == "Windows":
        path_name = path_name.replace('/', separator)
    else:
        path_name = path_name.replace('\\', separator)
    return path_name


def compare_file_md5(name1, name2):
    """对比文件md5"""
    name1_md5 = hashlib.md5()
    with open(name1, 'rb') as f:
        for line in f:
            name1_md5.update(line)
        name1_md5 = name1_md5.hexdigest()
    name2_md5 = hashlib.md5()
    with open(name2, 'rb') as f:
        for line in f:
            name2_md5.update(line)
        name2_md5 = name2_md5.hexdigest()
    return name1_md5 == name2_md5


def compare(s,t):
    '''比较两个无序列表,元素不能是容器'''
    return Counter(s) == Counter(t)


if __name__ == "__main__":
    s = ['3','2',9]
    t = [9,'2','3']
    res = compare(s,t)
    print(res)