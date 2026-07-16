"""
Q6. Longest Common Subsequence (LCS):
    Find the LCS of 'abcde' and 'ace'.
    Draw the complete DP table.
    How would you reconstruct the actual subsequence?

    LONGEST COMMON SUBSEQUENCE:
    ----------------------------
    A subsequence is obtained by deleting some characters (without
    changing the relative order). LCS finds the longest subsequence
    common to both strings.

    Example: 'abcde' and 'ace'  ->  LCS = 'ace', length = 3

    RECURRENCE:
    -----------
    Let s1 = 'abcde', s2 = 'ace'
    dp[i][j] = LCS length of s1[0..i-1] and s2[0..j-1]

    if s1[i-1] == s2[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1     (match: extend by 1)
    else:
        dp[i][j] = max(dp[i-1][j],       (skip s1[i-1])
                       dp[i][j-1])       (skip s2[j-1])

    BASE CASES:
    -----------
    dp[0][j] = 0  (empty s1 has no common chars with any s2)
    dp[i][0] = 0  (empty s2 has no common chars with any s1)

    COMPLETE DP TABLE for 'abcde' vs 'ace':
    -----------------------------------------
        ""  a  c  e
    ""   0  0  0  0
    a    0  1  1  1
    b    0  1  1  1
    c    0  1  2  2
    d    0  1  2  2
    e    0  1  2  3   <- answer = dp[5][3] = 3

    RECONSTRUCTION:
    ---------------
    Start at dp[m][n]. Trace backwards:
      If s1[i-1]==s2[j-1]: this char is in LCS -> go to dp[i-1][j-1]
      Else if dp[i-1][j] > dp[i][j-1]: go up   (dp[i-1][j])
      Else: go left (dp[i][j-1])

    TIME  : O(m x n)
    SPACE : O(m x n) for full table, O(min(m,n)) for space-optimised
"""


# =====================================================
# Core LCS  --  returns length only
# =====================================================
def lcs_length(s1, s2):
    """
    Builds the full (m+1) x (n+1) dp table.
    Returns dp[m][n] = LCS length.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


# =====================================================
# LCS with reconstruction
# =====================================================
def lcs_with_sequence(s1, s2):
    """Returns (length, lcs_string) by building + backtracking the table."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct the LCS string
    lcs  = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])   # this char is in LCS
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1                   # came from above
        else:
            j -= 1                   # came from the left

    lcs.reverse()
    return dp[m][n], ''.join(lcs), dp


# =====================================================
# Space-optimised (rolling two rows)
# =====================================================
def lcs_space_optimised(s1, s2):
    """
    Only keep two rows of the dp table at a time.
    Space O(n) instead of O(m*n).
    """
    m, n = len(s1), len(s2)
    # Ensure s2 is the shorter string for minimal space
    if m < n:
        s1, s2 = s2, s1
        m, n   = n, m

    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, [0] * (n + 1)

    return prev[n]


# =====================================================
# Table printer
# =====================================================
def print_dp_table(s1, s2, dp):
    """Prints the full DP table with row and column headers."""
    n = len(s2)
    # Header row
    header = f"  {'':>4}"
    for ch in ('""' + s2):
        header += f"  {ch:>2}"
    print(header)
    print("  " + "-" * (6 + 4 * (n + 2)))

    for i, row in enumerate(dp):
        if i == 0:
            label = '""'
        else:
            label = s1[i - 1]
        row_str = f"  {label:>4}"
        for v in row:
            row_str += f"  {v:>2}"
        print(row_str)


