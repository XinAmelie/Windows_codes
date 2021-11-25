'''
from selenium import webdriver
import time
from core.webbase import WebBase
from core.utils import read_yaml

from config.settings import Settings as ST


webinfo = read_yaml(ST.WEBINFO)['sanmao']
driver = webdriver.Firefox(executable_path=r'F:\python3.6.8\projects\auto_framework\tools\geckodriver.exe')
driver.maximize_window()
url1 = 'https://passport.hrloo.com/user/login?referer=https%3A%2F%2Fwww.hrloo.com&wx_check_login=no_check'
driver.get(url1)

web = WebBase(driver)
driver.implicitly_wait(5)
# driver.find_element_by_xpath(".//div[@class='new-login']/div[1]/div[1]/span[2]").click()

web.click(webinfo['pass_loginfox'])
time.sleep(2)
driver.find_element_by_xpath(".//p[@class='ps-username fn-login-input-item']/input[1]").send_keys(2008932277)
# web.sendKeys(webinfo['username'],2008932277)
# driver.find_element_by_id('j_username').send_keys(2008932277)
# web.sendKeys(webinfo['username_fox'], 2008932277)
web.sendKeys(webinfo['password'], 'hrloo.com')
web.click(webinfo['login_button'])

'''
import re
# 统计在一个队列中的数字，有多少个正数，多少个负数
a = [1, 3, 5, 7, 0, -1,-9, -4, -5, 8]
m = 0
n = 0
for i in a:
    if i > 0:
        m += 1
    elif i<0:
        n+=1
    else:
        pass
print("正数:%s"% m)
print("负数:%s"% n)

print('-'*30+str("分割线")+'-'*30)

# 字符串 "axbyczdj"，如果得到结果“abcd”
a = 'axbyczdj'
lst = a[::2] # 从0开始，0算第一个
print(lst)

print('-'*30+str("分割线")+'-'*30)

# 字符串切割
a = "hello_world_yoyo"
b = a.split("_")
print(b)

print('-'*30+str("分割线")+'-'*30)
# 已知一个数字为 1，如何输出“0001”

a = 1
print("000%s"%a)
print("%4d"% a)
print("%4.2f"%a)

# 已知一个队列,如： [1, 3, 5, 7], 如何把第一个数字，放到第三个位置，得到：
# [3, 5, 1, 7]

a = [1,3,5,7]
a.insert(3,a[0])
print(a[1:])

#已知 a = 9, b = 8,如何交换 a 和 b 的值，得到 a 的值为 8,b 的值为 9
a = 9
b = 8
a,b = b,a
print("a的值:{}".format(a))
print(b)
for i in range(100,200):
    print(int(i))


# 打印出 100-999 所有的"水仙花数"
# s的目的 153   第一次s的值是1的三次方，第二次是1的三次方值加5的三次值

sxh = []

for i in range(100,1000):
    s = 0
    m = list(str(i))
    for j in m:
        s += int(j)**len(m)
    if i == s:
        print(i)
        sxh.append(i)
print("100-999的水仙花数:{}".format(sxh))



# 求 1000 以内的完全数有哪些


print('-'*30+str("分割线")+'-'*30)
# 排序 sort正序  倒序sort(reverse = True)
a = [1, 3, 6, 9, 7, 3, 4, 6]
a.sort()
print("这是正序的:%s"% a)

b = [1, 3, 6, 9, 7, 3, 4, 6]
b.sort(reverse=True)
print("这是正序的:{}".format(b) )

## set(list) 可以去重，不过返回的是字典格式的
c = [1, 3, 6, 9, 7, 3, 4, 6]
c = list(set(c))
print("去重:%s" % c)

# 递归
# 调用 reduce(f, [1, 3, 5, 7, 9])时，reduce函数将做如下计算：
#
# 先计算头两个元素：f(1, 3)，结果为4；
# 再把结果和第3个元素计算：f(4, 5)，结果为9；
# 再把结果和第4个元素计算：f(9, 7)，结果为16；
# 再把结果和第5个元素计算：f(16, 9)，结果为25；
# 由于没有更多的元素了，计算结束，返回结果25。


from functools import reduce

def digui(x,y):
    return x*y

a = 10
c = reduce(digui,range(1,a+1))
print("{}!的结果:{}".format(a,c))

# 斐波那契数列




