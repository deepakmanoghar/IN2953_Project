"""
Q5. Longest Increasing Subsequence (LIS):
    Find the LIS of [10, 9, 2, 5, 3, 7, 101, 18].
    Show the DP array at each step. What is the time complexity?

    LONGEST INCREASING SUBSEQUENCE:
    --------------------------------
    A subsequence is a set of elements chosen from the array in order
    (not necessarily contiguous) where each element is STRICTLY GREATER
    than the previous.

    Example: [10, 9, 2, 5, 3, 7, 101, 18]
      LIS = [2, 5, 7, 101] or [2, 3, 7, 101] or [2, 5, 7, 18]
      Length = 4

    APPROACH 1 -- O(n^2) DP:
    -------------------------
    dp[i] = length of LIS ending AT index i
    dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])
            (at minimum every element is its own LIS of length 1)

    APPROACH 2 -- O(n log n) Patience Sorting:
    -------------------------------------------
    Maintain a 'tails' array where tails[k] is the smallest tail
    element of all increasing subsequences of length k+1.
    Use binary search to find insertion position.

    TIME:
      O(n^2)    -- DP approach (two nested loops)
      O(n logn) -- Patience sorting with binary search

    SPACE: O(n) for the dp or tails array.
"""

import bisect


# =====================================================
# Approach 1 -- O(n^2) DP
# =====================================================
def lis_dp(nums):
    """
    dp[i] = length of the LIS ending at index i.
    For each i, look back at all j < i where nums[j] < nums[i].
    """
    if not nums:
        return 0
    n   = len(nums)
    dp  = [1] * n          # every element is at least a subsequence of 1

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_dp_with_path(nums):
    """
    Returns (length, one_actual_LIS_sequence).
    Uses a 'parent' array to reconstruct the subsequence.
    """
    if not nums:
        return 0, []
    n      = len(nums)
    dp     = [1] * n
    parent = [-1] * n      # parent[i] = index of previous element in LIS

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i]     = dp[j] + 1
                parent[i] = j

    # Find the index with maximum LIS length
    max_len = max(dp)
    idx     = dp.index(max_len)

    # Reconstruct path by following parent pointers
    path = []
    while idx != -1:
        path.append(nums[idx])
        idx = parent[idx]
    path.reverse()

    return max_len, path


# =====================================================
# Approach 2 -- O(n log n) Patience Sorting
# =====================================================
def lis_patience(nums):
    """
    'tails[i]' = smallest tail of all increasing subsequences of
    length i+1 seen so far.
    For each number x:
      - If x > all tails -> extend the longest subsequence.
      - Otherwise        -> replace the leftmost tail >= x with x.
    The length of tails at the end is the LIS length.
    """
    tails = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)   # binary search
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# =====================================================
# Step-by-step DP trace
# =====================================================
def lis_trace(nums):
    """Prints the dp array after each element is processed."""
    n      = len(nums)
    dp     = [1] * n
    parent = [-1] * n

    print(f"\n  nums = {nums}")
    print(f"\n  {'i':>4}   {'nums[i]':>8}   {'dp array after step i':}")
    print("  " + "-" * 65)
    print(f"  {'--':>4}   {'-------':>8}   {[1]*n}")

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i]     = dp[j] + 1
                parent[i] = j

        comparisons = [f"nums[{j}]={nums[j]}<{nums[i]}: dp[{j}]+1={dp[j]+1 if nums[j]<nums[i] else 'skip'}"
                       for j in range(i) if nums[j] < nums[i]]
        print(f"  {i:>4}   {nums[i]:>8}   {list(dp)}  "
              f"(best extension: {'max from j<'+str(i) if any(nums[j]<nums[i] for j in range(i)) else 'none'})")

    max_len = max(dp)
    print(f"\n  Final dp = {dp}")
    print(f"  LIS length = max(dp) = {max_len}")
    return dp, parent


