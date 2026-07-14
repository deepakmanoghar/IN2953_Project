"""
Q7. Search a 2D matrix where each row and column is sorted.
    Write an O(m+n) solution.
    Example: search for 5 in [[1,4,7],[2,5,8],[3,6,9]].

    MATRIX STRUCTURE:
    -----------------
    Each row is sorted left-to-right AND each column is sorted top-to-bottom.
    (Note: this is different from LeetCode 74 where rows are also globally sorted.)

    O(m+n) ALGORITHM -- "Staircase Search":
    ----------------------------------------
    Start at the TOP-RIGHT corner (row=0, col=n-1).
    At each step:
      - If matrix[row][col] == target  -> FOUND!
      - If matrix[row][col] >  target  -> move LEFT  (col -= 1)
                                          current column is too large
      - If matrix[row][col] <  target  -> move DOWN  (row += 1)
                                          current row is too small

    WHY IT WORKS:
    Starting at top-right, we have a "staircase" property:
      - Moving LEFT decreases the value (elements to the left are smaller).
      - Moving DOWN increases the value (elements below are larger).
    At each step we eliminate either an entire ROW or an entire COLUMN.
    After at most m+n steps, we either find the target or exhaust options.

    WHY NOT TOP-LEFT or BOTTOM-RIGHT?
    - Top-left (min): moving right OR down both increase value -> ambiguous.
    - Bottom-right (max): moving left OR up both decrease -> ambiguous.
    - Top-right / bottom-left are the unique corners with one direction
      increasing and one decreasing -> unambiguous decision each step.

    TIME  : O(m + n)  -- at most m downward + n leftward moves
    SPACE : O(1)
"""


# =====================================================
# O(m+n) Staircase Search
# =====================================================
def search_matrix(matrix, target):
    """
    Search 'target' in a row-sorted and column-sorted matrix.
    Starts at top-right corner.

    Args:
        matrix : list[list[int]] -- m x n matrix
        target : int

    Returns:
        tuple (row, col) if found, else (-1, -1)
    """
    if not matrix or not matrix[0]:
        return (-1, -1)

    rows = len(matrix)
    cols = len(matrix[0])

    row = 0           # start at TOP row
    col = cols - 1    # start at RIGHT-MOST column

    while row < rows and col >= 0:
        val = matrix[row][col]

        if val == target:
            return (row, col)
        elif val > target:
            col -= 1        # too large -> move LEFT
        else:
            row += 1        # too small -> move DOWN

    return (-1, -1)


# =====================================================
# Bottom-left variant (equivalent alternative)
# =====================================================
def search_matrix_bottom_left(matrix, target):
    """
    Same algorithm but starts at the BOTTOM-LEFT corner.
      - If val > target -> move UP    (row -= 1)
      - If val < target -> move RIGHT (col += 1)
    """
    if not matrix or not matrix[0]:
        return (-1, -1)

    rows = len(matrix)
    cols = len(matrix[0])
    row  = rows - 1   # bottom
    col  = 0          # left

    while row >= 0 and col < cols:
        val = matrix[row][col]
        if val == target:
            return (row, col)
        elif val > target:
            row -= 1    # move UP
        else:
            col += 1    # move RIGHT

    return (-1, -1)


# =====================================================
# Brute force O(m*n) for verification
# =====================================================
def search_matrix_brute(matrix, target):
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == target:
                return (r, c)
    return (-1, -1)


