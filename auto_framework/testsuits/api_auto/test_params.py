from config.settings import Settings as ST
from core.utils import read_yaml
import pytest
from core.apibase import ApiBase


api = ApiBase()
apiInfo = read_yaml(ST.API_DATA)['test_data1']

# test_data = [
#
#     ('', {'result': result, 'resultcode': 1, 'msg': '参数不正确', 'errormsg': ''}),
#     (333333, {'result': False, 'resultcode': 2, 'msg': '课程不存在', 'errormsg': '' }),
#     (214, {'result': True, 'resultcode': 0, 'msg': '获取成功', 'errormsg':''})
#                     ]

@pytest.mark.parametrize('test_input,expect',apiInfo)
def test_params(login_forwards,test_input,expect):
    url = 'https://api.hrloo.com/hrloo.php?m=class&c=group&a=course_play_info'
    paras = {
            'course_id':test_input
            }

    r = api.get(url,params=paras)
    print(r.json())
    assert  r.json()['result'] == expect['result']
    assert  r.json()['resultcode'] == expect['resultcode']
    assert  r.json()['msg'] == expect['msg']