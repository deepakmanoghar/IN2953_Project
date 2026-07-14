"""
Q6. Implement counting sort for an array of integers in range [0, k].
    What are its limitations compared to comparison-based sorts?

    COUNTING SORT:
    --------------
    A NON-COMPARISON sort that works by counting the frequency of each
    distinct value, then using those counts to place elements directly
    at their correct positions.

    STEPS:
    ------
    1. Find the max value k (or accept k as parameter).
    2. Create a COUNT array of size k+1, initialised to 0.
    3. Count occurrences: count[arr[i]] += 1 for each element.
    4. Compute prefix sums: count[i] += count[i-1].
       Now count[i] = number of elements <= i = final position of last i.
    5. Build output array (traverse input in REVERSE for stability):
       output[ count[arr[i]] - 1 ] = arr[i]; count[arr[i]] -= 1.

    TIME  : O(n + k)  -- n for array traversal, k for count array work
    SPACE : O(n + k)  -- count array of size k+1, output array of size n

    LIMITATIONS vs COMPARISON-BASED SORTS:
    ----------------------------------------
    1. Only works for NON-NEGATIVE INTEGERS (or mappable to them).
       Cannot sort strings, floats, or custom objects without adaptation.
    2. Space is O(k) -- if k >> n, it wastes huge amounts of memory.
       E.g., array [0, 999999] needs a count array of 1,000,000 entries.
    3. Not suitable when the range k is very large compared to n.
       Rule of thumb: use counting sort only when k = O(n).
    4. Comparison-based sorts (merge, quick, timsort) work on ANY
       comparable data type without knowing the range in advance.
"""


# =====================================================
# Counting sort (stable, handles range [0, k])
# =====================================================
def counting_sort(arr, k=None):
    """
    Sort arr (non-negative integers) using counting sort.

    Args:
        arr : list[int] -- input array (values in [0, k])
        k   : int | None -- max value; auto-detected if None

    Returns:
        list[int] -- sorted array
    """
    if not arr:
        return []

    if k is None:
        k = max(arr)

    # Step 1: count frequencies
    count = [0] * (k + 1)
    for val in arr:
        count[val] += 1

    # Step 2: prefix sums (gives final position of each value)
    for i in range(1, k + 1):
        count[i] += count[i - 1]

    # Step 3: build output (reverse traversal for stability)
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        val            = arr[i]
        pos            = count[val] - 1
        output[pos]    = val
        count[val]    -= 1

    return output


# =====================================================
# Simplified version (no stability required)
# =====================================================
def counting_sort_simple(arr, k=None):
    """
    Simpler counting sort that doesn't need the prefix-sum trick.
    NOT stable (doesn't preserve relative order of equal elements).
    """
    if not arr:
        return []
    if k is None:
        k = max(arr)

    count = [0] * (k + 1)
    for val in arr:
        count[val] += 1

    result = []
    for val, freq in enumerate(count):
        result.extend([val] * freq)
    return result


# =====================================================
# Extended: handle negative integers by shifting
# =====================================================
def counting_sort_with_negatives(arr):
    """
    Handle negative integers by shifting all values up by |min_val|,
    sorting, then shifting back.
    """
    if not arr:
        return []
    min_val = min(arr)
    shifted = [x - min_val for x in arr]   # shift to [0, max-min]
    sorted_shifted = counting_sort(shifted)
    return [x + min_val for x in sorted_shifted]


# =====================================================
# Verbose step-by-step trace
# =====================================================
def counting_sort_verbose(arr):
    """Same algorithm with printed intermediate states."""
    if not arr:
        return []

    k = max(arr)
    print(f"\n  Input : {arr}")
    print(f"  k (max value) = {k}")

    # Step 1: count
    count = [0] * (k + 1)
    for val in arr:
        count[val] += 1
    print(f"\n  Step 1 - Count array:")
    print(f"    index : {list(range(k+1))}")
    print(f"    count : {count}")

    # Step 2: prefix sums
    for i in range(1, k + 1):
        count[i] += count[i - 1]
    print(f"\n  Step 2 - Prefix sum (position markers):")
    print(f"    index : {list(range(k+1))}")
    print(f"    count : {count}")
    print(f"    (count[i] = how many elements are <= i)")

    # Step 3: build output
    output = [0] * len(arr)
    print(f"\n  Step 3 - Place elements (reverse order for stability):")
    for i in range(len(arr) - 1, -1, -1):
        val         = arr[i]
        pos         = count[val] - 1
        output[pos] = val
        count[val] -= 1
        print(f"    arr[{i}]={val} -> place at output[{pos}], count[{val}] now {count[val]}")

    print(f"\n  Output: {output}")
    return output


