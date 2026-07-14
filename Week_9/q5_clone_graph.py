"""
Q5. Clone a Graph: given a reference to a node in a connected undirected
    graph, return a deep copy of the graph.

    PROBLEM:
    --------
    Each node has a val (int) and a list of neighbors (list[Node]).
    We must create entirely NEW node objects (not references to originals)
    such that the structure is identical.

    WHY A HASH MAP?
    ---------------
    Graphs can have cycles. Without tracking which nodes have already been
    cloned, DFS/BFS would loop forever.

    The hash map acts as:
      1. A visited set  -- "have I cloned this node already?"
      2. A lookup table -- "what is the clone of original node X?"

    ALGORITHM (BFS approach):
    -------------------------
    1. Create a clone of the start node and store it in the map:
         clone_map[original] = clone
    2. Use a queue seeded with the original start node.
    3. For each original node u dequeued:
       a. For each neighbour v of u:
          - If v is not in clone_map: create clone_map[v] = Node(v.val)
            and enqueue v.
          - Append clone_map[v] to clone_map[u].neighbors.
    4. Return clone_map[start].

    ALGORITHM (DFS approach):
    -------------------------
    Same idea, just recursive instead of a queue.

    TIME  : O(V + E) -- each node and edge visited exactly once.
    SPACE : O(V)     -- hash map holds one entry per node.
"""

from collections import deque


# =====================================================
# Node definition
# =====================================================
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self):
        return f"Node({self.val})"


# =====================================================
# BFS Clone
# =====================================================
def clone_graph_bfs(node):
    """
    Deep-copy the graph using BFS + a visited hash map.

    Args:
        node : Node | None -- reference to any node in the graph

    Returns:
        Node | None -- the corresponding node in the cloned graph
    """
    if node is None:
        return None

    clone_map = {}                         # original -> clone
    clone_map[node] = Node(node.val)       # clone the start node

    queue = deque([node])

    while queue:
        orig = queue.popleft()

        for neighbour in orig.neighbors:
            if neighbour not in clone_map:
                # First time seeing this neighbour -- create its clone
                clone_map[neighbour] = Node(neighbour.val)
                queue.append(neighbour)
            # Connect the cloned edge
            clone_map[orig].neighbors.append(clone_map[neighbour])

    return clone_map[node]


# =====================================================
# DFS Clone (recursive)
# =====================================================
def clone_graph_dfs(node, clone_map=None):
    """
    Deep-copy the graph using DFS + a visited hash map.

    Args:
        node      : Node | None
        clone_map : dict (internal, used for recursion)

    Returns:
        Node | None -- corresponding clone node
    """
    if node is None:
        return None

    if clone_map is None:
        clone_map = {}

    if node in clone_map:
        return clone_map[node]   # already cloned -> return existing clone

    clone = Node(node.val)
    clone_map[node] = clone      # register BEFORE recursing (handles cycles)

    for neighbour in node.neighbors:
        clone.neighbors.append(clone_graph_dfs(neighbour, clone_map))

    return clone


# =====================================================
# Helper: build a graph from adjacency list
# =====================================================
def build_graph(n, adj):
    """
    Create n nodes (1-indexed) connected by adjacency list adj.
    adj: list[list[int]] -- adj[i] is the list of neighbours of node i+1
    Returns the node with val=1.
    """
    if n == 0:
        return None
    nodes = [Node(i+1) for i in range(n)]
    for i, neighbours in enumerate(adj):
        nodes[i].neighbors = [nodes[j-1] for j in neighbours]
    return nodes[0]


# =====================================================
# Helper: serialise graph to adjacency list (for comparison)
# =====================================================
def serialise(node):
    """BFS traversal to produce adjacency list for easy printing."""
    if node is None:
        return []
    visited = {}
    queue   = deque([node])
    result  = {}
    while queue:
        u = queue.popleft()
        if u.val in visited:
            continue
        visited[u.val] = True
        result[u.val] = sorted([v.val for v in u.neighbors])
        for v in u.neighbors:
            if v.val not in visited:
                queue.append(v)
    return dict(sorted(result.items()))


def are_equal_graphs(n1, n2):
    """Check that two graphs have identical structure (by serialisation)."""
    return serialise(n1) == serialise(n2)


def are_disjoint(n1, n2):
    """Check that the two graphs share NO Node objects."""
    def collect_nodes(node):
        visited = set()
        queue   = deque([node])
        while queue:
            u = queue.popleft()
            if id(u) in visited:
                continue
            visited.add(id(u))
            for v in u.neighbors:
                queue.append(v)
        return visited

    ids1 = collect_nodes(n1)
    ids2 = collect_nodes(n2)
    return ids1.isdisjoint(ids2)


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        {
            "label": "4-node cycle: 1-2-3-4-1",
            "n": 4,
            "adj": [[2,4],[1,3],[2,4],[1,3]],   # 1-indexed neighbours
        },
        {
            "label": "Two nodes connected",
            "n": 2,
            "adj": [[2],[1]],
        },
        {
            "label": "Single isolated node",
            "n": 1,
            "adj": [[]],
        },
        {
            "label": "Star graph (node 1 connects to all)",
            "n": 4,
            "adj": [[2,3,4],[1],[1],[1]],
        },
    ]

    print("=" * 60)
    print("Clone Graph -- BFS + Hash Map")
    print("=" * 60)

    for tc in test_cases:
        original = build_graph(tc["n"], tc["adj"])
        clone_b  = clone_graph_bfs(original)
        clone_d  = clone_graph_dfs(original)

        struct_ok_b = are_equal_graphs(original, clone_b)
        struct_ok_d = are_equal_graphs(original, clone_d)
        deep_ok_b   = are_disjoint(original, clone_b)
        deep_ok_d   = are_disjoint(original, clone_d)

        print(f"\n  {tc['label']}")
        print(f"    Original structure : {serialise(original)}")
        print(f"    BFS clone structure: {serialise(clone_b)}")
        print(f"    DFS clone structure: {serialise(clone_d)}")
        print(f"    Structures match (BFS): {struct_ok_b}  {'[OK]' if struct_ok_b else '[X]'}")
        print(f"    Structures match (DFS): {struct_ok_d}  {'[OK]' if struct_ok_d else '[X]'}")
        print(f"    Deep copy (no shared objects) BFS: {deep_ok_b}  {'[OK]' if deep_ok_b else '[X]'}")
        print(f"    Deep copy (no shared objects) DFS: {deep_ok_d}  {'[OK]' if deep_ok_d else '[X]'}")

    print("\n" + "=" * 60)
    print("WHY THE HASH MAP IS ESSENTIAL:")
    print("  Without it, on a cycle like 1-2-3-1:")
    print("    Clone 1 -> clone its neighbour 2")
    print("    -> clone 2's neighbour 3")
    print("    -> clone 3's neighbour 1  <-- already cloned!")
    print("    Without the map we'd create a NEW node 1 and loop forever.")
    print("  The map lets us detect 'already cloned' and return the")
    print("  existing clone object instead of creating a duplicate.")
    print()
    print("  Time : O(V + E)")
    print("  Space: O(V) for the hash map")
    print("=" * 60)
