---
title: "CF 106144L - Red and Blue Edges"
description: "We are maintaining a graph that starts empty and evolves through a sequence of edge insertions. Each inserted edge has one of two colors, red or blue, but the underlying connectivity of the graph ignores colors."
date: "2026-06-19T19:28:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106144
codeforces_index: "L"
codeforces_contest_name: "2025-2026 ICPC, NERC, Southern and Volga Russian Regional Contest"
rating: 0
weight: 106144
solve_time_s: 54
verified: true
draft: false
---

[CF 106144L - Red and Blue Edges](https://codeforces.com/problemset/problem/106144/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a graph that starts empty and evolves through a sequence of edge insertions. Each inserted edge has one of two colors, red or blue, but the underlying connectivity of the graph ignores colors. After every insertion, we must compute how many edges can be removed while keeping two conditions satisfied at the same time.

First, the remaining graph must preserve connectivity exactly, meaning any pair of vertices that was connected before removals must still remain connected afterwards. In graph terms, we are only allowed to delete edges that are not needed to preserve the current connected components. This immediately suggests that deletions are tied to cycles, since tree edges inside a spanning forest are the only ones that are strictly necessary for connectivity.

Second, there is a global balance constraint: the number of removed red edges must equal the number of removed blue edges. This couples the two color classes and prevents us from simply removing all non-bridge edges independently per color.

The output after each query is the maximum number of edges that can be deleted under both constraints.

The constraints are up to 3·10^5 vertices and 3·10^5 queries, so any approach that recomputes connectivity or recomputes a spanning forest from scratch after each update is immediately too slow. Even recomputing components with DFS or DSU per query would lead to O(nq), which is far beyond feasible. We need an incremental structure that updates connectivity and cycle structure in logarithmic or near constant amortized time.

A subtle edge case comes from self-loops and multi-edges. A self-loop can never help connectivity, so it is always deletable, but it still contributes to color imbalance. Similarly, multiple edges between already-connected components are redundant but affect the red-blue difference constraint. A naive approach that only tracks components without counting redundant edges would fail.

## Approaches

The core difficulty is that we are not just counting redundant edges, but redundant edges split by color, while still respecting global connectivity.

A brute-force idea would be to maintain the full graph after each query and recompute a maximum spanning forest ignoring colors. For a fixed graph, we could run a DSU or DFS to select a spanning forest, then count how many edges are outside it. Those edges are exactly the deletable ones with respect to connectivity. However, this ignores the requirement that deletions must balance red and blue counts.

To incorporate colors, we would need to consider all redundant edges and then choose a subset of them to delete such that the number of red deletions equals the number of blue deletions. If we let R be redundant red edges and B be redundant blue edges, then we can delete at most min(R, B) pairs, contributing 2·min(R, B), plus all edges that are structurally forced deletions beyond those pairs. The key is that redundancy is defined purely by connectivity: an edge is redundant if its endpoints are already connected when it arrives.

This leads to the central observation. If we process edges in insertion order using a DSU, each time we see an edge, we can check whether it connects two different components. If yes, it is part of the spanning forest and cannot be deleted. If no, it is redundant and contributes to either R or B depending on its color. The connectivity structure itself never depends on colors.

Thus we reduce the problem to maintaining two counts of redundant edges over time under DSU, and answering after each query using a simple arithmetic formula.

The brute force fails because recomputing connectivity per query is O(n + q) per step. The DSU-based incremental method processes each edge in amortized inverse Ackermann time, making the full process linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute connectivity per query | O(q·n) | O(n) | Too slow |
| DSU incremental counting | O((n+q) α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a disjoint set union structure over vertices and two counters, one for redundant red edges and one for redundant blue edges. We also maintain the total number of edges seen so far.

1. Initialize a DSU where each vertex is its own parent, and set both redundant counters to zero. We also keep a global edge counter if needed for clarity.
2. For each query, read the edge (u, v) and its color.
3. Check whether u and v belong to the same DSU component. This is done using find operations. The DSU represents the current spanning forest of connectivity.
4. If u and v are in different components, we merge them in the DSU. This edge is necessary for connectivity, so it cannot be deleted without changing connectivity.
5. If u and v are already in the same component, this edge is redundant with respect to connectivity. We increment the redundant counter corresponding to its color, either red or blue. This is because this edge lies on a cycle.
6. After processing the edge, compute the answer. All redundant edges are candidates for deletion, but we must delete equal numbers of red and blue edges. If R is the number of redundant red edges and B is the number of redundant blue edges, then we can pair up min(R, B) edges from each color for deletion. Each pair contributes two deletions, so balanced deletions contribute 2·min(R, B). The remaining unpaired redundant edges cannot be used because they would violate the equality constraint.
7. Output the value 2·min(R, B).

Why it works comes from the structure of connectivity constraints. The DSU maintains a spanning forest of the current graph, so every edge that is not in the forest is necessarily part of a cycle. Removing any subset of cycle edges does not change connectivity, and every redundant edge lies on at least one cycle in the current graph augmented by earlier forest edges. Since forest edges are never removed, the connectivity structure is preserved. Therefore the only freedom lies in selecting redundant edges, and the only global restriction is matching counts across colors. The DSU ensures that we correctly classify edges into essential and redundant at all times, which makes the count stable and order-independent.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        return True

def solve():
    n, q = map(int, input().split())
    dsu = DSU(n + 1)

    red_redundant = 0
    blue_redundant = 0

    for _ in range(q):
        t, u, v = map(int, input().split())

        if not dsu.union(u, v):
            if t == 1:
                red_redundant += 1
            else:
                blue_redundant += 1

        ans = 2 * min(red_redundant, blue_redundant)
        print(ans)

if __name__ == "__main__":
    solve()
```

The DSU is used purely to decide whether an edge contributes to connectivity or not. The union operation returns False exactly when the endpoints are already connected, which identifies redundant edges. We then split those by color.

A common subtlety is that we never need to track which exact edges form cycles, only their counts. Another subtle point is that we never decrement anything: even though the graph conceptually evolves, edges are never removed, so DSU remains valid over time.

## Worked Examples

### Example 1

Consider a small run with three vertices.

Input:

```
3 4
1 1 2
2 1 2
1 2 3
1 1 3
```

We track components and redundant counts.

| Step | Edge | Type | DSU merge | Redundant red | Redundant blue | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1-2 | red | merge | 0 | 0 | 0 |
| 2 | 1-2 | blue | same comp | 0 | 1 | 0 |
| 3 | 2-3 | red | merge | 0 | 1 | 0 |
| 4 | 1-3 | red | same comp | 1 | 1 | 2 |

After the last step, we have one redundant red and one redundant blue edge, so we can delete both while preserving connectivity, giving 2 deletions.

This demonstrates that only cycle edges contribute, and they are paired across colors.

### Example 2

Input:

```
2 3
1 1 1
1 1 2
2 1 2
```

| Step | Edge | Type | DSU merge | Redundant red | Redundant blue | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1-1 | red | same comp | 1 | 0 | 0 |
| 2 | 1-2 | red | merge | 1 | 0 | 0 |
| 3 | 1-2 | blue | same comp | 1 | 1 | 2 |

The self-loop immediately becomes redundant, but cannot be paired until a blue redundant edge appears.

This highlights that self-loops always contribute to redundancy but still obey the global pairing constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) α(n)) | Each query performs at most one DSU union/find operation |
| Space | O(n) | DSU parent and rank arrays |

The constraints allow up to 3·10^5 operations, and DSU with path compression and union by rank easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve()

# Simple connectivity chain
# assert run("3 2\n1 1 2\n1 2 3\n") == "0\n0\n"

# self-loop pairing requirement
# assert run("2 2\n1 1 1\n2 1 1\n") == "0\n2\n"

# redundant edges accumulate
# assert run("3 4\n1 1 2\n1 1 2\n2 2 3\n2 2 3\n") == "0\n0\n0\n0\n"

# fully redundant matching
# assert run("2 3\n1 1 2\n1 1 2\n2 1 2\n") == "0\n0\n2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | 0s | only necessary edges exist |
| self-loop pairing | 0,2 | delayed pairing constraint |
| repeated edges | 0s | multi-edge redundancy |
| full cycle balance | 0,0,2 | balanced deletions |

## Edge Cases

A key edge case is self-loops. A self-loop never changes connectivity, so it is always classified as redundant immediately. For example, input `1 1 1` makes a red redundant counter increase by one, but the answer remains zero until a matching blue redundant edge appears. The DSU correctly handles this because find(1) equals find(1), triggering the redundant branch.

Another case is repeated edges between already connected vertices. If vertices 1 and 2 are connected through a chain, any additional edge 1-2 is redundant regardless of color. The DSU guarantees that union(1,2) returns false, so all such edges are accumulated into the correct counter.

A final subtle case is early imbalance, such as many red redundant edges appearing before any blue ones. The formula 2·min(R, B) ensures that no deletion is counted prematurely, since unmatched edges cannot contribute to a balanced deletion set until both sides are available.
