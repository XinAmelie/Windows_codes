#!/usr/bin/python3
#coding:utf8
from core.logger import Logger
from core.utils import read_yaml
from config.settings import Settings as ST
import copy
from urllib.parse import urljoin
from requests_toolbelt import MultipartEncoder
from core.apibase import ApiBase
from pageobject.apipage.api_sanmao_login import Sanmao

logger = Logger('api_hr_upload.py').getLogger()
hr_sanmao = read_yaml(ST.UPLOAD_HR)['Hr_Sanmao']




class Up_Files():
    def __init__(self,*args,**kwargs):
        self.api = ApiBase()

    def upload_pic(self,name,files_name,path,type,*args):
        logger.info('开始上传图片')
        up_pic = copy.deepcopy(hr_sanmao['Upload_Pic'])
        url = urljoin(ST.SANMAO_SERVER_FILES, up_pic['url'])
        m = MultipartEncoder(

            fields=[

                (name , (files_name,
                          open(path, "rb"), type)),

            ],
        )

        res = self.api.post(url,data=m,headers={'Content-Type':m.content_type})
        return res.text
    # 利用eval的方法将字符串改为字典的模式
    def assert_ok(self,res,text):
        res_dic = eval(res)
        assert res_dic['msg'] == text,"断言成功:{}".format(res['msg'])
        print('_'*30+str('恭喜你断言成功'),'_'*30)
        logger.info('登录失败:%s'% (res_dic['msg']))


    def up_zl(self,name,files_name,path,type,*args):
        logger.info('开始上传资料')
        up_zl = copy.deepcopy(hr_sanmao['Upload_Zl'])
        url = urljoin(ST.SANMAO_HR_ZL, up_zl['url'])
        cookie1 = up_zl['cookie']
        hr_body = up_zl['body']
        # 自定义参数
        hr_body['name'] = name
        hr_body['filename'] = files_name
        hr_body['path'] = path
        hr_body['type'] = type

        m = MultipartEncoder(

            fields=[

                (name , (files_name,
                          open(path, "rb"), type)),

            ],
        )
        # 资料的传递有点沙雕，不会自己带cookies,需要自己写cookie
        res = self.api.post(url,data=m,headers={'Content-Type':m.content_type,'cookie':cookie1})
        return res.text

    def assert_zl(self,res,text):
        res = eval(res)
        assert  res['msg'] == text,"[断言]: {}".format( res['msg'])
        print('断言成功')
        logger.info('断言失败:{}'.format(res['msg']))



if __name__ == '__main__':
    s = Sanmao()
    res1 = s.login_plat(user = 1406607478, pwd='hrloo.com')
    print(res1)
    U = Up_Files()
    # 图片的上传
    res = U.upload_pic(name='file',files_name='6ca7fdb3-2878-403a-8721-fc41b4ee2429.jpg',path=r'C:\Users\www\Desktop\6ca7fdb3-2878-403a-8721-fc41b4ee2429.jpg',type='image/jpeg')
    print(res)
    # U.assert_ok(res,'请求成功！')

    # 文件资料的上传
    res3 = U.up_zl(name='imgFile',files_name='试卷一主观题.xlsx',path=r'F:\python3.6.8\projects\auto_framework\data_hrzl\hr_zl\试卷一主观题.xlsx',type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    print(res3)
    U.assert_zl(res3,'请求成功！')








