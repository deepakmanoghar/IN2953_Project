"""
Q7. Compare Adjacency List vs Adjacency Matrix representations.
    When is each preferred? What are the space complexities?

    DEFINITIONS:
    ─────────────────────────────────────────────────────────────────────────────
    Adjacency LIST : a dictionary (or array of lists) where adj[u] holds
                     all vertices v such that edge (u,v) exists.

    Adjacency MATRIX: a V x V 2D array where matrix[u][v] = 1 (or weight)
                      if an edge (u,v) exists, 0 otherwise.

    SPACE COMPLEXITY:
    ─────────────────────────────────────────────────────────────────────────────
      Representation     Space
      ─────────────────  ─────────────────────────────────────────────────────
      Adjacency List     O(V + E)   -- stores only actual edges
      Adjacency Matrix   O(V^2)     -- stores all V*V possible pairs

    OPERATION COMPLEXITIES:
    ─────────────────────────────────────────────────────────────────────────────
      Operation              Adj List    Adj Matrix
      ─────────────────────  ──────────  ──────────
      Check edge (u,v)       O(degree)   O(1)
      Add edge               O(1)        O(1)
      Remove edge            O(degree)   O(1)
      Find all neighbours    O(degree)   O(V)
      BFS / DFS              O(V + E)    O(V^2)

    WHEN TO USE ADJACENCY LIST:
    ─────────────────────────────────────────────────────────────────────────────
      - Sparse graphs (E << V^2): social networks, road maps, dependency graphs
      - BFS/DFS traversals (only iterate actual edges, not all possible ones)
      - Memory-constrained environments
      - Most competitive programming and interview problems

    WHEN TO USE ADJACENCY MATRIX:
    ─────────────────────────────────────────────────────────────────────────────
      - Dense graphs (E ~= V^2): complete graphs, fully connected networks
      - Frequent edge existence queries: O(1) lookup vs O(degree) for list
      - Floyd-Warshall all-pairs shortest path algorithm
      - Small graphs where V is bounded (e.g., V <= 1000)
      - Weighted graphs where quick weight lookup is needed
"""


# =====================================================
# Adjacency LIST implementation
# =====================================================
class AdjList:
    def __init__(self, vertices, directed=False):
        self.V        = vertices
        self.directed = directed
        self.adj      = {i: [] for i in range(vertices)}

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def has_edge(self, u, v):
        return any(nb == v for nb, _ in self.adj[u])

    def neighbours(self, u):
        return [nb for nb, _ in self.adj[u]]

    def edge_count(self):
        total = sum(len(nb) for nb in self.adj.values())
        return total if self.directed else total // 2

    def space_used(self):
        """Approximate number of stored entries."""
        return self.V + sum(len(nb) for nb in self.adj.values())

    def display(self):
        print("  Adjacency List:")
        for v in range(self.V):
            nbs = [(nb, w) for nb, w in self.adj[v]]
            print(f"    {v}: {nbs}")


# =====================================================
# Adjacency MATRIX implementation
# =====================================================
class AdjMatrix:
    def __init__(self, vertices, directed=False):
        self.V        = vertices
        self.directed = directed
        self.matrix   = [[0] * vertices for _ in range(vertices)]

    def add_edge(self, u, v, weight=1):
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight

    def has_edge(self, u, v):
        return self.matrix[u][v] != 0

    def neighbours(self, u):
        return [v for v in range(self.V) if self.matrix[u][v] != 0]

    def edge_count(self):
        total = sum(1 for r in self.matrix for val in r if val != 0)
        return total if self.directed else total // 2

    def space_used(self):
        """Exact number of stored entries."""
        return self.V * self.V

    def display(self):
        print("  Adjacency Matrix:")
        header = "    " + "  ".join(str(j) for j in range(self.V))
        print(header)
        print("    " + "-" * (3 * self.V))
        for i, row in enumerate(self.matrix):
            print(f"    {i}| " + "  ".join(str(v) for v in row))


