import time
import pyautogui
import pyperclip
from core.utils import *
from core.logger import Logger
from config.settings import Settings as ST
from exts.picAi.ai_recognition import AiServe

logger = Logger('aitestbase.py').getLogger()

ai = AiServe()


class AiBase(AiServe):

    def __init__(self):
        self.duration = ST.duration  # 设置鼠标移动速度；0为立即执行
        self.interval = ST.interval  # 每次点击间隔时间；0为立即执行
        super(AiBase,self).__init__()

    def click_picture(self, el, clicks=1, button='left', isclick=True):
        """点击图片方法"""
        pos_x_y = ai.ai_isexist(el)
        if not pos_x_y:
            self._error_record(el, "click_picture")
        pyautogui.moveTo(*pos_x_y)
        if isclick:
            pyautogui.click(*pos_x_y, duration=self.duration, interval=self.interval, clicks=clicks, button=button)
        logger.debug('移动到图片 {} 位置{}, 点击:{} 成功'.format(el, isclick, pos_x_y))

    def click(self, posx=None, posy=None, clicks=1, button='left'):
        """鼠标点击方法"""
        pyautogui.click(posx, posy, clicks=clicks, button=button, duration=self.duration, interval=self.interval)
        logger.debug('鼠标在坐标{},{} 点击{}键 {}次'.format(posx, posy, button, clicks))

    def rel_click(self, rel_x=0, rel_y=0, clicks=1, button='left'):
        """相对坐标点击"""
        pyautogui.move(rel_x, rel_y)
        pyautogui.click(clicks=clicks, button=button, duration=self.duration, interval=self.interval)
        logger.debug('鼠标在相对坐标{},{} 点击{}键 {}次'.format(rel_x, rel_y, button, clicks))

    def rel_picture_click(self, el, rel_x=0, rel_y=0, clicks=1, button='left', isclick=True):
        """图像的相对位置点击"""
        pos_x_y = ai.ai_isexist(el)
        if not pos_x_y:
            self._error_record(el, "rel_picture_click")
        pyautogui.moveTo(*pos_x_y, duration=self.duration)  # 移动到 (100,100)
        pyautogui.move(rel_x, rel_y, duration=self.duration)  # 从当前位置右移100像素
        if isclick == True:
            pyautogui.click(clicks=clicks, button=button, duration=self.duration)
        logger.debug('查找图片{}, 位置{}, 偏移{},点击{}, 成功'.format(el, pos_x_y, (rel_x, rel_y), isclick))

    def moveto(self, posx=0, posy=0, rel=False):
        """鼠标移动方法"""
        if rel:
            pyautogui.move(posx, posy, duration=self.duration)
            logger.debug('鼠标偏移{},{}'.format(posx, posy))
        else:
            pyautogui.moveTo(posx, posy, duration=self.duration)
            logger.debug('鼠标移动到{},{}'.format(posx, posy))

    def dragto(self, posx, posy, button='left', rel=False):
        """鼠标拖拽"""
        if rel:
            pyautogui.dragRel(posx, posy, duration=self.duration)
            logger.debug('鼠标相对拖拽{},{}'.format(posx, posy))
        else:
            pyautogui.dragTo(posx, posy, duration=self.duration, button=button)
            logger.debug('鼠标拖拽{},{}'.format(posx, posy))

    def type(self, *args):
        pyautogui.write(*args)
        logger.debug('文本框输入{}'.format(*args))

    def hotkey(self, *keys):
        time.sleep(1)
        pyautogui.hotkey(*keys)
        logger.debug("执行快捷键{}".format(keys))

    def press(self, key):
        pyautogui.press(key)

    def scroll(self, amount_to_scroll, moveToX=None, moveToY=None):
        """鼠标滚动"""
        pyautogui.scroll(clicks=amount_to_scroll, x=moveToX, y=moveToY)
        logger.debug('鼠标在{}位置滚动{}值'.format(moveToX, moveToY), amount_to_scroll)

    def input_string(self, text, clear=False):
        """输入中文"""
        pyperclip.copy(text)
        if not clear:
            pyautogui.hotkey('ctrl', 'v')
        logger.debug('{}输入完成'.format(text))

    def _error_record(self, name, type):
        pyautogui.screenshot(os.path.join(ST.SCREENSHOT_DIR, name))
        logger.error('类型：{},查找图片 {} 位置, 当前屏幕无此内容，已截图'.format(type, name))
        raise pyautogui.ImageNotFoundException


if __name__ == '__main__':
    ai = AiBase()
    ai.click_picture("username")
    ai.type('aaa')
    ai.click_picture("password")
    ai.type('bbb')
    ai.click_picture("loginbtn")




