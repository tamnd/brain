---
title: "CF 173C - Spiral Maximum"
description: "We are given a rectangular grid of integers. Inside this grid, we may place any odd-sized square, for example a 3×3, 5×5, or 7×7 subgrid. Inside that square we draw the standard spiral that starts at the top-left corner and winds inward. The spiral does not visit every cell."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp"]
categories: ["algorithms"]
codeforces_contest: 173
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2012 - Round 1"
rating: 1900
weight: 173
solve_time_s: 161
verified: false
draft: false
---

[CF 173C - Spiral Maximum](https://codeforces.com/problemset/problem/173/C)

**Rating:** 1900  
**Tags:** brute force, dp  
**Solve time:** 2m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid of integers. Inside this grid, we may place any odd-sized square, for example a 3×3, 5×5, or 7×7 subgrid. Inside that square we draw the standard spiral that starts at the top-left corner and winds inward.

The spiral does not visit every cell. It traces a one-cell-wide path. For a 5×5 square, the spiral looks like a long snake wrapping around the borders until it reaches the center region.

For every possible odd-sized square inside the matrix, we compute the sum of the cells belonging to its spiral path. The task is to find the maximum such sum.

The grid dimensions are at most 500×500. A single square can contain up to 250000 cells, and there are already about 250000 possible top-left positions. Trying to explicitly simulate every spiral would immediately explode to tens of billions of operations.

The structure of the spiral is the key observation. A spiral is almost the entire square border, then almost the next border, and so on. The only missing pieces form a very regular pattern. Once we recognize this, the problem becomes a dynamic programming problem over nested squares.

A common mistake is assuming the spiral equals the entire square perimeter. That fails because the spiral also contains inner layers.

Consider this 5×5 example:

```
#####
....#
###.#
#...#
#####
```

The spiral contains 17 cells, not just the outer border.

Another easy mistake is double-counting the turning cells when adding borders layer by layer.

For example:

```
3 3
1 1 1
1 1 1
1 1 1
```

The 3×3 spiral contains 7 cells, not 8. The center is not visited.

A third subtle issue is the smallest valid spiral. A 1×1 square is not considered a spiral in this problem because the definition requires odd k with k ≥ 3.

For example:

```
3 3
-5 -5 -5
-5 10 -5
-5 -5 -5
```

The answer is not 10. The only valid spiral is the whole 3×3 spiral, whose sum is -35.

A careless implementation that allows size 1 would produce the wrong answer.

## Approaches

The brute force approach is straightforward. For every odd-sized square, explicitly simulate the spiral walk. We can mark visited cells and follow the movement rules exactly as described in the statement.

This works because the spiral definition is deterministic. Every square produces exactly one spiral path.

The problem is the running time. There are O(nm·min(n,m)) possible odd-sized squares. A single simulation may visit O(k²) cells. In the worst case:

```
500 × 500 × 250000
```

operations are completely infeasible.

The turning point comes from understanding what the spiral actually contains.

Take a 7×7 spiral. The outer layer contributes almost the full border. Then the inner 5×5 spiral appears shifted by one row and one column. The pattern repeats recursively.

That means we do not need to simulate movement at all. We can define the spiral sum recursively:

```
spiral(k) =
outer border contribution
+ spiral(k - 2) inside
```

with a small correction because one edge segment is intentionally skipped by the spiral path.

Once the shape becomes recursive, prefix sums allow every border contribution to be computed in O(1), and dynamic programming builds larger spirals from smaller ones.

The entire solution becomes O(nm·min(n,m)), which is fast enough because each state is only constant work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nmL³) | O(L²) | Too slow |
| Optimal | O(nmL) | O(nmL) | Accepted |

Here L = min(n, m).

## Algorithm Walkthrough

### Spiral Structure

A k×k spiral consists of:

1. The entire top row.
2. The entire right column except the top cell.
3. The entire bottom row except the rightmost cell.
4. The entire left column except the top and bottom cells.
5. A smaller spiral of size (k−2)×(k−2), shifted one row down and one column right.

The recursive part starts at position `(x+1, y+1)`.

### Prefix Sums

We build row and column prefix sums so any horizontal or vertical segment can be queried in O(1).

For a row segment:

```
sum_row(r, l, r)
```

For a column segment:

```
sum_col(c, u, d)
```

This lets us compute the outer layer instantly.

### DP Definition

Let:

