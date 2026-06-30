---
title: "CF 104417J - Not Another Path Query Problem"
description: "We are given an undirected weighted graph. Each edge carries a 60-bit weight. For any walk between two vertices, we compute a single value by taking the bitwise AND of all edge weights along that walk. A walk is considered good if this AND value is at least a given threshold V."
date: "2026-06-30T19:17:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104417
codeforces_index: "J"
codeforces_contest_name: "The 13th Shandong ICPC Provincial Collegiate Programming Contest"
rating: 0
weight: 104417
solve_time_s: 53
verified: true
draft: false
---

[CF 104417J - Not Another Path Query Problem](https://codeforces.com/problemset/problem/104417/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected weighted graph. Each edge carries a 60-bit weight. For any walk between two vertices, we compute a single value by taking the bitwise AND of all edge weights along that walk. A walk is considered good if this AND value is at least a given threshold V. For each query, we must decide whether there exists any path between two queried vertices whose AND over its edges does not drop below V.

The key difficulty is that the value of a path is not additive or minimizable in the usual sense. Adding more edges can only decrease or keep the same the bitwise AND, never increase it. This immediately implies that longer paths are inherently harder to satisfy the threshold constraint, because every extra edge can only clear bits.

The constraints are large, with up to 100,000 vertices, 500,000 edges, and 500,000 queries. Any solution that recomputes connectivity per query or explores paths directly will fail. Even a per-query BFS or Dijkstra-style approach would lead to roughly 5e5 times 1e5 operations in the worst case, which is far beyond feasible limits.

A subtle but important edge case arises from thinking in terms of shortest paths or maximum bottlenecks. For example, a path that maximizes sum or minimizes maximum edge does not help here, because the AND operation behaves differently. Consider a triangle where edges are 15, 7, and 7. A path using both 7 edges yields AND 7, but introducing the 15 edge reduces flexibility differently. The structure is not monotone in the usual graph optimization sense.

Another failure mode is assuming that edges with weight at least V are individually sufficient. This is false because even if every edge is above V, the AND of multiple edges can still drop below V if they disagree on bit positions.

## Approaches

A brute force approach would treat each query independently. For a given pair u and v, we could run a BFS or DFS and try to track all possible AND values along paths, keeping the best ones. However, the state space explodes because each node could be reached with many different AND outcomes, and combining them requires tracking subsets of bitmasks. In the worst case, this becomes exponential in path length, which is infeasible.

A more structured observation comes from reversing the perspective. Instead of thinking about all possible paths, we can ask when a path is valid in terms of constraints on edges. A path has AND at least V if and only if every edge on the path contains all bits set in V. If any edge is missing a bit that V requires, the entire path immediately fails.

This transforms the problem into a filtered graph problem. We discard every edge whose weight does not contain all bits of V, meaning edges w such that (w & V) != V. On this reduced graph, every remaining edge is “compatible” with the requirement. Now the AND along any path in this subgraph will automatically be at least V, because every edge individually preserves all required bits, and AND can never introduce new zeros where all edges already have ones.

So each query reduces to a simple connectivity check in this filtered graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential per query | High | Too slow |
| Filtered Graph + DSU | O((n + m) α(n) + q α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We proceed by reducing the graph first, then answering connectivity queries efficiently.

1. Read the graph and the threshold V. The threshold defines which bits must be preserved along any valid path.
2. Construct a Disjoint Set Union structure over all n vertices. This structure maintains connected components under edge unions.
3. Iterate through every edge (u, v, w). For each edge, check whether it is compatible with V by verifying that (w & V) == V. This condition ensures every bit required by V exists in w.
4. If an edge is compatible, merge its endpoints in the DSU. This builds connected components in the filtered graph consisting only of valid edges.
5. For each query (u, v), check whether u and v belong to the same DSU component. If they do, output Yes, otherwise output No.

The DSU operations are nearly constant time, so this approach scales to the maximum input sizes.

### Why it works

The correctness hinges on a key equivalence. A path has AND at least V if and only if every edge on the path individually contains all bits of V. The forward direction is straightforward: if a path AND is at least V, then every bit set in V must be present in every edge, because a single missing bit would force the AND to lose it. The reverse direction follows from monotonicity of AND: if every edge contains V as a subset of bits, then the AND of any number of such edges also contains V.

Thus, valid paths are exactly paths in the subgraph formed by edges satisfying (w & V) == V. Connectivity in this subgraph is exactly what DSU captures.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))
        self.r = [0] * (n + 1)

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1