# =====================================================
# Side-by-side benchmark
# =====================================================
def benchmark(V, edges, directed=False):
    al = AdjList(V, directed)
    am = AdjMatrix(V, directed)
    for u, v in edges:
        al.add_edge(u, v)
        am.add_edge(u, v)

    E = al.edge_count()

    print(f"\n  V={V}, E={E}, directed={directed}")
    print(f"  {'Metric':<30} {'Adj List':>12} {'Adj Matrix':>12}")
    print(f"  {'-'*30} {'-'*12} {'-'*12}")
    print(f"  {'Space entries stored':<30} {al.space_used():>12} {am.space_used():>12}")
    print(f"  {'Theoretical space':<30} {'O(V+E)':>12} {'O(V^2)':>12}")
    print(f"  {'has_edge(0,1) result':<30} {str(al.has_edge(0,1)):>12} {str(am.has_edge(0,1)):>12}")
    print(f"  {'neighbours(0)':<30} {str(al.neighbours(0)):>12} {str(am.neighbours(0)):>12}")


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    edges = [(0,1),(0,2),(1,3),(2,3),(3,4)]

    # ── Small graph display ──────────────────────────
    print("=" * 60)
    print("GRAPH REPRESENTATION COMPARISON  (V=5, E=5)")
    print("=" * 60)
    al = AdjList(5, directed=False)
    am = AdjMatrix(5, directed=False)
    for u, v in edges:
        al.add_edge(u, v)
        am.add_edge(u, v)
    al.display()
    print()
    am.display()

    # ── Benchmarks: sparse vs dense ─────────────────
    print("\n" + "=" * 60)
    print("SPACE COMPARISON: SPARSE vs DENSE")
    print("=" * 60)

    # Sparse graph (road map like)
    sparse_edges = [(i, i+1) for i in range(9)]                    # 10 nodes, 9 edges
    benchmark(10, sparse_edges)

    # Dense graph (nearly complete)
    dense_edges  = [(i, j) for i in range(8) for j in range(i+1,8)]  # 8 nodes, 28 edges
    benchmark(8, dense_edges)

    # ── Weighted graph ────────────────────────────────
    print("\n" + "=" * 60)
    print("WEIGHTED GRAPH (Adj Matrix is natural for weights)")
    print("=" * 60)
    wm = AdjMatrix(4, directed=True)
    wm.add_edge(0, 1, weight=5)
    wm.add_edge(0, 2, weight=3)
    wm.add_edge(1, 3, weight=2)
    wm.add_edge(2, 3, weight=7)
    wm.display()
    print("  Quick weight lookup: matrix[0][1] =", wm.matrix[0][1])

    # ── Summary table ─────────────────────────────────
    print("\n" + "=" * 60)
    print("SUMMARY COMPARISON TABLE")
    print("=" * 60)
    rows = [
        ("Space complexity",    "O(V + E)",   "O(V^2)"),
        ("Check edge (u,v)",    "O(degree)",  "O(1)"),
        ("Add / remove edge",   "O(1) / O(d)","O(1)"),
        ("List all neighbours", "O(degree)",  "O(V)"),
        ("BFS / DFS",           "O(V + E)",   "O(V^2)"),
        ("Best for sparse?",    "YES",         "No"),
        ("Best for dense?",     "Less ideal",  "YES"),
        ("Floyd-Warshall?",     "Awkward",     "Natural"),
        ("Memory usage",        "Low",         "High (V^2)"),
    ]
    print(f"  {'Property':<28} {'Adj List':^14} {'Adj Matrix':^14}")
    print(f"  {'-'*28} {'-'*14} {'-'*14}")
    for prop, al_v, am_v in rows:
        print(f"  {prop:<28} {al_v:^14} {am_v:^14}")

    print("\n  RULE OF THUMB:")
    print("    E << V^2  (sparse)  ->  Adjacency List")
    print("    E ~= V^2  (dense)   ->  Adjacency Matrix")
    print("=" * 60)
