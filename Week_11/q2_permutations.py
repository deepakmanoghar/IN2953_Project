"""
Q2. Generate all permutations of [1, 2, 3].
    How many permutations does a set of n elements have?
    What is the time complexity?

    PERMUTATIONS:
    -------------
    A permutation is an ORDERED arrangement of all elements.
    Unlike subsets, EVERY element must appear exactly once.

    COUNTING FORMULA:
    -----------------
    n elements -> n! (n factorial) permutations.
      n = 3 -> 3! = 3 x 2 x 1 = 6 permutations

    RECURSION TREE for [1, 2, 3]:
    -------------------------------
    At each level we pick one unused element for the next position.

                         start=[]  used={}
               /              |              \\
          pick 1           pick 2           pick 3
        [1] {1}           [2] {2}          [3] {3}
        /    \\             /    \\            /    \\
    pick2  pick3       pick1  pick3      pick1  pick2
    [1,2]  [1,3]      [2,1]  [2,3]     [3,1]  [3,2]
      |      |          |      |          |      |
   pick3  pick2      pick3  pick1      pick2  pick1
  [1,2,3][1,3,2]  [2,1,3][2,3,1]  [3,1,2][3,2,1]

    TIME  : O(n! x n)  -- n! permutations, each takes O(n) to copy
    SPACE : O(n)       -- recursion depth = n, 'used' set = O(n)
"""

import math


# =====================================================
# Approach 1 - Backtracking with a "used" boolean array
# =====================================================
def generate_permutations(nums):
    """
    At each recursive call, iterate over ALL elements and pick any
    that has not yet been 'used' on the current path.

    used[i] == True  ->  nums[i] is already in the current permutation.
    used[i] == False ->  nums[i] is still available to pick.
    """
    result = []
    used   = [False] * len(nums)

    def backtrack(current):
        # Base case: permutation is complete
        if len(current) == len(nums):
            result.append(list(current))
            return

        for i in range(len(nums)):
            if used[i]:
                continue           # skip already chosen elements

            # -- Choose ---------------------------------------------
            used[i] = True
            current.append(nums[i])

            backtrack(current)

            # -- Un-choose (backtrack) -------------------------------
            current.pop()
            used[i] = False

    backtrack([])
    return result


# =====================================================
# Approach 2 - Swap-based in-place permutation
# =====================================================
def generate_permutations_swap(nums):
    """
    Fix position 'start' by swapping each element nums[start..end]
    to that position, recurse for start+1, then swap back.

    No extra 'used' array needed; the swap itself ensures uniqueness.
    """
    result = []
    nums   = list(nums)   # work on a copy

    def backtrack(start):
        if start == len(nums):
            result.append(list(nums))
            return

        for i in range(start, len(nums)):
            # -- Choose: bring nums[i] to position 'start' ----------
            nums[start], nums[i] = nums[i], nums[start]

            backtrack(start + 1)

            # -- Un-choose: restore original order ------------------
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result


# =====================================================
# Step-by-step trace printer
# =====================================================
def trace_permutations(nums):
    """Prints a detailed step-by-step trace of the backtracking."""
    step   = [0]
    result = []
    used   = [False] * len(nums)

    print(f"\n  Tracing permutations of {nums}")
    print("  " + "-" * 50)

    def backtrack(current, depth):
        indent = "    " * depth

        if len(current) == len(nums):
            step[0] += 1
            result.append(list(current))
            print(f"  {indent}[OK]  Step {step[0]:2}: COMPLETE -> {current}")
            return

        available = [nums[i] for i in range(len(nums)) if not used[i]]
        print(f"  {indent}pos={depth}  current={current}  "
              f"available={available}")

        for i in range(len(nums)):
            if used[i]:
                continue

            print(f"  {indent}  +- choose {nums[i]}")
            used[i] = True
            current.append(nums[i])

            backtrack(current, depth + 1)

            current.pop()
            used[i] = False
            print(f"  {indent}  +- backtrack from {nums[i]}")

    backtrack([], 0)
    return result


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    nums = [1, 2, 3]

    # -- Step-by-step trace -----------------------------------------
    print("=" * 60)
    print("  Backtracking Trace  -  permutations of [1, 2, 3]")
    print("=" * 60)
    traced = trace_permutations(nums)

    # -- Approach 1: used-array backtracking ------------------------
    print("\n" + "=" * 60)
    print("  Approach 1 - Backtracking with 'used' array")
    print("=" * 60)
    perms1 = generate_permutations(nums)
    print(f"\n  Input  : {nums}")
    print(f"  Permutations ({len(perms1)} total):")
    for i, p in enumerate(perms1, 1):
        print(f"    {i}. {p}")

    # -- Approach 2: swap-based -------------------------------------
    print("\n" + "=" * 60)
    print("  Approach 2 - Swap-based In-Place")
    print("=" * 60)
    perms2 = generate_permutations_swap(nums)
    print(f"\n  Input  : {nums}")
    print(f"  Permutations ({len(perms2)} total):")
    for i, p in enumerate(perms2, 1):
        print(f"    {i}. {p}")

    # -- Factorial table --------------------------------------------
    print("\n" + "=" * 60)
    print("  Permutation Count  -  n!")
    print("=" * 60)
    print()
    for n in range(1, 8):
        print(f"    n = {n}  ->  {n}! = {math.factorial(n):5d} permutations")

    print(f"\n  For n = {len(nums)}: {len(nums)}! = "
          f"{math.factorial(len(nums))} permutations  [OK]")

    # -- Complexity analysis ----------------------------------------
    print("\n" + "=" * 60)
    print("  Complexity Analysis")
    print("=" * 60)
    print("""
    Time Complexity  : O(n! x n)
      * The recursion tree has n! leaf nodes (one per permutation).
      * At depth d, there are (n-d) branches to explore.
      * Total internal nodes: n! x (1/1! + 1/2! + … + 1/n!) ~= e x n!
      * Copying each complete permutation costs O(n).
      * Overall: O(n! x n).

    Space Complexity : O(n)
      * Recursion call stack depth = n.
      * 'used' array and 'current' list each hold at most n elements.
      * (Result list itself is O(n! x n), not counted as auxiliary space.)

    Permutation Count:
      * Position 1 has n choices.
      * Position 2 has (n-1) remaining choices.
      * …
      * Position n has 1 remaining choice.
      * Total = n x (n-1) x … x 1 = n!
    """)
