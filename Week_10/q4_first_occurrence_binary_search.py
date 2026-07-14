"""
Q4. Write a binary search function that finds the FIRST OCCURRENCE of a
    target in a sorted array with duplicates.
    Example: [1,2,2,2,3,4] with target=2 -> index 1.

    STANDARD BINARY SEARCH LIMITATION:
    ------------------------------------
    Standard binary search returns SOME index where target == arr[mid],
    but not necessarily the LEFTMOST (first) occurrence.
    In [1,2,2,2,3,4] it might return index 2 or 3 (middle 2's), not 1.

    MODIFICATION:
    -------------
    When arr[mid] == target, instead of returning immediately:
      - Record mid as a CANDIDATE answer.
      - Continue searching LEFT (hi = mid - 1) to find an earlier one.
    When the loop ends, return the last recorded candidate (the leftmost).

    SIMILARLY for LAST occurrence:
    When arr[mid] == target:
      - Record mid as candidate.
      - Continue searching RIGHT (lo = mid + 1).

    TIME  : O(log n)  -- same as standard binary search
    SPACE : O(1)
"""


# =====================================================
# First occurrence (leftmost index)
# =====================================================
def find_first(arr, target):
    """
    Return the index of the FIRST occurrence of target in sorted arr.
    Returns -1 if target is not found.
    """
    lo, hi  = 0, len(arr) - 1
    result  = -1

    while lo <= hi:
        mid = (lo + hi) // 2

        if arr[mid] == target:
            result = mid        # record this as a candidate
            hi     = mid - 1   # keep searching LEFT for an earlier one
        elif arr[mid] < target:
            lo = mid + 1       # target is to the right
        else:
            hi = mid - 1       # target is to the left

    return result


# =====================================================
# Last occurrence (rightmost index)
# =====================================================
def find_last(arr, target):
    """
    Return the index of the LAST occurrence of target in sorted arr.
    Returns -1 if target is not found.
    """
    lo, hi  = 0, len(arr) - 1
    result  = -1

    while lo <= hi:
        mid = (lo + hi) // 2

        if arr[mid] == target:
            result = mid        # record this as a candidate
            lo     = mid + 1   # keep searching RIGHT for a later one
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return result


# =====================================================
# Count occurrences using first + last
# =====================================================
def count_occurrences(arr, target):
    """Count how many times target appears using binary search."""
    first = find_first(arr, target)
    if first == -1:
        return 0
    last = find_last(arr, target)
    return last - first + 1


# =====================================================
# Find range [first, last] in one call
# =====================================================
def search_range(arr, target):
    """Return [first_index, last_index] or [-1, -1] if not found."""
    return [find_first(arr, target), find_last(arr, target)]


# =====================================================
# Verbose trace for find_first
# =====================================================
def find_first_verbose(arr, target):
    lo, hi  = 0, len(arr) - 1
    result  = -1
    step    = 0

    print(f"\n  Searching for FIRST occurrence of {target} in {arr}")
    print(f"  {'Step':>4} | {'lo':>3} {'mid':>4} {'hi':>4} | "
          f"{'arr[mid]':>9} | Action")
    print(f"  {'-'*4}-+-{'-'*3}-{'-'*4}-{'-'*4}-+-{'-'*9}-+-{'-'*35}")

    while lo <= hi:
        mid   = (lo + hi) // 2
        step += 1
        val   = arr[mid]

        if val == target:
            action = f"MATCH -> candidate={mid}, search LEFT (hi={mid-1})"
            result = mid
            hi     = mid - 1
        elif val < target:
            action = f"arr[mid]={val} < {target} -> go RIGHT (lo={mid+1})"
            lo = mid + 1
        else:
            action = f"arr[mid]={val} > {target} -> go LEFT  (hi={mid-1})"
            hi = mid - 1

        print(f"  {step:>4} | {lo:>3} {mid:>4} {hi:>4} | {val:>9} | {action}")

    if result == -1:
        print(f"  Result: NOT FOUND")
    else:
        print(f"  Result: index {result} (value={arr[result]})")
    return result


# =====================================================
# Standard binary search (for comparison - finds ANY occurrence)
# =====================================================
def binary_search_standard(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    # ── Given example from question ──────────────────
    arr    = [1, 2, 2, 2, 3, 4]
    target = 2

    print("=" * 60)
    print(f"FIRST OCCURRENCE BINARY SEARCH")
    print(f"Array : {arr}")
    print(f"Target: {target}")
    print("=" * 60)

    first  = find_first(arr, target)
    last   = find_last(arr, target)
    count  = count_occurrences(arr, target)
    std    = binary_search_standard(arr, target)

    print(f"\n  Standard binary search : index {std}  (not guaranteed to be first!)")
    print(f"  First occurrence       : index {first}  (expected 1)  {'[OK]' if first == 1 else '[X]'}")
    print(f"  Last  occurrence       : index {last}")
    print(f"  Count of {target}'s          : {count}")
    print(f"  Range                  : {search_range(arr, target)}")

    # ── Verbose trace ─────────────────────────────────
    print("\n" + "=" * 60)
    print("VERBOSE TRACE (find_first):")
    print("=" * 60)
    find_first_verbose(arr[:], target)

    # ── Test cases ────────────────────────────────────
    print("\n" + "=" * 60)
    print("COMPREHENSIVE TEST CASES:")
    print("=" * 60)
    tests = [
        ([1,2,2,2,3,4],  2,  1,  3),
        ([1,1,1,1,1],    1,  0,  4),
        ([1,2,3,4,5],    3,  2,  2),
        ([1,2,3,4,5],    6, -1, -1),
        ([2,2],          2,  0,  1),
        ([1],            1,  0,  0),
        ([1],            2, -1, -1),
        ([1,1,2,2,3,3,3,4], 3, 4, 6),
        ([5,7,7,8,8,10], 8,  3,  4),   # LeetCode 34 example
    ]

    print(f"  {'Array':<30} {'target':>6} | {'first':>5} {'last':>5} | {'exp_f':>5} {'exp_l':>5} | OK?")
    print(f"  {'-'*30} {'-'*6}-+-{'-'*5}-{'-'*5}-+-{'-'*5}-{'-'*5}-+-{'-'*4}")

    for a, t, ef, el in tests:
        f = find_first(a, t)
        l = find_last(a, t)
        ok = "[OK]" if f == ef and l == el else "[X]"
        print(f"  {str(a):<30} {t:>6} | {f:>5} {l:>5} | {ef:>5} {el:>5} | {ok}")

    print("\n" + "=" * 60)
    print("WHY STANDARD BINARY SEARCH IS NOT ENOUGH:")
    print("  In [1,2,2,2,3,4], mid starts at index 2 (value=2).")
    print("  Standard binary search returns index 2 immediately.")
    print("  But the FIRST occurrence is at index 1.")
    print()
    print("  FIX: When arr[mid]==target, do NOT return.")
    print("       Instead record mid as 'candidate' and search LEFT.")
    print("       Only return when lo > hi (loop ends).")
    print()
    print("  Time  : O(log n)  -- same as standard binary search")
    print("  Space : O(1)")
    print("=" * 60)
