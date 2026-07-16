"""
Q7. 0/1 Knapsack:
    Items have weights=[2,3,4,5] and values=[3,4,5,6], capacity=5.
    Find the maximum value. Show the DP table.

    0/1 KNAPSACK PROBLEM:
    ---------------------
    Given n items each with a weight and a value, and a knapsack of
    capacity W, find the subset of items that maximises total value
    without exceeding total weight.

    '0/1' means each item can be taken AT MOST ONCE
    (unlike unbounded knapsack where items can be reused).

    RECURRENCE:
    -----------
    dp[i][w] = max value using first i items with weight limit w

    if weight[i-1] > w:                 (item i too heavy to include)
        dp[i][w] = dp[i-1][w]

    else:                               (item i can fit)
        dp[i][w] = max(dp[i-1][w],                  <- exclude item i
                       dp[i-1][w - weight[i-1]] + value[i-1])  <- include

    BASE CASES:
    -----------
    dp[0][w] = 0  for all w   (no items -> value = 0)
    dp[i][0] = 0  for all i   (no capacity -> value = 0)

    COMPLETE DP TABLE:
    ------------------
    weights=[2,3,4,5], values=[3,4,5,6], capacity=5

    Item  | weight | value |  w=0  w=1  w=2  w=3  w=4  w=5
    ----------------------------------------------------------
    none  |   --   |   --  |   0    0    0    0    0    0
    Item1 |    2   |    3  |   0    0    3    3    3    3
    Item2 |    3   |    4  |   0    0    3    4    4    7
    Item3 |    4   |    5  |   0    0    3    4    5    7
    Item4 |    5   |    6  |   0    0    3    4    5    7
                                                        ^
                                               dp[4][5] = 7

    Answer: max value = 7 (take Item1 weight=2,value=3 + Item2 weight=3,value=4)

    TIME  : O(n x W)   where n=items, W=capacity
    SPACE : O(n x W)   full table, O(W) with rolling 1D array
"""


# =====================================================
# Approach 1 -- Full 2D DP table
# =====================================================
def knapsack_2d(weights, values, capacity):
    """
    Builds the full (n+1) x (capacity+1) dp table.
    dp[i][w] = max value with first i items and weight limit w.
    """
    n  = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Exclude item i
            dp[i][w] = dp[i - 1][w]
            # Include item i (only if it fits)
            if weights[i - 1] <= w:
                include = dp[i - 1][w - weights[i - 1]] + values[i - 1]
                dp[i][w] = max(dp[i][w], include)

    return dp[n][capacity], dp


# =====================================================
# Approach 2 -- 1D space-optimised
# =====================================================
def knapsack_1d(weights, values, capacity):
    """
    Rolling 1D dp array. Process weights in REVERSE to avoid reusing
    the same item twice (key for 0/1 knapsack correctness).
    """
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        # MUST iterate right-to-left to prevent item reuse
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w],
                        dp[w - weights[i]] + values[i])

    return dp[capacity]


# =====================================================
# Reconstruction: which items were selected?
# =====================================================
def knapsack_with_items(weights, values, capacity, names=None):
    """Returns (max_value, list_of_selected_item_indices)."""
    n  = len(weights)
    if names is None:
        names = [f"Item{i+1}" for i in range(n)]

    _, dp = knapsack_2d(weights, values, capacity)

    # Backtrack to find selected items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:   # item i was included
            selected.append(i - 1)      # 0-indexed
            w -= weights[i - 1]

    selected.reverse()
    return dp[n][capacity], selected


