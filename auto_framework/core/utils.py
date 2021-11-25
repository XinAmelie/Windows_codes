import platform
import hashlib
import json
# from ruamel.yaml import YAML
import yaml
import os

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


def md5_sum(name):
    """计算文件md5"""
    md5sum = hashlib.md5()
    with open(name, 'rb') as f:
        for line in f:
            md5sum.update(line)
        md5sum = md5sum.hexdigest()
    return md5sum


def read_json(jsonPath):
    """
        从json中获取数据
        json_name: 绝对路径
    """
    if not os.path.isfile(jsonPath):
        raise FileNotFoundError("文件路径不存在，请检查路径是否正确：%s" % jsonPath)
    with open(jsonPath, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data


def read_yaml(yamlPath):
    '''读取yaml文件内容
    realPath: 文件的真实绝对路径 '''
    if not os.path.isfile(yamlPath):
        raise FileNotFoundError("文件路径不存在，请检查路径是否正确：%s" % yamlPath)
    # open方法打开直接读出来
    with open(yamlPath, 'r', encoding='utf-8') as f:
        cfg = f.read()
    content = yaml.load(cfg,Loader=yaml.FullLoader)
    # 用load方法转字典
    return content


def write_yaml(yamlPath, data):
    '''写入yaml文件单组数据'''
    with open(yamlPath, 'w', encoding='utf-8') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


def init_pic_path(pic_path):
    """遍历目录下所有层级获取所有图片的路径"""
    path = {}
    path_lists = [ path_list for path_list in os.walk(pic_path) ]
    for path_list in path_lists:
        for file_path in path_list:
            if isinstance(file_path, str):
                value = file_path
            elif isinstance(file_path, list):
                for file_name in file_path:
                    path[file_name.split('.')[0]] = os.path.join(value, file_name)
    return path


if __name__ == "__main__":
    # res = read_yaml('./democases.yaml')
    # print(res)
    d = {}
    d['a']['b'] = 'c'
    print(d)
