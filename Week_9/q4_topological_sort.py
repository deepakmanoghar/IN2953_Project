"""
Q4. Topological Sort using Kahn's Algorithm (BFS with in-degree).

    TOPOLOGICAL SORT:
    -----------------
    A linear ordering of vertices such that for every directed edge u -> v,
    vertex u appears BEFORE v in the ordering.
    Only possible on a Directed Acyclic Graph (DAG).

    KAHN'S ALGORITHM:
    -----------------
    1. Compute the IN-DEGREE (number of incoming edges) for each vertex.
    2. Enqueue all vertices with in-degree == 0 (no prerequisites).
    3. While the queue is not empty:
       a. Dequeue a vertex u -> add it to the result order.
       b. For each neighbour v of u:
          - Decrease in-degree[v] by 1  (u is now "done").
          - If in-degree[v] becomes 0 -> enqueue v.
    4. If len(result) == V, no cycle exists and result is a valid order.
       Otherwise a cycle exists (some vertices were never enqueued).

    WHY BFS + IN-DEGREE?
    - In-degree 0 = "all prerequisites satisfied" -> safe to take.
    - Removing a completed course decreases the prerequisite count
      of dependent courses, eventually unlocking them.

    TIME  : O(V + E)  -- each vertex and edge processed once
    SPACE : O(V + E)  -- adjacency list + in-degree array + queue

    EXAMPLE (given in the question):
    ---------------------------------
    4 courses (0, 1, 2, 3)
    Prerequisites: [[1,0],[2,0],[3,1],[3,2]]
      [1,0] -> must take 0 before 1  (edge 0 -> 1)
      [2,0] -> must take 0 before 2  (edge 0 -> 2)
      [3,1] -> must take 1 before 3  (edge 1 -> 3)
      [3,2] -> must take 2 before 3  (edge 2 -> 3)

    Graph:  0 -> 1 -> 3
             \\-> 2 ->/

    Expected valid orderings: [0, 1, 2, 3]  or  [0, 2, 1, 3]
"""

from collections import deque, defaultdict


def topological_sort_kahn(num_vertices, prerequisites):
    """
    Kahn's algorithm for topological sort.

    Args:
        num_vertices  : int
        prerequisites : list[list[int]] -- [a, b] means b must come before a

    Returns:
        list[int] -- a valid topological order, or [] if a cycle exists
    """
    # Build adjacency list and in-degree array
    graph    = defaultdict(list)
    in_degree = [0] * num_vertices

    for a, b in prerequisites:
        graph[b].append(a)     # b -> a  (b must precede a)
        in_degree[a] += 1

    # Step 2: enqueue all zero-in-degree vertices
    queue = deque()
    for v in range(num_vertices):
        if in_degree[v] == 0:
            queue.append(v)

    order = []

    # Step 3: BFS
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1         # "remove" edge u -> v
            if in_degree[v] == 0:
                queue.append(v)       # all prerequisites of v are done

    # Step 4: cycle check
    if len(order) == num_vertices:
        return order        # valid topological order
    else:
        return []           # cycle detected


# =====================================================
# Verbose version: shows in-degree state at each step
# =====================================================
def topological_sort_kahn_verbose(num_vertices, prerequisites):
    graph     = defaultdict(list)
    in_degree = [0] * num_vertices
    for a, b in prerequisites:
        graph[b].append(a)
        in_degree[a] += 1

    print(f"\n  Initial in-degrees: {list(enumerate(in_degree))}")

    queue = deque()
    for v in range(num_vertices):
        if in_degree[v] == 0:
            queue.append(v)

    print(f"  Starting queue (in-degree 0): {list(queue)}\n")
    print(f"  {'Step':>4} | {'Dequeued':>8} | {'in-degree update':^28} | Queue after")
    print(f"  {'-'*4}-+-{'-'*8}-+-{'-'*28}-+-{'-'*20}")

    order = []
    step  = 0
    while queue:
        u = queue.popleft()
        order.append(u)
        step += 1
        updates = []
        for v in graph[u]:
            in_degree[v] -= 1
            updates.append(f"in[{v}]: {in_degree[v]+1}->{in_degree[v]}")
            if in_degree[v] == 0:
                queue.append(v)
        update_str = ", ".join(updates) if updates else "none"
        print(f"  {step:>4} | course {u}  | {update_str:<28} | {list(queue)}")

    return order if len(order) == num_vertices else []


