"""
Q1. Implement merge sort and trace through the algorithm for
    [38, 27, 43, 3, 9, 82, 10].
    Draw the divide and merge steps.

    MERGE SORT:
    -----------
    A divide-and-conquer algorithm that:
      1. DIVIDES the array into two halves.
      2. RECURSIVELY sorts each half.
      3. MERGES the two sorted halves back into one sorted array.

    KEY PROPERTIES:
    ---------------
    - Stable sort (equal elements keep original relative order).
    - Guaranteed O(n log n) in ALL cases (best, average, worst).
    - Requires O(n) extra space for the temporary merge buffer.
    - Preferred for linked lists and external sorting.

    TIME  : O(n log n)  -- log n levels, each level does O(n) work
    SPACE : O(n)        -- temporary arrays during merge
"""

STEP = [0]   # global step counter for tracing


# =====================================================
# Core merge sort
# =====================================================
def merge_sort(arr):
    """
    Sort and return a new sorted list (non-destructive).
    """
    if len(arr) <= 1:
        return arr[:]

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j  = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:     # <= preserves stability
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# =====================================================
# In-place merge sort (modifies array directly)
# =====================================================
def merge_sort_inplace(arr, lo=0, hi=None):
    """In-place merge sort using slice indices."""
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    merge_sort_inplace(arr, lo, mid)
    merge_sort_inplace(arr, mid + 1, hi)
    _merge_inplace(arr, lo, mid, hi)


def _merge_inplace(arr, lo, mid, hi):
    left  = arr[lo:mid+1]
    right = arr[mid+1:hi+1]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]; i += 1
        else:
            arr[k] = right[j]; j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]; i += 1; k += 1
    while j < len(right):
        arr[k] = right[j]; j += 1; k += 1


# =====================================================
# Traced merge sort -- prints every divide/merge step
# =====================================================
def merge_sort_traced(arr, depth=0):
    """
    Same algorithm as merge_sort but prints each step.
    depth controls indentation to visualise the recursion tree.
    """
    pad = "  " * depth

    if len(arr) <= 1:
        print(f"{pad}BASE  {arr}  (length <= 1, return as-is)")
        return arr[:]

    mid   = len(arr) // 2
    left  = arr[:mid]
    right = arr[mid:]

    STEP[0] += 1
    print(f"{pad}DIVIDE [{', '.join(map(str,arr))}]")
    print(f"{pad}  --> left  {left}")
    print(f"{pad}  --> right {right}")

    sorted_left  = merge_sort_traced(left,  depth + 1)
    sorted_right = merge_sort_traced(right, depth + 1)

    merged = _merge(sorted_left, sorted_right)
    print(f"{pad}MERGE  {sorted_left} + {sorted_right} --> {merged}")
    return merged


# =====================================================
# Draw divide/merge tree (ASCII art)
# =====================================================
def draw_divide_steps(arr):
    """Print a neat tree showing all split levels."""
    print("\n  DIVIDE STEPS:")
    print("  " + str(arr))

    def show_splits(a, indent=0):
        if len(a) <= 1:
            return
        pad = "  " * (indent + 1)
        mid = len(a) // 2
        L, R = a[:mid], a[mid:]
        print(f"{pad}|-- L: {L}")
        print(f"{pad}|-- R: {R}")
        show_splits(L, indent + 1)
        show_splits(R, indent + 1)

    show_splits(arr)


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]

    print("=" * 60)
    print(f"MERGE SORT  Input: {arr}")
    print("=" * 60)

    # ── ASCII divide tree ─────────────────────────────
    draw_divide_steps(arr)

    # ── Full trace ────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP-BY-STEP TRACE:")
    print("=" * 60)
    STEP[0] = 0
    result = merge_sort_traced(arr[:])

    # ── Verify ────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"Input  : {arr}")
    print(f"Output : {result}")
    print(f"Correct: {'[OK]' if result == sorted(arr) else '[X]'}")

    # ── In-place variant ──────────────────────────────
    arr2 = arr[:]
    merge_sort_inplace(arr2)
    print(f"In-place output: {arr2}  {'[OK]' if arr2 == sorted(arr) else '[X]'}")

    # ── Additional tests ─────────────────────────────
    print("\n" + "=" * 60)
    print("ADDITIONAL TEST CASES:")
    extra = [
        [5, 4, 3, 2, 1],
        [1],
        [],
        [2, 2, 2],
        [1, 2, 3, 4, 5],
    ]
    for tc in extra:
        got = merge_sort(tc)
        exp = sorted(tc)
        print(f"  {str(tc):<25} -> {str(got):<25} {'[OK]' if got == exp else '[X]'}")

    print("\n" + "=" * 60)
    print("COMPLEXITY SUMMARY:")
    print("  Time  (all cases): O(n log n)")
    print("  Space            : O(n)  -- temporary merge arrays")
    print("  Stable           : Yes")
    print("  In-place         : No (needs O(n) extra)")
    print("=" * 60)
