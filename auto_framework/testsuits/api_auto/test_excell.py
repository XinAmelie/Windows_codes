from exts.comExts.read_excel import ExcelRead,ExcelWrite
from core.apibase import ApiBase
import  pytest

api = ApiBase()
# 写入数据
# data = ExcelWrite()
# filepath = r'C:\Users\www\Desktop\test111.xls'
# m = [{'uid':'1999','username':'你好'},
#      {'uid':'200','username':'你不好'},
#      {'uid':'400','username':'我很好'}]
# data.excl_write(m,filepath)
# 获取行或者列的数据
path = r'F:\python3.6.8\projects\auto_framework\testsuits\api_auto\test.xls'
read_data = ExcelRead(path,'Sheet1')
co1 = read_data.get_colinfo('uid')   # 第一列
co2 = read_data.get_colinfo('username')  # 第二列
row2 = read_data.get_rowinfo(2)  # 获取第2行的数据
print(co1,co2,row2)
test_data = [ co1, co2]
# # co1是第一列的uid,co2是第二列的username
@pytest.mark.parametrize('test_input',test_data[0])
@pytest.mark.parametrize('test_input1',test_data[1])
def test_params(login_forwards,test_input,test_input1):
        url = 'https://api.hrloo.com/hrloo.php'
        # m需要username  c需要uid
        pars = {
                'm':test_input,
                'c':test_input1,
                'a':'homePage'

                             }
        print(pars)




