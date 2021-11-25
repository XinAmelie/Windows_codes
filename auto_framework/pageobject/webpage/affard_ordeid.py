import time
from config.settings import Settings as ST
from core.utils import read_yaml
import pyautogui
from core.webbase import WebBase
from core.guibase import GuiBase
import sys
from core.logger import Logger

logger = Logger('affard_ordeid.py').getLogger()
import random
Gui = GuiBase()

class Buy_Course(WebBase):
    '''购买课程并支付'''
    def __init__(self,driver):
        super().__init__(driver)
        self.webInfo = read_yaml(ST.WEBINFO)['sanmao']

    def affard_oride(self):

        # driver.maximize_window()
        # url = 'https://passport.hrloo.com/user/login?referer=https%3A%2F%2Fwww.hrloo.com&wx_check_login=no_check'
        # driver.get(url)
        # web.click(webInfo["pass_login"])
        # web.sendKeys(webInfo["username"], 1907753493  )
        # web.sendKeys(webInfo["password"], 'hrloo.com')
        # web.click(webInfo['login_button'])
        # lg.sanmao_login(driver,1907753493,'hrloo.com')

        # 点击课程

        self.click(self.webInfo['but_kecheng'])
        handle = self.driver.window_handles
        self.switch_handle(handle[1])
        time.sleep(3)

            # 下滑鼠标
        x,y = pyautogui.position()
        print(x,y)
        Gui.moveto(842,453)
        print('\n移动到842，453的位置')
        time.sleep(2)
        Gui.scroll(amount_to_scroll=-300, moveToX=842, moveToY=453)

            # 点击随机的商品
        lst = [self.webInfo['course_1'], self.webInfo['course_2'], self.webInfo['course_3']]
        lst_course = random.choice(lst)

        for i in lst:
            if lst_course == i:
                self.click(i)
                handle7 = self.driver.window_handles
                self.switch_handle(handle7[-1])
                break

                    # -1是最新的页面

        if self.isElementExist(self.webInfo['ins_study'], 3):
            '''判断是否有立即学习。有'''

            try:
                time.sleep(2)
                handle1 = self.driver.window_handles
                self.switch_handle(handle1[0])
                logger.info(" 我在这里发现了{},我要退出".format(self.webInfo['ins_study']))
                print('关闭')
                handle19 = self.driver.window_handles
                self.switch_handle(handle19[0])
            except:
                sys.exit(0)
            # System.exit(0)是正常退出程序，而System.exit(1)或者说非0表示非正常退出程序

        else:
            '''无'''
            time.sleep(3)
            handle10 = self.driver.window_handles
            self.switch_handle(handle10[-1])
            self.click(self.webInfo['affard'])

            # time.sleep(5)
            # driver.quit()
            # 系统退出 0正常退出  1异常退出
            # sys.exit(0)

        handle1 = self.driver.window_handles
        self.switch_handle(handle1[-1])

        time.sleep(3)
        self.click(self.webInfo['ins_affard'])

        time.sleep(3)

        # 打开新页面
        js = "window.open('www.google.com')"
        self.driver.execute_script(js)

        # 切换页面到最新页
        handle2 = self.driver.window_handles
        self.switch_handle(handle2[-1])

        time.sleep(3)

        Gui.rel_picture_click('browser', rel_x=-150, rel_y=0, button='left', clicks=3)
        Gui.type("https://www.hrloo.com/hr/product/order/pay_nofity?orderid=2020053015908185564491")

        Gui.hotkey('Enter')

        handle2 = self.driver.window_handles
        self.switch_handle(handle2[-2])

        Gui.rel_picture_click('orderid', rel_x=-150, rel_y=0, button='left', clicks=2)
        Gui.hotkey('ctrl', 'c')

        time.sleep(3)

        handle2 = self.driver.window_handles
        self.switch_handle(handle2[-1])
        time.sleep(3)

        Gui.rel_picture_click('browser', rel_x=-150, rel_y=0, button='left', clicks=2)
        Gui.hotkey('ctrl', 'v')
        Gui.hotkey('Enter')

        time.sleep(3)
        handle2 = self.driver.window_handles
        self.switch_handle(handle2[-2])


    def judge_result(self,text1):
        assert self.get_text(self.webInfo['is_affard']) == text1
        print(text1)






