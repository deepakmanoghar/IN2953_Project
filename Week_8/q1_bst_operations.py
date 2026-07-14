"""
Q1. Implement a BST with insert, search, delete, and inorder traversal.
    The delete operation should handle all three cases:
      Case 1 - Leaf node (no children)
      Case 2 - One child (left or right)
      Case 3 - Two children (replace with inorder successor)
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
# BST Class
# ---------------------------------------------
class BST:
    def __init__(self):
        self.root = None

    # ===============================================
    # INSERT
    # ===============================================
    def insert(self, val):
        """Insert a value into the BST."""
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        # Base case: empty spot found, create node here
        if node is None:
            return Node(val)
        if val < node.val:
            node.left = self._insert(node.left, val)   # go left
        elif val > node.val:
            node.right = self._insert(node.right, val) # go right
        # val == node.val -> duplicate; ignore
        return node

    # ===============================================
    # SEARCH
    # ===============================================
    def search(self, val):
        """Return True if val exists in the BST, else False."""
        return self._search(self.root, val)

    def _search(self, node, val):
        if node is None:
            return False           # reached a dead-end -> not found
        if val == node.val:
            return True            # found!
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    # ===============================================
    # DELETE
    # Three cases handled:
    #   Case 1 -> node is a leaf               -> simply remove it
    #   Case 2 -> node has exactly one child   -> bypass node, link child up
    #   Case 3 -> node has two children        -> replace val with inorder
    #                                            successor (smallest in right
    #                                            subtree), then delete successor
    # ===============================================
    def delete(self, val):
        """Delete val from the BST (if it exists)."""
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if node is None:
            return None            # val not found; nothing to do

        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # -- node to delete found ------------------
            # Case 1: Leaf (no children)
            if node.left is None and node.right is None:
                return None

            # Case 2a: Only right child exists
            if node.left is None:
                return node.right

            # Case 2b: Only left child exists
            if node.right is None:
                return node.left

            # Case 3: Two children
            #   Find inorder successor = leftmost node in right subtree
            successor = self._min_node(node.right)
            node.val = successor.val          # overwrite current with successor
            node.right = self._delete(node.right, successor.val)  # delete successor

        return node

    def _min_node(self, node):
        """Return the node with the smallest value in a subtree."""
        while node.left:
            node = node.left
        return node

    # ===============================================
    # INORDER TRAVERSAL  (Left -> Root -> Right)
    # Produces sorted output for a valid BST
    # ===============================================
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    # ---------------------------------------------
    # Helper: pretty-print the tree
    # ---------------------------------------------
    def print_tree(self, node="_root_", level=0, prefix="Root: "):
        """Simple sideways tree printer (right at top, left at bottom)."""
        if node == "_root_":
            node = self.root          # resolve default only once
        if node is not None:
            self.print_tree(node.right, level + 1, "R--- ")
            print(" " * (level * 5) + prefix + str(node.val))
            self.print_tree(node.left,  level + 1, "L--- ")


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    bst = BST()

    # Build tree by inserting values
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for v in values:
        bst.insert(v)

    print("=" * 55)
    print("BST after inserting:", values)
    print("=" * 55)
    bst.print_tree()

    print("\nInorder (should be sorted):", bst.inorder())

    # -- Search -----------------------------------
    print("\n--- SEARCH ---")
    for target in [40, 55, 10, 100]:
        found = bst.search(target)
        print(f"  search({target}) -> {'Found [OK]' if found else 'Not Found [--]'}")

    # -- Delete Case 1: Leaf (10) ------------------
    print("\n--- DELETE Case 1: Leaf node (10) ---")
    bst.delete(10)
    print("Inorder after deleting 10:", bst.inorder())

    # -- Delete Case 2: One child (20 has only right child 25) --
    print("\n--- DELETE Case 2: One-child node (20) ---")
    bst.delete(20)
    print("Inorder after deleting 20:", bst.inorder())

    # -- Delete Case 3: Two children (30 has 25 and 40) --
    print("\n--- DELETE Case 3: Two-children node (30) ---")
    print("  Inorder successor of 30 is 35 -> 35 replaces 30")
    bst.delete(30)
    print("Inorder after deleting 30:", bst.inorder())

    # Final tree
    print("\nFinal tree structure:")
    bst.print_tree()
