# ══════════════════════════════════════════════
#  BINARY SEARCH TREE  (BST)
#  insert  : O(log n) avg  / O(n) worst
#  search  : O(log n) avg  / O(n) worst
#  inorder : O(n)
# ══════════════════════════════════════════════
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left  = None
        self.right = None


class BST:
    """
    Binary Search Tree to store and range-query flight prices.
    All values must be comparable (int or float for prices).
    """

    def __init__(self):
        self._root = None

    # ---------- insert ----------

    def insert(self, value) -> None:
        self._root = self._insert(self._root, value)

    def _insert(self, node, value):
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left  = self._insert(node.left,  value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        # duplicate values are silently ignored
        return node

    # ---------- search ----------

    def search(self, value) -> bool:
        return self._search(self._root, value)

    def _search(self, node, value) -> bool:
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    # ---------- range query ----------

    def range_query(self, low, high) -> list:
        """Return all values in [low, high] in sorted order – O(log n + k)."""
        result = []
        self._range(self._root, low, high, result)
        return result

    def _range(self, node, low, high, result):
        if node is None:
            return
        if low < node.value:
            self._range(node.left, low, high, result)
        if low <= node.value <= high:
            result.append(node.value)
        if node.value < high:
            self._range(node.right, low, high, result)

    # ---------- inorder (sorted list) ----------

    def inorder(self) -> list:
        result = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left,  result)
            result.append(node.value)
            self._inorder(node.right, result)


# ══════════════════════════════════════════════
#  AVL TREE  –  Self-Balancing BST
#  insert  : O(log n)  guaranteed
#  search  : O(log n)  guaranteed
#  Balance factor kept in [-1, 0, +1]
# ══════════════════════════════════════════════
class AVLNode:
    def __init__(self, value):
        self.value  = value
        self.left   = None
        self.right  = None
        self.height = 1


class AVLTree:
    """
    AVL Tree for flight price storage.
    Guarantees O(log n) search even for sorted insertions (unlike plain BST).
    """

    def __init__(self):
        self._root = None

    # ---------- helpers ----------

    def _height(self, node) -> int:
        return node.height if node else 0

    def _balance(self, node) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        x     = y.left
        temp  = x.right
        x.right = y
        y.left  = temp
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y     = x.right
        temp  = y.left
        y.left  = x
        x.right = temp
        self._update_height(x)
        self._update_height(y)
        return y

    # ---------- insert ----------

    def insert(self, value) -> None:
        self._root = self._insert(self._root, value)

    def _insert(self, node, value):
        # Standard BST insert
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left  = self._insert(node.left,  value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node    # duplicate – ignore

        self._update_height(node)
        bf = self._balance(node)

        # ── 4 rotation cases ──
        # Left-Left
        if bf > 1 and value < node.left.value:
            return self._rotate_right(node)
        # Right-Right
        if bf < -1 and value > node.right.value:
            return self._rotate_left(node)
        # Left-Right
        if bf > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right-Left
        if bf < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # ---------- search & range ----------

    def search(self, value) -> bool:
        node = self._root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def range_query(self, low, high) -> list:
        result = []
        self._range(self._root, low, high, result)
        return result

    def _range(self, node, low, high, result):
        if node is None:
            return
        if low < node.value:
            self._range(node.left, low, high, result)
        if low <= node.value <= high:
            result.append(node.value)
        if node.value < high:
            self._range(node.right, low, high, result)

    def inorder(self) -> list:
        result = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left,  result)
            result.append(node.value)
            self._inorder(node.right, result)


# ══════════════════════════════════════════════
#  HASH TABLE  –  PNR → Passenger Profile
#  get / set : O(1) average
#  Space     : O(n)
# ══════════════════════════════════════════════
class HashTable:
    """
    Maps Passenger Name Records (PNR) to passenger profile dicts.
    Uses Python's built-in dict (hash table) for O(1) average operations.
    """

    def __init__(self):
        self._data = {}

    def add(self, pnr: str, profile) -> None:
        if not pnr.strip():
            raise ValueError("PNR key cannot be empty.")
        self._data[pnr] = profile

    def get(self, pnr: str):
        if pnr not in self._data:
            return f"PNR '{pnr}' not found."
        return self._data[pnr]

    def delete(self, pnr: str) -> bool:
        if pnr in self._data:
            del self._data[pnr]
            return True
        return False

    def exists(self, pnr: str) -> bool:
        return pnr in self._data

    def all_records(self) -> dict:
        return dict(self._data)


# ══════════════════════════════════════════════
#  KMP ALGORITHM  –  Knuth-Morris-Pratt
#  Preprocessing : O(m)   m = pattern length
#  Search        : O(n)   n = text length
#  Total         : O(n + m)   vs  O(n*m) naive
# ══════════════════════════════════════════════
class KMP:
    """
    Efficient string pattern matching using the KMP algorithm.
    Used to find passenger names within large flight manifests.

    Key idea: build a 'failure function' (partial match table) from
    the pattern so we never re-check characters already matched.
    """

    # ---------- failure function (LPS array) ----------

    def _build_lps(self, pattern: str) -> list:
        """
        Compute the Longest Proper Prefix which is also Suffix (LPS) array.
        lps[i] = length of the longest proper prefix of pattern[0..i]
                 that is also a suffix.
        Example:  pattern = "ABABC"
                  lps     = [0, 0, 1, 2, 0]
        """
        m   = len(pattern)
        lps = [0] * m
        length = 0    # length of previous longest prefix-suffix
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i]  = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]   # fall back (don't increment i)
                else:
                    lps[i] = 0
                    i += 1
        return lps

    # ---------- search ----------

    def search(self, text: str, pattern: str) -> list:
        """
        Return a list of all starting indices where pattern is found in text.
        Returns an empty list if no match.

        Example:
            kmp.search("Ali is at Dubai Ali", "Ali")  →  [0, 16]
        """
        if not pattern:
            return []
        if not text:
            return []

        n, m = len(text), len(pattern)
        lps  = self._build_lps(pattern)

        indices = []
        i = 0   # index for text
        j = 0   # index for pattern

        while i < n:
            if text[i] == pattern[j]:
                i += 1
                j += 1
            if j == m:
                indices.append(i - j)   # found at position i-j
                j = lps[j - 1]          # look for next match
            elif i < n and text[i] != pattern[j]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        return indices

    def contains(self, text: str, pattern: str) -> bool:
        """Convenience method – returns True/False."""
        return len(self.search(text, pattern)) > 0