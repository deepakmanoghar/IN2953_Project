"""
Q2. Write a function to find the maximum depth of a binary tree.
    Then modify it to find the minimum depth
    (shortest path from root to nearest leaf).
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────
# Maximum Depth
# ─────────────────────────────────────────────
def max_depth(root):
    """
    Recursively: depth = 1 + max(left_depth, right_depth).
    Base case: None → 0.
    Time: O(n)  Space: O(h) where h = height of tree.
    """
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# ─────────────────────────────────────────────
# Minimum Depth
# ─────────────────────────────────────────────
def min_depth(root):
    """
    The tricky part: if a node has only ONE child, we must NOT count
    the missing side (which would give 0 + 1 = 1 and never reach a leaf).
    Rules:
      1. None            → 0
      2. Leaf            → 1
      3. Only left child → 1 + min_depth(left)
      4. Only right child→ 1 + min_depth(right)
      5. Both children   → 1 + min(min_depth(left), min_depth(right))
    Time: O(n)  Space: O(h)
    """
    if root is None:
        return 0
    # leaf node
    if root.left is None and root.right is None:
        return 1
    # only right subtree exists
    if root.left is None:
        return 1 + min_depth(root.right)
    # only left subtree exists
    if root.right is None:
        return 1 + min_depth(root.left)
    # both children exist
    return 1 + min(min_depth(root.left), min_depth(root.right))


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Tree 1 – balanced
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    t1 = Node(1)
    t1.left        = Node(2)
    t1.right       = Node(3)
    t1.left.left   = Node(4)
    t1.left.right  = Node(5)

    print("Tree 1:")
    print("        1")
    print("       / \\")
    print("      2   3")
    print("     / \\")
    print("    4   5")
    print(f"  Max Depth : {max_depth(t1)}")   # 3
    print(f"  Min Depth : {min_depth(t1)}")   # 2 (1→3 is the shortest leaf path)

    # Tree 2 – skewed (linked list style)
    #  1 → 2 → 3 → 4
    t2 = Node(1)
    t2.left       = Node(2)
    t2.left.left  = Node(3)
    t2.left.left.left = Node(4)

    print("\nTree 2 (skewed):")
    print("  1 - 2 - 3 - 4")
    print(f"  Max Depth : {max_depth(t2)}")   # 4
    print(f"  Min Depth : {min_depth(t2)}")   # 4 (only one path)

    # Tree 3 – single node
    t3 = Node(42)
    print("\nTree 3 (single node: 42):")
    print(f"  Max Depth : {max_depth(t3)}")   # 1
    print(f"  Min Depth : {min_depth(t3)}")   # 1