# =====================================================
# Patience sorting trace
# =====================================================
def patience_trace(nums):
    """Shows tails array evolution during patience sorting."""
    tails = []
    print(f"\n  nums = {nums}")
    print(f"\n  {'x':>6}   {'action':>30}   {'tails':}")
    print("  " + "-" * 65)
    for x in nums:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
            action = f"extend  -> append {x}"
        else:
            action = f"replace tails[{pos}]={tails[pos]} with {x}"
            tails[pos] = x
        print(f"  {x:>6}   {action:>30}   {tails}")
    print(f"\n  LIS length = len(tails) = {len(tails)}")
    return len(tails)


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    nums = [10, 9, 2, 5, 3, 7, 101, 18]

    # -- DP trace ---------------------------------------------------
    print("=" * 60)
    print("  LIS -- O(n^2) DP Trace")
    print("=" * 60)
    dp_arr, parent_arr = lis_trace(nums)

    # -- Result with reconstruction ---------------------------------
    print("\n" + "=" * 60)
    print("  LIS -- Result with Actual Subsequence")
    print("=" * 60)
    length, seq = lis_dp_with_path(nums)
    print(f"\n  nums = {nums}")
    print(f"  LIS length : {length}")
    print(f"  One LIS    : {seq}")

    # -- Patience sorting trace -------------------------------------
    print("\n" + "=" * 60)
    print("  LIS -- O(n log n) Patience Sorting Trace")
    print("=" * 60)
    patience_trace(nums)

    # -- Compare both approaches ------------------------------------
    print("\n" + "=" * 60)
    print("  Both Approaches Agree")
    print("=" * 60)
    r1 = lis_dp(nums)
    r2 = lis_patience(nums)
    print(f"\n  DP approach (O(n^2))       : {r1}")
    print(f"  Patience   (O(n log n))    : {r2}")
    print(f"  Same result                : {r1 == r2}")

    # -- Additional test cases --------------------------------------
    print("\n" + "=" * 60)
    print("  Additional Test Cases")
    print("=" * 60)
    tests = [
        [0, 1, 0, 3, 2, 3],
        [7, 7, 7, 7],
        [1, 3, 6, 7, 9, 4, 10, 5, 6],
        [5, 4, 3, 2, 1],    # all decreasing -> LIS = 1
        [1, 2, 3, 4, 5],    # all increasing -> LIS = n
    ]
    for t in tests:
        ln, sq = lis_dp_with_path(t)
        print(f"\n  nums = {t}")
        print(f"    LIS length = {ln},  one LIS = {sq}")

    # -- dp array step-by-step for the main example -----------------
    print("\n" + "=" * 60)
    print("  dp[i] at Each Step  --  [10,9,2,5,3,7,101,18]")
    print("=" * 60)
    print("""
    i=0  nums[0]=10   dp=[1,1,1,1,1,1,1,1]  (no j < 0)
    i=1  nums[1]= 9   dp=[1,1,1,1,1,1,1,1]  (9 < 10? No)
    i=2  nums[2]= 2   dp=[1,1,1,1,1,1,1,1]  (2<10? No; 2<9? No)
    i=3  nums[3]= 5   dp=[1,1,1,2,1,1,1,1]  (5>2 -> dp[2]+1=2)
    i=4  nums[4]= 3   dp=[1,1,1,2,2,1,1,1]  (3>2 -> dp[2]+1=2)
    i=5  nums[5]= 7   dp=[1,1,1,2,2,3,1,1]  (7>5->dp[3]+1=3; 7>3->dp[4]+1=3)
    i=6  nums[6]=101  dp=[1,1,1,2,2,3,4,1]  (101>7->dp[5]+1=4)
    i=7  nums[7]= 18  dp=[1,1,1,2,2,3,4,4]  (18>7->dp[5]+1=4)

    LIS length = max(dp) = 4
    """)

    # -- Complexity summary -----------------------------------------
    print("=" * 60)
    print("  Complexity Summary")
    print("=" * 60)
    print("""
    Approach 1 -- O(n^2) DP:
      Time  : O(n^2)    -- two nested loops (i from 1..n, j from 0..i-1)
      Space : O(n)      -- dp array + parent array for reconstruction

    Approach 2 -- O(n log n) Patience Sorting:
      Time  : O(n log n) -- n elements, each binary search is O(log n)
      Space : O(n)       -- tails array of size <= n

    Note: Patience sorting gives the CORRECT LENGTH but the 'tails'
    array itself is NOT a valid LIS (elements may not be contiguous).
    To reconstruct the actual sequence, an additional O(n) array is
    needed alongside the patience sort process.

    When to choose which:
      O(n^2)    -- simpler, easy to reconstruct, fine for n < 10000
      O(n logn) -- needed for large inputs (n up to 10^5 or more)
    """)
