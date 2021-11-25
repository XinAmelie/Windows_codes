from core.webbase import WebBase
from config.settings import Settings as ST
from exts.comExts.read_yaml import read_yaml
from core.guibase import GuiBase
import pyautogui
import random
import sys

import time
import pyperclip

Gui = GuiBase()




# 写项目pag类之前，需要先建立test_*.py和 test 的函数,不然driver不能引用

class Write_Ariticle(WebBase):
    '''写文章'''
    def __init__(self,driver):
        super().__init__(driver)
        self.webinfo = read_yaml(ST.WEBINFO)['sanmao']
        self.webinfo_sanmo = read_yaml(ST.WEBINFO)['Sanmao_project']
        self.webinfo_sum = self.webinfo_sanmo['Summarize']

    def write_summarize(self):
        '''写总结'''
        # driver.maximize_window()
        # url = "https://passport.hrloo.com/user/login?referer=https%3A%2F%2Fwww.hrloo.com&wx_check_login=no_check"
        # driver.get(url)
        #
        # driver.implicitly_wait(10)
        #
        # web.click(webinfo['pass_login'])
        # web.sendKeys(webinfo['username'],'1608556481')
        # web.sendKeys(webinfo['password'],'hrloo.com')
        # web.click(webinfo['login_button'])

        self.click(self.webinfo_sum['figure_icon'])

        # 切换页面，到最新的一页
        handle1 = self.driver.window_handles
        self.switch_handle(handle1[-1])

        # 展开

        time.sleep(3)

        Gui.click_picture('show',clicks=1,button='left')

        self.click(self.webinfo_sum['tag_sum'])

        handle2 = self.driver.window_handles
        self.switch_handle(handle2[-1])

        time.sleep(3)

        self.click(self.webinfo_sum['write_sum'])

        # 安装pyperclip 先复制中文，再粘贴
        # copy()用于向计算机的剪贴板发送文本，paste()用于从计算机剪贴板接收文本。先定位,再粘贴
        # sendkey万能写

        self.sendKeys(self.webinfo_sum['write_content_title'],'你我皆是羔羊却没有草原')
        time.sleep(3)

        x,y = pyautogui.position()
        print(x,y)
        pyautogui.moveTo(839,427,2,pyautogui.easeInElastic)

        Gui.click_picture('write_content',clicks=1,button='left')
        time.sleep(3)

        str = "你我皆是羔羊却没有草原宁静的城市搅起阵阵喧嚣柴门闻犬吠的日子已越来越远，说到底我还是没法跟我的队友彻底和解，我灵魂最深处永远保留一小块顽固的恨意，相信他们也是。就好像公主床垫下的一粒豌豆，不至于让我丧命，但让我遍体硌得青紫，漫漫长夜里睁着眼无法入眠。长大之后，我与所有人相处融洽，我们有分寸，往来得体，举杯的时候会讲甜美的祝酒词，隔着一层肚皮，谁也不肯把鲜活的心脏放在餐盘中供人展览点评，“真实”变成一种猎奇。悲哀的是，我仍然渴望真爱。事实清晰又绝望：想要找到真正理解我的恋人，竟然只能从我恨的人里找。"
        pyperclip.copy(str)
        pyperclip.paste()
        Gui.hotkey('ctrl','v')

        self.click(self.webinfo_sum['publish'])

        time.sleep(3)

        # 随机的两个标签
        lst = [self.webinfo_sum['tag1'],self.webinfo_sum['tag2'],self.webinfo_sum['tag3']]
        lst_result = random.sample(lst,2)

        a = 0
        for i in lst:
            if i in lst_result and a<2:
                self.click(lst_result[a])
                a += 1
                time.sleep(3)
            else:
                self.click(self.webinfo_sum['tag2'])

        time.sleep(3)
        self.sendKeys(self.webinfo_sum['input_text'],'人力效率1')
        self.click(self.webinfo_sum['paste'])
        self.sendKeys(self.webinfo_sum['input_text'], '人力效率2')
        self.click(self.webinfo_sum['paste'])
        self.click(self.webinfo_sum['submit'])

    def assert_ok(self,text):
        assert self.get_text(self.webinfo_sum['assert_ok']) == text
        print('发布成功')










































