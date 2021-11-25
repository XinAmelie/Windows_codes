a = [1,2,3,4,5,6]
b = [11,12,24,56,33]
c = [95,98,0,26]

lst = [a,b,c]

for i in lst:
    if  0 in i:
        if a == i:
            print('a')
        elif b == i:
            print('b')
        else:
            print('c')