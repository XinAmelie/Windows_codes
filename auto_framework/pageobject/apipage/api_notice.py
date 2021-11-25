import copy
from config.settings  import Settings as ST
from exts.comExts.read_yaml import read_yaml
from core.logger import Logger
from core.apibase import ApiBase
from urllib.parse import urljoin

logger = Logger('api_notice.py').getLogger()
notice = read_yaml(ST.LOGIN_INFO)['Notice']

class Notice():
    def __init__(self,*args,**kwargs):
        self.api= ApiBase()

    def login(self,device_Id,os_type):
        '''上报device id及通知设置等信息'''
        logger.info('开始获取app的设备号')
        info = copy.deepcopy(notice['report_deviceid'])
        # post的方法
        url = urljoin(ST.SERVER,info['url'])
        body = info['data']
        header = info['header']

        data_info = info['data']
        data_info['device_id'] = device_Id
        data_info['os_type'] = os_type

        pars = info['query_string']
        res = self.api.post(url,data=body,headers=header,params=pars)
        logger.info('获取流程结束')
        return res.json()

    def assert_ok(self,res,text):
        assert res['result'] == text,"【断言】：当前页面标题验证失败：{}".format(res['result'])
        print('断言成功')
        logger.info("【断言】：当前页面标题验证成功：{}".format(res['result']))

if __name__ == '__main__':
    N = Notice()
    res = N.login(device_Id='13eef3bfa53445de902f30012de1cbbd',os_type='Android')
    N.assert_ok(res,True)
    print(res)





