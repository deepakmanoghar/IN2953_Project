"""
Q8. Given two sorted arrays, find the median of the combined sorted array
    in O(log(min(m,n))) time.

    BINARY SEARCH APPROACH:
    -----------------------
    Key idea: instead of merging (O(m+n)), use binary search on the
    SHORTER array to find the correct PARTITION POINT that splits both
    arrays into a left half and a right half such that:

      1. The left half has exactly (m+n+1)//2 total elements.
      2. Every element in the left half <= every element in the right half.

    Let the two arrays be A (length m) and B (length n), with m <= n.
    We binary search on A's partition index i (0 to m).
    j = half_len - i  (B's partition index, determined by i).

    The partition is VALID if:
      A[i-1] <= B[j]   (left-A's max <= right-B's min)
      B[j-1] <= A[i]   (left-B's max <= right-A's min)

    If A[i-1] > B[j]  -> i is too large -> hi = i - 1
    If B[j-1] > A[i]  -> i is too small -> lo = i + 1

    MEDIAN CALCULATION (once valid partition is found):
      max_left  = max(A[i-1], B[j-1])   -- largest on the left
      min_right = min(A[i],   B[j])     -- smallest on the right
      If (m+n) is ODD  -> median = max_left
      If (m+n) is EVEN -> median = (max_left + min_right) / 2

    EDGE CASES:
      i=0 means A contributes nothing to the left  -> A[i-1] = -inf
      i=m means A contributes everything           -> A[i]   = +inf
      Same for j and B.

    TIME  : O(log(min(m, n)))  -- binary search on the shorter array
    SPACE : O(1)
"""

import math


# =====================================================
# Median of two sorted arrays -- O(log(min(m,n)))
# =====================================================
def find_median_sorted_arrays(A, B):
    """
    Find the median of the merged sorted array of A and B.

    Args:
        A, B : list[int] -- sorted arrays

    Returns:
        float -- the median value
    """
    # Ensure A is the shorter array (binary search on shorter = fewer steps)
    if len(A) > len(B):
        A, B = B, A

    m, n   = len(A), len(B)
    half   = (m + n + 1) // 2   # number of elements in the left half

    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2      # partition A: A[:i] goes left, A[i:] goes right
        j = half - i            # partition B: B[:j] goes left, B[j:] goes right

        # Guard against out-of-bounds using -inf / +inf sentinels
        A_left  = A[i-1] if i > 0 else -math.inf
        A_right = A[i]   if i < m else  math.inf
        B_left  = B[j-1] if j > 0 else -math.inf
        B_right = B[j]   if j < n else  math.inf

        if A_left <= B_right and B_left <= A_right:
            # Valid partition found!
            max_left  = max(A_left,  B_left)
            min_right = min(A_right, B_right)

            if (m + n) % 2 == 1:
                return float(max_left)          # odd total -> left's max IS the median
            else:
                return (max_left + min_right) / 2.0  # even total -> average of neighbours

        elif A_left > B_right:
            hi = i - 1      # A's left part is too large, shrink it
        else:
            lo = i + 1      # B's left part is too large, grow A's left part

    raise ValueError("Input arrays are not sorted or are invalid.")


