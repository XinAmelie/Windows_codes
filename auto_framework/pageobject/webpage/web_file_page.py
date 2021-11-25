import os

from core.logger import Logger
from core.webbase import WebBase
from core.utils import read_yaml
from config.settings import Settings as ST
import time
from exts.comExts.database_oper import MysqlHelp
from core.guibase import GuiBase

logger = Logger('web_file_page.py').getLogger()


class FilePage(WebBase):

    def __init__(self,driver):
        super().__init__(driver)
        self.filedata = read_yaml(ST.WEBINFO)['file']

    def select_db_info(self,sql):
        '''查询数据库'''
        dbInfo = read_yaml(ST.CASEDATA)['DBinfo']
        db = MysqlHelp(dbInfo['host'],dbInfo['user'],dbInfo['passwd'],dbInfo['port'],dbInfo['database'])
        res = db.select_fetchall(sql)
        return res

    def add_folder(self,name,desc):
        '''新增文件夹'''
        logger.info("新增文件夹开始")
        self.click(self.filedata['file_page'])
        self.click(self.filedata['add_btn'])
        self.sendKeys(self.filedata['folder_name'],name)
        self.sendKeys(self.filedata['folder_desc'],desc)
        self.click(self.filedata['save_folder'])
        logger.info("新增文件夹结束")

    def del_folder(self):
        '''删除文件夹'''
        logger.info("删除文件夹开始")
        self.click(self.filedata['first_del'])
        time.sleep(1)
        if not self.is_alert():
            self.click(self.filedata['first_del'])
        self.is_alert().accept()
        logger.info("删除文件夹结束")

    def upload_file(self,rename,desc):
        '''上传文档'''
        logger.info("上传文档开始")
        self.click(self.filedata['first_name'])
        self.click(self.filedata['upload_btn'])
        self.switch_iframe(self.filedata['iframe'])
        self.sendKeys(self.filedata['input_file'],ST.UPLOADFILE)
        self.sendKeys(self.filedata['rename_file'],rename)
        self.sendKeys(self.filedata['desc_file'],desc)
        self.click(self.filedata['sub_file'])
        self.switch_iframe_up()
        logger.info("上传文档结束")

    def download_file(self):
        '''文档下载'''
        logger.info("文档下载开始")
        url = self.get_attribute(self.filedata['first_size'],'href')
        self.get_url(url)
        GuiBase().hotkey('alt','s')
        time.sleep(1)
        logger.info("文档下载结束")

    def select_file(self,rename):
        '''文档查询'''
        logger.info("文档查询开始")
        fix_name = rename.split('.')[0]
        self.sendKeys(self.filedata['select_file'],fix_name)
        self.click(self.filedata['select_btn'])
        logger.info("文档查询结束")

    def del_file(self):
        '''文档删除'''
        logger.info("文档删除开始")
        self.click(self.filedata['delect_file'])
        time.sleep(1)
        self.is_alert().accept()
        logger.info("文档删除结束")

    def assert_addfolder_page(self,name):
        '''断言页面：文件夹新增'''
        name_info = self.get_text(self.filedata['first_name'])
        assert name_info == name,'【断言页面】:文件夹新增失败：{}'.format(name_info)
        logger.info("【断言页面】:文件夹新增成功：{}".format(name_info))

    def assert_addfolder_database(self,name,desc):
        '''断言数据库：文件夹新增'''
        res = self.select_db_info('SELECT `name`,description FROM dlfolder ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == name, '【断言数据库】:文件夹名称验证失败：{}'.format(res[0])
        logger.info("【断言数据库】:文件夹名称验证成功：{}".format(res[0]))
        assert res[1] == desc, '【断言数据库】:文件夹描述验证失败：{}'.format(res[1])
        logger.info("【断言数据库】:文件夹描述验证成功：{}".format(res[1]))

    def assert_delfolder_page(self):
        '''断言页面：文件夹删除'''
        name_info = self.get_text(self.filedata['msg_success'])
        assert name_info == '您的请求执行成功。','【断言页面】:文件夹删除失败：{}'.format(name_info)
        logger.info("【断言页面】:文件夹删除成功：{}".format(name_info))

    def assert_upload_page(self,rename,desc):
        '''断言页面：文档上传'''
        file_name = self.get_text(self.filedata['first_file'])
        assert file_name.split('\n')[0] == rename,'【断言页面】:文档上传验证-标题失败：{}'.format(rename)
        logger.info("【断言页面】:文档上传验证-标题成功：{}".format(file_name[0]))
        assert file_name.split('\n')[1] == desc,'【断言页面】:文档上传验证-描述失败：{}'.format(desc)
        logger.info("【断言页面】:文档上传验证-描述成功：{}".format(file_name[1]))

    def assert_upload_database(self,rename,desc):
        '''断言数据库：文档上传'''
        res = self.select_db_info('SELECT title,description FROM dlfileentry ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == rename.split('.')[0], '【断言数据库】:文档上传验证-标题失败：{}'.format(res[0])
        logger.info("【断言数据库】:文档上传验证-标题成功：{}".format(res[0]))
        assert res[1] == desc, '【断言数据库】:文档上传验证-描述验证失败：{}'.format(res[1])
        logger.info("【断言数据库】:文档上传验证-描述验证成功：{}".format(res[1]))

    def assert_download_file(self,rename):
        '''断言文档下载'''
        path = os.path.join(ST.DOWN_FILE,rename)
        is_exist = os.path.exists(path)
        assert is_exist,'文件不存在：{}'.format(path)
        logger.info("【断言】:断言文档下载验证成功：{}".format(path))
        for filename in os.listdir(ST.DOWN_FILE):
            path_i = os.path.join(ST.DOWN_FILE,filename)
            os.unlink(path_i)

    def assert_select_page(self,rename):
        '''断言页面：文档查询'''
        name = self.get_text(self.filedata['select_first'])
        fix_name = rename.split('.')[0]
        assert name == fix_name, '【断言数据库】:文档查询失败：{}'.format(fix_name)
        logger.info("【断言页面】:文档查询成功：{}".format(fix_name))

    def assert_select_database(self,rename):
        '''断言数据库：文档查询'''
        fix_name = rename.split('.')[0]
        res = self.select_db_info('SELECT COUNT(*) FROM dlfileentry WHERE title = "{}";'.format(fix_name))[0]
        assert res[0] == 1, '【断言数据库】:文档查询失败：{}'.format(res[0])
        logger.info("【断言数据库】:文档查询成功：{}".format(res[0]))

    def assert_del_page(self):
        '''断言页面：文档删除'''
        name_info = self.get_text(self.filedata['msg_success'])
        assert name_info == '您的请求执行成功。','【断言页面】:文件夹删除失败：{}'.format(name_info)
        logger.info("【断言页面】:文件夹删除成功：{}".format(name_info))

    def assert_del_database(self,rename):
        '''断言数据库：文档删除'''
        fix_name = rename.split('.')[0]
        res = self.select_db_info('SELECT COUNT(*) FROM dlfileentry WHERE title = "{}";'.format(fix_name))[0]
        assert res[0] == 0, '【断言数据库】:文档查询失败：{}'.format(res[0])
        logger.info("【断言数据库】:文档查询成功：{}".format(res[0]))




if __name__ == '__main__':
    from selenium import webdriver
    from pageobject.webpage.web_login_page import LoginPage
    driver = webdriver.Ie(executable_path=r'C:\Users\Admin\Desktop\auto_framework\tools\IEDriverServer.exe')
    l = LoginPage(driver)
    a = FilePage(driver)
    l.login('test01','1111')
    a.add_folder('aaa','bbb')
    a.upload_file('test.txt','这是描述信息')
    a.download_file()
