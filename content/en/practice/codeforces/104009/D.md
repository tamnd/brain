---
title: "CF 104009D - Bipartite"
description: "We are given a sequence of edges of an undirected graph, presented in a fixed order. We are not allowed to reorder edges, but we can cut this sequence into consecutive blocks. Each block forms its own independent graph using exactly the edges inside it."
date: "2026-07-02T05:24:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104009
codeforces_index: "D"
codeforces_contest_name: "AGM 2022, Final Round, Day 1"
rating: 0
weight: 104009
solve_time_s: 49
verified: true
draft: false
---

[CF 104009D - Bipartite](https://codeforces.com/problemset/problem/104009/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of edges of an undirected graph, presented in a fixed order. We are not allowed to reorder edges, but we can cut this sequence into consecutive blocks. Each block forms its own independent graph using exactly the edges inside it.

For each block, we check whether the graph formed by those edges is bipartite. A valid partition is one where every block is bipartite, and we want to split the original edge list into the smallest possible number of such blocks.

So the task is essentially online segmentation of an edge stream: we scan edges left to right, and whenever the current block stops being bipartite, we cut it and start a new block.

The key constraint is that both the number of nodes and edges can go up to two hundred thousand, so any approach that recomputes bipartiteness from scratch for every possible segment is too slow. A naive O(M²) attempt over all segment endpoints would involve checking bipartiteness repeatedly on large subgraphs, which is far beyond the limit.

A subtle failure case appears when a graph becomes non-bipartite due to an odd cycle that spans multiple edges. For example, edges (1,2), (2,3), (3,1) form a triangle. If a naive approach delays detection and tries to “fix” it later, it may incorrectly merge edges into a single segment even though the bipartiteness condition is already violated at the moment the third edge is added.

## Approaches

A brute-force idea is to maintain the current segment and, after each new edge, rebuild a graph and run a bipartite check using BFS or DFS. This works logically, because bipartiteness is straightforward to verify with a two-coloring. However, if we do this for every edge, the total cost becomes O(M × (N + M)) in the worst case, since each BFS may traverse almost the entire segment and we repeat it M times. With M up to 200000, this is not feasible.

The key observation is that we never need to reconsider past decisions once we cut a segment. Inside a segment, we only need to know whether adding a new edge creates a contradiction in a bipartite coloring. This is exactly what a Disjoint Set Union structure with parity (also known as DSU with bipartite tracking) is designed for.

We maintain a DSU where each node is split conceptually into two states representing its color. Each union operation enforces that endpoints of an edge must have opposite colors. If at any point this condition contradicts previous assignments, the current segment becomes invalid, so we must cut here.

Thus, we greedily extend the current segment as far as possible while it remains bipartite. When a contradiction occurs, we start a new segment and reset the DSU.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute BFS per segment | O(M²) | O(N) | Too slow |
| DSU with parity + greedy segmentation | O(M α(N)) | O(N) | Accepted |

## Algorithm Walkthrough

We process edges from left to right while maintaining a DSU that tracks bipartite constraints inside the current segment.

1. We initialize a fresh DSU for the current segment, where each node is initially in its own set with no parity constraints.
2. For each edge (u, v), we try to merge u and v with opposite parity. This enforces that u and v must belong to different color classes in a bipartite coloring of the current segment.
3. If u and v already belong to the same DSU component with the same parity requirement, then adding this edge creates an odd cycle. At this point, the current segment is no longer bipartite, so we finalize the segment ending at the previous edge.
4. When a segment ends, we record it, clear the DSU state, and start a new segment beginning at the current edge.
5. After processing all edges, we output the number of segments.

The non-trivial part is how parity is stored. Each DSU node keeps a parent pointer and a parity value meaning whether the node’s color differs from its parent’s color. Path compression updates both structure and parity consistently, ensuring we can always compute whether two nodes must be equal or opposite in color.

### Why it works

Inside each segment, we are effectively building a partial bipartite coloring as edges arrive. The DSU invariant is that for every processed edge, the enforced constraints are consistent and no odd cycle exists. If a contradiction appears, it corresponds exactly to discovering an odd cycle in that segment, which is the only reason a graph fails to be bipartite. Since we cut immediately when this happens, every produced segment is guaranteed to remain bipartite, and maximality of each segment follows because we only cut when extension becomes impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.parity = [0] * n  # parity to parent

    def find(self, x):
        if self.parent[x] == x:
            return x
        px = self.parent[x]
        root = self.find(px)
        self.parity[x] ^= self.parity[px]
        self.parent[x] = root
        return root

    def get_parity(self, x):
        self.find(x)
        return self.parity[x]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        pa = self.get_parity(a)
        pb = self.get_parity(b)

        if ra == rb:
            return (pa ^ pb) == 1

        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
            a, b = b, a
            pa, pb = pb, pa

        self.parent[rb] = ra
        self.parity[rb] = pa ^ pb ^ 1

        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1

        return True

def solve():
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]

    dsu = DSU(n + 1)
    res = 1

    for u, v in edges:
        if not dsu.union(u, v):
            res += 1
            dsu = DSU(n + 1)
            dsu.union(u, v)

    print(res)

