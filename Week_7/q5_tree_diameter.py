"""
Q5. Write a function to find the diameter of a binary tree
    (longest path between any two nodes).

    Explain why a simple approach of left_height + right_height at
    every node works.

    ─────────────────────────────────────────────────────────────────
    EXPLANATION
    ─────────────────────────────────────────────────────────────────
    The diameter of a binary tree is the length of the longest path
    between any two leaf nodes (the path may or may not pass through
    the root).

    KEY INSIGHT
    ───────────
    For every node N, the longest path that PASSES THROUGH N is:
        left_height(N) + right_height(N)
    because the path goes:
        (deepest node in left subtree) → N → (deepest node in right subtree)

    Why does this work?
    • The height of a subtree rooted at a node is the number of edges
      on the longest path from that node downward to a leaf.
    • Summing the left and right heights gives the total edge count
      of the longest path that uses N as the "turning point."
    • By computing this value at EVERY node and keeping a running
      maximum, we guarantee we don't miss any path, because every
      path in the tree must have some highest node (LCA of its endpoints)
      through which it "bends."
    • We never need to check paths that don't pass through the current
      root because those are handled when we recurse into child nodes.

    ALGORITHM (optimised – single DFS pass)
    ────────────────────────────────────────
    Instead of two separate calls (one for height, one for diameter),
    we compute height bottom-up and update the diameter in the same
    DFS pass.

    Time:  O(n)   – each node visited once.
    Space: O(h)   – recursion stack (h = height of tree).
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────
# Approach 1: Naïve O(n²)
# ─────────────────────────────────────────────
def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def diameter_naive(root):
    """
    For every node compute left_height + right_height.
    Recurse into subtrees to find their own diameters.
    Take the maximum. O(n²) because height() is called repeatedly.
    """
    if root is None:
        return 0
    # diameter passing through current root
    through_root = height(root.left) + height(root.right)
    # diameter entirely in left or right subtree
    left_diam  = diameter_naive(root.left)
    right_diam = diameter_naive(root.right)
    return max(through_root, left_diam, right_diam)


# ─────────────────────────────────────────────
# Approach 2: Optimised O(n)
# ─────────────────────────────────────────────
def diameter_optimised(root):
    """
    Single DFS: each call returns the height of the subtree while
    updating a shared 'max_diameter' variable.
    """
    max_diameter = [0]   # use list so inner function can mutate it

    def dfs(node):
        if node is None:
            return 0
        left_h  = dfs(node.left)
        right_h = dfs(node.right)
        # update global diameter at this node
        max_diameter[0] = max(max_diameter[0], left_h + right_h)
        return 1 + max(left_h, right_h)

    dfs(root)
    return max_diameter[0]


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    #
    #         1
    #        / \
    #       2   3
    #      / \
    #     4   5
    #    /
    #   6
    #
    # Longest path: 6 → 4 → 2 → 5  or  6 → 4 → 2 → 1 → 3
    # Diameter = 4 edges

    root = Node(1)
    root.left           = Node(2)
    root.right          = Node(3)
    root.left.left      = Node(4)
    root.left.right     = Node(5)
    root.left.left.left = Node(6)

    print("Tree:")
    print("        1")
    print("       / \\")
    print("      2   3")
    print("     / \\")
    print("    4   5")
    print("   /")
    print("  6")
    print()
    print(f"Diameter (naive  O(n^2)): {diameter_naive(root)}")       # 4
    print(f"Diameter (optimised O(n)): {diameter_optimised(root)}") # 4

    # Edge cases
    single = Node(1)
    print(f"\nSingle node diameter: {diameter_optimised(single)}")   # 0

    line = Node(1)
    line.left = Node(2)
    line.left.left = Node(3)
    print(f"Linear tree 1-2-3 diameter: {diameter_optimised(line)}") # 2