# =====================================================
# Brute force for verification: O(m+n)
# =====================================================
def find_median_brute(A, B):
    """Merge then find median. O(m+n) time, O(m+n) space."""
    merged = sorted(A + B)
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    else:
        return (merged[n//2 - 1] + merged[n//2]) / 2.0


# =====================================================
# Verbose trace showing binary search decisions
# =====================================================
def find_median_verbose(A, B):
    if len(A) > len(B):
        A, B = B, A

    m, n = len(A), len(B)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    step = 0

    print(f"\n  A = {A}  (m={m})")
    print(f"  B = {B}  (n={n})")
    print(f"  Total elements = {m+n}, half = {half}")
    print(f"\n  {'Step':>4} | {'i':>3} {'j':>3} | "
          f"{'A_left':>8} {'A_right':>9} | {'B_left':>8} {'B_right':>9} | Decision")
    print(f"  {'-'*4}-+-{'-'*3}-{'-'*3}-+-"
          f"{'-'*8}-{'-'*9}-+-{'-'*8}-{'-'*9}-+-{'-'*25}")

    while lo <= hi:
        i  = (lo + hi) // 2
        j  = half - i
        step += 1

        A_left  = A[i-1] if i > 0 else -math.inf
        A_right = A[i]   if i < m else  math.inf
        B_left  = B[j-1] if j > 0 else -math.inf
        B_right = B[j]   if j < n else  math.inf

        A_l_str = str(A_left)  if A_left  != -math.inf else "-inf"
        A_r_str = str(A_right) if A_right !=  math.inf else "+inf"
        B_l_str = str(B_left)  if B_left  != -math.inf else "-inf"
        B_r_str = str(B_right) if B_right !=  math.inf else "+inf"

        if A_left <= B_right and B_left <= A_right:
            decision = "VALID partition!"
        elif A_left > B_right:
            decision = f"A_left>{B_r_str} -> hi={i-1}"
            hi = i - 1
        else:
            decision = f"B_left>{A_r_str} -> lo={i+1}"
            lo = i + 1

        print(f"  {step:>4} | {i:>3} {j:>3} | "
              f"{A_l_str:>8} {A_r_str:>9} | "
              f"{B_l_str:>8} {B_r_str:>9} | {decision}")

        if A_left <= B_right and B_left <= A_right:
            max_left  = max(A_left,  B_left)
            min_right = min(A_right, B_right)
            if (m + n) % 2 == 1:
                med = float(max_left)
            else:
                med = (max_left + min_right) / 2.0
            print(f"\n  max_left={max_left}, min_right={min_right}")
            print(f"  Median = {med}")
            return med

    return None


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        ([1, 3],          [2],              2.0),
        ([1, 2],          [3, 4],           2.5),
        ([0, 0],          [0, 0],           0.0),
        ([],              [1],              1.0),
        ([2],             [],               2.0),
        ([1, 3, 5, 7],    [2, 4, 6, 8],     4.5),
        ([1, 2],          [3, 4, 5, 6, 7],  4.0),
        ([1, 3],          [2, 4, 5, 6],     3.5),
        ([100001, 100002],[100003, 100004], 100002.5),
    ]

    print("=" * 65)
    print("MEDIAN OF TWO SORTED ARRAYS  O(log(min(m,n)))")
    print("=" * 65)
    print(f"\n  {'A':<20} {'B':<22} {'Binary':>8} {'Brute':>7} {'OK':>4}")
    print(f"  {'-'*20} {'-'*22} {'-'*8} {'-'*7} {'-'*4}")

    for A, B, expected in test_cases:
        bs  = find_median_sorted_arrays(A[:], B[:])
        bf  = find_median_brute(A[:], B[:])
        ok  = "[OK]" if abs(bs - expected) < 1e-9 and abs(bf - expected) < 1e-9 else "[X]"
        print(f"  {str(A):<20} {str(B):<22} {bs:>8} {bf:>7} {ok:>4}")

    # ── Verbose trace ─────────────────────────────────
    print("\n" + "=" * 65)
    print("VERBOSE TRACE  A=[1,3]  B=[2,4,6]:")
    print("=" * 65)
    find_median_verbose([1, 3], [2, 4, 6])

    print("\n" + "=" * 65)
    print("VERBOSE TRACE  A=[1,2]  B=[3,4]:")
    print("=" * 65)
    find_median_verbose([1, 2], [3, 4])

    # ── Concept explanation ───────────────────────────
    print("\n" + "=" * 65)
    print("BINARY SEARCH APPROACH EXPLAINED:")
    print("=" * 65)
    print("""
  Goal: find a split point (i in A, j in B) such that:
    - Left side has exactly (m+n+1)//2 total elements.
    - max(A[i-1], B[j-1]) <= min(A[i], B[j]).

  Binary search on A (the shorter array, size m):
    i ranges from 0 to m.
    j = half - i  (determined by i).

  At each step:
    If A[i-1] > B[j]:  i is too large -> search left  (hi = i-1).
    If B[j-1] > A[i]:  i is too small -> search right (lo = i+1).
    Otherwise         : valid partition found.

  Once valid:
    Odd  total: median = max(A[i-1], B[j-1])
    Even total: median = (max(A[i-1],B[j-1]) + min(A[i],B[j])) / 2

  Time:  O(log(min(m,n)))  -- binary search on the shorter array.
  Space: O(1)              -- only a few pointers/variables.

  Why log(min(m,n)) and not log(m+n)?
    We only search in the shorter array (length min(m,n)).
    Partitioning A automatically determines B's partition via j=half-i.
""")
    print("=" * 65)
