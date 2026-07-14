"""
Q3. Search for a target in a sorted array that has been rotated at an
    unknown pivot. Example: [4,5,6,7,0,1,2], target=0.
    Use modified binary search.

    KEY INSIGHT:
    ------------
    Even after rotation, at least ONE of the two halves is always
    sorted (monotonically increasing). We can determine which half
    is sorted by comparing arr[lo] with arr[mid]:

      If arr[lo] <= arr[mid]:  the LEFT  half  [lo .. mid] is sorted.
      Else:                    the RIGHT half  [mid .. hi] is sorted.

    Once we know which half is sorted, we check whether the target
    lies within that sorted range:
      - If yes  -> narrow to that half.
      - If no   -> search the OTHER half.

    This gives us O(log n) time even on a rotated array.

    EDGE CASE -- DUPLICATES:
    If arr[lo] == arr[mid] we cannot determine which side is sorted.
    We can only safely increment lo (skip one element).
    Worst case with duplicates becomes O(n).

    TIME  : O(log n) -- no duplicates
    SPACE : O(1)     -- iterative
"""


# =====================================================
# Search in rotated sorted array (no duplicates)
# =====================================================
def search_rotated(arr, target):
    """
    Binary search in a rotated sorted array (no duplicates).
    Returns the index of target, or -1 if not found.
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = (lo + hi) // 2

        if arr[mid] == target:
            return mid

        # Determine which half is sorted
        if arr[lo] <= arr[mid]:
            # LEFT half [lo..mid] is sorted
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1        # target is in the sorted left half
            else:
                lo = mid + 1        # target is in the right half

        else:
            # RIGHT half [mid..hi] is sorted
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1        # target is in the sorted right half
            else:
                hi = mid - 1        # target is in the left half

    return -1   # not found


# =====================================================
# Handle duplicates (worst case O(n))
# =====================================================
def search_rotated_with_dups(arr, target):
    """
    Modified binary search for rotated array that may have duplicates.
    When arr[lo] == arr[mid], we can't determine sorted half,
    so we just increment lo.
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = (lo + hi) // 2

        if arr[mid] == target:
            return mid

        if arr[lo] == arr[mid]:
            lo += 1      # can't determine which side is sorted, skip
        elif arr[lo] < arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1


# =====================================================
# Verbose trace showing each decision
# =====================================================
def search_rotated_verbose(arr, target):
    lo, hi = 0, len(arr) - 1
    step = 0

    print(f"\n  Searching for {target} in {arr}")
    print(f"  {'Step':>4} | {'lo':>3} {'mid':>4} {'hi':>4} | "
          f"{'arr[lo]':>8} {'arr[mid]':>9} {'arr[hi]':>8} | Decision")
    print(f"  {'-'*4}-+-{'-'*3}-{'-'*4}-{'-'*4}-+-"
          f"{'-'*8}-{'-'*9}-{'-'*8}-+-{'-'*30}")

    while lo <= hi:
        mid  = (lo + hi) // 2
        step += 1
        decision = ""

        if arr[mid] == target:
            decision = f"FOUND at index {mid}!"
            print(f"  {step:>4} | {lo:>3} {mid:>4} {hi:>4} | "
                  f"{arr[lo]:>8} {arr[mid]:>9} {arr[hi]:>8} | {decision}")
            return mid

        if arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                decision = "left half sorted, target in it -> hi=mid-1"
                hi = mid - 1
            else:
                decision = "left half sorted, target NOT in it -> lo=mid+1"
                lo = mid + 1
        else:
            if arr[mid] < target <= arr[hi]:
                decision = "right half sorted, target in it -> lo=mid+1"
                lo = mid + 1
            else:
                decision = "right half sorted, target NOT in it -> hi=mid-1"
                hi = mid - 1

        print(f"  {step:>4} | {lo:>3} {mid:>4} {hi:>4} | "
              f"{arr[lo] if lo < len(arr) else '-':>8} "
              f"{arr[mid]:>9} "
              f"{arr[hi] if hi >= 0 else '-':>8} | {decision}")

    print(f"  {step+1:>4} | --- NOT FOUND ---")
    return -1


