"""
Q3. Combination Sum: Find all combinations of [2, 3, 6, 7] that sum to 7.
    Elements can be reused. Trace through the backtracking for this example.

    COMBINATION SUM:
    ----------------
    * Each number in the candidates array can be used UNLIMITED times.
    * Combinations (not permutations) -- order does NOT matter.
      [2, 2, 3] and [3, 2, 2] are the same combination.
    * To avoid duplicates we only move forward in the candidates array
      (never go back to a previous index on the same path).

    BACKTRACKING TRACE for candidates=[2,3,6,7], target=7:
    --------------------------------------------------------
    start=0, remain=7, path=[]
      pick 2 -> remain=5, path=[2]
        pick 2 -> remain=3, path=[2,2]
          pick 2 -> remain=1, path=[2,2,2]
            pick 2 -> remain=-1 [X] (overshoot, prune)
            pick 3 -> remain=-2 [X]
          backtrack -> path=[2,2]
          pick 3 -> remain=0 [OK] -> FOUND [2,2,3]
          pick 6 -> remain=-3 [X]
        backtrack -> path=[2]
        pick 3 -> remain=2, path=[2,3]
          pick 3 -> remain=-1 [X]
          ...
        backtrack -> path=[2]
        pick 6 -> remain=-1 [X]
      backtrack -> path=[]
      pick 3 -> remain=4, path=[3]
        pick 3 -> remain=1, path=[3,3]
          pick 3 -> remain=-2 [X]
          pick 6 -> remain=-5 [X]
        backtrack -> path=[3]
        pick 6 -> remain=-2 [X]
      backtrack -> path=[]
      pick 6 -> remain=1, path=[6]
        pick 6 -> remain=-5 [X]
      backtrack -> path=[]
      pick 7 -> remain=0 [OK] -> FOUND [7]
    ---------------------------------
    Results: [[2, 2, 3], [7]]

    TIME  : O(n^(T/M))  where T=target, M=min(candidates)
    SPACE : O(T/M)      max recursion depth when using smallest element
"""


# =====================================================
# Core Combination Sum (with reuse allowed)
# =====================================================
def combination_sum(candidates, target):
    """
    Backtracking solution:
      - 'start'   : index in candidates; we never go left of start
                    to avoid duplicate combinations.
      - 'remain'  : how much more we need to reach the target.
      - 'path'    : current combination being built.

    Pruning: if remain < 0 we overshoot -> stop this branch.
    """
    candidates.sort()   # sort so we can prune early (remain < 0)
    result = []

    def backtrack(start, remain, path):
        # -- Base cases ---------------------------------------------
        if remain == 0:
            result.append(list(path))   # found a valid combination
            return
        if remain < 0:
            return                      # overshot -> prune this branch

        # -- Explore each candidate starting from 'start' -----------
        for i in range(start, len(candidates)):
            # Early termination: sorted array -> all further nums bigger
            if candidates[i] > remain:
                break

            # -- Choose ---------------------------------------------
            path.append(candidates[i])

            # Recurse with the SAME index i (reuse allowed)
            backtrack(i, remain - candidates[i], path)

            # -- Un-choose (backtrack) -------------------------------
            path.pop()

    backtrack(0, target, [])
    return result


# =====================================================
# Detailed step-by-step trace
# =====================================================
def combination_sum_trace(candidates, target):
    """Prints every decision point of the backtracking process."""
    candidates = sorted(candidates)
    result = []
    step   = [0]

    print(f"\n  candidates = {candidates}  |  target = {target}")
    print("  " + "-" * 54)

    def backtrack(start, remain, path, depth):
        indent = "    " * depth
        print(f"  {indent}call: start={start}, remain={remain}, "
              f"path={path}")

        if remain == 0:
            step[0] += 1
            result.append(list(path))
            print(f"  {indent}[OK]  Step {step[0]}: FOUND -> {path}")
            return
        if remain < 0:
            print(f"  {indent}[X]  Overshoot (remain={remain}) -> PRUNE")
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                print(f"  {indent}  [X] {candidates[i]} > remain={remain}"
                      f" -> prune rest")
                break

            print(f"  {indent}  +- pick {candidates[i]}")
            path.append(candidates[i])
            backtrack(i, remain - candidates[i], path, depth + 1)
            path.pop()
            print(f"  {indent}  +- backtrack, remove {candidates[i]}")

    backtrack(0, target, [], 0)
    return result


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    candidates = [2, 3, 6, 7]
    target     = 7

    # -- Full backtracking trace ------------------------------------
    print("=" * 60)
    print("  Combination Sum Trace  -  candidates=[2,3,6,7], target=7")
    print("=" * 60)
    traced = combination_sum_trace(candidates, target)

    # -- Clean result -----------------------------------------------
    print("\n" + "=" * 60)
    print("  Final Results")
    print("=" * 60)
    combos = combination_sum(candidates, target)
    print(f"\n  candidates = {candidates}")
    print(f"  target     = {target}")
    print(f"\n  Combinations that sum to {target}:")
    for i, c in enumerate(combos, 1):
        print(f"    {i}. {c}  (sum = {sum(c)})")

    # -- Additional test cases --------------------------------------
    print("\n" + "=" * 60)
    print("  Additional Test Cases")
    print("=" * 60)
    tests = [
        ([2, 3, 5], 8),
        ([2], 4),
        ([1, 2], 3),
    ]
    for cands, tgt in tests:
        res = combination_sum(cands, tgt)
        print(f"\n  candidates={cands}, target={tgt}")
        print(f"    -> {res}")

    # -- Key concepts -----------------------------------------------
    print("\n" + "=" * 60)
    print("  Key Backtracking Concepts")
    print("=" * 60)
    print("""
    1. REUSE ALLOWED: pass the same index i (not i+1) when recursing,
       so the same element can be chosen again on the next level.

    2. NO DUPLICATES: always move forward (start from index i),
       never go back -- this ensures [2,2,3] is found only once.

    3. PRUNING: sort candidates first.  When candidates[i] > remain,
       all subsequent candidates are even larger -> prune the rest.

    4. BACKTRACK: after exploring a branch, pop the last element to
       restore the path for the next candidate at this level.

    Time  Complexity : O(n ^ (T/M))
      T = target value, M = smallest candidate
      In the worst case (M=1) the tree has n^T nodes.

    Space Complexity : O(T/M)
      Maximum depth of the recursion stack.
    """)
