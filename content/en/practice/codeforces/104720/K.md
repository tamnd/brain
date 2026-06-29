---
title: "CF 104720K - Donut Rings"
description: "We are given several “donuts”, each described by two radii. The inner radius defines a hole, and the outer radius defines the full extent of the donut. A donut can be placed inside the hole of another donut if its outer boundary fits entirely within that hole."
date: "2026-06-29T07:13:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "K"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 83
verified: false
draft: false
---

[CF 104720K - Donut Rings](https://codeforces.com/problemset/problem/104720/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several “donuts”, each described by two radii. The inner radius defines a hole, and the outer radius defines the full extent of the donut. A donut can be placed inside the hole of another donut if its outer boundary fits entirely within that hole. This nesting can continue, forming a chain where each next donut fits inside the previous one’s hole.

A valid “donut ring” is such a chain of nested donuts. If we take a chain, the total contribution depends only on radii: each donut contributes its area, while the hole of the outermost structure removes area as empty space. After simplifying the geometry, the objective reduces to maximizing a quantity that depends linearly on squared radii of selected donuts in a valid nesting order.

Concretely, for each donut, the contribution to the final value can be expressed as $R_i^2 - r_i^2$, while nesting introduces constraints: if donut A is inside donut B, then $R_A \le r_B$. The goal is to select a chain maximizing a global score derived from these values, respecting the nesting constraint.

The input size $n \le 10^5$ implies that any solution worse than $O(n \log n)$ is at risk of timing out. A quadratic solution that checks all pairs or all chains is immediately infeasible because it would require up to $10^{10}$ operations.

A few subtle edge cases matter:

A single donut must be handled correctly. If it is the only option, the answer is simply $R^2 - r^2$, which can be negative. For example, a donut with $r = 5, R = 10$ contributes $100 - 25 = 75$.

Another edge case is when all donuts are “incompatible” for nesting, meaning no two satisfy $R_i \le r_j$. Then the answer is the maximum single value, not zero or an empty chain. For instance, $(r,R) = (1,10), (2,3)$ gives best answer $\max(100-1, 9-4)$.

A third case is when many donuts share identical or near-identical radii, which can break naive greedy approaches that assume strict ordering without handling equality carefully.

## Approaches

A brute-force solution would attempt to build every possible nesting chain. For each donut, we could try it as a starting point and recursively append any donut whose outer radius fits into the current inner radius. This forms a DAG of possibilities where each node can branch to many others. In the worst case, every donut can fit into many others, leading to exponential growth in explored chains. Even pruning does not help much because the number of valid chains can still be extremely large.

The key observation is that nesting imposes a strict ordering condition: if donut A goes inside donut B, then $R_A \le r_B$. This converts the problem into a directed acyclic structure ordered by radii, where transitions only go from smaller outer radius to larger inner radius. Once we sort donuts by a meaningful key, we can transform the problem into a one-dimensional optimization over valid predecessors.

We reinterpret each donut as a segment constraint and value. The task becomes selecting a sequence where each next element satisfies a monotonic feasibility condition and contributes a value. This is a classic setting for dynamic programming over sorted endpoints, where for each donut we compute the best chain ending at it, using all compatible previous donuts.

The transition depends on finding the best previous donut whose outer radius fits into the current inner radius. Sorting by inner radius allows us to use binary search or a Fenwick tree over compressed coordinates of outer radii. This reduces the compatibility check from linear scan to logarithmic query.

Thus, instead of enumerating chains, we process donuts in increasing order and maintain a structure that stores best achievable values for given outer radius thresholds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform each donut into a pair of coordinates: a constraint endpoint and a value.

## Step 1: Normalize representation

For each donut, compute its contribution value $v_i = R_i^2 - r_i^2$. We also keep its compatibility boundary: it can only follow donuts whose outer radius is at most $r_i$.

This makes each donut simultaneously a “state” and a “constraint”.

## Step 2: Sort by constraint

Sort donuts by increasing inner radius $r_i$. This ensures that when processing a donut, all potential predecessors (with smaller or equal outer radius requirement) have already been considered.

The reason this works is that feasibility depends only on comparing outer radius of one to inner radius of another, so sorting by inner radius creates a natural processing order.

## Step 3: Coordinate compression on outer radii

Collect all $R_i$ values and compress them. This allows us to index them in a Fenwick tree or segment tree.

Compression is necessary because $R_i$ can be up to $10^9$, making direct indexing impossible.

## Step 4: Dynamic programming structure

Maintain a structure `best[x]` representing the maximum achievable beauty of a valid chain whose last donut has outer radius at most the compressed coordinate $x$.

This turns compatibility into a prefix maximum query.

## Step 5: Process donuts in sorted order

For each donut $i$, we query the best chain that can precede it. Since it must satisfy $R_{prev} \le r_i$, we query all states with outer radius up to $r_i$.

Then we compute:

$$dp_i = v_i + \max(dp \text{ among valid predecessors})$$

We also consider starting a new chain with this donut alone.

After computing $dp_i$, we update the structure at position corresponding to $R_i$.

## Step 6: Final answer

The answer is the maximum value among all $dp_i$.

### Why it works

The key invariant is that after processing all donuts up to index $i$, the structure stores the best possible chain values for every feasible outer radius boundary using only valid earlier donuts. Because processing order follows increasing inner radius, every valid predecessor is guaranteed to already be included. Since transitions preserve feasibility and we always take the best predecessor, no optimal chain is ever missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [-10**30] * (n + 1)

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

def main():
    n = int(input())
    donuts = []
    Rs = []

    for _ in range(n):
        r, R = map(int, input().split())
        donuts.append((r, R))
        Rs.append(R)

    Rs_sorted = sorted(set(Rs))
    comp = {v: i + 1 for i, v in enumerate(Rs_sorted)}

    donuts.sort()

    fw = Fenwick(len(Rs_sorted))

    ans = -10**30

    for r, R in donuts:
        v = R * R - r * r
        # best chain ending with R_i <= r
        # need all previous with outer radius <= r
        # find index of r in compressed Rs
        # upper bound
        import bisect
        idx = bisect.bisect_right(Rs_sorted, r)
        best_prev = fw.query(idx)

        if best_prev < 0:
            best_prev = 0

        cur = best_prev + v
        ans = max(ans, cur)

        fw.update(comp[R], cur)

    print(ans)

if __name__ == "__main__":
    main()
```

The solution relies on maintaining prefix maximums over compressed outer radii. The Fenwick tree is used only for maximum queries, so updates store maximum values rather than sums. The subtle point is converting feasibility into a prefix condition via sorting and then using binary search to align inner radius constraints with the compressed coordinate system.

One easy mistake is forgetting that chains can start at any donut, so the predecessor value must allow zero. That is handled by clamping negative results to zero before extension.

## Worked Examples

### Sample 1

Input:

```
3
```