# =====================================================
# Verbose trace showing staircase path
# =====================================================
def search_matrix_verbose(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    row, col   = 0, cols - 1
    step       = 0

    print(f"\n  Target: {target}")
    print(f"  {'Step':>4} | {'(row,col)':>9} | {'val':>5} | Decision")
    print(f"  {'-'*4}-+-{'-'*9}-+-{'-'*5}-+-{'-'*30}")

    while row < rows and col >= 0:
        val  = matrix[row][col]
        step += 1

        if val == target:
            decision = f"FOUND at ({row},{col})!"
        elif val > target:
            decision = f"{val} > {target} -> move LEFT  (col {col}->{col-1})"
        else:
            decision = f"{val} < {target} -> move DOWN  (row {row}->{row+1})"

        print(f"  {step:>4} | ({row},{col})     | {val:>5} | {decision}")

        if val == target:
            return (row, col)
        elif val > target:
            col -= 1
        else:
            row += 1

    print(f"  {step+1:>4} | out of bounds -- NOT FOUND")
    return (-1, -1)


# =====================================================
# Pretty-print matrix with path highlighted
# =====================================================
def print_matrix(matrix, highlight=None, title="Matrix"):
    print(f"\n  {title}:")
    for r, row in enumerate(matrix):
        line = "    "
        for c, val in enumerate(row):
            if highlight and (r, c) == highlight:
                line += f"[{val:2}]"
            else:
                line += f" {val:2} "
        print(line)


# =====================================================
# LeetCode 74 variant: strictly sorted matrix (each row continues from prev)
# =====================================================
def search_matrix_lc74(matrix, target):
    """
    O(log(m*n)) -- treat the matrix as a flat sorted array and binary search.
    Works ONLY when rows are globally sorted (row i+1 starts > row i ends).
    """
    if not matrix:
        return False
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


# -----------------------------------------------------
# Driver
# -----------------------------------------------------
if __name__ == "__main__":
    matrix = [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
    ]
    target = 5

    print("=" * 60)
    print("SEARCH IN ROW/COLUMN SORTED MATRIX  (O(m+n) Staircase)")
    print("=" * 60)
    print_matrix(matrix, title="Input matrix")

    # ── Verbose trace ─────────────────────────────────
    print("\n" + "=" * 60)
    print("VERBOSE TRACE (top-right start):")
    print("=" * 60)
    result = search_matrix_verbose(matrix, target)
    print_matrix(matrix, highlight=result if result != (-1,-1) else None,
                 title=f"Result: target={target} at {result}")

    # ── Both variants ─────────────────────────────────
    print("\n" + "=" * 60)
    print("BOTH CORNER STRATEGIES:")
    print("=" * 60)
    for t in [1, 5, 9, 6, 10]:
        tr  = search_matrix(matrix, t)
        bl  = search_matrix_bottom_left(matrix, t)
        bf  = search_matrix_brute(matrix, t)
        ok  = "[OK]" if tr == bl == bf else "[X]"
        print(f"  target={t:<3}  top-right={tr}  bottom-left={bl}  brute={bf}  {ok}")

    # ── Larger matrix test ────────────────────────────
    print("\n" + "=" * 60)
    print("LARGER MATRIX TEST (5x5):")
    print("=" * 60)
    big = [
        [ 1,  5,  9, 13, 17],
        [ 2,  6, 10, 14, 18],
        [ 3,  7, 11, 15, 19],
        [ 4,  8, 12, 16, 20],
        [21, 22, 23, 24, 25],
    ]
    print_matrix(big, title="5x5 row+col sorted")
    for t in [11, 1, 25, 100, 4]:
        r = search_matrix(big, t)
        b = search_matrix_brute(big, t)
        ok = "[OK]" if r == b else "[X]"
        print(f"  target={t:<4}: found={r}  {ok}")

    print("\n" + "=" * 60)
    print("WHY O(m+n) STAIRCASE WORKS:")
    print("  Start at top-right corner (largest in row 0).")
    print("    val > target -> can't be in this column -> move LEFT.")
    print("    val < target -> can't be in this row    -> move DOWN.")
    print("  Each step eliminates one row OR one column.")
    print("  Maximum steps = m (rows eliminated) + n (cols eliminated).")
    print("  Total: O(m+n).")
    print()
    print("  Top-left  DOES NOT work: both right and down increase value.")
    print("  Top-right WORKS:         left decreases, down increases -> unambiguous.")
    print("=" * 60)
