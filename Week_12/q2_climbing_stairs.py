"""
Q2. Climbing Stairs: You can climb 1 or 2 steps.
    How many distinct ways to reach step n? Solve for n=10.
    Then extend to allow 1, 2, or 3 steps.

    INSIGHT:
    --------
    To reach step n, you must have come from step (n-1) or step (n-2).
    So:  ways(n) = ways(n-1) + ways(n-2)

    This is exactly the Fibonacci recurrence!

    BASE CASES:
    -----------
    ways(0) = 1   (one way to stand at ground: do nothing)
    ways(1) = 1   (only one step: climb 1)
    ways(2) = 2   (climb 1+1, or climb 2)

    TRACE for n=5 (1 or 2 steps):
    ------------------------------
    n   ways(n)   how to get here
    0   1         base
    1   1         [1]
    2   2         [1,1], [2]
    3   3         [1,1,1], [1,2], [2,1]
    4   5         [1,1,1,1],[1,1,2],[1,2,1],[2,1,1],[2,2]
    5   8         ... (ways(4)+ways(3) = 5+3)

    EXTENSION -- 1, 2, or 3 steps:
    --------------------------------
    ways(n) = ways(n-1) + ways(n-2) + ways(n-3)
    Base: ways(0)=1, ways(1)=1, ways(2)=2, ways(3)=4

    TIME  : O(n)   SPACE: O(n) for table, O(1) with rolling variables
"""


# =====================================================
# Version A -- 1 or 2 steps, tabulation
# =====================================================
def climb_stairs_2(n):
    """
    dp[i] = number of distinct ways to reach step i.
    Recurrence: dp[i] = dp[i-1] + dp[i-2]
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    dp    = [0] * (n + 1)
    dp[0] = 1    # standing at ground
    dp[1] = 1    # only one way to reach step 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def climb_stairs_2_optimised(n):
    """O(1) space: rolling two variables."""
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        curr  = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1


# =====================================================
# Version B -- 1, 2, or 3 steps
# =====================================================
def climb_stairs_3(n):
    """
    dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
    Base: dp[0]=1, dp[1]=1, dp[2]=2
    """
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2
    dp    = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
    return dp[n]


# =====================================================
# General version -- any allowed step sizes
# =====================================================
def climb_stairs_general(n, steps):
    """
    Generalised: 'steps' is a list of allowed step sizes.
    dp[i] = sum of dp[i-k] for each k in steps (if i-k >= 0)
    """
    dp    = [0] * (n + 1)
    dp[0] = 1                   # base: one way to be at ground
    for i in range(1, n + 1):
        for k in steps:
            if i - k >= 0:
                dp[i] += dp[i - k]
    return dp[n]


# =====================================================
# List all distinct paths (backtracking) for small n
# =====================================================
def list_paths(n, steps):
    """Returns all distinct ways to climb n stairs using allowed steps."""
    result = []
    def bt(remaining, path):
        if remaining == 0:
            result.append(list(path))
            return
        for k in steps:
            if remaining - k >= 0:
                path.append(k)
                bt(remaining - k, path)
                path.pop()
    bt(n, [])
    return result


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":

    # -- DP table for n=10, 1-or-2 steps ---------------------------
    print("=" * 60)
    print("  Climbing Stairs (1 or 2 steps) -- DP Table  n=10")
    print("=" * 60)
    n = 10
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    print(f"\n  {'Step i':>8}   {'dp[i]':>8}   {'Recurrence':}")
    print("  " + "-" * 48)
    print(f"  {0:>8}   {dp[0]:>8}   base case (ground)")
    print(f"  {1:>8}   {dp[1]:>8}   base case")
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        print(f"  {i:>8}   {dp[i]:>8}   dp[{i-1}]({dp[i-1]}) + dp[{i-2}]({dp[i-2]})")

    print(f"\n  Answer for n=10: {climb_stairs_2(10)} distinct ways")

    # -- List all paths for n=5 (small enough to enumerate) ---------
    print("\n" + "=" * 60)
    print("  All Paths to Step 5  (1 or 2 steps)")
    print("=" * 60)
    paths = list_paths(5, [1, 2])
    for i, p in enumerate(paths, 1):
        print(f"  {i:>2}. {p}  (sum={sum(p)})")
    print(f"\n  Total: {len(paths)} paths")

    # -- Extension: 1, 2, or 3 steps --------------------------------
    print("\n" + "=" * 60)
    print("  Extension: 1, 2, or 3 Steps -- DP Table  n=10")
    print("=" * 60)
    n = 10
    dp3 = [0] * (n + 1)
    dp3[0] = 1; dp3[1] = 1; dp3[2] = 2
    print(f"\n  {'Step i':>8}   {'dp[i]':>8}   {'Recurrence':}")
    print("  " + "-" * 56)
    print(f"  {0:>8}   {dp3[0]:>8}   base case")
    print(f"  {1:>8}   {dp3[1]:>8}   base case")
    print(f"  {2:>8}   {dp3[2]:>8}   base case")
    for i in range(3, n + 1):
        dp3[i] = dp3[i-1] + dp3[i-2] + dp3[i-3]
        print(f"  {i:>8}   {dp3[i]:>8}   "
              f"dp[{i-1}]({dp3[i-1]}) + dp[{i-2}]({dp3[i-2]}) + "
              f"dp[{i-3}]({dp3[i-3]})")

    print(f"\n  Answer for n=10 (1/2/3 steps): {climb_stairs_3(10)} ways")

    # -- Comparison table: 1-2 vs 1-2-3 steps ----------------------
    print("\n" + "=" * 60)
    print("  Comparison: Ways to Reach Each Step")
    print("=" * 60)
    print(f"\n  {'n':>4}   {'1-2 steps':>12}   {'1-2-3 steps':>14}")
    print("  " + "-" * 35)
    for n in range(1, 11):
        w2 = climb_stairs_2(n)
        w3 = climb_stairs_3(n)
        print(f"  {n:>4}   {w2:>12}   {w3:>14}")

    # -- General version demo ---------------------------------------
    print("\n" + "=" * 60)
    print("  General Version  --  Steps {1,3,5}  for n=10")
    print("=" * 60)
    result = climb_stairs_general(10, [1, 3, 5])
    print(f"\n  Ways to reach step 10 using steps {{1,3,5}}: {result}")

    # -- Complexity summary -----------------------------------------
    print("\n" + "=" * 60)
    print("  Complexity Summary")
    print("=" * 60)
    print("""
    1-or-2 steps:
      Time  : O(n)    -- one pass through dp[2..n]
      Space : O(n)    -- dp array of size n+1
              O(1)    -- with rolling variables (prev2, prev1)

    1, 2, or 3 steps:
      Time  : O(n)    -- same single pass
      Space : O(n) or O(1) rolling three variables

    General k allowed steps:
      Time  : O(n * k)  -- for each of n positions, try k step sizes
      Space : O(n)

    Why is this DP?
      OPTIMAL SUBSTRUCTURE: ways(n) depends only on smaller sub-problems.
      OVERLAPPING SUBPROBLEMS: ways(n-1) and ways(n-2) both need ways(n-2).
    """)
