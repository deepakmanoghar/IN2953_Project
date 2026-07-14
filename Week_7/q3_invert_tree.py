r"""
Q3. Implement invert (mirror) a binary tree.
    Draw the tree before and after inversion for: [4, 2, 7, 1, 3, 6, 9].

    Original:
            4
          /   \
         2     7
        / \   / \
       1   3 6   9

    Inverted (mirrored):
            4
          /   \
         7     2
        / \   / \
       9   6 3   1
"""

from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────
# Build tree from level-order list
# ─────────────────────────────────────────────
def build_tree(values):
    """Builds a complete binary tree from a level-order list."""
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


# ─────────────────────────────────────────────
# Pretty-print the tree (rotated 90° sideways)
# ─────────────────────────────────────────────
def print_tree(node, prefix="", is_left=True):
    if node is None:
        return
    print_tree(node.right, prefix + ("|   " if is_left else "    "), False)
    print(prefix + ("+-- " if is_left else "+-- ") + str(node.val))
    print_tree(node.left, prefix + ("    " if is_left else "|   "), True)


# ─────────────────────────────────────────────
# Invert (mirror) the tree — RECURSIVE
# ─────────────────────────────────────────────
def invert_tree(root):
    """
    At every node swap left and right children, then recurse.
    Time: O(n)  —  every node visited once.
    Space: O(h) —  recursion stack (h = height).
    """
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root


# ─────────────────────────────────────────────
# Invert (mirror) the tree — ITERATIVE (BFS)
# ─────────────────────────────────────────────
def invert_tree_iterative(root):
    if not root:
        return None
    queue = deque([root])
    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return root


# ─────────────────────────────────────────────
# Level-order list helper (for display)
# ─────────────────────────────────────────────
def level_order_list(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    values = [4, 2, 7, 1, 3, 6, 9]
    root = build_tree(values)

    print("=" * 45)
    print("ORIGINAL TREE  (level-order input:", values, ")")
    print("=" * 45)
    print("""
            4
          /   \\
         2     7
        / \\   / \\
       1   3 6   9
    """)
    print("Sideways view:")
    print_tree(root)
    print("\nLevel-order:", level_order_list(root))

    # Invert
    invert_tree(root)

    print("\n" + "=" * 45)
    print("INVERTED (MIRRORED) TREE")
    print("=" * 45)
    print("""
            4
          /   \\
         7     2
        / \\   / \\
       9   6 3   1
    """)
    print("Sideways view:")
    print_tree(root)
    print("\nLevel-order:", level_order_list(root))
