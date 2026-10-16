def quick_sort(s):
    if len(s) <= 1:
        return s
    p = s[len(s) // 2]
    l = [x for x in s if x < p]
    m = [x for x in s if x == p]
    r = [x for x in s if x > p]
    return quick_sort(l) + m + quick_sort(r)
a = [10, 7, 8, 9, 1, 5]
print("Отсортированный массив:", quick_sort(a))
