'''AI-图像识别-获取接口信息'''
import time
import requests
from PIL import ImageGrab
import base64
from config.settings import Settings as ST
from core.utils import read_yaml

id2name = read_yaml(ST.ID2NAME)


class AiServe():

    def __init__(self):
        self.device = ST.DEVICE
        self.minSearchTime = ST.minSearchTime
        self.confidence = ST.AICONF
        self.id2name = id2name
        self.results = []

    def get_weight_name(self,btnName):
        '''获取权重文件名'''
        for k,v in self.id2name.items():
            if btnName in v.values():
                return k

    def ai_pic_base64(self):
        '''图片转base64格式'''
        current_screen = ImageGrab.grab()
        current_screen.save("aiTemp.png")
        f = open('aiTemp.png', 'rb')
        img_b64encode = base64.b64encode(f.read())
        s = img_b64encode.decode()
        picbase64 = 'data:image/png;base64,%s' % s
        return picbase64

    def ai_post_predict(self,btnName):
        '''向服务端发送请求'''
        try:
            start = time.time()
            weights = self.get_weight_name(btnName)
            while True:
                picbase64 = self.ai_pic_base64()
                header = {
                    'Content-Type':'application/json'
                }
                id2name_str = str(id2name[weights])
                json = {
                    "image": picbase64,
                    "id2name": id2name_str,
                    "weights": weights,
                    "device": self.device
                }
                res = requests.post(url=ST.AI_SERVER,headers=header,json=json)
                if res.json()['results'] or time.time() - start > self.minSearchTime:
                    self.results = res.json()['results']
                    return self.results
        except Exception as e:
            raise e

    def is_btn_exist(self,btnName):
        '''判断按钮是否存在与结果中'''
        btnInfo = {}
        for btn in self.results:
            if btn['name'] == btnName:
                btnInfo = btn
        return btnInfo

    def get_btn_coordinates(self,bbox):
        '''获取按钮坐标'''
        x = int(bbox[0] + (bbox[2] - bbox[0])/2)
        y = int(bbox[1] + (bbox[3] - bbox[1])/2)
        return x,y

    def ai_isexist(self,btnName):
        try:
            btnInfo = self.is_btn_exist(btnName)
            if not btnInfo:
                self.ai_post_predict(btnName)
                btnInfo = self.is_btn_exist(btnName)
            if btnInfo and float(btnInfo['conf']) >= self.confidence:
                coordinates = self.get_btn_coordinates(btnInfo['bbox'])
                return coordinates
        except Exception as e:
            raise e


if __name__ == '__main__':
    weights = 'zflogin.pt'
    ai = AiServe()
    res = ai.ai_isexist('username')
    print(res)


