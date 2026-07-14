"""
Q6. Implement level order traversal that returns values in zigzag order
    (left-to-right, then right-to-left, alternating).

    Example output: [[3], [20, 9], [15, 7]]

    Tree used:
            3
           / \
          9  20
            /  \
           15   7

    Level 0 (root)  → left-to-right  → [3]
    Level 1         → right-to-left  → [20, 9]
    Level 2         → left-to-right  → [15, 7]
"""

from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────
# Zigzag Level-Order Traversal
# ─────────────────────────────────────────────
def zigzag_level_order(root):
    """
    Algorithm:
      1. Use a queue for standard BFS.
      2. Track a boolean 'left_to_right' that toggles each level.
      3. Collect all nodes at each level into a list.
      4. If 'left_to_right' is False, reverse that list before appending.
      5. Toggle the flag after each level.

    Time:  O(n)  – every node processed exactly once.
    Space: O(w)  – w is the maximum width of the tree (queue size).
    """
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

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

        # Reverse for right-to-left levels
        if not left_to_right:
            level.reverse()

        result.append(level)
        left_to_right = not left_to_right   # toggle direction

    return result


# ─────────────────────────────────────────────
# Alternative: using deque for each level
# (avoids list reversal — slightly more efficient)
# ─────────────────────────────────────────────
def zigzag_level_order_deque(root):
    """
    Instead of reversing, we use a deque per level and append from
    the correct end based on direction.
    """
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level_size = len(queue)
        level = deque()

        for _ in range(level_size):
            node = queue.popleft()
            if left_to_right:
                level.append(node.val)       # add to right end
            else:
                level.appendleft(node.val)   # add to left end (reverses order)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(list(level))
        left_to_right = not left_to_right

    return result


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    #       3
    #      / \
    #     9  20
    #       /  \
    #      15   7

    root = Node(3)
    root.left        = Node(9)
    root.right       = Node(20)
    root.right.left  = Node(15)
    root.right.right = Node(7)

    print("Tree:")
    print("        3")
    print("       / \\")
    print("      9  20")
    print("        /  \\")
    print("       15   7")
    print()

    result1 = zigzag_level_order(root)
    print("Zigzag (list-reverse method) :", result1)
    # Expected: [[3], [20, 9], [15, 7]]

    result2 = zigzag_level_order_deque(root)
    print("Zigzag (deque method)        :", result2)
    # Expected: [[3], [20, 9], [15, 7]]

    print()
    print("Level-by-level breakdown:")
    for i, level in enumerate(result1):
        direction = "L->R" if i % 2 == 0 else "R->L"
        print(f"  Level {i} ({direction}): {level}")

    # Test with a deeper tree
    print("\n--- Deeper tree test ---")
    #           1
    #          / \
    #         2   3
    #        / \ / \
    #       4  5 6  7
    deep = Node(1)
    deep.left        = Node(2)
    deep.right       = Node(3)
    deep.left.left   = Node(4)
    deep.left.right  = Node(5)
    deep.right.left  = Node(6)
    deep.right.right = Node(7)

    result3 = zigzag_level_order(deep)
    print("Zigzag:", result3)
    # Expected: [[1], [3, 2], [4, 5, 6, 7]]
