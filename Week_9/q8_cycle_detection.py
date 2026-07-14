"""
Q8. Detect if adding an edge would create a cycle in a directed graph.
    Use DFS with three states: UNVISITED, VISITING, VISITED.

    THREE-STATE DFS CYCLE DETECTION:
    ---------------------------------
    State 0 - UNVISITED : node not yet touched by DFS
    State 1 - VISITING  : node is on the CURRENT DFS call path (ancestors)
    State 2 - VISITED   : node and ALL its descendants fully explored (no cycle)

    BACK EDGE = CYCLE:
    When DFS reaches a node that is currently VISITING (state 1),
    it means we've found a path that leads back to an ancestor on the
    current call stack -> CYCLE!

    WHY THREE STATES (not two)?
    ---------------------------
    Two states (visited / unvisited) fail on directed graphs:
      Consider:   A -> C
                  B -> C
    When DFS from A finishes C, C is marked visited.
    When DFS from B then reaches C (already visited), we'd wrongly
    report a cycle even though A-C-B forms no cycle.
    The VISITED state (fully explored) tells us: "safe, no cycle below".
    Only the VISITING state indicates a problematic back edge.

    ADDING EDGE CHECK:
    ------------------
    To check if adding edge (u -> v) would create a cycle:
      1. Temporarily add the edge to the graph.
      2. Run DFS cycle detection.
      3. Remove the edge (restore graph).
      4. Return whether a cycle was found.

    Optimisation: if v can reach u (without adding the edge),
    then adding u -> v would create a cycle.

    TIME  : O(V + E) per check
    SPACE : O(V)     for state array + recursion stack
"""

from collections import defaultdict


UNVISITED = 0
VISITING  = 1
VISITED   = 2


# =====================================================
# Core: detect cycle in a directed graph (DFS 3-state)
# =====================================================
def has_cycle(graph, num_vertices):
    """
    Return True if the directed graph contains at least one cycle.

    Args:
        graph        : dict[int -> list[int]] -- adjacency list
        num_vertices : int

    Returns:
        bool
    """
    state = [UNVISITED] * num_vertices

    def dfs(u):
        state[u] = VISITING
        for v in graph.get(u, []):
            if state[v] == VISITING:
                return True      # back-edge -> cycle
            if state[v] == UNVISITED:
                if dfs(v):
                    return True
        state[u] = VISITED
        return False

    for node in range(num_vertices):
        if state[node] == UNVISITED:
            if dfs(node):
                return True

    return False


# =====================================================
# Check if adding (u -> v) would create a cycle
# =====================================================
def would_add_cycle(graph, num_vertices, u, v):
    """
    Check if adding the directed edge u -> v would create a cycle.

    Strategy:
      Adding u -> v creates a cycle if and only if there already exists
      a directed path from v to u. We detect this by checking reachability:
      can we reach u starting from v?

    Args:
        graph        : dict[int -> list[int]] -- existing adjacency list
        num_vertices : int
        u, v         : the proposed edge u -> v

    Returns:
        bool -- True if adding this edge would create a cycle
    """
    # If v can reach u (without the new edge), adding u->v closes a cycle
    return _can_reach(graph, v, u, num_vertices)


def _can_reach(graph, src, dst, num_vertices):
    """DFS reachability: can we reach 'dst' from 'src'?"""
    if src == dst:
        return True    # self-loop
    visited = set()
    stack   = [src]
    while stack:
        node = stack.pop()
        if node == dst:
            return True
        if node in visited:
            continue
        visited.add(node)
        for nb in graph.get(node, []):
            if nb not in visited:
                stack.append(nb)
    return False


# =====================================================
# Full check: add edge, run full cycle detection, remove
# =====================================================
def would_add_cycle_full_dfs(graph, num_vertices, u, v):
    """
    Alternative: literally add the edge, check for cycle, then remove.
    Useful when the graph might already have cycles.
    """
    graph[u].append(v)
    cycle_found = has_cycle(graph, num_vertices)
    graph[u].remove(v)    # restore
    return cycle_found


# =====================================================
# DFS with verbose state output
# =====================================================
def detect_cycle_verbose(graph, num_vertices):
    """Shows DFS state transitions for learning purposes."""
    state      = [UNVISITED] * num_vertices
    state_name = {UNVISITED: "UNVISITED", VISITING: "VISITING", VISITED: "VISITED"}
    indent     = [0]

    def dfs(u):
        indent[0] += 1
        pad = "  " * indent[0]
        state[u] = VISITING
        print(f"{pad}Enter node {u}  -> state: VISITING")
        for v in graph.get(u, []):
            print(f"{pad}  -> neighbour {v}  state={state_name[state[v]]}")
            if state[v] == VISITING:
                print(f"{pad}  *** CYCLE DETECTED: back-edge {u}->{v} ***")
                return True
            if state[v] == UNVISITED:
                if dfs(v):
                    return True
        state[u] = VISITED
        print(f"{pad}Exit  node {u}  -> state: VISITED")
        indent[0] -= 1
        return False

    for node in range(num_vertices):
        if state[node] == UNVISITED:
            print(f"\n[Starting DFS from node {node}]")
            if dfs(node):
                return True
    return False


