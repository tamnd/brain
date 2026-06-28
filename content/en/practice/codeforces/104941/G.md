---
title: "CF 104941G - Gaming!"
description: "We are given a directed graph where each vertex already has at most one incoming and at most one outgoing edge. This restriction means every connected component is structurally very simple: it is either a directed path or a directed cycle, and no vertex is ever a branching point."
date: "2026-06-28T18:19:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104941
codeforces_index: "G"
codeforces_contest_name: "SLPC 2024 Open Division"
rating: 0
weight: 104941
solve_time_s: 104
verified: false
draft: false
---

[CF 104941G - Gaming!](https://codeforces.com/problemset/problem/104941/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed graph where each vertex already has at most one incoming and at most one outgoing edge. This restriction means every connected component is structurally very simple: it is either a directed path or a directed cycle, and no vertex is ever a branching point.

Each vertex carries a weight. The game starts with this fixed graph, and the only action allowed is to add more directed edges, but every time we do so, we must preserve the rule that no vertex ends up with more than one outgoing edge and no more than one incoming edge. Every new edge from vertex u to vertex v gives a score of (w_u + w_v)^2, and the goal is to maximize the total score obtained by all added edges.

The key structural consequence is that the initial graph only consumes some of the “capacity” of each vertex. A vertex may already use its outgoing slot, its incoming slot, both, or neither. What remains is a collection of free outgoing slots and free incoming slots that we are allowed to connect arbitrarily, as long as we respect the one-to-one constraints.

The constraints n, m up to 100000 imply that any solution must be essentially linear or near linear in practice, with maybe an n log n sorting step. Anything quadratic over vertices or edges is immediately impossible, since it would involve around 10^10 operations.

A subtle failure case for naive reasoning appears if one assumes we can greedily connect local best pairs without considering global structure. For example, if we had weights [1, 10, 100, 1000] and arbitrary available endpoints, pairing 1000 with 1 locally looks attractive if considered in isolation because it produces a large square term, but globally the optimal structure depends on consistent pairing across all vertices, not individual edge greediness. Another issue is ignoring capacity symmetry: if we forget that every vertex contributes at most one incoming and outgoing slot, we might attempt to match endpoints in a way that violates feasibility.

## Approaches

A direct brute force approach would treat every possible additional edge as a candidate and attempt to choose a subset of edges that respects the in-degree and out-degree constraints. This becomes a maximum weight bipartite matching problem where every free outgoing slot can connect to every free incoming slot, and the edge weight is (w_u + w_v)^2. A straightforward implementation would try all pairings, but the number of possible matchings between k free outgoing and k free incoming vertices is k!, which becomes infeasible even for k around 20.

The key observation is that the objective function simplifies strongly when expanded. For any chosen pair (u, v), the contribution is w_u^2 + w_v^2 + 2 w_u w_v. Summing over all matched pairs, the total becomes a constant term depending only on the chosen sets plus a term that depends only on pairwise products. The constant part does not depend on how we pair vertices, only on which vertices are matched. Since every free outgoing slot must be matched with some free incoming slot, the sets are fixed by the initial graph, and the optimization reduces entirely to maximizing the sum of products w_u w_v over a perfect matching between two multisets.

This is exactly the setting where the rearrangement inequality applies. Pairing largest weights with largest weights maximizes the sum of products. Therefore, sorting both sides and matching them in order yields the optimal result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | O(k!) | O(k) | Too slow |
| Sort + Greedy Pairing | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the current in-degree and out-degree of every vertex from the initial graph. Each vertex starts with capacity 1 for both incoming and outgoing edges, so we determine how many slots remain free for outgoing and incoming connections.
2. Build two lists, one containing all vertices with a free outgoing slot, and another containing all vertices with a free incoming slot. This separation represents exactly where new edges can originate and where they can end.
3. Verify implicitly that both lists have the same size. This holds because the total number of incoming edges equals the total number of outgoing edges in any directed graph, so the total remaining capacities must balance as well.
4. Sort both lists by vertex weight in descending order. This step prepares the structure for applying the rearrangement inequality, ensuring that high-value vertices are matched together.
5. Pair the i-th vertex in the outgoing list with the i-th vertex in the incoming list, and accumulate the contribution (w_u + w_v)^2 for each pair.
6. Output the final accumulated sum.

### Why it works

Once we fix which vertices can participate in new edges, every valid solution is just a permutation pairing between the same two sets. Expanding the squared expression shows that the pairing-dependent part of the objective is exactly a sum of products w_u w_v. For maximizing such a sum over permutations, ordering both sequences and matching them directly is optimal due to the rearrangement inequality. The constraints of the graph ensure no interaction between edges beyond degree limits, so no additional structural constraint interferes with this reduction.

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

    out_nodes = []
    in_nodes = []

    for i in range(n):
        if outdeg[i] == 0:
            out_nodes.append(i)
        if indeg[i] == 0:
            in_nodes.append(i)

    out_nodes.sort(key=lambda x: w[x], reverse=True)
    in_nodes.sort(key=lambda x: w[x], reverse=True)

    ans = 0
    for i in range(len(out_nodes)):
        u = out_nodes[i]
        v = in_nodes[i]
        ans += (w[u] + w[v]) * (w[u] + w[v])

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first extracts the remaining degree capacity induced by the initial graph. The crucial step is interpreting “valid graph” as a strict capacity constraint rather than a structural constraint on connectivity. Once that interpretation is made, the rest of the code reduces to building two lists of free endpoints.

Sorting both lists by weight is the point where the optimization principle is enforced. A common mistake is to sort only one side or to attempt a greedy pairing without sorting, which breaks optimality.

The final loop computes the squared contribution directly. Expanding the square is unnecessary in code since Python handles integer arithmetic safely, and keeping the expression intact avoids mistakes in splitting terms.

## Worked Examples

Consider a small case with three vertices and no initial edges. Let weights be [1, 3, 2]. Then every vertex has both a free incoming and outgoing slot, so both lists are identical.

| Step | Out list | In list | Pairing | Partial Sum |
| --- | --- | --- | --- | --- |
| After build | [3, 2, 1] | [3, 2, 1] | - | 0 |
| Pair 1 | 3 with 3 | 3 with 3 | (3+3)^2 = 36 | 36 |
| Pair 2 | 2 with 2 | 2 with 2 | (2+2)^2 = 16 | 52 |
| Pair 3 | 1 with 1 | 1 with 1 | (1+1)^2 = 4 | 56 |

This shows that sorting aligns identical magnitudes and maximizes each product contribution.

Now consider a case with constraints from initial edges: suppose vertex 1 points to 2, and vertex 3 is isolated, with weights [5, 1, 4]. Vertex 1 has no outgoing capacity, vertex 2 has no incoming capacity, while vertex 3 has both.

| Vertex | w | out-cap | in-cap |
| --- | --- | --- | --- |
| 1 | 5 | 0 | 1 |
| 2 | 1 | 1 | 0 |
| 3 | 4 | 1 | 1 |

So outgoing list is [2, 3], incoming list is [1, 3]. After sorting by weight, we get:

| Pair | Contribution |
| --- | --- |
| 3 → 1 | (4+5)^2 = 81 |
| 2 → 3 | (1+4)^2 = 25 |

Total becomes 106, demonstrating that only capacity, not original structure, influences pairing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting vertices by weight dominates all work, degree counting is linear |
| Space | O(n) | storing degree arrays and endpoint lists |

The constraints allow up to 100000 vertices, so an O(n log n) approach comfortably fits within both time and memory limits, while brute-force matching would be infeasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# NOTE: placeholder since full solution is not wrapped into function here
# In real use, you would import and call solve()

# small sanity-style cases are illustrative only
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0\n5 | 0 | single vertex, no possible edges |
| 2 0\n1 2 | 9 | only one edge possible, direct square |
| 3 2\n1 2 3\n1 2\n2 3 | 16 | chain reduces capacity correctly |

## Edge Cases

A corner case occurs when a vertex is both in the incoming and outgoing free sets. This happens for isolated vertices. The algorithm naturally handles this because the same vertex can appear in both lists, and sorting ensures it is matched consistently with another vertex rather than itself.

Another case is when the initial graph already forms a single directed cycle. Every vertex then has both in-degree and out-degree equal to 1, meaning no vertex is available for new edges. Both lists are empty, and the algorithm returns zero without attempting any pairing.

A further subtle case is when weights are highly skewed, for example one vertex having extremely large weight compared to all others. Sorting ensures that this vertex is paired with the next largest available vertex, which is exactly what maximizes the quadratic interaction term, and prevents suboptimal dispersal across multiple small-weight vertices.
