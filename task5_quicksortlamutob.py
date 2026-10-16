from timeit import timeit

import matplotlib.pyplot as plt
import numpy as np

trys = 1000
def lomuto(s):
    if len(s) <= 1:
        return s
    p = s[-1]
    l = [x for x in s if x < p]
    m = [x for x in s if x == p]
    r = [x for x in s if x > p]
    return lomuto(l) + m + lomuto(r)
a = [1,4,8,6,7,42,2,2,8,100,3,5]
#print("Отсортированный массив:", quick_sort(a))
lomutotiming = lambda x: timeit(stmt="shuffle(a)\nb=lomuto(a)", setup=f'''from random import shuffle
def lomuto(s):
    if len(s) <= 1:
        return s
    p = s[-1]
    l = [x for x in s if x < p]
    m = [x for x in s if x == p]
    r = [x for x in s if x > p]
    return lomuto(l) + m + lomuto(r)
a = list(range({x}))
''', number=trys)
bubbletiming = lambda x: timeit(stmt="bubble(a)\nb=bubble(a)", setup=f'''from random import shuffle
def bubble(s):
    stack = [(0, len(s) - 1)]

    while stack:
        l, r = stack.pop()
        if l >= r:
            continue
        
        pivot = s[r]
        i = l - 1

        for j in range(l, r):
            if s[j] <= pivot:
                i += 1
                s[i], s[j] = s[j], s[i]

        s[i + 1], s[r] = s[r], s[i + 1]
        p = i + 1

        stack.append((p + 1, r))
        stack.append((l, p - 1))
    return s
a = list(range({x}))
''', number=trys)
shuffletiming = lambda x: timeit(stmt="shuffle(a)\n", setup=f"from random import shuffle\na = list(range({x}))", number=trys)
print((lomutotiming(trys)-shuffletiming(trys))/trys)

x = np.linspace(1, 100, 100)  # Sample data.

plt.figure(figsize=(5, 2.7), layout='constrained')
print([i for i in x])
plt.plot(x, [shuffletiming(int(i)) for i in x])
plt.plot(x, [lomutotiming(int(i)) for i in x])
plt.plot(x, [bubbletiming(int(i)) for i in x])
plt.legend(['shuffle', 'lomuto', 'bubble'])
plt.show()
