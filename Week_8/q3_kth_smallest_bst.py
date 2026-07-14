"""
Q3. Find the kth smallest element in a BST without converting to an array first.

    KEY INSIGHT:
    -----------------------------------------------------------------------------
    Inorder traversal of a BST visits nodes in ASCENDING order.
    Instead of collecting all values into a list, we count visits and stop
    as soon as we reach the kth visit.

    TIME COMPLEXITY:
    -----------------------------------------------------------------------------
    • Best case  : O(k)  -- we stop after visiting exactly k nodes.
    • Worst case : O(h + k) where h = height of the tree.
      For a balanced BST: h = O(log n), so worst case is O(log n + k).
      For a skewed BST:   h = O(n),     so worst case is O(n).
    • Space      : O(h) for the implicit call stack (recursion depth = height).

    Compared to converting to array first:
      Array approach -> O(n) time, O(n) extra space.
      This approach  -> O(h + k) time, O(h) extra space -- more efficient!
"""


# ---------------------------------------------
# Node definition
# ---------------------------------------------
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ---------------------------------------------
# BST insert helper
# ---------------------------------------------
def insert(root, val):
    if root is None:
        return Node(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def build_bst(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


# ===============================================
# APPROACH 1 - Recursive with early stopping
# ===============================================
def kth_smallest_recursive(root, k):
    """
    Uses a mutable list [count, result] to share state across recursive calls.
    Stops traversal as soon as the kth node is found.
    """
    state = [0, None]   # [visits_so_far, answer]

    def inorder(node):
        if node is None or state[1] is not None:
            return             # base case or already found answer
        inorder(node.left)
        state[0] += 1          # count this visit
        if state[0] == k:
            state[1] = node.val
            return
        inorder(node.right)

    inorder(root)
    return state[1]


# ===============================================
# APPROACH 2 - Iterative (explicit stack)
# ===============================================
def kth_smallest_iterative(root, k):
    """
    Simulates inorder traversal iteratively.
    Stops and returns the moment we have visited k nodes.
    Avoids any recursion overhead.
    """
    stack = []
    current = root
    count = 0

    while current or stack:
        # Dive as far left as possible
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()
        count += 1                   # visit this node
        if count == k:
            return current.val       # <- early exit: kth node found!
        current = current.right      # move to right subtree

    return None   # k is out of range


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    root = build_bst(values)

    #         50
    #        /  \
    #       30   70
    #      / \   / \
    #    20  40 60  80
    #   / \  / \
    #  10 25 35 45

    # Inorder (sorted): [10, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80]
    sorted_vals = [10, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80]

    print("=" * 55)
    print("BST values inserted:", sorted(values))
    print("Inorder (sorted)   :", sorted_vals)
    print("=" * 55)

    test_cases = [1, 3, 5, 7, 11]
    for k in test_cases:
        r = kth_smallest_recursive(root, k)
        i = kth_smallest_iterative(root, k)
        expected = sorted_vals[k - 1]
        print(f"\n  k={k}:")
        print(f"    Recursive  -> {r}  (expected {expected})")
        print(f"    Iterative  -> {i}  (expected {expected})")
        print(f"    Match: {'[OK]' if r == i == expected else '[X]'}")

    print("\n" + "=" * 55)
    print("TIME COMPLEXITY SUMMARY:")
    print("  • This approach : O(h + k) time, O(h) space")
    print("    h = tree height (O(log n) balanced, O(n) skewed)")
    print("  • Array approach: O(n) time,     O(n) space")
    print("  -> Early-stopping inorder is more efficient for small k!")
    print("=" * 55)
