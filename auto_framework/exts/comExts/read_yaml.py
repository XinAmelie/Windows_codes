 #!/usr/bin/python
# -*- coding:utf-8 -*-

import yaml
import os


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


def read_yaml_group(yamlPath):
    '''读取yaml文件中的多组数据'''
    if not os.path.isfile(yamlPath):
        raise FileNotFoundError("文件路径不存在，请检查路径是否正确：%s" % yamlPath)
    # open方法打开直接读出来
    with open(yamlPath, 'r', encoding='utf-8') as f:
        cfg = f.read()
    content = yaml.load_all(cfg,Loader=yaml.FullLoader)
    # 用load方法转字典
    return content


def write_yaml_group(yamlPath, documents):
    '''写入yaml文件多组数据'''
    if not isinstance(documents,list):
        raise TypeError("数据类型错误，请输入列表数据：%s" % yamlPath)
    with open(yamlPath, 'w', encoding='utf-8') as f:
        yaml.dump(documents=documents, stream=f, allow_unicode=True)


if __name__ == '__main__':
    yamlPath = r'C:\Users\19344\Desktop\AutoCode\auto_framework_v3\exts\picAi\id2name.yaml'
    data = read_yaml(yamlPath)
    print(data)
    from config.settings import Settings as ST
    print(ST.ID2NAME)

