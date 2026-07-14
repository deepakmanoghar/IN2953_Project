"""
Q7. Write a function that constructs a binary tree from preorder and
    inorder traversal arrays. Explain your approach step by step.

    ─────────────────────────────────────────────────────────────────
    APPROACH (Step-by-Step Explanation)
    ─────────────────────────────────────────────────────────────────

    Given:
        preorder = [3, 9, 20, 15, 7]
        inorder  = [9, 3, 15, 20, 7]

    STEP 1 — Root identification
        The FIRST element of preorder is always the root of the current
        subtree.  → root = 3

    STEP 2 — Split inorder around root
        Find '3' in inorder: index = 1.
        • Elements LEFT  of index in inorder → left subtree nodes:  [9]
        • Elements RIGHT of index in inorder → right subtree nodes: [15, 20, 7]

    STEP 3 — Split preorder accordingly
        • Left subtree has len([9]) = 1 node.
        • Next 1 element in preorder (after root) → left preorder:  [9]
        • Remaining elements → right preorder: [20, 15, 7]

    STEP 4 — Recurse
        build(preorder=[9],        inorder=[9])        → Node(9)
        build(preorder=[20,15,7],  inorder=[15,20,7])  → subtree rooted at 20

    STEP 5 — Base cases
        • Empty preorder/inorder → return None (no node)
        • Single element         → return leaf Node

    WHY IT WORKS
        Preorder guarantees the first element is the root.
        Inorder guarantees all elements to the left of the root come from
        the left subtree and all to the right from the right subtree.
        Together they uniquely reconstruct any binary tree.

    OPTIMISATION
        Instead of slicing arrays (O(n) per call), use an index map for
        O(1) lookup of root position in inorder. This brings overall
        complexity from O(n²) to O(n).

    Time:  O(n)   Space: O(n)  (index map + recursion stack)
    ─────────────────────────────────────────────────────────────────
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────
# Optimised construction using index map
# ─────────────────────────────────────────────
def build_tree(preorder, inorder):
    """
    Reconstruct a binary tree from its preorder and inorder traversals.

    Parameters
    ----------
    preorder : list[int]
    inorder  : list[int]

    Returns
    -------
    Node  — root of the reconstructed tree
    """
    # Map each value to its index in inorder for O(1) lookup
    inorder_index = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = [0]   # mutable container so inner function can advance it

    def helper(left, right):
        """Build subtree using inorder range [left, right]."""
        if left > right:
            return None

        # Root is next in preorder
        root_val = preorder[pre_idx[0]]
        pre_idx[0] += 1
        root = Node(root_val)

        # Find root in inorder
        mid = inorder_index[root_val]

        # IMPORTANT: build LEFT subtree BEFORE right (matches preorder)
        root.left  = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root

    return helper(0, len(inorder) - 1)


# ─────────────────────────────────────────────
# Simple (slice-based) version for clarity
# ─────────────────────────────────────────────
def build_tree_simple(preorder, inorder):
    """Easier to read but O(n²) due to list slicing."""
    if not preorder or not inorder:
        return None

    root_val = preorder[0]
    root = Node(root_val)
    mid = inorder.index(root_val)

    root.left  = build_tree_simple(preorder[1 : 1 + mid], inorder[:mid])
    root.right = build_tree_simple(preorder[1 + mid :],   inorder[mid + 1:])
    return root


# ─────────────────────────────────────────────
# Pretty printer & verifier
# ─────────────────────────────────────────────
def inorder_traverse(node, result=None):
    if result is None:
        result = []
    if node:
        inorder_traverse(node.left, result)
        result.append(node.val)
        inorder_traverse(node.right, result)
    return result


def preorder_traverse(node, result=None):
    if result is None:
        result = []
    if node:
        result.append(node.val)
        preorder_traverse(node.left, result)
        preorder_traverse(node.right, result)
    return result


def print_tree(node, prefix="", is_left=True):
    if node is None:
        return
    print_tree(node.right, prefix + ("|   " if is_left else "    "), False)
    print(prefix + ("+-- " if is_left else "+-- ") + str(node.val))
    print_tree(node.left,  prefix + ("    " if is_left else "|   "), True)


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    preorder = [3, 9, 20, 15, 7]
    inorder  = [9, 3, 15, 20, 7]

    print("Input:")
    print(f"  Preorder : {preorder}")
    print(f"  Inorder  : {inorder}")

    print("\nStep-by-step reconstruction:")
    print("  1. Root = preorder[0] = 3")
    print("  2. '3' is at index 1 in inorder")
    print("     Left  inorder  = [9]        (1 node)")
    print("     Right inorder  = [15, 20, 7] (3 nodes)")
    print("  3. Left  preorder = [9]")
    print("     Right preorder = [20, 15, 7]")
    print("  4. Recurse -> build subtrees")
    print("  5. Result tree:")
    print("          3")
    print("         / \\")
    print("        9  20")
    print("           / \\")
    print("          15  7")

    root = build_tree(preorder, inorder)

    print("\nReconstructed tree (sideways):")
    print_tree(root)

    print("\nVerification (should match inputs):")
    print(f"  Preorder  check: {preorder_traverse(root)}  OK" if preorder_traverse(root) == preorder else "  FAIL: Preorder mismatch!")
    print(f"  Inorder   check: {inorder_traverse(root)}  OK" if inorder_traverse(root) == inorder else "  FAIL: Inorder mismatch!")

    # Additional test
    print("\n--- Additional test ---")
    pre2 = [1, 2, 4, 5, 3, 6, 7]
    in2  = [4, 2, 5, 1, 6, 3, 7]
    root2 = build_tree(pre2, in2)
    print(f"Preorder  in : {pre2}")
    print(f"Preorder out : {preorder_traverse(root2)}")
    print(f"Inorder   in : {in2}")
    print(f"Inorder  out : {inorder_traverse(root2)}")
