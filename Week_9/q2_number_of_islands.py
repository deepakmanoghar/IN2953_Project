"""
Q2. Number of Islands: Given a 2D grid of '1's (land) and '0's (water),
    count the number of islands using DFS.

    DEFINITION:
    -----------
    An island is a maximal group of '1's connected horizontally or vertically
    (not diagonally). The grid is surrounded by water on all sides.

    ALGORITHM:
    -----------
    Iterate over every cell in the grid.
    When we find a '1' (unvisited land):
      1. Increment island counter.
      2. Run DFS from that cell to "sink" (mark as '0') all land cells
         that belong to the same island.
    Result: the counter equals the number of distinct islands.

    TIME COMPLEXITY:
    -----------
    O(M x N)  where M = rows, N = cols.
    Every cell is visited at most once — once sunk it is never revisited.

    SPACE COMPLEXITY:
    -----------
    O(M x N) in the worst case for the DFS call stack
    (e.g. a grid that is entirely land).
"""


# =====================================================
# DFS flood-fill helper
# =====================================================
def _dfs_sink(grid, r, c):
    """
    Sink all connected land cells reachable from (r, c).
    Modifies the grid in-place by turning '1' -> '0'.
    """
    rows, cols = len(grid), len(grid[0])

    # Base cases: out of bounds or already water
    if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
        return

    grid[r][c] = '0'          # mark visited (sink)

    # Explore all 4 directions
    _dfs_sink(grid, r - 1, c)   # up
    _dfs_sink(grid, r + 1, c)   # down
    _dfs_sink(grid, r, c - 1)   # left
    _dfs_sink(grid, r, c + 1)   # right


# =====================================================
# Iterative version (avoids recursion depth issues)
# =====================================================
def _dfs_sink_iterative(grid, r, c):
    """Same flood-fill using an explicit stack (no recursion limit concern)."""
    rows, cols = len(grid), len(grid[0])
    stack = [(r, c)]
    while stack:
        row, col = stack.pop()
        if row < 0 or row >= rows or col < 0 or col >= cols:
            continue
        if grid[row][col] != '1':
            continue
        grid[row][col] = '0'
        stack.extend([(row-1,col),(row+1,col),(row,col-1),(row,col+1)])


# =====================================================
# Main function: count islands
# =====================================================
def num_islands(grid, iterative=False):
    """
    Count the number of islands in a 2D grid.

    Args:
        grid      : list[list[str]] — '1' = land, '0' = water
        iterative : bool — use iterative DFS if True

    Returns:
        int — number of islands
    """
    if not grid or not grid[0]:
        return 0

    # Work on a deep copy to preserve the original grid
    import copy
    g = copy.deepcopy(grid)

    count = 0
    rows, cols = len(g), len(g[0])

    for r in range(rows):
        for c in range(cols):
            if g[r][c] == '1':
                count += 1
                if iterative:
                    _dfs_sink_iterative(g, r, c)
                else:
                    _dfs_sink(g, r, c)

    return count


# =====================================================
# Helper: pretty-print grid
# =====================================================
def print_grid(grid, title="Grid"):
    print(f"\n  {title}:")
    for row in grid:
        print("    " + " ".join(row))


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        {
            "label": "Example 1 (1 island)",
            "grid": [
                ["1","1","1","1","0"],
                ["1","1","0","1","0"],
                ["1","1","0","0","0"],
                ["0","0","0","0","0"],
            ],
            "expected": 1,
        },
        {
            "label": "Example 2 (3 islands)",
            "grid": [
                ["1","1","0","0","0"],
                ["1","1","0","0","0"],
                ["0","0","1","0","0"],
                ["0","0","0","1","1"],
            ],
            "expected": 3,
        },
        {
            "label": "All land (1 island)",
            "grid": [
                ["1","1"],
                ["1","1"],
            ],
            "expected": 1,
        },
        {
            "label": "All water (0 islands)",
            "grid": [
                ["0","0"],
                ["0","0"],
            ],
            "expected": 0,
        },
        {
            "label": "Checkerboard (4 islands)",
            "grid": [
                ["1","0","1"],
                ["0","1","0"],
                ["1","0","1"],
            ],
            "expected": 5,
        },
        {
            "label": "Single row",
            "grid": [["1","0","1","0","1"]],
            "expected": 3,
        },
    ]

    print("=" * 55)
    print("Number of Islands -- DFS Flood-Fill")
    print("=" * 55)

    for tc in test_cases:
        grid     = tc["grid"]
        expected = tc["expected"]
        r_rec  = num_islands(grid, iterative=False)
        r_iter = num_islands(grid, iterative=True)
        print_grid(grid, tc["label"])
        print(f"    Recursive DFS : {r_rec}  islands")
        print(f"    Iterative DFS : {r_iter}  islands")
        match = "[OK]" if r_rec == r_iter == expected else "[X]"
        print(f"    Expected      : {expected}  {match}")

    print("\n" + "=" * 55)
    print("ALGORITHM WALKTHROUGH (Example 2):")
    print("  Start scanning the grid left-to-right, top-to-bottom.")
    print("  (r=0,c=0) -> '1' found -> island #1 -> DFS sinks all")
    print("               connected land -> (0,0),(0,1),(1,0),(1,1)")
    print("  (r=2,c=2) -> '1' found -> island #2 -> DFS sinks (2,2)")
    print("  (r=3,c=3) -> '1' found -> island #3 -> DFS sinks (3,3),(3,4)")
    print()
    print("TIME  COMPLEXITY: O(M x N)  -- every cell visited at most once")
    print("SPACE COMPLEXITY: O(M x N)  -- DFS call stack (worst case: all land)")
    print("=" * 55)
