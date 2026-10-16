def insertion_sort(s):
    for i in range(1, len(s)):
        k = s[i]
        j = i - 1
        while j >= 0 and s[j] > k:
            s[j + 1] = s[j]
            j -= 1

        s[j + 1] = k

    return s


data = [5, 2, 9, 1, 5, 6]
sorted_data = insertion_sort(data)
print(sorted_data)