# =====================================================
# Find pivot index (where rotation happened)
# =====================================================
def find_pivot(arr):
    """Return the index of the minimum element (the rotation pivot)."""
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] > arr[hi]:
            lo = mid + 1    # min is in the right half
        else:
            hi = mid        # min is in the left half (including mid)
    return lo


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    # ── Given example from question ──────────────────
    arr    = [4, 5, 6, 7, 0, 1, 2]
    target = 0

    print("=" * 65)
    print(f"SEARCH IN ROTATED SORTED ARRAY")
    print(f"Input : {arr}")
    print(f"Target: {target}")
    print("=" * 65)

    result = search_rotated(arr, target)
    print(f"\n  Result index : {result}  (value: {arr[result] if result != -1 else 'N/A'})")
    print(f"  Expected     : {arr.index(target)}")
    print(f"  Correct      : {'[OK]' if result == arr.index(target) else '[X]'}")

    # ── Verbose trace ─────────────────────────────────
    print("\n" + "=" * 65)
    print("VERBOSE TRACE:")
    print("=" * 65)
    search_rotated_verbose(arr[:], target)

    # ── Key insight diagram ───────────────────────────
    pivot_idx = find_pivot(arr)
    print(f"\n  Array    : {arr}")
    print(f"  Pivot idx: {pivot_idx}  (value {arr[pivot_idx]} is the minimum)")
    print(f"  Original : [0, 1, 2, 4, 5, 6, 7]  rotated left by {pivot_idx} positions")

    # ── More test cases ───────────────────────────────
    print("\n" + "=" * 65)
    print("TEST CASES (no duplicates):")
    print("=" * 65)
    tests = [
        ([4,5,6,7,0,1,2], 0,  4),
        ([4,5,6,7,0,1,2], 4,  0),
        ([4,5,6,7,0,1,2], 7,  3),
        ([4,5,6,7,0,1,2], 3, -1),
        ([1],              1,  0),
        ([3,1],            1,  1),
        ([3,1],            3,  0),
        ([1,3,5],          5,  2),
        ([5,1,3],          3,  2),
    ]
    for a, t, exp in tests:
        got = search_rotated(a[:], t)
        ok  = "[OK]" if got == exp else "[X]"
        print(f"  {str(a):<25}  target={t:<3}  got={got:>2}  exp={exp:>2}  {ok}")

    # ── Duplicate test ────────────────────────────────
    print("\n" + "=" * 65)
    print("TEST CASES (with duplicates -- worst case O(n)):")
    print("=" * 65)
    dup_tests = [
        ([2,2,2,0,2,2], 0,  True),
        ([1,1,3,1],     3,  True),
        ([2,2,2,2,2],   3, False),
    ]
    for a, t, exp_found in dup_tests:
        idx = search_rotated_with_dups(a[:], t)
        found = idx != -1
        ok    = "[OK]" if found == exp_found else "[X]"
        print(f"  {str(a):<22}  target={t}  found={found}  expected={exp_found}  {ok}")

    print("\n" + "=" * 65)
    print("KEY INSIGHT RECAP:")
    print("  In a rotated sorted array [lo..hi], one half is ALWAYS sorted.")
    print("  Compare arr[lo] vs arr[mid] to identify which half:")
    print("    arr[lo] <= arr[mid]  ->  left  half [lo..mid] is sorted.")
    print("    arr[lo] >  arr[mid]  ->  right half [mid..hi] is sorted.")
    print("  Then check if target falls in the sorted half's range.")
    print("  If yes  -> narrow to that half.")
    print("  If no   -> search the other half.")
    print("  Time: O(log n)  |  Space: O(1)")
    print("=" * 65)
