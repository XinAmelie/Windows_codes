#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urljoin
import urllib3
from core.logger import Logger
from urllib3.exceptions import InsecureRequestWarning
logger = Logger('apibase.py').getLogger()


class ApiBase():
    '''接口测试工具类'''

    session = requests.session()

    def __init__(self):
        self.timeout = 10   #接口的超时时间，单位秒

    def post(self,url,data=None,json=None,params=None,headers=None,cookies=None,auth=None,files=None,allow_redirects=True):
        '''post请求'''
        logger.info('POST-接口请求地址：{}'.format(url))
        logger.debug('POST-接口请求体：{}'.format(data))
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            res = ApiBase.session.post(url=url,data=data,json=json,params=params,files=files,headers=headers,cookies=cookies,
                                       auth=auth,timeout=self.timeout,verify=False,allow_redirects=allow_redirects)
            assert res.status_code == 200
            logger.debug('POST-接口的响应码：{}'.format(res.status_code))
            logger.debug('POST-接口的返回结果: {}'.format(res.content.decode("utf-8"))) # 打印的是编码后的二进制流
            return res
        except Exception as e:
            logger.error('POST-接口请求超时：{}'.format(e))
            return None

    def get(self,url,data=None,params=None,headers=None,cookies=None,allow_redirects=True):
        '''get请求'''
        logger.info('GET-接口请求地址：{}'.format(url))
        logger.debug('GET-接口请求体：{}'.format(data))
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            res = ApiBase.session.get(url=url,data=data,headers=headers,params=params,cookies=cookies,
                                      timeout=self.timeout,verify=False,allow_redirects=allow_redirects)
            logger.debug('GET-接口请求总时长，单位秒：{}'.format(res.elapsed.total_seconds()))
            assert res.status_code == 200
            logger.debug('GET-接口的响应码：{}'.format(res.status_code))
            logger.debug('POST-接口的返回结果: {}'.format(res.content.decode("utf-8")))
            return res
        except Exception as e:
            logger.error('GET-接口请求超时：{}'.format(e))
            return None

    def urljoin(self, base, url):
        return urljoin(base, url)

    def update_head(self,headers=None):
        s = requests.session().headers.update(headers)
        return s

    def is_json(self, str):
        try:
            eval(str)
            return True
        except Exception as e:
            logger.debug("非json字符串:{}, error:{}".format(str, e))
            return False

    def get_content(self, content, is_json=True):
        try:
            res = False
            if is_json:
                content = eval(content)
                res = True
        except Exception as e:
            logger.error("非json字符串:{}, error:{}".format(content, e))
        finally:
            return content, res

    def __new__(cls, *args, **kwargs):
        if not hasattr(ApiBase, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
