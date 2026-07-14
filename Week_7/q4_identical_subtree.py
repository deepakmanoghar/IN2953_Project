"""
Q4. Given two binary trees, write a function to check if they are identical.
    Then write another to check if one is a subtree of the other.
"""

from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────
# Helper: build tree from level-order list
# ─────────────────────────────────────────────
def build_tree(values):
    if not values:
        return None
    root = Node(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = Node(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = Node(values[i])
            queue.append(node.right)
        i += 1
    return root


# ═══════════════════════════════════════════════
# 1. Check if two trees are IDENTICAL
# ═══════════════════════════════════════════════
def are_identical(t1, t2):
    """
    Two trees are identical if:
      - Both are None              → True
      - One is None, other isn't  → False
      - Root values differ         → False
      - Left subtrees are identical AND right subtrees are identical
    Time: O(n)  Space: O(h)
    """
    if t1 is None and t2 is None:
        return True
    if t1 is None or t2 is None:
        return False
    if t1.val != t2.val:
        return False
    return are_identical(t1.left, t2.left) and are_identical(t1.right, t2.right)


# ═══════════════════════════════════════════════
# 2. Check if one tree is a SUBTREE of another
# ═══════════════════════════════════════════════
def is_subtree(main_tree, sub_tree):
    """
    sub_tree is a subtree of main_tree if there exists a node in
    main_tree such that the subtree rooted at that node is identical
    to sub_tree.

    Approach:
      - For every node in main_tree, check are_identical(node, sub_tree).
      - If any call returns True, sub_tree is found.

    Time:  O(m * n)  where m = nodes in main_tree, n = nodes in sub_tree.
    Space: O(h_main) recursion stack.
    """
    if sub_tree is None:
        return True          # empty tree is subtree of anything
    if main_tree is None:
        return False         # non-empty sub_tree can't exist in empty tree

    if are_identical(main_tree, sub_tree):
        return True

    # Search in left and right subtrees of main_tree
    return is_subtree(main_tree.left, sub_tree) or \
           is_subtree(main_tree.right, sub_tree)


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # ── Identical Trees ────────────────────────
    print("=" * 50)
    print("IDENTICAL TREES TEST")
    print("=" * 50)

    tA = build_tree([1, 2, 3, 4, 5])
    tB = build_tree([1, 2, 3, 4, 5])
    tC = build_tree([1, 2, 3, 4, 6])   # differs at last node

    print("Tree A: [1, 2, 3, 4, 5]")
    print("Tree B: [1, 2, 3, 4, 5]")
    print("Tree C: [1, 2, 3, 4, 6]")
    print()
    print(f"A identical to B? {are_identical(tA, tB)}")   # True
    print(f"A identical to C? {are_identical(tA, tC)}")   # False

    # ── Subtree ────────────────────────────────
    print("\n" + "=" * 50)
    print("SUBTREE TEST")
    print("=" * 50)

    #  Main tree:         Sub tree:
    #       3                 4
    #      / \               / \
    #     4   5             1   2
    #    / \
    #   1   2

    main = build_tree([3, 4, 5, 1, 2])
    sub1 = build_tree([4, 1, 2])          # IS a subtree
    sub2 = build_tree([4, 1, 3])          # is NOT a subtree (3 ≠ 2)
    sub3 = Node(5)                         # single node subtree

    print("Main tree : [3, 4, 5, 1, 2]")
    print("Sub1      : [4, 1, 2]  <- should be subtree")
    print("Sub2      : [4, 1, 3]  <- should NOT be subtree")
    print("Sub3      : [5]        <- single node, should be subtree")
    print()
    print(f"Is sub1 a subtree of main? {is_subtree(main, sub1)}")   # True
    print(f"Is sub2 a subtree of main? {is_subtree(main, sub2)}")   # False
    print(f"Is sub3 a subtree of main? {is_subtree(main, sub3)}")   # True
