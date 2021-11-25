import os,time
import pyautogui
try:
    while True:
            print("Press Ctrl-C to end")
            x,y = pyautogui.position() #返回鼠标的坐标
            posStr="Position:"+str(x)+','+str(y)
            print (posStr)#打印坐标
            time.sleep(0.2)
            os.system('cls')#清楚屏幕
except  KeyboardInterrupt:
    print ('end....')