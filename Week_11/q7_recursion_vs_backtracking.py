"""
Q7. Explain the difference between recursion and backtracking.
    When does a recursive problem become a backtracking problem?

    RECURSION:
    ----------
    A function that calls ITSELF to solve a smaller sub-problem.
    It breaks the problem into smaller pieces until a base case is reached.
    Each sub-problem is typically INDEPENDENT of the others.

    Key traits:
      * Solves sub-problems in a fixed, top-down manner.
      * Each recursive call produces a result that is used by the caller.
      * Does NOT "undo" or revisit past decisions.
      * Examples: factorial, Fibonacci, merge sort, binary search.

    BACKTRACKING:
    -------------
    A SPECIAL FORM of recursion that:
      1. Builds a solution incrementally (step by step).
      2. ABANDONS a path as soon as it detects the path CANNOT lead
         to a valid solution (pruning).
      3. UNDOES the last choice (backtracks) and tries the next option.

    Key traits:
      * State is mutated before recursing and RESTORED after.
      * Explores a decision tree where some branches are pruned early.
      * Used when the solution space is large and many paths are invalid.
      * Examples: N-Queens, Sudoku, combination sum, word search.

    WHEN does recursion become backtracking?
    ----------------------------------------
    A recursive problem becomes a backtracking problem when:
      1. You need to EXPLORE MULTIPLE CHOICES at each step.
      2. Not all choices are valid -- you must CHECK CONSTRAINTS.
      3. An invalid choice must be UNDONE before trying the next one.
      4. You are searching for ONE or ALL solutions in a large space.

    COMPARISON TABLE:
    -----------------
    Feature               Recursion        Backtracking
    -------------------------------------------------------------
    Sub-problem type      independent      builds shared state
    State mutation        none (or simple) yes (undo on return)
    Pruning               no               yes (abandon early)
    Decision tree         linear/binary    n-ary (many branches)
    Goal                  compute a value  find valid arrangement(s)
    Examples              factorial, fib   N-Queens, Sudoku, subsets
"""

import time


# =====================================================
# PART A - Pure recursion examples
# =====================================================

def factorial(n):
    """Classic recursion: no state to undo, one call path."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n, memo={}):
    """Recursion with memoisation: still no backtracking."""
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


def binary_search(arr, target, lo, hi):
    """Divide-and-conquer recursion: eliminates half the space."""
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, hi)
    else:
        return binary_search(arr, target, lo, mid - 1)


# =====================================================
# PART B - Backtracking examples
# =====================================================

def subsets_backtrack(nums):
    """
    Backtracking: at each step include OR exclude the current element.
    'current' is mutated and RESTORED -> this is backtracking.
    """
    result  = []
    def bt(index, current):
        if index == len(nums):
            result.append(list(current)); return
        current.append(nums[index]);  bt(index + 1, current)  # include
        current.pop();                bt(index + 1, current)  # exclude <- backtrack
    bt(0, [])
    return result


def n_queens_count(n):
    """
    Backtracking: place a queen, check constraints, undo if invalid.
    The 'board' state is mutated and restored -> backtracking.
    """
    count = [0]
    cols  = set(); diag1 = set(); diag2 = set()

    def bt(row):
        if row == n:
            count[0] += 1; return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue
            cols.add(col); diag1.add(row-col); diag2.add(row+col)   # choose
            bt(row + 1)
            cols.remove(col); diag1.remove(row-col); diag2.remove(row+col)  # undo
    bt(0)
    return count[0]


# =====================================================
# PART C - Side-by-side comparison runner
# =====================================================

def run_comparison():
    """Demonstrates the structural difference between the two paradigms."""

    print("=" * 60)
    print("  PART A -- Pure Recursion")
    print("=" * 60)

    print("\n  1. Factorial (no state mutation, no undo)")
    for n in [0, 1, 5, 10]:
        print(f"     factorial({n:2d}) = {factorial(n)}")

    print("\n  2. Fibonacci with memoisation (no undo, cached sub-results)")
    fibs = [fibonacci(n, {}) for n in range(10)]
    print(f"     fib(0..9) = {fibs}")

    print("\n  3. Binary Search (divide-and-conquer, no state to undo)")
    arr = list(range(0, 20, 2))   # [0, 2, 4, ..., 18]
    target = 12
    idx = binary_search(arr, target, 0, len(arr) - 1)
    print(f"     arr    = {arr}")
    print(f"     target = {target}  ->  index {idx}  (value={arr[idx]})")

    print("\n\n" + "=" * 60)
    print("  PART B -- Backtracking")
    print("=" * 60)

    print("\n  4. Subsets (include/exclude with undo via pop())")
    subs = subsets_backtrack([1, 2, 3])
    print(f"     subsets([1,2,3]) = {subs}")
    print(f"     Total: {len(subs)} = 2^3")

    print("\n  5. N-Queens (place queen, check constraints, undo)")
    for n in range(1, 9):
        count = n_queens_count(n)
        print(f"     n={n}  ->  {count:3d} solution(s)")

    print("\n\n" + "=" * 60)
    print("  PART C -- When Recursion Becomes Backtracking")
    print("=" * 60)
    print("""
  Ask these four questions:

    Q1. Do I make a CHOICE at each step?
        If YES -> you need a decision tree -> consider backtracking.

    Q2. Can a choice be INVALID before reaching the end?
        If YES -> you need to prune and backtrack.

    Q3. Do I need to UNDO a choice to try the next option?
        If YES -> you need backtracking (undo = backtrack).

    Q4. Am I searching for ALL valid solutions, not just computing?
        If YES -> backtracking is typically the right approach.

  -------------------------------------------------------------
  TRANSFORMATION EXAMPLE:

    Recursive: count subsets of size k (compute a number)
      -> No need to track which elements are chosen.
      -> Pure recursion / combinatorics formula.

    Backtracking: enumerate all subsets of size k (find all sets)
      -> Must track the current subset.
      -> Undo each choice to try the next.
      -> Backtracking is required.

  -------------------------------------------------------------
  TEMPLATE for ANY backtracking problem:

    def backtrack(state):
        if is_solution(state):          # base case
            record(state)
            return

        for choice in get_choices(state):
            if is_valid(state, choice): # constraint check / pruning
                make_choice(state, choice)      # choose
                backtrack(state)                # recurse
                undo_choice(state, choice)      # BACKTRACK (undo)

  -------------------------------------------------------------
  SUMMARY TABLE:

    Aspect          Pure Recursion        Backtracking
    --------------- -------------------- ----------------------
    Sub-problem     Independent           Shared mutable state
    State change    None / return val     Mutate -> recurse -> undo
    Pruning         No                    Yes (early termination)
    Decision tree   1 or 2 branches       n branches per level
    Use case        Compute a value       Find valid arrangement(s)
    Complexity      Often O(n) or O(logn) Often O(k^n) or O(n!)
  """)


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    run_comparison()
