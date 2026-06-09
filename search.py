# ══════════════════════════════════════════════════════════
#  search.py  –  BST, AVL Tree, Hash Table, KMP Algorithm
# ══════════════════════════════════════════════════════════


# ─────────────────────────────────────────────────────
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left  = None
        self.right = None


class BST:
    """
    Binary Search Tree – flight narxlarini saqlash va
    O(log n) vaqtda range query bajarish uchun.
    """

    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left  = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def search(self, value):
        """Qiymat mavjudligini tekshiradi – O(log n)."""
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def range_query(self, low, high):
        """[low, high] oralig'idagi barcha narxlarni qaytaradi – O(log n + k)."""
        result = []
        self._range(self.root, low, high, result)
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

    def inorder(self):
        """Tartiblangan qiymatlar ro'yxatini qaytaradi."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)


# ─────────────────────────────────────────────────────
class AVLNode:
    def __init__(self, value):
        self.value  = value
        self.left   = None
        self.right  = None
        self.height = 1


class AVLTree:
    """
    AVL Tree – o'z-o'zini balanslaydigan BST.
    Har doim O(log n) ta qidirish kafolatlanadi.
    """

    def _height(self, node):
        return node.height if node else 0

    def _balance(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        x      = y.left
        T2     = x.right
        x.right = y
        y.left  = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y      = x.right
        T2     = y.left
        y.left  = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, node, value):
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left  = self.insert(node.left, value)
        elif value > node.value:
            node.right = self.insert(node.right, value)
        else:
            return node                       # takroriy qiymat qo'shilmaydi

        self._update_height(node)
        bf = self._balance(node)

        # LL
        if bf > 1 and value < node.left.value:
            return self._rotate_right(node)
        # RR
        if bf < -1 and value > node.right.value:
            return self._rotate_left(node)
        # LR
        if bf > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # RL
        if bf < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def inorder(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)
            result.append(node.value)
            self.inorder(node.right, result)
        return result


# ─────────────────────────────────────────────────────
class HashTable:
    """
    Hash Table – PNR → yo'lovchi profili.
    O(1) o'rtacha qidirish vaqti.
    Collision: chaining (zanjir) usuli.
    """

    def __init__(self, size=64):
        self.size  = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def add(self, key, value):
        idx    = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)    # mavjudni yangilaydi
                return
        bucket.append((key, value))
        self.count += 1

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx    = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.count -= 1
                return True
        return False

    def load_factor(self):
        return round(self.count / self.size, 2)


# ─────────────────────────────────────────────────────
class KMP:
    """
    Knuth-Morris-Pratt (KMP) string qidirish algoritmi.
    Murakkablik: O(n + m) – n=matn, m=pattern uzunligi.

    Oddiy brute-force O(n*m) ga nisbatan ancha tez.
    """

    def _build_failure(self, pattern):
        """
        Failure (prefix) funksiyasini quradi.
        f[i] = pattern[0..i] ning eng uzun
               haqiqiy prefix-suffix uzunligi.
        """
        m = len(pattern)
        f = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = f[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            f[i] = j
        return f

    def search(self, text, pattern):
        """
        text ichida pattern ni qidiradi.
        Topilgan barcha indekslarni ro'yxat sifatida qaytaradi.
        Bo'sh ro'yxat = topilmadi.
        """
        if not pattern:
            return []
        n, m    = len(text), len(pattern)
        failure = self._build_failure(pattern)
        matches = []
        j       = 0                             # pattern indeksi

        for i in range(n):                      # text indeksi
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]             # muvaffaqiyatsizlikda orqaga
            if text[i] == pattern[j]:
                j += 1
            if j == m:
                matches.append(i - m + 1)      # pattern topildi, boshi indeks
                j = failure[j - 1]             # keyingi qidiruv uchun davom

        return matches

    def contains(self, text, pattern):
        """Faqat mavjud/yo'qligini qaytaradi."""
        return len(self.search(text, pattern)) > 0