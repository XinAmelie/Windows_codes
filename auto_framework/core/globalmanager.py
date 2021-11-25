class GlobalManager(object):
    """模块间共享变量"""
    _globaldict = {}
    _instance = False

    def get_value(self, name):
        try:
            return self._globaldict[name]
        except KeyError as e:
            print("获取的变量名称：{}不存在！！！！！！！！！！！！！！！".format(name))
            return None

    def set_value(self, name, value):
        self._globaldict[name] = value

    def __new__(cls, *args, **kwargs):
        if cls._instance == False:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

if __name__ == "__main__":
    globalm = GlobalManager()

