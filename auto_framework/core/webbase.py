from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from core.logger import Logger

logger = Logger('webbase.py').getLogger()

class WebBase():

    _instance = False
    timeout = 10

    def __init__(self, driver):
        self.driver = driver
        self.t = 0.5

    def get_url(self, url):
        """打开url，最大化窗口"""
        self.driver.get(url)
        self.driver.maximize_window()
        logger.debug("浏览器访问请求地址：%s" % url)

    def findElement(self, locator, timeout=timeout):
        """定位到元素，返回元素对象，没定位到，Timeout异常"""
        try:
            if isinstance(locator, list):
                locator = tuple(locator)
            if not isinstance(locator, tuple):
                logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            logger.debug("正在定位元素信息：定位方式->%s, value值->%s" % (locator[0], locator[1]))
            ele = WebDriverWait(self.driver, timeout, self.t).until(EC.presence_of_element_located(locator))
            logger.debug("定位元素{}成功".format(locator))
            return ele
        except TimeoutException as e:
            logger.error('未定位到元素',locator)
            raise e

    def findElements(self, locator):
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元组类型：loc = ("id", "value1")')
        else:
            try:
                print("正在定位元素信息：定位方式->%s, value值->%s"%(locator[0], locator[1]))
                eles = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_all_elements_located(locator))
                return eles
            except:
                return []

    def sendKeys(self, locator, text=''):
        try:
            ele = self.findElement(locator)
            ele.send_keys(text)
            logger.debug('send keys {} 成功'.format(text))
        except Exception as e:
            logger.error('send keys {} 失败'.format(text))
            raise e

    def click(self, locator):
        try:
            # ele = self.findElement(locator)
            ele = WebDriverWait(self.driver, self.timeout, self.t).until(EC.element_to_be_clickable(tuple(locator)))
            ele.click()
            logger.debug('click {} 成功'.format(locator))
        except Exception as e:
            logger.error('click {} 失败'.format(locator))
            raise e

    def clear(self, locator):
        ele = self.findElement(locator)
        ele.clear()

    def isSelected(self, locator):
        """判断元素是否被选中，返回bool值"""
        ele = self.findElement(locator)
        r = ele.is_selected()
        return r

    def is_title(self, _title=''):
        """返回bool值"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_is(_title))
            print(result.get_attribute("innerHTML"))
            return result
        except:
            return False

    def is_title_contains(self, _title=''):
        """返回bool值"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(_title))
            return result
        except:
            return False

    def is_text_in_element(self, locator, _text=''):
        """返回bool值"""
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element(locator, _text))
            return result
        except:
            return False

    def is_value_in_element(self, locator, _value=''):
        """返回bool值, value为空字符串，返回Fasle"""
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element_value(locator, _value))
            return result
        except:
            return False

    def is_alert(self, timeout=3):
        """判断alert,存在返回alert实例，不存在，返回false"""
        try:
            result = WebDriverWait(self.driver, timeout, self.t).until(EC.alert_is_present())
            return result
        except:
            return False

    def get_title(self):
        """获取title"""
        return self.driver.title

    def get_text(self, locator):
        """获取文本"""
        try:
            t = self.findElement(locator).text
            return t
        except:
            print("获取text失败，返回'' ")
            return ""

    def get_attribute(self, locator, name):
        """获取属性"""
        try:
            element = self.findElement(locator)
            return element.get_attribute(name)
        except:
            print("获取%s属性失败，返回'' "%name)
            return ""

    def js_focus_element(self, locator):
        """聚焦元素"""
        target = self.findElement(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        """滚动到顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self,x=0):
        """滚动到底部"""
        js = "window.scrollTo(%s,document.body.scrollHeight)"%x
        self.driver.execute_script(js)

    def select_by_index(self, locator, index=0):
        """通过索引,index是索引第几个，从0开始，默认选第一个"""
        element = self.findElement(locator)  # 定位select这一栏
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        """通过value属性"""
        element = self.findElement(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        """通过文本值定位"""
        element = self.findElement(locator)
        Select(element).select_by_visible_text(text)

    def switch_iframe(self, id_index_locator):
        """切换iframe"""
        try:
            if isinstance(id_index_locator, int):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, tuple) or isinstance(id_index_locator, list):
                ele = self.findElement(id_index_locator)
                self.driver.switch_to.frame(ele)
            logger.info("iframe 切换为{}".format(id_index_locator))
        except Exception as e:
            logger.error("iframe{}切换异常".format(id_index_locator))
            raise e

    def switch_iframe_out(self):
        """切换iframe"""
        try:
            self.driver.switch_to.default_content()
        except:
            print("iframe切换异常")

    def switch_iframe_up(self):
        """切换iframe"""
        try:
            self.driver.switch_to.parent_frame()
        except:
             print("iframe切换异常")

    def switch_handle(self, window_name):
        self.driver.switch_to.window(window_name)

    def switch_alert(self):
        alert = WebDriverWait.until(EC.alert_is_present())
        return alert

    def move_to_element(self, locator):
        """鼠标悬停操作"""
        ele = self.findElement(locator)
        ActionChains(self.driver).move_to_element(ele).perform()

    def isElementExist(self,locator, timeout):
        try:
            if isinstance(locator, list):
                locator = tuple(locator)
            WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located(locator))
            logger.debug('只查询：查询元素{} 存在'.format(locator))
            return True
        except Exception as e:
            logger.debug('只查询：查询元素{} 不存在'.format(locator))
            return False

    def isShow(self, locator):
        """判断元素是否显示，返回bool值"""
        try:
            ele = self.findElement(locator)
            r = ele.is_displayed()
            return r
        except:
            return False

    def isShow2(self,xpath):
        try:
            ele = self.driver.find_element_by_xpath(xpath)
            r = ele.is_displayed()
            return r
        except:
            return False



