from config.settings import Settings as ST
from exts.comExts.read_yaml  import read_yaml
import copy
from core.apibase import ApiBase
from core.logger import Logger
from urllib.parse  import urljoin
from exts.comExts.database_oper import MysqlHelp
import time

logger = Logger('api_sanmao.py').getLogger()
sanmao = read_yaml(ST.LOGIN_INFO_SANMAO)['Sanmao']

class Api_Sanmao_Login():
    def __init__(self):
        self.api = ApiBase()

    def sanmao_login(self,user,pwd):
        logger.info('开始登录')
        # 拷贝数据，防止变量赋值，导致损坏yaml数据
        sanmao_data = copy.deepcopy(sanmao['login_sanmao'])
        url = urljoin(ST.SANMAO_SERVER,sanmao_data['url'])
        header = sanmao_data['header']

        body = sanmao_data['body']
        body['username'] = user
        body['password'] = pwd

        res = self.api.post(url,headers=header,data=body)
        return res.json()

    def assert_ok(self,res,text):
        assert res['result'] == text
        print('_'*30,'恭喜你登陆成功','_'*30)
        logger.info("[断言]成功: %s" % (res['result']) )

class Forth_Operation():
    '''前置操作'''
    def __init__(self,*args,**kwargs):
        self.api = ApiBase()

    def black_list(self,uid,is_remove):
        '''拉黑'''

        Black_List = read_yaml(ST.LOGIN_INFO_SANMAO)['Black_list']
        black_data = copy.deepcopy(Black_List['black_list'])

        logger.info('开始拉黑')

        url = urljoin(ST.SERVER,black_data['url'])
        pars = black_data['pars']
        pars['to_uid'] = uid
        pars['is_remove'] = is_remove

        res = self.api.get(url, params=pars)
        logger.info('拉黑结束')
        return res.json()


    def assert_ok(self,res,text):
        assert res['msg'] == text
        print('_'*30,'验证成功','_'*30)
        logger.info('此次拉黑为前置拉黑:{}'.format(res['msg']))

    def select_sql(self,sql):
        '''查询数据库'''
        database = read_yaml(ST.CASEDATA)['DBinfo']
        db = MysqlHelp(database['host'],database['user'],database['passwd'],database['port'],database['database'])
        res = db.select_fetchall(sql)
        print(res)

    def excute_sql(self,sql):
        '''执行sql'''
        database = read_yaml(ST.CASEDATA)['DBinfo']
        db = MysqlHelp(database['host'], database['user'], database['passwd'], database['port'], database['database'])
        db.insert_delete_update(sql)

