"""
Q2. Implement quicksort with the Lomuto partition scheme.
    What is the worst case? How can you avoid it?

    QUICKSORT:
    ----------
    A divide-and-conquer in-place sorting algorithm.
    At each step it selects a PIVOT element and partitions the array so:
      - All elements < pivot go LEFT of pivot.
      - All elements > pivot go RIGHT of pivot.
    Then it recurses on the left and right sub-arrays.

    LOMUTO PARTITION SCHEME:
    ------------------------
    Uses the LAST element as pivot.
    Maintains a boundary index 'i' such that arr[lo..i] <= pivot.
    Scans with pointer 'j'; swaps arr[j] left whenever arr[j] <= pivot.
    Places pivot at arr[i+1] at the end.

    WORST CASE:  O(n^2)
    -------------------
    Occurs when the pivot is ALWAYS the smallest or largest element,
    causing one partition of size 0 and one of size n-1 every time.
    Trigger: already sorted or reverse-sorted array + last-element pivot.

    HOW TO AVOID THE WORST CASE:
    -----------------------------
    1. RANDOM PIVOT -- choose a random element as pivot each time.
       Reduces probability of worst case to negligible.
    2. MEDIAN-OF-THREE -- pivot = median of (first, middle, last).
       Good practical choice.
    3. THREE-WAY PARTITION (Dutch-flag) -- handles duplicates efficiently.
    4. INTROSORT -- hybrid: QuickSort + HeapSort fallback when recursion
       depth exceeds 2*log(n). Used by C++ STL and Python's sort.

    TIME  : O(n log n) average,  O(n^2) worst
    SPACE : O(log n) average (call stack),  O(n) worst
"""

import random


# =====================================================
# Lomuto partition
# =====================================================
def _lomuto_partition(arr, lo, hi):
    """
    Partition arr[lo..hi] around pivot = arr[hi].
    After partitioning, pivot is at its correct sorted position.

    Returns: index of pivot after partitioning.
    """
    pivot = arr[hi]
    i     = lo - 1          # boundary of the 'less than pivot' region

    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]   # extend left region

    # Place pivot at its correct position
    arr[i+1], arr[hi] = arr[hi], arr[i+1]
    return i + 1


# =====================================================
# Quicksort with Lomuto (fixed last-element pivot)
# =====================================================
def quicksort_lomuto(arr, lo=0, hi=None):
    """In-place quicksort using Lomuto partition (last element as pivot)."""
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        pivot_idx = _lomuto_partition(arr, lo, hi)
        quicksort_lomuto(arr, lo, pivot_idx - 1)
        quicksort_lomuto(arr, pivot_idx + 1, hi)


# =====================================================
# Quicksort with RANDOM pivot (avoids worst case)
# =====================================================
def quicksort_random_pivot(arr, lo=0, hi=None):
    """Same as above but swaps a random element into the last position first."""
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        rand_idx = random.randint(lo, hi)
        arr[rand_idx], arr[hi] = arr[hi], arr[rand_idx]   # swap to last
        pivot_idx = _lomuto_partition(arr, lo, hi)
        quicksort_random_pivot(arr, lo, pivot_idx - 1)
        quicksort_random_pivot(arr, pivot_idx + 1, hi)


# =====================================================
# Quicksort with MEDIAN-OF-THREE pivot
# =====================================================
def _median_of_three(arr, lo, hi):
    """Swap the median of (arr[lo], arr[mid], arr[hi]) into arr[hi]."""
    mid = (lo + hi) // 2
    # Sort lo, mid, hi in-place then take arr[mid] as pivot
    if arr[lo] > arr[mid]:
        arr[lo], arr[mid] = arr[mid], arr[lo]
    if arr[lo] > arr[hi]:
        arr[lo], arr[hi] = arr[hi], arr[lo]
    if arr[mid] > arr[hi]:
        arr[mid], arr[hi] = arr[hi], arr[mid]
    # arr[mid] is now the median; swap to last so Lomuto can use it
    arr[mid], arr[hi] = arr[hi], arr[mid]


