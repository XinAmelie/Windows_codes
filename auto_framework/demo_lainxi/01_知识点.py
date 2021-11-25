
## 大小写转换
s = 'HELLO WORLD'
s1 = s.capitalize() # 首字母大写
print(s1)

# title是各个字母首字母大写
s2 = 'i have a dream'
s3 = s2.title()
print(s3)

# 小写变大写
s4 = s2.upper()
print(s4)
# lower 是大写变小写


## 字符串去空白、替换切割
s5 = ' 你好，  我叫   周杰伦  '
# sript去掉左右空白符（空格,\t,\n）
s6 = s5.strip()
print(s6)
# 替换
a = 'hello i am a man'
a1 = a.replace(' ','')
print(a1)

# 切割split切割的结果,放在列表当中:用什么切就会损失谁
b = 'c_java_uu'
b1 = b.split('_')
print(b1)


## 字符串查找和判断
a = 'hello i am a man'
# 查找
r = a.find('hello')  # 返回-1是没有
print(r)
res = a.index('hello') # 报错是没有
print('hello' in a) # in做条件的对象  not in


# 判断 strartwith 字符串以什么开头  endswith 以什么结尾  isdigit是不是整数组成
# f-string
# 字符串不可变,元组不可变
# 字典与列表可变
L = input('请你输入:')
if L.isdigit():
    print('下班泡酒吧')
else:
    print('睡觉吧')

name = 'lilei'
print(f"你的名字:{name}")

# len 长度,   join的拼接
print(len(a))

lst = ['hello', 'i' ,'am', 'a' ,'man']
dd = '_'.join(lst)
print(dd)

# 列表的增删改查、排序、嵌套
lst = [1,2,3,4,5,6,7,8,9]
# 增: insert(3,'你好')  extend(lst) 合并列表，并在A列表的后满排序。append
# 删除pop remove
# 改：lst[3] = '你好'
# lst[3]    直接索引


# 循环删除,删除一个元素，后面的元素顶上，循环又在进行，所以会轮空一个
# 基本思路：空列表存放需要删除的元素，轮询该列表，然后原列表删除

