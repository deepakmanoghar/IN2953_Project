"""
Q4. Using Python's heapq, write a function to find the kth largest element
    in an unsorted array.

    WHY does a MIN-HEAP of size k work?
    -----------------------------------------------------------------------------
    We maintain a min-heap that holds exactly k elements.

    • The heap's minimum (heap[0]) is always the SMALLEST among the k elements
      currently stored.
    • When a new element is larger than heap[0], it displaces the current minimum
      -> only the k largest elements ever seen are kept.
    • After processing all n elements, the k-largest are in the heap and
      heap[0] is the kth largest overall.

    Intuition: "I only care about the top-k. The smallest of my top-k is what
    I'd discard first -- and after all elements are processed, that discard
    candidate IS the kth largest."

    TIME COMPLEXITY:
    -----------------------------------------------------------------------------
    • Build initial heap of k elements : O(k)
    • Process remaining (n-k) elements : O((n-k) log k)  [each push/pop = O(log k)]
    • Total                            : O(n log k)
    • Space                            : O(k)

    Compare to sorting: O(n log n) time -- heap approach is faster when k << n.
"""

import heapq


# ===============================================
# APPROACH 1 - Min-heap of fixed size k
# ===============================================
def kth_largest_min_heap(nums, k):
    """
    Maintain a min-heap of size k.
    After processing all elements, heap[0] is the kth largest.

    Time : O(n log k)
    Space: O(k)
    """
    min_heap = []

    for num in nums:
        heapq.heappush(min_heap, num)        # push current element
        if len(min_heap) > k:
            heapq.heappop(min_heap)          # evict the smallest -> keep only top-k

    return min_heap[0]   # smallest in the min-heap = kth largest overall


# ===============================================
# APPROACH 2 - heapq.nlargest  (for comparison)
# ===============================================
def kth_largest_nlargest(nums, k):
    """
    Python's built-in convenience function.
    Internally uses a heap; returns the k largest elements sorted descending.
    Time: O(n log k)  Space: O(k)
    """
    return heapq.nlargest(k, nums)[-1]   # last of top-k = kth largest


# ===============================================
# APPROACH 3 - Brute force sort (for baseline)
# ===============================================
def kth_largest_sort(nums, k):
    """Sorting baseline. Time: O(n log n)  Space: O(n)"""
    return sorted(nums, reverse=True)[k - 1]


# ---------------------------------------------
# Step-by-step visualiser (small example)
# ---------------------------------------------
def kth_largest_verbose(nums, k):
    """Same as Approach 1 but prints each step."""
    min_heap = []
    print(f"\n  Processing {nums}  (k={k})")
    print(f"  {'num':>5} | heap after push       | action")
    print(f"  {'-'*5}-+-{'-'*22}-+-{'-'*22}")

    for num in nums:
        heapq.heappush(min_heap, num)
        action = ""
        if len(min_heap) > k:
            evicted = heapq.heappop(min_heap)
            action = f"evicted {evicted} (too small)"
        print(f"  {num:>5} | {str(sorted(min_heap)):<22} | {action}")

    return min_heap[0]


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    test_cases = [
        ([3, 2, 1, 5, 6, 4],        2),   # expected 5
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), # expected 4
        ([7, 10, 4, 3, 20, 15],     3),   # expected 10
        ([1],                        1),   # expected 1
    ]

    print("=" * 60)
    print("kth Largest Element using Min-Heap of size k")
    print("=" * 60)

    for nums, k in test_cases:
        r1 = kth_largest_min_heap(nums, k)
        r2 = kth_largest_nlargest(nums, k)
        r3 = kth_largest_sort(nums, k)
        print(f"\n  nums={nums}, k={k}")
        print(f"    Min-heap approach : {r1}")
        print(f"    heapq.nlargest    : {r2}")
        print(f"    Sort baseline     : {r3}")
        print(f"    All match: {'[OK]' if r1 == r2 == r3 else '[X]'}")

    # Verbose walk-through for intuition
    print("\n" + "=" * 60)
    print("STEP-BY-STEP TRACE  (nums=[3,2,1,5,6,4], k=2)")
    print("=" * 60)
    result = kth_largest_verbose([3, 2, 1, 5, 6, 4], 2)
    print(f"\n  kth largest = {result}")

    print("\n" + "=" * 60)
    print("WHY MIN-HEAP OF SIZE k WORKS:")
    print("  • We keep only the k LARGEST elements seen so far.")
    print("  • heap[0] = the SMALLEST of those k -> first to be evicted.")
    print("  • A new element replaces heap[0] only if it is LARGER.")
    print("  • After all n elements: heap[0] = kth largest.")
    print("  Time: O(n log k)  vs  O(n log n) for sort.")
    print("=" * 60)
