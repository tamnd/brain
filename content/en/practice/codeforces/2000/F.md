---
title: "CF 2000F - Color Rows and Columns"
description: "Each rectangle is a grid of $ai$ columns and $bi$ rows. We may color individual cells one by one. Whenever a row becomes completely colored, we gain one point. Whenever a column becomes completely colored, we also gain one point. The rectangles are independent."
date: "2026-06-08T14:15:32+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2000
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 966 (Div. 3)"
rating: 1900
weight: 2000
solve_time_s: 244
verified: true
draft: false
---

[CF 2000F - Color Rows and Columns](https://codeforces.com/problemset/problem/2000/F)

**Rating:** 1900  
**Tags:** dp, greedy, implementation, math  
**Solve time:** 4m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

Each rectangle is a grid of $a_i$ columns and $b_i$ rows. We may color individual cells one by one. Whenever a row becomes completely colored, we gain one point. Whenever a column becomes completely colored, we also gain one point.

The rectangles are independent. Cells colored in one rectangle do not affect any other rectangle. Our goal is to earn at least $k$ total points across all rectangles while minimizing the total number of colored cells.

The key difficulty is that coloring cells can contribute to both row completions and column completions. For example, if we color an entire column, we immediately gain one point. Later, after enough columns are fully colored, some rows may become completed automatically and yield additional points.

The constraints reveal the intended direction. We have up to $1000$ rectangles over all test cases, but $k \le 100$. The small value of $k$ is the most important fact. Any solution whose complexity depends polynomially on $k$ is likely acceptable, while anything depending on the rectangle area $a_i b_i$ is impossible because dimensions can be as large as $100$.

A common mistake is to treat every point inside a rectangle as having the same cost.

Consider a $6 \times 3$ rectangle.

```
1 4
6 3
```

The optimal way to get four points is to color four complete columns. Each column costs $3$ cells, so the answer is $12$. A naive "points cost min(a,b)" idea would incorrectly predict $4 \cdot 3 = 12$ even when the fourth point is obtained differently in other rectangles.

Another subtle case occurs when rows and columns interact.

For a $2 \times 2$ rectangle:

```
1 3
2 2
```

To get three points, color both columns. This costs $4$ cells. The two completed columns give two points, and both rows become complete automatically, giving two more points. Three points can be achieved with cost $4$, not $6$.

A final edge case is impossibility.

```
2 100
1 2
5 6
```

The first rectangle can contribute at most $1+2=3$ points, the second at most $5+6=11$, for a total of $14$. Reaching $100$ points is impossible, so the answer is $-1$.

## Approaches

The brute force viewpoint is to decide exactly which cells to color in every rectangle. That is immediately hopeless. A single $100 \times 100$ rectangle already contains $10^4$ cells, so the number of possible subsets is astronomical.

The first observation is that only completed rows and completed columns matter. Partial progress that never finishes a row or column is useless.

Suppose we focus on one rectangle of size $a \times b$. Imagine we want exactly $p$ points from this rectangle. What is the minimum number of colored cells required?

If we completely color a column, the cost is $b$ cells and we gain one column point. If we completely color a row, the cost is $a$ cells and we gain one row point.

The crucial insight is that an optimal strategy for a single rectangle always proceeds greedily by finishing entire rows or entire columns. Let

$$x = \text{number of completed columns},
\qquad
y = \text{number of completed rows}.$$

Then we gain $x+y$ points.

What is the cost?

All cells belonging to completed columns must be colored, contributing $xb$ cells. After that, each completed row already contains $x$ colored cells, so only $a-x$ additional cells are needed per completed row.

Hence

$$\text{cost}(x,y)
=
xb + y(a-x).$$

Symmetrically, we could start from rows first. The optimal sequence is obtained by repeatedly taking the cheaper of the two remaining directions. Since $a,b \le 100$, we can explicitly compute the minimum cost for every attainable point count $p$.

Once every rectangle provides a table

$$best_i[p]
=
\text{minimum cost to obtain } p \text{ points},$$

the global problem becomes a knapsack.

For each rectangle, choose how many points to take from it. The total points must reach at least $k$, and the sum of costs should be minimal.

Since $k \le 100$, a standard DP over points is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in rectangle area | Exponential | Too slow |
| Optimal | $O(nk^2)$ after preprocessing | $O(k)$ | Accepted |

## Algorithm Walkthrough

### Computing the cost table for one rectangle

For a rectangle $a \times b$, let $m=a+b$, the maximum possible points.

We build an array `cost[p]` where `cost[p]` is the minimum number of colored cells needed to obtain exactly `p` points.

The editorial solution uses a simple greedy simulation.

Suppose $a \le b$. Completing a column costs $b$ cells and completing a row costs $a$ cells. Initially rows are cheaper, so we repeatedly complete rows until they are exhausted. After a row is completed, future column completions become cheaper because part of each column is already colored.

The same reasoning works symmetrically when $b < a$.

By simulating the sequence of cheapest available completions, we obtain the minimum cumulative cost for every point count from $1$ to $a+b$.

### Global knapsack

Let `dp[j]` be the minimum total operations needed to obtain exactly `j` points after processing some rectangles.

Initially:

```
dp[0] = 0
dp[j] = INF for j > 0
```

For each rectangle we have its local table `cost`.

We create a new DP array. For every current score `j` and every attainable contribution `p` from this rectangle, we update

$$ndp[\min(k, j+p)]
=
\min(
ndp[\min(k,j+p)],
dp[j] + cost[p]
).$$

Scores above $k$ are capped at $k$, since only "at least $k$" matters.

After all rectangles are processed, `dp[k]` contains the answer.

### Why it works

For a fixed rectangle, every completed row or column contributes exactly one point. The greedy construction generates the minimum extra number of cells required for each successive point. Any alternative way of obtaining the same number of points must complete the same number of rows and columns, and cannot use fewer newly colored cells.

The global DP relies on optimal substructure. Once we know the minimum cost for every attainable point count in each rectangle, rectangles become independent choices. The knapsack DP enumerates all distributions of points among rectangles and keeps the cheapest cost for every total score. Since every possible allocation is considered exactly once, the final value is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 18

def rectangle_costs(a, b):
    m = a + b
    res = [INF] * (m + 1)
    res[0] = 0

    for cols in range(a + 1):
        cost = cols * b
        points = cols

        res[points] = min(res[points], cost)

        cur_cost = cost
        for rows in range(1, b + 1):
            cur_cost += a - cols
            res[points + rows] = min(
                res[points + rows],
                cur_cost
            )

    return res

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n, k = map(int, input().split())

        dp = [INF] * (k + 1)
        dp[0] = 0

        total_possible = 0

        rects = []
        for _ in range(n):
            a, b = map(int, input().split())
            rects.append((a, b))
            total_possible += a + b

        if total_possible < k:
            answers.append("-1")
            continue

        for a, b in rects:
            local = rectangle_costs(a, b)

            ndp = dp[:]

            for cur in range(k + 1):
                if dp[cur] == INF:
                    continue

                for gain in range(1, len(local)):
                    if local[gain] == INF:
                        continue

                    nxt = min(k, cur + gain)

                    ndp[nxt] = min(
                        ndp[nxt],
                        dp[cur] + local[gain]
                    )

            dp = ndp

        answers.append(str(dp[k]))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The helper `rectangle_costs` computes the minimum cost for every achievable score inside one rectangle. We enumerate how many columns are completed. Once those columns are fixed, every completed row requires only `a - cols` additional cells because the intersection cells are already colored.

That formula is the key implementation detail. Using `rows * a` would double count the cells lying inside completed columns.

The DP is a standard multiple-choice knapsack. Each rectangle contributes one option among several possible point gains. Scores are capped at `k` so the DP array never exceeds size `101`.

The impossibility check `total_possible < k` is not required for correctness, but it avoids unnecessary computation.

## Worked Examples

### Example 1

Input:

```
1
1 4
6 3
```

For the single rectangle:

| Completed Columns | Completed Rows | Points | Cost |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 3 |
| 2 | 0 | 2 | 6 |
| 3 | 0 | 3 | 9 |
| 4 | 0 | 4 | 12 |

The local table gives:

| Points | Minimum Cost |
| --- | --- |
| 0 | 0 |
| 1 | 3 |
| 2 | 6 |
| 3 | 9 |
| 4 | 12 |

The DP chooses 4 points from this rectangle and outputs 12.

This example shows that repeatedly completing columns is optimal because each column costs only three cells.

### Example 2

Input:

```
1
3 11
2 2
3 3
4 4
```

Local maximum scores:

| Rectangle | Maximum Points |
| --- | --- |
| 2×2 | 4 |
| 3×3 | 6 |
| 4×4 | 8 |

The DP gradually combines these possibilities.

| After Processing | Reachable Scores |
| --- | --- |
| First rectangle | 0..4 |
| Second rectangle | 0..10 |
| Third rectangle | 0..18 |

Since score 11 becomes reachable, the DP records the minimum cost among all allocations whose total score is at least 11.

This trace demonstrates the independence of rectangles. The DP never cares which exact rows or columns were colored, only the best cost for each score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nk^2)$ | Each rectangle updates a DP of size $k$, trying up to $k$ possible gains |
| Space | $O(k)$ | Only the current DP array is stored |