# 幂函数 此处定义的x为底数，n为指数
def mi(x,n):
    if n == 0:   # n = 0 幂函数恒等于1
        return 1
    else:
        return x*mi(x,n-1)  # 返回的依然是x的n次方
x = 4
n = 3
print(mi(x,n))

# 汉诺塔

# upper 小写变大写   lower大写变小写  while 1 和 True 1会更快  \_\- 原义字符
# 写一个小程序：控制台输入邮箱地址（格式为 username@companyname.com）， 程序识别用户名和公司名后，将用户名和公司名输出到控制台。
# 要求：
# 1.校验输入内容是否符合规范（xx@yy.com）, 如是进入下一步，如否则抛出提示"incorrect email format"。注意必须以.com 结尾
# 2.可以循环“输入--输出判断结果”这整个过程
# 3.按字母 Q（不区分大小写）退出循环，结束程序

def is_mail_style(x):
    a = re.match(r'^[0-9a-zA-Z\_\-]*@[0-9a-zA-Z]+(\.com)$',x)
    if a:
        gs = re.findall("^(.+?)@",x) # 因为正则匹配的结果是列表
        print("公司的用户名:{}".format(gs[0]))
        print(gs)
        gr = re.findall("@(.+?)\.com",x)
        print(gr)
        print("个人的用户名:{}".format(gr[0]))
        return True
    else:
        print('incorrect email format')

a = input('请输入:')

while 1:
    if a == 'q' or a == 'Q':
        exit()
    else:
        if is_mail_style(a):
            break

    a = input('请输入')

print('请下一步！')





# 4-遍历文件
# fpath 路径  dirname是文件夹名字  files是文件
import os
def get_files(path,rule):
    all = []
    for fpath,dirname,files in os.walk(path):
        for f in files:
            finame = os.path.join(fpath,f)
            if finame.endswith(rule):
                all.append(finame)
    return all

if __name__ == '__main__':

    b = get_files(path='F:\\11',rule='.py')
    for i in b:
        print(i)





