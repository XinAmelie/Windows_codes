import pytest
from pageobject.apipage.api_login_page import ApiLogin
from core.utils import read_yaml
from config.settings import Settings as ST

case_data =  read_yaml(ST.CASEDATA)['ApiCaseData']


class TestApiCase1():
    '''接口自动化-稿件管理系统：登录功能模块'''

    @pytest.mark.parametrize('case_data',case_data['login'])
    def test_login_case01(self,case_data):
        '''接口自动化用例-用户登录测试'''
        lp = ApiLogin()
        res = lp.login(case_data['username'],case_data['password'])
        lp.assert_login_ok(res,case_data['title'])


class TestApiCase2():
    '''接口自动化-稿件管理系统：稿件管理功能模块'''

    @pytest.mark.parametrize('case_data',case_data['add_article'])
    def test_article_case01(self,loginArt,case_data):
        '''接口自动化用例-稿件增加'''
        loginArt.add_article(case_data['title'],case_data['content'])
        loginArt.assert_add_art(case_data['title'])
        loginArt.assert_add_db(case_data['title'],case_data['content'])

    @pytest.mark.parametrize('case_data',case_data['dele_article'])
    def test_article_case02(self,loginArt,case_data):
        '''接口自动化用例-稿件删除'''
        loginArt.add_article(case_data['title'],case_data['content'])
        loginArt.delete_article(case_data['title'])
        loginArt.assert_dele_art(case_data['title'])
        loginArt.assert_dele_db(case_data['title'])

    @pytest.mark.parametrize('case_data',case_data['select_article'])
    def test_article_case03(self,addArtApi,case_data):
        '''接口自动化用例-稿件查询'''
        addArtApi.select_article(case_data['title'])
        addArtApi.assert_select_art(case_data['title'])
        addArtApi.assert_select_db(case_data['title'])

    @pytest.mark.parametrize('case_data',case_data['edit_article'])
    def test_article_case04(self,addArtApi,case_data):
        '''接口自动化用例-稿件修改'''
        addArtApi.edit_article(case_data['title'],case_data['content'])
        addArtApi.assert_add_art(case_data['title'])
        addArtApi.assert_add_db(case_data['title'],case_data['content'])

    def test_article_case05(self,addArtApi):
        '''接口自动化用例-稿件批准'''
        addArtApi.approved_article()
        addArtApi.assert_approved_art()
        addArtApi.assert_approved_db()

    def test_article_case06(self,addArtApi):
        '''接口自动化用例-稿件到期'''
        addArtApi.expired_article()
        addArtApi.assert_expired_art()
        addArtApi.assert_expired_db()


class TestApiCase3():
    '''接口自动化-稿件管理系统：文件上传下载功能模块'''

    @pytest.mark.parametrize('case_data',case_data['folder_add_del'])
    def test_file_case01(self,loginFile,case_data):
        '''接口自动化用例-新增文件夹，删除文件夹'''
        loginFile.api_add_folder(case_data['name'],case_data['desc'])
        loginFile.assert_addfolder_page(case_data['name'])
        loginFile.assert_addfolder_database(case_data['name'],case_data['desc'])
        loginFile.api_dele_folder(case_data['name'])
        loginFile.assert_delfolder_page()

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case02(self,addFileApi,case_data):
        '''接口自动化用例-文档上传'''
        res = addFileApi.upload_file(case_data['rename'],case_data['desc'])
        addFileApi.assert_upload_page(res,case_data['rename'])
        addFileApi.assert_upload_database(case_data['rename'],case_data['desc'])

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case03(self,uploadApi,case_data):
        '''接口自动化用例-文档查询'''
        res = uploadApi.select_file(case_data['rename'])
        uploadApi.assert_select_page(res,case_data['rename'])
        uploadApi.assert_select_database(case_data['rename'])

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case04(self,uploadApi,case_data):
        '''接口自动化用例-文档下载'''
        uploadApi.download_file(case_data['rename'])
        uploadApi.assert_download_file(case_data['rename'])

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case05(self,uploadApi,case_data):
        '''接口自动化用例-文档删除'''
        uploadApi.delete_file(case_data['rename'])
        uploadApi.assert_del_database(case_data['rename'])