"""
Q1. Implement Fibonacci three ways:
    (a) Naive recursion
    (b) Memoization with @lru_cache
    (c) Bottom-up tabulation
    Compare the time complexity of each.

    FIBONACCI SEQUENCE:
    -------------------
    F(0) = 0,  F(1) = 1
    F(n) = F(n-1) + F(n-2)   for n >= 2

    Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...

    THE CORE PROBLEM WITH NAIVE RECURSION:
    ---------------------------------------
    Computing F(5) causes repeated work:
                      F(5)
                   /        \\
               F(4)          F(3)
              /    \\         /   \\
           F(3)   F(2)    F(2)  F(1)
           /  \\   /  \\    /  \\
         F(2) F(1) F(1) F(0) F(1) F(0)
         /  \\
       F(1) F(0)

    F(3) is computed TWICE, F(2) THREE times -> exponential blowup!

    COMPLEXITY COMPARISON:
    ----------------------
    Approach          Time         Space
    -------------------------------------
    Naive recursion   O(2^n)       O(n)    recursion depth
    Memoization       O(n)         O(n)    cache + call stack
    Tabulation        O(n)         O(n)    dp array
    Space-optimised   O(n)         O(1)    only two variables
"""

import time
from functools import lru_cache
import sys

sys.setrecursionlimit(10000)


# =====================================================
# (a) Naive Recursion  --  O(2^n)
# =====================================================
def fib_naive(n):
    """
    Direct recursive definition.
    Recomputes the same sub-problems exponentially many times.
    DO NOT use for n > ~35; it becomes extremely slow.
    """
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# =====================================================
# (b) Memoization with @lru_cache  --  O(n) time, O(n) space
# =====================================================
@lru_cache(maxsize=None)
def fib_memo(n):
    """
    Top-down dynamic programming.
    @lru_cache stores results of every (n,) call automatically.
    Each unique sub-problem is solved exactly once.
    """
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


# Manual dictionary memoization (same idea without @lru_cache)
def fib_memo_manual(n, cache=None):
    """Same as fib_memo but using an explicit dict for teaching clarity."""
    if cache is None:
        cache = {}
    if n <= 1:
        return n
    if n in cache:
        return cache[n]
    cache[n] = fib_memo_manual(n - 1, cache) + fib_memo_manual(n - 2, cache)
    return cache[n]


