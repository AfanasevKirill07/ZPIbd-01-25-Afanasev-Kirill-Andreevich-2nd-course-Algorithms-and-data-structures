def bubblesort(s):
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
array = [10, 7, 8, 9, 1, 5]
sorted_array = bubblesort(array)
print("Отсортированный массив:", sorted_array)
