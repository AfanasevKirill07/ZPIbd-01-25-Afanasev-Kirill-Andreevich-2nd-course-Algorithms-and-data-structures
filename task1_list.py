class Node:

    __slots__ = ("next", "prev", "value")

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.value!r})"


class DoublyLinkedList:
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self._size = 0
        if values:
            for v in values:
                self.append(v)

    # ---------- basic info ----------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    # ---------- adding ----------

    def append(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError(f"индекс {index} вне рамок (size={self._size})")
        if index == 0:
            self.prepend(value)
        elif index == self._size:
            self.append(value)
        else:
            current = self._node_at(index)
            node = Node(value)
            node.prev = current.prev
            node.next = current
            current.prev.next = node
            current.prev = node
            self._size += 1



    def _unlink(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next 
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self._size -= 1

    def pop(self):

        if self.is_empty():
            raise IndexError("pop из пустого списка")
        value = self.tail.value
        self._unlink(self.tail)
        return value

    def popleft(self):

        if self.is_empty():
            raise IndexError("popleft из пустого списка")
        value = self.head.value
        self._unlink(self.head)
        return value

    def remove(self, value):
        current = self.head
        while current:
            if current.value == value:
                self._unlink(current)
                return True
            current = current.next
        return False

    def remove_at(self, index):

        node = self._node_at(index)
        value = node.value
        self._unlink(node)
        return value



    def _node_at(self, index):
        if not 0 <= index < self._size:
            raise IndexError(f"индекс {index} вне рамок (size={self._size})")
        if index < self._size // 2:        
            current = self.head
            for _ in range(index):
                current = current.next
        else:                              
            current = self.tail
            for _ in range(self._size - 1, index, -1):
                current = current.prev
        return current

    def get(self, index):
        return self._node_at(index).value

    def set(self, index, value):
        self._node_at(index).value = value

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)



    def index_of(self, value):
        current, i = self.head, 0
        while current:
            if current.value == value:
                return i
            current = current.next
            i += 1
        return -1

    def contains(self, value):
        return self.index_of(value) != -1

    def __contains__(self, value):
        return self.contains(value)

    def __iter__(self):

        current = self.head
        while current:
            yield current.value
            current = current.next

    def iter_reverse(self):
        current = self.tail
        while current:
            yield current.value
            current = current.prev

    def to_list(self):
        return list(self)

    def __str__(self):
        return " <-> ".join(repr(v) for v in self) or "(empty)"

    __repr__ = __str__


if __name__ == "__main__":
    print("=== проверка DoublyLinkedList ===\n")

    lst = DoublyLinkedList()
    print("пустой:", str(lst), "| is_empty:", lst.is_empty())

    print("\n-- добавить в конец или начало--")
    lst.append(1)
    lst.append(2)
    lst.append(3)
    lst.prepend(0)
    print(lst)

    print("\n-- insert(2, 99) --")
    lst.insert(2, 99)
    print(lst)

    print("\n-- доступ к элементам --")
    print("lst[0] =", lst[0], "| lst[3] =", lst[3])
    lst[0] = 111
    print("after lst[0] = 111:", lst)

    print("\n-- поиск --")
    print("index_of(99) =", lst.index_of(99))
    print("index_of(42) =", lst.index_of(42))
    print("2 in lst:", 2 in lst, "| 42 in lst:", 42 in lst)

    print("\n-- удаление --")
    print("remove(99):", lst.remove(99), "->", lst)
    print("remove_at(0) вернуло:", lst.remove_at(0), "->", lst)
    print("pop() вернуло:", lst.pop(), "->", lst)
    print("popleft() вернуло:", lst.popleft(), "->", lst)

    print("\n-- передвижение по листу --")
    bigger = DoublyLinkedList([5, 10, 15, 20, 25])
    print("вперед :", [x for x in bigger])
    print("назад:", list(bigger.iter_reverse()))
    print("сумма:", sum(bigger))
