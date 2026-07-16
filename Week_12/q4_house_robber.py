"""
Q4. House Robber: Given houses=[2,7,9,3,1],
    find the maximum money you can rob (no adjacent houses).
    Write both memoized and tabulated solutions.

    HOUSE ROBBER:
    -------------
    You cannot rob two ADJACENT houses (alarm will trigger).
    Maximise the total money robbed.

    RECURRENCE:
    -----------
    For each house i, you have TWO choices:
      1. ROB house i:     gain = houses[i] + rob(i-2)
                          (skip the previous house)
      2. SKIP house i:    gain = rob(i-1)
                          (take whatever was best up to i-1)

    dp[i] = max(houses[i] + dp[i-2],  dp[i-1])

    BASE CASES:
    -----------
    dp[0] = houses[0]                  (only one house)
    dp[1] = max(houses[0], houses[1])  (pick the bigger of first two)

    TRACE for houses=[2,7,9,3,1]:
    ------------------------------
    i=0: dp[0] = 2          (rob house 0: value 2)
    i=1: dp[1] = max(2,7)=7 (rob house 1: value 7 > 2)
    i=2: dp[2] = max(9+dp[0], dp[1]) = max(9+2, 7) = max(11,7) = 11
    i=3: dp[3] = max(3+dp[1], dp[2]) = max(3+7, 11) = max(10,11) = 11
    i=4: dp[4] = max(1+dp[2], dp[3]) = max(1+11, 11) = max(12,11) = 12

    Answer: 12 (rob houses at index 0, 2, 4: values 2+9+1=12)

    TIME  : O(n)    SPACE: O(n) tabulation, O(1) optimised
"""

from functools import lru_cache


# =====================================================
# Approach 1 -- Memoization (top-down)
# =====================================================
def house_robber_memo(houses):
    """
    Top-down DP with memoization.
    rob(i) = maximum money robbing from house 0 to house i.
    """
    if not houses:
        return 0

    n     = len(houses)
    cache = {}

    def rob(i):
        if i < 0:
            return 0
        if i == 0:
            return houses[0]
        if i in cache:
            return cache[i]

        # Either rob house i (skip i-1) or skip house i (keep i-1 best)
        cache[i] = max(houses[i] + rob(i - 2),   # rob i
                       rob(i - 1))               # skip i
        return cache[i]

    return rob(n - 1)


# =====================================================
# Approach 2 -- Tabulation (bottom-up)
# =====================================================
def house_robber_tabulation(houses):
    """
    Bottom-up DP: fill dp array from index 0 to n-1.
    dp[i] = max money we can rob from houses[0..i].
    """
    if not houses:
        return 0
    n = len(houses)
    if n == 1:
        return houses[0]

    dp    = [0] * n
    dp[0] = houses[0]
    dp[1] = max(houses[0], houses[1])

    for i in range(2, n):
        dp[i] = max(houses[i] + dp[i - 2],
                    dp[i - 1])
    return dp[n - 1]


# =====================================================
# Approach 3 -- Space-optimised (O(1) space)
# =====================================================
def house_robber_optimised(houses):
    """
    Only need the last two dp values.
    prev2 = dp[i-2], prev1 = dp[i-1]
    """
    if not houses:
        return 0
    n = len(houses)
    if n == 1:
        return houses[0]

    prev2 = houses[0]
    prev1 = max(houses[0], houses[1])

    for i in range(2, n):
        curr  = max(houses[i] + prev2, prev1)
        prev2, prev1 = prev1, curr

    return prev1


