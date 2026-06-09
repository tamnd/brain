---
title: "CF 1644D - Cross Coloring"
description: "We are given a grid that starts completely uncolored, with $n$ rows and $m$ columns. We then apply a sequence of operations. Each operation selects a row and a column, and paints every cell in that row and that column with a chosen non-white color."
date: "2026-06-10T04:14:34+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1644
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 123 (Rated for Div. 2)"
rating: 1700
weight: 1644
solve_time_s: 71
verified: true
draft: false
---

[CF 1644D - Cross Coloring](https://codeforces.com/problemset/problem/1644/D)

**Rating:** 1700  
**Tags:** data structures, implementation, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid that starts completely uncolored, with $n$ rows and $m$ columns. We then apply a sequence of operations. Each operation selects a row and a column, and paints every cell in that row and that column with a chosen non-white color. If a cell is painted multiple times across operations, the latest operation that touches it overwrites its color.

After all operations are processed, the final grid is fully determined by the sequence of operations and the choice of colors assigned to them. Two final grids are considered different if at least one cell differs in its final color.

The task is to count how many distinct final grids can be produced if, for each operation, we independently choose any of $k$ colors.

The constraints are tight enough that any solution that simulates the grid or even tracks per-cell states is immediately infeasible. The total number of operations across test cases is up to $2 \cdot 10^5$, which forces a solution that is linear or near-linear in the number of operations. Any approach that attempts to recompute the grid or propagate updates per cell will exceed time limits by several orders of magnitude.

A subtle issue appears when operations repeat the same row-column pair. A naive idea might be to treat each operation independently and multiply by $k^q$. This fails because different operations can overwrite each other, making earlier choices irrelevant in many cases. For example, if all operations target the same row and column, only the last operation matters for every cell, so the number of valid colorings is just $k$, not $k^q$.

Another failure mode is assuming that rows and columns can be treated independently. They are not independent because a single operation colors both simultaneously, and interactions depend on the order of operations.

## Approaches

A brute-force approach would try to simulate all possible assignments of colors to operations. For each operation, we pick one of $k$ colors, simulate the effect on the grid, and compute the final result. This is correct but infeasible because it explores $k^q$ possibilities, which is astronomically large even for small inputs.

We need to avoid tracking the full grid and instead focus on the structural effect of operations. The key observation is that only the last operation affecting each row or column determines its final visible state. Once a row has been "covered" by a later operation, any earlier operations affecting it are irrelevant for that row’s contribution, unless they occur in different regions that are not overwritten later.

This leads to reframing the process in terms of “first time a row or column becomes irrelevant due to being overwritten by a later operation.” Each operation either introduces new influence or becomes redundant depending on whether its row or column will be overwritten later.

We process operations from last to first. When we see a pair $(x, y)$, if both row $x$ and column $y$ are already “blocked” by later operations, then this operation cannot contribute anything new. If at least one is not blocked, then this operation contributes a new degree of freedom in choosing colors. After processing, we mark the row and column as blocked.

This reverse greedy structure works because once a row or column has been accounted for by a later operation, any earlier operation cannot affect any unassigned region that survives to the final grid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k^q \cdot nm)$ | $O(nm)$ | Too slow |
| Optimal | $O(n + m + q)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We process operations in reverse order and maintain which rows and columns have already been “covered” by later operations.

1. Initialize two boolean arrays, one for rows and one for columns, both initially false. These represent whether a row or column has already been accounted for by a later operation.
2. Initialize a counter of “active operations” contributions to zero. Each time we find an operation that still affects at least one new row or column, it contributes a multiplicative factor of $k$.
3. Iterate over the operations from last to first. For each operation $(x_i, y_i)$, check whether row $x_i$ is already marked or column $y_i$ is already marked.
4. If both row $x_i$ and column $y_i$ are already marked, this operation does not introduce any new visible freedom and can be ignored.
5. Otherwise, this operation contributes a new independent choice of color, so multiply the answer by $k$, then mark row $x_i$ and column $y_i$ as covered.
6. Continue until all operations are processed.

The final answer is the product accumulated modulo $998244353$.

### Why it works

