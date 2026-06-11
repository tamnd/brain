---
title: "CF 1413B - A New Technique"
description: "We are given all rows of an unknown matrix and all columns of the same matrix. The catch is that both collections are shuffled. The rows are presented in arbitrary order, and the columns are also presented in arbitrary order. Inside a row, the left-to-right order is preserved."
date: "2026-06-11T07:21:04+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1413
codeforces_index: "B"
codeforces_contest_name: "Technocup 2021 - Elimination Round 1"
rating: 1100
weight: 1413
solve_time_s: 143
verified: true
draft: false
---

[CF 1413B - A New Technique](https://codeforces.com/problemset/problem/1413/B)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given all rows of an unknown matrix and all columns of the same matrix.

The catch is that both collections are shuffled. The rows are presented in arbitrary order, and the columns are also presented in arbitrary order. Inside a row, the left-to-right order is preserved. Inside a column, the top-to-bottom order is preserved.

Every value from `1` to `n * m` appears exactly once in the matrix. Because all values are distinct, each number uniquely identifies a cell.

The task is to reconstruct the original matrix.

The constraints are the main clue. Although `n` and `m` can each reach `500`, the total number of matrix cells across all test cases is at most `250000`. This means a solution proportional to the number of cells is easily fast enough. A solution that repeatedly compares every row with every column and scans entire arrays inside those comparisons would approach `O(n * m * min(n,m))`, which is unnecessary and risks becoming slow near the limits.

The structure of the input hides a very useful property: every number is unique. That means if we know where one value belongs in the final row ordering, we immediately know the position of every row containing that value.

A common mistake is to try matching rows against all columns and rebuilding the matrix cell by cell. Consider:

```
n = 2, m = 3

Rows:
6 5 4
1 2 3

Columns:
1 6
2 5
3 4
```

If we arbitrarily choose the first row as the top row, we obtain:

```
6 5 4
1 2 3
```

This matrix does not match the column order. The correct reconstruction is:

```
1 2 3
6 5 4
```

The row order must be determined from the columns, not guessed.

Another subtle case occurs when `m = 1`.

```
Rows:
3
1
2

Column:
3 1 2
```

There is only one column, so that column completely determines the row ordering:

```
3
1
2
```

Any solution that assumes multiple columns exist or always uses the first row as an anchor can fail here.

## Approaches

A brute-force approach would try to determine the correct row order by comparing every row against every column. Since every value is unique, one could search for where a row's first element appears inside a column and use that information to place the row.

This works, but implemented naively it repeatedly scans rows and columns. With up to 250,000 total cells, unnecessary repeated searches create far more work than needed.

The key observation is that every value appears exactly once in the entire matrix.

Suppose `n <= m`. Then every column contains `n` values. If we inspect any row, its first element must appear in exactly one position inside one of the columns. That position is precisely the row index of that row in the final matrix.

Even better, Codeforces' intended solution uses the dimension with fewer entries per sequence.

When `n <= m`, we read the rows first and build a mapping:

```
first element of row -> row contents
```

Then we inspect the columns. The column containing one of those first elements reveals the complete row ordering because its top-to-bottom order is exactly the order of rows in the matrix.

When `n > m`, the same idea works symmetrically by using columns instead.

For this particular problem, an even simpler formulation is enough.

Every row is uniquely identified by its first element. Among the given columns, exactly one column contains those first elements. Once we find that column, its order immediately gives the order of rows in the answer.

This reduces reconstruction to a few hash-table lookups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m) | O(nm) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Read all `n` rows and store them.
2. Create a dictionary mapping the first element of each row to the entire row.

This allows us to recover a row instantly when we know its first value.
3. Read all `m` columns.
4. Find the column that contains one of the stored row-first-elements.

Since every row's first element appears exactly once in the matrix, there is exactly one column whose entries are precisely the first elements of all rows.
5. Use the order of values in that column to determine the row order.

If the column contains:

```
a
b
c
```

then the rows beginning with `a`, `b`, and `c` must appear in that order in the final matrix.
6. Output the corresponding rows.

### Why it works

Every row is uniquely identified by its first element because all matrix values are distinct.

Consider the column that contains the first element of the top row. Since columns preserve top-to-bottom order, that same column also contains the first elements of every other row in their correct vertical order.

Once that column is found, the sequence of first elements uniquely determines the sequence of rows. Replacing each first element with its corresponding row reconstructs the entire matrix. Because the problem guarantees a unique valid matrix, no ambiguity remains.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        rows = [list(map(int, input().split())) for _ in range(n)]

        pos = {}
        for row in rows:
            pos[row[0]] = row

        answer_order = None

        for _ in range(m):
            col = list(map(int, input().split()))

            if answer_order is None:
                for x in col:
                    if x in pos:
                        answer_order = col
                        break

        for first_value in answer_order:
            out.append(" ".join(map(str, pos[first_value])))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution stores every row in a dictionary keyed by its first element.