# =====================================================
# Reconstruction: which houses were robbed?
# =====================================================
def house_robber_with_path(houses):
    """Returns (max_money, list_of_robbed_indices)."""
    if not houses:
        return 0, []
    n = len(houses)
    if n == 1:
        return houses[0], [0]

    dp    = [0] * n
    dp[0] = houses[0]
    dp[1] = max(houses[0], houses[1])

    for i in range(2, n):
        dp[i] = max(houses[i] + dp[i - 2], dp[i - 1])

    # Backtrack to find which houses were robbed
    robbed = []
    i = n - 1
    while i >= 0:
        if i == 0 or dp[i] != dp[i - 1]:
            robbed.append(i)
            i -= 2       # skip the adjacent house
        else:
            i -= 1       # house i was skipped

    return dp[n - 1], sorted(robbed)


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    houses = [2, 7, 9, 3, 1]

    # -- DP table trace ---------------------------------------------
    print("=" * 60)
    print("  House Robber -- DP Table Trace")
    print("=" * 60)
    n = len(houses)
    print(f"\n  houses = {houses}")
    print(f"\n  {'i':>4}   {'house[i]':>10}   {'dp[i]':>8}   {'decision':}")
    print("  " + "-" * 58)

    dp = [0] * n
    dp[0] = houses[0]
    print(f"  {0:>4}   {houses[0]:>10}   {dp[0]:>8}   base case")

    if n > 1:
        dp[1] = max(houses[0], houses[1])
        chosen = f"max(h[0]={houses[0]}, h[1]={houses[1]})"
        print(f"  {1:>4}   {houses[1]:>10}   {dp[1]:>8}   {chosen}")

    for i in range(2, n):
        rob_i  = houses[i] + dp[i - 2]
        skip_i = dp[i - 1]
        dp[i]  = max(rob_i, skip_i)
        decision = (f"rob: h[{i}]({houses[i]})+dp[{i-2}]({dp[i-2]})={rob_i}, "
                    f"skip: dp[{i-1}]({skip_i}) -> max={dp[i]}")
        print(f"  {i:>4}   {houses[i]:>10}   {dp[i]:>8}   {decision}")

    # -- Result -----------------------------------------------------
    max_money, robbed = house_robber_with_path(houses)
    print(f"\n  Maximum money : {max_money}")
    print(f"  Robbed houses : indices {robbed}, "
          f"values {[houses[i] for i in robbed]}, "
          f"sum = {sum(houses[i] for i in robbed)}")

    # -- All three approaches compared ------------------------------
    print("\n" + "=" * 60)
    print("  All Three Approaches -- Results Match")
    print("=" * 60)
    r1 = house_robber_memo(houses)
    r2 = house_robber_tabulation(houses)
    r3 = house_robber_optimised(houses)
    print(f"\n  houses = {houses}")
    print(f"  Memoization  : {r1}")
    print(f"  Tabulation   : {r2}")
    print(f"  Optimised    : {r3}")
    assert r1 == r2 == r3, "Mismatch!"
    print(f"  All agree    : True")

    # -- Additional test cases --------------------------------------
    print("\n" + "=" * 60)
    print("  Additional Test Cases")
    print("=" * 60)
    test_cases = [
        [1, 2, 3, 1],
        [2, 1, 1, 2],
        [5],
        [1, 5],
        [10, 1, 1, 10],
        [2, 7, 9, 3, 1, 8, 4],
    ]
    for h in test_cases:
        money, idx = house_robber_with_path(h)
        print(f"\n  houses = {h}")
        print(f"    max money = {money}, "
              f"robbed {idx} -> values {[h[i] for i in idx]}")

    # -- Complexity summary -----------------------------------------
    print("\n" + "=" * 60)
    print("  Complexity Summary")
    print("=" * 60)
    print("""
    Time  Complexity : O(n)
      Single pass through the houses array.
      Each house processed exactly once.

    Space Complexity:
      Memoization  : O(n) -- cache + recursion stack
      Tabulation   : O(n) -- dp array of size n
      Optimised    : O(1) -- only two rolling variables (prev2, prev1)

    Recurrence:
      dp[i] = max(houses[i] + dp[i-2],   <- rob house i
                  dp[i-1])               <- skip house i

    Why DP?
      OPTIMAL SUBSTRUCTURE: max money up to house i depends only on
      the optimal solutions for i-1 and i-2.
      OVERLAPPING SUBPROBLEMS: dp[i-2] is needed by multiple houses.
    """)
