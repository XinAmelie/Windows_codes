#!/usr/bin/python3
#coding:utf8
from core.apibase import ApiBase

api = ApiBase()
class Sanmao():
    def login_plat(self,pwd,user):
        '''封装登录函数'''
        url = 'https://passport.hrloo.com/user/login'
        body = {

                'ajax': '1',
                'hold': '1',
                'password': pwd,
                'username': user,

            }

        header = {

            'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8',
            'Cookie': 'fensiNumCount=NaN; _pk_id.1.0d74=492f837df3e4e33f.1629773165.; PHPSESSID=ckvc1rbdpl8199ehcnhf6rd750; Hm_lvt_9a72351d0103e8e2a62c3abba9bb349e=1630630123,1630637641,1630720887,1630721207; Hm_lpvt_9a72351d0103e8e2a62c3abba9bb349e=1630734345; _pk_ref.1.0d74=%5B%22SY%22%2C%22PCSYDHL%22%2C1630734345%2C%22%22%5D; _pk_ses.1.0d74=1'
        }

        api.update_head(headers=header)
        r = api.post(url, data=body,headers=header)
        return r.json()

    def black_list(self,uid):
        '''设置黑名单,拉黑'''
        url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=msg&a=setBlackList'
        para = {
            'to_uid': uid,
            'is_remove': '0'
        }
        r = api.get(url, params=para)
        return r.json()



if __name__ == '__main__':
    s = Sanmao()
    r = s.login_plat('hrloo.com',1406607478)
    print(r)
    # r = s.black_list(2462096)
    # url = 'https://api.hrloo.com/hrloo.php?m=mapi2&c=user&a=left_maodou'
    # r = api.get(url)
    # print(r)

