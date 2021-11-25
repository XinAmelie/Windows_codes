import os


class Settings(object):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #根目录
    EXTS_PATH = os.path.join(PROJECT_ROOT, "exts")
    DATA_DIR = os.path.join(PROJECT_ROOT, "data") #data 目录
    PIC_DIR = os.path.join(PROJECT_ROOT, "pic", "contrast") #对比图片路径,都存在pic中
    SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "pic", "screenshots") #错误截图,都存在pic中
    DATA_ZL = os.path.join(PROJECT_ROOT,"data_hrzl") #  存放的上传资料和图片的路径
    TESTCASES = os.path.join(EXTS_PATH,'runApp','testcases.yaml')
    TEMPCASES = os.path.join(EXTS_PATH,'runApp','tempcases.yaml')
    DATABASEINFO = os.path.join(EXTS_PATH,'jdbcTool','dataBaseInfo.yaml')#数据库
    ID2NAME = os.path.join(EXTS_PATH,'picAi','id2name.yaml')#AI训练类
    WEBINFO = os.path.join(DATA_DIR,'webdata','locator_info.yaml')#WEB元素信息
    CASEDATA = os.path.join(DATA_DIR,'caseData.yaml')#测试用例数据
    UPLOADFILE = os.path.join(DATA_DIR,'tempfile','upload_file.txt')#测试用例文件
    LOGIN_INFO = os.path.join(DATA_DIR,'apidata','api_login.yaml')#登录接口数据
    LOGIN_INFO_SANMAO = os.path.join(DATA_DIR,'apidata','api_sanmao.yaml')# 三茅登录接口信息
    UPLOAD_HR = os.path.join(DATA_DIR,'apidata','api_hr_files.yaml') #三茅上传文件/图片
    ARTICLE_INFO = os.path.join(DATA_DIR,'apidata','api_article.yaml')#稿件接口数据
    FILE_INFO = os.path.join(DATA_DIR,'apidata','api_file.yaml')#文件上传接口数据
    API_DATA = os.path.join(DATA_DIR,'apidata','api_data.yaml')#接口的参数数据
#------------------------客户端自动化参数配置----------------------------#
    duration = 0.25  # 设置鼠标移动速度；0为立即执行
    interval = 0.25  # 每次点击间隔时间；0为立即执行
    minSearchTime = 5  # 隐试等待时间
    confidence = 0.97  # 设置图片识别信任度
    grayscale = True

# -------------------------AI自动化参数配置-----------------------------#
    AI_SERVER = 'http://127.0.0.1:5000/predict/'
    DEVICE = 'cpu'
    AICONF = 0.5

#############以下自定义配置#####################################################
    SERVER = 'https://api.hrloo.com'
    SANMAO_SERVER_FILES = 'https://www.hrloo.com'
    SANMAO_HR_ZL = 'https://zl.sanmao.com'
    SANMAO_SERVER = 'https://passport.hrloo.com'
    SERVER_APP = 'https://pcdyycs-design.a.onein.cn'
    BROWSER = 'chrome' #ie、firefox、chrome
    DBPATH = ''
    DOWN_FILE = r'C:\Users\Admin\Downloads'