# =====================================================
# DFS-based topological sort (for comparison)
# =====================================================
def topological_sort_dfs(num_vertices, prerequisites):
    """DFS post-order approach to topological sort."""
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    UNVISITED, VISITING, DONE = 0, 1, 2
    state  = [UNVISITED] * num_vertices
    result = []
    cycle  = [False]

    def dfs(u):
        if cycle[0]:
            return
        state[u] = VISITING
        for v in graph[u]:
            if state[v] == VISITING:
                cycle[0] = True
                return
            if state[v] == UNVISITED:
                dfs(v)
        state[u] = DONE
        result.append(u)   # post-order: append after all descendants

    for v in range(num_vertices):
        if state[v] == UNVISITED:
            dfs(v)
        if cycle[0]:
            return []

    result.reverse()   # reverse post-order = topological order
    return result


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    # ── Required example from the question ──────────
    print("=" * 60)
    print("GIVEN EXAMPLE: 4 courses, prerequisites [[1,0],[2,0],[3,1],[3,2]]")
    print("=" * 60)
    print("""
  Graph structure:
       0 ---> 1
       |       \\
       |        v
       +----> 2 -> 3

  Reading:  0 before 1, 0 before 2, 1 before 3, 2 before 3
  """)

    n      = 4
    prereqs = [[1,0],[2,0],[3,1],[3,2]]

    order_kahn = topological_sort_kahn(n, prereqs)
    order_dfs  = topological_sort_dfs(n, prereqs)
    print(f"  Kahn's (BFS) order : {order_kahn}")
    print(f"  DFS post-order     : {order_dfs}")
    print(f"  (Both are valid orderings — multiple correct answers exist)")

    # ── Verbose trace ────────────────────────────────
    print("\n" + "=" * 60)
    print("VERBOSE STEP-BY-STEP TRACE (Kahn's algorithm)")
    print("=" * 60)
    order_verbose = topological_sort_kahn_verbose(n, prereqs)
    print(f"\n  Final order: {order_verbose}")

    # ── Additional test cases ────────────────────────
    extra = [
        {"label": "Linear chain", "n": 4,
         "prereqs": [[1,0],[2,1],[3,2]], "expected_valid": True},
        {"label": "Cycle present", "n": 3,
         "prereqs": [[1,0],[2,1],[0,2]], "expected_valid": False},
        {"label": "No prerequisites", "n": 3,
         "prereqs": [], "expected_valid": True},
    ]

    print("\n" + "=" * 60)
    print("ADDITIONAL TEST CASES")
    print("=" * 60)
    for tc in extra:
        o = topological_sort_kahn(tc["n"], tc["prereqs"])
        valid = len(o) == tc["n"]
        ok = "[OK]" if valid == tc["expected_valid"] else "[X]"
        print(f"\n  {tc['label']}: prereqs={tc['prereqs']}")
        print(f"    Result : {o if o else 'CYCLE DETECTED - no valid order'}")
        print(f"    Expected cycle: {not tc['expected_valid']}  {ok}")

    print("\n" + "=" * 60)
    print("KAHN'S ALGORITHM SUMMARY:")
    print("  in-degree 0 => 'all prerequisites met' => safe to process.")
    print("  After processing u, decrement neighbours' in-degrees.")
    print("  If a neighbour hits in-degree 0, it joins the queue.")
    print("  If result length < V, a cycle exists (some nodes never freed).")
    print("=" * 60)
