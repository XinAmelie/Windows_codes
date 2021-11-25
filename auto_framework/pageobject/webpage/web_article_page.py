from core.logger import Logger
from core.webbase import WebBase
from core.utils import read_yaml
from config.settings import Settings as ST
import time

from exts.comExts.database_oper import MysqlHelp

logger = Logger('web_article_page.py').getLogger()

'''
application/x-www-form-urlencoded（大多数请求可用：eg：'name=Denzel&age=18'）
multipart/form-data（文件上传，这次重点说）
application/json（json格式对象，eg：{'name':'Denzel','age':'18'}）
text/xml(现在用的很少了，发送xml格式文件或流,webservice请求用的较多)
'''


class ArticlePage(WebBase):

    def __init__(self,driver):
        super().__init__(driver)
        self.articledata = read_yaml(ST.WEBINFO)['article']

    def add_article(self,title,content):
        '''稿件新增方法'''
        logger.info("稿件新增方法开始")
        self.click(self.articledata['add_article_btn'])
        self.sendKeys(self.articledata['title'],title)
        self.switch_iframe(self.articledata['add_iframe'])
        self.sendKeys(self.articledata['content'],content)
        self.switch_iframe_up()
        self.click(self.articledata['save'])
        self.click(self.articledata['select_btn'])
        logger.info("稿件新增方法结束")

    def delete_article(self):
        '''稿件删除方法'''
        logger.info("稿件删除方法开始")
        self.click(self.articledata['Check'])
        self.click(self.articledata['delete_btn'])
        self.is_alert().accept()
        logger.info("稿件删除方法结束")

    def select_article(self,title):
        '''稿件查询方法'''
        logger.info("稿件查询方法开始")
        self.sendKeys(self.articledata['select'],title)
        self.click(self.articledata['select_btn'])
        logger.info("稿件查询方法结束")

    def edit_article(self,title,content):
        '''稿件修改'''
        logger.info("稿件修改方法开始")
        self.click(self.articledata['first_article'])
        self.clear(self.articledata['title'])
        self.sendKeys(self.articledata['title'],title)
        self.switch_iframe(self.articledata['add_iframe'])
        self.clear(self.articledata['content'])
        self.sendKeys(self.articledata['content'],content)
        self.switch_iframe_up()
        self.click(self.articledata['save'])
        logger.info("稿件修改方法结束")

    def approved_article(self):
        '''稿件批准方法'''
        logger.info("稿件批准方法开始")
        self.click(self.articledata['first_article'])
        self.click(self.articledata['approve'])
        logger.info("稿件批准方法结束")

    def expired_article(self):
        '''稿件到期方法'''
        logger.info("稿件到期方法开始")
        self.click(self.articledata['Check'])
        self.click(self.articledata['expired_btn'])
        self.is_alert().accept()
        logger.info("稿件到期方法结束")

    def select_db_info(self,sql):
        '''查询数据库'''
        dbInfo = read_yaml(ST.CASEDATA)['DBinfo']
        db = MysqlHelp(dbInfo['host'],dbInfo['user'],dbInfo['passwd'],dbInfo['port'],dbInfo['database'])
        res = db.select_fetchall(sql)
        return res

    def assert_add_article(self,title,content):
        '''新增稿件断言'''
        approved = self.get_text(self.articledata['state'])
        assert '不批准' == approved,'【断言页面】:新增稿件的不批准失败：{}'.format(approved)
        logger.info("【断言页面】:新增稿件的不批准成功：{}".format(approved))
        self.click(self.articledata['first'])
        title_info = self.get_attribute(self.articledata['title'],'value')
        assert title == title_info,'【断言页面】:新增稿件的标题失败：{}'.format(title_info)
        logger.info("【断言页面】:新增稿件的标题成功：{}".format(title_info))
        self.switch_iframe(self.articledata['add_iframe'])
        content_info = self.get_attribute(self.articledata['content'],'value')
        assert content == content_info,'【断言页面】:新增稿件的内容失败：{}'.format(content_info)
        self.switch_iframe_up()
        self.click(self.articledata['save'])
        logger.info("【断言页面】:新增稿件的内容成功：{}".format(content_info))

    def assert_add_database(self,title,content):
        '''数据库新增断言'''
        res = self.select_db_info('SELECT title,content,approved FROM journalarticle ORDER BY createDate DESC LIMIT 1;')[0]
        assert title == res[0],'【断言数据库】:新增稿件的标题失败：{}'.format(res[0])
        logger.info("【断言数据库】:新增稿件的标题成功：{}".format(res[0]))
        assert content in res[1],'【断言数据库】:新增稿件的内容失败：{}'.format(res[1])
        logger.info("【断言数据库】:新增稿件的内容成功：{}".format(res[1]))
        assert 0 == res[2],'【断言数据库】:新增稿件的不批准失败：{}'.format(res[2])
        logger.info("【断言数据库】:新增稿件的不批准成功：{}".format(res[2]))

    def assert_dele_article(self,title):
        '''删除稿件断言'''
        title_info = self.get_text(self.articledata['first'])
        assert title != title_info,'【断言页面】:删除稿件失败：{}'.format(title_info)
        logger.info("【断言页面】:删除稿件成功：{}".format(title_info))

    def assert_dele_database(self,title):
        '''数据库删除断言'''
        res = self.select_db_info('SELECT COUNT(*) FROM journalarticle WHERE title = "{}";'.format(title))[0]
        assert res[0] == 0,'【断言数据库】:稿件删除失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件删除失败成功：{}".format(res[0]))

    def assert_select_article(self,title):
        '''查询稿件断言'''
        title_info = self.get_text(self.articledata['first'])
        assert title == title_info,'【断言页面】:查询稿件失败：{}'.format(title_info)
        logger.info("【断言页面】:查询稿件成功：{}".format(title_info))

    def assert_select_database(self, title):
        '''数据库查询断言'''
        res = self.select_db_info('SELECT COUNT(*) FROM journalarticle WHERE title = "{}";'.format(title))[0]
        assert res[0] == 1, '【断言数据库】:稿件查询失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件查询失败成功：{}".format(res[0]))

    def assert_approved_page(self):
        '''稿件批准页面断言'''
        approved_info = self.get_text(self.articledata['state'])
        assert '批准' == approved_info,'【断言页面】:批准稿件失败：{}'.format(approved_info)
        logger.info("【断言页面】:批准稿件成功：{}".format(approved_info))

    def assert_approved_database(self):
        '''稿件批准数据库断言'''
        res = self.select_db_info('SELECT approved FROM journalarticle  ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == 1, '【断言数据库】:稿件批准失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件批准失败成功：{}".format(res[0]))

    def assert_expired_page(self):
        '''稿件到期页面断言'''
        expired_info = self.get_text(self.articledata['state'])
        assert '到期' == expired_info,'【断言页面】:到期稿件失败：{}'.format(expired_info)
        logger.info("【断言页面】:到期稿件成功：{}".format(expired_info))

    def assert_expired_database(self):
        '''稿件到期数据库断言'''
        res = self.select_db_info('SELECT expired FROM journalarticle  ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == 1, '【断言数据库】:稿件到期失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件到期失败成功：{}".format(res[0]))


if __name__ == "__main__":
    from selenium import webdriver
    from pageobject.webpage.web_login_page import LoginPage
    driver = webdriver.Ie(executable_path=r'C:\Users\Admin\Desktop\auto_framework\tools\IEDriverServer.exe')
    l = LoginPage(driver)
    a = ArticlePage(driver)
    # l.login('test01','1111')
    # a.add_article('标题','内容')
    # a.select_article('标题')
    # a.edit_article('标题1','内容1')
    # a.approved_article()
    # a.delete_article()
    res = a.select_db_info('SELECT COUNT(*) FROM journalarticle WHERE title = "删除-这是标题";')[0]
    print(res)


