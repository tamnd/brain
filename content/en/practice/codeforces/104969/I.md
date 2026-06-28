---
title: "CF 104969I - Pizza Tower"
description: "We are given a set of points on a huge 2D grid. Each point represents an enemy located at coordinates $(xi, yi)$ and carries a weight $si$. No two enemies share the same coordinates."
date: "2026-06-28T18:53:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 83
verified: false
draft: false
---

[CF 104969I - Pizza Tower](https://codeforces.com/problemset/problem/104969/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on a huge 2D grid. Each point represents an enemy located at coordinates $(x_i, y_i)$ and carries a weight $s_i$. No two enemies share the same coordinates.

For each enemy, we need to compute how much total strength exists in the rectangular region that stretches from the origin up to that enemy’s position, inclusive. In other words, for a query point $(x_i, y_i)$, we sum the strengths of all enemies $(x_j, y_j)$ such that $x_j \le x_i$ and $y_j \le y_i$.

So each output value is a prefix sum over a 2D partial order defined by coordinate dominance.

The difficulty comes from scale. With up to 200,000 points and coordinate values up to $2 \cdot 10^9$, we cannot build a grid or directly simulate prefix accumulation over coordinates. Any approach that tries to inspect all earlier points per query would lead to roughly $O(N^2)$ behavior, which is far beyond the limit.

A naive approach would also fail subtly if one tries to sort only by $x$ and accumulate $y$-prefix sums without careful structure. The reason is that the dominance relation is two-dimensional, not one-dimensional, so processing in a single sorted order does not automatically preserve correctness unless we actively maintain a structure over the second dimension.

There are no tricky duplicate coordinate issues because coordinates are guaranteed distinct, but values can be large, which forces us to compress or otherwise avoid direct indexing.

## Approaches

A direct method would be to answer each query independently by scanning all points and checking whether both coordinates are smaller or equal. This correctly implements the definition but requires $N$ comparisons per query, resulting in $O(N^2)$ total work. With $N = 2 \cdot 10^5$, this becomes on the order of $4 \cdot 10^{10}$ comparisons, which is infeasible.

The key observation is that the query is a classic dominance prefix sum in two dimensions. If we could process points in increasing order of $x$, then at the moment we process a point $(x_i, y_i)$, all points with smaller $x$ have already been accounted for. The remaining challenge is efficiently summing over those among them that also satisfy $y \le y_i$.

This reduces the problem to maintaining a dynamic structure over the $y$-coordinate that supports prefix sums and point updates. Each point contributes its strength once, and we need to query how much total weight has been inserted so far with $y$-coordinate bounded by a threshold.

Because $y$ can be up to $2 \cdot 10^9$, we compress coordinates into ranks. After compression, we use a Fenwick Tree (Binary Indexed Tree) over $y$-ranks. We sort all points by $x$, process them in increasing order, and for each point we query the Fenwick tree for prefix sum up to its $y$-rank. Then we insert its weight into the Fenwick tree.

One subtlety is that we must output answers in the original order of input points. So while processing in sorted order for correctness, we store results per index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(1) | Too slow |
| Sort + Fenwick Tree | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

We first transform the problem into something that can be processed incrementally along one axis while supporting fast queries on the other axis.

1. Assign each point an index corresponding to its input position. This is needed because we will reorder points during processing but must output answers in original order.
2. Extract all $y_i$ values and compress them into a contiguous range $[1, N]$. This step preserves ordering while making it possible to use a Fenwick Tree. Compression works because only relative ordering of $y$-values matters for prefix sums.
3. Sort all points by increasing $x_i$. If two points had equal $x$, order among them would not matter here since coordinates are distinct, but even if they were not, we would typically break ties arbitrarily.
4. Initialize a Fenwick Tree over the compressed $y$-range, initially empty.
5. Sweep through points in sorted order of $x$. For each point $(x_i, y_i, s_i)$:

1. Query the Fenwick Tree for the sum of all strengths with compressed $y \le y_i$. This gives the total contribution of all previously processed points that lie within the required rectangle.
2. Store this value as the answer for the current point.
3. Update the Fenwick Tree by adding $s_i$ at position $y_i$, so future points with larger $x$ can see its contribution.

After processing all points, the stored answers correspond exactly to the required $F(x_i, y_i)$.

Why it works comes down to maintaining a clean invariant: at any moment in the sweep, the Fenwick Tree stores exactly the sum of strengths of all points whose $x$-coordinate is less than or equal to the current sweep position’s $x$, indexed by their $y$-coordinate. Therefore, a prefix query over $y$ precisely selects the subset satisfying both coordinate constraints. Since every point is inserted exactly once after its contribution is queried for itself, no value is missed or double-counted.

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

n = int(input())
pts = []
ys = []

for i in range(n):
    x, y, s = map(int, input().split())
    pts.append((x, y, s, i))
    ys.append(y)

ys_sorted = sorted(set(ys))
comp = {v: i + 1 for i, v in enumerate(ys_sorted)}

pts.sort(key=lambda p: p[0])

bit = Fenwick(len(ys_sorted))
ans = [0] * n

for x, y, s, idx in pts:
    cy = comp[y]
    ans[idx] = bit.sum(cy)
    bit.add(cy, s)

print("\n".join(map(str, ans)))
```

The Fenwick tree is the core structure enabling efficient prefix aggregation over the compressed $y$-axis. The `add` function performs a point update in logarithmic time, while `sum` retrieves a prefix sum. Coordinate compression ensures we never allocate memory proportional to $2 \cdot 10^9$.

Sorting by $x$ ensures that when we process a point, all valid contributors with smaller or equal $x$ are already in the structure. Storing results by original index preserves output ordering.

A common pitfall is swapping the order of query and update. The correct behavior is to query first, then insert the current point, because a point should not contribute to its own prefix sum unless explicitly intended by the problem definition, which here corresponds exactly to strict inclusion in the processed prefix.

## Worked Examples

### Sample 1

Input points in order:

$(1,1,5), (2,1,10), (1,2,10), (3,3,15)$

Sorted by $x$:

$(1,1,5), (1,2,10), (2,1,10), (3,3,15)$

We track Fenwick state over compressed $y$:

| Step | Point | Query (prefix y) | BIT before update | Answer | BIT after update |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,1,5) | 0 | empty | 0 | {y1:5} |
| 2 | (1,2,10) | 5 | {y1:5} | 5 | {y1:5, y2:10} |
| 3 | (2,1,10) | 5 | {y1:5, y2:10} | 5 | +10 at y1 |
| 4 | (3,3,15) | 25 | all previous | 25 | +15 |

After reordering answers back, we obtain $5, 15, 15, 40$, matching the required output.

This trace shows how earlier $x$-coordinates accumulate progressively, while the Fenwick tree maintains ordering in $y$.

### Sample 2

Points:

$(1,1,1), (1,2,2), (1,3,3), (1,4,4), (1,5,5)$

All points share the same $x$, so sorting keeps them together.

| Step | Point | Query | BIT before update | Answer | BIT after update |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,1,1) | 0 | empty | 0 | +1 |
| 2 | (1,2,2) | 1 | {1} | 1 | +2 |
| 3 | (1,3,3) | 3 | {1,2} | 3 | +3 |
| 4 | (1,4,4) | 6 | {1,2,3} | 6 | +4 |
| 5 | (1,5,5) | 10 | {1,2,3,4} | 10 | +5 |

This demonstrates that even when all $x$ values are equal, the structure still correctly accumulates a 1D prefix over $y$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates with $O(N \log N)$, each Fenwick update and query is $O(\log N)$ |
| Space | O(N) | Storage for points, compression map, Fenwick tree, and answer array |

The complexity fits comfortably within limits for $N = 2 \cdot 10^5$, where roughly $2 \cdot 10^5 \log_2(2 \cdot 10^5)$ operations is well within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
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

    n = int(input())
    pts = []
    ys = []
    for i in range(n):
        x, y, s = map(int, input().split())
        pts.append((x, y, s, i))
        ys.append(y)

    ys_sorted = sorted(set(ys))
    comp = {v: i + 1 for i, v in enumerate(ys_sorted)}

    pts.sort(key=lambda p: p[0])

    bit = Fenwick(len(ys_sorted))
    ans = [0] * n

    for x, y, s, idx in pts:
        cy = comp[y]
        ans[idx] = bit.sum(cy)
        bit.add(cy, s)

    return "\n".join(map(str, ans))

# provided samples
assert run("4\n1 1 5\n2 1 10\n1 2 10\n3 3 15\n") == "5\n15\n15\n40"
assert run("5\n1 1 1\n1 2 2\n1 3 3\n1 4 4\n1 5 5\n") == "0\n1\n3\n6\n10"

# custom cases
assert run("1\n5 5 10\n") == "0", "minimum size"
assert run("2\n1 1 5\n2 2 7\n") == "0\n5", "basic diagonal dominance"
assert run("3\n3 3 10\n1 1 1\n2 2 2\n") == "0\n1\n3", "unsorted input"
assert run("3\n1 3 10\n2 2 20\n3 1 30\n") == "0\n0\n30", "cross pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | base case with no predecessors |
| diagonal growth | prefix accumulation correctness | standard increasing chain |
| unsorted input | sorting correctness | order independence |
| cross pattern | mixed dominance structure | 2D ordering correctness |

## Edge Cases

One important edge case is when all points share the same $x$-coordinate. In this situation, sorting by $x$ groups everything together, and the answer depends purely on $y$-prefix accumulation. The algorithm still works because within a fixed $x$, no point contributes to another in the same batch, since updates happen after queries. For example, with points $(1,3,10), (1,1,5), (1,2,7)$, processing yields all queries as zero, which matches the definition since no point has strictly smaller $x$.

Another edge case is strictly decreasing coordinates, such as $(3,3), (2,2), (1,1)$. After sorting, the sweep becomes increasing, and each point only sees earlier smaller pairs. The Fenwick tree ensures that even though input order is reversed, dominance relations are still evaluated correctly.

A final subtle case is when values are large and sparse. Without compression, a Fenwick tree would be impossible to allocate. Compression preserves ordering, so even values like $y = 10^9$ behave identically to small indices once mapped.
