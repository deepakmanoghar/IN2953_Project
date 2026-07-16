"""
Q6. Write a function to generate all valid combinations of n pairs
    of parentheses.
    Example: n=3 -> ['((()))','(()())','(())()','()(())','()()()']

    VALID PARENTHESES GENERATION:
    ------------------------------
    Build the string character by character.
    At each position we can add:
      * '('  if we still have opening brackets left  (open < n)
      * ')'  if the number of open brackets exceeds close brackets
             i.e., open > close  (there is a '(' that needs closing)

    WHY this guarantees validity:
      * Never place ')' when there is no matching '(' still open.
      * Never place more '(' than n.
      * Stop when both open == n and close == n.

    DECISION TREE for n=2:
    -----------------------
                        ""
                    open=0 close=0
                        |
                    add '('
                        |
                       "("
                   open=1 close=0
                  /            \\
            add '('           add ')'
               /                  \\
            "(("              "()"
         open=2 close=0     open=1 close=1
            |                  |
         add ')'            add '('
            |                  |
          "(()"             "()('"
       open=2 close=1     open=2 close=1
            |                  |
         add ')'            add ')'
            |                  |
          "(())"           "()()"  <- valid
       open=2 close=2
            ^
          valid

    All valid strings for n=2: ['(())', '()()']
    All valid strings for n=3: ['((()))','(()())','(())()','()(())','()()()']

    COUNT: The number of valid combinations for n pairs is the
           n-th Catalan number: C(n) = (2n)! / ((n+1)! x n!)

    TIME  : O(4^n / sqrtn)  -- the n-th Catalan number times O(n) per string
    SPACE : O(n)          -- recursion depth = 2n, string built in-place
"""


# =====================================================
# Core generator - backtracking
# =====================================================
def generate_parentheses(n):
    """
    Builds each valid string character by character.

    Parameters:
      n     - number of pairs of parentheses.

    State at each recursive call:
      current - the string built so far (as a list for O(1) append).
      open    - number of '(' placed so far.
      close   - number of ')' placed so far.
    """
    result = []

    def backtrack(current, open_count, close_count):
        # -- Base case: used all n pairs -----------------------------
        if open_count == n and close_count == n:
            result.append(''.join(current))
            return

        # -- Place '(' if we still have opening brackets left --------
        if open_count < n:
            current.append('(')
            backtrack(current, open_count + 1, close_count)
            current.pop()                      # backtrack

        # -- Place ')' only if it closes an unmatched '(' ------------
        if close_count < open_count:
            current.append(')')
            backtrack(current, open_count, close_count + 1)
            current.pop()                      # backtrack

    backtrack([], 0, 0)
    return result


# =====================================================
# Step-by-step trace version
# =====================================================
def generate_parentheses_trace(n):
    """Prints every decision point of the recursion."""
    result = []
    step   = [0]

    print(f"\n  Generating all valid parentheses for n = {n}")
    print("  " + "-" * 50)

    def backtrack(current, open_count, close_count, depth):
        indent   = "    " * depth
        current_str = ''.join(current)
        remaining   = 2 * n - len(current)

        print(f"  {indent}state: '{current_str:12s}'  "
              f"open={open_count}  close={close_count}  "
              f"remaining={remaining}")

        if open_count == n and close_count == n:
            step[0] += 1
            result.append(current_str)
            print(f"  {indent}[OK] Step {step[0]}: COMPLETE -> '{current_str}'")
            return

        if open_count < n:
            print(f"  {indent}  +- add '('  (open {open_count} < n={n})")
            current.append('(')
            backtrack(current, open_count + 1, close_count, depth + 1)
            current.pop()
            print(f"  {indent}  <- backtrack '('")

        if close_count < open_count:
            print(f"  {indent}  +- add ')'  "
                  f"(close {close_count} < open {open_count})")
            current.append(')')
            backtrack(current, open_count, close_count + 1, depth + 1)
            current.pop()
            print(f"  {indent}  <- backtrack ')'")

    backtrack([], 0, 0, 0)
    return result


# =====================================================
# Catalan number calculator
# =====================================================
def catalan_number(n):
    """Returns the n-th Catalan number: C(n) = C(2n,n) / (n+1)."""
    from math import comb
    return comb(2 * n, n) // (n + 1)


# =====================================================
# Demonstration
# =====================================================
if __name__ == "__main__":

    # -- Trace for n=2 (small, readable) ---------------------------
    print("=" * 60)
    print("  Decision Tree Trace  -  n = 2")
    print("=" * 60)
    generate_parentheses_trace(2)

    # -- Results for n=1 through n=4 -------------------------------
    for n in range(1, 5):
        combos = generate_parentheses(n)
        print("\n" + "=" * 60)
        print(f"  n = {n}  ->  {catalan_number(n)} combination(s)")
        print("=" * 60)
        for i, s in enumerate(combos, 1):
            print(f"    {i:2}. {s}")

    # -- n=3 explicit (as asked in question) -----------------------
    print("\n" + "=" * 60)
    print("  n = 3  (Question Example)")
    print("=" * 60)
    n3 = generate_parentheses(3)
    print(f"\n  Result = {n3}\n")

    # -- Catalan number table ---------------------------------------
    print("=" * 60)
    print("  Catalan Numbers  C(n) = (2n)! / ((n+1)! x n!)")
    print("=" * 60)
    print()
    for n in range(1, 9):
        count = catalan_number(n)
        print(f"    n = {n}  ->  C({n}) = {count:4d} combinations")

    # -- Key logic explanation --------------------------------------
    print("\n" + "=" * 60)
    print("  Key Decision Rules")
    print("=" * 60)
    print("""
    At each step, we can add a character only if:

    Add '(' when:  open_count < n
      -> We still have opening brackets to place.

    Add ')' when:  close_count < open_count
      -> There exists an unmatched '(' that needs closing.
      -> Ensures we never have more ')' than '(' at any prefix.

    These two rules jointly ensure:
      1. Exactly n '(' are placed (from rule 1).
      2. Exactly n ')' are placed (string ends when both == n).
      3. No prefix ever has more ')' than '('  -> always valid.

    Why backtracking?
      We explore the '(' branch first (deeper open counts),
      then explore the ')' branch. If a branch leads to an
      invalid state (e.g., close >= open), it is simply never
      entered -- implicit pruning with no explicit undo needed
      for the validity check itself (only pop() for state).

    Time  Complexity : O(4^n / sqrtn)
      This is the n-th Catalan number x O(n) per string built.

    Space Complexity : O(n)
      Recursion depth = 2n; 'current' list holds <= 2n chars.
    """)
