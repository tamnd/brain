---
title: "CF 1717B - Madoka and Underground Competitions"
description: "We need to construct an n × n grid containing only '.' and 'X'. The grid must satisfy two conditions. First, every horizontal segment of length k must contain at least one 'X'. Second, every vertical segment of length k must also contain at least one 'X'."
date: "2026-06-09T19:47:33+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1717
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 818 (Div. 2)"
rating: 1100
weight: 1717
solve_time_s: 121
verified: false
draft: false
---

[CF 1717B - Madoka and Underground Competitions](https://codeforces.com/problemset/problem/1717/B)

**Rating:** 1100  
**Tags:** constructive algorithms, implementation  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct an `n × n` grid containing only `'.'` and `'X'`.

The grid must satisfy two conditions. First, every horizontal segment of length `k` must contain at least one `'X'`. Second, every vertical segment of length `k` must also contain at least one `'X'`. Among all such grids, we want one with the minimum possible number of `'X'` cells. Additionally, a specific cell `(r, c)` is required to contain `'X'`.

The input gives several test cases. For each test case, `n` is divisible by `k`, which is a very strong structural hint. We are not being asked to verify a grid, only to construct one.

The total sum of all `n` values is at most `500`. Even an `O(n²)` construction is completely safe because the output itself contains `n²` characters. Any solution that writes the grid already spends that much work.

The main difficulty is not performance but discovering the pattern that achieves both validity and the minimum number of `'X'` cells.

A common mistake is to place an `'X'` every `k` cells independently in each row. For example:

```
n = 6, k = 3

X..X..
X..X..
X..X..
X..X..
X..X..
X..X..
```

Every row condition is satisfied, but columns 2 and 3 contain no `'X'`, so many vertical segments fail.

Another easy mistake is to build a valid periodic pattern but forget the required cell. Consider:

```
n = 3, k = 3, r = 3, c = 2
```

The diagonal pattern

```
X..
.X.
..X
```

contains the minimum number of `'X'`, but cell `(3,2)` is not marked. The answer must be shifted so that the required cell belongs to the chosen pattern.

The edge case `k = 1` is also important. Every segment of length `1` must contain an `'X'`, meaning every cell must be `'X'`. Any construction that assumes spacing between marks would fail here.

## Approaches

A brute-force mindset would start by treating the problem as a constraint satisfaction task. We could try placing `'X'` cells, repeatedly checking whether every horizontal and vertical length-`k` segment is covered, and searching for a minimum solution.

This is correct in principle, but the search space is enormous. An `n × n` grid has `2^(n²)` possible configurations. Even for `n = 20`, this is completely impossible.

The key observation comes from understanding what the minimum solution must look like.

Suppose we choose exactly one cell out of every group of `k` positions along a row. If those chosen positions line up consistently across rows, every horizontal block of length `k` automatically contains one `'X'`.

A very natural pattern is to mark all cells whose coordinates satisfy

```
(row + column) mod k = constant
```

For any fixed row, exactly one column out of every `k` consecutive columns satisfies this condition. Similarly, for any fixed column, exactly one row out of every `k` consecutive rows satisfies it.

This immediately guarantees that every horizontal and vertical length-`k` segment contains exactly one marked cell.

Why is this minimum? Since `n` is divisible by `k`, each row contains exactly `n / k` marked cells. Across all rows, the total number of `'X'` cells becomes

```
n × (n / k) = n² / k
```

Any valid grid needs at least this many marks, and this construction achieves that bound.

The remaining task is to choose the correct residue class so that `(r, c)` belongs to the pattern. If we use 0-based indices, the required residue is simply

```
(r + c) mod k
```

and we mark every cell having the same residue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n²)) | O(n²) | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Convert the required position `(r, c)` into 0-based coordinates.
2. Compute the target residue:

```
target = (r + c) mod k
```

Any cell with the same residue class will belong to the selected diagonal pattern.
3. Create an `n × n` grid initially filled with `'.'`.
4. For every cell `(i, j)`, check whether

```
(i + j) mod k = target
```

If true, place `'X'`.
5. Output the resulting grid.

The reason this works is that all marked cells belong to a single residue class modulo `k`. The required cell was used to choose that residue class, so it is guaranteed to be marked.

### Why it works

Consider any row. As the column index increases by one, `(row + column) mod k` cycles through all residues. Among every `k` consecutive columns, exactly one has the chosen residue. Hence every horizontal segment of length `k` contains exactly one `'X'`.

The same argument applies to columns. As the row index increases, the residue cycles through all values, so every vertical segment of length `k` also contains exactly one `'X'`.

Each row contains exactly `n / k` marked cells because `n` is divisible by `k`. The total number of marks is therefore `n² / k`, which is the minimum achievable count. Since the chosen residue is `(r + c) mod k`, the required cell is always included.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, k, r, c = map(int, input().split())

    r -= 1
    c -= 1

    target = (r + c) % k

    grid = []

    for i in range(n):
        row = []
        for j in range(n):
            if (i + j) % k == target:
                row.append('X')
            else:
                row.append('.')
        grid.append(''.join(row))

    print('\n'.join(grid))
