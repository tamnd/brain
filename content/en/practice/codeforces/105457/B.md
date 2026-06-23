---
title: "CF 105457B - Islands and Mountains"
description: "We are given a line of land split into $n$ consecutive segments, each with a fixed height. Over time, the sea level rises in steps, and after each rise we must determine how many connected groups of dry land remain."
date: "2026-06-23T17:46:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105457
codeforces_index: "B"
codeforces_contest_name: "XXIII Spain Olympiad in Informatics, Online Qualifier 1"
rating: 0
weight: 105457
solve_time_s: 78
verified: true
draft: false
---

[CF 105457B - Islands and Mountains](https://codeforces.com/problemset/problem/105457/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of land split into $n$ consecutive segments, each with a fixed height. Over time, the sea level rises in steps, and after each rise we must determine how many connected groups of dry land remain.

A segment is considered dry if its height is strictly above the current sea level threshold condition $a_i > m$, otherwise it is submerged. Dry segments that are adjacent in the original line form a single island, so an island is simply a maximal contiguous block of indices whose heights are above the current sea level.

After each year, some segments become flooded permanently as the sea level increases, which can only break existing islands into smaller ones or eliminate them entirely.

The input consists of multiple independent cases. Each case gives a height array and a strictly increasing sequence of sea levels. For every sea level, we must output the number of connected dry components.

The constraints make the structure clear: $n$ and $k$ can reach $10^5$, so recomputing islands from scratch after each query would be far too slow. Any solution that repeatedly scans the array per query would cost $O(nk)$, which reaches $10^{10}$ operations in the worst case and is not viable.

A subtle failure case for naive approaches is recomputation without remembering previous state. For example, consider heights $[5, 1, 5]$ and sea levels $1$ then $5$. At level $1$, we have two islands: positions 0 and 2 are dry. At level $5$, everything is submerged, so the answer is $0$. A naive scan per query still works here, but many incorrect optimizations attempt to “update counts locally” without tracking that middle flooding merges separation events correctly in reverse reasoning, which breaks consistency when multiple points flood at once.

Another important edge case is equal heights. Since flooding happens when $a_i \le m_i$, segments disappear exactly at their height threshold, and failing to treat equality correctly leads to off-by-one island counts.

## Approaches

A direct approach recomputes the island count after each sea level by scanning the entire array and counting how many times a dry segment starts. This works because every island is a contiguous run of dry cells, so we can detect a new island whenever $a_i > m$ and either $i = 0$ or $a_{i-1} \le m$. The correctness is straightforward, but doing this for every query repeats the same full traversal $k$ times.

The bottleneck is obvious: each query costs $O(n)$, so total complexity becomes $O(nk)$. With both up to $10^5$, this is far beyond any practical limit.

The key observation is that flooding is monotonic. Once a segment is submerged, it never returns. Instead of simulating the process forward, we reverse the perspective: imagine all land is initially flooded and we “unflood” segments in decreasing order of sea level, or equivalently process segments by increasing height.

When we sort segments by height, each time we “activate” a segment (meaning it becomes dry as the sea level passes below it), it either forms a new island or merges two existing islands if both neighbors are already active. This is a classic dynamic connectivity process on a line, which can be maintained with a disjoint-set structure.

To connect this with queries, we process activations in increasing height order while simultaneously processing queries in increasing sea level order. For each query threshold, we activate all segments with height greater than that threshold, maintaining connected components.

Each activation either increases island count by one or decreases it depending on whether neighbors are active. Union-find on a line ensures each merge is $O(\alpha(n))$, giving an almost linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ | $O(1)$ | Too slow |
| Sorting + DSU sweep | $O((n+k)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform the problem into a reverse activation process where land appears gradually from highest to lowest.

1. Pair each segment index with its height and sort these pairs by height in descending order. This lets us activate land from tallest to shortest, ensuring that when a segment becomes active, all higher segments are already active. This ordering is crucial because island structure depends only on whether neighbors are active, not on absolute heights.
2. Sort queries by sea level in descending order while keeping original indices. Each query represents a threshold; we will activate all segments strictly above that threshold before answering it.
3. Maintain a boolean array `active[i]` indicating whether segment $i$ is currently dry. Also maintain a disjoint-set union structure over indices to track connected components among active segments.
4. Keep a counter `islands` initialized to zero. Each time a new segment becomes active, we tentatively treat it as a new island.
5. When activating position $i$, check its left neighbor $i-1$ and right neighbor $i+1$. If a neighbor is active, we union the sets. Every time two previously separate components merge, we reduce the island count by one. This ensures the count always matches the number of connected active components.
6. Process queries in descending order. For each query value $m$, activate all segments with height greater than $m$. After processing all such activations, store the current `islands` as the answer for that query.
7. Restore answers back to original query order.

The core invariant is that at any moment, DSU components exactly correspond to contiguous blocks of active indices. Each component represents one island because adjacency is the only allowed connection. When we activate a new cell, it either creates a new isolated component or merges with up to two neighbors, which correctly updates the island count.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

def solve_case(n, k, a, m):
    segs = sorted([(a[i], i) for i in range(n)], reverse=True)
    queries = sorted([(m[i], i) for i in range(k)], reverse=True)

    dsu = DSU(n)
    active = [False] * n

    ans = [0] * k
    ptr = 0
    islands = 0

    for qval, qi in queries:
        while ptr < n and segs[ptr][0] > qval:
            h, i = segs[ptr]
            active[i] = True
            islands += 1

            if i > 0 and active[i - 1]:
                if dsu.union(i, i - 1):
                    islands -= 1
            if i + 1 < n and active[i + 1]:
                if dsu.union(i, i + 1):
                    islands -= 1

            ptr += 1

        ans[qi] = islands

    return ans

def main():
    data = sys.stdin.read().strip().split()
    idx = 0
    out = []

    while idx < len(data):
        n = int(data[idx]); k = int(data[idx + 1])
        idx += 2
        a = list(map(int, data[idx:idx + n]))
        idx += n
        m = list(map(int, data[idx:idx + k]))
        idx += k

        res = solve_case(n, k, a, m)
        out.append(" ".join(map(str, res)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The DSU tracks connectivity among currently active segments. The `active` array ensures we only merge already-unflooded land. Each union corresponds to two islands merging, so decrementing the counter preserves correctness.

A subtle implementation detail is the strict comparison `a[i] > m`. This is why activation uses `> qval`. If we mistakenly used `>=`, segments exactly at water level would be treated incorrectly and would remain active too long, inflating island counts.

The pointer `ptr` ensures each segment is activated once across all queries, making the sweep linear after sorting.

## Worked Examples

### Example 1

Input:

```
n = 7, k = 1
a = [9, 1, 6, 1, 3, 7, 2]
m = [5]
```

Sorted segments by height:

| step | height | index | active set | islands |
| --- | --- | --- | --- | --- |
| 1 | 9 | 0 | {0} | 1 |
| 2 | 7 | 5 | {0,5} | 2 |
| 3 | 6 | 2 | {0,2,5} | 3 |
| 4 | 3 | 4 | {0,2,4,5} | 3 (merge if adjacent none) |
| 5 | 2 | 6 | {0,2,4,5,6} | 3 |
| 6 | 1 | 1 | {0,1,2,4,5,6} | 2 |
| 7 | 1 | 3 | all | 1 |

For threshold 5, only values strictly greater than 5 are activated: 9, 7, 6. These form components {0}, {5}, {2}, giving 3 islands.

This trace shows that islands correspond exactly to connected components in the activated set.

### Example 2

Input:

```
n = 5, k = 3
a = [2, 2, 2, 2, 2]
m = [1, 2, 3]
```

| query | activated indices | islands |
| --- | --- | --- |
| 3 | none | 0 |
| 2 | none (strict > 2) | 0 |
| 1 | all | 1 |

This case shows the strict inequality behavior clearly. At level 2, everything is submerged, so no islands exist. Only when threshold drops below 2 does land appear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + k)\log n)$ | sorting segments and queries dominates; DSU operations are almost constant |
| Space | $O(n)$ | DSU arrays and activation state |

The solution fits comfortably within limits because each element is sorted once and union-find operations are amortized inverse Ackermann time, effectively constant in practice even for $10^5$ elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import deque

    # assume solution is defined above in same runtime
    return main_capture(inp)

def main_capture(inp: str) -> str:
    import sys
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    idx = 0
    out = []

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return False
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]
            return True

    def solve_case(n, k, a, m):
        segs = sorted([(a[i], i) for i in range(n)], reverse=True)
        queries = sorted([(m[i], i) for i in range(k)], reverse=True)

        dsu = DSU(n)
        active = [False] * n
        ans = [0] * k
        ptr = 0
        islands = 0

        for qval, qi in queries:
            while ptr < n and segs[ptr][0] > qval:
                h, i = segs[ptr]
                active[i] = True
                islands += 1

                if i > 0 and active[i - 1]:
                    if dsu.union(i, i - 1):
                        islands -= 1
                if i + 1 < n and active[i + 1]:
                    if dsu.union(i, i + 1):
                        islands -= 1

                ptr += 1

            ans[qi] = islands

        return ans

    while idx < len(data):
        n = int(data[idx]); k = int(data[idx + 1])
        idx += 2
        a = list(map(int, data[idx:idx + n]))
        idx += n
        m = list(map(int, data[idx:idx + k]))
        idx += k
        out.append(" ".join(map(str, solve_case(n, k, a, m))))

    return "\n".join(out)

# provided samples
assert run("""7 1
9 1 6 1 3 7 2
5
""") == "3", "sample 1"

assert run("""10 5
9 5 4 10 3 2 5 6 2 6
3 4 6 8 9
""") == "3 4 2 2 1", "sample 2"

# custom cases
assert run("""1 1
5
4
""") == "1", "single element"

assert run("""5 1
1 2 3 4 5
5
""") == "0", "all submerged"

assert run("""5 1
1 2 3 4 5
0
""") == "1", "all active"

assert run("""6 1
5 1 5 1 5 1
3
""") == "3", "alternating heights"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal structure |
| all submerged | 0 | strict threshold behavior |
| all active | 1 | full connectivity merging |
| alternating heights | 3 | multiple island formation |

## Edge Cases

A key edge case is when multiple adjacent segments activate in the same query window and immediately merge. Consider input `a = [3, 2, 1]` with a query threshold `0`. All segments activate sequentially, but island count must end at 1, not 3. The algorithm handles this by incrementing islands on activation and then immediately merging with neighbors, decrementing for each successful union, ensuring the final merged structure is correct.

Another case is when no segment is activated for a query. If the sea level is already above all heights, the pointer does not move and the answer remains the previous state, which correctly reflects that no new land appears.

A third subtle case is equal heights with threshold exactly matching them. Because activation uses strict comparison `>`, segments with height equal to the sea level remain submerged, preventing premature island formation and keeping the count consistent with the definition of flooding.
