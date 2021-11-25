#!/usr/bin/python3
#coding:utf8
from core.webbase import WebBase
from config.settings import Settings as ST
from core.guibase import GuiBase
import time
import pyautogui
from core.utils import read_yaml
webInfo = read_yaml(ST.WEBINFO)['sanmao']
Gui = GuiBase()


class process_enter():
    '''流程类,砸金蛋'''
    def knock_egg(self,driver):
        '''砸蛋'''
        web = WebBase(driver)
        web.click(webInfo['vip_hrspl'])


        # 切换到最新的窗口，进行元素的定位
        handles = driver.window_handles
        web.switch_handle(handles[-1])


        # lst = [webInfo['click_close']]
        # for i in lst:
        #     if i in lst:
        #         web.click(i)
        #         handles = driver.window_handles
        #         web.switch_handle(handles[-1])
        #         break
        #     else:
        #         break

        # if web.isElementExist(webInfo['click_close']):
        #     time.sleep(2)
        #     handle1 = driver.window_handles
        #     web.switch_handle(handle1[0])
        #     driver.quit()
        # else:
        #     time.sleep(2)
        #     web.click(webInfo['enter_vip'])

        time.sleep(2)
        # 点击去听书
        web.click(webInfo['enter_vip'])

        # 切换到听书
        handles = driver.window_handles
        web.switch_handle(handles[-1])

        time.sleep(3)

        # 下滑滑轮
        x, y = pyautogui.position()
        print(x, y)
        Gui.scroll(amount_to_scroll=-500, moveToX=x - 10, moveToY=y - 10)

        # web.click(webInfo['click_books'])
        time.sleep(3)
        # 点击应知应会
        web.click(webInfo['click_book'])

        # 切换到应知应会音频页面  # json的格式只能有一个花括号
        # 点击第一个播放
        web.click(webInfo['click_cour1'])
        time.sleep(3)
        web.click(webInfo['click_cour2'])

        # 切换到最开始打开的页面
        h1 = driver.window_handles
        print(h1)
        web.switch_handle(h1[0])
        # 获取源码
        a = driver.page_source
        print(a)
        assert web.get_title() == "三茅人力资源网-专业的HR学习交流平台"
        print("登陆成功")
        time.sleep(3)

        # 点击会员中心
        web.click(webInfo['vip_hrspl'])

        h2 = driver.window_handles
        web.switch_handle(h2[-1])
        # 需要喘口气
        time.sleep(3)
        x1, y1 = pyautogui.position()
        print(x1, y1)
        Gui.scroll(amount_to_scroll=-1000, moveToX=x1, moveToY=y1)
        web.click(webInfo['click_jindan'])
        time.sleep(3)
        web.click(webInfo['za_jindan'])


    def verify_zajinda(self,driver,text1):
        web = WebBase(driver)
        assert web.get_text(webInfo['is_get']) == text1
        print('获取金蛋成功')
        driver.quit()






