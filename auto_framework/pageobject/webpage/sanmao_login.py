from core.webbase import WebBase
from core.utils import read_yaml
from config.settings import Settings as ST
from core.logger import Logger
import time

logger = Logger('sanmao_login.py').getLogger()



class login_sanmao(WebBase):
    '''登录类'''
    '''
    初始化driver
    '''
    def __init__(self,driver):
        super().__init__(driver)
        self.webInfo = read_yaml(ST.WEBINFO)['sanmao']

    def sanmao_login(self,username,password):
        '''三茅登录方法工具'''
        logger.info('三茅登录开始')
        # 让登录每次从首页开始

        handle = self.driver.window_handles
        self.switch_handle(handle[0])

        url = 'https://passport.hrloo.com/user/login?referer=https%3A%2F%2Fwww.hrloo.com&wx_check_login=no_check'
        self.get_url(url)
        self.click(self.webInfo["pass_login"])
        self.sendKeys(self.webInfo["username"], username)
        self.sendKeys(self.webInfo["password"], password)
        self.click(self.webInfo['login_button'])
        logger.info('三茅登录结束')

    def verify_content(self,text):
        assert self.get_text(self.webInfo['is_login']) == text
        print('验证成功')



if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Chrome(executable_path=r'D:\python3.6\projects\auto_framework\tools\chromedriver.exe')
    lg =login_sanmao(driver)
    lg.sanmao_login(2008932277,'hrloo.com')
    time.sleep(5)




