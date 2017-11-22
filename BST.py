class BSTNode():
    def __init__(self, val = None):
        self.left = None
        self.right = None
        self.parent = None

        self.val = val

    def __repr__(self):
        return '{}({})'.format('BSTNode', str(self.val))

    def printTree(self):
        def helper(node):
            return '({}){}({})'.format( helper(node.left), str(node.val), helper(node.right) ) \
                    if node else ''

        return helper(self).replace('()', '')

    def grandparent(self):
        return self.parent and self.parent.parent

    def sibling(self):
        p = self.parent
        return p and (p.left if p.left != self else p.right)

    def sib_before_deletion(self):
        """
        use this when self has been deleted from the tree
        use this only when sibling != None
        """
        p = self.parent
        return p and (p.left if p.left and p.left != self else p.right)

    def uncle(self):
        return self.parent and self.parent.sibling()

    def rotate_left(self):
        """
        self is the right child of its parent and is rotating to the left
        please make sure: self and self.parent != None
        """
        p = self.parent
        gp = p.parent
        child = self.left

        p.right, p.parent, self.left, self.parent = self.left, self, p, p.parent

        if gp:
            if gp.left == p:
                gp.left = self
            else:
                gp.right = self

        if child:
            child.parent = p

    def rotate_right(self):
        """
        self is the left child of its parent and is rotating to the right
        please make sure: self and self.parent != None
        """
        p = self.parent
        gp = p.parent
        child = self.right

        p.left, p.parent, self.right, self.parent = self.right, self, p, p.parent

        if gp:
            if gp.left == p:
                gp.left = self
            else:
                gp.right = self

        if child:
            child.parent = p

    def next(self):
        """
        the next element in the inorder traversal
        """
        node = self
        while node and not node.right:
            node = node.parent
        if not node:
            return

        node = self.right
        while node.left:
            node = node.left
        return node

    def prev(self):
        node = self
        while node and not node.left:
            node = node.parent
        if not node:
            return

        node = self.left
        while node.right:
            node = node.right
        return node
# END of BSTNode

class BST():
    def __init__(self, s = None):
        def init_helper(nums):
            if not nums:
                return None

            head = BSTNode(nums[len(nums)/2])

            head.left = init_helper( nums[:len(nums)/2] )
            head.right = init_helper( nums[len(nums)/2+1:] )

            if head.left:
                head.left.parent = head
            if head.right:
                head.right.parent = head

            return head

        self.root = init_helper( sorted(s)  )

    def __iter__(self):  # inorder traversal
        stack = []
        node = self.root
        while node:
            stack.append(node)
            node = node.left

        # we could use node.next() function here. This version is faster and just use O(log n) space
        while stack:
            node = stack.pop()
            yield node.val

            node = node.right
            while node:
                stack.append(node)
                node = node.left

    def __str__(self):
        return ' '.join(str(n) for n in iter(self))

    def __repr__(self):
        return self.root.printTree()

    def insert(self, n):
        def insert_helper(node):
            if n <= node.val:
                if node.left:
                    insert_helper(node.left)
                else:
                    node.left = BSTNode(n)
                    node.left.parent = node
            else:
                if node.right:
                    insert_helper(node.right)
                else:
                    node.right = BSTNode(n)
                    node.right.parent = node
        
        if self.root:
            insert_helper(self.root)
        else:
            self.root = BSTNode(n)

    def delete(self, n):
        """
        delete the highest possible node whose value is n
        returns the 'actually deleted' node if we delete anything and it is not the root
        """
        d = self.root
        while d and n != d.val:
            d = d.left if n < d.val else d.right

        if not d:
            print 'no such node'
            return

        if d.left:
            pre = d.prev()
            
            d.val = pre.val
            if pre.parent == d:
                d.left = pre.left
            else:
                pre.parent.right = pre.left

            if pre.left:
                pre.left.parent = pre.parent
            return pre
        elif d.right:
            nxt = d.next()

            d.val = nxt.val
            if nxt.parent == d:
                d.right = nxt.right
            else:
                nxt.parent.left = nxt.right

            if nxt.right:
                nxt.right.parent = nxt.parent
            return nxt
        elif not d.parent:
            self.root = None
        else:
            p = d.parent
            if n < p.val:
                p.left = None
            else:
                p.right = None
            return d

    def search(self, n):
        """
        serach if there is a node whose value is n
        """
        node = self.root
        while node and n != node.val:
            node = node.left if n < node.val else node.right

        return node != None

    def largestLessThan(self, n, strict = True):
        """
        will return None if there is no such number
        """
        node = self.root
        result = None

        if strict:
            while node:
                if n <= node.val:
                    node = node.left
                else:
                    result = node.val
                    node = node.right
        else:
            while node:
                if n < node.val:
                    node = node.left
                elif n > node.val:
                    result = node.val
                    node = node.right
                else:
                    return n
        
        return result

    def smallestGreaterThan(self, n, strict = True):
        """
        will return None if there is no such number
        """
        node = self.root
        result = None

        if strict:
            while node:
                if n >= node.val:
                    node = node.right
                else:
                    result = node.val
                    node = node.left
        else:
            while node:
                if n > node.val:
                    node = node.right
                elif n < node.val:
                    result = d.val
                    node = node.left
                else:
                    return n
        
        return result
# END of BST