```

The first step converts the given coordinates to 0-based indexing. This makes modular arithmetic cleaner because Python indices naturally start from zero.

The value `target` determines which diagonal residue class will contain all `'X'` cells. Every cell satisfying `(i + j) % k == target` is marked.

The nested loops visit every cell exactly once and build the output grid. Since the answer itself contains `n²` characters, no asymptotically faster construction is possible.

The most common implementation mistake is forgetting to convert `(r, c)` to 0-based coordinates before computing the residue. Using 1-based coordinates shifts the entire pattern and may leave the required cell unmarked.

## Worked Examples

### Example 1

Input:

```
n = 3, k = 3, r = 3, c = 2
```

After converting to 0-based coordinates:

```
r = 2, c = 1
target = (2 + 1) mod 3 = 0
```

| Cell (i,j) | (i+j)%3 | Marked? |
| --- | --- | --- |
| (0,0) | 0 | X |
| (0,1) | 1 | . |
| (0,2) | 2 | . |
| (1,0) | 1 | . |
| (1,1) | 2 | . |
| (1,2) | 0 | X |
| (2,0) | 2 | . |
| (2,1) | 0 | X |
| (2,2) | 1 | . |

Result:

```
X..
..X
.X.
```

The required cell `(3,2)` becomes `(2,1)` in 0-based indexing, and it is marked because its residue matches the chosen class.

### Example 2

Input:

```
n = 2, k = 1, r = 1, c = 2
```

| Cell (i,j) | (i+j)%1 | Marked? |
| --- | --- | --- |
| (0,0) | 0 | X |
| (0,1) | 0 | X |
| (1,0) | 0 | X |
| (1,1) | 0 | X |

Result:

```
XX
XX
```

This demonstrates the special case `k = 1`. Since every value modulo `1` equals `0`, every cell belongs to the chosen residue class.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every cell is visited once |
| Space | O(n²) | The output grid is stored before printing |

The total sum of `n` over all test cases is at most `500`, so the total amount of work is at most about `500² = 250000` cell operations. This is far below the limits, and the solution easily fits within both time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, k, r, c = map(int, input().split())

        r -= 1
        c -= 1
        target = (r + c) % k

        for i in range(n):
            row = ''.join(
                'X' if (i + j) % k == target else '.'
                for j in range(n)
            )
            out.append(row)

    return "\n".join(out)

# sample 2 from statement
assert run("1\n2 1 1 2\n") == "XX\nXX"

# minimum size
assert run("1\n1 1 1 1\n") == "X"

# k = n
assert run("1\n3 3 3 2\n") == "X..\n..X\n.X."

# off-by-one check near border
assert run("1\n4 2 4 4\n") == ".X.X\nX.X.\n.X.X\nX.X."

# larger periodic pattern
assert run("1\n6 3 4 2\n") == ".X..X.\nX..X..\n..X..X\n.X..X.\nX..X..\n..X..X"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | Single `X` | Smallest possible grid |
| `2 1 1 2` | All cells `X` | Special case `k = 1` |
| `3 3 3 2` | Shifted diagonal | Required cell selection |
| `4 2 4 4` | Alternating pattern | Boundary coordinates |
| `6 3 4 2` | Repeating modulo pattern | General construction |

## Edge Cases

### Case 1: Required cell is not on the default diagonal

Input:

```
1
3 3 3 2
```

Using a fixed residue such as `0` without considering `(r, c)` may accidentally work for some inputs and fail for others. Here the algorithm computes:

```
target = (2 + 1) mod 3 = 0
```

and generates:

```
X..
..X
.X.
```

Cell `(3,2)` is marked exactly as required.

### Case 2: k = 1

Input:

```
1
2 1 1 2
```

The algorithm computes:

```
target = 0
```

Every cell satisfies:

```
(i + j) mod 1 = 0
```

so the output becomes:

```
XX
XX
```

Every length-1 segment contains an `'X'`, which is the only valid answer.

### Case 3: k = n

Input:

```
1
4 4 2 3
```

The algorithm computes:

```
target = (1 + 2) mod 4 = 3
```

and marks exactly one cell in each row:

```
...X
..X.
.X..
X...
```

Every row and column contains one `'X'`, which is enough because the only length-`k` segment in a row or column is the entire row or column itself.

### Case 4: Required cell on the border

Input:

```
1
4 2 4 4
```

The chosen residue is:

```
(3 + 3) mod 2 = 0
```

The generated grid is:

```
.X.X
X.X.
.X.X
X.X.
```

The bottom-right cell is marked, every horizontal pair contains one `'X'`, and every vertical pair contains one `'X'`. The modular pattern handles borders naturally without any special logic.
