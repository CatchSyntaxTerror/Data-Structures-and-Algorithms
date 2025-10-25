"""
Author: Youssef Amin
This program carries out simple algorithms for as discribed by my HW2 pdf
"""
          
# Problem 1 implement a stack with a bst      

class Node:
    def __init__(self, val, index):
        self.val = val
        self.index = index
        self.right = None
        self.left = None
        
class StackBST:
    order = 0
    
    def __init__(self):
        self.root = None
        
    def push(self, x):
        """
        Assigns numerical order to nodes and appropriatly places them in the tree 
        """
        StackBST.order += 1
        node = Node(x, StackBST.order)
        
        if self.root is None:
            self.root = node
            return
        
        curr = self.root
        
        while True:
            if node.val > curr.val:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = node
                    break
            else:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = node
                    break
                
    def pop(self):
        """
        Searches for the largest order number in the tree,
        removes it, and returns its value.
        """
        if self.root is None:
            return None

        target = StackBST.order

        def find_node(node, parent=None):
            if node is None:
                return None

            if node.index == target:
                if parent is None:
                    self.root = node.left or node.right
                else:
                    if parent.left == node:
                        parent.left = node.left or node.right
                    else:
                        parent.right = node.left or node.right
                return node

            found = find_node(node.left, node)
            if found:
                return found
            return find_node(node.right, node)

        found_node = find_node(self.root)

        if found_node is None:
            return None

        StackBST.order -= 1
        return found_node.val

# test
# stack_bts = StackBST()
# stack_bts.push(15)
# stack_bts.push(2)
# stack_bts.push(30)
# nums = [stack_bts.pop(), stack_bts.pop(), stack_bts.pop()]
# print(", ".join(str(n) for n in nums))


# Problem 2: combining heaps 

def heapify(heap):
    """
    Starting from the last parent node 
    iterate upwards swapping elements with the smallest of its two children
    """
    last_parent = len(heap)//2 - 1
    
    for i in range(last_parent, -1, -1):
        while True:
            l = 2 * i + 1
            r = 2 * i + 2
            smallest = i

            if l < len(heap) and heap[l] < heap[smallest]:
                smallest = l
            if r < len(heap) and heap[r] < heap[smallest]:
                smallest = r

            if smallest == i:
                break
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest

#test
# heap1 = [5, 4, 3, 8, 6]
# heap2 = [3, 7, 4, 9, 5, 7]
# merged = heap1 + heap2
# heapify(heap1)
# heapify(heap2) 
# heapify(merged)
# print(f"heap1: {heap1}")
# print(f"heap2: {heap2}")
# print(f"merged heap: {merged}")


# probem 3, Merging to binary trees in O(m+n)

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, x: int):
        """
        creates a new node from a given integer and inserts it into the binary tree
        by checking the value of the index and inserting it in the first available
        and appropriate spot
        it finds the correct spot by recursive decent
        """
        new_node = Node(x, None)
        
        if self.root is None:
             self.root = new_node
             return
        
        def find_n_place(node: Node):
            val = node.val
            if val > x:
                if node.left is None:
                    node.left = new_node
                else:
                    find_n_place(node.left)
            elif val < x:
                if node.right is None:
                    node.right = new_node
                else:
                    find_n_place(node.right)
        
        find_n_place(self.root)
    
                
    def in_order_traversal(self):
        """
        Recursively decend left to the smallest node. 
        add node to list and then check right branch of each node 
        """
        
        ordered = []
        
        def traverse(node: Node):
            if node:
                traverse(node.left)
                
                ordered.append(node.val)
                
                traverse(node.right)
        
        traverse(self.root)
        return ordered
    
def make_tree_from_list(list: list)->BST:
    """
    This just makes it easier for me to create binary trees 
    and isnt involved in my algorithm
    """
    bst = BST()
    for i in list:
        bst.insert(i)
    return bst


