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
            res = pytest.main(['-s', '-q', '--co', 'testsuits'])
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
        pytest.main(['--html=auto_reports.html','-v', '--self-contained-html', *testcases])
    except FileNotFoundError as e:
        print("无用例文件,执行testsuits下所有用例")
        pytest.main(['--html=auto_reports.html', '--self-contained-html', 'testsuits'])


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


# 无法收集的时候是因为有bug
