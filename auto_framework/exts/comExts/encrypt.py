import execjs
import os


rootPath = os.path.dirname(__file__)
jsPath = os.path.join(rootPath, "encrypt.js")


class ExecJs(object):

    _instance = False

    def _get_js(self, name):
        js_str = ''
        with open(name, 'r', encoding="utf-8") as f:
            line = f.readline()
            while line:
                js_str = js_str + line
                line = f.readline()
        return js_str

    def get_encrypt_pwd(self, passwd, logincode):
        ctx = execjs.compile(self._get_js(jsPath))
        return ctx.call('get_encrypt_pwd', passwd, logincode)
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls._instance:
    #         return cls._instance
    #     else:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance


if __name__ == "__main__":
    e = ExecJs()
    #qrlzuR1sgbCy6iMCsmlDu/Jhs+aBRo2cYtSQO2t0ZPE+oLmY7ik/I3Tes4Eu0nZR
    print(e.get_encrypt_pwd('123ABCdef*', "zx3nhqeupprmhm2f"))

