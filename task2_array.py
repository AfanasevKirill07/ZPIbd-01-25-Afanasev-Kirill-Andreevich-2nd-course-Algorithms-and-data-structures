

class DynamicArray:
    INITIAL_CAPACITY = 4

    def __init__(self, values=None):
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._data = [None] * self._capacity
        if values:
            for v in values:
                self.append(v)



    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    @property
    def capacity(self):

        return self._capacity



    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity



    def _check_index(self, index):
        if not 0 <= index < self._size:
            raise IndexError(f"индекс {index} вне рамок (size={self._size})")

    def get(self, index):
        self._check_index(index)
        return self._data[index]

    def set(self, index, value):
        self._check_index(index)
        self._data[index] = value

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def append(self, value):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError(f"индекс {index} вне рамок (size={self._size})")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1



    def pop(self):
        if self.is_empty():
            raise IndexError("pop из пустого array")
        self._size -= 1
        value = self._data[self._size]
        self._data[self._size] = None
        if 0 < self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def remove_at(self, index):
        self._check_index(index)
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._size -= 1
        self._data[self._size] = None
        if 0 < self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def remove(self, value):

        i = self.index_of(value)
        if i == -1:
            return False
        self.remove_at(i)
        return True



    def index_of(self, value):

        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    def contains(self, value):
        return self.index_of(value) != -1

    def __contains__(self, value):
        return self.contains(value)

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def to_list(self):
        return [self._data[i] for i in range(self._size)]

    def __str__(self):
        return f"DynamicArray({self.to_list()}, size={self._size}, capacity={self._capacity})"

    __repr__ = __str__


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== проверка Dynamic Array ===\n")

    arr = DynamicArray()
    print("пустой:", arr, "| is_empty:", arr.is_empty())

    print("\n-- добавить 1..9 (смотреть на capacity) --")
    for i in range(1, 10):
        arr.append(i)
        print(f"append({i:2}) -> size={len(arr)}, capacity={arr.capacity}")

    print("\n-- insert(2, 99) --")
    arr.insert(2, 99)
    print(arr)

    print("\n-- доступ к элементам --")
    print("arr[0] =", arr[0], "| arr[4] =", arr[4])
    arr[0] = 111
    print("after arr[0] = 111:", arr)

    print("\n-- поиск --")
    print("index_of(99) =", arr.index_of(99))
    print("index_of(42) =", arr.index_of(42))
    print("7 in arr:", 7 in arr, "| 42 in arr:", 42 in arr)

    print("\n-- удаление --")
    print("remove(99):", arr.remove(99))
    print("remove_at(0) returned:", arr.remove_at(0))
    print("pop() returned:", arr.pop())
    print(arr)

    print("\n-- переход --")
    print("forward:", [x for x in arr])
    print("sum:", sum(arr))
