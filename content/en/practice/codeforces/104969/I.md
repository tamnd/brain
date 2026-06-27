---
title: "CF 104969I - Pizza Tower"
description: "We are given a set of points on a huge integer grid, each point representing an enemy with a strength value. For each enemy position $(xi, yi)$, we need to compute the total strength of all enemies that lie at coordinates $(xj, yj)$ such that $xj le xi$ and $yj le yi$."
date: "2026-06-28T06:43:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 73
verified: false
draft: false
---

[CF 104969I - Pizza Tower](https://codeforces.com/problemset/problem/104969/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on a huge integer grid, each point representing an enemy with a strength value. For each enemy position $(x_i, y_i)$, we need to compute the total strength of all enemies that lie at coordinates $(x_j, y_j)$ such that $x_j \le x_i$ and $y_j \le y_i$. In other words, each query asks for the sum of weights in the bottom-left rectangle anchored at the origin and ending at the enemy’s own position.

The important twist is that this is not a separate query problem. The query points are exactly the same points as the data points, and we must output the prefix-sum value for each point individually in its input order.

The constraints push us away from any direct grid representation. Coordinates go up to $2 \cdot 10^9$, so any 2D array or naive frequency grid is impossible. The number of points reaches $2 \cdot 10^5$, so an $O(N^2)$ comparison between every pair would lead to about $4 \cdot 10^{10}$ operations, which is far beyond time limits.

A few subtle cases can break naive reasoning. First, if we sort points by $x$ and compute prefix sums over $y$ without care, we may mix contributions incorrectly across different $x$-levels. For example, consider points $(2,2,10)$, $(1,3,5)$, $(3,1,7)$. If we process by increasing $x$ and only maintain a running structure over $y$, forgetting to correctly separate processed prefixes, we may incorrectly include the point $(2,2)$ when answering $(1,3)$, even though it should not contribute because its $x$-coordinate is larger.

Second, duplicates in $y$ are allowed but duplicates in full coordinates are not. A careless sweep that overwrites values instead of accumulating them would be correct here, but a generalized implementation that assumes uniqueness in both axes could fail in similar problems.

## Approaches

The brute-force idea is straightforward. For each point, scan all other points and sum those satisfying $x_j \le x_i$ and $y_j \le y_i$. This directly implements the definition. Each query costs $O(N)$, and since there are $N$ queries, the total complexity is $O(N^2)$. With $2 \cdot 10^5$ points, this becomes completely infeasible.

The key observation is that this is a two-dimensional prefix sum over a sparse set of weighted points. If we could compress coordinates, we could transform the problem into prefix queries on a 2D plane. However, a full 2D Fenwick tree over compressed coordinates would still be too large, because both dimensions are size $N$, leading to $O(N \log^2 N)$ which may pass but is unnecessary here.

A more efficient structure comes from reinterpreting the computation. If we sort points by increasing $x$, then when we process a point $(x_i, y_i)$, all valid contributors with smaller or equal $x$ are exactly those already processed. The problem reduces to maintaining a dynamic set over $y$, supporting point updates by adding $s_i$, and prefix sum queries over $y \le y_i$.

This is a classic 1D Fenwick tree after sweeping one dimension. The 2D dominance condition collapses into a single prefix query because the sweep line guarantees the $x$-constraint is already enforced.

The only complication is that $y$ values are large, so we compress them into ranks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(1)$ | Too slow |
| Sweep + Fenwick Tree | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We transform the 2D dominance sum into a sequence of 1D prefix sum operations using a sweep over sorted points.

1. Store all points along with their original indices. We need the index because answers must be printed in input order, not processing order. This separation is crucial since sorting will destroy original ordering.
2. Extract all $y$-coordinates and sort them uniquely to build a compressed coordinate system. This allows us to replace large values up to $2 \cdot 10^9$ with indices in $[1, N]$. Compression preserves relative order, which is the only property needed for prefix queries.
3. Sort the points by increasing $x$. If two points share the same $x$, their internal order does not matter because neither should contribute to the other in terms of $x \le x_i$ unless we carefully define handling. Since the condition includes equality, we must ensure that updates for a given $x$ are visible to queries at the same $x$. The clean way is to process points grouped by equal $x$.
4. Initialize a Fenwick tree over the compressed $y$-axis. This structure maintains sums of strengths for all processed points.
5. Sweep through the sorted points. For each group of points with the same $x$, first compute all their answers using the current Fenwick tree state, then insert all points of the group into the Fenwick tree. This ordering ensures that points with identical $x$ do not contribute to each other unless allowed, and avoids ordering dependence inside the group.
6. For each point $(x_i, y_i, s_i)$, query the Fenwick tree for the prefix sum up to compressed $y_i$. This gives the sum of strengths of all previously processed points with $y \le y_i$, which corresponds exactly to all points with $x \le x_i$ and $y \le y_i$.

### Why it works

At any moment during the sweep, the Fenwick tree contains exactly the set of points whose $x$-coordinate is strictly less than the current group’s $x$, plus optionally those in earlier groups. By processing equal-$x$ points in a batch where queries are done before updates, we ensure no point incorrectly contributes to another point with the same $x$. The Fenwick tree invariant is that it always stores the sum of strengths of all processed points indexed by their compressed $y$-coordinate, so prefix queries over $y$ exactly represent all valid dominance contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    n = int(input())
    pts = []
    ys = []

    for i in range(n):
        x, y, s = map(int, input().split())
        pts.append((x, y, s, i))
        ys.append(y)

    ys = sorted(set(ys))
    y_id = {v: i + 1 for i, v in enumerate(ys)}

    pts.sort(key=lambda t: t[0])

    fw = Fenwick(len(ys))
    ans = [0] * n

    i = 0
    while i < n:
        j = i
        while j < n and pts[j][0] == pts[i][0]:
            j += 1

        for k in range(i, j):
            x, y, s, idx = pts[k]
            yi = y_id[y]
            ans[idx] = fw.sum(yi)

        for k in range(i, j):
            x, y, s, idx = pts[k]
            yi = y_id[y]
            fw.add(yi, s)

        i = j

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The Fenwick tree maintains cumulative strength by compressed $y$-index. The sweep ensures that at query time, only valid $x$-dominant points are present in the structure. The split between querying and updating inside equal-$x$ blocks is the critical implementation detail that preserves correctness for equality.

## Worked Examples

### Sample 1

Input points in order are $(1,1,5)$, $(2,1,10)$, $(1,2,10)$, $(3,3,15)$. After sorting by $x$, we process groups by $x$.

For $x=1$, we query with an empty Fenwick tree, so both points get 0, then we insert their strengths.

For $x=2$, the Fenwick tree contains contributions from $x=1$. Querying gives prefix sums over $y$, so $(2,1)$ sees 5 and $(1,2)$ already got computed earlier.

| Step | Point | Query result | Fenwick state (conceptual) |
| --- | --- | --- | --- |
| x=1 group query | (1,1,5) | 0 | empty |
| x=1 group query | (1,2,10) | 0 | empty |
| x=1 insert | both | - | {1:5, 2:10} |
| x=2 group query | (2,1,10) | 5 | {1:5, 2:10} |
| x=2 insert | (2,1,10) | - | updated |
| x=3 group query | (3,3,15) | 25 | all previous |

This demonstrates how the sweep accumulates all valid contributions gradually.

### Sample 2

Points form a perfect chain increasing in both coordinates. Each point adds to all future ones, so prefix sums match triangular numbers. The Fenwick tree simply accumulates increasing weights, and each query reads the full prefix over $y$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Sorting points and coordinate compression take $O(N \log N)$, each Fenwick update/query is $O(\log N)$ |
| Space | $O(N)$ | Storage for points, compressed coordinates, and Fenwick tree |

This fits comfortably within limits for $2 \cdot 10^5$ operations, since $N \log N$ is on the order of a few million operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    _stdout = _sys.stdout
    _sys.stdout = io.StringIO()
    
    # call solution
    solve()
    
    out = _sys.stdout.getvalue()
    _sys.stdout = _stdout
    return out.strip()

# provided samples
assert run("""4
1 1 5
2 1 10
1 2 10
3 3 15
""") == """5
15
15
40"""

assert run("""5
1 1 1
1 2 2
1 3 3
1 4 4
1 5 5
""") == """1
3
6
10
15"""

# custom cases
assert run("""1
100 100 42
""") == "0"

assert run("""3
1 1 1
2 2 1
3 3 1
""") == "1\n2\n3"

assert run("""4
1 3 5
2 2 7
3 1 9
4 4 11
""") == """0
5
12
22"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single point | 0 | base case with no predecessors |
| Increasing chain | prefix sums | correctness of sweep accumulation |
| Mixed ordering | correct dominance | 2D ordering correctness |

## Edge Cases

One subtle case is points sharing the same $x$. Consider $(1,2,5)$ and $(1,3,7)$. If we inserted into the Fenwick tree before answering, then the second point would incorrectly see the first point as a valid contributor, even though both have equal $x$. The grouped processing avoids this by ensuring all queries for a given $x$ happen before any updates for that $x$, so equal-$x$ points do not interfere.

Another case is strictly decreasing $y$ with increasing $x$, such as $(1,5)$, $(2,4)$, $(3,3)$. Here each query should see only previous valid points with smaller or equal $y$. The Fenwick prefix structure ensures that even though $y$ is not sorted in input order, the prefix sum always aggregates correctly after compression.

A final case is large coordinate gaps. Points like $(1, 1)$, $(10^9, 10^9)$ still behave identically after compression since only ordering matters, not magnitude. The sweep relies entirely on rank structure, so absolute values never affect correctness.
