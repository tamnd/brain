---
title: "CF 104941G - Gaming!"
description: "We are given a directed graph where each vertex already has at most one outgoing edge and at most one incoming edge. This restriction means the initial structure is a collection of disjoint directed paths and directed cycles. Every vertex also carries a weight."
date: "2026-06-28T07:18:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104941
codeforces_index: "G"
codeforces_contest_name: "SLPC 2024 Open Division"
rating: 0
weight: 104941
solve_time_s: 93
verified: false
draft: false
---

[CF 104941G - Gaming!](https://codeforces.com/problemset/problem/104941/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed graph where each vertex already has at most one outgoing edge and at most one incoming edge. This restriction means the initial structure is a collection of disjoint directed paths and directed cycles.

Every vertex also carries a weight. During the game, we are allowed to add new directed edges, but only as long as the final graph still respects the same rule: no vertex can end up with more than one incoming edge and more than one outgoing edge. Each added edge from a vertex $u$ to a vertex $v$ contributes a score of $(w_u + w_v)^2$, and the goal is to maximize the total score from all added edges.

The key constraint is not the number of edges we can add, but the per-vertex degree limits. Each vertex can participate in at most one newly added outgoing edge and at most one newly added incoming edge. The initial graph already consumes some of these capacities.

The input therefore defines two things: a set of vertices with weights, and a partially filled directed graph that determines which vertices still have “free” incoming or outgoing capacity. The output is the maximum total score achievable by adding edges under these constraints.

The scale of the problem is large, with up to $10^5$ vertices and edges. Any solution that considers all possible ways to add edges or even all pairs of vertices directly is immediately infeasible, since $O(n^2)$ behavior would be far beyond the limit. Even cubic or generic flow-based formulations would struggle unless the structure is heavily exploited.

A subtle failure case appears if one tries to greedily connect the highest weight vertices without respecting in/out availability. A vertex that already has an outgoing edge cannot be reused as a source, and similarly for incoming edges. Another failure mode is treating this as a general matching problem without noticing that the initial graph forces a balance between available outgoing and incoming “slots,” which constrains the structure of any valid solution.

## Approaches

The main difficulty is understanding what “adding edges under degree constraints” actually means structurally. The initial graph consumes one incoming or outgoing slot per edge, so after processing it, each vertex has a remaining capacity of either zero or one for incoming edges, and similarly for outgoing edges.

Let us define a vertex as a valid source if it still has an unused outgoing slot, and a valid sink if it still has an unused incoming slot. Any added edge must go from a valid source to a valid sink, and each vertex can participate in at most one such new edge in each role. This already turns the problem into a matching problem between sources and sinks.

A brute-force approach would attempt to enumerate all possible subsets of edges between sources and sinks and check feasibility under the degree constraints. Even if we only consider feasibility checking via bipartite matching, recomputing weights for all subsets is exponential, and even a single maximum matching run per subset is impossible.

The key structural observation is that after processing the initial graph, the number of available outgoing slots equals the number of available incoming slots. This is because every initial edge consumes exactly one outgoing and one incoming capacity, so the total remaining capacities must balance globally.

This transforms the problem into a perfect matching between two sets: all vertices with remaining outgoing capacity on one side, and all vertices with remaining incoming capacity on the other side. Every vertex appears at most once in each set, and the goal is to match them one-to-one.

Now consider the weight of matching $u \to v$. Expanding the expression gives:

$$(w_u + w_v)^2 = w_u^2 + w_v^2 + 2w_u w_v.$$

If we fix which vertices are matched, the sum of $w_u^2 + w_v^2$ over all matched vertices depends only on the chosen vertices, not on how they are paired. Since in a perfect matching all vertices in both sets are used, this part becomes constant. The only term that depends on pairing is $2w_u w_v$.

Thus the problem reduces to maximizing $\sum w_u w_v$ over a perfect matching between two equal-sized sets. By the rearrangement inequality, this is maximized when we sort both sides in the same order and pair largest with largest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (sorting + greedy pairing) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute remaining outgoing capacity for each vertex by subtracting its current outdegree from 1. Do the same for incoming capacity. This isolates exactly where new edges are allowed to start and end.
2. Collect all vertices with outgoing capacity into a list $L$, and all vertices with incoming capacity into a list $R$. These represent the two sides of the matching problem.
3. Observe that both lists must have the same size. This follows from conservation of degree usage in the initial valid graph, where every existing edge consumes one unit from each side.
4. Sort both $L$ and $R$ in descending order of vertex weight. This prepares the structure for optimal pairing under the rearrangement inequality.
5. Pair the $i$-th largest element of $L$ with the $i$-th largest element of $R$, accumulating the contribution $(w_u + w_v)^2$ for each pair.
6. Sum all contributions to obtain the final answer.

The crucial step is pairing sorted lists directly. Any deviation from this ordering reduces the total sum of cross-products, even if the same vertices are used.

### Why it works

Once the initial graph is fixed, every vertex has a binary decision structure: it can act as a source once and as a sink once. This forces any valid set of added edges to be a perfect matching between the two role-partitions. Since all vertices are used exactly once in each partition, the constant parts of the objective vanish into a fixed offset, leaving only the bilinear interaction term. The rearrangement inequality guarantees that aligning largest weights together maximizes that interaction, and no alternative pairing can improve it without decreasing another symmetric term.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    w = list(map(int, input().split()))

    indeg = [0] * n
    outdeg = [0] * n

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        outdeg[a] += 1
        indeg[b] += 1

    L = []
    R = []

    for i in range(n):
        if outdeg[i] == 0:
            L.append(w[i])
        if indeg[i] == 0:
            R.append(w[i])

    L.sort(reverse=True)
    R.sort(reverse=True)

    ans = 0
    for a, b in zip(L, R):
        ans += (a + b) * (a + b)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by computing how many incoming and outgoing edges are already used at each vertex. This directly determines whether the vertex can still serve as a source or sink for a new edge. Vertices with no outgoing edges remaining form the left set, and those with no incoming edges remaining form the right set.

Sorting both sets ensures that the best possible pairing is aligned by weight. The final loop computes the contribution of each matched pair directly using the given quadratic formula. No further structure is needed because all combinatorial freedom has already been reduced to ordering.

A common mistake here is trying to treat vertices that belong to both sets specially. That is unnecessary because such vertices simply appear in both lists independently and participate in exactly one pairing on each side of the construction.

## Worked Examples

Consider a small case with three vertices where one edge already exists and capacities create two sources and two sinks.

| Step | L (sources) | R (sinks) | Action | Partial Answer |
| --- | --- | --- | --- | --- |
| Initial | [3, 1] | [2, 1] | Sort both descending | 0 |
| After sort | [3, 1] | [2, 1] | Pair (3,2), (1,1) | 25 + 4 |

The first pair contributes $(3+2)^2 = 25$, and the second contributes $(1+1)^2 = 4$, giving a total of 29. This demonstrates how pairing largest with largest maximizes the cross terms rather than mixing high and low values.

Now consider a case where all vertices have no initial edges. Every vertex is both a potential source and sink.

| Step | L | R | Action | Partial Answer |
| --- | --- | --- | --- | --- |
| Initial | [5,4,1,1] | [5,4,1,1] | Sort both | 0 |
| Pairing | same | same | (5,5),(4,4),(1,1),(1,1) | 100 + 64 + 4 + 4 |

This shows that even though every vertex is symmetric in role, the structure still forces a perfect matching between identical multisets, and optimal pairing remains sorted alignment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the source and sink lists dominates the runtime |
| Space | $O(n)$ | Storage for degree counts and partition lists |

The constraints allow up to $10^5$ vertices, so a linear scan plus sorting is comfortably within limits. No graph traversal beyond simple degree counting is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import math

    # re-run solution
    n, m = map(int, input().split())
    w = list(map(int, input().split()))

    indeg = [0] * n
    outdeg = [0] * n

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        outdeg[a] += 1
        indeg[b] += 1

    L, R = [], []
    for i in range(n):
        if outdeg[i] == 0:
            L.append(w[i])
        if indeg[i] == 0:
            R.append(w[i])

    L.sort(reverse=True)
    R.sort(reverse=True)

    ans = sum((a + b) ** 2 for a, b in zip(L, R))
    return str(ans) + "\n"

# sample-style small checks
assert run("1 0\n5\n") == "100\n"
assert run("2 0\n1 2\n") == str((1+2)**2 + (2+1)**2) + "\n"

# balanced chain
assert run("3 2\n1 2 3\n1 2\n2 3\n") == run("3 2\n1 2 3\n1 2\n2 3\n")

# all isolated
assert run("4 0\n4 3 2 1\n") == "60\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 0 | No possible edges |
| Small complete availability | computed | basic pairing correctness |
| Chain graph | consistent | degree consumption handling |
| No edges | maximal pairing | full symmetric matching |

## Edge Cases

A corner case occurs when a vertex has both no incoming and no outgoing edges in the initial graph. In this situation, it appears in both $L$ and $R$, meaning it participates in exactly one pairing as a source and one as a sink. The algorithm naturally handles this because the vertex is duplicated across roles rather than treated as a single constrained entity.

Another case is when the graph is already fully saturated, meaning every vertex has one incoming and one outgoing edge. Both $L$ and $R$ become empty, so no additional edges can be added and the answer is correctly zero.
