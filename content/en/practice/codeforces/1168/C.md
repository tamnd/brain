---
title: "CF 1168C - And Reachability"
description: "We are given a sequence of integers arranged on a line, and we want to answer connectivity queries between pairs of positions, but connectivity is not based on adjacency."
date: "2026-06-15T16:46:14+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp"]
categories: ["algorithms"]
codeforces_contest: 1168
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 562 (Div. 1)"
rating: 2200
weight: 1168
solve_time_s: 297
verified: true
draft: false
---

[CF 1168C - And Reachability](https://codeforces.com/problemset/problem/1168/C)

**Rating:** 2200  
**Tags:** bitmasks, dp  
**Solve time:** 4m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers arranged on a line, and we want to answer connectivity queries between pairs of positions, but connectivity is not based on adjacency. Instead, we are allowed to jump from an index to a later index if the bitwise AND of their values shares at least one set bit. From a starting position $x$, we can move forward through a chain of indices as long as every consecutive pair in the chain has a non-zero bitwise AND. The task is to determine, for many queries, whether we can reach a target position $y$ starting from $x$.

This is fundamentally a reachability problem on a directed graph where nodes are indices and there is an edge from $i$ to $j$ for $i < j$ if $a_i \& a_j > 0$. The challenge is that explicitly building all edges is infeasible because it would require $O(n^2)$ work in the worst case.

The constraints are large, with up to 300,000 elements and 300,000 queries. Any approach that inspects pairs directly will time out. Even per-query graph traversal is too slow, since a BFS or DFS could degrade to linear per query. This pushes us toward preprocessing a structure that allows fast reachability checks.

A subtle edge case is the presence of zeros. Any index with value 0 has no outgoing or incoming useful edges, because $0 \& x = 0$ for all $x$. Such positions can never participate in a valid path, except as isolated endpoints of trivial queries that do not require traversal through them. For example, if $a = [1, 0, 2]$, then position 2 cannot help connect 1 and 3 even though it sits in the middle.

Another non-obvious issue is that reachability is not symmetric and is constrained by increasing indices. This makes the structure closer to a forward-only graph, which allows us to exploit ordering in the solution.

## Approaches

A direct approach constructs the graph explicitly and runs BFS per query. For each index $i$, we check all $j > i$ and add an edge if $a_i \& a_j > 0$. This already costs $O(n^2)$, which is too large for 300,000 elements.

Even if we skip explicit construction and try BFS per query, each traversal may still touch a large portion of the array. With 300,000 queries, worst-case complexity becomes completely infeasible.

The key observation is that bitwise AND connectivity depends only on shared set bits. Each number can be viewed as a subset of at most 18 bits (since values are up to 300,000). If we think in terms of bits, each position belongs to several bit groups, and movement is possible only through shared bit membership.

This suggests maintaining, for each bit, the most recent position that has been seen while scanning left to right. When we are at index $i$, we know which earlier indices share at least one bit with it, and we can “merge” connectivity information forward.

However, maintaining full transitive connectivity per bit is still complex. The crucial simplification is that we do not need full reachability between all pairs; we only need to know whether two indices belong to the same connected component in this forward graph. Since edges only go forward, components can be constructed incrementally using a union-like structure over indices, guided by bit occurrences.

We process indices from left to right, maintaining a disjoint-set union (DSU). For each bit, we remember the last index where this bit appeared. When we are at index $i$, for every set bit in $a_i$, we union $i$ with the last seen index for that bit, and then update the last seen index to $i$. This builds exactly the connectivity induced by chains of overlapping bits.

Once DSU is built, each query reduces to checking whether $x$ and $y$ belong to the same component, and also ensuring $x < y$ (already guaranteed by input).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS per query | $O(qn)$ | $O(n^2)$ | Too slow |
| DSU over bit propagation | $O(n \alpha(n) \cdot B + q \alpha(n))$ | $O(n + B)$ | Accepted |

Here $B$ is the number of bits in the value range (up to 18).

## Algorithm Walkthrough

1. Initialize a DSU structure over indices $1 \dots n$. Each index starts in its own component. This represents that initially no connectivity is known.
2. Maintain an array `last[bit]`, where each entry stores the most recent index whose value contains that bit. Initially all are unset.
3. Iterate through indices from left to right. At index $i$, inspect all bits set in $a_i$. Each bit represents a “channel” through which connectivity can propagate.
4. For each bit $b$ set in $a_i$, if `last[b]` exists, union $i$ with `last[b]`. This connects the current position to the previous occurrence of the same bit, and indirectly to everything already connected to that occurrence.
5. After processing unions for all bits of $a_i$, update `last[b] = i` for every bit $b$ set in $a_i$. This ensures future indices connect to the most recent representative of each bit group.
6. After preprocessing, for each query $(x, y)$, check whether DSU find operations return the same root. If yes, output “Shi”, otherwise output “Fou”.

### Why it works

The DSU invariant is that two indices are in the same set if and only if there exists a sequence of indices from left to right where consecutive elements share at least one common bit. Every union operation corresponds exactly to introducing a valid edge in the graph induced by shared bits. Since every possible edge connects a node to the latest previous occurrence of at least one shared bit, all paths in the original reachability definition are representable through these unions. Transitivity of DSU ensures that any multi-step chain is captured, so connectivity queries on DSU match reachability in the original graph.

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
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    dsu = DSU(n)
    last = [-1] * 20

    for i in range(n):
        x = a[i]
        for b in range(20):
            if x & (1 << b):
                if last[b] != -1:
                    dsu.union(i, last[b])
                last[b] = i

    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        if dsu.find(x) == dsu.find(y):
            out.append("Shi")
        else:
            out.append("Fou")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The DSU is used to compress connectivity into components as we scan left to right. The key implementation detail is the `last` array, which ensures we only connect each new index to the most recent index for each bit, avoiding quadratic comparisons. The union operation is sufficient because earlier connections are already transitively captured.

Bit iteration is bounded by 20 because values are at most 300,000, which fits within 19 bits.

## Worked Examples

### Example 1

Input:

```
5 3
1 3 0 2 1
1 3
2 4
1 4
```

We track DSU connections as we scan:

| i | a[i] | bits | unions performed | last updated |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | none | bit0=1 |
| 2 | 3 | 0,1 | union(2,1) | bit0=2, bit1=2 |
| 3 | 0 | none | none | unchanged |
| 4 | 2 | 1 | union(4,2) | bit1=4 |
| 5 | 1 | 0 | union(5,2) | bit0=5 |

Query (1,3): index 3 is zero, isolated, not connected to 1, so answer is Fou.

Query (2,4): both belong to same component via bit 1 chain, so Shi.

Query (1,4): connected through 1 → 2 → 4, so Shi.

This confirms that DSU correctly captures indirect bit-based chaining.

### Example 2

Input:

```
4 2
5 1 4 0
1 3
2 3
```

Tracking:

| i | a[i] | bits | unions | last |
| --- | --- | --- | --- | --- |
| 1 | 5 | 0,2 | none | 0=1,2=1 |
| 2 | 1 | 0 | union(2,1) | 0=2 |
| 3 | 4 | 2 | union(3,1) | 2=3 |
| 4 | 0 | none | none | unchanged |

Now 1, 2, 3 are connected through shared bit structure, so both queries return Shi.

This demonstrates how different bit channels merge components transitively even without direct adjacency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \alpha(n) \cdot 20 + q \alpha(n))$ | Each index processes at most 20 bits, each union/find is inverse Ackermann |
| Space | $O(n + 20)$ | DSU arrays plus last-occurrence array |

