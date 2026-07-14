"""
Q6. Find the shortest path between two nodes in an unweighted graph using BFS.
    Return the ACTUAL PATH (list of vertices), not just the distance.

    WHY BFS GUARANTEES SHORTEST PATH (unweighted):
    -----------------------------------------------
    BFS explores vertices level by level (distance 1, then 2, then 3, ...).
    The FIRST time BFS reaches the destination, it must have done so via
    the fewest possible edges, because no shorter route has been overlooked
    (BFS never skips a level).

    Note: BFS only guarantees the shortest HOP COUNT path.
    For weighted graphs, use Dijkstra's algorithm.

    TRACKING THE PATH:
    ------------------
    Keep a 'parent' dictionary:
      parent[v] = u  means "we arrived at v from u during BFS"
    Once the destination is found, back-track through parent[] to reconstruct
    the full path from source to destination.

    TIME  : O(V + E)  -- standard BFS
    SPACE : O(V)      -- visited set + parent map + queue

    PATH RECONSTRUCTION: O(path_length)
"""

from collections import deque, defaultdict


# =====================================================
# Shortest path via BFS (returns path list)
# =====================================================
def shortest_path_bfs(graph, start, end):
    """
    Find the shortest path from 'start' to 'end' in an unweighted graph.

    Args:
        graph : dict[any -> list[any]] -- adjacency list
        start : starting vertex
        end   : destination vertex

    Returns:
        list -- shortest path [start, ..., end], or [] if unreachable
    """
    if start == end:
        return [start]

    if start not in graph:
        return []

    visited = {start}
    parent  = {start: None}   # parent[v] = the vertex we came from
    queue   = deque([start])

    while queue:
        current = queue.popleft()

        for neighbour in graph.get(current, []):
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = current

                if neighbour == end:
                    # Destination reached -- reconstruct path
                    return _reconstruct_path(parent, start, end)

                queue.append(neighbour)

    return []   # destination unreachable


def _reconstruct_path(parent, start, end):
    """Walk backwards through 'parent' to rebuild the path."""
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()    # reversal converts end->start to start->end
    return path


# =====================================================
# All shortest paths (BFS + backtrack)
# =====================================================
def all_shortest_paths(graph, start, end):
    """
    Find ALL shortest paths (same hop count) from start to end.
    Uses BFS for distance levels, then reconstructs via backtracking.
    """
    if start == end:
        return [[start]]

    # BFS to record all valid parents at each level
    dist    = {start: 0}
    parents = defaultdict(list)    # parents[v] = [all u from which v was reached]
    queue   = deque([start])

    while queue:
        u = queue.popleft()
        if u == end:
            break
        for v in graph.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
            if v in dist and dist[v] == dist[u] + 1:
                parents[v].append(u)

    if end not in dist:
        return []

    # Backtrack to find all paths
    paths = []

    def backtrack(node, path):
        if node == start:
            paths.append([start] + path[::-1])
            return
        for p in parents[node]:
            backtrack(p, path + [node])

    backtrack(end, [])
    return paths


# =====================================================
# Build undirected graph helper
# =====================================================
def build_undirected(edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    return g


# =====================================================
# Print path with arrows
# =====================================================
def fmt_path(path):
    if not path:
        return "No path exists"
    return " -> ".join(str(v) for v in path)


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    # Graph:
    #  0 - 1 - 2 - 5
    #  |   |       |
    #  3 - 4 ------+
    edges = [(0,1),(0,3),(1,2),(1,4),(2,5),(3,4),(4,5)]
    G = build_undirected(edges)

    print("=" * 60)
    print("Shortest Path in Unweighted Graph (BFS)")
    print("=" * 60)
    print("\n  Graph edges:", edges)
    print("\n  Adjacency list:")
    for v in sorted(G):
        print(f"    {v}: {sorted(G[v])}")

    queries = [
        (0, 5),
        (0, 4),
        (3, 2),
        (0, 0),   # same node
        (2, 3),
    ]

    print()
    for src, dst in queries:
        path = shortest_path_bfs(G, src, dst)
        dist = len(path) - 1 if path else -1
        print(f"  Shortest path {src} -> {dst}: {fmt_path(path)}  (hops: {dist})")

    # ── All shortest paths ───────────────────────────
    print("\n  All shortest paths from 0 to 5:")
    for p in all_shortest_paths(G, 0, 5):
        print(f"    {fmt_path(p)}")

    # ── Disconnected graph ────────────────────────────
    print("\n" + "=" * 60)
    print("DISCONNECTED GRAPH")
    print("=" * 60)
    disc = build_undirected([(0,1),(0,2),(3,4)])
    print(f"  Edges: [(0,1),(0,2),(3,4)]")
    path = shortest_path_bfs(disc, 0, 3)
    print(f"  Shortest path 0 -> 3: {fmt_path(path)}")

    print("\n" + "=" * 60)
    print("WHY BFS = SHORTEST PATH:")
    print("  BFS visits nodes in order of INCREASING distance from source.")
    print("  Level 0: {start}")
    print("  Level 1: all nodes exactly 1 hop away")
    print("  Level 2: all nodes exactly 2 hops away (not already seen)")
    print("  ...")
    print("  => First time destination is reached = shortest hop count.")
    print()
    print("PATH RECONSTRUCTION via parent[]:")
    print("  parent[v] = u  means 'BFS reached v through u'")
    print("  Backtrack: end -> parent[end] -> ... -> start")
    print("  Reverse the backtrack to get start -> ... -> end")
    print()
    print("  Time : O(V + E)")
    print("  Space: O(V) for visited, parent, queue")
    print("=" * 60)
