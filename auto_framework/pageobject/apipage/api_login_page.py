import copy
import re

from core.logger import Logger
from core.apibase import ApiBase
from core.utils import read_yaml
from urllib.parse import urljoin
from config.settings import Settings as ST

logger = Logger('guibase.py').getLogger()

login_page = read_yaml(ST.LOGIN_INFO)['LoginPage']


class ApiLogin(ApiBase):

    def login(self,username,password):
        '''登录'''
        logger.info("登录接口调用开始")
        #1.获取yaml文件中的接口数据
        login_api = copy.deepcopy(login_page['login_api'])
        #2，模拟第一次请求：get
        login_url = urljoin(ST.SERVER,login_api['url'])
        res = self.get(login_url,headers=login_api['header'])
        assert res.status_code == 200,'获取登录页面接口失败！'
        #3.模拟第二次请求：post
        login_data = login_api['data']
        login_data['_58_login'] = username
        login_data['_58_password'] = password
        res = self.post(login_url,data=login_data,params=login_api['query_string'],headers=login_api['header'])
        assert res.status_code == 200,'登录失败！'
        logger.info("登录接口调用结束")
        return res.text

    def assert_login_ok(self,res,title):
        '''断言登录是否成功'''
        title_page = re.findall('<title>(.*?)</title>',res)[0]
        assert title == title_page,"【断言】：当前页面标题验证失败：{}".format(title_page)
        logger.info("【断言】：当前页面标题验证成功：{}".format(title_page))


if __name__ == "__main__":
    l = ApiLogin()
    res = l.login('test01','1111')
    print(res)