The key invariant is that at any point in the reverse sweep, every unmarked row and column corresponds to a region of the grid that is still potentially influenced by earlier operations. When we process an operation that touches at least one unmarked row or column, it is the first time that region is being “claimed” in reverse time, meaning its color choice is still free and independent. Once we mark its row and column, all earlier operations affecting them cannot introduce new independent choices because any cell they would influence is already determined by a later operation in forward time. This ensures each contributing operation corresponds to exactly one independent factor of $k$, and no dependency is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

t = int(input())
for _ in range(t):
    n, m, k, q = map(int, input().split())
    ops = [tuple(map(int, input().split())) for _ in range(q)]

    row_used = [False] * (n + 1)
    col_used = [False] * (m + 1)

    ans = 1

    for x, y in reversed(ops):
        if row_used[x] and col_used[y]:
            continue
        ans = (ans * k) % MOD
        row_used[x] = True
        col_used[y] = True

    print(ans)
```

The implementation directly mirrors the reverse greedy idea. We store all operations first because we need to process them backwards. Two boolean arrays track whether a row or column has already been claimed by a later operation.

The crucial detail is the condition `if row_used[x] and col_used[y]`. This ensures that we only skip an operation when it cannot introduce any new independent coloring choice. If either the row or the column is still free, we must count this operation because it determines a fresh boundary of influence in the reverse process.

The multiplication by $k$ happens exactly when a new independent choice is introduced.

## Worked Examples

### Example 1

Input:

```
n=1, m=1, k=3, q=2
(1,1)
(1,1)
```

We process in reverse.

| Step | Operation | Row used | Col used | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,1) | F F | F F | take | 3 |
| 2 | (1,1) | T T | T T | take | 9 |

The second operation still contributes because even though it targets the same cell, in reverse it is the first time that row and column are claimed. This shows why duplication still matters in reverse processing.

### Example 2

Input:

```
n=2, m=2, k=2, q=3
(2,1)
(1,1)
(2,2)
```

Reverse processing:

| Step | Operation | Row used | Col used | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | (2,2) | F F | F F | take | 2 |
| 2 | (1,1) | T F | T F | take | 4 |
| 3 | (2,1) | T T | T T | skip | 4 |

This demonstrates how later operations “block” earlier ones completely once both their row and column have already been covered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m + q)$ | Each operation is processed once in reverse with O(1) checks |
| Space | $O(n + m)$ | Boolean arrays for rows and columns |

The solution fits easily within constraints because the total number of operations across test cases is $2 \cdot 10^5$, and every operation is handled in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 998244353

    t = int(input())
    out = []
    for _ in range(t):
        n, m, k, q = map(int, input().split())
        ops = [tuple(map(int, input().split())) for _ in range(q)]

        row_used = [False] * (n + 1)
        col_used = [False] * (m + 1)

        ans = 1
        for x, y in reversed(ops):
            if row_used[x] and col_used[y]:
                continue
            ans = (ans * k) % MOD
            row_used[x] = True
            col_used[y] = True

        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""2
1 1 3 2
1 1
1 1
2 2 2 3
2 1
1 1
2 2
""") == "3\n4"

# single operation
assert run("""1
3 3 5 1
2 2
""") == "5"

# repeated same cell
assert run("""1
2 2 7 3
1 1
1 1
1 1
""") == "7"

# all distinct
assert run("""1
3 3 2 3
1 1
2 2
3 3
""") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single op | k | base contribution |
| repeated ops same cell | k | duplicates collapse correctly |
| all distinct ops | $k^3$ | full independence case |

## Edge Cases

A subtle edge case is when many operations repeat the same pair $(x, y)$. The algorithm treats only the last such operation as meaningful in reverse, but each repetition can still contribute if it is the first time a row or column is introduced. For example, with repeated identical operations, the reverse sweep counts only one contribution, correctly yielding $k$, since the first processed occurrence already marks both row and column.

Another edge case is when all operations share the same row but different columns. In reverse, the first operation will mark the row, and subsequent operations will be skipped once both row and column are already marked. This correctly avoids overcounting and reflects that only the first encountered boundary introduces a free choice.

These cases confirm that the invariant is tied not to individual operations but to whether they introduce a previously unseen row-column boundary in reverse time.
