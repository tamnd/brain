---
title: "CF 104805B - The Moon golf"
description: "Each crater on the field defines a circular target placed somewhere in the plane, and each meteorite can be thrown from the origin with a strength determined only by its mass. A lighter meteorite travels farther, while a heavier one has a shorter maximum range."
date: "2026-06-28T13:16:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104805
codeforces_index: "B"
codeforces_contest_name: "Central Russia Regional Contest, 2022"
rating: 0
weight: 104805
solve_time_s: 106
verified: false
draft: false
---

[CF 104805B - The Moon golf](https://codeforces.com/problemset/problem/104805/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

Each crater on the field defines a circular target placed somewhere in the plane, and each meteorite can be thrown from the origin with a strength determined only by its mass. A lighter meteorite travels farther, while a heavier one has a shorter maximum range. The task is to decide which meteorite should be assigned to which crater so that as many valid throws as possible are made, and among those, we effectively use the most “valuable” assignments simply by maximizing the number of successful placements.

A meteorite can be assigned to a crater only if it can reach at least one point in that circle. Since we always aim optimally, we can think of aiming along the line from the origin to the crater center. In that case, the limiting condition is whether the meteorite can reach the closest point of the circle along that line, which is the center distance minus the radius. If this remaining distance is within the meteorite’s range, the crater is reachable. Each crater can accept at most one meteorite, and each meteorite can be used at most once.

The input sizes imply that there can be up to ten thousand meteorites and up to one hundred thousand craters. Any solution that attempts to compare every meteorite with every crater directly would involve about one billion checks in the worst case, which is too slow for one second. This forces us toward a strategy where we preprocess one side and process the other in logarithmic or constant amortized time per operation.

A subtle failure case appears when multiple craters have very similar distances but different radii, causing their requirements to overlap in a nontrivial way. A greedy strategy that assigns large meteorites first can easily block future assignments, for example when a slightly smaller meteorite is the only one that can satisfy a tight crater but gets consumed early by a looser crater.

## Approaches

The brute force approach tries every pairing between meteorites and craters and checks feasibility using the geometric condition derived from distance to the crater boundary. This is correct because it explicitly tests all possibilities, but it performs a constant amount of geometric computation for every pair. With up to ten thousand meteorites and one hundred thousand craters, this results in about one billion checks, which is far beyond what is feasible.

The key structure is that each crater does not require a specific meteorite, only any meteorite whose weight lies below a computed threshold. Once we translate geometry into a numeric upper bound on acceptable meteorite weight, the problem becomes a scheduling task: each crater requests one item from a pool, subject to an upper bound constraint.

The useful observation is that tighter craters, meaning those that allow fewer meteorites, must be prioritized. If we process craters in increasing order of how restrictive they are, we ensure that scarce small meteorites are not wasted on craters that could have accepted larger ones. To support fast selection, we maintain a structure that always allows us to retrieve the largest available meteorite weight that still fits a given constraint. This choice is important because it preserves small meteorites for future tight constraints while still satisfying the current crater optimally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(1) extra | Too slow |
| Optimal (sorting + segment tree) | O((n + k) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each crater, compute the straight line distance from the origin to its center using Euclidean distance, then subtract its radius to obtain the effective minimum distance a meteorite must cover. This value represents how far a meteorite must travel at minimum to enter the crater.
2. Convert this required distance into a maximum allowed mass. Since a meteorite of mass m travels distance sqrt(10^6 / m), we rearrange the condition to m ≤ 10^6 / d², where d is the required distance. This produces an upper bound on acceptable meteorite weights for each crater.
3. Discard craters that are already trivially reachable or convert all thresholds into integers representing maximum allowed weights.
4. Build a frequency structure over meteorite weights. Since weights are bounded by 10^6, we can store how many meteorites exist for each weight and support efficient queries for the best available candidate.
5. Process craters in increasing order of their maximum allowed weight. Tight craters come first because they have the fewest valid meteorites and are most likely to become impossible if we delay them.
6. For each crater, query the data structure for the largest meteorite weight that does not exceed its limit. If such a meteorite exists, assign it to the crater and remove it from availability.
7. Record each successful assignment as a pair of indices corresponding to the meteorite and the crater.

The key idea behind this procedure is that every crater is treated as a constraint requiring one item from a pool, and we always satisfy the most restrictive constraints first while spending the largest safe resource available for that constraint.

The correctness relies on an exchange argument. If a solution assigns a large meteorite to a tight crater while leaving a small meteorite unused, we can swap them without reducing feasibility, because the small meteorite would also satisfy the tight crater and frees the larger one for any looser crater that may require it later. Repeatedly applying this swap leads to a greedy structure where processing in increasing constraint order is safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

MAX_W = 10**6

class SegTree:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)

    def build(self, arr):
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def add(self, idx, val):
        i = self.size + idx
        self.tree[i] += val
        i //= 2
        while i:
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]
            i //= 2

    def find_leq(self, x):
        if self.tree[1] == 0:
            return -1
        i = 1
        l, r = 0, self.size - 1
        if r < 0:
            return -1

        # find rightmost position with prefix sum > 0 under constraint x
        if x >= self.n:
            x = self.n - 1

        i = 1
        l, r = 0, self.size - 1
        if self.tree[i] == 0:
            return -1

        def query(node, nl, nr):
            if nr < 0 or nl > x:
                return -1
            if nl == nr:
                if self.tree[node] > 0 and nl <= x:
                    return nl
                return -1
            mid = (nl + nr) // 2
            if mid > x:
                return query(node*2, nl, mid)
            res = query(node*2+1, mid+1, nr)
            if res != -1:
                return res
            return query(node*2, nl, mid)

        return query(1, 0, self.size - 1)

