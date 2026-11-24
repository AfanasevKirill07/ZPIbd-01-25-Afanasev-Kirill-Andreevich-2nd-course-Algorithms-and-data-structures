from typing import Any, List, Optional

class HashTable:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: List[List[tuple[Any, Any]]] = [[] for _ in range(capacity)]
    
    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity
    
    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v, _resizing=True)
    
    def put(self, key: Any, value: Any, _resizing: bool = False):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # update
                return
        
        bucket.append((key, value))
        self.size += 1
        
        if not _resizing and self.size / self.capacity > self.load_factor:
            self._resize()
    
    __setitem__ = put
    
    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return default
    
    def __getitem__(self, key: Any) -> Any:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)
    
    def delete(self, key: Any) -> bool:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False
    
    __delitem__ = delete
    
    def contains(self, key: Any) -> bool:
        idx = self._hash(key)
        return any(k == key for k, _ in self.buckets[idx])
    
    __contains__ = contains
    
    def keys(self):
        for bucket in self.buckets:
            for k, _ in bucket:
                yield k
    
    def values(self):
        for bucket in self.buckets:
            for _, v in bucket:
                yield v
    
    def items(self):
        for bucket in self.buckets:
            for k, v in bucket:
                yield (k, v)
    
    def __len__(self):
        return self.size
    
    def __repr__(self):
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashTable({{{items}}}, capacity={self.capacity})"
    
    def is_empty(self) -> bool:
        return self.size == 0
    
    def clear(self):
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0


if __name__ == "__main__":
    ht = HashTable(capacity=4)
    print("=== HashTable Demo ===")
    ht.put("apple", 5)
    ht.put("banana", 7)
    ht["cherry"] = 12
    print(f"get('apple') = {ht.get('apple')}")
    print(f"get('missing', 'default') = {ht.get('missing', 'default')}")
    print(f"'banana' in ht? { 'banana' in ht }")
    print(f"size: {len(ht)}, capacity: {ht.capacity}")
    
    ht.put("date", 3)
    ht.put("elderberry", 9)
    print(f"After adding more -> size: {len(ht)}, capacity: {ht.capacity} (resized)")
    print(f"keys: {list(ht.keys())}")
    
    ht.delete("banana")
    print(f"After delete('banana'): {ht}")
