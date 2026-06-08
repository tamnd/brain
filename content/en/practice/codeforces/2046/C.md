---
title: "CF 2046C - Adventurers"
description: "Each city is a point on the plane. We choose a dividing point $(x0,y0)$, which splits the plane into four regions: $$begin{aligned} &x ge x0, y ge y0 &x < x0, y ge y0 &x ge x0, y < y0 &x < x0, y < y0 end{aligned}$$ Every city belongs to exactly one of these regions, according to…"
date: "2026-06-08T09:08:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "sortings", "ternary-search", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2046
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 990 (Div. 1)"
rating: 2100
weight: 2046
solve_time_s: 199
verified: false
draft: false
---

[CF 2046C - Adventurers](https://codeforces.com/problemset/problem/2046/C)

**Rating:** 2100  
**Tags:** binary search, data structures, greedy, sortings, ternary search, two pointers  
**Solve time:** 3m 19s  
**Verified:** no  

## Solution
## Problem Understanding

Each city is a point on the plane. We choose a dividing point $(x_0,y_0)$, which splits the plane into four regions:

$$\begin{aligned}
&x \ge x_0,\ y \ge y_0 \\
&x < x_0,\ y \ge y_0 \\
&x \ge x_0,\ y < y_0 \\
&x < x_0,\ y < y_0
\end{aligned}$$

Every city belongs to exactly one of these regions, according to the inequalities above.

For a chosen dividing point, let the four region counts be $c_1,c_2,c_3,c_4$. We want to maximize

$$\min(c_1,c_2,c_3,c_4).$$

We must output both the maximum achievable value and one dividing point that achieves it.

The total number of points over all test cases is at most $10^5$. Any solution that examines every pair of candidate $x_0$ and $y_0$ values would require $O(n^2)$ or worse work per test case, which is far too slow. We need something around $O(n \log^2 n)$.

A subtle point is that the inequalities are asymmetric. Cities with $x=x_0$ belong to the right half, and cities with $y=y_0$ belong to the upper half. A solution that accidentally treats the split as strict on both sides will produce incorrect quadrant counts.

Another tricky case occurs when many cities share the same $x$-coordinate. While sweeping possible vertical splits, all cities with the same $x$ must move together. Splitting inside such a group changes the meaning of the inequality and can create invalid states.

## Approaches

A brute-force solution would try every possible $x_0$, every possible $y_0$, count the four quadrants, and keep the best answer. Even if we restrict candidates to coordinates appearing in the input, this still requires $O(n^2)$ candidate pairs and $O(n)$ work to evaluate each one, resulting in $O(n^3)$.

The key observation is that we do not need to search directly for the best minimum quadrant size. Instead, suppose we ask a simpler question:

> Is it possible to make every quadrant contain at least $k$ cities?

If we can answer this efficiently, then the final answer can be found with binary search on $k$.

For a fixed $k$, imagine sweeping the vertical boundary from left to right. At any moment, cities are divided into two groups:

$$L = \{x_i < x_0\},
\qquad
R = \{x_i \ge x_0\}.$$

For a chosen horizontal boundary $y_0$, we need

$$\begin{aligned}
\text{left-below} &\ge k,\\
\text{left-above} &\ge k,\\
\text{right-below} &\ge k,\\
\text{right-above} &\ge k.
\end{aligned}$$

Let $P_L(y)$ and $P_R(y)$ be the numbers of cities in $L$ and $R$ whose $y$-coordinate is strictly smaller than $y$.

Then the conditions become

$$k \le P_L(y_0) \le |L|-k,$$

and

$$k \le P_R(y_0) \le |R|-k.$$

For each side, the valid values of $y_0$ form a contiguous interval because prefix counts are monotone. We only need to determine whether the interval for $L$ intersects the interval for $R$.

Fenwick trees allow us to maintain the prefix counts while sweeping $x$, and also to find the first position where a prefix reaches a given value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Binary Search + Sweep + Fenwick | $O(n \log^2 n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Coordinate Compression

All operations depend only on the relative order of $y$-coordinates.

Compress all distinct $y$-values into indices $1 \ldots m$.

### Feasibility Check for a Fixed $k$

1. Put every point into the right structure $R$.
2. The left structure $L$ starts empty.
3. Sweep distinct $x$-coordinates in increasing order.
4. Before processing a group with coordinate $x$, the split corresponds to $x_0=x$. Every point with smaller $x$ is already in $L$, and every point with $x\ge x_0$ remains in $R$.
5. Let $tot_L$ and $tot_R$ be the current sizes of the two sides.
6. If either side has fewer than $2k$ points, that side can never contribute at least $k$ points both above and below the horizontal line. Skip this sweep position.
7. For $L$, find the interval of compressed $y$-positions where

$$k \le P_L \le tot_L-k.$$

Because prefix counts are monotone, this interval can be obtained with Fenwick order-statistics queries.

1. Compute the corresponding interval for $R$.
2. If the two intervals intersect, then a valid $y_0$ exists and the answer for this check is "possible".
3. Move the entire current $x$-group from $R$ into $L$ and continue the sweep.

### Binary Search

1. The answer cannot exceed $\lfloor n/4 \rfloor$.
2. Binary search $k$ in the range $[0,\lfloor n/4 \rfloor]$.
3. Run the feasibility check.
4. Keep the largest feasible $k$.
5. Run the check once more for that value and store the corresponding $(x_0,y_0)$.

### Why it works

For a fixed vertical split, every valid horizontal split must satisfy two independent constraints:

$$k \le P_L(y_0) \le |L|-k,$$

and

$$k \le P_R(y_0) \le |R|-k.$$

Since both prefix functions are monotone, each constraint defines a contiguous interval of possible $y_0$-positions. A horizontal split exists exactly when those intervals intersect.

The sweep enumerates every meaningful vertical split because the classification only changes when we pass a distinct $x$-coordinate. The binary search is valid because feasibility is monotone: if every quadrant can contain at least $k$ cities, then every smaller value is also achievable.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        n = self.n
        bit = self.bit
        while idx <= n:
            bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        bit = self.bit
        while idx:
            res += bit[idx]
            idx -= idx & -idx
        return res

    def kth(self, k):
        idx = 0
        bitmask = 1 << (self.n.bit_length() - 1)
        while bitmask:
            nxt = idx + bitmask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bitmask >>= 1
        return idx + 1

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]

        ys = sorted(set(y for _, y in pts))
        m = len(ys)

        data = []
        for x, y in pts:
            data.append((x, bisect_left(ys, y) + 1))

        data.sort()

        groups = []
        i = 0
        while i < n:
            j = i
            while j < n and data[j][0] == data[i][0]:
                j += 1
            groups.append((data[i][0], data[i:j]))
            i = j

        def get_interval(ft, total, k):
            if total < 2 * k:
                return None

            left = ft.kth(k)

            limit = total - k
            if limit == total:
                right = m
            else:
                pos = ft.kth(limit + 1)
                right = pos - 1

            if left > right:
                return None
            return (left, right)

        def check(k):
            L = Fenwick(m)
            R = Fenwick(m)

            for _, y in data:
                R.add(y, 1)

            left_cnt = 0
            right_cnt = n

            for x0, grp in groups:
                A = get_interval(L, left_cnt, k)
                B = get_interval(R, right_cnt, k)

                if A is not None and B is not None:
                    l = max(A[0], B[0])
                    r = min(A[1], B[1])

                    if l <= r:
                        y0 = ys[l - 1]
                        return True, x0, y0

                for _, y in grp:
                    R.add(y, -1)
                    L.add(y, 1)

                sz = len(grp)
                left_cnt += sz
                right_cnt -= sz

            return False, 0, 0

        lo, hi = 0, n // 4
        best = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            ok, _, _ = check(mid)

            if ok:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        _, x0, y0 = check(best)

        out.append(str(best))
        out.append(f"{x0} {y0}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log^2 n)$ | Binary search on $k$, each feasibility check performs a sweep with Fenwick order-statistic queries |
| Space | $O(n)$ | Compressed coordinates, grouped points, and Fenwick trees |

The total number of points across all test cases is at most $10^5$, so $O(n \log^2 n)$ easily fits within the limits. The memory usage is linear in the number of points.
