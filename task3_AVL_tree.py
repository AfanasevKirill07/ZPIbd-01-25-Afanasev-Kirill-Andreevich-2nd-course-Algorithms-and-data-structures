"""
avl_tree.py
-----------
An AVL tree (self-balancing binary search tree) implemented from scratch.

Every node stores its height, and after every insert/delete the tree
restores the AVL property: for every node, the heights of its left and
right subtrees differ by at most 1. Rebalancing is done with rotations.

Operations (all O(log n) guaranteed):
    insert(key)
    delete(key)
    search(key) / contains(key)
    min() / max()
    traversals: inorder, preorder, postorder, level_order
"""


class AVLNode:
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1                    # height of a single node is 1

    def __repr__(self):
        return f"AVLNode({self.key!r})"


class AVLTree:
    def __init__(self, keys=None):
        self.root = None
        self._size = 0
        if keys:
            for k in keys:
                self.insert(k)

    # ---------- basic info ----------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.root is None

    # ---------- height / balance helpers ----------

    @staticmethod
    def _height(node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        """height(left) - height(right); |factor| > 1 means unbalanced."""
        return self._height(node.left) - self._height(node.right) if node else 0

    # ---------- rotations ----------

    def _rotate_right(self, y):
        r"""       y                      x
                  / \                    / \
                 x   C      ==>         A   y
                / \                        / \
               A   B                      B   C
        """
        x = y.left
        B = x.right
        x.right = y
        y.left = B
        self._update_height(y)             # order matters: y first
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        r"""     x                        y
                / \                      / \
               A   y          ==>       x   C
                  / \                  / \
                 B   C                A   B
        """
        y = x.right
        B = y.left
        y.left = x
        x.right = B
        self._update_height(x)             # order matters: x first
        self._update_height(y)
        return y

    def _rebalance(self, node):
        """Restore the AVL property at node; returns the new subtree root."""
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            if self._balance_factor(node.left) < 0:      # Left-Right case
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)              # Left-Left case

        # Right heavy
        if balance < -1:
            if self._balance_factor(node.right) > 0:     # Right-Left case
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)               # Right-Right case

        return node                                      # already balanced

    # ---------- insert ----------

    def insert(self, key):
        """Insert a key. Duplicates are ignored. Returns True if inserted."""
        if self.contains(key):
            return False
        self.root = self._insert(self.root, key)
        self._size += 1
        return True

    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return self._rebalance(node)       # rebalance on the way back up

    # ---------- search ----------

    def search(self, key):
        """Return the node with the given key, or None."""
        current = self.root
        while current:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def contains(self, key):
        return self.search(key) is not None

    def __contains__(self, key):
        return self.contains(key)

    def min(self):
        if not self.root:
            raise ValueError("tree is empty")
        current = self.root
        while current.left:
            current = current.left
        return current.key

    def max(self):
        if not self.root:
            raise ValueError("tree is empty")
        current = self.root
        while current.right:
            current = current.right
        return current.key

    # ---------- delete ----------

    def delete(self, key):
        """Delete a key. Returns True if the key was found and removed."""
        if not self.contains(key):
            return False
        self.root = self._delete(self.root, key)
        self._size -= 1
        return True

    def _delete(self, node, key):
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # found the node to delete
            if node.left is None:
                return node.right          # 0 or 1 child (right)
            if node.right is None:
                return node.left           # 1 child (left)
            # two children: replace with the inorder successor (min of right)
            successor = node.right
            while successor.left:
                successor = successor.left
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)
        return self._rebalance(node)

    # ---------- traversals ----------

    def inorder(self):
        """Left - root - right. Yields keys in sorted order."""
        def walk(node):
            if node:
                yield from walk(node.left)
                yield node.key
                yield from walk(node.right)
        yield from walk(self.root)

    def preorder(self):
        """Root - left - right."""
        def walk(node):
            if node:
                yield node.key
                yield from walk(node.left)
                yield from walk(node.right)
        yield from walk(self.root)

    def postorder(self):
        """Left - right - root."""
        def walk(node):
            if node:
                yield from walk(node.left)
                yield from walk(node.right)
                yield node.key
        yield from walk(self.root)

    def level_order(self):
        """Breadth-first, level by level."""
        if not self.root:
            return
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            yield node.key
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def __iter__(self):
        """Default iteration: sorted (inorder)."""
        return self.inorder()

    # ---------- utilities ----------

    def height(self):
        return self._height(self.root)

    def is_balanced(self):
        """Verify the AVL property holds for every node (for testing)."""
        def check(node):
            if not node:
                return True
            if abs(self._balance_factor(node)) > 1:
                return False
            return check(node.left) and check(node.right)
        return check(self.root)

    def show(self):
        """Print the tree sideways (right subtree on top)."""
        def print_node(node, indent, label):
            if node:
                print_node(node.right, indent + "      ", "/")
                bf = self._balance_factor(node)
                print(f"{indent}{label}{node.key} (h={node.height}, bf={bf})")
                print_node(node.left, indent + "      ", "\\")
        if self.root:
            print_node(self.root, "", "")
        else:
            print("(empty tree)")

    def __str__(self):
        return f"AVLTree({list(self.inorder())})"

    __repr__ = __str__


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== AVL Tree demo ===\n")

    tree = AVLTree()

    print("-- inserting 10, 20, 30 --")
    print("(a plain BST would degenerate into a chain; the AVL tree rotates)\n")
    for k in (10, 20, 30):
        tree.insert(k)
    tree.show()

    print("\n-- inserting 40, 50, 25 --\n")
    for k in (40, 50, 25):
        tree.insert(k)
    tree.show()

    print("\n-- searching --")
    print("search(25):", tree.search(25))
    print("25 in tree:", 25 in tree, "| 99 in tree:", 99 in tree)
    print("min:", tree.min(), "| max:", tree.max())

    print("\n-- traversals --")
    print("inorder   (sorted):", list(tree.inorder()))
    print("preorder           :", list(tree.preorder()))
    print("postorder          :", list(tree.postorder()))
    print("level order        :", list(tree.level_order()))

    print("\n-- delete(10), then delete(30) --")
    tree.delete(10)
    tree.delete(30)
    print(tree)
    tree.show()

    print("\n-- stress test: insert 0..99 in order --")
    big = AVLTree(range(100))
    print("size:", len(big))
    print("height:", big.height(), "(a linear chain would have height 100)")
    print("balanced:", big.is_balanced())
    print("inorder stays sorted:", list(big.inorder()) == list(range(100)))
