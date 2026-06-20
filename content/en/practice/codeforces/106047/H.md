---
title: "CF 106047H - Not Another Path Query Problem"
description: "We are given an undirected graph where each edge carries a 60-bit weight. A path between two vertices is evaluated not by summing or minimizing weights, but by taking the bitwise AND of all edge weights along that path."
date: "2026-06-20T21:39:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106047
codeforces_index: "H"
codeforces_contest_name: "The 1st Universal Cup. Stage 21: Shandong"
rating: 0
weight: 106047
solve_time_s: 56
verified: true
draft: false
---

[CF 106047H - Not Another Path Query Problem](https://codeforces.com/problemset/problem/106047/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph where each edge carries a 60-bit weight. A path between two vertices is evaluated not by summing or minimizing weights, but by taking the bitwise AND of all edge weights along that path. This means every bit in the path value survives only if every edge on the path has that bit set.

For each query pair of vertices, we must decide whether there exists any path between them whose bitwise AND value is at least a given threshold value $V$. “At least” is important here because we compare the final AND result as an integer, not bit by bit in isolation.

The key structural constraint is that $n$ and $q$ can both reach $10^5$, and the number of edges can reach $5 \times 10^5$. Any approach that tries to explore paths per query, or even run a shortest-path-like search per query, will be far too slow. Even a single BFS per query leads to $O(q(m+n))$, which is completely infeasible. The solution must preprocess the graph so that each query is answered in almost constant time.

A subtle failure case appears when edges exist between two vertices but no valid path exists under the AND constraint. For example, if $V = 6$ and we have edges $1-2$ with weight 7 and $2-3$ with weight 1, then even though $1$ is connected to $3$ in the underlying graph, the path $1 \to 2 \to 3$ has AND value $7 \& 1 = 1$, which is below $V$, so the correct answer is “No”.

Another edge case is when $V = 0$. In this case every path trivially satisfies the condition because any AND result is always at least 0. So the answer reduces to standard connectivity in the full graph.

## Approaches

The brute-force idea is to process each query independently. For a query $(u, v)$, we try to find any path from $u$ to $v$ and compute the bitwise AND of the edges along that path. A naive DFS or BFS that tracks the current AND value would branch over all possible paths. In the worst case, the number of simple paths in a graph is exponential, and even restricting to BFS states, we would need to track pairs of the form $(node, current\_and)$, which leads to an explosion in state space. This quickly becomes impossible given $q = 10^5$.

The key insight comes from understanding how bitwise AND behaves along a path. Once a bit becomes 0 in any edge, it can never come back in later edges. This means that for the final AND to be at least $V$, every bit that is set in $V$ must survive every single edge in the path. If even one edge along the path is missing a required bit, that bit is permanently lost.

This turns the problem from a path optimization problem into a simple filtering problem on edges. We only care about edges that are compatible with $V$, meaning edges whose weight contains all bits set in $V$. Once we discard all incompatible edges, any path in the remaining graph automatically has AND value at least $V$, because every edge preserves all required bits.

So each query reduces to a pure connectivity check in a filtered graph. This can be handled efficiently using a disjoint set union structure built once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential per query | O(n + m) | Too slow |
| Optimal (DSU filtering) | O(m α(n) + q) | O(n) | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Read all edges and determine whether each edge is usable by checking if $(w_i \& V) = V$.

This condition ensures every required bit in $V$ is present in the edge weight.
2. Initialize a disjoint set union structure where each vertex starts in its own component.
3. For every edge that satisfies the condition, merge its endpoints in the DSU.

This builds connected components using only valid edges.
4. For each query $(u, v)$, check whether $u$ and $v$ belong to the same DSU component.

If yes, output “Yes”, otherwise output “No”.

### Why it works

Consider any path formed entirely from edges satisfying $(w \& V) = V$. For every bit set in $V$, every edge along the path has that bit set, so the bit survives the entire AND operation. Therefore the path value always contains all bits of $V$, implying it is at least $V$.

Conversely, if a path uses even one edge that violates the condition, then at least one required bit is removed permanently, making it impossible for the AND result to reach $V$. So every valid path must lie entirely inside the filtered graph, and connectivity in that graph exactly characterizes the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

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

def main():
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

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The DSU structure is used purely to compress connectivity information after filtering edges. Path compression ensures near-constant amortized time per operation, which is necessary given up to $10^5$ queries.

The critical implementation detail is the edge filter condition `(w & V) == V`. This is stricter than checking `w >= V`, which would be incorrect because numeric ordering does not preserve bit inclusion. Only bitwise inclusion guarantees stability under AND.

## Worked Examples

### Example 1

Input:

```
4 3 2 4
1 2 5
2 3 7
1 3 6
1 3
1 4
```

We process edges with respect to $V = 4$ (binary `100`).

| Edge | Weight (bin) | Valid | DSU action |
| --- | --- | --- | --- |
| 1-2 | 101 | Yes | union(1,2) |
| 2-3 | 111 | Yes | union(2,3) |
| 1-3 | 110 | Yes | union(1,3) |

After processing, all nodes {1,2,3} are connected.

Queries:

| Query | Same component | Answer |
| --- | --- | --- |
| 1-3 | Yes | Yes |
| 1-4 | No | No |

This shows that once edges satisfy the bit constraint, the problem collapses to connectivity.

### Example 2

Input:

```
3 2 1 6
1 2 7
2 3 1
1 3
```

Here $V = 6$ (`110`).

| Edge | Weight | Valid | Reason |
| --- | --- | --- | --- |
| 1-2 | 7 | Yes | contains 110 |
| 2-3 | 1 | No | missing required bits |

DSU components become {1,2} and {3}. Query 1-3 is between different components, so answer is No.

This demonstrates that even though a graph path exists, it is invalid under the AND constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \alpha(n) + q \alpha(n))$ | Each edge is processed once for filtering and union, each query is a DSU find |
| Space | $O(n)$ | DSU parent and size arrays |

