---
title: "CF 106513D - Highway"
description: "We are given a set of cities connected by potential highways, each highway having a fixed construction cost. These roads already form a connected undirected graph, so we know that a spanning tree always exists using some subset of these edges."
date: "2026-06-18T19:05:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106513
codeforces_index: "D"
codeforces_contest_name: "2026 Spring UT CS104c Final Exam"
rating: 0
weight: 106513
solve_time_s: 110
verified: true
draft: false
---

[CF 106513D - Highway](https://codeforces.com/problemset/problem/106513/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of cities connected by potential highways, each highway having a fixed construction cost. These roads already form a connected undirected graph, so we know that a spanning tree always exists using some subset of these edges.

Among all proposed highways, one specific edge is forced: it must appear in the final connected network no matter what. The task is to build a minimum-cost set of roads that still connects all cities while including this mandatory edge.

In graph terms, this is the minimum spanning tree problem with an additional constraint that one edge is pre-selected and must belong to the spanning tree.

The input size makes it clear why this is non-trivial. With up to $10^5$ vertices and $2 \cdot 10^5$ edges, any solution that tries to consider all subsets or recompute spanning trees from scratch per edge modification would be too slow. A naive recomputation of a spanning tree after forcing each possible edge would multiply the cost of Kruskal or Prim by $m$, which is far beyond feasible limits.

A subtle point is that forcing an edge can actually make the optimal solution worse than the global MST, because it may create a cycle where that edge is the most expensive member. A careless implementation that simply builds a normal MST and then “adds” the required edge would be wrong.

As a concrete failure case, imagine three nodes forming a triangle with edges:

```
1 - 2 (cost 1)
2 - 3 (cost 2)
1 - 3 (cost 100)
```

If the mandatory edge is $1-3$, the correct answer must include it, so we cannot pick the natural MST edges. The result becomes 1-3 plus one of the other edges, giving cost 101. A naive MST would give 3, which is invalid because it ignores the constraint.

## Approaches

The brute-force idea would be to treat the mandatory edge as fixed and then recompute a minimum spanning tree over the remaining graph with the endpoints already connected. Conceptually, we “contract” the two endpoints of the required edge and run Kruskal again.

This works because a spanning tree that contains a fixed edge is equivalent to a spanning tree of a graph where that edge is already chosen and its endpoints are merged. However, the direct recomputation still looks expensive if done repeatedly or inefficiently, since Kruskal itself is $O(m \log m)$.

The key observation is that we do not need to rebuild anything from scratch in a special way. We can simply force the edge into the DSU structure before processing all other edges. Once the endpoints of the mandatory edge are united, we proceed with the standard Kruskal ordering over all edges.

This works because Kruskal’s algorithm builds the MST by always taking the smallest edge that connects two different components. By pre-unioning the endpoints of the required edge and adding its cost upfront, we simulate the condition that this edge is already selected, and all later decisions naturally adapt.

The only subtlety is that the mandatory edge must be counted even if it would otherwise be skipped by Kruskal due to forming a cycle. That is exactly what the forced union guarantees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute MST after forcing edge via graph contraction | $O(m \log m)$ per rebuild | $O(m)$ | Too slow if repeated or implemented naively |
| Kruskal with pre-included edge | $O(m \log m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort all edges by increasing cost, keeping the mandatory edge identified separately. Sorting ensures we always consider cheaper connections first, which is the foundation of Kruskal’s correctness.
2. Initialize a DSU structure where each city starts in its own component. This tracks which nodes are already connected during construction.
3. Immediately union the endpoints of the mandatory edge and add its cost to the answer. This step forces the edge into the structure before any other decisions, ensuring it can never be excluded later.
4. Iterate over all edges in sorted order. For each edge, check whether its endpoints belong to different DSU components.
5. If they are in different components, include the edge in the answer and union the components. This preserves connectivity while avoiding cycles, exactly as in standard MST construction.
6. If they are already connected, skip the edge. Adding it would form a cycle and cannot reduce cost in a spanning tree.

### Why it works

Kruskal’s algorithm relies on the property that at any point, the edges chosen form a minimum-cost forest over the processed prefix of edges. By pre-unioning the endpoints of the mandatory edge, we enforce that this edge is part of the initial forest regardless of its weight. From that point onward, every decision is identical to running Kruskal on a graph where those two vertices are already connected, which is equivalent to forcing that edge into the spanning structure. The greedy choice property is preserved because all remaining edges are still processed in global increasing order.

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
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

def main():
    n, m = map(int, input().split())
    j = int(input()) - 1

    edges = []
    forced = None

    for i in range(m):
        u, v, c = map(int, input().split())
        edges.append((c, u, v, i))
        if i == j:
            forced = (c, u, v)

    edges.sort()

    dsu = DSU(n)
    ans = 0

    fc, fu, fv = forced
    ans += fc
    dsu.union(fu, fv)

    for c, u, v, _ in edges:
        if dsu.union(u, v):
            ans += c

    print(ans)

if __name__ == "__main__":
    main()
```

The DSU implementation uses path compression through iterative halving and union by size, which keeps operations effectively constant time. The critical implementation detail is adding the forced edge cost before any processing, not after, since otherwise it might be incorrectly skipped if it forms a cycle in the final structure.

The sorting step ensures Kruskal’s global greedy order is preserved. The union check ensures we never create cycles, which is essential because spanning trees must remain acyclic even when one edge is mandatory.

## Worked Examples

Consider the sample graph:

```
n = 4, m = 5, forced = 3
edges:
1 2 10
2 3 5
3 4 50   (forced)
1 4 20
2 4 15
```

We track DSU state.

| Step | Edge | Action | DSU merges | Cost |
| --- | --- | --- | --- | --- |
| init | forced 3-4 | pre-union | (3,4) | 50 |
| 1 | 2-3 (5) | merge | (2,3,4) | 55 |
| 2 | 1-2 (10) | merge | all connected | 65 |
| 3 | 2-4 (15) | skip | already connected | 65 |
| 4 | 1-4 (20) | skip | already connected | 65 |

The trace shows that after forcing the edge, Kruskal naturally fills the remaining structure with the cheapest possible connections.

Now consider a small cycle where the forced edge is not optimal:

```
1-2 (1), 2-3 (2), 1-3 (100), forced = 1-3
```

| Step | Edge | Action | DSU merges | Cost |
| --- | --- | --- | --- | --- |
| init | 1-3 forced | union | (1,3) | 100 |
| 1 | 1-2 | merge | (1,2,3) | 101 |
| 2 | 2-3 | skip | cycle | 101 |

This confirms that even when the forced edge is very expensive, the algorithm still produces a valid spanning tree containing it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m)$ | Sorting edges dominates; DSU operations are near constant amortized time |
| Space | $O(n + m)$ | Storage for edges and DSU arrays |

The constraints allow up to $2 \cdot 10^5$ edges, and a logarithmic factor is easily manageable within typical limits. Sorting plus DSU is well within the 2-second constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# sample
assert run("""4 5
3
1 2 10
2 3 5
3 4 50
1 4 20
2 4 15
""") == "65"

# minimal graph
assert run("""2 1
1
1 2 10
""") == "10"

# forced edge is expensive cycle
assert run("""3 3
3
1 2 1
2 3 2
1 3 100
""") == "101"

# star graph
assert run("""4 3
2
1 2 5
2 3 1
2 4 1
""") == "7"

# already optimal MST unaffected by forcing a low-cost edge
assert run("""4 5
1
1 2 1
2 3 1
3 4 1
1 3 10
2 4 10
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample case | 65 | correctness on general input |
| 2 nodes | 10 | minimal edge case |
| triangle forced expensive edge | 101 | cycle handling with forced edge |
| star graph | 7 | branching MST structure |
| dense alternative edges | 3 | ignoring expensive cross edges |

## Edge Cases

When the forced edge already belongs to the natural MST, the algorithm still works cleanly because pre-unioning does not change later decisions. For example, in a line graph, forcing a middle edge simply mirrors standard Kruskal behavior.

When the forced edge is the most expensive in a cycle, the DSU will still accept it first, and all cheaper edges will eventually connect the components. This demonstrates that the greedy structure is not violated, only constrained at initialization.

When the graph is already minimally connected with exactly $n-1$ edges, forcing any edge simply adds that cost and the rest of the algorithm performs no unions, which correctly yields the unique spanning tree containing the required edge.
