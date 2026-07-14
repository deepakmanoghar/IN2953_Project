"""
Q7. Write a function that converts a sorted array to a height-balanced BST.

    WHY does choosing the MIDDLE element as root guarantee balance?
    -----------------------------------------------------------------------------
    A height-balanced BST requires that for every node, the heights of its left
    and right subtrees differ by at most 1.

    If we pick the middle element of a sorted sub-array as the root:
      • All elements to its LEFT  -> go into the LEFT  subtree  (smaller values [OK])
      • All elements to its RIGHT -> go into the RIGHT subtree  (larger values  [OK])
      • The left half has  floor((n-1)/2)  elements
      • The right half has ceil((n-1)/2)  elements
      • They differ by at most 1 -> subtrees are balanced at every level!

    This is equivalent to building a complete binary tree from sorted data.
    Applying the same mid-selection recursively ensures balance at EVERY node.

    TIME COMPLEXITY:  O(n)  -- each element visited exactly once
    SPACE COMPLEXITY: O(n)  for the tree nodes + O(log n) recursion stack
                            (O(n) stack for skewed inputs, but array is sorted so
                             recursion depth = O(log n))
"""


# ---------------------------------------------
# Node definition
# ---------------------------------------------
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ===============================================
# sorted_array_to_bst -- O(n) time, O(log n) stack
# ===============================================
def sorted_array_to_bst(nums):
    """
    Convert a sorted array to a height-balanced BST.

    Args:
        nums: list[int] -- sorted in ascending order

    Returns:
        Node -- root of the height-balanced BST
    """
    def helper(left, right):
        if left > right:
            return None          # empty range -> no node

        mid = (left + right) // 2          # choose middle index
        node = Node(nums[mid])             # root of this sub-BST

        node.left  = helper(left,   mid - 1)   # build left  subtree from left half
        node.right = helper(mid + 1, right)    # build right subtree from right half
        return node

    return helper(0, len(nums) - 1)


# ---------------------------------------------
# Verification helpers
# ---------------------------------------------
def inorder(node, result=None):
    """Inorder traversal should reproduce the original sorted array."""
    if result is None:
        result = []
    if node:
        inorder(node.left, result)
        result.append(node.val)
        inorder(node.right, result)
    return result


def height(node):
    """Return the height of the tree."""
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def is_balanced(node):
    """
    Check whether every node is height-balanced.
    Returns (is_balanced, height) to avoid redundant computation.
    """
    if node is None:
        return True, 0
    left_bal,  lh = is_balanced(node.left)
    right_bal, rh = is_balanced(node.right)
    balanced = left_bal and right_bal and abs(lh - rh) <= 1
    return balanced, 1 + max(lh, rh)


def print_tree(node, level=0, prefix="Root: "):
    """Sideways tree printer."""
    if node:
        print_tree(node.right, level + 1, "R--- ")
        print(" " * (level * 5) + prefix + str(node.val))
        print_tree(node.left,  level + 1, "L--- ")


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    test_cases = [
        [-10, -3, 0, 5, 9],
        [1, 2, 3, 4, 5, 6, 7],
        [1],
        [1, 2],
        list(range(1, 16)),    # 15-element array -> perfect BST of height 4
    ]

    for nums in test_cases:
        root = sorted_array_to_bst(nums)
        bal, h = is_balanced(root)
        n = len(nums)

        print("=" * 55)
        print(f"Input ({n} elements): {nums}")
        print(f"Height            : {h}  (optimal ~= ceil(log2({n+1})) = {(n).bit_length()})")
        print(f"Height-balanced   : {'[OK] YES' if bal else '[X] NO'}")
        print(f"Inorder output    : {inorder(root)}")
        print(f"Matches original  : {'[OK]' if inorder(root) == nums else '[X]'}")
        if n <= 15:
            print("\nTree (sideways, right side up):")
            print_tree(root)

    print("\n" + "=" * 55)
    print("WHY MID SELECTION GUARANTEES BALANCE:")
    print("  Sorted array: [1, 2, 3, 4, 5, 6, 7]")
    print("  mid = 3 (index) -> value 4 becomes root")
    print("  Left  half: [1,2,3]  -> 3 nodes in left subtree")
    print("  Right half: [5,6,7]  -> 3 nodes in right subtree")
    print("  Difference in size = 0 -> perfectly balanced!")
    print()
    print("  For odd-length arrays the halves differ by 1 element,")
    print("  which translates to a height difference of at most 1.")
    print("  Recursive application ensures balance at EVERY level.")
    print("=" * 55)
