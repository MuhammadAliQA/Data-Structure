# BST - oddiy binary search tree

class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:

    def insert(self, root, value):

        if root is None:
            return BSTNode(value)

        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        return root

    def inorder(self, root, res):

        if root is not None:
            self.inorder(root.left, res)
            res.append(root.value)
            self.inorder(root.right, res)


# AVL TREE (balans uchun)

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        x = y.left
        temp = x.right

        x.right = y
        y.left = temp

        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def rotate_left(self, x):
        y = x.right
        temp = y.left

        y.left = x
        x.right = temp

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, node, value):

        if node is None:
            return AVLNode(value)

        if value < node.value:
            node.left = self.insert(node.left, value)
        else:
            node.right = self.insert(node.right, value)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        if balance > 1:
            if value < node.left.value:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if value > node.right.value:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def inorder(self, node, res):

        if node is not None:
            self.inorder(node.left, res)
            res.append(node.value)
            self.inorder(node.right, res)


# HASH TABLE (oddiy dictionary)

class HashTable:

    def __init__(self):
        self.data = {}

    def add(self, key, value):
        self.data[key] = value

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return "Topilmadi"


# KMP o‘rniga oddiy qidiruv (student style)

class KMP:

    def search(self, text, pattern):

        if pattern in text:
            return True
        return False