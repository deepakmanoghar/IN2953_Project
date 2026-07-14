"""
Q1. Implement a Graph class with adjacency list representation.
    Support both directed and undirected edges.
    Include BFS and DFS traversals.

    ADJACENCY LIST:
    ---------------
    A dictionary where each key is a vertex and its value is the
    list of neighbours reachable from that vertex.

      {
        0: [1, 2],
        1: [0, 3],
        2: [0],
        3: [1]
      }

    BFS (Breadth-First Search):
      Uses a QUEUE. Explores all neighbours at the current depth
      before moving deeper. Guarantees shortest hop-count path
      in unweighted graphs.

    DFS (Depth-First Search):
      Uses a STACK (or recursion). Dives as deep as possible along
      one branch before backtracking. Natural for cycle detection,
      topological sort, connected components.
"""

from collections import deque


class Graph:
    # =====================================================
    # Constructor
    # =====================================================
    def __init__(self, directed=False):
        """
        Args:
            directed (bool): True -> directed graph (digraph)
                             False -> undirected graph (default)
        """
        self.directed = directed
        self.adj = {}          # adjacency list: {vertex: [neighbours]}

    # =====================================================
    # Add vertex
    # =====================================================
    def add_vertex(self, v):
        """Add an isolated vertex (no edges yet)."""
        if v not in self.adj:
            self.adj[v] = []

    # =====================================================
    # Add edge
    # =====================================================
    def add_edge(self, u, v):
        """
        Add an edge u -> v.
        For undirected graphs also adds v -> u.
        Auto-creates vertices if they don't exist.
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)   # bidirectional

    # =====================================================
    # BFS  --  O(V + E)
    # =====================================================
    def bfs(self, start):
        """
        Breadth-First Search from 'start'.
        Returns the list of vertices in BFS visit order.

        Algorithm:
          1. Mark start as visited, enqueue it.
          2. While queue is not empty:
             a. Dequeue front vertex u.
             b. For each unvisited neighbour v of u:
                - Mark v visited, enqueue v.
        """
        if start not in self.adj:
            return []

        visited = set([start])
        queue   = deque([start])
        order   = []

        while queue:
            u = queue.popleft()
            order.append(u)
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)

        return order

    # =====================================================
    # DFS  --  O(V + E)
    # =====================================================
    def dfs(self, start):
        """
        Depth-First Search from 'start' (iterative with explicit stack).
        Returns the list of vertices in DFS visit order.

        Algorithm:
          1. Push start onto stack.
          2. While stack is not empty:
             a. Pop vertex u; if already visited, skip.
             b. Mark u visited, record it.
             c. Push all unvisited neighbours of u.
        """
        if start not in self.adj:
            return []

        visited = set()
        stack   = [start]
        order   = []

        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            order.append(u)
            # Push in reverse order so left-most neighbour is processed first
            for v in reversed(self.adj[u]):
                if v not in visited:
                    stack.append(v)

        return order

    def dfs_recursive(self, start):
        """Recursive DFS wrapper."""
        visited = set()
        order   = []

        def _dfs(u):
            visited.add(u)
            order.append(u)
            for v in self.adj[u]:
                if v not in visited:
                    _dfs(v)

        if start in self.adj:
            _dfs(start)
        return order

    # =====================================================
    # Utility: print adjacency list
    # =====================================================
    def print_graph(self):
        kind = "Directed" if self.directed else "Undirected"
        print(f"  {kind} Graph (adjacency list):")
        for v in sorted(self.adj):
            print(f"    {v} -> {self.adj[v]}")


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    # ── Undirected graph ─────────────────────────────
    #   0 -- 1 -- 3
    #   |         |
    #   2 --------+
    print("=" * 55)
    print("UNDIRECTED GRAPH")
    print("=" * 55)
    ug = Graph(directed=False)
    edges_u = [(0,1),(0,2),(1,3),(2,3),(3,4)]
    for u, v in edges_u:
        ug.add_edge(u, v)
    ug.print_graph()

    print("\n  BFS from 0:", ug.bfs(0))
    print("  DFS from 0 (iterative):", ug.dfs(0))
    print("  DFS from 0 (recursive):", ug.dfs_recursive(0))

    # ── Directed graph ───────────────────────────────
    #   0 -> 1 -> 3
    #   |
    #   v
    #   2 -> 4
    print("\n" + "=" * 55)
    print("DIRECTED GRAPH")
    print("=" * 55)
    dg = Graph(directed=True)
    edges_d = [(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)]
    for u, v in edges_d:
        dg.add_edge(u, v)
    dg.print_graph()

    print("\n  BFS from 0:", dg.bfs(0))
    print("  DFS from 0 (iterative):", dg.dfs(0))
    print("  DFS from 0 (recursive):", dg.dfs_recursive(0))

    # ── Disconnected graph ───────────────────────────
    print("\n" + "=" * 55)
    print("DISCONNECTED GRAPH  (two components)")
    print("=" * 55)
    disc = Graph(directed=False)
    for u, v in [(0,1),(1,2),(3,4)]:
        disc.add_edge(u, v)
    disc.print_graph()
    print("\n  BFS from 0 (only reaches component A):", disc.bfs(0))
    print("  BFS from 3 (only reaches component B):", disc.bfs(3))

    print("\n" + "=" * 55)
    print("COMPLEXITY SUMMARY:")
    print("  BFS / DFS : O(V + E) time,  O(V) space")
    print("  V = vertices,  E = edges")
    print("=" * 55)