# =====================================================
# Table printer
# =====================================================
def print_dp_table(weights, values, capacity, dp, names=None):
    """Prints the DP table with item labels and weight columns."""
    n = len(weights)
    if names is None:
        names = [f"Item{i+1}" for i in range(n)]

    # Header
    header = f"  {'Item':<8}  {'wt':>4}  {'val':>4}  "
    for w in range(capacity + 1):
        header += f"  w={w}"
    print(header)
    print("  " + "-" * (22 + 5 * (capacity + 1)))

    # Base row
    base_row = f"  {'none':<8}  {'--':>4}  {'--':>4}  "
    for v in dp[0]:
        base_row += f"    {v}"
    print(base_row)

    # Item rows
    for i in range(1, n + 1):
        row = f"  {names[i-1]:<8}  {weights[i-1]:>4}  {values[i-1]:>4}  "
        for v in dp[i]:
            row += f"    {v}"
        print(row)


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    weights  = [2, 3, 4, 5]
    values   = [3, 4, 5, 6]
    capacity = 5
    names    = ['Item1', 'Item2', 'Item3', 'Item4']

    # -- Full DP table ----------------------------------------------
    print("=" * 65)
    print("  0/1 Knapsack -- Full DP Table")
    print("=" * 65)
    max_val, dp = knapsack_2d(weights, values, capacity)
    print(f"\n  weights  = {weights}")
    print(f"  values   = {values}")
    print(f"  capacity = {capacity}\n")
    print_dp_table(weights, values, capacity, dp, names)

    # -- Cell-by-cell fill trace ------------------------------------
    print("\n" + "=" * 65)
    print("  Cell-by-Cell Fill Trace  (key decisions)")
    print("=" * 65)
    n = len(weights)
    print()
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            excl = dp[i-1][w]
            if weights[i-1] <= w:
                incl = dp[i-1][w - weights[i-1]] + values[i-1]
                chosen = "include" if incl > excl else "exclude"
                print(f"  dp[{i}][{w}]: excl={excl}, "
                      f"incl={incl} -> {chosen} -> {dp[i][w]}")
            else:
                print(f"  dp[{i}][{w}]: wt{weights[i-1]}>{w} (too heavy) "
                      f"-> exclude -> {dp[i][w]}")

    # -- Result and selected items ----------------------------------
    print("\n" + "=" * 65)
    print("  Result with Selected Items")
    print("=" * 65)
    best, selected = knapsack_with_items(weights, values, capacity, names)
    print(f"\n  Maximum value : {best}")
    print(f"  Selected items:")
    for idx in selected:
        print(f"    {names[idx]}: weight={weights[idx]}, value={values[idx]}")
    tw = sum(weights[i] for i in selected)
    tv = sum(values[i]  for i in selected)
    print(f"  Total weight  : {tw} (capacity={capacity})")
    print(f"  Total value   : {tv}")

    # -- Space-optimised verification -------------------------------
    r1d = knapsack_1d(weights, values, capacity)
    print(f"\n  1D optimised answer: {r1d}  (matches: {r1d == best})")

    # -- Different capacity examples --------------------------------
    print("\n" + "=" * 65)
    print("  Results for Various Capacities")
    print("=" * 65)
    print(f"\n  weights={weights}, values={values}")
    print(f"  {'Capacity':>10}   {'Max Value':>10}   {'Items selected':}")
    print("  " + "-" * 50)
    for cap in range(0, 11):
        val, sel = knapsack_with_items(weights, values, cap, names)
        item_str = ', '.join(names[i] for i in sel) if sel else 'none'
        print(f"  {cap:>10}   {val:>10}   {item_str}")

    # -- Complexity summary -----------------------------------------
    print("\n" + "=" * 65)
    print("  Complexity Summary")
    print("=" * 65)
    print("""
    Time Complexity : O(n x W)
      n = number of items, W = knapsack capacity.
      We fill an (n+1) x (W+1) table, one cell at a time.

    Space Complexity:
      Full 2D table : O(n x W)   (needed for reconstruction)
      1D optimised  : O(W)       (only the length; no item backtrack)

    KEY RULE for 1D array (0/1 knapsack):
      Iterate capacity RIGHT-TO-LEFT (from W down to weight[i]).
      This ensures each item is counted at most once, because when
      we update dp[w], dp[w - weight[i]] still holds the value from
      the PREVIOUS item (not the current one).

    Contrast with Unbounded Knapsack:
      Iterate capacity LEFT-TO-RIGHT to allow reuse of the same item.

    Optimal Substructure:
      dp[i][w] = best value using items {1..i} with capacity w,
      and it only depends on dp[i-1][...] (the previous item row).

    Overlapping Subproblems:
      dp[i-1][w - weight[i]] is reused across many different i and w.
    """)