def quicksort_median_of_three(arr, lo=0, hi=None):
    """Quicksort using median-of-three pivot selection."""
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        _median_of_three(arr, lo, hi)
        pivot_idx = _lomuto_partition(arr, lo, hi)
        quicksort_median_of_three(arr, lo, pivot_idx - 1)
        quicksort_median_of_three(arr, pivot_idx + 1, hi)


# =====================================================
# Traced quicksort (show each partition step)
# =====================================================
def quicksort_traced(arr, lo=0, hi=None, depth=0):
    """Lomuto quicksort that prints each partitioning step."""
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    pad = "  " * depth
    pivot = arr[hi]
    print(f"{pad}sort({arr[lo:hi+1]})  pivot={pivot}")
    pivot_idx = _lomuto_partition(arr, lo, hi)
    print(f"{pad}  after partition: {arr[lo:hi+1]}  pivot at index {pivot_idx} (value {arr[pivot_idx]})")
    quicksort_traced(arr, lo, pivot_idx - 1, depth + 1)
    quicksort_traced(arr, pivot_idx + 1, hi, depth + 1)


# =====================================================
# Worst-case demonstration
# =====================================================
def count_comparisons_lomuto(arr):
    """Count how many comparisons Lomuto makes (for worst-case demo)."""
    arr   = arr[:]
    count = [0]

    def partition(lo, hi):
        pivot = arr[hi]
        i     = lo - 1
        for j in range(lo, hi):
            count[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[hi] = arr[hi], arr[i+1]
        return i + 1

    def qs(lo, hi):
        if lo < hi:
            p = partition(lo, hi)
            qs(lo, p-1)
            qs(p+1, hi)

    qs(0, len(arr)-1)
    return count[0]


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]

    # ── Basic Lomuto sort ─────────────────────────────
    print("=" * 60)
    print(f"QUICKSORT (Lomuto)  Input: {arr}")
    print("=" * 60)

    a1 = arr[:]
    quicksort_traced(a1)
    print(f"\nFinal sorted: {a1}  {'[OK]' if a1 == sorted(arr) else '[X]'}")

    # ── All three variants ────────────────────────────
    print("\n" + "=" * 60)
    print("ALL THREE PIVOT STRATEGIES:")
    print("=" * 60)
    for label, fn in [
        ("Lomuto (last element)", quicksort_lomuto),
        ("Random pivot",          quicksort_random_pivot),
        ("Median-of-three",       quicksort_median_of_three),
    ]:
        tc = arr[:]
        fn(tc)
        ok = "[OK]" if tc == sorted(arr) else "[X]"
        print(f"  {label:<28}: {tc}  {ok}")

    # ── Worst-case demonstration ──────────────────────
    print("\n" + "=" * 60)
    print("WORST-CASE DEMONSTRATION:")
    print("=" * 60)
    n = 8
    already_sorted  = list(range(n))
    reverse_sorted  = list(range(n, 0, -1))
    random_arr      = [3,1,4,1,5,9,2,6]

    print(f"  n = {n},  worst case comparisons ~ n*(n-1)/2 = {n*(n-1)//2}")
    print(f"  {'Array type':<25} {'Comparisons':>13} {'vs n log n':>12}")
    import math
    nlogn = int(n * math.log2(n))
    for label, a in [
        ("Already sorted (WORST)", already_sorted),
        ("Reverse sorted (WORST)", reverse_sorted),
        ("Random (AVERAGE)",       random_arr),
    ]:
        c = count_comparisons_lomuto(a)
        print(f"  {label:<25} {c:>13} {nlogn:>12}")

    # ── Advice summary ────────────────────────────────
    print("\n" + "=" * 60)
    print("HOW TO AVOID WORST CASE:")
    print("  1. Random pivot        -- swap random element to last before partitioning.")
    print("     Expected O(n log n) with high probability.")
    print("  2. Median-of-three     -- use median of first/mid/last as pivot.")
    print("     Good for nearly-sorted data.")
    print("  3. Three-way partition -- group equal elements together.")
    print("     Excellent when many duplicates exist.")
    print("  4. Introsort (Python)  -- QuickSort + HeapSort fallback.")
    print("     Guarantees O(n log n) worst case. Used by Python's sort().")
    print("=" * 60)
