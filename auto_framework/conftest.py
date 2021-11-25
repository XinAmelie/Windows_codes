#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import base64
import pytest
from io import BytesIO
from py.xml import html
from PIL import ImageGrab
from selenium import webdriver
from core.utils import write_yaml
from config.settings import Settings as ST
import time

insert_js_html = False
report_result = {}

# _driver = None （driver用function需要把它注释掉,用sessio则打开，去掉前置中的_driver = None）



def pytest_addoption(parser):
    '''添加命令行参数--browser、--host'''
    parser.addoption(
        "--browser", action="store", default=ST.BROWSER, help="browser option: firefox or chrome or ie"
             )
    # 添加host参数，设置默认测试环境地址
    parser.addoption(
        "--host", action="store", default=ST.SERVER, help="test host->http://10.11.1.171:8888"
    )

# 此方法失灵的时候需要重启pycharm;注意此代码只能在conftest.py中才有作用
# def  pytest_addoption(parser):
#     '''定一个命里行的参数'''
#     parser.addoption(
#         "--cmdhost",
#         default="https://api.hrloo.com",
#         action = "store",
#         help = 'test case project host address'
#
#              )
#
# @pytest.fixture(scope='session',autouse=True)
# def get_cmdhost(request):
#     os.environ['xadd_host']=request.config.getoption('--cmdhost')
#     print('目前现在的输入的host的地址： %s' % os.environ['xadd_host'])



def pytest_html_results_summary(prefix, summary, postfix):
    '''Summary部分在此设置'''
    prefix.extend([html.p("测试开发组: 搬砖人--王新科")])


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    if hasattr(report,'description'):
        cells.insert(1, html.td(report.description))
        cells.pop()
    else:
        print("!!!!!!!!",report.longreprtext)


@pytest.fixture(scope='session')
def host(request):
    '''全局host参数'''
    return request.config.getoption("--host")



options = webdriver.ChromeOptions()

# options.add_argument('--headless')  #无头模式是不打开浏览器
options.add_argument('--disable-gpu')
options.add_argument("window-size=1024,768")
#添加沙盒模式，适用于root的情况下
options.add_argument("--no-sandbox")










## 想要html截图则需要注释掉allure截图的钩子函数
# @pytest.fixture(scope='session')
@pytest.fixture(scope='function')
def driver(request):
    '''定义全局driver参数'''
    global _driver
    _driver = None
    if _driver is None:
        name = request.config.getoption("--browser")
        if name == "firefox":
            _driver = webdriver.Firefox(executable_path=os.path.join(ST.PROJECT_ROOT, "tools", "geckodriver.exe"))
        # windows驱动
        elif name == "chrome":
            _driver = webdriver.Chrome(executable_path=os.path.join(ST.PROJECT_ROOT, "tools", "chromedriver.exe"))
        # Liunx驱动
        # elif name == "chrome":
        #     _driver = webdriver.Chrome(executable_path=os.path.join(ST.PROJECT_ROOT, "tools", "chromedriver"),chrome_options=options)

        elif name == "ie":
            _driver = webdriver.Ie(executable_path=os.path.join(ST.PROJECT_ROOT, "tools", "IEDriverServer.exe"))
        _driver.implicitly_wait(5)
        print("正在启动浏览器名称：%s" % name)
    def fn():
        print("当全部用例执行完之后：teardown quit driver！")
        _driver.quit()
    request.addfinalizer(fn)
    # return _driver
    yield _driver



def _capture_screenshot():
    output_buffer = BytesIO()
    img = ImageGrab.grab()
    img.save(output_buffer, "png")
    bytes_value = output_buffer.getvalue()
    output_buffer.close()
    return base64.b64encode(bytes_value).decode()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """当测试失败的时候，自动截图，展示到html报告中"""
    outcome = yield
    pytest_html = item.config.pluginmanager.getplugin('html')
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):  # 失败截图
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="lookimg(this.src)" align="right"/></div>' % screen_img
                #每条用例执行都会反复插入下面这段js
                script = '''
                <script>
                    function lookimg(str)
                    {
                        var newwin=window.open();
                        newwin.document.write("<img src="+str+" />");
                    }
                </script>
                '''
                extra.append(pytest_html.extras.html(html))
                if not insert_js_html:
                    extra.append(pytest_html.extras.html(script))
    report.extra = extra
    report.description = str(item.function.__doc__)


def pytest_collection_modifyitems(session, config, items):
    '''收集用例后修改'''
    if '--co' in config.invocation_params.args:
        testcases = {}
        for item in items:
            case_class_name = '::'.join(item.nodeid.split("::")[0:2])
            case_name = item.nodeid.split("::")[-1]
            if not testcases.get(case_class_name, None):
                testcases[case_class_name] = {}
            if not testcases[case_class_name].get('comment', None):
                testcases[case_class_name]['comment'] = item.cls.__doc__
            testcases[case_class_name][case_name] = item.function.__doc__
        tempcases_path = ST.TEMPCASES
        write_yaml(tempcases_path, testcases)





# allure报告失败的截图 [只截取web自动化的截图，需要接口自动化的截图需要把allure的代码注释掉]

import allure

_driver = None

res = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
r2 = os.path.join(res,'testsuits','api_auto')
print(r2)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    获取每个用例状态的钩子函数
    :param item:
    :param call:
    :return:
    '''
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # 添加allure报告截图
        if hasattr(_driver, "get_screenshot_as_png"):
            with allure.step('添加失败截图...'):
                allure.attach(_driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)



'''
@pytest.fixture(scope='session',autouse=True)
def browser():
    global _driver
    if _driver is None:
        _driver =webdriver.Chrome(executable_path=os.path.join(ST.PROJECT_ROOT, "tools", "chromedriver.exe"))
    yield _driver
    print("结束了，该关闭窗口了")
    _driver.quit()
'''