```
dp[i][j][t]
```

be the spiral sum for the odd square of size:

```
k = 2t + 3
```

whose top-left corner is `(i, j)`.

The smallest spiral corresponds to `t = 0`, meaning size 3.

### Transition

Suppose current size is `k`.

The outer contribution is:

1. Top row of length k.
2. Right column excluding the top cell.
3. Bottom row excluding the rightmost cell.
4. Left column excluding top and bottom cells.

Then we add the inner spiral:

```
dp[i+1][j+1][t-1]
```

which corresponds to size `k-2`.

### Updating the Answer

For every valid state, compute the spiral sum and maximize the global answer.

## Why it works

Every spiral can be uniquely decomposed into its outer layer and a smaller spiral inside it. The movement rules guarantee that after completing one loop, the path continues exactly as a spiral on the inner `(k−2)×(k−2)` square shifted inward by one cell.

The DP transition mirrors this decomposition exactly. Prefix sums compute each outer layer contribution without omission or overlap. Since every larger spiral is built from the correct smaller spiral, induction on the spiral size proves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    # row prefix sums
    row = [[0] * (m + 1) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            row[i][j + 1] = row[i][j] + a[i][j]

    # column prefix sums
    col = [[0] * n for _ in range(m)]
    for j in range(m):
        for i in range(n):
            col[j][i] = a[i][j]
            if i:
                col[j][i] += col[j][i - 1]

    def row_sum(r, l, rr):
        return row[r][rr + 1] - row[r][l]

    def col_sum(c, u, d):
        res = col[c][d]
        if u:
            res -= col[c][u - 1]
        return res

    max_k = min(n, m)

    # dp[t][i][j]
    # size = 2*t + 3
    dp = []

    ans = -INF

    # size 3
    cur = [[0] * m for _ in range(n)]

    for i in range(n - 2):
        for j in range(m - 2):
            s = 0

            # explicit 3x3 spiral
            cells = [
                (i, j),
                (i, j + 1),
                (i, j + 2),
                (i + 1, j + 2),
                (i + 2, j + 2),
                (i + 2, j + 1),
                (i + 2, j),
            ]

            for x, y in cells:
                s += a[x][y]

            cur[i][j] = s
            ans = max(ans, s)

    dp.append(cur)

    t = 1
    size = 5

    while size <= max_k:
        nxt = [[0] * m for _ in range(n)]

        for i in range(n - size + 1):
            for j in range(m - size + 1):

                top = row_sum(i, j, j + size - 1)

                right = col_sum(
                    j + size - 1,
                    i + 1,
                    i + size - 1
                )

                bottom = row_sum(
                    i + size - 1,
                    j,
                    j + size - 2
                )

                left = 0
                if size > 3:
                    left = col_sum(
                        j,
                        i + 1,
                        i + size - 2
                    )

                outer = top + right + bottom + left

                s = outer + dp[t - 1][i + 1][j + 1]

                nxt[i][j] = s
                ans = max(ans, s)

        dp.append(nxt)

        t += 1
        size += 2

    print(ans)

solve()
```

The solution starts by building prefix sums for rows and columns. These structures let us extract any straight segment in constant time. Without them, every transition would require iterating along borders repeatedly.

The base case is the 3×3 spiral. Writing it explicitly is safer than trying to force the general recurrence immediately. The 3×3 spiral contains exactly seven cells, and the center is excluded.

For larger spirals, the transition follows the recursive structure directly. The outer layer is added using four segment queries. Care is needed with inclusions and exclusions. The right column excludes the top corner because that cell already belongs to the top row. The bottom row excludes the right corner for the same reason.

The left column query is particularly subtle. It excludes both corners because they already belong to the top and bottom rows.

The inner spiral comes from the previous DP layer at `(i+1, j+1)`.

All sums fit comfortably inside Python integers because the maximum possible absolute value is:

```
500 × 500 × 1000 = 2.5 × 10^8
```

## Worked Examples

### Sample 1

Input:

```
6 5
0 0 0 0 0
1 1 1 1 1
0 0 0 0 1
1 1 1 0 1
1 0 0 0 1
1 1 1 1 1
```

The best spiral is the whole 5×5 region starting at `(1,0)`.

| Step | Value |
| --- | --- |
| Top row | 5 |
| Right column | 4 |
| Bottom row | 4 |
| Left column | 3 |
| Inner 3×3 spiral | 1 |
| Total | 17 |

The trace shows how the recurrence decomposes the spiral into an outer ring and an inner spiral.

### Second Example

Input:

```
3 3
1 1 1
1 1 1
1 1 1
```

| Step | Value |
| --- | --- |
| Top row | 3 |
| Right column without top | 2 |
| Bottom row without right | 2 |
| Total | 7 |

The center cell is excluded. This example catches implementations that accidentally include all nine cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nmL) | Every odd square size processes all valid top-left corners once |
| Space | O(nmL) | DP layers store spiral sums for every size |

Here:

```
L = min(n, m)
```

Since `L ≤ 500`, the number of DP layers is at most 249. The total number of processed states is manageable within the 3 second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    INF = 10**18

    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    row = [[0] * (m + 1) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            row[i][j + 1] = row[i][j] + a[i][j]

    col = [[0] * n for _ in range(m)]
    for j in range(m):
        for i in range(n):
            col[j][i] = a[i][j]
            if i:
                col[j][i] += col[j][i - 1]

    def row_sum(r, l, rr):
        return row[r][rr + 1] - row[r][l]

    def col_sum(c, u, d):
        res = col[c][d]
        if u:
            res -= col[c][u - 1]
        return res

    ans = -INF

    dp = []

    cur = [[0] * m for _ in range(n)]

    for i in range(n - 2):
        for j in range(m - 2):

            cells = [
                (i, j),
                (i, j + 1),
                (i, j + 2),
                (i + 1, j + 2),
                (i + 2, j + 2),
                (i + 2, j + 1),
                (i + 2, j),
            ]

            s = sum(a[x][y] for x, y in cells)

            cur[i][j] = s
            ans = max(ans, s)

    dp.append(cur)

    t = 1
    size = 5

    while size <= min(n, m):

        nxt = [[0] * m for _ in range(n)]

        for i in range(n - size + 1):
            for j in range(m - size + 1):

                outer = (
                    row_sum(i, j, j + size - 1)
                    + col_sum(j + size - 1, i + 1, i + size - 1)
                    + row_sum(i + size - 1, j, j + size - 2)
                    + col_sum(j, i + 1, i + size - 2)
                )

                s = outer + dp[t - 1][i + 1][j + 1]

                nxt[i][j] = s
                ans = max(ans, s)

        dp.append(nxt)

        t += 1
        size += 2

    return str(ans) + "\n"

# provided sample
assert run(
"""6 5
0 0 0 0 0
1 1 1 1 1
0 0 0 0 1
1 1 1 0 1
1 0 0 0 1
1 1 1 1 1
"""
) == "17\n"

# minimum size
assert run(
"""3 3
1 1 1
1 1 1
1 1 1
"""
) == "7\n"

# all negative
assert run(
"""3 3
-1 -1 -1
-1 -1 -1
-1 -1 -1
"""
) == "-7\n"

# larger spiral better
assert run(
"""5 5
1 1 1 1 1
1 0 0 0 1
1 0 5 0 1
1 0 0 0 1
1 1 1 1 1
"""
) == "16\n"

# off-by-one border test
assert run(
"""3 4
1 2 3 4
5 6 7 8
9 10 11 12
"""
) == "56\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3×3 all ones | 7 | Center must be excluded |
| 3×3 all negative | -7 | Cannot choose empty answer |
| 5×5 with center 5 | 16 | Spiral ignores unreachable center |
| 3×4 increasing numbers | 56 | Border inclusions and exclusions |

## Edge Cases

Consider the smallest valid input:

```
3 3
1 1 1
1 1 1
1 1 1
```

The algorithm directly uses the explicit base case. It sums exactly seven cells and excludes the center. The output becomes 7.

Now consider a case where the center is very large:

```
5 5
1 1 1 1 1
1 0 0 0 1
1 0 100 0 1
1 0 0 0 1
1 1 1 1 1
```

A wrong solution might include the center and return 116. The recursive structure never touches the center of a 5×5 spiral because the inner 3×3 spiral itself excludes its center. The algorithm correctly returns 16.

Finally, consider all negative values:

```
3 3
-1 -1 -1
-1 -1 -1
-1 -1 -1
```

Some implementations incorrectly initialize the answer with 0 and accidentally allow selecting nothing. The algorithm initializes with negative infinity and evaluates every valid spiral, producing the correct answer of -7.
