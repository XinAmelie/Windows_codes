import copy
from config.settings  import Settings as ST
from exts.comExts.read_yaml import read_yaml
from core.logger import Logger
from core.apibase import ApiBase
from urllib.parse import urljoin

logger = Logger('api_notice.py').getLogger()
ap = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']


class Notice1():
    def __init__(self,*args,**kwargs):
        self.api= ApiBase()

    def login(self):
        logger.info('开始获取app的设备号')
        info = copy.deepcopy(ap['get_app'])
        # post的方法
        url = urljoin(ST.SERVER_APP, info['url'])
        pars = info['query_string']
        header = info['header']
        res = self.api.post(url, params=pars, headers=header)
        print(res.json())
        return res

if __name__ == '__main__':
    N = Notice1()
    res = N.login()
    print(res)