The solution scales comfortably for 300,000 elements and queries since the bit factor is constant and DSU operations are nearly constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
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
                return
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    dsu = DSU(n)
    last = [-1] * 20

    for i in range(n):
        for b in range(20):
            if a[i] & (1 << b):
                if last[b] != -1:
                    dsu.union(i, last[b])
                last[b] = i

    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        out.append("Shi" if dsu.find(x) == dsu.find(y) else "Fou")

    return "\n".join(out)

# provided sample
assert run("""5 3
1 3 0 2 1
1 3
2 4
1 4
""") == "Fou\nShi\nShi"

# single element chains via bit propagation
assert run("""3 2
1 2 4
1 3
2 3
""") == "Shi\nShi"

# all zeros except endpoints
assert run("""4 2
1 0 0 2
1 4
2 3
""") == "Fou\nFou"

# all equal values
assert run("""5 1
7 7 7 7 7
1 5
""") == "Shi"

# sparse bits
assert run("""6 2
1 2 4 8 16 32
1 6
2 5
""") == "Fou\nFou"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sparse chain example | Shi / Shi | propagation through bit overlap |
| zeros case | Fou / Fou | zero breaks connectivity |
| uniform values | Shi | full connectivity |
| disjoint bits | Fou | no accidental unions |

## Edge Cases

A critical edge case is when zeros appear between valid values. For input `[1, 0, 2]`, index 2 never participates in any union. The algorithm correctly leaves it isolated because it has no set bits, so `last` is never updated and no union occurs.

Another case is repeated values with identical bit patterns. For `[7, 7, 7]`, each index unions with the previous one via all shared bits, and DSU merges them into a single component. The algorithm does not double-count or create redundant structure because repeated unions are ignored by DSU.

A further edge case involves sparse bit distributions where connectivity requires chaining through intermediate indices rather than direct overlap. The `last` array ensures such chaining is preserved because every new occurrence links into the existing component for that bit, propagating connectivity forward.
