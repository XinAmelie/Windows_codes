import pytest
from pageobject.webpage.web_article_page import ArticlePage
from pageobject.webpage.web_file_page import FilePage
from pageobject.webpage.web_login_page import LoginPage
from core.utils import read_yaml
from config.settings import Settings as ST

case_data =  read_yaml(ST.CASEDATA)['WebCaseData']


class TestCase1():
    '''WEB自动化-稿件管理系统：登录功能模块'''

    @pytest.mark.parametrize('case_data',case_data['login'])
    def test_login_case01(self,driver,case_data):
        '''WEB自动化用例-用户登录测试'''
        lp = LoginPage(driver)
        lp.login(case_data['username'],case_data['password'])
        lp.assert_login_ok(case_data['flag'])


class TestCase2():
    '''WEB自动化-稿件管理系统：稿件管理功能模块'''

    @pytest.mark.usefixtures('init_login')
    @pytest.mark.parametrize('case_data',case_data['add_article'])
    def test_article_case01(self,driver,case_data):
        '''WEB自动化用例-稿件增加'''
        ap = ArticlePage(driver)
        ap.add_article(case_data['title'],case_data['content'])
        ap.assert_add_article(case_data['title'],case_data['content'])
        ap.assert_add_database(case_data['title'],case_data['content'])

    @pytest.mark.parametrize('case_data',case_data['dele_article'])
    @pytest.mark.usefixtures('init_login')
    def test_article_case02(self,driver,case_data):
        '''WEB自动化用例-稿件删除'''
        ap = ArticlePage(driver)
        ap.add_article(case_data['title'],case_data['content'])
        ap.delete_article()
        ap.assert_dele_article(case_data['title'])
        ap.assert_dele_database(case_data['title'])

    @pytest.mark.parametrize('case_data',case_data['select_article'])
    def test_article_case03(self,addArt,case_data):
        '''WEB自动化用例-稿件查询'''
        addArt.select_article(case_data['title'])
        addArt.assert_select_article(case_data['title'])
        addArt.assert_select_database(case_data['title'])

    @pytest.mark.parametrize('case_data',case_data['edit_article'])
    def test_article_case04(self,addArt,case_data):
        '''WEB自动化用例-稿件修改'''
        addArt.edit_article(case_data['title'],case_data['content'])
        addArt.assert_add_article(case_data['title'],case_data['content'])
        addArt.assert_add_database(case_data['title'],case_data['content'])

    def test_article_case05(self,addArt):
        '''WEB自动化用例-稿件批准'''
        addArt.approved_article()
        addArt.assert_approved_page()
        addArt.assert_approved_database()

    def test_article_case06(self,addArt):
        '''WEB自动化用例-稿件到期'''
        addArt.expired_article()
        addArt.assert_expired_page()
        addArt.assert_expired_database()


class TestCase3():
    '''WEB自动化-稿件管理系统：文件上传下载功能模块'''

    @pytest.mark.parametrize('case_data',case_data['folder_add_del'])
    @pytest.mark.usefixtures('init_login')
    def test_file_case01(self,driver,case_data):
        '''WEB自动化用例-新增文件夹，删除文件夹'''
        fp = FilePage(driver)
        fp.add_folder(case_data['name'],case_data['desc'])
        fp.assert_addfolder_page(case_data['name'])
        fp.assert_addfolder_database(case_data['name'],case_data['desc'])
        fp.del_folder()
        fp.assert_delfolder_page()

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case02(self,addFile,case_data):
        '''WEB自动化用例-文档上传'''
        addFile.upload_file(case_data['rename'],case_data['desc'])
        addFile.assert_upload_page(case_data['rename'],case_data['desc'])
        addFile.assert_upload_database(case_data['rename'],case_data['desc'])

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case03(self,upload,case_data):
        '''WEB自动化用例-文档下载'''
        upload.download_file()
        upload.assert_download_file(case_data['rename'])

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case04(self,upload,case_data):
        '''WEB自动化用例-文档查询'''
        upload.select_file(case_data['rename'])
        upload.assert_select_page(case_data['rename'])
        upload.assert_select_database(case_data['rename'])

    @pytest.mark.parametrize('case_data',case_data['upload_file'])
    def test_file_case05(self,upload,case_data):
        '''WEB自动化用例-文档删除'''
        upload.del_file()
        upload.assert_del_page()
        upload.assert_del_database(case_data['rename'])

