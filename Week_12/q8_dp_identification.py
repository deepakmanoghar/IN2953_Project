"""
Q8. Identify which problems can be solved with DP and explain why:
    (a) Finding shortest path in a graph
    (b) Generating all permutations
    (c) Minimum edit distance between two strings
    (d) Sorting an array

    DP APPLICABILITY CRITERIA:
    --------------------------
    A problem is suitable for Dynamic Programming if and only if it
    has BOTH of these properties:

    1. OPTIMAL SUBSTRUCTURE:
       The optimal solution to the problem contains optimal solutions
       to its sub-problems. In other words, you can build the global
       optimum from local optima.

    2. OVERLAPPING SUBPROBLEMS:
       The same sub-problems are solved multiple times during the
       recursion. Caching (memoization) or tabulation avoids recomputation.

    If a problem has only one property, DP may not be the right tool:
      - Optimal substructure ONLY   -> Greedy may work (e.g., MST)
      - Overlapping subproblems ONLY -> Memoization helps, but may not
                                        give optimal results
"""

from functools import lru_cache
import heapq


# =====================================================
# (a) Shortest Path -- YES, DP applies
# =====================================================

def dijkstra(graph, start):
    """
    Dijkstra's algorithm: finds shortest paths from 'start' to all nodes.
    Uses optimal substructure: shortest path to v goes through the
    shortest path to some neighbour u of v.

    dist[v] = min(dist[u] + edge(u, v)) for all u adjacent to v
    """
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq   = [(0, start)]   # (distance, node)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))

    return dist


def bellman_ford(graph_edges, nodes, start):
    """
    Bellman-Ford: classic DP for shortest paths (handles negative weights).
    dp[v] after k iterations = shortest path using at most k edges.

    Recurrence: dp[v] = min(dp[u] + w(u,v)) for all edges (u,v,w)
    """
    dist = {node: float('inf') for node in nodes}
    dist[start] = 0

    # Relax all edges |nodes|-1 times (DP iterations)
    for _ in range(len(nodes) - 1):
        for u, v, w in graph_edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return dist


