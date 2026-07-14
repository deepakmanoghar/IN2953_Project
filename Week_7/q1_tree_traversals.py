"""
Q1. Implement all four tree traversals (preorder, inorder, postorder, level-order)
    both recursively and iteratively. Test with a tree of depth 4.
"""

from collections import deque


# ─────────────────────────────────────────────
# Node definition
# ─────────────────────────────────────────────
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────
# Build a sample tree of depth 4
#
#            1
#          /   \
#         2     3
#        / \   / \
#       4   5 6   7
#      / \
#     8   9
#
# ─────────────────────────────────────────────
def build_depth4_tree():
    root = Node(1)
    root.left          = Node(2)
    root.right         = Node(3)
    root.left.left     = Node(4)
    root.left.right    = Node(5)
    root.right.left    = Node(6)
    root.right.right   = Node(7)
    root.left.left.left  = Node(8)
    root.left.left.right = Node(9)
    return root


# ═══════════════════════════════════════════════
# 1. PREORDER  (Root → Left → Right)
# ═══════════════════════════════════════════════
def preorder_recursive(node, result=None):
    if result is None:
        result = []
    if node:
        result.append(node.val)
        preorder_recursive(node.left, result)
        preorder_recursive(node.right, result)
    return result


def preorder_iterative(root):
    if not root:
        return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        # push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


# ═══════════════════════════════════════════════
# 2. INORDER   (Left → Root → Right)
# ═══════════════════════════════════════════════
def inorder_recursive(node, result=None):
    if result is None:
        result = []
    if node:
        inorder_recursive(node.left, result)
        result.append(node.val)
        inorder_recursive(node.right, result)
    return result


def inorder_iterative(root):
    result, stack = [], []
    current = root
    while current or stack:
        # go as far left as possible
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right
    return result


# ═══════════════════════════════════════════════
# 3. POSTORDER (Left → Right → Root)
# ═══════════════════════════════════════════════
def postorder_recursive(node, result=None):
    if result is None:
        result = []
    if node:
        postorder_recursive(node.left, result)
        postorder_recursive(node.right, result)
        result.append(node.val)
    return result


def postorder_iterative(root):
    if not root:
        return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    # reverse gives Left → Right → Root
    return result[::-1]


# ═══════════════════════════════════════════════
# 4. LEVEL-ORDER (BFS)
# ═══════════════════════════════════════════════
def levelorder_recursive(root):
    """Returns a list-of-lists, one list per level."""
    result = []

    def helper(node, level):
        if not node:
            return
        if level == len(result):
            result.append([])
        result[level].append(node.val)
        helper(node.left,  level + 1)
        helper(node.right, level + 1)

    helper(root, 0)
    return result


def levelorder_iterative(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = build_depth4_tree()

    print("=" * 50)
    print("Tree structure (depth 4)")
    print("         1")
    print("       /   \\")
    print("      2     3")
    print("     / \\   / \\")
    print("    4   5 6   7")
    print("   / \\")
    print("  8   9")
    print("=" * 50)

    print("\n--- PREORDER (Root -> Left -> Right) ---")
    print("Recursive:", preorder_recursive(root))
    print("Iterative:", preorder_iterative(root))

    print("\n--- INORDER  (Left -> Root -> Right) ---")
    print("Recursive:", inorder_recursive(root))
    print("Iterative:", inorder_iterative(root))

    print("\n--- POSTORDER (Left -> Right -> Root) ---")
    print("Recursive:", postorder_recursive(root))
    print("Iterative:", postorder_iterative(root))

    print("\n--- LEVEL-ORDER (BFS) ---")
    print("Recursive:", levelorder_recursive(root))
    print("Iterative:", levelorder_iterative(root))
