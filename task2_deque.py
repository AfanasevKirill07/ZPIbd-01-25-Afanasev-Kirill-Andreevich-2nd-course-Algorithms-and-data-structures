class Deque:

    _MIN_CAP = 8

    __hash__ = None 
    def __init__(self, iterable=None, maxlen=None):
        if maxlen is not None:
            if not isinstance(maxlen, int) or isinstance(maxlen, bool) or maxlen < 0:
                raise ValueError("длина должна быть неотрицательной")
        self._maxlen = maxlen
        self._buf = [None] * self._MIN_CAP
        self._head = 0
        self._size = 0
        self._version = 0 
        if iterable is not None:
            for item in iterable:
                self.append(item)


    def _repack(self, new_cap):
        cap = len(self._buf)
        new_buf = [None] * new_cap
        end = self._head + self._size
        if end <= cap:
            new_buf[:self._size] = self._buf[self._head:end]
        else: 
            first = cap - self._head
            new_buf[:first] = self._buf[self._head:]
            new_buf[first:first + self._size - first] = self._buf[:self._size - first]
        self._buf = new_buf
        self._head = 0

    def _maybe_grow(self):
        if self._size == len(self._buf):
            self._repack(len(self._buf) * 2)

    def _maybe_shrink(self):
        cap = len(self._buf)
        if cap > self._MIN_CAP and self._size <= cap // 4:
            self._repack(max(self._MIN_CAP, cap // 2))

    def _push_right(self, x):
        self._maybe_grow()
        self._buf[(self._head + self._size) % len(self._buf)] = x
        self._size += 1
        self._version += 1

    def _push_left(self, x):
        self._maybe_grow()
        self._head = (self._head - 1) % len(self._buf)
        self._buf[self._head] = x
        self._size += 1
        self._version += 1

    def _pop_left(self):
        x = self._buf[self._head]
        self._buf[self._head] = None 
        self._head = (self._head + 1) % len(self._buf)
        self._size -= 1
        self._version += 1
        self._maybe_shrink()
        return x

    def _pop_right(self):
        self._size -= 1
        pos = (self._head + self._size) % len(self._buf)
        x = self._buf[pos]
        self._buf[pos] = None
        self._version += 1
        self._maybe_shrink()
        return x

    def _index(self, i):
        if not isinstance(i, int):
            raise TypeError(
                f"индексы deque должны быть int, а не {type(i).__name__}")
        size = self._size
        if i < 0:
            i += size
        if not 0 <= i < size:
            raise IndexError("индекс deque вне размера")
        return i

    def _find(self, value, start, stop):
        buf, cap = self._buf, len(self._buf)
        for k in range(start, stop):
            item = buf[(self._head + k) % cap]
            if item is value or item == value:
                return k
        return -1


    def append(self, x):
        if self._maxlen is not None and self._size >= self._maxlen:
            if self._maxlen == 0:
                return
            self._pop_left()
        self._push_right(x)

    def appendleft(self, x):
        if self._maxlen is not None and self._size >= self._maxlen:
            if self._maxlen == 0:
                return
            self._pop_right()
        self._push_left(x)

    def pop(self):
        if self._size == 0:
            raise IndexError("pop в пустом deque")
        return self._pop_right()

    def popleft(self):
        if self._size == 0:
            raise IndexError("pop в пустом deque")
        return self._pop_left()

    def extend(self, iterable):
        for x in iterable:
            self.append(x)

    def extendleft(self, iterable):
        for x in iterable:
            self.appendleft(x)

    def rotate(self, n=1):
        size = self._size
        if size <= 1:
            return
        n %= size
        if n == 0:
            return

        if n <= size // 2:
            for _ in range(n):
                self._push_left(self._pop_right())
        else:
            for _ in range(size - n):
                self._push_right(self._pop_left())

    def reverse(self):
        if self._size <= 1:
            return
        buf, cap = self._buf, len(self._buf)
        i, j = 0, self._size - 1
        while i < j:
            a = (self._head + i) % cap
            b = (self._head + j) % cap
            buf[a], buf[b] = buf[b], buf[a]
            i += 1
            j -= 1
        self._version += 1

    def clear(self):
        self._buf = [None] * self._MIN_CAP
        self._head = 0
        self._size = 0
        self._version += 1

    def copy(self):
        return self.__class__(self, maxlen=self._maxlen)

    def index(self, value, start=0, stop=None):
        size = self._size
        if start < 0:
            start += size
        if start < 0:
            start = 0
        if stop is None:
            stop = size
        elif stop < 0:
            stop += size
        if stop > size:
            stop = size
        k = self._find(value, start, stop)
        if k < 0:
            raise ValueError(f"{value!r} не содержиться в deque")
        return k

    def count(self, value):
        buf, cap = self._buf, len(self._buf)
        total = 0
        for k in range(self._size):
            item = buf[(self._head + k) % cap]
            if item is value or item == value:
                total += 1
        return total

    def insert(self, i, x):
        if self._maxlen is not None and self._size >= self._maxlen:
            raise IndexError("deque уже на предельном размере")
        size = self._size
        if i < 0:
            i += size
        i = min(max(i, 0), size)
        if i == size:
            self._push_right(x)
        elif i == 0:
            self._push_left(x)
        else:
            self.rotate(-i)
            self._push_left(x)
            self.rotate(i)

    def remove(self, value):
        k = self._find(value, 0, self._size)
        if k < 0:
            raise ValueError("deque.remove(x): x не содержиться в deque")
        self.rotate(-k)
        self._pop_left()
        self.rotate(k)


    def __len__(self):
        return self._size

    def __bool__(self):
        return self._size > 0

    def __iter__(self):
        return self._forward(0, self._size)

    def __reversed__(self):
        buf, cap = self._buf, len(self._buf)
        version = self._version
        for k in range(self._size - 1, -1, -1):
            if self._version != version:
                raise RuntimeError("deque изменился за итерацию")
            yield buf[(self._head + k) % cap]

    def _forward(self, start, stop):
        buf, cap = self._buf, len(self._buf)
        version = self._version
        for k in range(start, stop):
            if self._version != version:
                raise RuntimeError("deque изменился за итерацию")
            yield buf[(self._head + k) % cap]

    def __contains__(self, value):
        return self._find(value, 0, self._size) >= 0

    def __getitem__(self, i):
        if isinstance(i, slice):

            buf, cap = self._buf, len(self._buf)
            return [buf[(self._head + k) % cap]
                    for k in range(*i.indices(self._size))]
        i = self._index(i)
        return self._buf[(self._head + i) % len(self._buf)]

    def __setitem__(self, i, value):
        if isinstance(i, slice):
            raise TypeError("индексы deque должны быть int, а не slice")
        i = self._index(i)
        self._buf[(self._head + i) % len(self._buf)] = value

    def __delitem__(self, i):
        if isinstance(i, slice):
            raise TypeError("индексы deque должны быть int, а не slice")
        i = self._index(i)
        self.rotate(-i)
        self._pop_left()
        self.rotate(i)



    def __eq__(self, other):
        if isinstance(other, Deque):
            if self._size != other._size:
                return False
            return all(a is b or a == b for a, b in zip(self, other))
        return NotImplemented

    def __add__(self, other):
        if not isinstance(other, Deque):
            return NotImplemented
        result = Deque(self, maxlen=self._maxlen)
        result.extend(other)
        return result

    def __iadd__(self, other):
        if not hasattr(other, "__iter__"):
            return NotImplemented
        self.extend(other)
        return self

    def __mul__(self, n):
        if not isinstance(n, int):
            return NotImplemented
        result = Deque(maxlen=self._maxlen)
        if n > 0 and self._size:
            items = list(self)
            for _ in range(n):
                result.extend(items)
        return result

    __rmul__ = __mul__

    def __imul__(self, n):
        if not isinstance(n, int):
            return NotImplemented
        if n <= 0:
            self.clear()
        elif n > 1:
            items = list(self)
            for _ in range(n - 1):
                self.extend(items)
        return self



    @property
    def maxlen(self):
        return self._maxlen

    def __reduce__(self): 
        return (self.__class__, (list(self), self._maxlen))

    def __repr__(self):
        items = ", ".join(repr(x) for x in self)
        name = type(self).__name__
        if self._maxlen is not None:
            return f"{name}([{items}], maxlen={self._maxlen})"
        return f"{name}([{items}])"


if __name__ == "__main__":
    d = Deque([1, 2, 3])
    print("start:      ", d)
    d.append(4)
    d.appendleft(0)
    print("after appends:", d)
    print("pop():      ", d.pop(), "->", d)
    print("popleft():  ", d.popleft(), "->", d)
    d.rotate(2)
    print("rotate(2):  ", d)
    d.insert(1, 99)
    print("insert(1,99):", d)
    d.remove(3)
    print("remove(3):  ", d)
    print("index(2):   ", d.index(2))
    print("reversed:   ", list(reversed(d)))

    b = Deque(range(4), maxlen=3)
    print("\nbounded:    ", b)
    b.append(10)
    b.append(11)
    print("after 2x append with maxlen=3:", b)
