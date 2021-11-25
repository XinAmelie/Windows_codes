# 封装一个python执行js方法的类，用于调用js文件中的md5方法

# 1、read()读取整个文件，将文件内容放到一个字符串变量中
# 2、readline()每次读取一行,readline()返回的是一个字符串对象，
# 3、readlines()一次性读取整个文件，自动将文件内容分析成一个行的列表。
import execjs  # js的运行环境
import os
rootpath = os.path.dirname(__file__)
md5_js = os.path.join(rootpath,'md5.js')  # 根目录包含了demo_lainxi
print(md5_js)
class ExecJs(object):
    def _get_js(self, name):
        '''获取读js的内容'''
        js_str = ''
        with open(name, 'r', encoding="utf-8") as f:
            line = f.readline()    # f.readline()
            while line: # 读一行写一行，最后返回js_str的字符串
                js_str = js_str + line
                line = f.readline()
        return js_str

    def get_encrypt_pwd(self, function,*args):
        '''获取加密的密码'''
        ctx = execjs.compile(self._get_js(md5_js))  # compile() 函数将一个字符串编译为字节代码
        print(md5_js)
        return ctx.call(function, *args)   # execjs返回的特有结果函数
# eval()
# 输入参数：source(JS语句)、cwd(路径)
# 返回值：result(语句执行结果)
#
# compile()
# 输入参数：source(JS语句)、cwd(路径)
# 返回值：编译后的对象
#
# call()
# 输入参数：name(要调用的JS方法名称[md5就是一个方法])、*args(方法所需要的参数，可多个)
# 返回值：result(运行方法的返回结果)

if __name__ == "__main__":
    e = ExecJs()
    print(e.get_encrypt_pwd('md5','123456'))
    # 此处的123456是*args传来的形参,对数据类型进行处理