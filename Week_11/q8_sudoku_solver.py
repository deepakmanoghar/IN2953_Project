"""
Q8. Implement a Sudoku solver using backtracking.
    For each empty cell, try digits 1-9 and check validity.
    Include the validation logic.

    SUDOKU RULES:
    -------------
    A valid Sudoku board satisfies:
      1. Each ROW contains digits 1-9 with no repetition.
      2. Each COLUMN contains digits 1-9 with no repetition.
      3. Each of the nine 3x3 SUB-BOXES contains digits 1-9
         with no repetition.

    BACKTRACKING APPROACH:
    ----------------------
    1. Find the next empty cell (marked '.' or 0).
    2. Try placing digits '1' through '9'.
    3. For each digit, check is_valid() against row, col, and box.
    4. If valid -> place the digit and recurse to the next empty cell.
    5. If the recursion returns False (dead end) -> ERASE the digit
       and try the next one (backtrack).
    6. If all 9 digits fail -> return False (trigger backtrack above).
    7. If no empty cell remains -> puzzle is solved -> return True.

    VALIDATION LOGIC (is_valid):
    -----------------------------
    For a digit d placed at (row, col):
      * ROW check:  d must not appear in board[row][0..8].
      * COL check:  d must not appear in board[0..8][col].
      * BOX check:  find the top-left corner of the 3x3 box:
                    box_row = (row // 3) * 3
                    box_col = (col // 3) * 3
                    d must not appear in that 3x3 sub-grid.

    TIME  : O(9^m)  where m = number of empty cells
    SPACE : O(m)    recursion depth = number of empty cells
"""


