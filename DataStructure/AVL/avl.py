import random
from avlnode import AVLNode

import logging



def debug(msg):
    logging.debug(msg)

class AVLTree():
    def __init__(self):
        self.root = None

    def insert(self, key, value=None, duplicated_keys=False):
        newnode = AVLNode(key, value)
        debug("[+] New node created: [{0}; {1}]".format(key, value))
        self.root = self._insert(self.root, newnode, duplicated_keys)

    def _insert(self, root: AVLNode, newnode: AVLNode, duplicated_keys=False) -> AVLNode:
        debug("[+] Inserting {0} (root: {1})".format(newnode, root))
        if not root: 
            return newnode
        elif newnode.key < root.key: 
            debug("[+] Going left")
            root.left = self._insert(root.left, newnode, duplicated_keys)
        elif newnode.key > root.key: 
            debug("[+] Going right")
            root.right = self._insert(root.right, newnode, duplicated_keys)
        else:
            if duplicated_keys:
                if type(root.value) is not list:
                    aux = root.value
                    root.value = []
                    root.value.append(aux)
                root.value.append(newnode.value)
            else:
                return root 
        root.update_height()
        debug("[+] Updated height of node {0}".format(root))
        return self._rebalance(root)

    def _rebalance(self, root: AVLNode) -> AVLNode:
        bf = root.get_balance_factor()
        if bf > 1:
            if root.right.get_height(root.right.right) > root.right.get_height(root.right.left): # left-left imbalance
                root = self._left_rotate(root)
            else: 
                root = self._right_left_rotate(root)
        elif bf < -1:
            if root.left.get_height(root.left.left) > root.left.get_height(root.left.right): # right-right imbalance
                root = self._right_rotate(root)
            else: 
                root = self._left_right_rotate(root)
            
        return root

    def _right_rotate(self, root: AVLNode) -> AVLNode:
        debug("[+] Right rotation ")
        tmp = root.left
        root.left = tmp.right
        tmp.right = root

        root.update_height()
        tmp.update_height()

        return tmp

    def _left_right_rotate(self, root: AVLNode) -> AVLNode:
        debug("[*] Left-Right rotation ")
        root.left = self._left_rotate(root.left)
        return self._right_rotate(root)
    
    def _left_rotate(self, root: AVLNode) -> AVLNode:
        debug("[+] Left rotation ")
        tmp = root.right
        root.right = tmp.left
        tmp.left = root

        root.update_height()
        tmp.update_height()

        return tmp

    def _right_left_rotate(self, root: AVLNode) -> AVLNode:
        debug("[+] Right-Left rotation ")
        root.right = self._right_rotate(root.right)
        return self._left_rotate(root)

    def _remove(self, root: AVLNode, key) -> AVLNode:
        if root is None:
            return None
        elif key < root.key:
            root.left = self._remove(root.left, key)
        elif key > root.key:
            root.right = self._remove(root.right, key)
        else: 
            if root.left is None and root.right is None:
                return None
            elif root.left is None:
                root = root.right
            elif root.right is None:
                
                root = root.left
            else:
                
                aux = self.find_min(root.right)
                root.update_content(aux)
                root.right = self.remove(root.right, aux.key)
        
        
        root.update_height()
        if root is not None:
            root = self._rebalance(root)

        return root
    
    def remove(self, key):
        if self.root is None:
            print('[-] AVL tree is empty!')
        else:
            self.root = self._remove(self.root, key)

    def _display(self, node: AVLNode, level=0, prefix=''):
        if node != None:
            print('{0}{1}{2}'.format('-'*level, prefix, node))
            if node.left != None:
                self._display(node.left, level + 1, '<')
            if node.right != None:
                self._display(node.right, level + 1, '>')

    def display(self):
        debug("[+] Displaying the AVL ...")
        if self.root != None:
            self._display(self.root)
        else:
            print('[-] AVL tree is empty!')
    
    def _post_order(self, node: AVLNode):
        _str = ""
        if node is not None:
            _str = _str + self._post_order(node.left)
            _str = _str + self._post_order(node.right)
            _str = str(_str) + str(node) + ';'
        return _str

    def post_order(self, print_to_stdout=True):
        _str = self._post_order(self.root)
        if print_to_stdout:
            print(_str)
        
        return _str
    
    def _pre_order(self, node: AVLNode):
        _str = ""
        if node is not None:
            _str = _str + str(node) + ';'
            _str = _str + self._pre_order(node.left)
            _str = _str + self._pre_order(node.right)
        return _str

    def pre_order(self, print_to_stdout=True):
        _str = self._pre_order(self.root)
        if print_to_stdout:
            print(_str)
        return _str

    def _in_order(self, node: AVLNode):
        _str = ""
        if node is not None:
            _str = _str + self._in_order(node.left)
            _str = _str + str(node) + ';'
            _str = _str + self._in_order(node.right)
        return _str

    def in_order(self, print_to_stdout=True):
        _str = self._in_order(self.root)
        if print_to_stdout:
            print(_str)
        return _str

    def _find_max(self, root: AVLNode) -> AVLNode:
        if root.right is None:
            return root
        else:
            return self._find_max(root.right)



    


    def _search(self, root: AVLNode, key) -> AVLNode:
        if root is None:
            return None
        elif key < root.key:
            return self._search(root.left, key)
        elif key > root.key:
            return self._search(root.right, key)
        else: 
            return root

    

    def get_height(self) -> int:

        if self.root is None:
            return 0
        else:
            return self.root.get_height()

    def _get_count(self, root: AVLNode) -> int:
        if root is None:
            return 0
        count = 1
        if root.left:
            count = count + self._get_count(root.left)
        if root.right:
            count = count + self._get_count(root.right)
        return count

    def get_count(self) -> int:
        return self._get_count(self.root)


if __name__ == "__main__":
    a = AVLTree()
    print("[*] Inserting random data ...")
    randomlist = [1, 2, 3, 7,6]   # => 5num
    print("[*] Data: " + str(randomlist))
    
    for i in randomlist:
        a.insert(i)
    
    print("current AVL:")
    a.display()
    
    #please enter every node you want to remove or insert in the lower variables
    
    node_tobe_remove1 = 1
    a.remove(node_tobe_remove1)
    print('After removing the node', node_tobe_remove1 )
    a.display()
    
    
    node_tobe_remove2 = 2
    a.remove(node_tobe_remove2)
    print('After removing the node', node_tobe_remove2 )
    a.display()
    
    node_tobe_insert1 = 5
    a.insert(node_tobe_insert1)
    print('After inserting the node', node_tobe_insert1 )
    a.display()
    node_tobe_insert2 = 4
    a.insert(node_tobe_insert2)
    print('After inserting the node', node_tobe_insert2 )
    a.display()
    
    node_tobe_insert3 = 10
    a.insert(node_tobe_insert3)
    print('After inserting the node', node_tobe_insert3 )
    a.display()
    node_tobe_insert4 = 8
    a.insert(node_tobe_insert4)
    print('After inserting the node', node_tobe_insert4 )
    a.display()


    print('Number of nodes: ' + str(a.get_count()))
    

