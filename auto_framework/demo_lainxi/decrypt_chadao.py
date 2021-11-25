#coding = 'utf-8'
from urllib.parse import urljoin
import requests
from  requests import utils
from   demo_lainxi.demo_jsencrypt import ExecJs
from core.logger import Logger


logger = Logger('decrypt_chadao.py').getLogger()

base_url = 'http://zentaomax.demo.zentao.net'

#模拟登录
# #1.先获取登录首页的cookies
url1 = urljoin(base_url, '/user-login.html')
home_res = requests.get(url1)
cookies_dict = requests.utils.dict_from_cookiejar(home_res.cookies)
print(cookies_dict)

#2.获取加密用的随机数字rand
url2 = urljoin(base_url,'/user-refreshRandom.html')
heads1 = {
'Host': 'zentaomax.demo.zentao.net',
'Connection':'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
'Referer': 'http://zentaomax.demo.zentao.net/user-login.html',
'Accept-Encoding': 'gzip, deflate',
}
rand_value = requests.get(url=url2,headers = heads1,cookies = cookies_dict) # 此处加cookies
rand = rand_value.text
print('取到的随机值:%s' % rand)

#3.用python实现js密码加密逻辑
pwd = '123456'
e = ExecJs()
step1 = e.get_encrypt_pwd('md5',pwd) + rand
step2 = e.get_encrypt_pwd('md5', step1)
print('加密的密码:%s'% step2)
#4.请求登录接口
url3 = 'http://zentaomax.demo.zentao.net/user-login.html'

# header3 = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
#             "X-Requested-With": "XMLHttpRequest",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             #'Cookie': 'zentaosid=4e3n6kfm6l311n0e5lpbanc4c2; lang=zh-cn; device=desktop; theme=default; feedbackView=0; tab=my; windowWidth=1669; windowHeight=969'
#             }

header3 = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Host": "zentaomax.demo.zentao.net",
            "Proxy-Connection": "keep-alive",
            "Accept": "application/json, text/javascript, ""*/*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://zentaomax.demo.zentao.net",
            "Referer": "http://zentaomax.demo.zentao.net/user-login.html",
            }
# 该参数开发进行了检验："X-Requested-With": "XMLHttpRequest",

body = {
'account':'demo',
'password':step2,
'passwordStrength':'0',
'referer':'/',
'verifyRand':rand,
'keepLogin':'0',
'captcha':''

      }
r = requests.post(url3, data = body,headers = header3,cookies = cookies_dict) # 此处要data
res = r.json()
print(r.json())


logger.info('开始断言')
assert res['result'] == 'success' ,'登陆失败:{}'.format(res['result'])
print('登陆成功:{}'.format(res['result']))


# "X-Requested-With": "XMLHttpRequest"很重要，不能遗漏(开发校验此参数)
'''
$.get(createLink('user', 'refreshRandom'), function(data)
createLink是把baserl+user-refreshRandom.html
'''
# 用 requests.utils.dict_from_cookiejar()
# 把返回的cookies转换成字典
# rand的地址  url = 'http://zentaomax.demo.zentao.net/user-refreshRandom.html