class RBTNode(BSTNode):
    def __init__(self, val = None, color = 1):
        BSTNode.__init__(self, val)

        self.color = color # default color is 1 which means red

    def __repr__(self):
        return '{}({}, {})'.format('RBTNode', str(self.val), str(self.color))


    # from DaShen
    # https://dreampuf.github.io/GraphvizOnline/
    # use the above website to visualize
    def graphviz(self):

        node = 'node{} [style=filled, color={}]\n'.format(self.val, 'red' if self.color else 'grey')
        relation = []

        if self.left:
            relation.append('node{} -> node{}\n'.format(self.val, self.left.val))

        if self.right:
            relation.append('node{} -> node{}\n'.format(self.val, self.right.val))

        return ''.join([node]+relation)

    def graphviz_all(self):

        output = self.graphviz()
        if self.left:
            output += self.left.graphviz_all()
        if self.right:
            output += self.right.graphviz_all()

        return output

    def printTree(self):
        def helper(node):
            return '({}){}({})'.format( helper(node.left), str(node.val)+','+str(node.color), helper(node.right) ) \
                    if node else ''

        return helper(self).replace('()', '')
# END of BRTNode

class RBT(BST):
    def __init__(self, s = None):
        """
        RBTree has to satisfiy the following properties:
        1. All nodes are either red (1) or black (0)
        2. All leaves (they are None's in this implementation) are black (0)
        3. If a node is red (1), then both of its children are black (0)
        4. Every path from a given node to any of its descendant None node (leave) contains the same number of black nodes
        5. The root is black (0)
        """
        self.root = None
        if s:
            map(self.insert, s)

    def __repr__(self):
        return self.root.printTree()

    def graphvizTree(self):
        return self.root.graphviz_all()

    def isBlack(self, node):
        """
        this function is independent of the RBTree
        """
        return node == None or node.color == 0

    def insert(self, n):
        def insert_helper(node):
            """
            node is the root of the tree in which we want to insert the value n
            returns the inserted node
            """
            if n <= node.val:
                if node.left:
                    return insert_helper(node.left)
                else:
                    node.left = RBTNode(n)
                    node.left.parent = node
                    return node.left
            else:
                if node.right:
                    return insert_helper(node.right)
                else:
                    node.right = RBTNode(n)
                    node.right.parent = node
                    return node.right

        def insert_repair(node):
            """
            after insertion, repair the tree so that it satisfies the RBTree properties
            """
            # node.color is red (1)
            if node == self.root:
                #print 'insert repair step 1'
                node.color = 0
                return

            if node.parent.color == 0:
                #print 'insert repair step 2'
                return

            # now node.parent.color is red (1), so we must have grandparent whose color is black (0) and we must have uncle (might be leaf)
            uncle = node.uncle()
            gp = node.grandparent()
            if uncle and uncle.color == 1:
                #print 'insert repair step 3'
                uncle.color, node.parent.color = 0, 0
                gp.color = 1
                insert_repair(gp)
                return

            # now node.parent.color = 1 and node.uncle().color = 0
            if node == node.parent.left and node.parent == gp.right:
                #print 'insert repair step 4.1 rotate_right'
                node.rotate_right()
            elif node == node.parent.right and node.parent == gp.left:
                #print 'insert repair step 4.1 rotate_left'
                node.rotate_left()
            else:
                node = node.parent

            # now node.color = 1, node.sibling().color = 0, node.parent.color = 0, ready to rotate
            if gp.left == node:
                #print 'insert repair step 4.2 rotate_right'
                node.rotate_right()
            else:
                #print 'insert repair step 4.2 rotate_left'
                node.rotate_left()
            node.color = 0
            node.left.color, node.right.color = 1, 1
        # the end of repair

        if not self.root:
            node = self.root = RBTNode(n)
        else:
            node = insert_helper(self.root) # insert_helper returns the node we inserted.

        insert_repair(node)

        # find the neww root of the tree
        while node.parent:
            node = node.parent
        self.root = node

    def delete(self, n):
        node = BST.delete(self, n)
        if not node or node.color == 1:
            return

        # node.color = 0
        child = node.left or node.right
        if child:   # if non-leaf child exists, its color must be 1
            child.color = 0
            return

        # node.color = 0, node has only leaf children
        # so all paths passing through node essentially has one fewer black, so we have to recursively go up.
        def delete_repair(node):
            """
            all paths passing through 'node' essentially has one fewer black
            ('essentially' means all 'node''s children including itself are already black but still one fewer black)
            the goal is to rebalance black counts of paths
            warning: node might have been deleted from the tree!
            """
            # node.color = 0
            if not node.parent:
                return

            sib = node.sib_before_deletion()
            p = node.parent
            if sib.color == 1:
                if sib == p.right:
                    sib.rotate_left()
                else:
                    sib.rotate_right()

                sib.color = 0
                p.color = 1

                sib = node.sib_before_deletion()

            # node.color = 0, sib.color = 0
            if self.isBlack(sib.left) and self.isBlack(sib.right): 
            # if both of sib's children are black (0)
                sib.color = 1

                if p.color == 1:
                    p.color = 0
                else:
                    delete_repair(p)
                return

            # node.color = 0, sib.color = 0, and at least one of the children is red
            if sib == p.left and self.isBlack(sib.left):
                sib = sib.right
                sib.rotate_left()

                sib.color = 0
                sib.left.color = 1
            elif sib == p.right and self.isBlack(sib.right):
                sib = sib.left
                sib.rotate_right()

                sib.color = 0
                sib.right.color = 1

            # node.color = 0, sib.color = 0, and the child on the same direction is red, so ready to rotate
            if sib == p.left:
                sib.rotate_right()
                sib.left.color = 0
            else:
                sib.rotate_left()
                sib.right.color = 0

            sib.color, p.color = p.color, sib.color

        delete_repair(node)

        while node.parent:
            node = node.parent
        self.root = node
    # end of delete
# END of RBT

