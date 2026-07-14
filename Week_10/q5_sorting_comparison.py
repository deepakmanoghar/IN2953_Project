"""
Q5. Compare the time and space complexity of:
    Bubble Sort, Merge Sort, Quick Sort, and Python's built-in sorted().
    When would you use each?

    ─────────────────────────────────────────────────────────────────────────
    ALGORITHM COMPARISON TABLE
    ─────────────────────────────────────────────────────────────────────────
    Algorithm   | Best      | Average   | Worst     | Space  | Stable
    ────────────-+-----------+-----------+-----------+--------+-------
    Bubble Sort | O(n)      | O(n^2)    | O(n^2)    | O(1)   | Yes
    Merge Sort  | O(n log n)| O(n log n)| O(n log n)| O(n)   | Yes
    Quick Sort  | O(n log n)| O(n log n)| O(n^2)    | O(log n)| No
    Python sort | O(n)      | O(n log n)| O(n log n)| O(n)   | Yes
    ─────────────────────────────────────────────────────────────────────────

    PYTHON'S sorted() / list.sort():
    ---------------------------------
    Uses TIMSORT -- a hybrid of Merge Sort + Insertion Sort.
      - Detects already-sorted (or nearly sorted) runs in data.
      - Merges them using merge-sort logic.
      - Insertion sort (O(n^2) worst but fast cache behaviour) is used
        for small sub-arrays (size < 64).
    TIMSORT guarantees O(n log n) worst case AND O(n) best case.
    It is stable and uses O(n) auxiliary space.
    Almost always the best choice for general-purpose sorting in Python.
"""

import time
import random


# =====================================================
# Bubble Sort
# =====================================================
def bubble_sort(arr):
    """
    Compare adjacent elements and swap if out of order.
    After each pass, the largest unsorted element "bubbles" to its position.

    Optimisation: if no swap in a pass, the array is already sorted -> stop early.
    Best case: O(n) with the early-exit optimisation (already sorted input).
    """
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if not swapped:
            break    # early exit: already sorted
    return a


# =====================================================
# Merge Sort
# =====================================================
def merge_sort(arr):
    """Divide-and-conquer, guaranteed O(n log n), stable, O(n) space."""
    if len(arr) <= 1:
        return arr[:]
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result


# =====================================================
# Quick Sort (random pivot)
# =====================================================
def quick_sort(arr, lo=0, hi=None):
    """In-place quicksort with random pivot. Average O(n log n)."""
    a = arr[:] if hi is None else arr
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        rand_idx = random.randint(lo, hi)
        a[rand_idx], a[hi] = a[hi], a[rand_idx]
        pivot = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i+1], a[hi] = a[hi], a[i+1]
        p = i + 1
        quick_sort(a, lo, p-1)
        quick_sort(a, p+1, hi)
    return a


# =====================================================
# Python built-in sorted() (Timsort)
# =====================================================
def python_timsort(arr):
    """Python's built-in Timsort. Always the recommended choice."""
    return sorted(arr)


# =====================================================
# Count swaps / comparisons for bubble sort analysis
# =====================================================
def bubble_sort_count(arr):
    a = arr[:]
    n = len(a)
    comparisons = 0
    swaps       = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comparisons, swaps


# =====================================================
# Benchmark all four algorithms
# =====================================================
def benchmark(sizes=(100, 500, 1000)):
    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARK (average over 5 runs each)")
    print("=" * 70)
    algos = [
        ("Bubble Sort", bubble_sort),
        ("Merge Sort",  merge_sort),
        ("Quick Sort",  quick_sort),
        ("Python sort", python_timsort),
    ]

    for n in sizes:
        data = [random.randint(0, 10000) for _ in range(n)]
        print(f"\n  n = {n}")
        for name, fn in algos:
            times = []
            for _ in range(5):
                t0 = time.perf_counter()
                fn(data[:])
                times.append(time.perf_counter() - t0)
            avg_ms = sum(times) / len(times) * 1000
            print(f"    {name:<15}: {avg_ms:.4f} ms")


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90, 3, 47, 55]

    print("=" * 60)
    print(f"SORTING ALGORITHM COMPARISON  Input: {arr}")
    print("=" * 60)

    for name, fn in [
        ("Bubble Sort",  bubble_sort),
        ("Merge Sort",   merge_sort),
        ("Quick Sort",   quick_sort),
        ("Python sort",  python_timsort),
    ]:
        result = fn(arr[:])
        ok = "[OK]" if result == sorted(arr) else "[X]"
        print(f"  {name:<15}: {result}  {ok}")

    # ── Bubble sort detail ────────────────────────────
    print("\n" + "=" * 60)
    print("BUBBLE SORT DETAIL (comparisons and swaps):")
    print("=" * 60)
    cases = [
        ("Already sorted",  sorted(arr)),
        ("Reverse sorted",  sorted(arr, reverse=True)),
        ("Random",          arr),
    ]
    for label, a in cases:
        _, comps, swaps = bubble_sort_count(a)
        print(f"  {label:<20}: {comps} comparisons, {swaps} swaps")

    # ── Benchmark ─────────────────────────────────────
    benchmark(sizes=(200, 1000))

    # ── When to use each ─────────────────────────────
    print("\n" + "=" * 60)
    print("COMPLEXITY TABLE:")
    print("=" * 60)
    rows = [
        ("Bubble Sort",  "O(n)",      "O(n^2)",    "O(n^2)",    "O(1)",      "Yes", "Teaching / nearly-sorted tiny arrays"),
        ("Merge Sort",   "O(n log n)","O(n log n)","O(n log n)","O(n)",      "Yes", "Linked lists, external sort, need stability"),
        ("Quick Sort",   "O(n log n)","O(n log n)","O(n^2)",    "O(log n)",  "No",  "General in-memory sort, cache-friendly"),
        ("Python sort",  "O(n)",      "O(n log n)","O(n log n)","O(n)",      "Yes", "ALWAYS -- Timsort is the best default"),
    ]
    hdr = f"  {'Algorithm':<13} {'Best':^12} {'Avg':^12} {'Worst':^12} {'Space':^9} {'Stable':^7}"
    print(hdr)
    print("  " + "-" * 68)
    for r in rows:
        print(f"  {r[0]:<13} {r[1]:^12} {r[2]:^12} {r[3]:^12} {r[4]:^9} {r[5]:^7}")

    print("\n" + "=" * 60)
    print("WHEN TO USE EACH:")
    print("  Bubble Sort : AVOID for production. Use only for teaching.")
    print("  Merge Sort  : Best for linked lists (no random access needed).")
    print("                Required for stable sort on external/large data.")
    print("  Quick Sort  : Fast in-place sort. Use with random pivot.")
    print("                Preferred in C/C++ standard libraries.")
    print("  Python sort : ALWAYS prefer sorted() / list.sort().")
    print("                Timsort is highly optimised for real-world data.")
    print("=" * 60)
