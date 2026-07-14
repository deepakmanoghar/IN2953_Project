"""
Q2. Write a function to validate whether a binary tree is a valid BST.

    WHY is checking  node.left.val < node.val < node.right.val  alone INSUFFICIENT?
    ---------------------------------------------------------------------------------
    That check only compares a node with its immediate children.
    It does NOT enforce the global BST property:
      "Every node in the LEFT subtree must be LESS than the current node,
       and every node in the RIGHT subtree must be GREATER."

    Counter-example:
             10
            /  \\
           5    15
          / \\
         3   12   <- 12 > 10 (root), so this violates BST -- but the local
                      check (5 < 12) passes!

    CORRECT APPROACH: pass a valid [min, max] range down the tree.
    As we go RIGHT we raise the lower bound; as we go LEFT we lower the upper bound.
"""

import math


# ---------------------------------------------
# Node definition
# ---------------------------------------------
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ===============================================
# WRONG approach - only checks immediate children
# ===============================================
def is_bst_wrong(node):
    """
    Naive check: only verifies each node against its direct children.
    FAILS for the counter-example below.
    """
    if node is None:
        return True
    if node.left and node.left.val >= node.val:
        return False
    if node.right and node.right.val <= node.val:
        return False
    return is_bst_wrong(node.left) and is_bst_wrong(node.right)


# ===============================================
# CORRECT approach - min/max bound propagation
# ===============================================
def is_valid_bst(root):
    """
    Validates the full BST property by threading allowed [min, max] bounds
    through every recursive call.
    Time:  O(n)  -- each node visited once
    Space: O(h)  -- call stack depth = tree height h
    """
    def validate(node, min_val, max_val):
        if node is None:
            return True                          # empty subtree is valid
        if not (min_val < node.val < max_val):  # violates allowed range
            return False
        # Going LEFT  -> current node is new upper bound
        # Going RIGHT -> current node is new lower bound
        return (validate(node.left,  min_val,   node.val) and
                validate(node.right, node.val,  max_val))

    return validate(root, -math.inf, math.inf)


# ---------------------------------------------
# Helper builders
# ---------------------------------------------
def build_valid_bst():
    """
        10
       /  \\
      5    15
     / \\     \\
    3   7     20
    """
    root = Node(10)
    root.left         = Node(5)
    root.right        = Node(15)
    root.left.left    = Node(3)
    root.left.right   = Node(7)
    root.right.right  = Node(20)
    return root


def build_invalid_bst_local_ok():
    """
    Looks locally fine but violates global BST property.
         10
        /  \\
       5    15
      / \\
     3   12    <- 12 is in left subtree of 10, but 12 > 10 -> INVALID
    """
    root = Node(10)
    root.left        = Node(5)
    root.right       = Node(15)
    root.left.left   = Node(3)
    root.left.right  = Node(12)   # the problematic node
    return root


def build_invalid_bst_obvious():
    """
        5
       / \\
      1   4   <- 4 < 5 but on the right -> INVALID
         / \\
        3   6
    """
    root = Node(5)
    root.left       = Node(1)
    root.right      = Node(4)
    root.right.left = Node(3)
    root.right.right = Node(6)
    return root


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("BST Validation Demo")
    print("=" * 60)

    # -- Test 1: Valid BST ------------------------
    t1 = build_valid_bst()
    print("\nTree 1 (valid BST):  10 / [5,15] / [3,7,_,20]")
    print(f"  Wrong check  -> {is_bst_wrong(t1)}")
    print(f"  Correct check -> {is_valid_bst(t1)}")
    print("  Expected: True / True")

    # -- Test 2: Locally-OK but globally INVALID --
    t2 = build_invalid_bst_local_ok()
    print("\nTree 2 (12 in left subtree of 10 -- locally OK, globally WRONG):")
    print("       10")
    print("      /  \\")
    print("     5    15")
    print("    / \\")
    print("   3   12   <- 12 > 10 violates BST")
    print(f"  Wrong check  -> {is_bst_wrong(t2)}   <- BUG: says True!")
    print(f"  Correct check -> {is_valid_bst(t2)}  <- Correctly says False")
    print("  Expected: False (wrong check fails here -- demonstrates the bug)")

    # -- Test 3: Obvious invalid BST -------------
    t3 = build_invalid_bst_obvious()
    print("\nTree 3 (5 with right child 4 -- obviously invalid):")
    print(f"  Wrong check  -> {is_bst_wrong(t3)}")
    print(f"  Correct check -> {is_valid_bst(t3)}")
    print("  Expected: False / False")

    # -- Explanation summary ----------------------
    print("\n" + "=" * 60)
    print("WHY local check is insufficient:")
    print("  node.left.val < node.val < node.right.val")
    print("  -> only checks ONE level deep.")
    print("  -> a value deep in the left subtree can still be > root.")
    print("  The correct fix: propagate a (min_bound, max_bound) range")
    print("  and verify  min_bound < node.val < max_bound  at every node.")
    print("=" * 60)
