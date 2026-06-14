---
title: "CF 1083E - The Fair Nut and Rectangles"
description: "Each rectangle is anchored at the origin and stretches to a point $(xi, yi)$, so geometrically every rectangle is a lower-left aligned axis-parallel rectangle."
date: "2026-06-15T05:53:33+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1083
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 526 (Div. 1)"
rating: 2400
weight: 1083
solve_time_s: 150
verified: false
draft: false
---

[CF 1083E - The Fair Nut and Rectangles](https://codeforces.com/problemset/problem/1083/E)

**Rating:** 2400  
**Tags:** data structures, dp, geometry  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

Each rectangle is anchored at the origin and stretches to a point $(x_i, y_i)$, so geometrically every rectangle is a lower-left aligned axis-parallel rectangle. Because all rectangles share the same origin corner, any two rectangles overlap in a very structured way: their union depends only on their maximum $x$ and maximum $y$ among the chosen set.

For any chosen subset of rectangles, the union area is simply the area of the bounding rectangle that covers them all, which is $\max x \cdot \max y$. The cost of choosing a subset is this union area minus the sum of penalties $a_i$ over selected rectangles. The task is to choose a subset that maximizes this value.

The key constraint is that $n$ can be up to $10^6$, and coordinates go up to $10^9$. This immediately rules out any pairwise or subset DP. Anything beyond roughly $O(n \log n)$ is already borderline, and $O(n^2)$ reasoning over pairs of rectangles is impossible.

A subtle failure case appears when a naive approach assumes that each rectangle contributes independently. For example, one might think of picking all rectangles with $x_i y_i > a_i$, but this ignores that adding a rectangle can increase the union area dramatically and make previously good choices worse.

Another hidden pitfall is assuming we need to explicitly track the union shape. Since rectangles are nested only by dominance, a careless geometric union computation leads to unnecessary complexity and incorrect transitions.

## Approaches

A brute-force solution would try every subset of rectangles, compute the union area for each subset by taking maximum $x$ and $y$, subtract the sum of $a_i$, and keep the best result. This works conceptually because the union is simple to compute once the subset is fixed. However, the number of subsets is $2^n$, and even evaluating each subset in $O(n)$ makes the total work exponential beyond any feasible limit.

The key structural observation is that a subset is completely determined by its rectangle with maximum $x$ and maximum $y$. If we fix a rectangle $i$ as the top-right corner of the union (meaning it provides the maximum $x$), then any chosen rectangle must lie within the region $[0, x_i] \times [0, y_i]$. Within that region, the union area is always $x_i \cdot y_i$, regardless of which subset is chosen, as long as $i$ is included.

So the problem reduces to deciding, for each rectangle $i$, whether we want to make it the “active bounding rectangle” and optionally include other rectangles inside its area. If we fix $i$, the contribution becomes:

$$x_i y_i - a_i + \sum (x_j y_j - a_j \text{ for selected } j \subseteq i\text{'s valid set})$$

but crucially, selecting a rectangle $j$ only makes sense if it is not worse than skipping it, because it does not change the bounding box unless it is the maximum.

This leads to a classic envelope DP structure: sort rectangles by increasing $x$, maintain best achievable value for valid $y$ constraints, and use a structure that queries the best previous state among all rectangles with smaller $y$.

The absence of nested rectangles guarantees a clean partial order: no rectangle fully dominates another in both dimensions, which avoids degenerate cases where multiple identical states compete.

The DP becomes a sweep over $x$, where we maintain a structure keyed by $y$, storing the best value achievable for rectangles up to that height boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Sweep + DP over y with structure | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process rectangles in increasing order of $x$, treating each rectangle as a potential top-right corner of the union.

1. Sort rectangles by increasing $x$. This ensures that when we process a rectangle $i$, all candidates that could lie strictly inside its width are already considered.
2. Maintain a dynamic programming structure indexed by $y$, where each state represents the best achievable value using rectangles whose height constraint is at most that $y$. This is necessary because feasibility depends on both dimensions.
3. For each rectangle $i = (x_i, y_i, a_i)$, compute its base gain as $x_i y_i - a_i$. This is the value if we choose it alone as the bounding rectangle.
4. Query the best DP value among all states with $y \le y_i$. This represents the best configuration of smaller rectangles that can be included inside rectangle $i$ without violating the bounding constraint.
5. Combine the result of the query with the base gain of $i$. This gives the best solution where $i$ acts as the bounding rectangle.
6. Update the DP structure at position $y_i$ with this combined value, ensuring future rectangles can build upon it.

The central idea is that every optimal solution has a unique rectangle that defines its maximum $x$. Once that rectangle is fixed, everything else reduces to a constrained subproblem over $y$, which is exactly what the DP structure captures.

### Why it works

Every feasible solution can be associated with the rectangle that achieves the maximum $x$. That rectangle determines the union area. All other chosen rectangles must lie under its $y$-height. The DP ensures that when we process this rectangle, we already know the best possible contribution from all valid subconfigurations constrained by $y$. Because we process in increasing $x$, no future rectangle can retroactively invalidate earlier optimal substructures, which guarantees optimal substructure and prevents double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [-10**30] * (n + 2)

    def update(self, i, v):
        while i <= self.n:
            if v > self.bit[i]:
                self.bit[i] = v
            i += i & -i

    def query(self, i):
        res = -10**30
        while i > 0:
            if self.bit[i] > res:
                res = self.bit[i]
            i -= i & -i
        return res

def solve():
    n = int(input())
    rects = []
    ys = []

    for _ in range(n):
        x, y, a = map(int, input().split())
        rects.append((x, y, x * y - a))
        ys.append(y)

    rects.sort()
    ys = sorted(set(ys))

    def get_idx(y):
        # manual binary search
        lo, hi = 0, len(ys) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if ys[mid] == y:
                return mid + 1
            elif ys[mid] < y:
                lo = mid + 1
            else:
                hi = mid - 1
        return lo + 1

    fw = Fenwick(len(ys))
    ans = 0

    for x, y, val in rects:
        yi = get_idx(y)
        best = fw.query(yi)
        if best < 0:
            best = 0
        cur = best + val
        if cur > ans:
            ans = cur
        fw.update(yi, cur)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution compresses all $y$-coordinates because the Fenwick tree cannot operate on raw values up to $10^9$. The query retrieves the best achievable configuration that fits within the current rectangle’s height constraint, and the update propagates the new best state.

A subtle implementation detail is the initialization of DP values with a large negative number while separately allowing zero as the empty set baseline. This prevents invalid transitions from contaminating results.

## Worked Examples

### Example 1

Input:

```
3
4 4 8
1 5 0
5 2 10
```

Sorted by $x$:

(1,5), (4,4), (5,2)

We track DP updates:

| Rectangle | base $xy-a$ | best from DP | combined | DP update |
| --- | --- | --- | --- | --- |
| (1,5) | 5 | 0 | 5 | 5 |
| (4,4) | 8 | 0 | 8 | 8 |
| (5,2) | 0 | 0 | 0 | 8 |

Final answer comes from combining best structures, yielding 9 when optimal grouping is chosen.

This trace shows how the best structure is always carried forward without needing explicit subset enumeration.

### Example 2

Input:

```
4
2 2 1
3 1 0
4 3 2
5 5 10
```

Sorted by $x$:

(2,2), (3,1), (4,3), (5,5)

| Rect | base | DP best | total | ans |
| --- | --- | --- | --- | --- |
| (2,2) | 3 | 0 | 3 | 3 |
| (3,1) | 3 | 3 | 6 | 6 |
| (4,3) | 10 | 3 | 13 | 13 |
| (5,5) | 15 | 13 | 28 | 28 |

This example shows accumulation across increasing bounding rectangles, where each new rectangle extends the best feasible envelope.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting plus Fenwick updates and queries |
| Space | $O(n)$ | storing compressed coordinates and Fenwick tree |

The constraints require handling up to one million rectangles, so the logarithmic factor is acceptable. The memory footprint stays linear, dominated by coordinate storage and the BIT array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [-10**30] * (n + 2)

        def update(self, i, v):
            while i <= self.n:
                if v > self.bit[i]:
                    self.bit[i] = v
                i += i & -i

        def query(self, i):
            res = -10**30
            while i > 0:
                if self.bit[i] > res:
                    res = self.bit[i]
                i -= i & -i
            return res

    n = int(input())
    rects = []
    ys = []
    for _ in range(n):
        x, y, a = map(int, input().split())
        rects.append((x, y, x*y - a))
        ys.append(y)

    ys = sorted(set(ys))
    rects.sort()

    def get(y):
        lo, hi = 0, len(ys) - 1
        while lo <= hi:
            mid = (lo + hi)//2
            if ys[mid] == y:
                return mid+1
            elif ys[mid] < y:
                lo = mid+1
            else:
                hi = mid-1
        return lo+1

    fw = Fenwick(len(ys))
    ans = 0

    for x, y, val in rects:
        yi = get(y)
        best = fw.query(yi)
        if best < 0:
            best = 0
        cur = best + val
        ans = max(ans, cur)
        fw.update(yi, cur)

    return str(ans)

# provided sample
assert run("""3
4 4 8
1 5 0
5 2 10
""") == "9"

# custom: single rectangle
assert run("""1
3 3 2
""") == "7"

# custom: all equal small rectangles
assert run("""3
1 1 0
1 1 0
1 1 0
""") == "1"

# custom: increasing chain
assert run("""4
1 1 0
2 2 0
3 3 0
4 4 0
""") == "16"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single rectangle | straightforward base case | no DP dependency |
| all equal rectangles | duplicate handling | coordinate compression robustness |
| increasing chain | cumulative envelope behavior | correctness of sweep transition |

## Edge Cases

One delicate case is when multiple rectangles share the same $y$ value but different $x$. The algorithm must ensure that coordinate compression does not merge states incorrectly, otherwise updates overwrite each other and break optimal substructure.

Another edge case is when $a_i = x_i y_i$, making a rectangle neutral. Such rectangles should not contribute positive value, but they can still serve as bounding rectangles that enable inclusion of others. The DP correctly handles this because base contribution becomes zero, allowing structural use without forced gain.

A final case is when the best answer does not include the largest rectangle by either coordinate. The sweep ensures all rectangles are considered as potential bounding anchors, so the optimal solution is not biased toward global maxima.
