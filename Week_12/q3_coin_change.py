"""
Q3. Coin Change: Given coins=[1,5,10,25] and amount=37,
    find the minimum number of coins needed.
    Draw the DP table and trace the solution.

    COIN CHANGE (Minimum Coins):
    ----------------------------
    Classic DP problem: find the fewest coins that sum to 'amount'.
    Each coin can be used UNLIMITED times (unbounded knapsack variant).

    RECURRENCE:
    -----------
    dp[a] = min coins needed to make amount a
    dp[0] = 0                       (0 coins to make 0)
    dp[a] = min(dp[a - c] + 1)      for each coin c <= a
          = INF if no combination reaches a

    GREEDY FAILS for some inputs!
    Example: coins=[1,3,4], amount=6
      Greedy: 4+1+1 = 3 coins
      Optimal: 3+3   = 2 coins  <-- DP finds this

    TRACE for coins=[1,5,10,25], amount=37:
    ----------------------------------------
    dp[0] = 0
    dp[1] = dp[0]+1 (using 1) = 1
    dp[5] = dp[0]+1 (using 5) = 1
    dp[10]= dp[0]+1 (using 10)= 1
    dp[25]= dp[0]+1 (using 25)= 1
    dp[35]= dp[10]+1(using 25)= 2  (10+25)
    dp[36]= dp[35]+1(using 1) = 3  (1+10+25)
    dp[37]= dp[36]+1(using 1) = 4  (1+1+10+25) or
            dp[12]+1(using 25)= 3  (12=10+1+1, total=10+1+1+25)
            Actually dp[12]=3 -> 3+1=4
            dp[27]=dp[2]+1(25)=dp[2]+1 -> dp[2]=2 -> 3
            dp[37]: try 25->dp[12]=3->4; try 10->dp[27]=3->4;
                    try 5->dp[32]=? ; try 1->dp[36]=3->4
                    all give 4  -> answer = 4 coins: 25+10+1+1

    SOLUTION RECONSTRUCTION:
    Track which coin was used at each amount, then backtrack.

    TIME  : O(amount x len(coins))
    SPACE : O(amount)
"""

INF = float('inf')


# =====================================================
# Core DP solver
# =====================================================
def coin_change(coins, amount):
    """
    Returns minimum number of coins to make 'amount'.
    Returns -1 if it is impossible.
    """
    dp   = [INF] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] != INF:
                dp[a] = min(dp[a], dp[a - c] + 1)

    return dp[amount] if dp[amount] != INF else -1


# =====================================================
# Solver that also reconstructs the actual coins used
# =====================================================
def coin_change_with_path(coins, amount):
    """
    Returns (min_coins, list_of_coins_used).
    Uses a 'used' array to track which coin was chosen at each amount.
    """
    dp   = [INF]  * (amount + 1)
    used = [-1]   * (amount + 1)   # used[a] = coin chosen at amount a
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in sorted(coins):
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a]   = dp[a - c] + 1
                used[a] = c

    if dp[amount] == INF:
        return -1, []

    # Reconstruct solution by backtracking through 'used'
    path = []
    curr = amount
    while curr > 0:
        coin = used[curr]
        path.append(coin)
        curr -= coin

    return dp[amount], sorted(path, reverse=True)


# =====================================================
# Full DP table printer (for small amounts)
# =====================================================
def print_dp_table(coins, amount):
    """Prints the complete dp table row by row."""
    dp   = [INF]  * (amount + 1)
    used = [-1]   * (amount + 1)
    dp[0] = 0

    print(f"\n  coins  = {coins}")
    print(f"  amount = {amount}")
    print(f"\n  {'Amount':>8}   {'dp[a]':>8}   {'best coin':>10}   "
          f"{'came from':>12}")
    print("  " + "-" * 50)
    print(f"  {0:>8}   {dp[0]:>8}   {'---':>10}   {'base case':>12}")

    for a in range(1, amount + 1):
        for c in sorted(coins):
            if c <= a and dp[a - c] != INF and dp[a - c] + 1 < dp[a]:
                dp[a]   = dp[a - c] + 1
                used[a] = c
        if dp[a] == INF:
            print(f"  {a:>8}   {'INF':>8}   {'---':>10}   {'impossible':>12}")
        else:
            came_from = a - used[a] if used[a] != -1 else 0
            print(f"  {a:>8}   {dp[a]:>8}   {used[a]:>10}   "
                  f"{'dp[' + str(came_from) + ']+1':>12}")

    return dp, used


