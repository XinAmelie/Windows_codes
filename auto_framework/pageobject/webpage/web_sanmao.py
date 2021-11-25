from config.settings import Settings as  ST
from core.utils import read_yaml
from  core.webbase import WebBase
import time
import random
import pyperclip
from core.guibase import GuiBase
from selenium import webdriver

gui = GuiBase()

webinfo = read_yaml(ST.WEBINFO)['sanmao']
sanmao_chat=read_yaml(ST.WEBINFO)['Sanmao_project']['Chat']


class Tools():
    '''工具类'''
    # def __init__(self):
    #     self.driver1 = webdriver.Firefox(executable_path=r'F:\python3.6.8\projects\auto_framework\tools\geckodriver.exe')

    def chat_text(self,driver,el, text):
        '''谷歌聊天'''
        web = WebBase(driver)
        web.click(el)
        web.sendKeys(el, text)
        gui.hotkey('enter')

    def chat_fox(self,driver1,el,text):
        '''火狐聊天'''
        web1 = WebBase(driver1)
        web1.click(el)
        web1.sendKeys(el, text)
        gui.hotkey('enter')
        time.sleep(2)

    def gle_browser(self, el_pic):
        '''切换到谷歌'''
        gui.click_picture(el_pic, clicks=1, button='left')
        time.sleep(2)

    def fox_browser(self, el_pic):
        '''切换到火狐'''
        gui.click_picture(el_pic, clicks=1, button='left')
        time.sleep(2)

class Sanmao_Chat():
    '''三茅聊天'''
    def chat_each(self,driver):
        '''聊天'''
        t = Tools()  # 工具实例化
        web = WebBase(driver)
        # driver.maximize_window()
        # url = "https://passport.hrloo.com/user/login?referer=https%3A%2F%2Fwww.hrloo.com&wx_check_login=no_check"
        # driver.get(url)
        # # 隐形等待
        # driver.implicitly_wait(5)
        # web.click(webinfo['pass_login'])
        # web.sendKeys(webinfo['username'], 1406607478)
        # web.sendKeys(webinfo['password'], 'hrloo.com')
        # web.click(webinfo['login_button'])


        # 点击消息中心
        web.click(sanmao_chat['msg_center'])
        time.sleep(2)

        # 二选择一吧
        lst_data = [sanmao_chat['user1'],sanmao_chat['user2']]
        lst_ran = random.choice(lst_data)

        if web.isElementExist(lst_ran,10):
            print('-'*30+ ("我选择点击:%s"%(lst_ran))+'_'*30)
            web.click(lst_ran)
        else:
            print('_'*30+("没办法了，我只能点击这一个了:%s" % (sanmao_chat['user4']))+'_'*30)
            web.click(sanmao_chat['user4'])

        time.sleep(2)

        web.sendKeys(sanmao_chat['input_text'],'你今天好吗？')

        gui.hotkey('shift','enter')
        gui.hotkey('shift','enter')

        str = "生活的无奈，有时并不源于自我，别人无心的筑就，那是一种阴差阳错。生活本就是矛盾的，白天与黑夜间的距离，春夏秋冬之间的轮回，于是有了挑剔的喜爱，让无奈加上了喜悦的等待。面和小编一起来看经典优美的句子，希望有所帮助"
        str_1 = "我爸一天只让我看两个小时的手机，等我一有时间就给你们更新故事"
        str_2= "我要是撩他，可能我就没有明天了"
        str_3 = "你一定遇到过这样的人，说话思维跳跃，问他吃了没，他会和你说昨天跑了马拉松的事。他的逻辑是：一说吃，他就想到昨天跑马饿坏了，所以说的就是马拉松的事。"
        lst_str = [str,str_1,str_2,str_3]
        lst_random = random.choice(lst_str)

        pyperclip.copy(lst_random)
        pyperclip.paste()
        gui.hotkey('ctrl', 'v')

        time.sleep(2)
        # 点击发送
        web.click(sanmao_chat['send_msg'])
        # 点击发送图片
        web.click(sanmao_chat['select_img'])
        # 选择windows的图片一栏
        time.sleep(5)

        gui.click_picture('img',button='left',clicks=1)
        gui.click_picture('img2',clicks=2,button='left')

        # 火狐
        driver1 = webdriver.Firefox(executable_path=r'F:\python3.6.8\projects\auto_framework\tools\geckodriver.exe')
        driver1.maximize_window()
        url1 = 'https://passport.hrloo.com/user/login?referer=https%3A%2F%2Fwww.hrloo.com&wx_check_login=no_check'
        driver1.get(url1)
        time.sleep(2)
        # 为了区分与定义的公共driver，我采用另外设置一个driver,实例化web1
        # 程序定位不到时：1.元素 2.时间间隔 3.页面不对
        web1 = WebBase(driver1)
        web1.click(webinfo['pass_login'])
        time.sleep(2)
        # 以及lst_ran的聊天人，我们火狐进行相应的登录



        if lst_data[0] == lst_ran:
            web1.sendKeys(webinfo['username'], 2111713263)
            web1.sendKeys(webinfo['password'], 'hrloo.com')
            web1.click(webinfo['login_button'])
        else:
            web1.sendKeys(webinfo['username'], 2111636936)
            web1.sendKeys(webinfo['password'], 'hrloo.com')
            web1.click(webinfo['login_button'])




        time.sleep(3)

        # 火狐聊天
        web1.click(sanmao_chat['msg_center'])
        web1.click(sanmao_chat['user_xubo'])
        web1.sendKeys(sanmao_chat['input_text'], '重新认识下，你好')
        time.sleep(2)
        web1.click(sanmao_chat['send_msg1'])

        time.sleep(2)
        t.gle_browser(el_pic='google')

        # 关键字参数放最后
        t.chat_text(driver,sanmao_chat['input_text'],text='你好啊！')



        t.fox_browser(el_pic='fox_browser')


        t.chat_fox(driver1,sanmao_chat['input_text'],'第一次聊天，紧张了')

        t.gle_browser(el_pic='google')

        t.chat_text(driver,sanmao_chat['input_text'],'加油！,放松')


        t.fox_browser(el_pic='fox_browser')

        t.chat_fox(driver1,sanmao_chat['input_text'],'嗯嗯')



        t.gle_browser(el_pic='google')
        t.chat_text(driver,sanmao_chat['input_text'],'哈哈哈')

        time.sleep(2)
        t.fox_browser(el_pic='fox_browser')
        time.sleep(2)
        driver1.quit()


    def assert_chat(self,driver,text):
        t = Tools()
        web = WebBase(driver)
        t.gle_browser(el_pic='google')
        web.click(sanmao_chat['click_out'])
        time.sleep(2)
        assert web.get_text(sanmao_chat['assert_chat']) == text
        print('_'*30+str('聊天流程完成!!')+'_'*30)
        time.sleep(2)
        driver.quit()













































    