def floyd_warshall(n, edges):
    """
    Floyd-Warshall: all-pairs shortest paths -- classic O(n^3) DP.
    dp[i][j][k] = shortest path from i to j using only nodes {1..k}
    Simplified: dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])
    """
    INF = float('inf')
    dp  = [[INF] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 0
    for u, v, w in edges:
        dp[u][v] = w

    for k in range(n):                   # intermediate node
        for i in range(n):
            for j in range(n):
                if dp[i][k] + dp[k][j] < dp[i][j]:
                    dp[i][j] = dp[i][k] + dp[k][j]
    return dp


# =====================================================
# (b) Generating all permutations -- NO, DP does NOT apply
# =====================================================

def all_permutations(nums):
    """
    Backtracking: generates ALL permutations.
    This is ENUMERATION, not optimisation or counting.
    There is NO re-use of sub-problem results because each arrangement
    is unique and cannot be built from cached smaller arrangements.
    """
    result = []
    used   = [False] * len(nums)

    def bt(current):
        if len(current) == len(nums):
            result.append(list(current))
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                bt(current)
                current.pop()
                used[i] = False

    bt([])
    return result


def count_permutations_dp(n):
    """
    COUNTING permutations CAN use DP: n! = n * (n-1)!
    This is essentially the factorial recurrence.
    But enumerating all of them requires backtracking, not DP.
    """
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = i * dp[i - 1]
    return dp[n]


# =====================================================
# (c) Minimum Edit Distance -- YES, DP applies
# =====================================================

def edit_distance(s1, s2):
    """
    Levenshtein distance: minimum insertions, deletions, substitutions
    to transform s1 into s2.

    dp[i][j] = edit distance between s1[0..i-1] and s2[0..j-1]

    if s1[i-1] == s2[j-1]:
        dp[i][j] = dp[i-1][j-1]               (no op needed)
    else:
        dp[i][j] = 1 + min(dp[i-1][j],        (delete from s1)
                           dp[i][j-1],        (insert into s1)
                           dp[i-1][j-1])      (substitute)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i    # delete all chars of s1
    for j in range(n + 1):
        dp[0][j] = j    # insert all chars of s2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    # delete
                                   dp[i][j - 1],    # insert
                                   dp[i - 1][j - 1])# substitute

    return dp[m][n], dp


def edit_distance_trace(s1, s2):
    """Prints the full edit distance DP table."""
    dist, dp = edit_distance(s1, s2)
    m, n     = len(s1), len(s2)

    header = f"  {'':>4}"
    for ch in ('""' + s2):
        header += f"  {ch:>3}"
    print(header)
    print("  " + "-" * (6 + 4 * (n + 2)))

    for i, row in enumerate(dp):
        label = '""' if i == 0 else s1[i - 1]
        print(f"  {label:>4}  " + "  ".join(f"{v:>3}" for v in row))

    return dist


# =====================================================
# (d) Sorting -- NO, DP does NOT apply
# =====================================================

def merge_sort(arr):
    """
    Merge sort uses divide-and-conquer.
    Sub-problems are DISJOINT (left half and right half never overlap).
    Since sub-problems DON'T overlap, there's nothing to cache.
    DP requires overlapping sub-problems -- sorting has none.
    """
    if len(arr) <= 1:
        return arr
    mid  = len(arr) // 2
    left = merge_sort(arr[:mid])
    rght = merge_sort(arr[mid:])
    return merge(left, rght)


def merge(l, r):
    result = []
    i = j  = 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            result.append(l[i]); i += 1
        else:
            result.append(r[j]); j += 1
    result.extend(l[i:])
    result.extend(r[j:])
    return result


# =====================================================
# Analysis summary
# =====================================================
def print_analysis():
    print("""
  PROBLEM ANALYSIS
  ================================================================

  (a) SHORTEST PATH IN A GRAPH  ->  YES, DP applies
  -----------------------------------------------------------------
  Optimal Substructure:   YES
    The shortest path from A to C going through B consists of:
      - shortest path from A to B, PLUS
      - shortest path from B to C.
    This is known as Bellman's Principle of Optimality.

  Overlapping Subproblems: YES
    Finding shortest path to node v requires the shortest path to
    multiple intermediate nodes, which are shared across many paths.

  Examples:
    - Bellman-Ford: dp[v][k] = shortest path using at most k edges
    - Dijkstra:     greedy + DP (relaxation)
    - Floyd-Warshall: all-pairs O(n^3) DP

  EXCEPTION: Finding ANY path (not shortest) does not need DP.
  Also: shortest path in a DAG can be solved with a single
  topological sort -- a simpler DP variant.

  ================================================================

  (b) GENERATING ALL PERMUTATIONS  ->  NO, DP does NOT apply
  -----------------------------------------------------------------
  Optimal Substructure:   NO
    There is no "optimal" permutation; we need ALL of them.
    We cannot build a complete permutation from cached partial ones
    in any meaningful reusable way.

  Overlapping Subproblems: PARTIAL
    Counting permutations has the recurrence P(n) = n * P(n-1),
    which is just n! and CAN be computed with DP.
    But ENUMERATING all permutations requires backtracking because
    each arrangement is unique and cannot be composed from cached ones.

  Correct approach: BACKTRACKING
    Generate each permutation by choosing an unused element at
    each position and undoing that choice to try the next.
    Time: O(n! x n), Space: O(n)

  ================================================================

  (c) MINIMUM EDIT DISTANCE  ->  YES, DP applies
  -----------------------------------------------------------------
  Optimal Substructure:   YES
    edit_distance(s1[0..i], s2[0..j]) =
      0                                   if s1[i]==s2[j]
      1 + min(edit_dist(s1[0..i-1], s2[0..j]),    delete
              edit_dist(s1[0..i], s2[0..j-1]),    insert
              edit_dist(s1[0..i-1], s2[0..j-1]))  substitute
    Each subproblem is an optimal sub-edit.

  Overlapping Subproblems: YES
    Subproblem edit_dist(i-1, j-1) is referenced by multiple cells
    in the dp table.

  Algorithm: Levenshtein distance -- O(m x n) time, O(m x n) space
  Applications: spell checkers, DNA alignment, git diff, NLP.

  ================================================================

  (d) SORTING AN ARRAY  ->  NO, DP does NOT apply
  -----------------------------------------------------------------
  Optimal Substructure:   PARTIAL (for some sorts)
    Merge sort: sort(left) + sort(right) + merge.
    The sub-problems are optimal but they are DISJOINT.

  Overlapping Subproblems: NO
    At each level of merge sort, the left and right halves are
    DIFFERENT sub-arrays -- they never overlap.
    Quicksort, heapsort, insertion sort -- similarly no overlap.

  Correct approaches: Comparison-based sorts (O(n log n)),
    counting sort O(n+k), radix sort O(nk).
    None requires caching sub-problem solutions.

  RELATED problem that IS DP: Longest Increasing Subsequence
    is related to sorting but IS a DP problem because it has
    overlapping subproblems (dp[i] reused by multiple dp[j]).

  ================================================================

  SUMMARY TABLE:
  -----------------------------------------------------------------
  Problem                   Optimal    Overlapping   DP?
                            Subst.     Subproblems
  -----------------------------------------------------------------
  (a) Shortest Path         YES        YES           YES
  (b) All Permutations      NO         NO            NO (backtrack)
  (c) Edit Distance         YES        YES           YES
  (d) Sorting an Array      PARTIAL    NO            NO (D&C/greedy)
  -----------------------------------------------------------------

  Other DP problems (for reference):
    - Fibonacci, Climbing Stairs, Coin Change, House Robber
    - LCS, LIS, 0/1 Knapsack
    - Matrix Chain Multiplication, Palindrome Partitioning
    - Subset Sum, Partition Equal Subset Sum
    - Unique Paths (grid DP), Minimum Path Sum
  """)


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":

    # -- (a) Shortest path examples ---------------------------------
    print("=" * 65)
    print("  (a) Shortest Path in a Graph  --  Dijkstra + Floyd-Warshall")
    print("=" * 65)

    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('D', 3), ('C', 1)],
        'C': [('B', 1), ('D', 5)],
        'D': []
    }
    dist = dijkstra(graph, 'A')
    print(f"\n  Dijkstra from 'A': {dist}")

    # Floyd-Warshall on a 4-node graph
    n4 = 4
    edges4 = [(0,1,3),(0,2,6),(1,2,2),(1,3,1),(2,3,4)]
    fw = floyd_warshall(n4, edges4)
    print(f"\n  Floyd-Warshall all-pairs distances (4 nodes):")
    for i in range(n4):
        print(f"    from node {i}: {fw[i]}")

    # -- (b) Permutations -------------------------------------------
    print("\n" + "=" * 65)
    print("  (b) All Permutations  --  Backtracking (NOT DP)")
    print("=" * 65)
    perms = all_permutations([1, 2, 3])
    print(f"\n  all_permutations([1,2,3]) -> {len(perms)} permutations")
    print(f"  First 3: {perms[:3]}")
    print(f"  Counting with DP: 3! = {count_permutations_dp(3)}")

    # -- (c) Edit distance ------------------------------------------
    print("\n" + "=" * 65)
    print("  (c) Edit Distance  --  Classic DP")
    print("=" * 65)
    s1, s2 = "kitten", "sitting"
    dist_val, _ = edit_distance(s1, s2)
    print(f"\n  edit_distance('{s1}', '{s2}') = {dist_val}")
    print(f"\n  Edit Distance DP Table for 'horse' vs 'ros':")
    d = edit_distance_trace("horse", "ros")
    print(f"\n  edit_distance('horse', 'ros') = {d}")

    # -- (d) Sorting ------------------------------------------------
    print("\n" + "=" * 65)
    print("  (d) Sorting  --  Divide-and-Conquer (NOT DP)")
    print("=" * 65)
    arr = [5, 2, 8, 1, 9, 3]
    sorted_arr = merge_sort(arr)
    print(f"\n  merge_sort({arr}) = {sorted_arr}")
    print("  (No sub-problem overlap -> DP not applicable)")

    # -- Full analysis ----------------------------------------------
    print("\n" + "=" * 65)
    print("  DP Applicability Analysis")
    print("=" * 65)
    print_analysis()