The solution fits easily within limits because both $m$ and $q$ are $5 \times 10^5$, and DSU operations are effectively constant time in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    try:
        main()
    except Exception:
        pass
    return sys.stdout.getvalue().strip()

# sample-like small case
assert run("""4 3 2 4
1 2 5
2 3 7
1 3 6
1 3
1 4
""") == "Yes\nNo"

# disconnected graph
assert run("""3 2 1 6
1 2 7
2 3 1
1 3
""") == "No"

# V = 0, all edges valid, connectivity works
assert run("""3 2 2 0
1 2 1
2 3 2
1 3
1 2
""") == "Yes\nYes"

# single edge only
assert run("""2 1 1 5
1 2 7
1 2
""") == "Yes"

# no edges
assert run("""3 0 2 0
1 2
2 3
""") == "No\nNo"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small filtered graph | Yes/No | correctness of DSU filtering |
| broken path | No | invalid intermediate edge blocks path |
| V = 0 case | Yes/Yes | all edges accepted |
| single edge | Yes | minimal connectivity |
| empty graph | No/No | no connectivity at all |

## Edge Cases

When $V = 0$, the condition $(w \& V) = V$ is always true for every edge because both sides are zero. The DSU therefore merges according to the full graph, and every query reduces to standard connectivity, which correctly matches the fact that any AND result is always at least zero.

When the graph is connected in the original sense but no valid edges exist under the filter, every node becomes isolated. For an input like $V = 63$ and all edges having random low bits, DSU never merges any vertices, so even queries between directly connected nodes in the original graph return “No”, matching the requirement that every edge in a valid path must satisfy the bit constraint.

When multiple edges connect the same pair of nodes, they are processed independently. If at least one satisfies the condition, the DSU merges them, but duplicate merges do not affect correctness due to idempotence of union operations.
