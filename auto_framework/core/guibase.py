import sys
import time
import pyautogui
import pyperclip
from core.utils import *
from core.logger import Logger
from config.settings import Settings as ST

logger = Logger('guibase.py').getLogger()


class GuiBase(object):
    SCREENSIZE = (1920, 1080)

    def __init__(self):
        self.duration = ST.duration  # 设置鼠标移动速度；0为立即执行
        self.interval = ST.interval  # 每次点击间隔时间；0为立即执行
        self.minSearchTime = ST.minSearchTime  # 隐试等待时间
        self.confidence = ST.confidence  # 设置图片识别信任度
        self.grayscale = ST.grayscale
        self.pic_path = init_pic_path(ST.PIC_DIR)


    def click_picture(self, el, clicks=1, button='left', isclick=True):
        """点击图片方法"""
        pos_x_y = self.isexist(el)
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
        """图像的相对位置,然后偏移点击：就是先定位到图片，然后相对移动"""
        pos_x_y = self.isexist(el)
        if not pos_x_y:
            self._error_record(el, "rel_picture_click")
        pyautogui.moveTo(*pos_x_y, duration=self.duration)  # 移动到 (100,100)
        pyautogui.move(rel_x, rel_y, duration=self.duration)  # 从当前位置右移100像素
        if isclick == True:
            pyautogui.click(clicks=clicks, button=button, duration=self.duration)
        logger.debug('查找图片{}, 位置{}, 偏移{},点击{}, 成功'.format(el, pos_x_y, (rel_x, rel_y), isclick))

    def isexist(self, el, searchTime=None):
        """检查图片是否呈现在当前屏幕"""
        picPath = self._is_file_exist(el)
        if not searchTime:
            searchTime = self.minSearchTime
        coordinates = pyautogui.locateOnScreen(picPath, minSearchTime=searchTime,
                                               confidence=self.confidence, grayscale=True)
        if coordinates:
            logger.debug('查找对象{}存在'.format(el.split('.')[0]))
            return pyautogui.center(coordinates)
        logger.debug('查找对象{}不存在'.format(el.split('.')[0]))
        return None

    def _is_file_exist(self, el):
        """检查json中读取的图片名称获取全路径后是否存在"""
        abs_path = self.pic_path.get(el)
        if not abs_path:
            raise FileNotFoundError('el:{} 不存在检查文件名'.format(el))
        return abs_path

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
        '''文本输入'''
        pyautogui.write(*args)
        logger.debug('文本框输入{}'.format(*args))

    def hotkey(self, *keys):
        '''组合键'''
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


    @classmethod
    def screen_size_check(cls):
        if cls.SCREENSIZE != pyautogui.size():
            logger.debug("SystemError:plz use 1080p resolution")
            sys.exit(1)
        else:
            print("screen resolution {}\nrun test...............".format(pyautogui.size()))

    def _error_record(self, name, type):
        pyautogui.screenshot(os.path.join(ST.SCREENSHOT_DIR, name))
        logger.error('类型：{},查找图片 {} 位置, 当前屏幕无此内容，已截图'.format(type, name))
        raise pyautogui.ImageNotFoundException

    @staticmethod
    def always_get_position():
        '''获取当前位置'''
        while True:
            time.sleep(1)
            x, y = pyautogui.position()
            print(x, y)