if __name__ == "__main__":
    solve()
```

The DSU stores parity information relative to parent links. The union function returns whether adding the edge is still valid. If it returns False, it means a contradiction was found and we immediately start a new segment.

A subtle detail is resetting the DSU entirely when we cut. Since segments are independent graphs, no information carries over between them.

## Worked Examples

### Example 1

Input:

```
3 3
1 3
1 2
2 3
```

We process edges sequentially.

| Step | Edge | DSU State Valid? | Segment |
| --- | --- | --- | --- |
| 1 | (1,3) | Yes | [1] |
| 2 | (1,2) | Yes | [1,2] |
| 3 | (2,3) | No | cut before this |

So we get two segments: [1,2] and [3].

This shows how the triangle forces a split exactly when the third edge is processed.

### Example 2

Input:

```
4 4
1 2
2 3
3 4
4 1
```

| Step | Edge | DSU State Valid? | Segment |
| --- | --- | --- | --- |
| 1 | (1,2) | Yes | [1] |
| 2 | (2,3) | Yes | [1,2] |
| 3 | (3,4) | Yes | [1,2,3] |
| 4 | (4,1) | No | cut |

The final edge closes an odd cycle across the current structure, forcing a second segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M α(N)) | Each edge triggers at most a few DSU operations with path compression |
| Space | O(N) | DSU arrays for parent, rank, parity |

The constraints allow up to 200000 edges, and the DSU-based solution processes each edge in near constant amortized time, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0]*n
            self.parity = [0]*n

        def find(self, x):
            if self.parent[x] == x:
                return x
            px = self.parent[x]
            r = self.find(px)
            self.parity[x] ^= self.parity[px]
            self.parent[x] = r
            return r

        def get_parity(self, x):
            self.find(x)
            return self.parity[x]

        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            pa, pb = self.get_parity(a), self.get_parity(b)
            if ra == rb:
                return (pa ^ pb) == 1
            if self.rank[ra] < self.rank[rb]:
                ra, rb = rb, ra
                pa, pb = pb, pa
            self.parent[rb] = ra
            self.parity[rb] = pa ^ pb ^ 1
            if self.rank[ra] == self.rank[rb]:
                self.rank[ra] += 1
            return True

    n, m = map(int, inp.splitlines()[0].split())
    edges = [tuple(map(int, x.split())) for x in inp.splitlines()[1:]]

    dsu = DSU(n+1)
    ans = 1

    for u, v in edges:
        if not dsu.union(u, v):
            ans += 1
            dsu = DSU(n+1)
            dsu.union(u, v)

    return str(ans)

# sample
assert run("3 3\n1 3\n1 2\n2 3\n") == "2"

# all independent edges
assert run("4 3\n1 2\n3 4\n1 3\n") == "1"

# triangle forces split
assert run("3 3\n1 2\n2 3\n3 1\n") == "2"

# chain remains bipartite
assert run("5 4\n1 2\n2 3\n3 4\n4 5\n") == "1"

# repeated cycle pattern
assert run("4 5\n1 2\n2 3\n3 4\n4 1\n1 3\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| triangle | 2 | detects first odd cycle |
| chain | 1 | fully bipartite segment |
| mixed edges | 1 | independent components |
| extra chord | 2 | late violation handling |

## Edge Cases

One important edge case is when the first edge already creates a contradiction in the current DSU state. In that situation, the algorithm immediately starts a new segment containing only that edge, and the reset DSU ensures no stale parity information leaks forward.

Another case is a graph where multiple odd cycles overlap. For example, a dense triangle-like structure can trigger repeated segment cuts. Each cut resets all constraints, so even if previous edges formed complex conflicts, only the current active segment matters.

A final subtle case is a long chain where the last edge closes a cycle. The algorithm correctly delays the failure until the exact edge that completes the contradiction, because DSU parity only detects inconsistency when a same-component opposite-parity requirement is violated.
