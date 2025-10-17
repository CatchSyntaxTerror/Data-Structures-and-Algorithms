import numpy as np
from scipy.optimize import linprog

"""
Author: Youssef Amin
This program uses numpy and scipy to solve hw questions from my Data Structures and Algorithms class 
"""
# * question 1
print("\n\nquestion 1")

edges = [(0,1), (0,4), (1,2), (1,3), (2,5), (3,4), (3,5), (4,5)]
costs = np.array([8, 6, 1, 3, 1, 5, 3, 5])
capacity = np.array([5, 1, 1, 2, 1, 2, 3, 2])
bounds = [(0,i) for i in capacity]
num_nodes = 6

ballance = np.zeros(6)
ballance[0] = -1
ballance[5] = 1

A = np.zeros((num_nodes, len(edges)))
for i, (u,v) in enumerate(edges):
    A[u, i] -= 1
    A[v, i] += 1


sol = linprog(costs, A_eq = A, b_eq = ballance, bounds = bounds, method="highs")
print("Optimal cost: ", sol.fun)

for val, e in zip(sol.x, edges):
    if val > 1e-9:
        print(f"flow {val:.3f} on edge {e}")


# * question 2
print("\n\nquestion 2")

bounds1 = [(0, None), (0, None)]

A1 = np.array([[-1,-1], [600, 2300], [1,-2], [-2,1]])
b1 = np.array([-10, 10000, 0, 0])
c = np.array([600, 2300])

sol1 = linprog(c, A_ub = A1, b_ub = b1, bounds = bounds1, method = "highs")


print("Solution: ", sol1.fun)

# * question 3
print("\n\nquestion 3")

cards = [8, 8, 5, 7, 8, 3, 6]
n = len(cards)

def find_local_min(arr, low, high):
    """
    binary search without sorting
    """
    if low == high:
        return arr[low]
    
    i = (low + high) // 2
    
    left_ok  = (i == 0) or (arr[i] <= arr[i - 1])
    right_ok = (i == len(arr) - 1) or (arr[i] <= arr[i + 1])
    
    if left_ok and right_ok:
        return arr[i]
    
    if i > 0 and arr[i - 1] < arr[i]:
        return find_local_min(arr, low, i - 1)
    return find_local_min(arr, i + 1, high)


sol2 = find_local_min(cards, 0, n-1)

print("local min: ", sol2)


# * question 6
print("question 6")

def is_tree(num, dict):
    """
    checks if given graph is a tree
    """
    if (num == 0) or (num == 1):
        return True
    
    visited = [False] * num
    parent = [-1] * num
    
    if not check_no_cycles(0, visited, parent, dict):
        return False
    
    for i in range(num):
        if not visited[i]:
            return False
        
    edges = 0
    for i in range(num):
        edges += len(dict.get(i, []))
    edges //= 2
    if not edges == num - 1:
        return False
    
    return True
        
    
def check_no_cycles(u, visited, parent, dict):
    """
    Used to detect cycles 
    """
    visited[u] = True
    for v in dict.get(u, []):
        if not visited[v]:
            parent[v] = u
            if not check_no_cycles(v, visited, parent, dict):
                return False
        elif v != parent[u]:
            return False
    return True 


tree_graph = {
    0: [1],
    1: [0, 2],
    2: [1]
}

not_tree_graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1]
}
print("Testing tree_graph: ", is_tree(3, tree_graph))
print("Testing not_tree_graph: ", is_tree(3, not_tree_graph))
