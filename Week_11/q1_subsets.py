"""
Q1. Generate all subsets of [1, 2, 3].
    Draw the complete recursion tree showing each choice point.
    How many subsets does a set of n elements have?

    SUBSETS (Power Set):
    --------------------
    For each element in the set, we have exactly TWO choices:
      1. INCLUDE the element in the current subset.
      2. EXCLUDE the element from the current subset.

    This binary choice at each level creates a BINARY RECURSION TREE.

    KEY INSIGHT:
    ------------
    A set of n elements has exactly 2^n subsets.
    Each element is either IN or OUT -> 2 choices x n elements = 2^n.

    RECURSION TREE for [1, 2, 3]:
    ------------------------------
                        []
                  /           \\
              [](excl 1)    [1](incl 1)
              /    \\           /    \\
          [](e2) [2](i2)   [1](e2) [1,2](i2)
          / \\    / \\        / \\      / \\
        [] [3] [2] [2,3] [1] [1,3] [1,2] [1,2,3]
        ^   ^   ^    ^    ^    ^     ^      ^
       (8 leaf nodes = 2^3 subsets)

    TIME  : O(2^n x n)  -- 2^n subsets, each up to n elements to copy
    SPACE : O(n)        -- recursion depth is n (height of tree)
"""


# =====================================================
# Approach 1 - Classic backtracking (include / exclude)
# =====================================================
def generate_subsets(nums):
    """
    Explores two branches at every index:
      * Include nums[index] -> recurse with index + 1
      * Exclude nums[index] -> recurse with index + 1

    Returns a list of all 2^n subsets.
    """
    result = []

    def backtrack(index, current):
        # Base case: processed all elements -> record the subset
        if index == len(nums):
            result.append(list(current))   # snapshot of current path
            return

        # -- Branch 1: INCLUDE nums[index] --------------------------
        current.append(nums[index])
        backtrack(index + 1, current)

        # -- Branch 2: EXCLUDE nums[index] --------------------------
        current.pop()                      # undo inclusion (backtrack)
        backtrack(index + 1, current)

    backtrack(0, [])
    return result


# =====================================================
# Approach 2 - Iterative (build up subset list)
# =====================================================
def generate_subsets_iterative(nums):
    """
    Start with [[]] and for every new element, duplicate every
    existing subset and append the new element to each duplicate.

    Example trace:
      Start  : [[]]
      Add 1  : [[], [1]]
      Add 2  : [[], [1], [2], [1,2]]
      Add 3  : [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
    """
    result = [[]]
    for num in nums:
        new_subsets = [existing + [num] for existing in result]
        result.extend(new_subsets)
    return result


# =====================================================
# Recursion tree printer (visual aid)
# =====================================================
def print_recursion_tree(nums):
    """Prints a text-based recursion tree, showing each choice point."""
    print("\n" + "=" * 60)
    print("  RECURSION TREE  -  generate_subsets([1, 2, 3])")
    print("=" * 60)

    def recurse(index, current, depth, branch_label):
        indent  = "    " * depth
        connector = "+-- " if branch_label == "INCL" else "+-- "
        label   = f"[{', '.join(map(str, current))}]"
        choice  = f"(include {nums[index - 1]})" if depth > 0 else ""

        if depth == 0:
            print(f"\n  {label}  <- root (empty subset, no choice yet)")
        else:
            tag = "INCLUDE" if branch_label == "INCL" else "EXCLUDE"
            print(f"  {indent}{connector}{label}  <- {tag} {nums[index - 1]}")

        if index == len(nums):
            result_indent = "    " * (depth + 1)
            print(f"  {result_indent}[OK] LEAF -> record {label}")
            return

        # Include branch (left / first child)
        current.append(nums[index])
        recurse(index + 1, current, depth + 1, "INCL")
        current.pop()

        # Exclude branch (right / second child)
        recurse(index + 1, current, depth + 1, "EXCL")

    recurse(0, [], 0, "")
    print()


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    nums = [1, 2, 3]

    # -- Visual recursion tree --------------------------------------
    print_recursion_tree(nums)

    # -- Backtracking approach --------------------------------------
    print("=" * 60)
    print("  Approach 1 - Backtracking (include / exclude)")
    print("=" * 60)
    subsets_bt = generate_subsets(nums)
    print(f"\n  Input  : {nums}")
    print(f"  Subsets ({len(subsets_bt)} total):")
    for i, s in enumerate(subsets_bt, 1):
        print(f"    {i:2}. {s}")

    # -- Iterative approach -----------------------------------------
    print("\n" + "=" * 60)
    print("  Approach 2 - Iterative Build-Up")
    print("=" * 60)
    subsets_it = generate_subsets_iterative(nums)
    print(f"\n  Input  : {nums}")
    print(f"  Subsets ({len(subsets_it)} total):")
    for i, s in enumerate(subsets_it, 1):
        print(f"    {i:2}. {s}")

    # -- Formula demonstration --------------------------------------
    print("\n" + "=" * 60)
    print("  Power Set Size  -  2^n")
    print("=" * 60)
    print()
    for n in range(1, 6):
        print(f"    n = {n}  ->  2^{n} = {2**n:3d} subsets")

    print(f"\n  For n = {len(nums)}: 2^{len(nums)} = {2**len(nums)} subsets  [OK]")

    # -- Complexity summary -----------------------------------------
    print("\n" + "=" * 60)
    print("  Complexity Summary")
    print("=" * 60)
    print("""
    Time  Complexity : O(2^n x n)
      * 2^n leaf nodes in the recursion tree (one per subset).
      * Copying each subset into the result takes O(n) time.

    Space Complexity : O(n)
      * Recursion call stack depth = n (one level per element).
      * The 'current' list holds at most n elements at any time.
      * (Result storage itself is O(2^n x n), not counted as aux space.)

    Number of Subsets:
      * Every element is independently IN or OUT.
      * 2 choices per element, n elements  ->  2 x 2 x … x 2 = 2^n.
      * This is called the POWER SET of the original set.
    """)