# =====================================================
# (c) Bottom-up Tabulation  --  O(n) time, O(n) space
# =====================================================
def fib_tabulation(n):
    """
    Bottom-up dynamic programming.
    Build a dp table from the smallest sub-problems up to n.
    No recursion stack needed.

    dp[i] = F(i)
    dp[0] = 0
    dp[1] = 1
    dp[i] = dp[i-1] + dp[i-2]
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# =====================================================
# (d) Space-optimised tabulation  --  O(n) time, O(1) space
# =====================================================
def fib_optimised(n):
    """
    We only need the LAST TWO values at any point.
    Replace the entire dp array with two variables.
    """
    if n <= 1:
        return n
    prev2, prev1 = 0, 1          # F(0), F(1)
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    return prev1


# =====================================================
# Recursion call counter (to visualise O(2^n))
# =====================================================
def fib_count_calls(n):
    """Returns (result, num_calls) to show exponential growth."""
    calls = [0]
    def _fib(n):
        calls[0] += 1
        if n <= 1:
            return n
        return _fib(n - 1) + _fib(n - 2)
    result = _fib(n)
    return result, calls[0]


# =====================================================
# Timing helper
# =====================================================
def time_it(func, *args, repeat=3):
    """Returns the minimum elapsed time in microseconds."""
    best = float('inf')
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = func(*args)
        t1 = time.perf_counter()
        best = min(best, (t1 - t0) * 1e6)
    return result, best


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":

    # -- First 15 Fibonacci numbers ---------------------------------
    print("=" * 60)
    print("  Fibonacci Sequence  (first 15 values)")
    print("=" * 60)
    seq = [fib_tabulation(i) for i in range(15)]
    print(f"\n  {seq}\n")

    # -- Exponential call count (why naive is slow) -----------------
    print("=" * 60)
    print("  Naive Recursion -- Call Count Growth")
    print("=" * 60)
    print(f"\n  {'n':>4}   {'F(n)':>10}   {'Calls':>12}   {'Ratio':>8}")
    print("  " + "-" * 42)
    prev_calls = 1
    for n in [5, 10, 15, 20, 25, 30]:
        val, calls = fib_count_calls(n)
        ratio = calls / prev_calls if prev_calls else 1
        print(f"  {n:>4}   {val:>10}   {calls:>12,}   {ratio:>7.2f}x")
        prev_calls = calls

    # -- dp table trace for tabulation ------------------------------
    print("\n" + "=" * 60)
    print("  Tabulation DP Table  --  n = 10")
    print("=" * 60)
    n = 10
    dp = [0] * (n + 1)
    dp[0] = 0
    if n >= 1:
        dp[1] = 1
    print(f"\n  {'i':>4}   {'dp[i]':>8}   note")
    print("  " + "-" * 35)
    print(f"  {0:>4}   {dp[0]:>8}   base case")
    if n >= 1:
        print(f"  {1:>4}   {dp[1]:>8}   base case")
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        print(f"  {i:>4}   {dp[i]:>8}   dp[{i-1}] + dp[{i-2}] = "
              f"{dp[i-1]} + {dp[i-2]}")

    # -- Timing comparison ------------------------------------------
    print("\n" + "=" * 60)
    print("  Timing Comparison")
    print("=" * 60)
    print(f"\n  {'Approach':<25} {'n':>4}   {'Result':>12}   {'Time (us)':>10}")
    print("  " + "-" * 58)

    fib_memo.cache_clear()

    for n in [20, 30]:
        r1, t1 = time_it(fib_naive, n)
        fib_memo.cache_clear()
        r2, t2 = time_it(fib_memo, n)
        r3, t3 = time_it(fib_tabulation, n)
        r4, t4 = time_it(fib_optimised, n)
        print(f"\n  n = {n}")
        print(f"  {'(a) Naive recursion':<25} {n:>4}   {r1:>12}   {t1:>10.2f}")
        print(f"  {'(b) Memoization':<25} {n:>4}   {r2:>12}   {t2:>10.2f}")
        print(f"  {'(c) Tabulation':<25} {n:>4}   {r3:>12}   {t3:>10.2f}")
        print(f"  {'(d) Space-optimised':<25} {n:>4}   {r4:>12}   {t4:>10.2f}")

    # Large n (naive would hang, so skip it)
    for n in [100, 500]:
        fib_memo.cache_clear()
        r2, t2 = time_it(fib_memo, n)
        r3, t3 = time_it(fib_tabulation, n)
        r4, t4 = time_it(fib_optimised, n)
        print(f"\n  n = {n}  (naive omitted -- too slow)")
        print(f"  {'(b) Memoization':<25} {n:>4}   {str(r2)[:12]:>12}   {t2:>10.2f}")
        print(f"  {'(c) Tabulation':<25} {n:>4}   {str(r3)[:12]:>12}   {t3:>10.2f}")
        print(f"  {'(d) Space-optimised':<25} {n:>4}   {str(r4)[:12]:>12}   {t4:>10.2f}")

    # -- Complexity summary -----------------------------------------
    print("\n" + "=" * 60)
    print("  Complexity Summary")
    print("=" * 60)
    print("""
    (a) Naive Recursion
        Time  : O(2^n)  -- each call branches into two, with no caching
        Space : O(n)    -- maximum recursion depth is n
        Note  : Unusable for n > 40 on modern hardware

    (b) Memoization (@lru_cache / dict)
        Time  : O(n)    -- each unique sub-problem solved exactly once
        Space : O(n)    -- cache stores n entries + O(n) call stack
        Note  : Top-down; easy to write, same logic as naive

    (c) Bottom-up Tabulation
        Time  : O(n)    -- single pass through indices 2..n
        Space : O(n)    -- dp array of size n+1
        Note  : No recursion stack; cache-friendly iteration

    (d) Space-optimised Tabulation
        Time  : O(n)    -- same loop as tabulation
        Space : O(1)    -- only two variables (prev2, prev1)
        Note  : Best overall; only trade-off is losing dp history

    KEY INSIGHT -- What makes this Dynamic Programming?
      1. OVERLAPPING SUBPROBLEMS: F(n-2) is needed by both F(n) and F(n-1).
      2. OPTIMAL SUBSTRUCTURE:   F(n) is fully determined by F(n-1) + F(n-2).
      Both properties must hold for DP to apply.
    """)