# =====================================================
# Validation
# =====================================================
def is_valid(board, row, col, digit):
    """
    Returns True if 'digit' can be placed at board[row][col]
    without violating Sudoku rules.

    digit is a string character ('1'..'9').
    """
    # -- Row check ---------------------------------------------------
    if digit in board[row]:
        return False

    # -- Column check ------------------------------------------------
    if digit in [board[r][col] for r in range(9)]:
        return False

    # -- 3x3 box check -----------------------------------------------
    box_row = (row // 3) * 3   # top-left row of this 3x3 box
    box_col = (col // 3) * 3   # top-left col of this 3x3 box
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == digit:
                return False

    return True                # digit is safe to place here


# =====================================================
# Sudoku Solver
# =====================================================
def solve_sudoku(board):
    """
    Solves the Sudoku board IN-PLACE using backtracking.
    Returns True if a solution exists, False otherwise.

    board: 9x9 list of lists; empty cells represented as '.'.
    """
    # -- Find the next empty cell ------------------------------------
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                # -- Try each digit 1-9 -----------------------------
                for digit in '123456789':
                    if is_valid(board, row, col, digit):
                        # -- Choose ---------------------------------
                        board[row][col] = digit

                        if solve_sudoku(board):   # recurse
                            return True

                        # -- Un-choose (backtrack) -------------------
                        board[row][col] = '.'

                # All digits 1-9 failed -> trigger backtrack above
                return False

    # No empty cell found -> puzzle is completely solved
    return True


# =====================================================
# Optimised solver with constraint sets (O(1) lookups)
# =====================================================
def solve_sudoku_optimised(board):
    """
    Same backtracking logic but uses sets for O(1) validity checks
    instead of scanning rows/cols/boxes each time.
    """
    from collections import defaultdict

    # Pre-build constraint sets from the initial board
    rows  = defaultdict(set)
    cols  = defaultdict(set)
    boxes = defaultdict(set)

    empty_cells = []

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val != '.':
                rows[r].add(val)
                cols[c].add(val)
                boxes[(r // 3, c // 3)].add(val)
            else:
                empty_cells.append((r, c))

    def backtrack(idx):
        if idx == len(empty_cells):
            return True                # all empty cells filled

        r, c   = empty_cells[idx]
        box_key = (r // 3, c // 3)

        for digit in '123456789':
            if (digit not in rows[r]
                    and digit not in cols[c]
                    and digit not in boxes[box_key]):

                # -- Choose -----------------------------------------
                board[r][c]         = digit
                rows[r].add(digit)
                cols[c].add(digit)
                boxes[box_key].add(digit)

                if backtrack(idx + 1):
                    return True

                # -- Un-choose (backtrack) ---------------------------
                board[r][c]           = '.'
                rows[r].discard(digit)
                cols[c].discard(digit)
                boxes[box_key].discard(digit)

        return False                   # no valid digit -> backtrack

    backtrack(0)
    return board


# =====================================================
# Board utilities
# =====================================================
def print_board(board, title=""):
    """Prints a Sudoku board with box separators."""
    if title:
        print(f"\n  {title}")
    print("  +-------+-------+-------+")
    for r in range(9):
        row_vals = []
        for c in range(9):
            row_vals.append(board[r][c] if board[r][c] != '.' else '.')
        print(f"  | {row_vals[0]} {row_vals[1]} {row_vals[2]} | "
              f"{row_vals[3]} {row_vals[4]} {row_vals[5]} | "
              f"{row_vals[6]} {row_vals[7]} {row_vals[8]} |")
        if r in (2, 5):
            print("  +-------+-------+-------+")
    print("  +-------+-------+-------+")


def count_empty(board):
    return sum(1 for r in range(9) for c in range(9) if board[r][c] == '.')


def copy_board(board):
    return [row[:] for row in board]


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    import time

    # -- Example puzzle ---------------------------------------------
    # A "hard" puzzle with 51 clues missing (standard difficulty)
    puzzle = [
        ['5','3','.',  '.','7','.',  '.','.','.'],
        ['6','.',  '.',  '1','9','5',  '.','.','.'],
        ['.','9','8',  '.','.',  '.',  '.','6','.'],

        ['8','.',  '.',  '.','6','.',  '.','.','3'],
        ['4','.',  '.',  '8','.','3',  '.','.','1'],
        ['7','.',  '.',  '.','2','.',  '.','.','6'],

        ['.','6','.',  '.','.',  '.',  '2','8','.'],
        ['.','.',  '.',  '4','1','9',  '.','.','5'],
        ['.',  '.',  '.',  '.','8','.',  '.','7','9'],
    ]

    print("=" * 60)
    print("  Sudoku Solver - Backtracking")
    print("=" * 60)
    print_board(puzzle, title="Unsolved Puzzle")
    print(f"\n  Empty cells: {count_empty(puzzle)}")

    # -- Solve using basic approach ---------------------------------
    board1 = copy_board(puzzle)
    t0 = time.perf_counter()
    solve_sudoku(board1)
    t1 = time.perf_counter()
    print_board(board1, title="Solved Board (basic)")
    print(f"  Time taken: {(t1 - t0) * 1000:.3f} ms")

    # -- Solve using optimised approach -----------------------------
    board2 = copy_board(puzzle)
    t0 = time.perf_counter()
    solve_sudoku_optimised(board2)
    t1 = time.perf_counter()
    print_board(board2, title="Solved Board (optimised with sets)")
    print(f"  Time taken: {(t1 - t0) * 1000:.3f} ms")

    # -- Validation walkthrough -------------------------------------
    print("\n" + "=" * 60)
    print("  is_valid() Walkthrough")
    print("=" * 60)
    print("""
    is_valid(board, row, col, digit):

    Given the board state and a candidate digit at (row, col):

    1. ROW CHECK:
       Scan all 9 cells in board[row][0..8].
       If digit is already present -> invalid.

    2. COLUMN CHECK:
       Scan all 9 cells in board[0..8][col].
       If digit is already present -> invalid.

    3. 3x3 BOX CHECK:
       Find the top-left corner of the sub-box:
         box_row = (row // 3) * 3
         box_col = (col // 3) * 3
       Scan all 9 cells in rows [box_row, box_row+3)
                              x cols [box_col, box_col+3).
       If digit is already present -> invalid.

    Optimisation (sets):
       Pre-build three dictionaries of sets:
         rows[r]  - digits placed in row r
         cols[c]  - digits placed in col c
         boxes[(r//3, c//3)] - digits placed in box
       Each lookup is O(1) instead of O(9).

    Overall is_valid cost:
       Basic  : O(9) per check  = O(27) total scans
       Optimised: O(1) per check = O(3)  total lookups
    """)

    # -- Algorithm complexity ---------------------------------------
    print("=" * 60)
    print("  Complexity Analysis")
    print("=" * 60)
    print("""
    Time Complexity : O(9^m)
      m = number of empty cells.
      At each empty cell we try at most 9 digits.
      In the absolute worst case (all cells empty, m=81):
        9^81 ~= 10^77 -- but pruning makes real puzzles solve in ms.

    Space Complexity : O(m)
      The recursion stack depth equals the number of empty cells m.
      No extra board copy needed (we mutate in-place and undo).

    Backtracking Efficiency:
      * Constraint checking prunes huge portions of the search tree.
      * A "hard" puzzle with ~51 empty cells typically requires
        only a few thousand recursive calls with good pruning.
      * Further optimisations: choose the empty cell with the
        FEWEST valid digits first (Minimum Remaining Values heuristic).
    """)
