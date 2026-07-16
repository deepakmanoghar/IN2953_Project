"""
Q4. Solve the N-Queens problem for n=4.
    Draw all valid board configurations.
    Explain the is_safe() check for diagonals.

    N-QUEENS PROBLEM:
    -----------------
    Place n queens on an nxn chessboard so that NO two queens
    threaten each other.  Queens attack along:
      * the same ROW
      * the same COLUMN
      * either DIAGONAL (main and anti)

    APPROACH:
    ---------
    Place queens one per row (so ROW conflicts are impossible by design).
    For each row, try every column and check column + diagonal safety.

    is_safe(board, row, col, n):
    -----------------------------------------------------------------
    We only look at ROWS ABOVE the current row (queens already placed).

    1. COLUMN CHECK
       Walk up in the same column: board[r][col] == 'Q'
         (r from row-1 down to 0)

    2. UPPER-LEFT DIAGONAL CHECK (NW)
       r = row-1, c = col-1  ->  r--, c-- each step
       Cells on the main diagonal satisfy (row-r) == (col-c).

    3. UPPER-RIGHT DIAGONAL CHECK (NE)
       r = row-1, c = col+1  ->  r--, c++ each step
       Cells on the anti-diagonal satisfy (row-r) == (c-col).

    VALID BOARDS for n=4:
    ---------------------
    Solution 1:          Solution 2:
    . Q . .              . . Q .
    . . . Q              Q . . .
    Q . . .              . . . Q
    . . Q .              . Q . .

    TIME  : O(n!)   -- at row k there are at most (n-k) valid columns
    SPACE : O(n^2)   -- board storage; recursion depth = n
"""


# =====================================================
# Safety check
# =====================================================
def is_safe(board, row, col, n):
    """
    Returns True if placing a queen at (row, col) is safe.
    Only checks rows ABOVE because rows below are not yet placed.

    Three checks:
      1. Same column
      2. Upper-left diagonal  (NW)
      3. Upper-right diagonal (NE)
    """
    # 1. Column check ------------------------------------------------
    for r in range(row):
        if board[r][col] == 'Q':
            return False

    # 2. Upper-left diagonal (NW) -------------------------------------
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == 'Q':
            return False
        r -= 1
        c -= 1

    # 3. Upper-right diagonal (NE) ------------------------------------
    r, c = row - 1, col + 1
    while r >= 0 and c < n:
        if board[r][c] == 'Q':
            return False
        r -= 1
        c += 1

    return True


# =====================================================
# N-Queens solver
# =====================================================
def solve_n_queens(n):
    """
    Places queens row by row.
    board[r][c] is either '.' (empty) or 'Q' (queen).
    """
    # Initialise empty board
    board  = [['.' for _ in range(n)] for _ in range(n)]
    result = []

    def backtrack(row):
        # Base case: all n queens placed successfully
        if row == n:
            result.append([''.join(r) for r in board])
            return

        for col in range(n):
            if is_safe(board, row, col, n):
                # -- Choose -----------------------------------------
                board[row][col] = 'Q'

                backtrack(row + 1)

                # -- Un-choose (backtrack) ---------------------------
                board[row][col] = '.'

    backtrack(0)
    return result


# =====================================================
# Pretty-print a board
# =====================================================
def print_board(board, title=""):
    """Displays a board with row/column indices and queens."""
    n = len(board)
    if title:
        print(f"\n  {title}")
    col_header = "    " + "  ".join(str(c) for c in range(n))
    print(col_header)
    print("    " + "--" * n)
    for r, row in enumerate(board):
        row_str = "  ".join(cell for cell in row)
        print(f"  {r} | {row_str}")


# =====================================================
# Diagonal explanation visualiser
# =====================================================
def explain_diagonal_check(n=4, row=2, col=1):
    """
    Prints a board that highlights the three is_safe() checks
    for a queen placed at (row, col).
    """
    print(f"\n  is_safe() visual for n={n}, placing queen at "
          f"row={row}, col={col}")
    print("  " + "-" * 40)

    board = [['.' for _ in range(n)] for _ in range(n)]
    board[row][col] = 'Q'   # the queen we are testing

    # Mark column cells above
    for r in range(row):
        if board[r][col] == '.':
            board[r][col] = '|'   # column threat

    # Mark upper-left diagonal
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == '.':
            board[r][c] = '\\'
        r -= 1; c -= 1

    # Mark upper-right diagonal
    r, c = row - 1, col + 1
    while r >= 0 and c < n:
        if board[r][c] == '.':
            board[r][c] = '/'
        r -= 1; c += 1

    col_header = "    " + "  ".join(str(c) for c in range(n))
    print(col_header)
    print("    " + "--" * n)
    for r, row_data in enumerate(board):
        row_str = "  ".join(cell for cell in row_data)
        print(f"  {r} | {row_str}")

    print("""
    Legend:
      Q  = queen being placed (current position)
      |  = column threat      (check 1)
      \\ = upper-left diagonal (check 2, NW)
      /  = upper-right diag  (check 3, NE)
      .  = not checked (rows below not yet filled)
    """)


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    n = 4

    # -- is_safe() explanation --------------------------------------
    print("=" * 60)
    print("  is_safe() Diagonal Check Explained")
    print("=" * 60)
    explain_diagonal_check(n=4, row=2, col=1)

    # -- Solve for n=4 ---------------------------------------------
    print("=" * 60)
    print(f"  N-Queens Solver  -  n = {n}")
    print("=" * 60)
    solutions = solve_n_queens(n)
    print(f"\n  Found {len(solutions)} solution(s) for n = {n}:\n")

    for idx, sol in enumerate(solutions, 1):
        print_board(sol, title=f"Solution {idx}")
        print()

    # -- Solutions for various n ------------------------------------
    print("=" * 60)
    print("  N-Queens Solution Counts")
    print("=" * 60)
    print()
    for size in range(1, 10):
        count = len(solve_n_queens(size))
        print(f"    n = {size}  ->  {count:4d} solution(s)")

    # -- is_safe() code walkthrough ---------------------------------
    print("\n" + "=" * 60)
    print("  is_safe() Walkthrough")
    print("=" * 60)
    print("""
    WHY only check rows above?
      We place queens one row at a time from top to bottom.
      Rows below the current row are all empty, so threats can
      only come from already-placed queens (rows 0 .. row-1).

    CHECK 1 -- Column:
      Iterate r from (row-1) down to 0.
      If board[r][col] == 'Q' -> same column -> NOT safe.

    CHECK 2 -- Upper-Left Diagonal (NW):
      Start at (row-1, col-1), step r--, c-- each iteration.
      Diagonal condition: row - r == col - c  (same difference)
      Stop when r < 0 or c < 0.

    CHECK 3 -- Upper-Right Diagonal (NE):
      Start at (row-1, col+1), step r--, c++ each iteration.
      Anti-diagonal condition: row - r == c - col
      Stop when r < 0 or c >= n.

    Optimisation -- O(1) checks using hash sets:
      * cols      : set of occupied columns
      * diag1     : set of (row - col) values  (NW diagonals)
      * diag2     : set of (row + col) values  (NE diagonals)
      All three sets allow O(1) lookup, reducing each call to O(1).

    Time  Complexity : O(n!)
      At row 0: n choices; row 1: <= n-1; … row n-1: <= 1.
      Upper bound: n x (n-1) x … x 1 = n!

    Space Complexity : O(n^2)
      Board is nxn; recursion depth is n.
    """)
