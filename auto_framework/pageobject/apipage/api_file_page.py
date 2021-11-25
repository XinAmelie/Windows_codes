import copy
import os
import re

from core.apibase import ApiBase
from core.logger import Logger
from core.utils import read_yaml
from urllib.parse import urljoin
from exts.comExts.database_oper import MysqlHelp
from config.settings import Settings as ST
from pageobject.apipage.api_login_page import ApiLogin

logger = Logger('api_file_page.py').getLogger()

file_page = read_yaml(ST.FILE_INFO)['FilePage']


class ApiFile(ApiLogin):

    def __init__(self):
        super().__init__()
        self.login('test01','1111')

    def select_db_info(self,sql):
        '''查询数据库'''
        dbInfo = read_yaml(ST.CASEDATA)['DBinfo']
        db = MysqlHelp(dbInfo['host'],dbInfo['user'],dbInfo['passwd'],dbInfo['port'],dbInfo['database'])
        res = db.select_fetchall(sql)
        return res

    def api_add_folder(self,name,desc):
        '''新增文件夹'''
        logger.info("新增文件夹接口调用开始")
        #1.获取yaml文件中的接口数据
        add_api = copy.deepcopy(file_page['add_folder'])
        #2.模拟添加稿件请求
        #（1）准备接口请求数据
        add_url = urljoin(ST.SERVER,add_api['url'])
        add_data = add_api['data']
        add_data['_20_name'] = name
        add_data['_20_description'] = desc
        #（2）发送请求
        res = self.post(add_url,data=add_data,params=add_api['query_string'],headers=add_api['header'])
        assert res.status_code == 200,'稿件新增接口调用失败！'
        return res.text

    def select_folder(self):
        '''查询文件夹是否存在'''
        logger.info("查询文件夹是否存接口调用开始")
        #1.获取yaml文件中的接口数据
        add_folder = copy.deepcopy(file_page['add_folder'])
        #2.模拟添加稿件请求
        #（1）准备接口请求数据
        add_url = urljoin(ST.SERVER,add_folder['url'])
        #（2）发送请求
        res = self.get(add_url,headers=add_folder['header'])
        assert res.status_code == 200,'查询文件夹是否存接口调用失败！'
        #（3）正则提取数据
        folder_info = re.findall('&_20_struts_action=%2Fdocument_library%2Fview&_20_folderId=(.*?)">(.*?)</a>', res.text)
        logger.info("查询文件夹是否存接口调用结束")
        return folder_info

    def api_dele_folder(self,name):
        '''删除文件夹'''
        logger.info("删除文件夹接口调用开始")
        #1.获取yaml文件中的接口数据
        dele_api = copy.deepcopy(file_page['dele_folder'])
        #2.模拟添加稿件请求
        #（1）准备接口请求数据
        dele_url = urljoin(ST.SERVER,dele_api['url'])
        dele_query = dele_api['query_string']
        #（2）根据名称查询id
        sele_info = self.select_folder()
        id = None
        for i in sele_info:
            if name in i:
                id = i[0]
        dele_query['_20_folderId'] = id
        #（3）发送请求
        res = self.post(dele_url,params=dele_query,headers=dele_api['header'])
        assert res.status_code == 200,'删除文件夹接口调用失败！'
        logger.info("删除文件夹接口调用结束")
        return res.text

    def upload_file(self,rename,desc):
        '''上传文档'''
        logger.info("上传文档接口调用开始")
        #1.获取yaml文件中的接口数据
        file_upload = copy.deepcopy(file_page['file_upload'])
        #2.模拟添加稿件请求
        #（1）准备接口请求数据
        upload_url = urljoin(ST.SERVER,file_upload['url'])
        upload_data = file_upload['data']
        upload_data['_20_title'] = rename.split('.')[0]
        upload_data['_20_description'] = desc
        #（2）获取文件夹id
        first_id = self.select_folder()[0][0]
        upload_data['_20_redirect'] = upload_data['_20_redirect'] + first_id
        upload_data['_20_folderId'] = first_id
        #（3）构造file参数
        file = {
            "_20_file": ("upload_file.txt", open(ST.UPLOADFILE, "r"), "text/plain")
        }
        #（4）发送请求
        res = self.post(upload_url,data=upload_data,files=file,
                        params=file_upload['query_string'],headers=file_upload['header'])
        assert res.status_code == 200,'上传文档接口调用失败！'
        logger.info("上传文档接口调用结束")
        return res.text

    def select_file(self,rename):
        '''文档查询'''
        logger.info("文档查询接口调用开始")
        #1.获取yaml文件中的接口数据
        select_file = copy.deepcopy(file_page['select_file'])
        #2.模拟添加稿件请求
        #（1）准备接口请求数据
        select_url = urljoin(ST.SERVER,select_file['url'])
        select_query = select_file['query_string']
        select_query['_20_keywords'] = rename.split('.')[0]
        #（2）获取文件夹id
        first_id = self.select_folder()[0][0]
        select_query['_20_redirect'] = select_query['_20_redirect'] + first_id
        select_query['_20_breadcrumbsFolderId'] = first_id
        select_query['_20_searchFolderId'] = first_id
        #（3）发送请求
        res = self.get(select_url,
                        params=select_query,headers=select_file['header'])
        assert res.status_code == 200,'文档查询接口调用失败！'
        logger.info("文档查询接口调用结束")
        return res.text

    def download_file(self,rename):
        '''文档下载'''
        logger.info("文档下载接口调用开始")
        #1.获取下载链接
        select_res = self.select_file(rename.split('.')[0])
        #正则提取下载数据
        down_url = re.findall('<td align="left" class="col-3" colspan="1" valign="middle">\\r<a href="(.*?)">{}</a>'.format(rename.split('.')[0]), select_res)[0]
        #2.发送请求
        res = self.get(down_url)
        assert res.status_code == 200,'文档下载接口调用失败！'
        filename = os.path.join(ST.DOWN_FILE,rename)
        with open(filename, "wb") as f:
            f.write(res.content)
        logger.info("文档下载接口调用结束")

    def delete_file(self,rename):
        '''文档删除'''
        logger.info("文档删除接口调用开始")
        #1.获取yaml文件中的接口数据
        delete_file = copy.deepcopy(file_page['delete_file'])
        #2.模拟添加稿件请求
        #（1）准备接口请求数据
        del_url = urljoin(ST.SERVER,delete_file['url'])
        del_query = delete_file['query_string']
        #（2）获取文件夹id
        res_text = self.select_file(rename)
        fix_name = rename.split('.')[0]
        down_url = re.findall('<td align="left" class="col-3" colspan="1" valign="middle">\\r<a href="(.*?)">{}</a>'.format(fix_name), res_text)[0]
        down_query = down_url.split('?')[1].split('&')[-2:]
        folderId = down_query[0].split('=')[1]
        del_query['_20_redirect'] = del_query['_20_redirect'].replace('{id}',folderId)
        del_query['_20_redirect'] = del_query['_20_redirect'].replace('{keywords}',fix_name)
        del_query['_20_folderId'] = down_query[0].split('=')[1]
        del_query['_20_name'] = down_query[1].split('=')[1]
        #（3）发送请求
        res = self.post(del_url,
                        params=del_query,headers=delete_file['header'])
        assert res.status_code == 200,'文档删除接口调用失败！'
        logger.info("文档删除接口调用结束")
        return res.text

    def assert_addfolder_page(self,name):
        '''断言页面：文件夹新增'''
        select_info = self.select_folder()[0]
        assert name in select_info,'【断言页面接口】:文件夹新增失败：{}'.format(select_info)
        logger.info("【断言页面接口】:文件夹新增成功：{}".format(select_info))

    def assert_addfolder_database(self,name,desc):
        '''断言数据库：文件夹新增'''
        res = self.select_db_info('SELECT `name`,description FROM dlfolder ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == name, '【断言数据库】:文件夹名称验证失败：{}'.format(res[0])
        logger.info("【断言数据库】:文件夹名称验证成功：{}".format(res[0]))
        assert res[1] == desc, '【断言数据库】:文件夹描述验证失败：{}'.format(res[1])
        logger.info("【断言数据库】:文件夹描述验证成功：{}".format(res[1]))

    def assert_delfolder_page(self):
        '''断言页面：文件夹删除'''
        select_info = self.select_folder()
        assert select_info == [],'【断言页面接口】:文件夹删除失败：{}'.format(select_info)
        logger.info("【断言页面接口】:文件夹删除成功：{}".format(select_info))

    def assert_upload_page(self,res,rename):
        '''断言页面：文档上传'''
        #正则提前页面中的文件名，描述信息
        rename = rename.split('.')[0]
        rename_info = re.findall('<input  id="_20_title" name="_20_title" style="width: 350px; " type="text" value="(.*?)"',res)[0]
        assert rename == rename_info,'【断言页面接口】:文档上传验证-标题失败：{}'.format(rename_info)
        logger.info("【断言页面接口】:文档上传验证-标题成功：{}".format(res[1]))

    def assert_upload_database(self,rename,desc):
        '''断言数据库：文档上传'''
        rename = rename.split('.')[0]
        res = self.select_db_info('SELECT title,description FROM dlfileentry ORDER BY createDate DESC LIMIT 1;')[0]
        assert res[0] == rename.split('.')[0], '【断言数据库】:文档上传验证-标题失败：{}'.format(res[0])
        logger.info("【断言数据库】:文档上传验证-标题成功：{}".format(res[0]))
        assert res[1] == desc, '【断言数据库】:文档上传验证-描述验证失败：{}'.format(res[1])
        logger.info("【断言数据库】:文档上传验证-描述验证成功：{}".format(res[1]))

    def assert_download_file(self,rename):
        '''断言文档下载'''
        path = os.path.join(ST.DOWN_FILE,rename)
        is_exist = os.path.exists(path)
        assert is_exist,'文件不存在：{}'.format(path)
        logger.info("【断言】:断言文档下载验证成功：{}".format(path))
        for filename in os.listdir(ST.DOWN_FILE):
            path_i = os.path.join(ST.DOWN_FILE,filename)
            os.unlink(path_i)

    def assert_select_page(self,res,rename):
        '''断言页面：文档查询'''
        rename_info = re.findall('<td align="left" class="col-3" colspan="1" valign="middle">\\r<a href="http://127.0.0.1/group/10779/upload.*?">(.*?)</a>',res)[0]
        fix_name = rename.split('.')[0]
        assert rename_info == fix_name, '【断言数据库】:文档查询失败：{}'.format(rename_info)
        logger.info("【断言页面接口】:文档查询成功：{}".format(rename_info))

    def assert_select_database(self,rename):
        '''断言数据库：文档查询'''
        fix_name = rename.split('.')[0]
        res = self.select_db_info('SELECT COUNT(*) FROM dlfileentry WHERE title = "{}";'.format(fix_name))[0]
        assert res[0] == 1, '【断言数据库】:文档查询失败：{}'.format(res[0])
        logger.info("【断言数据库】:文档查询成功：{}".format(res[0]))

    def assert_del_database(self,rename):
        '''断言数据库：文档删除'''
        fix_name = rename.split('.')[0]
        res = self.select_db_info('SELECT COUNT(*) FROM dlfileentry WHERE title = "{}";'.format(fix_name))[0]
        assert res[0] == 0, '【断言数据库】:文档查询失败：{}'.format(res[0])
        logger.info("【断言数据库】:文档查询成功：{}".format(res[0]))


if __name__ == '__main__':
    af = ApiFile()
    res = af.del_file('qqqq.txt')
    # res1 = af.select_folder()
    print(res)
    # print(res1)