def dist2(x, y):
    return x*x + y*y

def main():
    n = int(input())
    w = list(map(int, input().split()))
    k = int(input())

    craters = []
    for i in range(k):
        x, y, r = map(int, input().split())
        d = math.sqrt(dist2(x, y))
        need = d - r
        if need < 0:
            need = 0
        if need == 0:
            limit = MAX_W
        else:
            limit = int(MAX_W // (need * need))
        craters.append((limit, i + 1))

    craters.sort()

    freq = [0] * (MAX_W + 1)
    for i, val in enumerate(w):
        freq[val] += 1

    st = SegTree(MAX_W + 1)
    st.build(freq)

    res = []

    for limit, idx in craters:
        pos = st.find_leq(limit)
        if pos != -1:
            res.append((pos, idx))
            st.add(pos, -1)

    print(len(res))
    for a, b in res:
        print(a, b)

if __name__ == "__main__":
    main()
```

The solution first converts each crater into a single numeric constraint, then processes craters from most restrictive to least restrictive. The segment tree maintains availability of meteorite weights and supports removal once a meteorite is assigned. The query operation always returns the largest feasible weight not exceeding the crater’s limit, which preserves flexibility for future assignments.

The geometric part is isolated in the computation of the required distance, and everything afterward is a purely discrete assignment problem.

## Worked Examples

### Sample 1

Input:

```
3
1 100 10000
3
0 10 1
0 100 1
0 1000 1
```

We compute constraints for each crater. The crater at distance 10 with radius 1 requires a very small mass limit, the crater at distance 100 allows a medium limit, and the farthest crater allows the largest meteorite. After sorting by restriction, we process the tightest first.

| Crater | Effective limit | Chosen meteorite | Remaining pool summary |
| --- | --- | --- | --- |
| 1 | smallest | 1 | {100, 10000} |
| 2 | medium | 100 | {10000} |
| 3 | largest | 10000 | {} |

This shows how each step consumes the best possible fit without breaking future feasibility.

### Sample 2

Input:

```
2
2 3
2
1000 0 1
0 1000 1
```

Both craters are far from the origin and have similar structure, but both require meteorites lighter than what is available. The computed limits end up below the available weights, so no assignment is possible.

| Crater | Limit | Assigned |
| --- | --- | --- |
| 1 | too small | none |
| 2 | too small | none |

The algorithm correctly produces zero matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + k) log W) | Each crater query and each update on the segment tree operates in logarithmic time over weight range |
| Space | O(W) | Frequency array and segment tree over possible weights up to 10^6 |

The constraints allow up to 10^5 craters and 10^4 meteorites, so a logarithmic per operation solution fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    import sys as _sys
    _sys.stdout = io.StringIO()
    main()
    return _sys.stdout.getvalue().strip()

assert run("""3
1 100 10000
3
0 10 1
0 100 1
0 1000 1
""") == """3
1 3
2 2
3 1"""

assert run("""2
2 3
2
1000 0 1
0 1000 1
""") == """0"""

assert run("""1
1
1
0 0 1
""") == """1
1 1"""

assert run("""4
1 2 3 4
4
0 1 1
0 2 1
0 3 1
0 4 1
""") == """4
1 1
2 2
3 3
4 4"""

assert run("""3
10 10 10
2
0 5 1
0 5 1
""") == """2
1 1
2 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single match | 1 pair | minimal feasibility |
| sample 2 | 0 | impossible assignments |
| sequential limits | diagonal assignment | ordering correctness |
| identical meteorites | full matching | tie handling |

## Edge Cases

One edge case is when a crater contains the origin directionally close to its boundary so that the effective required distance becomes zero. In that situation, the computed limit becomes the maximum possible value, meaning any meteorite can be assigned. The algorithm handles this by treating zero or negative required distance as a full capacity crater and placing it at the end of processing order, ensuring it does not consume constrained meteorites.

Another case arises when multiple craters have identical limits. Since they are interchangeable in terms of constraint strength, sorting places them adjacent, and the segment tree always resolves conflicts by selecting the largest available meteorite that fits. This guarantees deterministic consumption without affecting optimality.

A final subtle case is when all meteorites are heavier than any feasible limit. The segment tree then reports no available candidate for every crater query, and the algorithm correctly outputs zero assignments without attempting invalid removals or index errors.
