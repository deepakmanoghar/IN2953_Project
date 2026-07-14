"""
Q6. Given k sorted lists, merge them into one sorted list using a heap.

    ALGORITHM:
    -----------------------------------------------------------------------------
    1. Build a min-heap of size k, seeded with the FIRST element of each list
       (along with the list index and element index for navigation).
    2. Repeatedly:
       a. Pop the minimum element from the heap -> append to result.
       b. If the list that produced this element has more elements, push
          the NEXT element from that same list onto the heap.
    3. Repeat until the heap is empty.

    WHY IT WORKS:
      The heap always contains exactly one candidate from each non-exhausted list.
      Because each list is already sorted, the next candidate from a list is
      always larger than the last element taken from it.
      -> The heap invariant guarantees we always extract the global minimum.

    TIME COMPLEXITY:
    -----------------------------------------------------------------------------
      Let n = total elements across all k lists.
      • Initialising the heap  : O(k log k)
      • Each element is pushed/popped from the heap exactly once: O(log k) each
      • Total for n elements   : O(n log k)
      -- OVERALL: O(n log k) --

    SPACE COMPLEXITY: O(k) for the heap  +  O(n) for the result list.

    Compare:
      Naive concatenate + sort -> O(n log n)   (worse when k << n)
      Heap approach            -> O(n log k)   (better because log k <= log n)
"""

import heapq


# ===============================================
# merge_k_sorted_lists -- O(n log k)
# ===============================================
def merge_k_sorted_lists(lists):
    """
    Merge k sorted lists into a single sorted list.

    Args:
        lists: list[list[int]] -- k sorted lists

    Returns:
        list[int] -- merged sorted list
    """
    result = []
    # Min-heap entries: (value, list_index, element_index)
    min_heap = []

    # Seed heap with the first element of each non-empty list
    for i, lst in enumerate(lists):
        if lst:                                   # skip empty lists
            heapq.heappush(min_heap, (lst[0], i, 0))

    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)

        # If there is a next element in the same list, push it
        next_idx = elem_idx + 1
        if next_idx < len(lists[list_idx]):
            next_val = lists[list_idx][next_idx]
            heapq.heappush(min_heap, (next_val, list_idx, next_idx))

    return result


# ---------------------------------------------
# Verbose version: shows heap state at each step
# ---------------------------------------------
def merge_k_sorted_lists_verbose(lists):
    """Same algorithm but prints heap state at each extraction."""
    result = []
    min_heap = []

    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))

    print(f"\n  {'Step':>4} | {'Extracted':>9} | {'From list':>9} | Heap after")
    print(f"  {'-'*4}-+-{'-'*9}-+-{'-'*9}-+-{'-'*30}")
    step = 0

    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)
        step += 1

        next_idx = elem_idx + 1
        if next_idx < len(lists[list_idx]):
            next_val = lists[list_idx][next_idx]
            heapq.heappush(min_heap, (next_val, list_idx, next_idx))

        heap_display = [v for v, _, _ in sorted(min_heap)]
        print(f"  {step:>4} | {val:>9} | list[{list_idx}]    | {heap_display}")

    return result


# ---------------------------------------------
# Naive O(n log n) reference for verification
# ---------------------------------------------
def merge_naive(lists):
    all_vals = []
    for lst in lists:
        all_vals.extend(lst)
    return sorted(all_vals)


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Merge k Sorted Lists using a Min-Heap")
    print("=" * 60)

    test_cases = [
        {
            "lists": [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
            "label": "k=3 lists of 3 elements each"
        },
        {
            "lists": [[1, 2, 3], [4, 5, 6]],
            "label": "k=2 lists"
        },
        {
            "lists": [[1], [0]],
            "label": "k=2 single-element lists"
        },
        {
            "lists": [[5], [1, 3, 4], [2, 6]],
            "label": "k=3 unequal-length lists"
        },
    ]

    for tc in test_cases:
        lists  = tc["lists"]
        label  = tc["label"]
        result = merge_k_sorted_lists(lists)
        naive  = merge_naive(lists)
        ok     = result == naive
        n_total = sum(len(l) for l in lists)
        k = len(lists)
        print(f"\n  {label}")
        print(f"  Input : {lists}")
        print(f"  Output: {result}")
        print(f"  Correct: {'[OK]' if ok else '[X]'}   n={n_total}, k={k}")

    # -- Verbose trace -----------------------------
    print("\n" + "=" * 60)
    print("STEP-BY-STEP TRACE  lists=[[1,4,7],[2,5,8],[3,6,9]]")
    print("=" * 60)
    merged = merge_k_sorted_lists_verbose([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
    print(f"\n  Final merged list: {merged}")

    print("\n" + "=" * 60)
    print("TIME COMPLEXITY ANALYSIS:")
    print("  n = total elements across all k lists")
    print("  k = number of lists")
    print()
    print("  Init heap        : O(k log k)")
    print("  n push/pop ops   : O(n log k)  <- each op touches heap of size k")
    print("  ---------------------------------")
    print("  TOTAL            : O(n log k)")
    print()
    print("  vs. naive sort   : O(n log n)  -- worse when k << n")
    print("  Space            : O(k) heap + O(n) result")
    print("=" * 60)