def merge_trees(o1, o2):
    """
    This method takes two lists which represent in order traversals of trees
    it loops through the trees adding the smaller of the two values to a new list which represents
    an in order traversal of a new merged binary tree
    """
    merged = []
    j = 0
    i = 0
    while i < len(o1) and j < len(o2):
        if o1[i] < o2[j]:
            merged.append(o1[i])
            i += 1
        else:
            merged.append(o2[j])
            j += 1
    
    merged.extend(o1[i:])
    merged.extend(o2[j:])
    
    return merged


#test
#creation of trees not involved in runtime
# tree1 = make_tree_from_list([5, 1, 3, 7, 9])
# tree2 = make_tree_from_list([4, 2, 6, 8])

# order1 = tree1.in_order_traversal()
# order2 = tree2.in_order_traversal()
# merged = merge_trees(order1, order2)

# print(f"in order tree1: {order1}")
# print(f"in order tree2: {order2}")
# print(f"tree1 and tree2 merged: {merged}")


# problem 5 finding the largest subsequence of monotonically increasing O(n^2)

def find_mono_increasing(sequence):
    """
    Using two lists, track the longest increasing subsequece
    Loop through sequence for each index i starts at 1 and j starts at 0
    check if the sequence at i is greater than the sequence at j
    if it is add the lessers largest counter to the current largest counter
    record the index of the element that the current element is larger than at the current 
    elements previous
    This creats a back path that we can use to construct the largest monoincreasing subsequence  
    """
    length = len(sequence)
    largest = [1] * length
    previous = [-1] * length
    
    for i in range(1, length):
        for j in range(0, i):
            if sequence[i] > sequence[j]:
                if largest[i] < largest[j] + 1:
                    largest[i] = largest[j] + 1
                    previous[i] = j
                    
    max_i = largest.index(max(largest))
    subsequence = []
    while max_i >= 0:
        subsequence = [sequence[max_i]] + subsequence
        max_i = previous[max_i]
        
    return subsequence

#tests
# A = [3, 10, 2, 1, 20]
# B = find_mono_increasing(A)

# print(f"A: {A}")
# print(f"B: {B}")

# Problem 6: Sorting by permutation order

def order_by_permutation(A, w):
    """
    Reorder A in place according to permutation w
    """
    n = len(A)
    i = 0
    while i < n:
        if w[i] != i + 1:
            j = w[i] - 1
            A[i], A[j] = A[j], A[i]
            w[i], w[j] = w[j], w[i]
        else:
            i += 1
        
        
# tests
# A = [10.5, 9.3, 2.7, 13.6]
# w = [4, 2, 3, 1]
# order_by_permutation(A, w)
# print(f"A: {A}")
# print(f"w: {w}") 
# B = [2, 4, 6, 8]
# mu = [4, 3, 2, 1]       
# order_by_permutation(B, mu)
# print(f"B: {B}")
# print(f"mu: {mu}")

# Problem 8: Finding intervals contained in other intervals
 
def find_contained_intervals(intervals):
    intervals.sort(key=lambda x: (x[0], -x[1]))
    
    contained = []
    end_point = -100000
    
    for x1, x2 in intervals:
        if x2 <= end_point:
            contained.append((x1,x2))
        else:
            end_point = x2
    return contained


# tests
intervals1 = [(1, 2), (3, 6), (4, 5), (0, 7)]
print(f"  Original Intervals: {intervals1}")
contained1 = find_contained_intervals(intervals1)
print(f"  Contained Intervals: {contained1}\n")

intervals2 = [(0, 2), (3, 6), (4, 5), (3, 7)]
print(f"  Original Intervals: {intervals2}")
contained2 = find_contained_intervals(intervals2)
print(f"  Contained Intervals: {contained2}\n")

intervals3 = [(0, 1), (3, 6), (4, 11), (3, 7)]
print(f"  Original Intervals: {intervals3}")
contained3 = find_contained_intervals(intervals3)
print(f"  Contained Intervals: {contained3}")
