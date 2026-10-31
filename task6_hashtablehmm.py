from random import randint
from time import time
data1 = [randint(0,100) for i in range(100)]
data2 = [randint(0,100) for i in range(10**4)]
data3 = [randint(0,100) for i in range(10**6)]
ds1 = set(data1)
ds2 = set(data2)
ds3 = set(data3)
def find(lst, num):
    for i in lst:
        if i==num:
            return i
start = time()
_ = find(data1, 100)
print(time()-start, "d1")
start = time()
_ = find(data2, len(ds2))
print(time()-start, "d2")
start = time()
_ = find(data3, len(ds3))
print(time()-start, "d3")
start = time()
_ = find(ds1, 1000)
print(time()-start, "ds1")
start = time()
_ = find(ds2, len(ds2))
print(time()-start, "ds2")
start = time()
_ = find(ds3, len(ds3))
print(time()-start, "ds3")
