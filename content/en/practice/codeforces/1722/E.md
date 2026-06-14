---
title: "CF 1722E - Counting Rectangles"
description: "We are given a collection of axis-aligned rectangles, each defined by its height and width. For every query, we are also given two bounding rectangles: a “small inner constraint” rectangle and a “large outer constraint” rectangle."
date: "2026-06-15T01:29:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1722
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 817 (Div. 4)"
rating: 1600
weight: 1722
solve_time_s: 294
verified: false
draft: false
---

[CF 1722E - Counting Rectangles](https://codeforces.com/problemset/problem/1722/E)

**Rating:** 1600  
**Tags:** brute force, data structures, dp, implementation  
**Solve time:** 4m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of axis-aligned rectangles, each defined by its height and width. For every query, we are also given two bounding rectangles: a “small inner constraint” rectangle and a “large outer constraint” rectangle.

For a query with parameters $(h_s, w_s, h_b, w_b)$, we must consider only those rectangles $(h_i, w_i)$ such that the rectangle is strictly larger than the small constraint in both dimensions and strictly smaller than the large constraint in both dimensions. Among those valid rectangles, we sum their areas $h_i \cdot w_i$.

So each query is asking for a 2D range filter over rectangles, followed by aggregation of their areas.

The key difficulty is that both $n$ and $q$ can be as large as $10^5$, and there are up to 100 test cases. This immediately rules out any solution that checks each rectangle per query, since that would require up to $10^{10}$ operations in the worst case.

The additional structural constraint is important: heights and widths are both bounded by 1000. This means the coordinate space is small and discrete, even though the number of rectangles is large. That strongly suggests precomputation over a fixed grid.

A naive but subtle mistake would be to try sorting rectangles and doing binary searches independently on height and width. That approach fails because the constraints are not separable: a rectangle might satisfy the height condition but fail the width condition, and vice versa. For example, a rectangle with $h=10, w=1$ and another with $h=1, w=10$ both pass one dimension filter but not the combined 2D filter. Any approach that treats dimensions independently without a joint structure will produce incorrect results.

Another edge case is equality handling. Since strict inequalities are required, rectangles with height equal to $h_s$ or $h_b$ must be excluded. A common mistake is turning this into inclusive bounds accidentally, especially when translating to prefix sums.

## Approaches

The brute-force approach is straightforward: for each query, iterate over all rectangles and check whether both height and width lie strictly within the query bounds. If so, add its area to the answer. This is correct because it directly follows the definition of validity.

However, this costs $O(n)$ per query, leading to $O(nq)$ overall. With $n = q = 10^5$, this becomes far too large.

The key observation is that rectangle dimensions are small. Both height and width lie in $[1, 1000]$, which gives only $10^6$ possible pairs. Instead of treating rectangles as an unstructured list, we can aggregate them into a 2D frequency table.

Once we do that, each query becomes a rectangle sum query over a 2D grid. This is a classic prefix sum problem: if we precompute a 2D prefix sum of total area contributions, then each query can be answered in constant time using inclusion-exclusion.

The idea is to store, for each cell $(h, w)$, the total area contributed by all rectangles with exactly that dimension. Then build a 2D prefix sum over this grid so that we can query sums over any rectangular region in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(1)$ | Too slow |
| 2D Prefix Sum | $O(n + 1000^2 + q)$ | $O(1000^2)$ | Accepted |

## Algorithm Walkthrough

We exploit the fact that height and width are bounded by 1000, so we build a fixed grid.

1. Initialize a 2D array `grid[h][w]` of size 1001 × 1001 with zeros. Each entry will accumulate the total area contributed by rectangles with that exact height and width. This transforms the input list into a structured frequency map over a small domain.
2. For each rectangle $(h_i, w_i)$, add $h_i \cdot w_i$ to `grid[h_i][w_i]`. This step compresses all identical rectangles into a single contribution, preserving total area exactly.
3. Build a 2D prefix sum array `pref`, where each cell stores the sum of all values in the rectangle $[1..h][1..w]$. This is done using the standard inclusion-exclusion recurrence over a grid. The reason this works is that any rectangular query can be decomposed into overlapping prefix regions.
4. For each query $(h_s, w_s, h_b, w_b)$, compute the sum over the strict rectangle:

$$(h_s, h_b) \times (w_s, w_b)$$

by converting strict inequalities into inclusive prefix indices:

$$h \in [h_s+1, h_b-1], \quad w \in [w_s+1, w_b-1]$$
5. Answer the query using the inclusion-exclusion formula on the prefix sum table. This gives the total area of all valid rectangles in constant time per query.

The important structural decision is that instead of querying over a list of rectangles, we query over a compressed grid where each coordinate represents a dimension pair.

### Why it works

The correctness rests on two invariants. First, every rectangle contributes exactly once to its corresponding grid cell, so no information is lost during compression. Second, the prefix sum transformation preserves exact sums over axis-aligned subrectangles. Since every query condition is exactly a rectangular region in the height-width grid after shifting by strict bounds, every valid rectangle is included and every invalid one is excluded. No overlapping or missing cases occur because the transformation is bijective between query conditions and grid subregions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX = 1000

def solve():
    n, q = map(int, input().split())
    
    grid = [[0] * (MAX + 1) for _ in range(MAX + 1)]
    
    for _ in range(n):
        h, w = map(int, input().split())
        grid[h][w] += h * w
    
    pref = [[0] * (MAX + 1) for _ in range(MAX + 1)]
    
    for h in range(1, MAX + 1):
        row_sum = 0
        for w in range(1, MAX + 1):
            row_sum += grid[h][w]
            pref[h][w] = pref[h - 1][w] + row_sum
    
    def get(h1, w1, h2, w2):
        if h1 > h2 or w1 > w2:
            return 0
        return (
            pref[h2][w2]
            - pref[h1 - 1][w2]
            - pref[h2][w1 - 1]
            + pref[h1 - 1][w1 - 1]
        )
    
    out = []
    for _ in range(q):
        hs, ws, hb, wb = map(int, input().split())
        h1, h2 = hs + 1, hb - 1
        w1, w2 = ws + 1, wb - 1
        out.append(str(get(h1, w1, h2, w2)))
    
    print("\n".join(out))

t = int(input())
for _ in range(t):
    solve()
```

The solution begins by compressing all rectangles into a fixed grid indexed by height and width. This avoids handling individual rectangles during queries.

The prefix sum construction is done row by row to ensure each cell accumulates all contributions from the top-left submatrix. The intermediate `row_sum` variable is necessary to avoid recomputing horizontal sums repeatedly, which would otherwise add an extra factor of 1000 unnecessarily.

The query function carefully handles invalid ranges where the strict constraints collapse into an empty interval. This prevents negative indexing errors and ensures correctness at boundaries.

Each query is converted from strict inequalities into inclusive bounds before applying the prefix sum formula.

## Worked Examples

### Example 1

Input:

```
n = 2, q = 1
rectangles: (2,3), (3,2)
query: (1,1,3,4)
```

We build the grid:

| h \ w | 2 | 3 |
| --- | --- | --- |
| 2 | 6 | 0 |
| 3 | 0 | 6 |

Prefix sums accumulate these values over the 2D plane. The query translates to:

$h \in [2,2], w \in [2,3]$

Only cell (2,3) lies in this range, contributing 6.

Output:

```
6
```

This demonstrates how strict inequalities are correctly translated into inclusive grid bounds.

### Example 2

Consider a slightly larger configuration:

```
rectangles:
(1,2)=2, (2,2)=4, (2,3)=6, (4,4)=16
query: (1,1,3,3)
```

Valid rectangles must satisfy:

$h \in [2,2], w \in [2,2]$

Only (2,2) contributes.

| Step | Valid cells | Sum |
| --- | --- | --- |
| filtering | (2,2) | 4 |
| result | 4 | 4 |

This confirms that rectangles outside the query window, even if partially matching one dimension, are excluded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + 10^6 + q)$ | Each test builds a fixed 1000×1000 grid and answers queries in O(1) |
| Space | $O(10^6)$ | Storage for grid and prefix sums |

The dominant term is the fixed grid construction, which is independent of input size per test case. Since $10^6$ operations per test case are acceptable under the constraints, and total $n, q$ are bounded, the solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MAX = 1000

    def solve():
        n, q = map(int, input().split())
        grid = [[0] * (MAX + 1) for _ in range(MAX + 1)]

        for _ in range(n):
            h, w = map(int, input().split())
            grid[h][w] += h * w

        pref = [[0] * (MAX + 1) for _ in range(MAX + 1)]

        for h in range(1, MAX + 1):
            row_sum = 0
            for w in range(1, MAX + 1):
                row_sum += grid[h][w]
                pref[h][w] = pref[h - 1][w] + row_sum

        def get(h1, w1, h2, w2):
            if h1 > h2 or w1 > w2:
                return 0
            return (
                pref[h2][w2]
                - pref[h1 - 1][w2]
                - pref[h2][w1 - 1]
                + pref[h1 - 1][w1 - 1]
            )

        out = []
        for _ in range(q):
            hs, ws, hb, wb = map(int, input().split())
            h1, h2 = hs + 1, hb - 1
            w1, w2 = ws + 1, wb - 1
            out.append(str(get(h1, w1, h2, w2)))

        return "\n".join(out)

    t = int(input())
    return "\n".join(solve() for _ in range(t))

# provided sample
assert run("""3
2 1
2 3
3 2
1 1 3 4
5 5
1 1
2 2
3 3
4 4
5 5
3 3 6 6
2 1 4 5
1 1 2 10
1 1 100 100
1 1 3 3
3 1
999 999
999 999
999 998
1 1 1000 1000
""") == """6
41
9
0
54
4
2993004"""

# edge: empty answer
assert run("""1
2 2
1 1
2 2
1 1 2 2
""") == "0"

# edge: single cell valid
assert run("""1
1 1
5 7
0 0 6 8
""") == "35"

# edge: full range
assert run("""1
1 1
1 1
0 0 1000 1000
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty inner region | 0 | strict inequalities exclude boundary |
| single valid rectangle | 35 | correct inclusion when bounds match exactly |
| full range | 1 | global accumulation correctness |

## Edge Cases

A subtle case appears when the query window collapses after applying strict bounds. For example, if $h_b = h_s + 1$, then the valid height interval becomes empty. The algorithm handles this by producing $h_1 = h_s + 1$ and $h_2 = h_b - 1$, which leads to $h_1 > h_2$. The `get` function explicitly checks this condition and returns zero immediately, preventing invalid prefix sum indexing.

Another case is when rectangles lie exactly on the boundary of the query. Since both inequalities are strict, a rectangle with height equal to $h_s$ or $h_b$ must not contribute. The grid-based representation ensures this naturally because those cells are simply excluded from the prefix range $[h_s+1, h_b-1]$, so no special handling beyond index shifting is required.