# =====================================================
# Greedy failure demonstration
# =====================================================
def greedy_coins(coins, amount):
    """Greedy: always pick the largest coin <= remaining amount."""
    coins_sorted = sorted(coins, reverse=True)
    count  = 0
    used   = []
    remain = amount
    for c in coins_sorted:
        while remain >= c:
            remain -= c
            count  += 1
            used.append(c)
    return count if remain == 0 else -1, used


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    coins  = [1, 5, 10, 25]
    amount = 37

    # -- Full DP table ----------------------------------------------
    print("=" * 60)
    print("  Coin Change -- Full DP Table")
    print("=" * 60)
    dp_arr, used_arr = print_dp_table(coins, amount)

    # -- Solution with reconstruction -------------------------------
    print("\n" + "=" * 60)
    print("  Solution with Coin Reconstruction")
    print("=" * 60)
    min_coins, path = coin_change_with_path(coins, amount)
    print(f"\n  coins  = {coins}")
    print(f"  amount = {amount}")
    print(f"\n  Minimum coins needed : {min_coins}")
    print(f"  Coins used           : {path}  (sum={sum(path)})")

    # Backtrack trace
    print(f"\n  Backtrack reconstruction:")
    curr = amount
    steps = []
    while curr > 0:
        c = used_arr[curr]
        steps.append(f"    amount={curr} -> used coin {c} -> came from dp[{curr-c}]={dp_arr[curr-c]}")
        curr -= c
    for s in steps:
        print(s)

    # -- Greedy vs DP comparison ------------------------------------
    print("\n" + "=" * 60)
    print("  Greedy vs DP  --  where Greedy FAILS")
    print("=" * 60)
    test_cases = [
        ([1, 5, 10, 25], 37),
        ([1, 3, 4],      6),    # greedy gives 3, DP gives 2
        ([2],            3),    # impossible
        ([1, 5, 10, 25], 30),
    ]
    for cns, amt in test_cases:
        g_count, g_path = greedy_coins(cns, amt)
        d_count, d_path = coin_change_with_path(cns, amt)
        flag = "<-- Greedy SUBOPTIMAL!" if g_count != d_count and g_count != -1 else ""
        print(f"\n  coins={cns}, amount={amt}")
        print(f"    Greedy : {g_count} coins -> {g_path}")
        print(f"    DP     : {d_count} coins -> {d_path}  {flag}")

    # -- Compact table for amount 0-15 -----------------------------
    print("\n" + "=" * 60)
    print("  Compact DP Table  --  coins=[1,5,10,25],  amount 0..15")
    print("=" * 60)
    print(f"\n  {'a':>4}", end="")
    for a in range(16):
        print(f"  {a:>3}", end="")
    print()
    print("  " + "-" * 70)
    dp_row = [INF] * 16
    dp_row[0] = 0
    for a in range(1, 16):
        for c in [1, 5, 10, 25]:
            if c <= a and dp_row[a - c] + 1 < dp_row[a]:
                dp_row[a] = dp_row[a - c] + 1
    print(f"  {'dp':>4}", end="")
    for v in dp_row:
        print(f"  {v:>3}", end="")
    print()

    # -- Complexity summary -----------------------------------------
    print("\n\n" + "=" * 60)
    print("  Complexity Summary")
    print("=" * 60)
    print("""
    Time Complexity  : O(amount x len(coins))
      For each of the (amount+1) sub-problems, we try every coin.
      With coins=[1,5,10,25] and amount=37 -> 37 x 4 = 148 operations.

    Space Complexity : O(amount)
      dp array of size (amount+1).
      used array of same size for reconstruction.

    Why DP and NOT greedy?
      Greedy (largest coin first) fails when smaller denominations
      combine more efficiently. Example: coins=[1,3,4], amount=6:
        Greedy: 4+1+1 = 3 coins
        DP opt: 3+3   = 2 coins
      DP considers ALL combinations, not just the locally best choice.

    Optimal Substructure:
      min_coins(amount) = 1 + min(min_coins(amount - c) for c in coins)
      The optimal solution for 'amount' uses an optimal solution
      for 'amount - c' for the chosen coin c.
    """)