With $k \le 100$ and total $n \le 1000$, the number of state transitions is only around $10^7$ in the worst case, which comfortably fits the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from math import inf

    data = io.StringIO(inp)
    input = data.readline

    INF = 10 ** 18

    def rectangle_costs(a, b):
        m = a + b
        res = [INF] * (m + 1)
        res[0] = 0

        for cols in range(a + 1):
            cost = cols * b
            res[cols] = min(res[cols], cost)

            cur = cost
            for rows in range(1, b + 1):
                cur += a - cols
                res[cols + rows] = min(
                    res[cols + rows],
                    cur
                )
        return res

    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())

        rects = []
        total = 0

        for _ in range(n):
            a, b = map(int, input().split())
            rects.append((a, b))
            total += a + b

        if total < k:
            out.append("-1")
            continue

        dp = [INF] * (k + 1)
        dp[0] = 0

        for a, b in rects:
            local = rectangle_costs(a, b)
            ndp = dp[:]

            for i in range(k + 1):
                if dp[i] == INF:
                    continue

                for gain in range(1, len(local)):
                    j = min(k, i + gain)
                    ndp[j] = min(
                        ndp[j],
                        dp[i] + local[gain]
                    )

            dp = ndp

        out.append(str(dp[k]))

    return "\n".join(out)

