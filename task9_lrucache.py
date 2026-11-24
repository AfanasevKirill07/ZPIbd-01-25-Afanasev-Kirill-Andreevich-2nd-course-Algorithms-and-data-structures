from task3_hashtable import HashTable

class LRUCache:
    def __init__(self, capacity):
        self.cache = HashTable(capacity=max(8, capacity*2)) # ← was dict {}
        self.head = _Node() # MRU
        self.tail = _Node() # LRU

    def get(self, key):
        node = self.cache.get(key) # O(1) HashTable lookup
        if not node: return -1
        self._move_to_head(node)   # O(1) DLL
        return node.value

    def put(self, key, value):
        node = self.cache.get(key)
        if node:
            node.value = value
            self._move_to_head(node)
        else:
            new = _Node(key, value)
            self.cache.put(key, new)      # store Node in HashTable
            self._add_to_head(new)
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                self.cache.delete(lru.key) # evict from BOTH structures
