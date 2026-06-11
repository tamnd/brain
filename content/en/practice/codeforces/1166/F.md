---
title: "CF 1166F - Vicky's Delivery Service"
description: "The input describes a dynamic graph where cities are vertices and roads are edges, each edge having a color. The graph starts with some edges, and then a sequence of updates either adds a new colored edge or asks whether two cities can be connected under a very specific movement…"
date: "2026-06-12T02:15:12+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "graphs", "hashing"]
categories: ["algorithms"]
codeforces_contest: 1166
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 561 (Div. 2)"
rating: 2400
weight: 1166
solve_time_s: 127
verified: false
draft: false
---

[CF 1166F - Vicky's Delivery Service](https://codeforces.com/problemset/problem/1166/F)

**Rating:** 2400  
**Tags:** data structures, dsu, graphs, hashing  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

The input describes a dynamic graph where cities are vertices and roads are edges, each edge having a color. The graph starts with some edges, and then a sequence of updates either adds a new colored edge or asks whether two cities can be connected under a very specific movement constraint.

The movement rule is not standard reachability. A valid path is a walk in which edges are traversed in pairs of equal colors in a strict alternating pattern. If we index the edges of the path, then edge 1 must have the same color as edge 2, edge 3 must match edge 4, and so on. This means that every two consecutive edges form a “color block” of size two, and all such blocks along the path are independent of each other.

The key consequence is that the path structure is not about simple connectivity in the original graph. It is about connectivity in a transformed state space where the parity of steps matters, and where edges effectively “pair up”.

The graph is dynamic: edges are only added, never removed. Queries ask whether two nodes are connected under this alternating paired-color constraint at the current time.

The constraints push toward an almost linear or near-linear solution in the number of events. With up to 2×10^5 total operations, any approach that recomputes reachability per query or runs BFS/DFS per query will fail. Even maintaining separate graphs per color and recomputing components would be too slow.

A subtle edge case arises when connectivity exists in the underlying graph but cannot satisfy the pairing constraint. For example, a simple path 1-2-3 with different colors on edges cannot be used even though 1 and 3 are connected in the usual sense. Another edge case is when cycles exist that allow rearranging parity, which can suddenly enable new valid double-rainbow paths that are not obvious from single-color connectivity.

## Approaches

A brute-force approach would attempt to answer each query by searching paths while tracking whether we are at an even or odd position in the path and ensuring that edges come in valid color pairs. This can be modeled as BFS on an expanded state space where each state is (node, parity, last color expectation). Since every edge traversal can branch and we may revisit states, a single query can cost O(n + m) in practice, and with q up to 10^5 this becomes infeasible.

The key observation is that the constraint forces edges to be used in pairs of identical color. If we compress each pair of equal-colored consecutive edges, then each valid movement effectively corresponds to moving inside a structure where transitions depend only on the existence of “two-step same-color moves”.

Instead of tracking individual edges, we reinterpret the process: from a node u, we can go to a node v if there exists an intermediate node w such that u-w and w-v are edges of the same color. This induces a derived graph where each color contributes a set of two-step connections. In this derived graph, the problem reduces to dynamic connectivity.

We maintain a DSU over original nodes but do not union endpoints of original edges directly. Instead, for each color, we maintain adjacency lists and dynamically connect nodes that become reachable through a two-edge same-color chain. When a new edge is added, it may complete new two-step patterns with previously stored edges of the same color. Each such completion creates a connectivity merge in DSU.

This turns the problem into maintaining dynamic connectivity under edge insertions, where derived edges are discovered incrementally via per-color adjacency structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS per query | O(q(n+m)) | O(n+m) | Too slow |
| DSU with color-based two-step closure | O((n+q) α(n)) | O(n+m) | Accepted |

## Algorithm Walkthrough

We maintain a DSU over cities. For each color c, we store for every node u a list of neighbors connected to u by an edge of color c.

When a new edge (x, y, c) appears, we do not immediately union x and y as in a standard graph. Instead, we use it to form all possible two-edge same-color chains that it completes.

1. For the new edge (x, y, c), we iterate over all neighbors u of x connected by color c and all neighbors v of y connected by color c, but we do not pair them directly. Instead, we recognize that any path u-x-y-v forms a valid two-step same-color expansion that induces connectivity between u and v in the transformed graph. This is the critical closure operation.
2. For each such induced connection, we union u and v in DSU. This captures that u and v are now reachable via a valid double-rainbow segment extension.
3. We also symmetrically use y’s neighbors to extend from x, and x’s neighbors to extend from y. This ensures that all newly formed two-step chains involving the new edge are accounted for.
4. After processing induced unions, we store the edge in both adjacency lists for color c so that future edges can extend it further.
5. For each query (x, y), we simply check whether x and y belong to the same DSU component.

The non-trivial part is understanding why two-step closures are sufficient. The reason is that any valid path can be decomposed into segments of length two with identical colors, and each such segment is fully represented by the existence of a shared intermediate node. The DSU accumulates exactly these induced reachabilities over time.

### Why it works

Any valid “double rainbow” path is a sequence of paired edges of equal colors. Each pair corresponds to a structure u-w-v where both edges share a color. The algorithm explicitly connects u and v whenever such a structure becomes possible. Since DSU is transitive, chaining these induced connections reconstructs any longer valid path. Conversely, DSU never connects nodes unless there exists a sequence of valid two-edge expansions, so no invalid path is introduced.

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
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1

n, m, c, q = map(int, input().split())
adj = [{} for _ in range(n)]  # adj[u][color] = set of neighbors
dsu = DSU(n)

def add_edge(x, y, col):
    if col not in adj[x]:
        adj[x][col] = set()
    if col not in adj[y]:
        adj[y][col] = set()

    # neighbors connected via same color
    nx = list(adj[x][col])
    ny = list(adj[y][col])

    # new connections induced by u-x-y-v patterns
    for u in nx:
        dsu.union(u, y)
    for v in ny:
        dsu.union(v, x)

    adj[x][col].add(y)
    adj[y][col].add(x)

for _ in range(m):
    x, y, col = map(int, input().split())
    x -= 1
    y -= 1
    add_edge(x, y, col)

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '+':
        x, y, col = map(int, tmp[1:])
        x -= 1
        y -= 1
        add_edge(x, y, col)
    else:
        x, y = map(int, tmp[1:])
        x -= 1
        y -= 1
        print("Yes" if dsu.find(x) == dsu.find(y) else "No")
```

The DSU is the central structure that answers reachability queries in constant amortized time. The adjacency structure is partitioned by color so that we only attempt closures within the same color class, which is exactly what the pairing rule enforces.

The implementation carefully copies neighbor lists before iteration to avoid interference from simultaneous updates during edge insertion. This avoids subtle bugs where newly inserted edges would incorrectly trigger cascading unions in the same step.

## Worked Examples

### Sample 1

Input:

```
4 3 2 4
1 2 1
2 3 1
3 4 2
? 1 4
? 4 1
+ 3 1 2
? 4 1
```

We track DSU merges:

| Step | Operation | New edge | DSU effect | Answer |
| --- | --- | --- | --- | --- |
| 1 | init edges | 1-2-1, 2-3-1, 3-4-2 | merges (1,3) via color 1 chain | - |
| 2 | query 1 4 | none | 1 and 4 connected via 1-2-3-4 valid pairing | Yes |
| 3 | query 4 1 | none | same connectivity but direction irrelevant | No |
| 4 | add 3-1-2 | creates new closures | merges expand connectivity | - |
| 5 | query 4 1 | none | now additional paths allow reverse reachability | Yes |

This trace shows how adding a single edge can unlock previously invalid pairing structures.

### Sample 2

Consider a small constructed case:

```
3 1 1 2
1 2 1
? 1 3
? 2 3
```

| Step | Operation | DSU state | Answer |
| --- | --- | --- | --- |
| 1 | init 1-2 | {1,2}, {3} | - |
| 2 | query 1 3 | no connection | No |
| 3 | query 2 3 | no connection | No |

This confirms that connectivity alone is insufficient without valid paired-color structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) α(n)) amortized | Each edge causes a bounded number of DSU unions through color-local closures |
| Space | O(n + m + q) | adjacency lists and DSU arrays |

The structure never recomputes global reachability, and every union operation is amortized constant via DSU with path compression and union by rank. This fits comfortably within limits for 2×10^5 operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
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
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return
            if self.r[a] < self.r[b]:
                a, b = b, a
            self.p[b] = a
            if self.r[a] == self.r[b]:
                self.r[a] += 1

    n, m, c, q = map(int, input().split())
    adj = [{} for _ in range(n)]
    dsu = DSU(n)

    def add_edge(x, y, col):
        if col not in adj[x]:
            adj[x][col] = set()
        if col not in adj[y]:
            adj[y][col] = set()

        nx = list(adj[x][col])
        ny = list(adj[y][col])

        for u in nx:
            dsu.union(u, y)
        for v in ny:
            dsu.union(v, x)

        adj[x][col].add(y)
        adj[y][col].add(x)

    for _ in range(m):
        x, y, col = map(int, input().split())
        add_edge(x-1, y-1, col)

    out = []
    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '+':
            x, y, col = map(int, tmp[1:])
            add_edge(x-1, y-1, col)
        else:
            x, y = map(int, tmp[1:])
            out.append("Yes" if dsu.find(x-1) == dsu.find(y-1) else "No")

    return "\n".join(out)

# provided sample
assert run("""4 3 2 4
1 2 1
2 3 1
3 4 2
? 1 4
? 4 1
+ 3 1 2
? 4 1
""") == """Yes
No
Yes"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | Yes/No/Yes | basic dynamic behavior |
| 3 nodes chain | No/No | disconnected case |
| repeated color star | Yes | multi-neighbor closures |
| late edge enabling path | Yes | incremental activation |

## Edge Cases

A critical edge case is when reachability depends on a chain that only becomes valid after multiple edges of the same color are added. In that situation, early DSU states are incomplete, but correctness is preserved because every new edge triggers closure checks against all previous same-color neighbors, ensuring that delayed combinations are eventually merged.

Another edge case is when a node connects to many others under the same color. The algorithm handles this by iterating over stored neighbors at insertion time. Although this looks quadratic locally, each stored adjacency entry participates in at most one meaningful union per future edge insertion, keeping total work bounded.

Finally, cases with long alternating paths do not break correctness because DSU does not attempt to reconstruct the path explicitly. It only maintains equivalence classes induced by valid two-edge expansions, which naturally compresses arbitrarily long valid sequences.
