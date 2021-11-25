import pytest
from exts.comExts.read_yaml import read_yaml
from pageobject.apipage.api_article_page import ApiArticle
from pageobject.apipage.api_file_page import ApiFile
from pageobject.apipage.api_login_page import ApiLogin
# from pageobject.webpage.web_file_page import FilePage
from pageobject.webpage.web_login_page import LoginPage
from pageobject.webpage.web_article_page import ArticlePage
from config.settings import Settings as ST
from pageobject.apipage.api_sanmao_login import Sanmao
from pageobject.webpage.sanmao_login import login_sanmao
from pageobject.apipage.api_sanmao import Api_Sanmao_Login,Forth_Operation


s = Sanmao()
webcase_data = read_yaml(ST.CASEDATA)['WebCaseData']
apicase_data = read_yaml(ST.CASEDATA)['ApiCaseData']
sanmao = Api_Sanmao_Login()
Bla = Forth_Operation()



@pytest.fixture(scope="function")
def init_login(driver):
    '''登录前置'''
    lg = LoginPage(driver)
    lg.login("test01","1111")
    yield
    lg.quit()


@pytest.fixture()
def addArt(driver):
    '''新建稿件前置'''
    lg = LoginPage(driver)
    ap = ArticlePage(driver)
    lg.login("test01","1111")
    ap.add_article(webcase_data['select_article'][0]['title'],webcase_data['select_article'][0]['content'])
    yield ap
    ap.delete_article()
    lg.quit()


# @pytest.fixture()
# def addFile(driver):
#     '''新建文件夹前置'''
#     lg = LoginPage(driver)
#     fp = FilePage(driver)
#     lg.login("test01","1111")
#     fp.add_folder(webcase_data['folder_add_del'][0]['name'],webcase_data['folder_add_del'][0]['desc'])
#     yield fp
#     fp.click(["xpath",".//span[text()='文档上传下载']"])
#     fp.del_folder()
#     lg.quit()


# @pytest.fixture()
# def upload(driver):
#     '''文档上传前置'''
#     lg = LoginPage(driver)
#     fp = FilePage(driver)
#     lg.login("test01","1111")
#     fp.add_folder(webcase_data['folder_add_del'][0]['name'],webcase_data['folder_add_del'][0]['desc'])
#     fp.upload_file(webcase_data['upload_file'][0]['rename'],webcase_data['upload_file'][0]['desc'])
#     yield fp
#     fp.click(["xpath",".//span[text()='文档上传下载']"])
#     fp.del_folder()
#     lg.quit()


@pytest.fixture(scope="function")
def loginArt():
    '''登录前置'''
    aa = ApiArticle()
    yield aa


@pytest.fixture(scope="function")
def loginFile():
    '''登录前置'''
    af = ApiFile()
    yield af


@pytest.fixture()
def addArtApi():
    '''新建稿件前置'''
    aa = ApiArticle()
    aa.add_article(apicase_data['select_article'][0]['title'],apicase_data['select_article'][0]['content'])
    yield aa
    aa.delete_article()


@pytest.fixture()
def addFileApi():
    '''新建文件夹前置'''
    af = ApiFile()
    af.api_add_folder(apicase_data['folder_add_del'][0]['name'],apicase_data['folder_add_del'][0]['desc'])
    yield af
    af.api_dele_folder(apicase_data['folder_add_del'][0]['name'])


@pytest.fixture()
def uploadApi():
    '''文档上传前置'''
    af = ApiFile()
    af.api_add_folder(apicase_data['folder_add_del'][0]['name'],apicase_data['folder_add_del'][0]['desc'])
    af.upload_file(apicase_data['upload_file'][0]['rename'],apicase_data['upload_file'][0]['desc'])
    yield af
    af.api_dele_folder(apicase_data['folder_add_del'][0]['name'])


@pytest.fixture(scope='function')
def login_forwards():
    '''登录的前置处理器'''
    r = s.login_plat('hrloo.com',1406607478)
    yield r


@pytest.fixture(scope='session')
def black_list():
    '''拉黑的前置操作，拉黑'''
    s.login_plat('hrloo.com', 110300423)
    r = s.black_list(2462096)
    print('前置已拉黑')
    yield r


@pytest.fixture(scope="function")
def sanmao_log(driver):
    '''登录web自动化前置'''
    lgn = login_sanmao(driver)
    lgn.sanmao_login(110300836,'hrloo.com')


@pytest.fixture(scope='function')
def login_forward():
    '''三茅api登录，数据代码分离版'''
    r = sanmao.sanmao_login(110300724,'hrloo.com')
    print('已登录')
    yield r


def black_list_forward():
    '''拉黑前置'''
    res = Bla.black_list(uid=2686548,is_remove=0)
    yield res