# # 统计在一个队列中的数字，有多少个正数，多少个负数，如[1, 3, 5, 7, 0, -1,-9, -4, -5, 8]
# # elif又如果
#
# m =0
# n =0
# lst = [1, 3, 5, 7, 0, -1,-9, -4, -5, 8]
# for i in lst:
#     if i > 0:
#         m += 1
#     elif i<0:
#         n += 1
#     else:
#         pass
#
# print('正数的个数:{}'.format(m))
# print('负数的个数:%s'% n )
#
#
# # 字符串 "axbyczdj"，如果得到结果“abcd”
#
# str2 = 'axbyczdj'
# a = str2[::2]
# print(a)
#
# # 3.字符串切割
# # 已知一个字符串为“hello_world_yoyo”, 如何得到一个队列["hello","world","yoyo"]
# str1 = 'hello_world_yoyo'
# b = str1.split('_')
# print(b)
#
# # 4.格式化输出
# # 已知一个数字为 1，如何输出“0001” a = 1
# a = 1
# print("%04d"% a)
#
# # 5.队列
# # 已知一个队列,如： [1, 3, 5, 7], 如何把第一个数字，放到第三个位置，得到：[3, 5, 1, 7]
# # insert的用法: 需要索引的位置，添加数字
# a = [1, 3, 5, 7]
# a.insert(1,100)
# # lst2 = lst1.insert(1,lst1[1])
# print(a)
#
# # 6.已知 a = 9, b = 8,如何交换 a 和 b 的值，得到 a 的值为 8,b 的值为 9
# a = 9
# b =8
# a,b = b,a
# print("a的值:%s" % a)
# print("b的值:{}".format(b))
#
# # 7.水仙花打印出 100-999 所有的"水仙花数"，
# # 所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。
# # 例如：153 是一个"水仙花数"，因为 153=1 的三次方＋ 5 的三次方＋3 的三次方。
#
# sxh = []
# for i in range(100,1000):
#     s = 0
#     m = list(str(i))
#     for j in m:
#         s += int(j)**len(m)
#
#     if i == s:
#         print(i)
#         sxh.append(i)
# print("100-999的水仙花:{}".format(sxh))
#
# # 10.sort 排序
# #已知一个队列[1, 3, 6, 9, 7, 3, 4, 6]
# '''
# 按从小到大排序
# 按从大大小排序
# 去除重复数字
# '''
# # 正序
# a = [1, 3, 6, 9, 7, 3, 4, 6]
# a.sort()
# print(a)
# # 倒序
# b = [1, 3, 6, 9, 7, 3, 4, 6]
# b.sort(reverse=True)
# print(b)
# # 去重 set是去重,并生成字典的样式
# c = list(set(b))
# print(c)
#
# # 冒泡排序 range(1,10,3) # 1-10 步长3 但是只显示10-1个数     range(7)  就是0开始到7
#
# # 1-7就会有6轮，所以1-n,就会有n-1轮
# '''
# 就拿1到6来举例子吧！这里面有n个数字，你要对其进行从大到小的排序的话,你就要拿相邻的两个数进行比较，如果第一个数比第二个大就交换他们的位置：第二个就和第三个比较，一直这样下去，直到最小的就会在最后面了，然后继续从第一和第二个进行比较，如此下去。
# 第1轮： 1,2,3,4,5,6   2,1,3,4,5,6     2,3,1,4,5,6    2,3,4,1,5,6    2,3,4,5,1,6    2,3,4,5,6,1
# 第2轮：2,3,4,5,6,1   3,2,4,5,6,1     3,4,2,5,6,1    3,4,5,2,6,1    3,4,5,6,2,1
# 第3轮：3,4,5,6,2,1   4,3,5,6,2,1     4,5,3,6,2,1    4,5,6,3,2,1
# 第4轮：4,5,6,3,2,1   5,4,6,3,2,1     5,6,4,3,2,1
# 第5轮：5,6,4,3,2,1  6,5,4,3,2,1
# '''
# # 7个数字，只需要6轮排序，a-i-1   i=0  才等于a-i-1=6
# def maopao(arr):
#     a = len(arr)
#     for i in range(a):
#         for j in range(0,a-i-1):
#             if arr[j] > arr[j+1]:
#                 arr[j],arr[j+1] = arr[j+1],arr[j]
#
# arr = [64, 34, 25, 12, 22, 11, 90]
# maopao(arr)
# for e in arr:
#     print("冒泡排序后的结果:%s"% e)
#
# # 计算n 的阶乘
# from  functools  import reduce
# def digui(x,y):
#     return x*y
# a = 10
# c = reduce(digui,range(1,a+1))
# print("{}!的结果:{}".format(a,c))
#
#
#
# # 幂的递归 x的是底数  n是次方
#
# def mi(x,n):
#     if n == 0:
#         return 1
#
#     else:
#         return x*mi(x,n-1)
# x = 3
# n = 2
# print(mi(x,n))
#
#
# # n的阶乘n!
#
# def digui(x,y):
#     return x*y
# a = 10
# c = reduce(digui,range(1,a+1))
#
# # 幂的运算
# def mi(x,n):
#     if n == 0:
#         return 1
#     else:
#         return x*mi(x,n-1)
# x = 10
# n = 2
# print(mi(10,2))
#
#
# # 要求：
# #1.校验输入内容是否符合规范（xx@yy.com）, 如是进入下一步，如否则抛出提示"incorrect email format"。注意必须以.com 结尾
# #2.可以循环“输入--输出判断结果”这整个过程
# #3.按字母 Q（不区分大小写）退出循环，结束程序
# import re
#
# def is_mail_style(x):
#     a = re.match('^[0-9a-zA-Z\_\-]*@[0-9a-zA-Z]+(\.com)$',x)
#     if a:
#         gr = re.findall("^(.+?)@",x) # 因为正则匹配的结果是列表
#         print("个人的用户名:{}".format(gr[0]))
#         print(gr)
#         gs = re.findall("@(.+?)\.com",x)
#         print(gs)
#         print("公司的用户名:{}".format(gs[0]))
#         return True
#     else:
#         print('incorrect email format')
#         return False
#
# a = input('请输入:')
#
# while 1:
#     if a == 'q' or a == 'Q':
#         exit()
#     else:
#         if is_mail_style(a):
#             break
#
#     a = input('请输入')
#
# print('请下一步！')
#
#
#
# # python 编程 4-遍历文件
# import os
#
# all = []
# def get_files(path,rule):
#     for fpath,dirname,fs in os.walk(path):
#         for i in fs:
#             file_path = os.path.join(fpath,i) # 路径要写对
#             if file_path.endswith(rule):
#                 print(file_path)
#                 all.append(file_path)
#     return all
#
# if __name__ == '__main__':
#     a = get_files(path='F:\\11',rule='.py')
#     for l in a:
#         print(l)



