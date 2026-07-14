"""
Q3. Course Schedule: Given numCourses and a list of prerequisites [a, b]
    (meaning "you must take b before a"), determine if it is possible to
    finish all courses.

    HOW THIS IS A CYCLE DETECTION PROBLEM:
    ----------------------------------------
    Model courses as NODES and prerequisites as DIRECTED EDGES.
      [a, b]  ==>  edge  b -> a   ("b must come before a")

    If there is a CYCLE in this directed graph, it means some course
    depends on itself (directly or indirectly) -> impossible to finish.

    Example of a cycle:
      Course 0 requires Course 1  (1 -> 0)
      Course 1 requires Course 0  (0 -> 1)
      -> deadlock: can't start either!

    No cycle = there exists a valid order to take all courses
    (the topological ordering).

    ALGORITHM: DFS with three node states
    ----------------------------------------
      UNVISITED (0) : not yet explored
      VISITING  (1) : currently in the DFS call stack (being processed)
      VISITED   (2) : fully processed (all descendants explored, no cycle)

    When we encounter a node in state VISITING during DFS,
    we have found a back-edge -> CYCLE DETECTED.

    TIME  : O(V + E)  -- standard DFS
    SPACE : O(V + E)  -- adjacency list + recursion stack
"""

from collections import defaultdict


UNVISITED = 0
VISITING  = 1
VISITED   = 2


def can_finish(num_courses, prerequisites):
    """
    Determine if all courses can be finished.

    Args:
        num_courses   : int
        prerequisites : list[list[int]]  -- [a, b] means b must precede a

    Returns:
        bool -- True if no cycle (courses can be finished), False otherwise
    """
    # Build adjacency list: b -> a (b is a prerequisite of a)
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    state = [UNVISITED] * num_courses

    def dfs(course):
        """Return True if a cycle is found starting from 'course'."""
        if state[course] == VISITING:
            return True    # back-edge found -> cycle!
        if state[course] == VISITED:
            return False   # already fully explored, safe

        state[course] = VISITING      # mark as in-progress

        for neighbour in graph[course]:
            if dfs(neighbour):
                return True           # propagate cycle detection

        state[course] = VISITED       # fully explored, no cycle here
        return False

    # Check every course (graph may be disconnected)
    for course in range(num_courses):
        if state[course] == UNVISITED:
            if dfs(course):
                return False   # cycle found

    return True   # no cycle -> all courses can be finished


# =====================================================
# Iterative version using explicit stack + state array
# =====================================================
def can_finish_iterative(num_courses, prerequisites):
    """Iterative DFS cycle detection using explicit stack."""
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    state = [UNVISITED] * num_courses

    for start in range(num_courses):
        if state[start] != UNVISITED:
            continue
        # Stack stores (course, iterator_over_neighbours)
        stack = [(start, iter(graph[start]))]
        state[start] = VISITING

        while stack:
            course, neighbours = stack[-1]
            try:
                nxt = next(neighbours)
                if state[nxt] == VISITING:
                    return False        # cycle detected
                if state[nxt] == UNVISITED:
                    state[nxt] = VISITING
                    stack.append((nxt, iter(graph[nxt])))
            except StopIteration:
                state[course] = VISITED
                stack.pop()

    return True


# =====================================================
# Helper: explain why it is a cycle detection problem
# =====================================================
def explain_cycle(num_courses, prerequisites):
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    print(f"  Courses: 0 to {num_courses-1}")
    print(f"  Prerequisites (raw): {prerequisites}")
    print(f"  Directed graph edges (b -> a means b before a):")
    edges = [(b, a) for a, b in prerequisites]
    for u, v in edges:
        print(f"    {u} -> {v}")


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        {
            "label": "No prerequisites (trivially OK)",
            "n": 3,
            "prereqs": [],
            "expected": True,
        },
        {
            "label": "Linear chain (OK): 0->1->2->3",
            "n": 4,
            "prereqs": [[1,0],[2,1],[3,2]],
            "expected": True,
        },
        {
            "label": "Simple cycle (FAIL): 0 requires 1, 1 requires 0",
            "n": 2,
            "prereqs": [[1,0],[0,1]],
            "expected": False,
        },
        {
            "label": "Three-node cycle (FAIL)",
            "n": 3,
            "prereqs": [[1,0],[2,1],[0,2]],
            "expected": False,
        },
        {
            "label": "DAG with multiple paths (OK)",
            "n": 4,
            "prereqs": [[1,0],[2,0],[3,1],[3,2]],
            "expected": True,
        },
        {
            "label": "Self-loop (FAIL): course requires itself",
            "n": 2,
            "prereqs": [[0,0]],
            "expected": False,
        },
    ]

    print("=" * 60)
    print("Course Schedule -- Cycle Detection via DFS")
    print("=" * 60)

    for tc in test_cases:
        n, prereqs, expected = tc["n"], tc["prereqs"], tc["expected"]
        r1 = can_finish(n, prereqs)
        r2 = can_finish_iterative(n, prereqs)
        ok = "[OK]" if r1 == r2 == expected else "[X]"
        print(f"\n  {tc['label']}")
        explain_cycle(n, prereqs)
        print(f"  Recursive result  : {'Can finish' if r1 else 'CANNOT finish'}")
        print(f"  Iterative result  : {'Can finish' if r2 else 'CANNOT finish'}")
        print(f"  Expected          : {'Can finish' if expected else 'CANNOT finish'}  {ok}")

    print("\n" + "=" * 60)
    print("THREE NODE STATES EXPLAINED:")
    print("  UNVISITED (0) : node not yet touched by DFS")
    print("  VISITING  (1) : node is on the current DFS path (call stack)")
    print("  VISITED   (2) : node fully explored, no cycle below it")
    print()
    print("  If during DFS we reach a node in VISITING state,")
    print("  it means we followed a path back to an ancestor")
    print("  currently on the stack -> BACK EDGE -> CYCLE!")
    print()
    print("  Two-state (visited/unvisited) is insufficient for")
    print("  directed graphs because a node can be safely reachable")
    print("  from multiple paths without forming a cycle.")
    print("=" * 60)
