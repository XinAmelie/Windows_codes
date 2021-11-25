import pytest
import sys
import os
import multiprocessing
import ctypes
from exts.runApp.app import run
from config.settings import Settings as ST
from core.utils import read_yaml
from contextlib import contextmanager


@contextmanager
def output_to_null():
    f = open(os.devnull, 'w')
    saved_stdout= sys.stdout
    sys.stdout = f
    yield
    sys.stdout = saved_stdout


def run_collect_testcase(v):
    with output_to_null():
        try:
            # res = pytest.main(['-s', '-q', '--co', './testsuits/'])
            res = pytest.main(['-s','-q','--co','./testsuits/'])    # 执行testsuits下的用例
            # os.system("allure generate  ./  --clean-alluredir -o allure_report/allure_result")

        except Exception as e:
            sys.exit('收集用例时发生错误,{}'.format(e))
    if res == 0:
        v.value = True
        print("收集用例成功，生成用例集testcases.yaml")


def run_testcase():
    try:
        datas = read_yaml(ST.TESTCASES)
        testcases = []
        if not datas:
            print("未选择任何用例")
            return
        for module in datas:
            for key in datas[module]:
                if key == "comment":
                    continue
                testcase = key
                testcase = module + "::" + testcase
                testcases.append(testcase)
        pytest.main(['-vs', 'testsuits',*testcases])
        # os.system("allure generate  ./  --clean-alluredir -o report")
    except FileNotFoundError as e:
        print("无用例文件,执行testsuits下所有用例")
        pytest.main(['-vs', 'testsuits'])

        # os.system("allure generate  ./testsuits  --clean-alluredir -o report")



def run_app(name, *args):
    app = multiprocessing.Process(target=name, args=args)
    app.start()
    app.join()


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    v = manager.Value(ctypes.c_bool, False)
    print("正在加载用例集，请稍后...")
    run_app(run_collect_testcase, v)
    if not v.value:
        sys.exit()
    run_app(run)
    run_testcase()




# pytest.main(['-vs','./testsuits/'])  # 执行当前目录下的这里面的用例 , 一定要记住 目录/
# os.system("allure generate  ./testsuits  --clean-alluredir -o report") 系统命令行

# 带参数运行
# 在运行的时候，也可以指定参数运行
# -s：显示程序中的print/logging输出
# -v：丰富信息模式，输出更详细的用例执行信息
# -k：运行包含某个字符的测试用例，eg：pytest -k add xx.py 中包含add的用例
# -q：简单输出模式，不输出环境信息
# -x：出现一条测试用例失败就退出测试，在调试阶段非常有用，当测试用例失败时，应调试通过，而不是继续执行测试用例
