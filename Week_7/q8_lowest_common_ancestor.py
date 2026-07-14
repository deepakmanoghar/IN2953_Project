"""
Q8. Find the lowest common ancestor (LCA) of two nodes in a binary tree.
    What changes if it is a Binary Search Tree instead?

    ─────────────────────────────────────────────────────────────────
    LOWEST COMMON ANCESTOR — Binary Tree (General)
    ─────────────────────────────────────────────────────────────────
    Definition:
        The LCA of two nodes p and q is the deepest node in the tree
        that has both p and q as descendants (a node is a descendant
        of itself).

    Algorithm (Recursive post-order DFS):
    1. If current node is None  → return None.
    2. If current node is p or q → return current node (found one target).
    3. Recurse into left and right subtrees.
    4. If BOTH left and right return non-None → current node is the LCA
       (p is on one side, q is on the other).
    5. Otherwise return whichever side returned non-None (both targets
       may be in the same subtree).

    Time:  O(n)  — visit every node once in worst case.
    Space: O(h)  — recursion stack.

    ─────────────────────────────────────────────────────────────────
    LCA — Binary Search Tree (BST)
    ─────────────────────────────────────────────────────────────────
    In a BST, node values follow the invariant:
        left.val < node.val < right.val

    This lets us NAVIGATE to the LCA without visiting every node:
    1. Start at root.
    2. If BOTH p and q are LESS than current node    → LCA is in left subtree.
    3. If BOTH p and q are GREATER than current node → LCA is in right subtree.
    4. Otherwise (p ≤ node ≤ q, i.e., node is between p and q, or equals one)
       → current node IS the LCA.

    This reduces the search to O(h) where h = height of BST.
    For a balanced BST that is O(log n).

    KEY DIFFERENCE SUMMARY
    ─────────────────────────────────────────────────────────────────
    | Property            | Binary Tree     | BST               |
    |---------------------|-----------------|-------------------|
    | Ordering invariant  | None            | left < node < right|
    | Algorithm           | Post-order DFS  | Value comparison  |
    | Time complexity     | O(n)            | O(h) ≈ O(log n)   |
    | Extra data needed   | No              | No                |
    ─────────────────────────────────────────────────────────────────
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ═══════════════════════════════════════════════
# LCA — General Binary Tree
# ═══════════════════════════════════════════════
def lca_binary_tree(root, p, q):
    """
    Find LCA of nodes with values p and q in a general binary tree.

    Parameters
    ----------
    root : Node
    p    : int  — value of first target node
    q    : int  — value of second target node

    Returns
    -------
    Node  — LCA node, or None if not found
    """
    if root is None:
        return None

    # If current node is one of the targets, it is the LCA candidate
    if root.val == p or root.val == q:
        return root

    left_lca  = lca_binary_tree(root.left,  p, q)
    right_lca = lca_binary_tree(root.right, p, q)

    # p found on one side, q found on the other → current node is LCA
    if left_lca and right_lca:
        return root

    # Both targets are in the same subtree
    return left_lca if left_lca else right_lca


# ═══════════════════════════════════════════════
# LCA — Binary Search Tree
# ═══════════════════════════════════════════════
def lca_bst(root, p, q):
    """
    Find LCA of values p and q in a Binary Search Tree.
    Exploits BST ordering to navigate in O(h) time.
    """
    if root is None:
        return None

    # Both values smaller → LCA is in left subtree
    if p < root.val and q < root.val:
        return lca_bst(root.left, p, q)

    # Both values larger → LCA is in right subtree
    if p > root.val and q > root.val:
        return lca_bst(root.right, p, q)

    # Current node is between p and q (or equals one of them)
    return root


def lca_bst_iterative(root, p, q):
    """Iterative version of BST LCA — O(h) time, O(1) space."""
    node = root
    while node:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node
    return None


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # ── Test 1: General Binary Tree ─────────────
    #         3
    #        / \
    #       5   1
    #      / \ / \
    #     6  2 0  8
    #       / \
    #      7   4
    #
    # LCA(5, 1) = 3   (root)
    # LCA(5, 4) = 5   (5 is ancestor of 4)
    # LCA(7, 4) = 2

    print("=" * 55)
    print("GENERAL BINARY TREE LCA")
    print("=" * 55)
    print("""
         3
        / \\
       5   1
      / \\ / \\
     6  2 0  8
       / \\
      7   4
    """)

    bt = Node(3)
    bt.left              = Node(5)
    bt.right             = Node(1)
    bt.left.left         = Node(6)
    bt.left.right        = Node(2)
    bt.right.left        = Node(0)
    bt.right.right       = Node(8)
    bt.left.right.left   = Node(7)
    bt.left.right.right  = Node(4)

    tests = [(5, 1), (5, 4), (7, 4), (6, 4), (0, 8)]
    for p, q in tests:
        result = lca_binary_tree(bt, p, q)
        print(f"  LCA({p}, {q}) = {result.val if result else None}")

    # ── Test 2: BST ──────────────────────────────
    #        6
    #       / \
    #      2   8
    #     / \ / \
    #    0  4 7  9
    #      / \
    #     3   5
    #
    # LCA(2, 8) = 6
    # LCA(2, 4) = 2
    # LCA(3, 5) = 4

    print("\n" + "=" * 55)
    print("BINARY SEARCH TREE LCA")
    print("=" * 55)
    print("""
         6
        / \\
       2   8
      / \\ / \\
     0  4 7  9
       / \\
      3   5
    """)

    bst = Node(6)
    bst.left             = Node(2)
    bst.right            = Node(8)
    bst.left.left        = Node(0)
    bst.left.right       = Node(4)
    bst.right.left       = Node(7)
    bst.right.right      = Node(9)
    bst.left.right.left  = Node(3)
    bst.left.right.right = Node(5)

    bst_tests = [(2, 8), (2, 4), (3, 5), (0, 9), (7, 9)]
    for p, q in bst_tests:
        r1 = lca_bst(bst, p, q)
        r2 = lca_bst_iterative(bst, p, q)
        print(f"  LCA({p}, {q}) = {r1.val if r1 else None}  "
              f"(iterative: {r2.val if r2 else None})")