class App_Msg():
    '''app消息'''
    def __init__(self,*args,**kwargs):
        self.api = ApiBase()

    def app_center(self,uid):
        '''获取个人中心'''
        logger.info("个人中心")
        mgcenter = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        # 获取到消息中心，个人主页的数据，进行深拷贝，防止变量的赋值，破坏yaml文件的数据
        per_center = copy.deepcopy(mgcenter['person_center'])
        url = urljoin(ST.SERVER,per_center['url'])

        pars = per_center['pars']
        pars['uid'] = uid
        res = self.api.get(url,params=pars)
        return res.json()

    def assert_ok(self,res,text):
        assert res['result'] == text,"验证失败:{}".format(res['result'])
        print('验证成功')
        logger.info('验证成功:%s'% (res['result']))

    def select_sql(self,sql):
        database = read_yaml(ST.CASEDATA)['DBinfo']
        db = MysqlHelp(database['host'], database['user'], database['passwd'], database['port'], database['database'])
        db.select_fetchall(sql)

    def get_maodou(self):
        '''获取用户剩余的茅豆'''
        logger.info('开始获取茅豆')
        getmaodou1 = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        copy_maodou = copy.deepcopy(getmaodou1['get_maodou'])
        url = urljoin(ST.SERVER,copy_maodou['url'])
        pars = copy_maodou['pars']

        res = self.api.get(url,params=pars)
        return res.json()

    def assert_maodou(self,res,text):
        '''验证获取剩余茅豆'''
        assert res['msg'] == text,"验证失败:{}".format(res['msg'])
        print("验证成功")
        logger.info('验证成功:%s'%(res['msg']))

    def guest_inters(self):
        '''猜你感兴趣'''
        logger.info('开始获取猜你感兴趣的接口')
        msg_center = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        guest_inters = copy.deepcopy(msg_center['guest_inters'])
        url = urljoin(ST.SERVER,guest_inters['url'])
        pars = guest_inters['pars']

        res = self.api.get(url,params=pars)
        return res.json()

    def assert_inters(self,res,text):
        '''断言猜你感兴趣'''
        assert res['msg'] == text,"验证失败".format(res['msg'])
        print('验证成功')
        logger.info("验证成功：%s" % res['msg'] )



    def msg_category(self):
        '''消息中心分类列表'''
        logger.info('消息分类')
        msg_list = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        msg_cate = copy.deepcopy(msg_list['category'])

        url = urljoin(ST.SERVER,msg_cate['url'])
        pars = msg_cate['pars']

        res = self.api.get(url,params = pars)
        return res.json()

    def assert_msg(self,res,text):
        '''判断消息中心分类列表'''
        assert res['data']['chat_list']['count'] == text,"验证失败".format(res['data']['chat_list']['count'])
        print('-'*30+str('恭喜你验证成功')+'-'*30)
        logger.info('验证成功:%s'% res['data']['chat_list']['count'])


    def get_chatrecord(self,gid,to_uid,max_id):
        '''聊天、创建团队并获取历史聊天记录'''
        logger.info('开始获取历史聊天记录')
        msg_list = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        chatcord = copy.deepcopy(msg_list['get_chatrecord'])
        url = urljoin(ST.SERVER,chatcord['url'])
        body = chatcord['body']
        body['gid'] = gid
        body['to_uid'] = to_uid
        body['max_id'] = max_id
        pars = chatcord['query_string']
        res = self.api.post(url,data=body,params=pars)
        return res.json()

    def assert_chatcord(self,res,text):
        '''断言聊天记录'''
        assert  res['resultcode'] == text,"验证失败".format(res['resultcode'])
        print('-'*30+str('恭喜你断言成功')+'-'*30)
        logger.info("验证成功".format(res['resultcode']))

    def get_chatlist(self):
        '''聊天列表数据'''
        logger.info('获取聊天列表数据')
        msg_list = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        chatlist = copy.deepcopy(msg_list['get_chatlist_data'])

        url = urljoin(ST.SERVER,chatlist['url'])
        pars = chatlist['pas']
        res = self.api.get(url,params=pars)
        return res.json()

    def assert_chatlist(self, res, text):
        '''断言聊天列表数据'''
        assert res['msg'] == text, "验证失败".format(res['msg'])
        print('-' * 30 + str('恭喜你断言成功') + '-' * 30)
        logger.info("验证成功".format(res['msg']))


    def get_unreadmsg(self):
        '''获取消息中心未读数量'''
        logger.info("开始获取未读数")
        msg_list = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        unread = copy.deepcopy(msg_list['get_unreadmsg'])
        url = urljoin(ST.SERVER,unread['url'])
        pars = unread['pars']

        res = self.api.get(url,params=pars)
        return res.json()

    def assert_unread(self,res,text):
        '''断言获取消息中心未读数量'''
        assert res['resultcode'] == text,"验证失败".format(res['resultcode'])
        print('-'*30 +str('恭喜验证成功')+'-'*30)
        logger.info('验证成功:%s' % res['resultcode'])


    def add_groupsend(self,content,text_type):
        '''添加群发消息'''
        logger.info('添加群发消息')
        msg_list = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        group_send=copy.deepcopy(msg_list['add_groupsend'])
        url = urljoin(ST.SERVER,group_send['url'])
        pars = group_send['pras']
        pars['content'] = content
        pars['text_type'] = text_type
        res = self.api.get(params=pars,url=url)
        return res.json()

    def assert_groupsend(self,res,text):
        '''断言群发消息'''
        assert res['msg'] == text, "验证失败".format(res['msg'])
        print('-' * 30 + str('恭喜验证成功') + '-' * 30)
        logger.info("验证失败".format(res['msg']))


    def get_admire(self,touid,moduleid,itemid,fee):
        '''赞赏'''

        logger.info('开始赞善')
        msg_list = read_yaml(ST.LOGIN_INFO_SANMAO)['Msg_Center']
        admire = copy.deepcopy(msg_list['admire_others'])

        url  = urljoin(ST.SERVER,admire['url'])
        pars = admire['query_string']
        body = admire['body']
        body['touid'] = touid
        body['moduleid'] = moduleid
        body['itemid'] = itemid
        body['fee'] = fee
        res = self.api.post(url,data=body,params=pars)
        time.sleep(2)
        return res.json()

    def assert_admire(self,res,text):
        '''断言赞赏消息'''
        assert res['data']['msg'] == text, "验证失败".format(res['data']['msg'])
        print('-' * 30 + str('恭喜验证成功') + '-' * 30)
        logger.info("验证失败".format(res['data']['msg']))



if __name__ == '__main__':
    # API = Api_Sanmao_Login()
    # r = API.sanmao_login(1406607478,'hrloo.com')
    # API.assert_ok(r,0)
    # print(r)
    # print('-'*30,'分割线','-'*30)
    # Bla = Forth_Operation()
    # res = Bla.black_list(uid=2686548,is_remove=0)
    # print(res)
    print('-' * 30, '分割线', '-' * 30)
    APP = App_Msg()
    # r = APP.app_center(4567612)
    # APP.assert_ok(r,True)
    res = APP.get_maodou()
    print(res)













