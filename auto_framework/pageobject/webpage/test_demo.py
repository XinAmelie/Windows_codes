from core.guibase import GuiBase
from core.webbase import WebBase
from core.utils import read_yaml
from config.settings import Settings as ST
import time
gui = GuiBase()
webInfo = read_yaml(ST.WEBINFO)['sanmao']



def test_pic(driver):
    driver.implicitly_wait(5)
    web = WebBase(driver)
    driver.maximize_window()
    url = 'https://passport.hrloo.com/user/login?referer=https%3A%2F%2Fwww.hrloo.com&wx_check_login=no_check'
    driver.get(url)
    web.click(webInfo["pass_login"])
    web.sendKeys(webInfo["username"], 1907753493  )
    web.sendKeys(webInfo["password"], 'hrloo.com')
    web.click(webInfo['login_button'])
    # lg.sanmao_login(driver,1907753493,'hrloo.com')
    time.sleep(5)
    hand1 = driver.window_handles
    web.switch_handle(hand1[-1])
    time.sleep(2)
    gui.click_picture('test_pic',clicks=2,button='left')
    driver.quit()
