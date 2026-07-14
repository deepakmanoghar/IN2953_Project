"""
Q5. Implement a MedianFinder class that supports:
      addNum(num)  - add a number to the data stream
      findMedian() - return the current median

    DESIGN: Two-Heap Approach
    -----------------------------------------------------------------------------
    We maintain two heaps that together hold all numbers seen so far:

      max_heap  (left half)  -> stores the SMALLER half of numbers
                               Python's heapq is a min-heap, so we negate
                               values to simulate a max-heap.

      min_heap  (right half) -> stores the LARGER half of numbers
                               Standard min-heap; heap[0] is the minimum.

    BALANCING RULE (invariant after every addNum):
      1. len(max_heap) == len(min_heap)        -> even total: median = avg of tops
      2. len(max_heap) == len(min_heap) + 1    -> odd total:  median = top of max_heap

    FINDING MEDIAN:
      Even count -> ( max_heap[0_negated] + min_heap[0] ) / 2
      Odd count  ->   max_heap[0_negated]   (max_heap always has the extra element)

    TIME COMPLEXITY:
    -----------------------------------------------------------------------------
      addNum   -> O(log n)  -- at most two heap push/pop operations
      findMedian -> O(1)   -- just read heap tops

    SPACE: O(n)
"""

import heapq


class MedianFinder:
    def __init__(self):
        # max_heap (left half): store negated values so Python min-heap acts as max-heap
        self.max_heap = []   # top = -max_heap[0]  (largest in left half)
        # min_heap (right half): standard min-heap
        self.min_heap = []   # top = min_heap[0]   (smallest in right half)

    # ===============================================
    # addNum -- O(log n)
    # ===============================================
    def addNum(self, num: int) -> None:
        """
        BALANCING LOGIC (step-by-step):
        ---------------------------------------------
        Step 1: Push num onto max_heap.
                (Always route new numbers through max_heap first so
                 the max_heap top is always <= min_heap top.)

        Step 2: Balance the tops.
                After step 1, max_heap's largest might exceed min_heap's smallest
                -> move max_heap's top to min_heap.

        Step 3: Re-balance sizes.
                If min_heap grows larger than max_heap, move min_heap's top back
                so max_heap is either equal or one larger.
        """
        # Step 1: Push to max_heap (negate for max-heap simulation)
        heapq.heappush(self.max_heap, -num)

        # Step 2: Ensure max_heap's max <= min_heap's min
        if self.min_heap and (-self.max_heap[0]) > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)

        # Step 3: Re-balance sizes (max_heap can be at most 1 larger)
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    # ===============================================
    # findMedian -- O(1)
    # ===============================================
    def findMedian(self) -> float:
        """
        Even count -> average of the two heap tops.
        Odd count  -> top of max_heap (the extra element lives there).
        """
        if len(self.max_heap) == len(self.min_heap):
            # Even number of elements
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0
        else:
            # Odd: max_heap has one extra element
            return float(-self.max_heap[0])

    def _state(self):
        """Debug helper: show current heap contents."""
        left  = sorted([-x for x in self.max_heap], reverse=True)
        right = sorted(self.min_heap)
        return f"max_heap(left)={left}  min_heap(right)={right}"


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("MedianFinder -- Two-Heap Implementation")
    print("=" * 60)

    mf = MedianFinder()
    stream = [5, 15, 1, 3, 8, 7, 2, 20, 10, 4]

    print(f"\n{'Num':>5} | {'Left (max-heap)':^22} | {'Right (min-heap)':^22} | Median")
    print("-" * 75)

    for num in stream:
        mf.addNum(num)
        left  = sorted([-x for x in mf.max_heap], reverse=True)
        right = sorted(mf.min_heap)
        median = mf.findMedian()
        print(f"  +{num:<3} | {str(left):<22} | {str(right):<22} | {median}")

    print("\n" + "=" * 60)
    print("BALANCING LOGIC RECAP:")
    print("  1. New number always enters via max_heap first.")
    print("  2. If max_heap's top > min_heap's top -> move it right.")
    print("  3. Size invariant: |max_heap| == |min_heap|  (even)")
    print("                     |max_heap| == |min_heap|+1 (odd)")
    print("  -> Median is always accessible in O(1) from heap tops.")
    print("=" * 60)

    # Quick correctness check
    print("\nQuick correctness verification:")
    mf2 = MedianFinder()
    nums2 = [2, 3, 4]
    for i, n in enumerate(nums2):
        mf2.addNum(n)
        s = sorted(nums2[:i+1])
        mid = len(s) // 2
        exp_med = (s[mid-1] + s[mid]) / 2 if len(s) % 2 == 0 else s[mid]
        got_med = mf2.findMedian()
        print(f"  After adding {s}: median={got_med}  expected={exp_med}  {'[OK]' if got_med == exp_med else '[X]'}")
