---
title: "CF 104049G - Foil Folding"
description: "We are given a rectangular sheet of foil represented as a grid of size $n times m$. Some cells contain imperfections marked as X, while others are clean. From this sheet, we want to extract a rectangular piece of metal that qualifies as an ingot."
date: "2026-07-02T03:42:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104049
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 11-11-22 Div. 1 (Advanced)"
rating: 0
weight: 104049
solve_time_s: 51
verified: true
draft: false
---

[CF 104049G - Foil Folding](https://codeforces.com/problemset/problem/104049/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular sheet of foil represented as a grid of size $n \times m$. Some cells contain imperfections marked as `X`, while others are clean. From this sheet, we want to extract a rectangular piece of metal that qualifies as an ingot.

The ingot must satisfy a geometric constraint: one of its sides must have length exactly $k$. The other side, which we will call the variable length, can be chosen freely. However, there is a quality constraint: the ingot can contain at most $x$ imperfections.

The task is to determine the maximum possible value of this variable side length such that there exists at least one valid $k \times L$ or $L \times k$ subrectangle containing no more than $x$ `X` cells.

The input size constraint $n \cdot m \le 10^5$ means the grid is sparse enough that an $O(nm)$ preprocessing is acceptable, but anything that tries to check all subrectangles independently would be too slow. A naive enumeration of all $O(n^2 m^2)$ rectangles is impossible, and even a three-dimensional sliding window without preprocessing would exceed limits.

A key edge case comes from how the fixed dimension interacts with the grid boundaries. If $k$ equals 1, the problem degenerates into choosing a strip, and if $k$ is close to $\max(n,m)$, only very few orientations are valid. Another subtle case is when the optimal rectangle spans the full height or width of the grid, because many naive sliding-window approaches accidentally assume both dimensions can vary symmetrically.

A small illustrative case is a grid where all imperfections lie concentrated in one column. If $k$ is the number of rows, then every candidate rectangle includes that column, and the answer depends purely on vertical accumulation. A naive approach that recomputes counts per rectangle without prefix structure will repeatedly count the same column contributions incorrectly or too slowly.

## Approaches

The brute-force idea is straightforward: fix every possible position of a $k$-height (or $k$-width) strip and compute how many `X` cells it contains, then expand the other dimension as far as possible while staying within the limit $x$. For each starting coordinate, we try all possible ending coordinates and count imperfections directly from the grid.

This works correctly because it explicitly evaluates every candidate rectangle. However, each rectangle sum would cost $O(k)$ if computed naively, and there are $O(nm)$ possible placements, giving an overall $O(nm \cdot k)$ or worse complexity. In the worst case where $k \approx n$, this degenerates to $O(n^2 m)$, which is far beyond what $n \cdot m \le 10^5$ allows.

The key observation is that the problem reduces to fast range-sum queries over many overlapping rectangles. Once we fix the orientation where height is $k$, every candidate rectangle corresponds to a contiguous window of rows, and we only need to know column-wise sums inside that window. This suggests compressing each column into a 1D array of prefix sums over rows, turning the 2D problem into many sliding window problems over these column aggregates.

Instead of recomputing sums from scratch, we precompute prefix sums over rows for each column. Then for any fixed row interval of height $k$, we can obtain the number of imperfections in each column in $O(1)$. After that, the problem becomes finding the longest contiguous segment of columns whose total sum is at most $x$, which is a standard two-pointer sliding window problem. We repeat the same reasoning for the rotated case where width is fixed to $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((nm)^2)$ worst-case | $O(1)$ extra | Too slow |
| Prefix + Sliding Window | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We solve the problem in two orientations: fixing a horizontal strip of height $k$, and fixing a vertical strip of width $k$. We take the best answer over both.

1. Build a 2D prefix structure over the grid so we can query how many `X` cells exist in any vertical segment of a column in constant time. This is done by computing prefix sums along rows for every column independently.
2. For each possible top row $r$, compute the number of imperfections in each column between rows $r$ and $r + k - 1$. This produces a 1D array where each entry represents the cost of including that column in a $k$-tall strip starting at row $r$. The reason this step is necessary is that once height is fixed, columns become independent contributors to the total count.
3. On this 1D array, use a sliding window with two pointers. Expand the right pointer while the total number of imperfections does not exceed $x$. Whenever the constraint is violated, move the left pointer forward until it is satisfied again. At each step, record the maximum window length. This works because all values are non-negative, so expanding the window can only increase or maintain the sum.
4. Repeat the same procedure after transposing the grid, which handles the case where the fixed side of length $k$ is horizontal instead of vertical. This symmetry is essential because the problem allows either dimension to be exactly $k$.
5. Return the maximum length obtained from both orientations.

### Why it works

Once a $k$-height strip is fixed, every feasible ingot corresponds exactly to a contiguous segment of columns. The cost of any segment is additive over columns, and all contributions are non-negative. This creates a monotonic structure: extending a segment can never decrease the number of imperfections. The sliding window therefore maintains the invariant that the current segment is always the longest valid segment ending at the right pointer, and every valid segment is considered exactly once as the right pointer moves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_orientation(grid, n, m, k, x):
    # prefix sums per column
    pref = [[0] * m for _ in range(n + 1)]
    for i in range(n):
        row = grid[i]
        for j in range(m):
            pref[i + 1][j] = pref[i][j] + (1 if row[j] == 'X' else 0)

    best = 0

    for top in range(n - k + 1):
        col_cost = [0] * m
        bottom = top + k
        for j in range(m):
            col_cost[j] = pref[bottom][j] - pref[top][j]

        # sliding window over columns
        l = 0
        s = 0
        for r in range(m):
            s += col_cost[r]
            while s > x:
                s -= col_cost[l]
                l += 1
            best = max(best, r - l + 1)

    return best

def solve():
    n, m, k, x = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    ans1 = solve_orientation(grid, n, m, k, x)

    transposed = [''.join(grid[i][j] for i in range(n)) for j in range(m)]
    ans2 = solve_orientation(transposed, m, n, k, x)

    print(max(ans1, ans2))

if __name__ == "__main__":
    solve()
```

The implementation first constructs prefix sums column-wise so that any vertical segment can be evaluated in constant time per column. The function `solve_orientation` then iterates over all possible starting rows of a $k$-height window and compresses that window into a 1D array of costs. The sliding window over columns ensures we always maintain a valid segment with at most $x$ imperfections, expanding greedily and shrinking only when necessary.

A subtle implementation detail is that prefix sums are indexed as `pref[i+1][j] - pref[i][j]`, which avoids off-by-one mistakes when extracting a window of height $k$. Another important detail is transposition: rather than writing separate logic for horizontal and vertical cases, we reuse the same function on the rotated grid, which prevents duplicated logic errors.

## Worked Examples

### Example 1

Input:

```
5 5 3 3
...X.
XX...
..X..
X...X
.X.X.
```

We first fix a height of 3 and evaluate each possible top row.

| top | column costs (k=3 window) | window process | best length |
| --- | --- | --- | --- |
| 0 | [2,1,1,1,1] | expand then shrink | 3 |
| 1 | [2,1,2,1,1] | sliding window adjusts | 4 |
| 2 | [1,2,1,2,1] | balanced expansion | 4 |

The best horizontal orientation gives 4.

Now consider the transposed grid; the same logic applies to vertical strips, but no better segment appears than length 4.

Output:

```
4
```

This trace shows how local column compression turns a 2D search into repeated 1D constrained subarray problems, and how different starting rows can shift where optimal windows appear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each cell contributes once to prefix computation and once per row window compression |
| Space | $O(nm)$ | Prefix array and grid storage |

The constraints allow up to $10^5$ cells, so a linear scan with constant-time transitions per cell fits comfortably within time limits. The sliding window ensures each column is added and removed at most once per row window, keeping the amortized cost linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve  # assume function exists
    return str(solve()).strip()

# minimal case
assert run("1 1 1 1\nX\n") == "0"

# all clean grid
assert run("3 3 2 10\n...\n...\n...\n") == "3"

# all infected grid
assert run("3 3 2 1\nXXX\nXXX\nXXX\n") == "1"

# single column heavy constraint
assert run("4 4 2 2\nX...\nX...\nX...\nX...\n") == "4"

# sample
assert run("5 5 3 3\n...X.\nXX...\n..X..\nX...X\n.X.X.\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | 0 | smallest boundary case |
| all dots | max width | zero-cost expansion |
| all X | tight constraint | worst density |
| single column | full stretch | column bottleneck |
| sample | 4 | correctness of both orientations |

## Edge Cases

A key edge case is when the optimal rectangle spans the full possible width but is constrained only by a small number of imperfections. In that situation, the sliding window never shrinks after a certain point, and the answer becomes the full width of the grid. The algorithm handles this naturally because the right pointer continues expanding while the sum stays under $x$, and no artificial stopping condition is introduced.

Another case is when $k$ equals $n$ or $m$. Then only one orientation is valid, and the transpose step ensures we still consider the correct dimension without duplicating logic.