# =====================================================
# Reconstruction trace
# =====================================================
def reconstruction_trace(s1, s2, dp):
    """Prints the step-by-step backtrack path through the DP table."""
    print(f"\n  Backtrack reconstruction:")
    print(f"  Start at dp[{len(s1)}][{len(s2)}] = {dp[len(s1)][len(s2)]}")
    print(f"  " + "-" * 50)

    i, j = len(s1), len(s2)
    lcs  = []
    step = 1
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            print(f"  Step {step}: s1[{i-1}]='{s1[i-1]}' == s2[{j-1}]='{s2[j-1]}' "
                  f"-> IN LCS, move to dp[{i-1}][{j-1}]={dp[i-1][j-1]}")
            lcs.append(s1[i - 1])
            i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            print(f"  Step {step}: s1[{i-1}]='{s1[i-1]}' != s2[{j-1}]='{s2[j-1]}' "
                  f"-> move UP to dp[{i-1}][{j}]={dp[i-1][j]}")
            i -= 1
        else:
            print(f"  Step {step}: s1[{i-1}]='{s1[i-1]}' != s2[{j-1}]='{s2[j-1]}' "
                  f"-> move LEFT to dp[{i}][{j-1}]={dp[i][j-1]}")
            j -= 1
        step += 1

    lcs.reverse()
    print(f"\n  LCS = '{''.join(lcs)}'")


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":
    s1 = 'abcde'
    s2 = 'ace'

    # -- Build table and show ----------------------------------------
    length, seq, dp = lcs_with_sequence(s1, s2)

    print("=" * 60)
    print("  LCS -- Complete DP Table")
    print("=" * 60)
    print(f"\n  s1 = '{s1}'   s2 = '{s2}'\n")
    print_dp_table(s1, s2, dp)

    # -- Reconstruction trace ----------------------------------------
    print("\n" + "=" * 60)
    print("  Reconstruction Trace (backtrack through table)")
    print("=" * 60)
    reconstruction_trace(s1, s2, dp)

    # -- Final answer ------------------------------------------------
    print("\n" + "=" * 60)
    print("  Result")
    print("=" * 60)
    print(f"\n  s1     = '{s1}'")
    print(f"  s2     = '{s2}'")
    print(f"  LCS    = '{seq}'")
    print(f"  Length = {length}")

    # -- Compare all approaches --------------------------------------
    r1 = lcs_length(s1, s2)
    r2 = lcs_space_optimised(s1, s2)
    print(f"\n  Full table result     : {r1}")
    print(f"  Space-optimised result: {r2}")
    assert r1 == r2 == length

    # -- Additional test cases ---------------------------------------
    print("\n" + "=" * 60)
    print("  Additional Test Cases")
    print("=" * 60)
    tests = [
        ('abcba', 'abcbcba'),
        ('AGGTAB', 'GXTXAYB'),
        ('abc', 'abc'),
        ('abc', 'def'),
        ('', 'abc'),
        ('ABCBDAB', 'BDCAB'),
    ]
    for a, b in tests:
        ln, sq, _ = lcs_with_sequence(a, b)
        print(f"\n  '{a}' vs '{b}'")
        print(f"    LCS = '{sq}',  length = {ln}")

    # -- Variants and applications -----------------------------------
    print("\n" + "=" * 60)
    print("  Real-world Applications of LCS")
    print("=" * 60)
    print("""
    1. DIFF tools (git diff, Unix diff):
       Find differences between two files by computing LCS of lines.

    2. DNA Sequence Alignment:
       Find the longest common genetic subsequence.

    3. Spell Checkers / Edit Distance:
       LCS is related to Levenshtein edit distance:
         edit_distance = m + n - 2 * lcs_length(s1, s2)

    4. Plagiarism Detection:
       Compare documents by finding common subsequences.

    COMPLEXITY:
      Time  : O(m x n)    -- fill the entire dp table
      Space : O(m x n)    -- store the full table (needed for reconstruction)
              O(min(m,n)) -- if only the length is needed (rolling rows)

    RELATED PROBLEMS:
      - Shortest Common Supersequence (SCS)
      - Longest Common Substring (contiguous -- different from LCS)
      - Edit Distance (Levenshtein)
      - Print all LCS (exponential in the worst case)
    """)