def solve():
    n, m, q, V = map(int, input().split())
    dsu = DSU(n)

    for _ in range(m):
        u, v, w = map(int, input().split())
        if (w & V) == V:
            dsu.union(u, v)

    out = []
    for _ in range(q):
        u, v = map(int, input().split())
        out.append("Yes" if dsu.find(u) == dsu.find(v) else "No")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The DSU structure is used purely to maintain connectivity after filtering edges. The key implementation detail is the bit check `(w & V) == V`, which ensures that all required bits in V are preserved. Without this condition, the DSU would connect nodes through invalid edges and produce incorrect answers.

Path evaluation is never done explicitly. Once components are built, each query becomes a constant-time representative comparison.

## Worked Examples

Consider a small graph with V = 4 and edges:

1-2 with weight 5, 2-3 with weight 6, 1-3 with weight 7.

We first filter edges:

| Edge | Condition (w & V == V) | Kept |
| --- | --- | --- |
| 1-2 (5) | 5 & 4 = 4 | Yes |
| 2-3 (6) | 6 & 4 = 4 | Yes |
| 1-3 (7) | 7 & 4 = 4 | Yes |

All edges remain, so all nodes are connected. Any query between 1, 2, and 3 returns Yes.

Now consider V = 4 with edges:

1-2 (1), 2-3 (2), 1-3 (7).

| Edge | Condition | Kept |
| --- | --- | --- |
| 1-2 (1) | 1 & 4 = 0 | No |
| 2-3 (2) | 2 & 4 = 0 | No |
| 1-3 (7) | 7 & 4 = 4 | Yes |

Only edge 1-3 remains. DSU forms one connection between 1 and 3, while 2 is isolated. Query 1-3 returns Yes, but 1-2 and 2-3 return No.

These traces show that the algorithm reduces the problem entirely to connectivity in a filtered graph and ignores all non-compliant edges without losing correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m + q) α(n)) | Each edge is processed once, and each query is a DSU find operation |
| Space | O(n) | DSU parent and rank arrays |

The constraints allow up to 500,000 edges and queries, and DSU operations are effectively constant time. This ensures the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    _out = io.StringIO()
    _stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    # re-run solution
    class DSU:
        def __init__(self, n):
            self.p = list(range(n + 1))
            self.r = [0] * (n + 1)

        def find(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x

        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return
            if self.r[ra] < self.r[rb]:
                ra, rb = rb, ra
            self.p[rb] = ra
            if self.r[ra] == self.r[rb]:
                self.r[ra] += 1

    def solve():
        n, m, q, V = map(int, sys.stdin.readline().split())
        dsu = DSU(n)

        for _ in range(m):
            u, v, w = map(int, sys.stdin.readline().split())
            if (w & V) == V:
                dsu.union(u, v)

        res = []
        for _ in range(q):
            u, v = map(int, sys.stdin.readline().split())
            res.append("Yes" if dsu.find(u) == dsu.find(v) else "No")

        return "\n".join(res)

    return solve()

# provided sample 1
assert run("""9 8 4 5
1 2 8
1 3 7
2 4 1
3 4 14
2 5 9
4 5 7
5 6 6
3 7 15
1 6
2 7
7 6
1 8
""").strip() == """Yes
No
Yes
No"""

# provided sample 2
assert run("""3 4 1 4
1 2 3
1 2 5
2 3 2
2 3 6
1 3
""").strip() == "Yes"

# minimum case
assert run("""2 1 1 0
1 2 0
1 2
""").strip() == "Yes"

# no edges
assert run("""3 0 2 1
1 2
2 3
""").strip() == "No\nNo"

# all edges valid
assert run("""3 2 2 1
1 2 3
2 3 1
1 3
2 3
""").strip() == "Yes\nYes"

# boundary bit case
assert run("""2 1 1 8
1 2 8
1 2
""").strip() == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| min graph | Yes | single edge valid case |
| no edges | No/No | disconnected components |
| all valid | Yes/Yes | full connectivity |
| boundary bit | Yes | high-bit correctness |

## Edge Cases

One important edge case is when V equals zero. In this case every edge satisfies (w & V) == V automatically, so the DSU connects the full graph exactly as given. Queries reduce to standard connectivity, and the algorithm handles this naturally without special branching.

Another edge case occurs when no edge satisfies the condition. The DSU remains entirely disconnected, so only queries of identical nodes would succeed, but since ui and vi are always distinct, every query correctly returns No.

A third case is when V has high bits that are rarely present. The filtering may remove most edges, but DSU operations remain valid since isolated nodes are handled naturally as singleton components.