# sample 1
assert run(
"""1
1 4
6 3
"""
) == "12"

# minimum size
assert run(
"""1
1 1
1 1
"""
) == "1"

# impossible
assert run(
"""1
1 3
1 1
"""
) == "-1"

# exact maximum score
assert run(
"""1
1 4
2 2
"""
) == "4"

# two rectangles
assert run(
"""1
2 2
1 1
1 1
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 rectangle, k=1 | 1 | Smallest non-trivial case |
| 1×1 rectangle, k=3 | -1 | Impossible target |
| 2×2 rectangle, k=4 | 4 | Full completion of a rectangle |
| Two 1×1 rectangles, k=2 | 2 | Combining contributions from multiple rectangles |

## Edge Cases

### Target score exceeds all available points

Input:

```
1
1 3
1 1
```

The rectangle contains one row and one column, so at most two points can be earned. The algorithm computes `total_possible = 2`, which is less than `k = 3`, and immediately returns `-1`.

### Points obtained through overlap

Input:

```
1
1 3
2 2
```

Coloring both columns costs four cells.

| Columns | Rows | Points | Cost |
| --- | --- | --- | --- |
| 2 | 0 | 2 | 4 |
| 2 | 1 | 3 | 4 |
| 2 | 2 | 4 | 4 |

The implementation correctly accounts for intersections by adding only `a - cols` new cells per completed row. Once all columns are colored, every row is already complete, so extra points can appear at zero additional cost.

### Large rectangle with small target

Input:

```
1
1 2
100 100
```

A careless solution might attempt to reason about all $10^4$ cells. The algorithm only computes costs for point counts up to $a+b=200$, then the global DP uses only scores up to $k=2$. The answer is obtained efficiently without ever touching individual cells.
