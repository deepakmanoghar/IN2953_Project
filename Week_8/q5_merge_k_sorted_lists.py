"""
Q5. Merge K sorted lists into one sorted list using a Min-Heap.

    PROBLEM:
    ─────────────────────────────────────────────────────────────────────────────
    Given k sorted lists (each already sorted in ascending order), produce a
    single merged, sorted list.

    NAIVE APPROACH (for comparison):
    ─────────────────────────────────────────────────────────────────────────────
    Concatenate all lists then sort → O(N log N)  where N = total elements.
    This ignores the fact that the lists are already sorted.

    HEAP APPROACH (optimal):
    ─────────────────────────────────────────────────────────────────────────────
    Use a min-heap of size k.  At any moment the heap holds one "current
    candidate" from each list — whichever is the global minimum pops out next.

    Algorithm:
      1. Push (value, list_index, element_index) for the first element of
         every non-empty list into the heap.                    → O(k log k)
      2. While the heap is non-empty:
           a. Pop the smallest triple (val, li, ei).            → O(log k)
           b. Append val to the result.
           c. If list li has a next element, push it.           → O(log k)
      3. Return result.

    TIME  : O(N log k)   — N pops × O(log k) per pop
    SPACE : O(k)         — heap holds at most one node per list
"""

import heapq


# ═══════════════════════════════════════════════
# APPROACH 1 – Min-heap (optimal)
# ═══════════════════════════════════════════════
def merge_k_sorted_heap(lists):
    """
    Merge k sorted lists using a min-heap.

    Each heap entry: (value, list_index, element_index)
    The tuple comparison ensures the smallest value is always popped first.

    Time : O(N log k)   N = total elements across all lists
    Space: O(k)         heap size bounded by number of lists
    """
    result = []
    min_heap = []

    # Step 1: seed the heap with the first element of each list
    for li, lst in enumerate(lists):
        if lst:                                    # skip empty lists
            heapq.heappush(min_heap, (lst[0], li, 0))

    # Step 2: repeatedly extract the minimum
    while min_heap:
        val, li, ei = heapq.heappop(min_heap)
        result.append(val)

        next_ei = ei + 1
        if next_ei < len(lists[li]):               # list li has more elements
            heapq.heappush(min_heap, (lists[li][next_ei], li, next_ei))

    return result


# ═══════════════════════════════════════════════
# APPROACH 2 – Naive (concatenate + sort)
# ═══════════════════════════════════════════════
def merge_k_sorted_naive(lists):
    """
    Concatenate all lists then sort.
    Time : O(N log N)   wastes the pre-sorted property
    Space: O(N)
    """
    combined = []
    for lst in lists:
        combined.extend(lst)
    return sorted(combined)


# ─────────────────────────────────────────────
# Step-by-step verbose trace
# ─────────────────────────────────────────────
def merge_k_sorted_verbose(lists):
    """Same as heap approach but prints each heap operation."""
    result   = []
    min_heap = []
    step     = 0

    print("\n  Initial seeding:")
    for li, lst in enumerate(lists):
        if lst:
            entry = (lst[0], li, 0)
            heapq.heappush(min_heap, entry)
            print(f"    push {lst[0]} from list {li}")

    print(f"\n  {'Step':<5} {'Popped':<8} {'From list':<12} {'Result so far'}")
    print("  " + "─" * 55)

    while min_heap:
        val, li, ei = heapq.heappop(min_heap)
        result.append(val)
        step += 1
        print(f"  {step:<5} {val:<8} list[{li}]       {result}")

        next_ei = ei + 1
        if next_ei < len(lists[li]):
            heapq.heappush(min_heap, (lists[li][next_ei], li, next_ei))

    return result


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        {
            "lists"   : [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
            "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "desc"    : "3 lists, evenly interleaved",
        },
        {
            "lists"   : [[1, 3, 5, 7], [2, 4, 6, 8], [0, 9, 10, 11]],
            "expected": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "desc"    : "3 lists, varying ranges",
        },
        {
            "lists"   : [[1], [0]],
            "expected": [0, 1],
            "desc"    : "2 single-element lists",
        },
        {
            "lists"   : [[], [1], [0, 2]],
            "expected": [0, 1, 2],
            "desc"    : "includes an empty list",
        },
        {
            "lists"   : [[1, 2, 3]],
            "expected": [1, 2, 3],
            "desc"    : "single list (trivial)",
        },
    ]

    print("=" * 60)
    print("Merge K Sorted Lists — Min-Heap vs Naive")
    print("=" * 60)

    all_passed = True
    for tc in test_cases:
        h = merge_k_sorted_heap(tc["lists"])
        n = merge_k_sorted_naive(tc["lists"])
        ok = h == n == tc["expected"]
        if not ok:
            all_passed = False
        status = "✓" if ok else "✗"
        print(f"\n  [{status}] {tc['desc']}")
        print(f"      Input    : {tc['lists']}")
        print(f"      Heap     : {h}")
        print(f"      Naive    : {n}")
        print(f"      Expected : {tc['expected']}")

    print("\n" + "=" * 60)
    print("STEP-BY-STEP TRACE  (3 lists: [1,4,7], [2,5,8], [3,6,9])")
    print("=" * 60)
    merge_k_sorted_verbose([[1, 4, 7], [2, 5, 8], [3, 6, 9]])

    print("\n" + "=" * 60)
    print("COMPLEXITY COMPARISON:")
    print("  Heap approach : O(N log k) time,  O(k) space")
    print("  Naive sort    : O(N log N) time,  O(N) space")
    print("  → Heap is significantly faster when k << N")
    print("=" * 60)

    print(f"\nAll tests passed: {'✓' if all_passed else '✗'}")
