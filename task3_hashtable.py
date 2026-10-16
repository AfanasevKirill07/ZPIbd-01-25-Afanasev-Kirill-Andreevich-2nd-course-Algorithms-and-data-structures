class Hashtable:
    def __init__(self):
        self._data = []

    def add(self, element):
        for i in range(len(self._data)):
            if element <= self._data[i]:
                self._data.insert(i, element)
                return
        self._data.append(element)

    def __repr__(self):
        return self._data

    def __str__(self):
        return str(self._data)

    
a = Hashtable()
a.add(1)
print(a)
a.add(2)
print(a)
a.add(-1)
print(a)
