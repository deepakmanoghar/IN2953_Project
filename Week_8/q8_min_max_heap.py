"""
Q8. Explain the difference between a min-heap and a max-heap.
    Why does Python's heapq only provide min-heap, and how do you simulate a max-heap?

    -----------------------------------------------------------------------------
    MIN-HEAP vs MAX-HEAP
    -----------------------------------------------------------------------------
    Both are complete binary trees satisfying the HEAP PROPERTY:

      Min-Heap:  parent <= children   ->  SMALLEST element is always at the root
      Max-Heap:  parent >= children   ->  LARGEST  element is always at the root

    Internal structure (array-backed):
      For a node at index i:
        left child  = 2i + 1
        right child = 2i + 2
        parent      = (i - 1) // 2

    Common operations (same complexity for both):
      peek   -> O(1)       (read root without removing)
      push   -> O(log n)   (heapify up)
      pop    -> O(log n)   (remove root, heapify down)
      build  -> O(n)       (heapify all nodes bottom-up)

    -----------------------------------------------------------------------------
    WHY Python's heapq IS ONLY A MIN-HEAP
    -----------------------------------------------------------------------------
    Python's heapq module implements a min-heap because:
      1. Simplicity & UNIX philosophy -- one correct implementation is better
         than duplicating code for two variants.
      2. A max-heap is trivially derived from a min-heap using negation.
      3. Most standard algorithms (Dijkstra, priority queues, scheduling)
         naturally express "process smallest first".
      4. Providing only one type avoids confusion and API bloat.

    -----------------------------------------------------------------------------
    HOW TO SIMULATE A MAX-HEAP IN PYTHON
    -----------------------------------------------------------------------------
    Technique: NEGATE all values before pushing; negate again when popping.

      push max_heap: heapq.heappush(h, -value)
      pop  max_heap: -heapq.heappop(h)
      peek max_heap: -h[0]

    This works because: if we negate all values, the min-heap orders them such
    that the most-negative (= originally largest) sits at the root.

    For complex objects: use a wrapper class with __lt__ reversed, or store
    (-priority, data) tuples so the tuple comparison handles ordering.
"""

import heapq


# ===============================================
# Demo 1: Pure Min-Heap
# ===============================================
def demo_min_heap(values):
    """Standard heapq usage -- smallest element always at top."""
    h = []
    for v in values:
        heapq.heappush(h, v)

    print("  Min-Heap extraction order (smallest first):")
    result = []
    while h:
        result.append(heapq.heappop(h))
    print(" ", result)
    return result


# ===============================================
# Demo 2: Simulated Max-Heap via negation
# ===============================================
def demo_max_heap(values):
    """
    Simulate max-heap by pushing negated values.
    The min-heap on negated values = max-heap on original values.
    """
    h = []
    for v in values:
        heapq.heappush(h, -v)   # <- negate before push

    print("  Max-Heap extraction order (largest first):")
    result = []
    while h:
        result.append(-heapq.heappop(h))   # <- negate after pop
    print(" ", result)
    return result


# ===============================================
# Demo 3: Max-Heap with (priority, task) tuples
# ===============================================
def demo_max_heap_tuples():
    """
    Real-world pattern: use (-priority, item) so the item with the
    HIGHEST priority is always popped first.
    """
    tasks = [
        (3, "Low priority task"),
        (10, "Critical task"),
        (7, "Medium priority task"),
        (1, "Very low priority"),
        (10, "Another critical task"),
    ]

    h = []
    for priority, task in tasks:
        heapq.heappush(h, (-priority, task))   # negate priority

    print("  Task processing order (highest priority first):")
    while h:
        neg_pri, task = heapq.heappop(h)
        print(f"    Priority {-neg_pri:>2}: {task}")


# ===============================================
# Demo 4: Custom class with reversed __lt__
# ===============================================
class MaxHeapItem:
    """
    Wrapper that reverses comparison so Python's min-heap behaves as a max-heap.
    Useful when negation is not straightforward (e.g., non-numeric keys).
    """
    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val   # reversed comparison!

    def __repr__(self):
        return str(self.val)


def demo_max_heap_class(values):
    h = []
    for v in values:
        heapq.heappush(h, MaxHeapItem(v))

    print("  Max-Heap (class wrapper) extraction order:")
    result = []
    while h:
        result.append(heapq.heappop(h).val)
    print(" ", result)
    return result


# ---------------------------------------------
# Driver
# ---------------------------------------------
if __name__ == "__main__":
    values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    print("=" * 60)
    print("Min-Heap vs Max-Heap in Python")
    print("=" * 60)
    print(f"\nInput values: {values}\n")

    # -- Min-Heap ----------------------------------
    print("-- MIN-HEAP (heapq default) -----------------")
    min_result = demo_min_heap(values)

    # -- Max-Heap (negation) -----------------------
    print("\n-- MAX-HEAP (negation trick) -----------------")
    max_result = demo_max_heap(values)

    # -- Max-Heap (class) --------------------------
    print("\n-- MAX-HEAP (reversed __lt__ class) ---------")
    class_result = demo_max_heap_class(values)

    print(f"\n  Min sorted  : {sorted(values)}")
    print(f"  Max sorted  : {sorted(values, reverse=True)}")
    print(f"  Min matches : {'[OK]' if min_result   == sorted(values)              else '[X]'}")
    print(f"  Max matches : {'[OK]' if max_result   == sorted(values, reverse=True) else '[X]'}")
    print(f"  Class matches: {'[OK]' if class_result == sorted(values, reverse=True) else '[X]'}")

    # -- Priority queue demo -----------------------
    print("\n-- PRIORITY QUEUE WITH TUPLES ---------------")
    demo_max_heap_tuples()

    # -- Conceptual summary ------------------------
    print("\n" + "=" * 60)
    print("SUMMARY TABLE:")
    print(f"  {'Property':<30} {'Min-Heap':<15} {'Max-Heap'}")
    print(f"  {'-'*30} {'-'*15} {'-'*15}")
    print(f"  {'Root element':<30} {'smallest':<15} largest")
    print(f"  {'Heap property':<30} {'parent <= child':<15} parent >= child")
    print(f"  {'Python heapq support':<30} {'Native [OK]':<15} Via negation")
    print(f"  {'peek (root)':<30} {'h[0]':<15} -h[0]")
    print(f"  {'push value v':<30} {'heappush(h,v)':<15} heappush(h,-v)")
    print(f"  {'pop minimum/maximum':<30} {'-heappop(h)':<15} -heappop(h)")
    print(f"  {'Time complexity (all ops)':<30} {'O(log n)':<15} O(log n)")
    print(f"  {'Build from n elements':<30} {'O(n)':<15} O(n)")
    print("=" * 60)

    print("\nWHY PYTHON ONLY PROVIDES MIN-HEAP:")
    print("  1. Max-heap = min-heap on negated values -> trivially derived.")
    print("  2. Avoids API duplication and maintains simplicity.")
    print("  3. Standard algorithms (Dijkstra, A*) use min-heap natively.")
    print("  4. Negate once: cost is O(1) per operation, zero overhead.")
