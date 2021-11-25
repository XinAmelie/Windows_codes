import copy
import re
import time
from core.apibase import ApiBase
from core.logger import Logger
from core.utils import read_yaml
from urllib.parse import urljoin
from exts.comExts.database_oper import MysqlHelp
from config.settings import Settings as ST
from pageobject.apipage.api_login_page import ApiLogin

logger = Logger('api_article_page.py').getLogger()

article_page = read_yaml(ST.ARTICLE_INFO)['ArticlePage']



# 此继承方法会有问题。我采用第二种：init中初始化并实例化

# class ApiArticle():
#     def __init__(self):
#         self.api = ApiLogin
#         self.api.login('test01','1111')

class ApiArticle(ApiLogin):

    def __init__(self):
        super().__init__()
        self.login('test01','1111')

    def select_db_info(self,sql):
        '''查询数据库'''
        dbInfo = read_yaml(ST.CASEDATA)['DBinfo']
        db = MysqlHelp(dbInfo['host'],dbInfo['user'],dbInfo['passwd'],dbInfo['port'],dbInfo['database'])
        res = db.select_fetchall(sql)
        return res

    def add_article(self, title, content):
        '''稿件新增'''
        logger.info("稿件新增接口调用开始")
        #1.获取yaml文件中的接口数据
        add_api = copy.deepcopy(article_page['add_api'])
        #2.模拟添加稿件请求：post multipart/form-data;
        #（1）准备接口请求数据
        add_url = urljoin(ST.SERVER,add_api['url'])
        add_data = add_api['data']
        add_data['_15_title'] = title
        add_data['_15_content'] = content
        #（2）发送请求
        res = self.post(add_url,data=add_data,params=add_api['query_string'],headers=add_api['header'])
        assert res.status_code == 200,'稿件新增接口调用失败！'
        logger.info("稿件新增接口调用结束")
        return res.text

    def select_article(self,title=''):
        '''稿件查询方法'''
        logger.info("稿件查询接口调用开始")
        #1.获取yaml文件中的接口数据
        select_api = copy.deepcopy(article_page['select_api'])
        #2.模拟添加稿件请求：post multipart/form-data;
        #（1）准备接口请求数据
        select_url = urljoin(ST.SERVER,select_api['url'])
        select_data = select_api['data']
        select_data['_15_keywords'] = title
        #（2）发送请求
        select_res = self.post(select_url,data=select_data,params=select_api['query_string'],headers=select_api['header'])
        time.sleep(1)
        #（3）正则提取数据
        re_info = re.findall('&_15_version=1.0">(.*?)</a>',select_res.text)[:7]
        assert select_res.status_code == 200,'稿件查询接口调用失败！'
        logger.info("稿件查询接口调用结束")
        return re_info

    def delete_article(self,title=''):
        '''稿件删除'''
        logger.info("稿件删除接口调用开始")
        #1.选择第一条稿件
        delete_api = copy.deepcopy(article_page['delete_api'])
        #2.删除稿件
        # （1）准备接口请求数据
        delete_url = urljoin(ST.SERVER,delete_api['url'])
        delete_data = delete_api['data']
        # （2）获取编号并修改请求体
        id = self.select_article(title)[0]
        delete_data['_15_deleteArticleIds'] = '{}_version_1.0'.format(id)
        delete_data['_15_rowIds'] = '{}_version_1.0'.format(id)
        # （3）发送请求
        res = self.post(delete_url,data=delete_data,params=delete_api['query_string'],headers=delete_api['header'])
        assert res.status_code == 200,'稿件删除接口调用失败！'
        assert not id in res.text
        logger.info("稿件删除接口调用结束")

    def edit_article(self,title,content):
        '''稿件修改'''
        logger.info("稿件修改接口调用开始")
        #1.获取yaml文件中的接口数据
        edit_api = copy.deepcopy(article_page['edit_api'])
        #2.模拟添加稿件请求：post multipart/form-data;
        #（1）准备接口请求数据
        edit_url = urljoin(ST.SERVER,edit_api['url'])
        edit_data = edit_api['data']
        #（2）修改请求体
        edit_data['_15_title'] = title
        edit_data['_15_content'] = content
        edit_id = self.select_article()[0]
        edit_data['_15_articleId'] = edit_id
        edit_data['_15_deleteArticleIds'] = '{}_version_1.0'.format(edit_id)
        edit_data['_15_expireArticleIds'] = '{}_version_1.0'.format(edit_id)
        #（2）发送请求
        res = self.post(edit_url,data=edit_data,params=edit_api['query_string'],headers=edit_api['header'])
        assert res.status_code == 200,'稿件新增接口调用失败！'
        logger.info("稿件修改接口调用结束")
        return res.text

    def approved_article(self):
        '''稿件批准'''
        logger.info("稿件批准接口调用开始")
        #1.获取yaml文件中的接口数据
        edit_api = copy.deepcopy(article_page['edit_api'])
        #2.模拟添加稿件请求：post multipart/form-data;
        #（1）准备接口请求数据
        edit_url = urljoin(ST.SERVER,edit_api['url'])
        edit_data = edit_api['data']
        #（2）修改请求体
        edit_data['_15_title'] = '这是标题'
        edit_data['_15_content'] = '这是内容'
        edit_id = self.select_article()[0]
        edit_data['_15_articleId'] = edit_id
        edit_data['_15_approve'] = '1'
        edit_data['_15_deleteArticleIds'] = '{}_version_1.0'.format(edit_id)
        edit_data['_15_expireArticleIds'] = '{}_version_1.0'.format(edit_id)
        #（2）发送请求
        res = self.post(edit_url,data=edit_data,params=edit_api['query_string'],headers=edit_api['header'])
        assert res.status_code == 200,'稿件新增接口调用失败！'
        logger.info("稿件批准接口调用结束")
        return res.text

    def expired_article(self):
        '''稿件到期'''
        logger.info("稿件到期接口调用开始")
        #1.选择第一条稿件
        expired_api = copy.deepcopy(article_page['expired_api'])
        #2.删除稿件
        # （1）准备接口请求数据
        expired_url = urljoin(ST.SERVER,expired_api['url'])
        expired_data = expired_api['data']
        # （2）获取编号并修改请求体
        id = self.select_article()[0]
        expired_data['_15_expireArticleIds'] = '{}_version_1.0'.format(id)
        expired_data['_15_rowIds'] = '{}_version_1.0'.format(id)
        # （3）发送请求
        res = self.post(expired_url,data=expired_data,params=expired_api['query_string'],headers=expired_api['header'])
        assert res.status_code == 200,'稿件删除接口调用失败！'
        logger.info("稿件到期接口调用结束")

    def assert_add_art(self,title):
        '''新增稿件断言'''
        first_info = self.select_article(title)
        assert '不批准' == first_info[3],'【断言页面接口】:新增稿件的不批准失败：{}'.format(first_info[3])
        logger.info("【断言页面接口】:新增稿件的不批准成功：{}".format(first_info[3]))
        assert title == first_info[1],'【断言页面接口】:新增稿件的标题失败：{}'.format(first_info[1])
        logger.info("【断言页面接口】:新增稿件的标题成功：{}".format(first_info[1]))

    def assert_add_db(self,title,content):
        '''数据库新增断言'''
        res = self.select_db_info('SELECT title,content,approved FROM journalarticle ORDER BY createDate DESC LIMIT 1;')[0]
        assert title == res[0],'【断言数据库】:新增稿件的标题失败：{}'.format(res[0])
        logger.info("【断言数据库】:新增稿件的标题成功：{}".format(res[0]))
        assert content in res[1],'【断言数据库】:新增稿件的内容失败：{}'.format(res[1])
        logger.info("【断言数据库】:新增稿件的内容成功：{}".format(res[1]))
        assert 0 == res[2],'【断言数据库】:新增稿件的不批准失败：{}'.format(res[2])
        logger.info("【断言数据库】:新增稿件的不批准成功：{}".format(res[2]))

    def assert_dele_art(self,title):
        '''删除稿件断言'''
        title_info = self.select_article(title)
        assert [] == title_info,'【断言页面接口】:删除稿件失败：{}'.format(title_info)
        logger.info("【断言页面接口】:删除稿件成功：{}".format(title_info))

    def assert_dele_db(self,title):
        '''数据库删除断言'''
        res = self.select_db_info('SELECT COUNT(*) FROM journalarticle WHERE title = "{}";'.format(title))[0]
        assert res[0] == 0,'【断言数据库】:稿件删除失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件删除失败成功：{}".format(res[0]))

    def assert_select_art(self,title):
        '''查询稿件断言'''
        title_info = self.select_article(title)
        assert title == title_info[1],'【断言页面接口】:查询稿件失败：{}'.format(title_info)
        logger.info("【断言页面接口】:查询稿件成功：{}".format(title_info))

    def assert_select_db(self, title):
        '''数据库查询断言'''
        res = self.select_db_info('SELECT COUNT(*) FROM journalarticle WHERE title = "{}";'.format(title))[0]
        assert res[0] == 1, '【断言数据库】:稿件查询失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件查询失败成功：{}".format(res[0]))

    def assert_approved_art(self):
        '''稿件批准页面断言'''
        approved_info = self.select_article()[3]
        assert '批准' == approved_info,'【断言页面接口】:批准稿件失败：{}'.format(approved_info)
        logger.info("【断言页面接口】:批准稿件成功：{}".format(approved_info))

    def assert_approved_db(self):
        '''稿件批准数据库断言'''
        res = self.select_db_info('SELECT approved FROM journalarticle  ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == 1, '【断言数据库】:稿件批准失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件批准失败成功：{}".format(res[0]))

    def assert_expired_art(self):
        '''稿件到期页面断言'''
        expired_info = self.select_article()[3]
        assert '到期' == expired_info,'【断言页面接口】:到期稿件失败：{}'.format(expired_info)
        logger.info("【断言页面接口】:到期稿件成功：{}".format(expired_info))

    def assert_expired_db(self):
        '''稿件到期数据库断言'''
        res = self.select_db_info('SELECT expired FROM journalarticle  ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == 1, '【断言数据库】:稿件到期失败：{}'.format(res[0])
        logger.info("【断言数据库】:稿件到期失败成功：{}".format(res[0]))


if __name__ == '__main__':
    a = ApiArticle()
    res = a.add_article('这是标题aaa','这是内容bbb')
    # res = a.select_article('这是标题aaa')
    res = a.edit_article('这是标题aaa','aaa')
    print(res)