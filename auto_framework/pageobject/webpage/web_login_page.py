from core.logger import Logger
from core.webbase import WebBase
from core.utils import read_yaml
from config.settings import Settings as ST
import time

logger = Logger('guibase.py').getLogger()


class LoginPage(WebBase):

    def __init__(self,driver):
        super().__init__(driver)
        self.logindata = read_yaml(ST.WEBINFO)['login']

    def login(self,username,password):
        """稿件系统登录"""
        logger.info('稿件系统登录开始')
        self.get_url(ST.SERVER)
        time.sleep(1)
        self.clear(self.logindata['username'])
        self.sendKeys(self.logindata['username'],username)
        self.click(self.logindata['password'])
        self.clear(self.logindata['password'])
        self.sendKeys(self.logindata['password'],password)
        self.click(self.logindata['loginbtn'])
        logger.info('稿件系统登录结束')

    def quit(self):
        '''退出'''
        logger.info('稿件系统退出开始')
        self.click(self.logindata['welcome'])
        self.click(self.logindata['quitbtn'])
        logger.info('稿件系统退出结束')

    def assert_login_ok(self,flag='1'):
        '''登录断言'''
        if flag == '1':
            text = self.get_text(self.logindata['welcome'])
            assert text == 'Welcome test01!','断言：登录失败:{}'.format(text)
            logger.info('【断言】：登录成功！')
            self.quit()
        elif flag == '2':
            text = self.get_text(self.logindata['error1'])
            assert text == '请输入有效的登入。','断言：用户名错误登录失败:{}'.format(text)
            logger.info('【断言】：用户名错误登录成功！')
        elif flag == '3':
            text = self.get_text(self.logindata['error1'])
            assert text == '登入认证失败。请再试试。','断言：密码错误登录失败:{}'.format(text)
            logger.info('【断言】：密码错误登录成功！')


if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Ie(executable_path=r'C:\Users\19344\Desktop\auto_framework\tools\IEDriverServer.exe')
    lg = LoginPage(driver)
    lg.login('test01','1111')
    time.sleep(5)