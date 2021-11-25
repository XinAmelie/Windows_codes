from core.apibase import ApiBase
api = ApiBase()
import pytest
import allure


# pytet test_2.py --alluredir=./allure --clean-alluredir （运行tesst2,清除其他的记录）
# allure test_demo.py --alluredir ./report/allure_raw1 --allure-serverity=blocked\critrial\normal\minor\trivial

@allure.feature('app聊天')
class Test_Appchat():
    '''测试的app聊天，第一步个人主页，第二步猜你感兴趣等等'''

    @allure.story('获取我的茅豆')
    @allure.title('我的剩余茅豆')
    @allure.severity('blocked')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_maodou(self):
        '''获取茅豆'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=user&a=left_maodou'
        r = api.get(url)
        print(r.json())

# 遇到不能注释的情况是你用“中文冒号了"
    @allure.story('获取个人主页')
    @allure.title('个人主页')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_maodou1(self):
        '''获取个人主页'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=uc&a=homePage'
        para={
                'uid':'1980788'
            }
        r = api.get(url,params=para)
        print(r.json())

    @allure.story('猜你感兴趣')
    @allure.title('感兴趣')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_interesting_user(self):
        '''猜你感兴趣'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=uc&a=recommendUsers'
        r = api.get(url)
        print(r.json())

    @allure.story('设置黑名单,拉黑')
    @allure.title('拉黑')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_setBlackList(self):
        '''设置黑名单,拉黑'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=setBlackList'
        para={
                'to_uid':'110302923',
                'is_remove':'0'

                }
        r = api.get(url,params=para)
        print(r.json())


    @allure.story('设置黑名单,取消拉黑(需要先设置前置处理器拉黑)')
    @allure.title('取消拉黑')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('black_list')
    def test_setBlackList1(self):
        '''设置黑名单,取消拉黑(需要先设置前置处理器拉黑)'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=setBlackList'
        para = {
                'to_uid': '2462096',
                'is_remove': '1'

            }
        r = api.get(url, params=para)
        print(r.json())

    @allure.story('获取用户拉黑数据')
    @allure.title('拉黑数据')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_getBlackList(self):
        '''获取用户拉黑数据'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=getBlackList'
        para = {
                'page':'1'
            }
        r = api.get(url,params=para)
        print(r.json())

    @allure.story('消息中心分类列表')
    @allure.title('分类列表')
    @allure.severity('normal')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_msgCenterList(self):
        '''消息中心分类列表'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=msgCenterList'
        r = api.get(url)
        print(r.json())


    # @pytest.mark.skip
    @allure.story('发起聊天、创建团队并获取历史聊天记录')
    @allure.title('聊天、创建团队并获取历史聊天记录')
    @allure.severity('minor')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_startChat(self):
        '''发起聊天、创建团队并获取历史聊天记录'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=startChat'
        body = {

                'gid': '146',
                'to_uid': '3899156',
                'max_id':' 0'

                }
        r = api.post(url,data=body)
        print(r.json())

    @allure.story('聊天列表数据')
    @allure.title('列表数据')
    @allure.severity('minor')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_chatList(self):
        '''聊天列表数据'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=chatList'
        r = api.get(url)
        print(r.json())

    @allure.story('消息中心类型列表数据,消息类型:1=评论与点赞')
    @allure.title('评论与点赞')
    @allure.severity('critical')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_centerDetails(self):
        '''消息中心类型列表数据,消息类型:1=评论与点赞；2=服务通知；3=学习小助手；'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=centerDetails'
        body = {
                    'type':'1',
                    'page':'1'

            }
        r=api.post(url,data=body)
        print(r.json())

    @allure.story('消息中心类型列表数据,消息类型:2=服务通知')
    @allure.title('服务通知')
    @allure.severity('critical')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_centerDetails_1(self):
        '''消息中心类型列表数据,消息类型:1=评论与点赞；2=服务通知；3=学习小助手；'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=centerDetails'
        body = {
                    'type':'2',
                    'page':'1'

            }
        r=api.post(url,data=body)
        print(r.json())

    @allure.story('消息中心类型列表数据,消息类型:3=学习小助手')
    @allure.title('学习小助手')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_centerDetails_3(self):
        '''消息中心类型列表数据,消息类型:1=评论与点赞；2=服务通知；3=学习小助手；'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=centerDetails'
        body = {
                    'type':'3',
                    'page':'1'

            }
        r=api.post(url,data=body)
        print(r.json())

    @allure.story('获取消息中心未读数量')
    @allure.title('消息中心未读数量')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_getMsgUnread(self):
        '''获取消息中心未读数量'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=getMsgUnread'
        r=api.get(url)
        print(r.json())

    @allure.story('上传聊天图片')
    @allure.title('聊天图片')
    @allure.severity('blocked')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    # @pytest.mark.skip
    def test_uploadImg(self,login_forwards):
        '''上传聊天图片'''
        # url ='https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=uploadImg'
        url = 'https://www.hrloo.com/hr/uc/msg/ajax_upload_cp'
        body = {

                "file":"d76c1d9ad54f43929fd96a58058c18d1!400x400.png"
            }
        r = api.post(url,data=body)
        print(r.json())

    @allure.story('获取当前用户群发列表数据')
    @allure.title('群发列表数据')
    @allure.severity('critical')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_groupSendList(self):
        '''获取当前用户群发列表数据'''
        url = "https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=groupSendList"
        para ={
                'page':'1'
            }
        r = api.get(url,params=para)
        print(r.json())

    @allure.story('添加群发消息')
    @allure.title('群发消息')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_setGroupSend(self):
        '''添加群发消息'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=setGroupSend'
        para = {

                'content': 'ddddddddddd',
                'text_type': '0',
                'seo_title': '三茅人力资源网-专业的HR学习交流平台',
                'seo_desc': '三茅人力资源网，是专业的HR学习交流平台，汇集数十万份人力资源六大模块案例资料和完善的人力资源学习课程，吸引了众多HR精英分享人力资源从业经验，更有特色的三茅打卡学习方式，鼓励HR每天学习一个人力资源知识点，建立良好的学习习惯。加入三茅，你将收获知识、导师和朋友，成就更好的自己。',

            }
        res = api.get(url,params=para)
        print(res.json())

    @allure.story('赞赏')
    @allure.title('赞赏')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_admire(self):
        '''赞赏'''

        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=uc&a=admire'
        body ={

                'touid':'你好3108768',
                'fee':'10',
                'moduleid':'9',
                'itemid': '3108768'
            }

        r = api.post(url,data=body)
        print(r.json())

    @allure.story('赞赏1')
    @allure.title('赞赏1')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    def test_admire(self):
        '''赞赏1'''

        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=uc&a=admire'
        body = {

            'touid': '你好3108768',
            'fee': '10',
            'moduleid': '9',
            'itemid': '3108768'
        }

        r = api.post(url, data=body)
        print(r.json())





    @allure.story('app消息推送')
    @allure.title('消息推送')
    @allure.severity('trivial')
    @allure.issue('http://10.1.3.253/issues/25762')
    @allure.testcase('http://10.1.3.253/issues/25762')
    @pytest.mark.usefixtures('login_forwards')
    @pytest.mark.skip
    def test_msgPush(self):
        '''app消息推送'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=msgPush'
        body ={

                'uid':'1980788',
                'content':'333'
            }
        r = api.post(url,data=body)
        print(r.json())


if __name__=="__main__":
    pytest.main(['-s',"--alluredir,./reports/allure","--clean-alluredir"])
