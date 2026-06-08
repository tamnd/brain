---
title: "CF 1915B - Not Quite Latin Square"
description: "We are given a fixed 3 by 3 grid containing the characters A, B, and C, with the structure of a Latin square except for one missing cell. A valid Latin square here means that each row contains exactly one of each letter A, B, and C, and the same holds for each column."
date: "2026-06-08T19:55:22+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1915
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 918 (Div. 4)"
rating: 800
weight: 1915
solve_time_s: 89
verified: true
draft: false
---

[CF 1915B - Not Quite Latin Square](https://codeforces.com/problemset/problem/1915/B)

**Rating:** 800  
**Tags:** bitmasks, brute force, implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed 3 by 3 grid containing the characters A, B, and C, with the structure of a Latin square except for one missing cell. A valid Latin square here means that each row contains exactly one of each letter A, B, and C, and the same holds for each column.

In each test case, exactly one cell is replaced with a question mark. All other eight cells are filled correctly so that completing the Latin square uniquely determines the missing character. The task is simply to recover that missing character.

The input size is large in terms of number of test cases, up to $10^8$. Each test case is constant work: a 3 by 3 grid. This immediately implies that any solution must run in constant time per test case and avoid unnecessary overhead such as backtracking or simulation over permutations.

Since the grid size is fixed, there are no meaningful algorithmic edge cases related to dimensions. The only edge condition is the position of the missing character, which can be anywhere in the grid. A naive mistake would be to assume a fixed location for the question mark and only check that position. For example, if one assumes it is always in the middle row or column, that will fail on inputs like:

```
?AB
BCA
CAB
```

The correct answer depends on global constraints of rows and columns, not local position.

Another subtle pitfall is trying to reconstruct the missing letter by checking only the row or only the column. Either alone is insufficient because each row and column must simultaneously satisfy the permutation constraint.

## Approaches

A brute-force way to think about the problem is to try all possible letters for the question mark and verify whether the resulting grid satisfies the Latin square constraints. Since there are only three possible letters, this is already constant work per test case, but we can describe it in a more general brute-force sense: fill the missing cell with A, B, or C, and check all rows and columns.

Verification of a full 3 by 3 grid takes constant time because we only check 6 lines. So even this brute approach is effectively optimal for the constraints.

However, we can simplify further by exploiting a structural property: in every valid row of a Latin square, the three letters A, B, C appear exactly once. Therefore, if we know two letters in a row, the third is uniquely determined. The same holds for columns.

This means we do not need to test all possibilities. We can directly locate the row or column containing the question mark and compute the missing letter as the one not present in that row (or column). Since each row is guaranteed to contain exactly one missing element overall, either approach works, and row-based recovery is simplest.

We compute the full set {A, B, C}, remove the two known letters from the row containing '?', and the remaining element is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try A, B, C and validate) | O(1) per test | O(1) | Accepted |
| Optimal (set difference in row/column) | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the 3 by 3 grid for each test case. The grid is small, so we can process it directly without preprocessing.
2. Locate the position of the question mark. We do this by scanning all 9 cells. Since the grid is constant size, this scan is constant time.
3. Identify the row that contains the question mark. This row will contain exactly two known letters and one missing position.
4. Collect the characters in that row and compare them against the set {A, B, C}.
5. The missing character is the one not present in that row.
6. Output the recovered character.

The key decision is using the row containing the question mark instead of trying to combine row and column information. Since each row must contain all three letters exactly once in a valid completion, the row alone is sufficient to reconstruct the missing value.

### Why it works

Each row of a Latin square is a permutation of {A, B, C}. Removing one entry leaves exactly two distinct letters. The remaining letter is uniquely determined as the complement of that pair. Since the input is guaranteed to differ from a valid Latin square in exactly one position, the row containing the missing value still preserves this structure in its completed form. Therefore, identifying the missing element reduces to computing a deterministic set complement, which cannot yield ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

ALL = {"A", "B", "C"}

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        grid = [input().strip() for _ in range(3)]

        ans = None

        for r in range(3):
            if "?" in grid[r]:
                s = set(grid[r])
                s.discard("?")
                ans = (ALL - s).pop()
                break

        out.append(ans)

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution scans each row to find the one containing the question mark. Once found, it converts that row into a set, removes the placeholder, and computes the missing character via set difference against {A, B, C}. The `.pop()` is safe because the set difference always contains exactly one element.

The implementation relies on the fact that only one row contains the missing character, so we can break immediately after processing it. This avoids unnecessary checks.

## Worked Examples

### Example 1

Input:

```
ABC
C?B
BCA
```

| Step | Row examined | Row contents | Known letters | Missing computation | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | Row 0 | ABC | A, B, C | already complete | skip |
| 2 | Row 1 | C?B | C, B | {A, B, C} - {B, C} | A |

This confirms that the missing value is determined purely by row completeness, without needing column checks.

### Example 2

Input:

```
BCA
CA?
ABC
```

| Step | Row examined | Row contents | Known letters | Missing computation | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | Row 0 | BCA | B, C, A | complete | skip |
| 2 | Row 1 | CA? | C, A | {A, B, C} - {A, C} | B |

This shows that even when the missing element is at the end of the row, the method still works without positional assumptions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each grid is fixed size 3 by 3, so operations are constant |
| Space | O(1) | Only a fixed grid and a constant set are used |

The constraints allow up to $10^8$ test cases, so the constant-time per test case behavior is essential. Any algorithm that scales with input size beyond constant per case would be infeasible, but here every operation is bounded by a fixed number of character comparisons.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline  # placeholder, replace with solve() capture

# corrected runner
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    ALL = {"A", "B", "C"}

    t = int(input())
    out = []
    for _ in range(t):
        grid = [input().strip() for _ in range(3)]
        for r in range(3):
            if "?" in grid[r]:
                s = set(grid[r])
                s.discard("?")
                out.append((ALL - s).pop())
                break
    return "\n".join(out)

# provided samples
assert run("""3
ABC
C?B
BCA
BCA
CA?
ABC
?AB
BCA
ABC
""") == "A\nB\nC"

# custom cases
assert run("""1
ABC
BCA
CA?
""") == "B"

assert run("""1
?BC
CAB
ABC
""") == "A"

assert run("""1
ABC
A?C
BAC
""") == "B"

assert run("""1
ABC
BCA
A?C
""") == "B"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single row missing at end | B | missing at last column |
| missing at top-left | A | position independence |
| middle-row missing middle cell | B | central position handling |
| lower row missing middle cell | B | column interaction consistency |

## Edge Cases

One edge case is when the missing character appears at the first position of a row. For example:

```
?BC
CAB
ABC
```

The algorithm identifies the first row as containing the question mark. The known letters are B and C, so the set difference from {A, B, C} yields A. The position of the missing cell does not affect the computation, because set membership ignores ordering entirely.

Another case is when the missing character is in the last column:

```
ABC
BCA
CA?
```

The second row contains the question mark, and the known letters are C and A. The complement is B. The algorithm does not rely on index arithmetic, so column position has no effect.

A final structural edge case is that all rows except one are complete permutations. The algorithm still only inspects the incomplete row, so no ambiguity arises from fully valid rows elsewhere.
