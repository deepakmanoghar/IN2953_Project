"""
Q5. Word Search: Given a 2D board and a word, determine if the word
    exists in the grid. Implement with backtracking.
    Handle the visited cell constraint.

    WORD SEARCH:
    ------------
    Starting from any cell that matches word[0], perform a DFS exploring
    all 4 neighbours (up, down, left, right) to build the word letter
    by letter. A cell may NOT be reused within the same path.

    VISITED CELL CONSTRAINT:
    -------------------------
    We must not revisit a cell in the CURRENT path (but we can use
    the same cell in a DIFFERENT search path from a different start).

    Two strategies:
      1. Use a 'visited' boolean matrix (reset on backtrack).
      2. Temporarily overwrite board[r][c] with a sentinel (e.g., '#')
         and restore it on backtrack -- no extra O(mxn) space needed.

    EXAMPLE:
    --------
    Board:
      A  B  C  E
      S  F  C  S
      A  D  E  E

    Word = "ABCCED"
    Path: A(0,0) -> B(0,1) -> C(0,2) -> C(1,2) -> E(2,2) -> D(2,1) [OK]

    Word = "SEE"
    Path: S(1,3) -> E(2,3) -> E(2,2) [OK]

    Word = "ABCB"
    Path: A(0,0) -> B(0,1) -> C(0,2) -> B? B(0,1) already visited [X]

    TIME  : O(m x n x 4^L)  where L = len(word)
              mxn starting cells, each DFS explores 4^L paths
    SPACE : O(L)            recursion stack depth = L
"""


# =====================================================
# Approach 1 - In-place marking (no extra visited array)
# =====================================================
def word_search(board, word):
    """
    Tries every cell as a starting point.
    Marks visited cells with '#' temporarily and restores on backtrack.
    """
    if not board or not word:
        return False

    rows, cols = len(board), len(board[0])
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    def dfs(r, c, index):
        """Returns True if word[index:] can be built starting at (r, c)."""
        # -- Base case: all characters matched ----------------------
        if index == len(word):
            return True

        # -- Boundary and character mismatch check ------------------
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[index]:
            return False

        # -- Mark as visited (overwrite with sentinel) ---------------
        original   = board[r][c]
        board[r][c] = '#'

        # -- Explore all 4 neighbours --------------------------------
        for dr, dc in DIRECTIONS:
            if dfs(r + dr, c + dc, index + 1):
                board[r][c] = original   # restore before returning True
                return True

        # -- Backtrack: restore original character -------------------
        board[r][c] = original
        return False

    # Try every cell as a potential starting position
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True

    return False


# =====================================================
# Approach 2 - Explicit visited matrix
# =====================================================
def word_search_visited(board, word):
    """
    Uses a separate boolean 'visited' matrix.
    Easier to reason about; slightly more memory (O(mxn)).
    """
    if not board or not word:
        return False

    rows, cols = len(board), len(board[0])
    visited    = [[False] * cols for _ in range(rows)]
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(r, c, index):
        if index == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if visited[r][c] or board[r][c] != word[index]:
            return False

        # -- Choose: mark visited ------------------------------------
        visited[r][c] = True

        for dr, dc in DIRECTIONS:
            if dfs(r + dr, c + dc, index + 1):
                visited[r][c] = False   # restore before returning True
                return True

        # -- Un-choose: unmark visited -------------------------------
        visited[r][c] = False
        return False

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True

    return False


# =====================================================
# Trace version: prints every step of the DFS
# =====================================================
def word_search_trace(board, word):
    """Shows the DFS path and backtracking steps."""
    if not board or not word:
        return False

    rows, cols = len(board), len(board[0])
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    DIR_NAMES  = {(-1,0): "up", (1,0): "down", (0,-1): "left", (0,1): "right"}
    found      = [False]

    def dfs(r, c, index, path, depth):
        indent = "  " * depth

        if index == len(word):
            found[0] = True
            print(f"{indent}[OK] FOUND! Complete path: {path}")
            return True

        if (r < 0 or r >= rows or c < 0 or c >= cols
                or board[r][c] == '#' or board[r][c] != word[index]):
            return False

        print(f"{indent}-> ({r},{c})='{board[r][c]}' matches word[{index}]"
              f"='{word[index]}'  path={path}")

        original    = board[r][c]
        board[r][c] = '#'

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if dfs(nr, nc, index + 1, path + [(nr, nc)], depth + 1):
                board[r][c] = original
                return True

        board[r][c] = original
        print(f"{indent}<- backtrack from ({r},{c})")
        return False

    print(f"\n  Searching for '{word}' in board:")
    for row in board:
        print("    " + "  ".join(row))
    print()

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                print(f"  -- Try start at ({r},{c})='{word[0]}' --")
                if dfs(r, c, 0, [(r, c)], 1):
                    return True

    if not found[0]:
        print(f"  [X] Word '{word}' NOT found.")
    return found[0]


# =====================================================
# Board printer
# =====================================================
def print_board(board, title=""):
    if title:
        print(f"\n  {title}")
    cols = len(board[0])
    print("    " + "  ".join(str(c) for c in range(cols)))
    print("    " + "--" * cols)
    for r, row in enumerate(board):
        print(f"  {r}|  " + "  ".join(row))


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    board_data = [
        ['A','B','C','E'],
        ['S','F','C','S'],
        ['A','D','E','E']
    ]

    print("=" * 60)
    print("  Board")
    print("=" * 60)
    print_board(board_data)

    # -- Trace for "ABCCED" -----------------------------------------
    print("\n" + "=" * 60)
    print("  Trace: word = 'ABCCED'")
    print("=" * 60)
    import copy
    word_search_trace(copy.deepcopy(board_data), "ABCCED")

    # -- Quick results for several words ---------------------------
    print("\n" + "=" * 60)
    print("  Test Cases")
    print("=" * 60)
    test_words = ["ABCCED", "SEE", "ABCB", "SFCS", "ABCD"]
    for w in test_words:
        result = word_search(copy.deepcopy(board_data), w)
        status = "[OK]  Found" if result else "[X]  Not found"
        print(f"\n  '{w:8s}' -> {status}")

    # -- Visited cell explanation -----------------------------------
    print("\n" + "=" * 60)
    print("  Visited Cell Constraint -- Explanation")
    print("=" * 60)
    print("""
    WHY we need a 'visited' constraint:
      Without it, the DFS could loop back and reuse a cell.
      Example: searching "ABA" starting at (0,0)='A':
        A(0,0) -> B(0,1) -> A(0,0)  <- same cell used twice! [X]

    IMPLEMENTATION -- two equivalent strategies:

    Strategy 1: Sentinel overwrite (space-efficient)
      * Replace board[r][c] with '#' before recursing.
      * Restore board[r][c] = original after recursing (backtrack).
      * '#' never matches any letter -> auto-blocked in future steps.
      * Extra space: O(1).

    Strategy 2: Visited matrix (explicit, easy to reason about)
      * visited[r][c] = True before recursing.
      * visited[r][c] = False after recursing (backtrack).
      * Extra space: O(m x n).

    Both strategies correctly allow the same cell to be used in a
    DIFFERENT path (from a different starting cell or branch).

    Complexity:
      Time  : O(m x n x 4^L)
        mxn starting cells; each DFS explores at most 4^L paths.
      Space : O(L)
        Recursion depth equals word length L.
    """)
