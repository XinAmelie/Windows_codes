#!/usr/bin/python3
#coding:utf8
from core.utils import read_yaml
from config.settings import Settings as ST
from core.guibase import GuiBase
from pageobject.webpage.sanmao_login import login_sanmao
import time
from pageobject.webpage.affard_ordeid import Buy_Course
from pageobject.webpage.za_jindan import process_enter
from pageobject.webpage.write_article_sanmao import Write_Ariticle
from pageobject.webpage.web_sanmao import Sanmao_Chat



webInfo = read_yaml(ST.WEBINFO)['sanmao']

pro = process_enter()

import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_NONE')



# 三茅聊天
sanmao_chat = Sanmao_Chat()


# 正则
# filter:progid:DXImageTransform.Microsoft.Alpha(Opacity=30);
# hd_msg_settings: (.+?),

# crsf = re.findall(" filter: \'progid:DXImageTransform.Microsoft.Alpha(Opacity=30)\'  hd_msg_settings: \'(.+?)\' ",r.text )
# print(crsf[0])


Gui = GuiBase()

import pytest


# from selenium.webdriver import ChromeOptions, Chrome
# opts = ChromeOptions()
# opts.add_experimental_option("detach", True)
# driver = Chrome(chrome_options=opts)




# class Test_Web():
#     '''web的测试类,三茅网站登录'''
#     def test_hrloo_001(self,driver):
#         lgn = login_sanmao(driver)
#         lgn.sanmao_login(1406607478,'hrloo.com')
#         time.sleep(3)
#         lgn.verify_content('创作中心')

class Test_Case():
    '''砸蛋'''
    @pytest.mark.usefixtures('sanmao_log')
    def test_sanmao_zajindan(self,driver):
        '''会员中心'''
        pro.knock_egg(driver)
        time.sleep(3)
        pro.verify_zajinda(driver,'已发放至您账户，可兑换或抵扣商品')



# class Test_Case2():
#     '''购物支付'''
#
#     @pytest.mark.usefixtures('sanmao_log')
#     def test_orider(self, driver):
#         '''购买课程'''
#         by = Buy_Course(driver)
#         by.affard_oride()
#         time.sleep(3)
#         by.judge_result('支付成功')
#
#     @pytest.mark.usefixtures('sanmao_log')
#     def test_write_Sum(self,driver):
#         '''写总结'''
#         wri = Write_Ariticle(driver)
#         wri.write_summarize()
#         time.sleep(3)
#         wri.assert_ok('发布成功')


# class Test_Case4():
#     @pytest.mark.usefixtures('sanmao_log')
#     def test_chat(self, driver):
#         '''聊天'''
#         sanmao_chat.chat_each(driver)
#         sanmao_chat.assert_chat(driver, text='会员中心')
#         driver.quit()



# pytest -v -m 装饰器的 sanmao
# pytest -v -m 装饰器的 'not sanmao'

# if __name__ == '__main__':
#     pytest.main(['-s','test001webauto.py','-m=sanmao'])
# allure test_demo.py --alluredir ./report/allure_raw1
# allure test_demo.py --alluredir ./report/allure_raw1 --allure-serverity=blocked\critrial\normal\minor\trivial