While reading columns, we search for the special column containing row-leading values. Because all values are unique, once a column contains any row-leading value, that column is exactly the column formed by all row-leading values. Its ordering is the desired row ordering.

After discovering that column, reconstruction becomes a sequence of dictionary lookups.

A common implementation mistake is to stop after finding a matching value without keeping the entire column. The whole column is needed because it provides the ordering of all rows, not just one row.

Another easy mistake is assuming the matching column must be the first column read. The columns are shuffled, so every column must be checked until the correct one is found.

## Worked Examples

### Example 1

Input:

```
n = 2, m = 3

Rows:
6 5 4
1 2 3

Columns:
1 6
2 5
3 4
```

Dictionary construction:

| First Element | Stored Row |
| --- | --- |
| 6 | [6,5,4] |
| 1 | [1,2,3] |

Column scan:

| Column | Contains Row First Element? | Action |
| --- | --- | --- |
| [1,6] | Yes | Select this column |

Recovered order:

| Value in Selected Column | Output Row |
| --- | --- |
| 1 | [1,2,3] |
| 6 | [6,5,4] |

Final matrix:

```
1 2 3
6 5 4
```

This example shows the central idea. The column `[1,6]` directly tells us the vertical order of rows.

### Example 2

Input:

```
n = 3, m = 1

Rows:
3
1
2

Column:
3 1 2
```

Dictionary construction:

| First Element | Stored Row |
| --- | --- |
| 3 | [3] |
| 1 | [1] |
| 2 | [2] |

Column scan:

| Column | Contains Row First Element? | Action |
| --- | --- | --- |
| [3,1,2] | Yes | Select |

Recovered order:

| Value | Output Row |
| --- | --- |
| 3 | [3] |
| 1 | [1] |
| 2 | [2] |

Final matrix:

```
3
1
2
```

This demonstrates that the method works even when there is only one column.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every matrix value is read a constant number of times |
| Space | O(nm) | Stores all rows and the lookup dictionary |

The total number of cells across all test cases is at most 250,000. A linear pass over those cells is comfortably within the time limit, and storing the matrix requires only a few megabytes of memory.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        rows = [list(map(int, input().split())) for _ in range(n)]

        pos = {row[0]: row for row in rows}

        answer_order = None

        for _ in range(m):
            col = list(map(int, input().split()))

            if answer_order is None:
                for x in col:
                    if x in pos:
                        answer_order = col
                        break

        for x in answer_order:
            out.append(" ".join(map(str, pos[x])))

    return "\n".join(out)

# provided sample
assert run(
"""2
2 3
6 5 4
1 2 3
1 6
2 5
3 4
3 1
2
3
1
3 1 2
"""
) == (
"""1 2 3
6 5 4
3
1
2"""
)

# minimum size
assert run(
"""1
1 1
1
1
"""
) == "1"

# single column
assert run(
"""1
3 1
3
1
2
3 1 2
"""
) == (
"""3
1
2"""
)

# single row
assert run(
"""1
1 4
1 2 3 4
1
2
3
4
"""
) == "1 2 3 4"

# reordered rows and columns
assert run(
"""1
3 2
5 6
1 2
3 4
1 3 5
2 4 6
"""
) == (
"""1 2
3 4
5 6"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 matrix | same single value | Minimum boundary |
| 3×1 matrix | column order preserved | Single-column handling |
| 1×4 matrix | original row | Single-row handling |
| Shuffled rows | reconstructed matrix | Correct row ordering recovery |

## Edge Cases

Consider the single-column case:

```
1
3 1
3
1
2
3 1 2
```

The dictionary becomes:

```
3 -> [3]
1 -> [1]
2 -> [2]
```

The only column is `[3,1,2]`. That column is selected as the ordering column. Looking up each value yields:

```
[3]
[1]
[2]
```

which is exactly the correct matrix.

Consider a case where the first row in the input is not the top row:

```
1
2 3
6 5 4
1 2 3
1 6
2 5
3 4
```

A careless solution might output rows in input order:

```
6 5 4
1 2 3
```

The algorithm instead finds the column `[1,6]`, interprets it as the vertical ordering of row leaders, and outputs:

```
1 2 3
6 5 4
```

which matches all columns.

Consider a single-row matrix:

```
1
1 4
1 2 3 4
1
2
3
4
```

The row dictionary contains only one entry. Every column consists of a single value. The first matching column immediately identifies the only row, and the algorithm outputs the unique valid matrix unchanged.
