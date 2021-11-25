from pageobject.apipage.api_notice import Notice
from pageobject.apipage.api_sanmao import Forth_Operation
from pageobject.apipage.api_sanmao import App_Msg
import allure
import pytest
from core.utils import read_yaml
from config.settings import Settings as ST

app_msg = App_Msg()

admire_data = read_yaml(ST.LOGIN_INFO_SANMAO)['Testsuit_Data']

@allure.feature('通知/消息推送')
class Test_Notice():
    '''通知/消息推送'''

    @allure.story('上报device id模块')
    @allure.title('上报device id及通知设置等信息')
    @allure.severity('block')
    @allure.testcase('http://10.1.3.253/issues/25332')
    @allure.issue('http://10.1.3.253/issues/25332')
    @pytest.mark.usefixtures('login_forward')
    def test_app(self):
        N = Notice()
        res = N.login(device_Id='13eef3bfa53445de902f30012de1cbbd', os_type='Android')
        N.assert_ok(res,True)
        print(res)


    @allure.story('设置黑名单,拉黑')
    @allure.title('拉黑')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forward')
    def test_setBlackList(self):
        '''设置黑名单,拉黑'''
        Api = Forth_Operation()
        r = Api.black_list(2686548,0)
        Api.assert_ok(r,'ok')
        print(r)


    @allure.story('获取剩余的茅豆')
    @allure.title('剩余的茅豆')
    @allure.issue('http://10.1.3.253/issues/24622')
    @allure.testcase('http://10.1.3.253/issues/24622')
    @pytest.mark.usefixtures('login_forward')
    def test_getmaodou(self):
        '''剩余的茅豆'''
        r = app_msg.get_maodou()
        app_msg.assert_maodou(r,'获取成功')
        print(r)

    @allure.story('获取猜你感兴趣')
    @allure.title('猜你感兴趣')
    @allure.issue('http://10.1.3.253/issues/24622')
    @allure.testcase('http://10.1.3.253/issues/24622')
    @pytest.mark.usefixtures('login_forward')
    def test_guestinters(self):
        '''猜你感兴趣'''
        r = app_msg.guest_inters()
        app_msg.assert_inters(r,'ok')
        print(r)



    @allure.story('消息中心分类列表')
    @allure.title('分类列表')
    @allure.severity('block')
    @allure.testcase('http://10.1.3.253/issues/24622')
    @allure.issue('http://10.1.3.253/issues/24622')
    @pytest.mark.usefixtures('login_forward')
    def test_msgcategory(self):
        '''消息中心分类列表'''
        res = app_msg.msg_category()
        app_msg.assert_msg(res,26)
        print(res)


    @allure.story('聊天、创建团队并获取历史聊天记录')
    @allure.title('聊天记录')
    @allure.issue('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.testcase('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.severity('crivial')
    @pytest.mark.usefixtures('login_forward')
    def test_chatcord(self):
        '''聊天、创建团队并获取历史聊天记录'''
        r = app_msg.get_chatrecord(gid=47000,to_uid=4769524,max_id=0)
        app_msg.assert_chatcord(r,0)
        print(r)

    @allure.story('聊天列表数据')
    @allure.title('列表数据')
    @allure.issue('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.testcase('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.severity('normal')
    @pytest.mark.usefixtures('login_forward')
    def test_chatlist(self):
        '''聊天列表数据'''
        r = app_msg.get_chatlist()
        app_msg.assert_chatlist(r,'ok')
        print(r)

    @allure.story('获取消息中心未读数')
    @allure.title('消息中心未读数')
    @allure.issue('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.testcase('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.severity('normal')
    @pytest.mark.usefixtures('login_forward')
    def test_unread(self):
        '''获取消息中心未读数'''
        r = app_msg.get_unreadmsg()
        app_msg.assert_unread(r,0)
        print(r)

    @allure.story('获取群发消息')
    @allure.title('群发消息')
    @allure.issue('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.testcase('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.severity('normal')
    @pytest.mark.usefixtures('login_forward')
    def test_groupsend(self):
        '''群发消息'''

        res=app_msg.add_groupsend(content='你好,社会!',text_type=0)
        print(res)

    @allure.story('获取群发消息')
    @allure.title('群发消息')
    @allure.issue('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.testcase('http://10.1.3.253/projects/www-hrloo-com/issues')
    @allure.severity('normal')
    @pytest.mark.usefixtures('login_forward')
    @pytest.mark.parametrize('test_data',admire_data['admire'])
    def test_admire(self,test_data):
        # r = app_msg.get_admire(touid='1430152',moduleid = 9 ,itemid = 1430152,fee =1)
        r = app_msg.get_admire(touid=test_data['touid'],moduleid =test_data['moduleid']  ,itemid =test_data['itemid'] ,fee =test_data['fee'] )
        # app_msg.assert_admire(r,'赞赏成功!')
        # print(r['data']['msg'])
        print(r)





