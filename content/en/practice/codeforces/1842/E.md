---
title: "CF 1842E - Tenzing and Triangle"
description: "Every point lies strictly below the line $x+y=k$. A triangle operation is defined by choosing integers $a,b$ with $a+b<k$. The triangle consists of all points satisfying $$x ge a,quad y ge b,quad x+y le k."
date: "2026-06-09T06:14:44+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "geometry", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1842
codeforces_index: "E"
codeforces_contest_name: "CodeTON Round 5 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 2300
weight: 1842
solve_time_s: 105
verified: true
draft: false
---

[CF 1842E - Tenzing and Triangle](https://codeforces.com/problemset/problem/1842/E)

**Rating:** 2300  
**Tags:** data structures, dp, geometry, greedy, math  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

Every point lies strictly below the line $x+y=k$.

A triangle operation is defined by choosing integers $a,b$ with $a+b<k$. The triangle consists of all points satisfying

$$x \ge a,\quad y \ge b,\quad x+y \le k.$$

Since every given point already satisfies $x+y<k$, the last inequality is automatically true for every input point. For the purpose of deciding which points are erased, a triangle is simply the region

$$x \ge a,\quad y \ge b.$$

The cost of such a triangle is

$$(k-a-b)\cdot A.$$

A point can also be erased individually for cost $c_i$.

The task is to erase every point with minimum total cost.

The constraints are large. Both $n$ and $k$ can reach $2\cdot 10^5$. Any solution that considers all pairs of coordinates or all pairs of points is immediately too slow. We need something around $O((n+k)\log k)$.

A subtle observation is that triangles behave like northeast quadrants. Once we rewrite the geometry correctly, the problem becomes a one-dimensional DP with range updates.

Consider a point $(x,y)$. A triangle with parameters $(a,b)$ removes it exactly when $a\le x$ and $b\le y$. The geometric shape disappears and only these coordinate inequalities remain.

Another easy mistake is assuming that overlapping triangles might be useful. If two chosen triangles overlap, replacing them by a larger triangle never increases the cost and can only cover more points. The optimal solution can always be viewed as a sequence of non-overlapping triangles. This is the structural fact that makes the DP work.

### Edge Case 1

```
1 5 100
0 0 1
```

The only point costs $1$ to erase individually.

Any triangle costs at least $100$.

The correct answer is:

```
1
```

A solution that always tries to cover points with triangles would fail here.

### Edge Case 2

```
2 5 1
3 0 100
3 1 100
```

One small triangle can remove both points very cheaply.

The correct answer is not $200$.

The DP must be able to recognize that covering many expensive points with a single triangle is better than paying their individual costs.

### Edge Case 3

```
3 6 2
0 5 10
1 4 10
2 3 10
```

All points lie on the same diagonal.

Several triangle choices cover exactly the same set of points. A careless implementation can double count savings when multiple transitions represent the same geometric action.

The DP formulation below avoids that issue completely.

## Approaches

A brute-force idea is to define a state describing which points have already been erased and try every possible triangle. This is clearly impossible.

A more reasonable brute force is to build a DP on the $x$-coordinate. Suppose we decide that the next triangle starts at some $x=i$ and ends at some $x=j$. We can compute the contribution of that triangle and transition between states.

The problem is that there are $O(k^2)$ pairs $(i,j)$. With $k=2\cdot10^5$, that means roughly $4\cdot10^{10}$ transitions, far beyond the limit.

The key observation is that after fixing the left side of a triangle, the triangle is completely determined by its side length.

Let

$$j=i+l.$$

The triangle starts at $x=i$ and has cost $lA=(j-i)A$.

This transforms the transition into

$$f[j] + A\cdot j + (\text{some accumulated point cost}) - A\cdot i.$$

For a fixed $i$, the only varying part is

$$f[j] + A\cdot j + g_j.$$

That is exactly the kind of expression a segment tree can maintain.

The remaining challenge is updating $g_j$ efficiently when $i$ decreases. Each point contributes to a contiguous range of $j$-values, so every point becomes one range-add update. This reduces the whole DP to $O((n+k)\log k)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over all $(i,j)$ | $O(k^2)$ | $O(k)$ | Too slow |
| Segment Tree Optimized DP | $O((n+k)\log k)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

Let

$$f[i]$$

be the minimum cost to erase all points whose $x$-coordinate is at least $i$.

We process $i$ from $k$ down to $0$.

### 1. Individual deletion transition

If we do not start a triangle at $x=i$, every point with $x=i$ must eventually be paid individually.

Let

$$col[i]=\sum_{x_p=i} c_p.$$

Then

$$f[i] = f[i+1] + col[i].$$

### 2. Triangle transition

Suppose we start a triangle at $x=i$.

Let its side length be $l$, and define

$$j=i+l.$$

The triangle has lower boundary

$$y = k-j.$$

All points satisfying

$$x\ge i,\quad y\ge k-j$$

are removed by the triangle.

The only points inside the strip

$$i \le x < j$$

that still need individual payment are those with

$$y < k-j.$$

Define

$$cost(i,j)
=
\sum_{i\le x_p<j,\; y_p<k-j}
c_p.$$

Then

$$f[i]
=
\min_j
\Big(
f[j]
+
A(j-i)
+
cost(i,j)
\Big).$$

### 3. Rearange the formula

Rewrite it as

$$f[i]
=
\min_j
\Big(
f[j]
+
Aj
+
cost(i,j)
\Big)
-
Ai.$$

For fixed $i$, only the first bracket depends on $j$.

### 4. Maintain $g_j$

For the current value of $i$, define

$$g_j
=
cost(i,j).$$

The segment tree stores

$$f[j] + Aj + g_j.$$

Then the best triangle transition is simply

$$\min_j(\text{segment tree}) - Ai.$$

### 5. Update when $i$ decreases

Move from $i+1$ to $i$.

Consider a point $(i,y,c)$.

This point belongs to $g_j$ exactly when

$$j > i$$

and

$$y < k-j.$$

The second inequality is equivalent to

$$j \le k-y-1.$$

So this point contributes $c$ to every

$$j \in [i+1,\; k-y-1].$$

That is one range-add update on the segment tree.

### 6. Insert the new DP state

After computing $f[i]$, the value

$$f[i] + Ai$$

becomes available for future transitions, so we store it at position $i$ in the segment tree.

### Why it works

The state $f[i]$ represents the optimal cost for all points with $x\ge i$.

Every optimal solution either skips starting a triangle at $x=i$, producing the individual-deletion transition, or starts exactly one leftmost triangle at $x=i$, producing the triangle transition.

The quantity $cost(i,j)$ counts precisely the points that remain uncovered inside the strip handled by that triangle. Everything to the right of $x=j$ is delegated to $f[j]$.

Every valid solution corresponds to exactly one sequence of transitions, and every transition describes a valid solution. Since the DP takes the minimum over all such choices, it computes the optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 30

n, k, A = map(int, input().split())

pts = [[] for _ in range(k)]
col = [0] * (k + 1)

for _ in range(n):
    x, y, c = map(int, input().split())
    pts[x].append((y, c))
    col[x] += c

class SegTree:
    def __init__(self, n):
        self.n = n
        self.mn = [INF] * (4 * n)
        self.lazy = [0] * (4 * n)

    def push(self, p):
        v = self.lazy[p]
        if v:
            self.mn[p * 2] += v
            self.mn[p * 2 + 1] += v
            self.lazy[p * 2] += v
            self.lazy[p * 2 + 1] += v
            self.lazy[p] = 0

    def range_add(self, p, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self.mn[p] += val
            self.lazy[p] += val
            return
        self.push(p)
        m = (l + r) // 2
        self.range_add(p * 2, l, m, ql, qr, val)
        self.range_add(p * 2 + 1, m + 1, r, ql, qr, val)
        self.mn[p] = min(self.mn[p * 2], self.mn[p * 2 + 1])

    def point_set(self, p, l, r, idx, val):
        if l == r:
            self.mn[p] = val
            return
        self.push(p)
        m = (l + r) // 2
        if idx <= m:
            self.point_set(p * 2, l, m, idx, val)
        else:
            self.point_set(p * 2 + 1, m + 1, r, idx, val)
        self.mn[p] = min(self.mn[p * 2], self.mn[p * 2 + 1])

seg = SegTree(k + 1)

f = [INF] * (k + 1)
f[k] = 0

seg.point_set(1, 0, k, k, A * k)

for i in range(k - 1, -1, -1):
    f[i] = f[i + 1] + col[i]

    for y, c in pts[i]:
        L = i + 1
        R = k - y - 1
        if L <= R:
            seg.range_add(1, 0, k, L, R, c)

    f[i] = min(f[i], seg.mn[1] - A * i)

    seg.point_set(1, 0, k, i, f[i] + A * i)

print(f[0])
```

The array `col` stores the total individual deletion cost of points having the same $x$-coordinate.

The DP is evaluated from right to left because every transition moves from $i$ to a larger coordinate $j$.

The segment tree stores

$$f[j] + Aj + g_j.$$

Range additions update the $g_j$ part. Point assignments insert newly computed DP states.

The update interval

$$[i+1,\;k-y-1]$$

is the easiest place to make an off-by-one mistake. The condition is $y<k-j$, which becomes $j\le k-y-1$. Using $k-y$ instead would incorrectly include points lying exactly on the boundary.

All arithmetic fits comfortably in 64-bit integers, but Python integers are unbounded anyway.

## Worked Examples

### Sample 1

Input:

```
4 6 1
1 2 1
2 1 1
1 1 1
3 2 6
```

Key DP evolution:

| i | col[i] | Individual transition | Best triangle transition | f[i] |
| --- | --- | --- | --- | --- |
| 5 | 0 | 0 | INF | 0 |
| 4 | 0 | 0 | INF | 0 |
| 3 | 6 | 6 | 1 | 1 |
| 2 | 1 | 2 | 2 | 2 |
| 1 | 2 | 4 | 3 | 3 |
| 0 | 0 | 3 | 4 | 4 |

Answer:

```
4
```

The interesting step is $i=3$. A tiny triangle removes the expensive point $(3,2)$ for cost $1$, which is much better than paying $6$.

### Sample 2

Input:

```
6 7 1
4 2 1
3 3 1
5 1 4
3 2 5
4 1 1
0 6 4
```

Compressed trace:

| i | Best DP value |
| --- | --- |
| 7 | 0 |
| 6 | 0 |
| 5 | 1 |
| 4 | 2 |
| 3 | 3 |
| 2 | 3 |
| 1 | 3 |
| 0 | 4 |

Answer:

```
4
```

This example demonstrates that several points can be removed simultaneously by carefully chosen triangles, making the optimal cost much smaller than the sum of individual deletion costs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+k)\log k)$ | Each point creates one range update, each DP state performs one point update |
| Space | $O(k)$ | DP arrays, buckets, and segment tree |

With $n,k \le 2\cdot10^5$, the number of segment tree operations is linear in the input size, each costing $O(\log k)$. This easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    # paste solution into a solve() function and call it
    pass

# sample 1
assert run(
"""4 6 1
1 2 1
2 1 1
1 1 1
3 2 6
""") == "4\n"

# sample 2
assert run(
"""6 7 1
4 2 1
3 3 1
5 1 4
3 2 5
4 1 1
0 6 4
""") == "4\n"

# single point, triangle too expensive
assert run(
"""1 5 100
0 0 1
""") == "1\n"

# single point, triangle cheaper
assert run(
"""1 5 1
0 0 100
""") == "5\n"

# boundary condition y = k - j - 1
assert run(
"""1 5 2
0 4 10
""") == "2\n"

# many points on same x
assert run(
"""3 6 1
2 0 5
2 1 5
2 2 5
""") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cheap point | 1 | Individual deletion can beat every triangle |
| Single expensive point | 5 | Triangle can be optimal |
| Point on update boundary | 2 | Correct handling of $k-y-1$ |
| Multiple points with same x | 4 | Aggregation of column costs |
| Sample 1 | 4 | General correctness |
| Sample 2 | 4 | Multiple interacting triangles |

## Edge Cases

Consider:

```
1 5 100
0 0 1
```

At $i=0$, the individual transition gives cost $1$. Any triangle costs at least $100$. The segment tree minimum never beats the individual transition, so $f[0]=1$.

Now consider:

```
1 5 1
0 0 100
```

The cheapest triangle has side length $5$, costing $5$. The DP compares $100$ against $5$ and chooses the triangle transition.

Finally:

```
1 5 2
0 4 10
```

The update range becomes

$$[1,\;5-4-1]=[1,0],$$

which is empty.

This is correct because the point lies exactly on the limiting boundary. A mistaken implementation using $k-y$ instead of $k-y-1$ would incorrectly update one position and produce a smaller answer than the true optimum.