# =====================================================
# Build a directed graph from edge list
# =====================================================
def build_graph(edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
    return g


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    # ── Test 1: no cycle ────────────────────────────
    print("=" * 60)
    print("CYCLE DETECTION -- 3-State DFS")
    print("=" * 60)

    tests = [
        {
            "label" : "DAG (no cycle): 0->1->2->3",
            "V"     : 4,
            "edges" : [(0,1),(1,2),(2,3)],
            "expect": False,
        },
        {
            "label" : "Simple cycle: 0->1->2->0",
            "V"     : 3,
            "edges" : [(0,1),(1,2),(2,0)],
            "expect": True,
        },
        {
            "label" : "Self-loop: 0->0",
            "V"     : 2,
            "edges" : [(0,0),(0,1)],
            "expect": True,
        },
        {
            "label" : "Diamond DAG (no cycle): 0->1, 0->2, 1->3, 2->3",
            "V"     : 4,
            "edges" : [(0,1),(0,2),(1,3),(2,3)],
            "expect": False,
        },
        {
            "label" : "Complex with cycle: A->B->C->D, C->B (back-edge)",
            "V"     : 4,
            "edges" : [(0,1),(1,2),(2,3),(2,1)],
            "expect": True,
        },
    ]

    for tc in tests:
        g   = build_graph(tc["edges"])
        res = has_cycle(g, tc["V"])
        ok  = "[OK]" if res == tc["expect"] else "[X]"
        print(f"\n  {tc['label']}")
        print(f"    Cycle detected: {res}  (expected {tc['expect']})  {ok}")

    # ── Test 2: would adding an edge create a cycle? ─
    print("\n" + "=" * 60)
    print("WOULD ADDING AN EDGE CREATE A CYCLE?")
    print("=" * 60)

    base_edges = [(0,1),(1,2),(2,3)]
    G = build_graph(base_edges)
    proposed_edges = [
        (3, 0, True),    # 3->0 closes the chain into a cycle
        (3, 1, True),    # 3->1 creates cycle 1->2->3->1
        (0, 2, False),   # shortcut, no new cycle
        (0, 3, False),   # shortcut, no new cycle
        (2, 0, True),    # 2->0 creates cycle 0->1->2->0
    ]

    print(f"\n  Base graph: {base_edges}   (0->1->2->3)")
    print(f"\n  {'Proposed edge':>15} | {'Creates cycle?':^16} | Expected | OK?")
    print(f"  {'-'*15}-+-{'-'*16}-+-{'-'*8}-+-{'-'*4}")
    for u, v, expected in proposed_edges:
        result = would_add_cycle(G, 4, u, v)
        ok     = "[OK]" if result == expected else "[X]"
        print(f"  {'%d -> %d' % (u,v):>15} | {str(result):^16} | {str(expected):^8} | {ok}")

    # ── Verbose trace for a cycle ────────────────────
    print("\n" + "=" * 60)
    print("VERBOSE DFS TRACE -- cycle: 0->1->2->0")
    print("=" * 60)
    g_cycle = build_graph([(0,1),(1,2),(2,0)])
    detect_cycle_verbose(g_cycle, 3)

    # ── State explanation ────────────────────────────
    print("\n" + "=" * 60)
    print("THREE STATES EXPLAINED:")
    print("  UNVISITED (0): DFS has not reached this node yet.")
    print("  VISITING  (1): Node is on the CURRENT active DFS path.")
    print("                 Any edge to a VISITING node = CYCLE.")
    print("  VISITED   (2): Node + all descendants fully explored.")
    print("                 Reaching a VISITED node is safe (no cycle).")
    print()
    print("WHY TWO STATES ARE NOT ENOUGH (directed graphs):")
    print("  A -> C  and  B -> C")
    print("  With 2 states: DFS from A explores C (marks C visited).")
    print("  DFS from B sees C is 'visited' and wrongly reports a cycle.")
    print("  With 3 states: C is VISITED (fully done), not VISITING,")
    print("  so B->C is correctly identified as safe (cross-edge).")
    print("=" * 60)