# =====================================================
# Radix sort (uses counting sort as subroutine, handles large k)
# =====================================================
def radix_sort(arr):
    """
    Sort non-negative integers using Radix Sort (LSD).
    Uses counting sort on each digit position.
    Time: O(d * (n + 10))  where d = number of digits
    Avoids the large-k limitation of counting sort alone.
    """
    if not arr:
        return []
    max_val = max(arr)
    exp     = 1   # 1, 10, 100, ...
    a       = arr[:]

    while max_val // exp > 0:
        # Counting sort by the digit at position 'exp'
        output = [0] * len(a)
        count  = [0] * 10   # digits 0-9

        for val in a:
            digit = (val // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i-1]

        for i in range(len(a) - 1, -1, -1):
            digit        = (a[i] // exp) % 10
            pos          = count[digit] - 1
            output[pos]  = a[i]
            count[digit] -= 1

        a   = output
        exp *= 10

    return a


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    arr = [4, 2, 2, 8, 3, 3, 1, 7, 0, 5]

    print("=" * 60)
    print(f"COUNTING SORT  Input: {arr}")
    print("=" * 60)

    r1 = counting_sort(arr)
    r2 = counting_sort_simple(arr)
    exp = sorted(arr)
    print(f"\n  Stable counting sort : {r1}  {'[OK]' if r1 == exp else '[X]'}")
    print(f"  Simple counting sort : {r2}  {'[OK]' if r2 == exp else '[X]'}")

    # ── Verbose trace ─────────────────────────────────
    print("\n" + "=" * 60)
    print("VERBOSE TRACE:")
    print("=" * 60)
    counting_sort_verbose([3, 1, 4, 1, 5, 9, 2, 6])

    # ── Negative integers ─────────────────────────────
    print("\n" + "=" * 60)
    print("NEGATIVE INTEGER EXTENSION (shift trick):")
    print("=" * 60)
    neg_arr = [-3, -1, 0, -2, 2, 1]
    r3 = counting_sort_with_negatives(neg_arr)
    print(f"  Input : {neg_arr}")
    print(f"  Output: {r3}  {'[OK]' if r3 == sorted(neg_arr) else '[X]'}")

    # ── Radix sort for large k ────────────────────────
    print("\n" + "=" * 60)
    print("RADIX SORT (overcomes large-k limitation of counting sort):")
    print("=" * 60)
    big = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"  Input : {big}")
    print(f"  Output: {radix_sort(big)}  {'[OK]' if radix_sort(big) == sorted(big) else '[X]'}")

    # ── Limitation demo ───────────────────────────────
    print("\n" + "=" * 60)
    print("LIMITATIONS OF COUNTING SORT:")
    print("=" * 60)
    print("  1. INTEGERS ONLY.")
    print("     Cannot sort ['banana','apple','cherry'] without conversion.")
    print()
    print("  2. RANGE k MUST BE SMALL relative to n.")
    arr_small_n_large_k = [0, 1000000]
    print(f"     Array {arr_small_n_large_k}: n=2 but k=1,000,000")
    print(f"     -> count array needs 1,000,001 slots for just 2 elements!")
    print(f"     -> Space = O(k) = O(1,000,000)  vs  O(n) = O(2) for merge sort")
    print()
    print("  3. NO NEGATIVES (without shift trick).")
    print()
    print("  4. COMPARISON-BASED sorts (merge, quick, timsort) work on")
    print("     ANY comparable type: strings, floats, custom objects.")
    print()
    print("  WHEN TO USE COUNTING SORT:")
    print("    n elements, values in [0, k], and k = O(n).")
    print("    E.g., sorting exam scores 0-100, sorting ages 0-150.")
    print("    Time O(n+k) beats O(n log n) when k is small.")
    print("=" * 60)
