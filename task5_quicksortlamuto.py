from random import shuffle
from sys import setrecursionlimit
from timeit import timeit

trys = 1000
setrecursionlimit(2**16)

def lomuto(a):
    #print(a)
    if len(a) < 2:
        return a
    pivot = a[-1]
    j=0
    if all((a[x] <= a[x+1] for x in range(len(a)-1))):
        return a
    while a[j] < pivot:
        j += 1
    i = j
    while i < len(a)-1:
        i += 1
        if a[i] < a[j]:
            a[i], a[j] = a[j], a[i]
            while a[j] < pivot:
                j += 1
    return lomuto(a[:j]) + [a[j]] + lomuto(a[j+1:])


#print(lomuto([1,4,8,6,7,42,2,2,8,100,3,5]))
lomutotime = timeit(stmt="shuffle(a)\nb=lomuto(a)", setup='''
from random import shuffle
def lomuto(a):
    #print(a)
    if len(a) < 2:
        return a
    pivot = a[-1]
    j=0
    if all(map(lambda x: a[x] <= a[x+1], range(len(a)-1))):
        return a
    while a[j] < pivot:
        j += 1
    i = j
    while i < len(a)-1:
        i += 1
        if a[i] < a[j]:
            a[i], a[j] = a[j], a[i]
            while a[j] < pivot:
                j += 1
    return lomuto(a[:j]) + [a[j]] + lomuto(a[j+1:])

a = list(range(400))
''', number=trys)
shuffletime = timeit(stmt="shuffle(a)\n", setup="from random import shuffle\na = list(range(400))", number=trys)
print((lomutotime-shuffletime)/trys)
