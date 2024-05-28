class BSTNode:
    def __init__(self, key=None):
        self.key = key
        self.parent = self.left = self.right = None
        self.height = None

    def __str__(self):
        if not self or not self.key:
            return "None"

        ptr = self
        res = []

        def create_str(ptr):
            if not ptr:
                return

            res.append(' (')
            res.append(str(f'{ptr.key}/{ptr.height}'))
            if not ptr.left:
                res.append(' .')
            else:
                create_str(ptr.left)
            if not ptr.right:
                res.append(' .')
            else:
                create_str(ptr.right)
            res.append(')')

        create_str(ptr)
        return "".join(res).lstrip()


class BST:
    def __init__(self, lst=None):
        self.root = None
        if lst:
            lst.sort()
            self.construct(lst)

    def construct(self, lst, i=None, j=None):
        if i == j == None:
            i = 0
            j = len(lst) - 1

        if i > j:
            return

        mid = (i + j) // 2

        self.add(lst[mid])

        self.construct(lst, i, mid - 1)
        self.construct(lst, mid + 1, j)

    def add(self, key):
        if self.root == None:
            self.root = BSTNode(key)
            # print("!")
            return self.root

        ptr = self.root
        while True:
            if key < ptr.key:
                if ptr.left:
                    ptr = ptr.left
                else:
                    ptr.left = BSTNode(key)
                    ptr.left.parent = ptr
                    return ptr.left
            elif key > ptr.key:
                if ptr.right:
                    ptr = ptr.right
                else:
                    ptr.right = BSTNode(key)
                    ptr.right.parent = ptr
                    return ptr.right
            else:
                return

    def search(self, key):
        if not self.root:
            return
        if key == self.root.key:
            return self.root

        ptr = self.root
        res = None
        while True:
            if key == ptr.key:
                res = ptr
                break
            if key < ptr.key and ptr.left:
                ptr = ptr.left
            elif key > ptr.key and ptr.right:
                ptr = ptr.right
            else:
                break
        return res

    def __str__(self):
        return str(self.root)

    def min(self, node=None):
        if not self.root:
            return None
        if not node:
            current_node = self.root
        else:
            current_node = node

        while True:
            if current_node.left:
                current_node = current_node.left
            else:
                return current_node

    def max(self, node=None):
        if not self.root:
            return None
        if not node:
            current_node = self.root
        else:
            current_node = node

        while True:
            if current_node.right:
                current_node = current_node.right
            else:
                return current_node

    def prev(self, node=None):
        if not self.root:
            return None
        if not node:
            current_node = self.root
        else:
            current_node = node

        if current_node.left:
            current_node = current_node.left
            if current_node.right:
                current_node = current_node.right
                while True:
                    if current_node.right:
                        current_node = current_node.right
                    else:
                        break
                return current_node
            else:
                return current_node
        else:
            while True:
                if current_node.parent:
                    p = current_node.parent
                    if p.right == current_node:
                        return p
                    current_node = p
                else:
                    return None

    def succ(self, node=None):
        if not self.root:
            return None
        if not node:
            current_node = self.root
        else:
            current_node = node

        if current_node.right:
            current_node = current_node.right
            if current_node.left:
                current_node = current_node.left
                while True:
                    if current_node.left:
                        current_node = current_node.left
                    else:
                        break
                return current_node
            else:
                return current_node
        else:
            while True:
                if current_node.parent:
                    p = current_node.parent
                    if p.left == current_node:
                        return p
                    current_node = p
                else:
                    return None

    def remove(self, node):
        if not node:
            return None

        if not node.left or not node.right:
            y = node
        else:
            y = self.succ(node)

        if y.left:
            x = y.left
        elif y.right:
            x = y.right
        else:
            x = None

        if y == self.root:
            if x:
                self.root = x
            else:
                self.root = None
                return y

        elif y != self.root and x:
            x.parent = y.parent
            if y.parent.left == y:
                y.parent.left = x
            elif y.parent.right == y:
                y.parent.right = x
        elif y != self.root and not x:
            if y.parent.left == y:
                y.parent.left = None
            elif y.parent.right == y:
                y.parent.right = None

        if y != node:
            node.key = y.key
        return y

    def get_array(self, root_=None, result=None):
        current_node = root_ or self.root

        if result == None:
            result = []

        if current_node == None:
            return result

        if current_node.left:
            self.get_array(current_node.left, result)

        result.append(current_node.key)

        if current_node.right:
            self.get_array(current_node.right, result)

        return result

    def floor(self, key):
        return self.get_floor(self.root, key)

    def get_floor(self, node, key):
        if not node:
            return None

        if key == node.key:
            return node

        if key < node.key:
            return self.get_floor(node.left, key)

        if key > node.key:
            return self.get_floor(node.right, key) or node

    def ceiling(self, key):
        return self.get_ceiling(self.root, key)

    def get_ceiling(self, node, key):
        if not node:
            return None

        if key == node.key:
            return node

        if key > node.key:
            return self.get_ceiling(node.right, key)

        if key < node.key:
            return self.get_ceiling(node.left, key) or node

class AVLTree(BST):
    def __init__(self, lst=None):
        super().__init__(lst)

    def adjust_height(self, node):
        node.height = max(node.left.height if node.left else -1,
                          node.right.height if node.right else -1) + 1

        # node.height = max(self.get_height(node.left))

        if node.parent:
            self.adjust_height(node.parent)

    def adjust_balance(self, node):
        if node == None:
            return

        new_node = self.balance(node)

        if new_node.parent:
            self.adjust_balance(new_node.parent)

    def add(self, key):
        node = super().add(key)
        self.adjust_height(node)
        self.adjust_balance(node)

    def remove(self, node):
        node = super().remove(node)
        self.adjust_height(node.parent)
        self.adjust_balance(node.parent)

    def rotate_right(self, node):
        if not node:
            return
        if not node.left:
            return
        new_root = node.left
        if node.parent:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
            new_root.parent = node.parent
        else:
            self.root = new_root
            new_root.parent = None
        if new_root.right:
            x = new_root.right
            node.left = x
            x.parent = node
        else:
            node.left = None
        new_root.right = node
        node.parent = new_root
        self.adjust_height(node)
        return new_root

    def rotate_left(self, node):
        if not node:
            return
        if not node.right:
            return
        new_root = node.right
        if node.parent:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
            new_root.parent = node.parent
        else:
            new_root.parent = None
            self.root = new_root
        if new_root.left:
            x = new_root.left
            node.right = x
            x.parent = node
        else:
            node.right = None
        new_root.left = node
        node.parent = new_root
        self.adjust_height(node)
        return new_root

    def get_height(self, node):
        if node == None:
            return -1
        return node.height

    def balance(self, node):
        if not node:
            return

        if (self.get_height(node.left) > self.get_height(node.right) + 1):
            ptr = node.left
            if (self.get_height(ptr.right) > self.get_height(ptr.left)):
                self.rotate_left(ptr)
            return self.rotate_right(node)

        elif (self.get_height(node.right) > self.get_height(node.left) + 1):
            ptr = node.right
            if (self.get_height(ptr.left) > self.get_height(ptr.right)):
                self.rotate_right(ptr)
            return self.rotate_left(node)
        else:
            # print('1')
            return node


commands = input().split()

tree = AVLTree()

for i in commands:
    if i == 'print':
        print(tree)
    elif int(i) >= 0:
        tree.add(int(i))
    elif int(i) < 0:
        tree.remove(tree.search(abs(int(i))))