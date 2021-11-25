#!/usr/bin/python3
#coding:utf8
import pytest
from pageobject.apipage.api_hr_upload import Up_Files
from config.settings import Settings as ST
import os


data_hrzl = ST.DATA_ZL

data_pic = os.path.join(data_hrzl,'hr_pic','d76c1d9ad54f43929fd96a58058c18d1!400x400.png')
print(data_pic)
data_zl = os.path.join(data_hrzl,'hr_zl','试卷一主观题.xlsx')
print(data_zl)



class Test_Sanmao():
    '''三茅网站接口'''
    @pytest.mark.usefixtures('login_forward')
    def test_upload_pic(self):
        '''上传图片'''
        # s = Sanmao()
        # res1 = s.login_plat(user=1103028621, pwd='hrloo.com')
        # print(res1)
        U = Up_Files()
        res = U.upload_pic(name='file', files_name='d76c1d9ad54f43929fd96a58058c18d1!400x400.png',
                           path=data_pic, type='image/jpeg')
        # print(type(res))
        # 利用eval()方法，可以将字典格式的字符串转换为字典
        print(res)
        # print(res.json())
        # dic = eval(res)
        # print(type(dic))

    @pytest.mark.usefixtures('login_forward')
    def test_upload_zl(self):
        '''上传资料'''
        null = None
        # 因为接口返回了null,偏偏python识别不到。所以定义下
        U = Up_Files()
        res3 = U.up_zl(name='imgFile', files_name='试卷一主观题.xlsx',
                       path=data_zl,
                       type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        print(res3)
        print(type(res3))
        zl_dict = eval(res3)
        print(type(zl_dict))
        # 利用eval()方法，可以将字典格式的字符串转换为字典


