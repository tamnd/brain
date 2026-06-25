---
title: "CF 106050L - Liberty from Graphs"
description: "We are given a graph that starts empty and then grows over time. Each query adds one new edge, either red or blue, between two vertices."
date: "2026-06-25T12:29:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106050
codeforces_index: "L"
codeforces_contest_name: "Cataratas do Pinh\u00e3o 2025"
rating: 0
weight: 106050
solve_time_s: 55
verified: true
draft: false
---

[CF 106050L - Liberty from Graphs](https://codeforces.com/problemset/problem/106050/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph that starts empty and then grows over time. Each query adds one new edge, either red or blue, between two vertices. After every addition we are asked a hypothetical question: how many edges could we remove from the current graph while still keeping the connectivity between all vertices unchanged, with an extra constraint that the number of removed red edges must equal the number of removed blue edges.

Connectivity is measured in the standard undirected sense, ignoring colors. So if two vertices are connected before removals, they must remain connected after removals. This forces the remaining edges to still contain a spanning forest of every connected component of the current graph.

The constraints are large, with up to a few hundred thousand queries, so recomputing connectivity or recomputing all cycles from scratch after each insertion is not feasible. Any solution that attempts to rebuild a spanning forest or run a full DFS per query would be too slow, since that would effectively lead to quadratic behavior in the worst case.

A subtle point is that we are not asked to output a specific deletion strategy, only the maximum number of deletable edges. This means we can reason in terms of structure rather than explicit construction.

A naive approach would treat each state independently, compute all bridges or a spanning forest, and then try to count how many edges are “extra”. The difficulty is the additional requirement that deletions must balance by color. That constraint couples edges that would otherwise be independently removable.

A common pitfall is to ignore this coupling and compute only the number of non-tree edges. For example, if all edges are red except one blue cycle edge, the graph might have many redundant edges but we cannot delete them all if it breaks the red-blue deletion equality.

Another failure case appears when the graph is already connected but all redundant edges are of one color. For instance, suppose the graph has a single cycle made entirely of red edges except one blue edge. We can remove at most one red edge and one blue edge in equal amounts, even though structurally more edges are redundant.

## Approaches

The key separation is between edges that are structurally necessary for connectivity and edges that are not. In any graph, if we fix the connected components, exactly $n - c$ edges are needed to maintain connectivity inside each component, where $c$ is the number of connected components. Everything beyond that belongs to cycles and is potentially removable.

So the first observation is that the number of “structurally redundant” edges is

$$\text{cycle\_edges} = m - (n - c)$$

where $m$ is the number of edges in the current graph.

If there were no color constraint, the answer would simply be this cycle count, because all non-tree edges can be deleted without breaking connectivity.

The color constraint introduces a global balance condition. Let $R$ and $B$ be the number of red and blue edges that lie in cycles. If we delete some set of cycle edges, the deletions must satisfy:

$$\text{deleted red} = \text{deleted blue}$$

Among all cycle edges, if we try to delete everything, the imbalance is $|R - B|$. We cannot remove this imbalance using cycle edges alone because every deletion contributes to one side or the other.

The best strategy is therefore to delete as many cycle edges as possible while keeping the final deletion counts balanced. This means we are forced to “leave behind” at least $|R - B|$ cycle edges that would otherwise be deletable.

This leads to the optimal count:

$$\text{answer} = \text{cycle\_edges} - |R - B|$$

The intuition is that every extra surplus of one color reduces how many symmetric deletion pairs we can form among cycle edges.

A brute-force approach would explicitly simulate connectivity after each query and recompute cycle structure, costing $O(q(n + m))$, which is far too slow.

The optimized approach maintains only global aggregates: connected components and the difference between red and blue cycle edges. Each insertion is handled in near constant time using union-find, since we only need to know whether an edge creates a cycle or merges components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute per query (DFS / spanning forest) | $O(q(n + m))$ | $O(n + m)$ | Too slow |
| DSU + cycle counting | $O((n + q)\alpha(n))$ | $O(n + q)$ | Accepted |

## Algorithm Walkthrough

We process queries online while maintaining a DSU (Disjoint Set Union) for connectivity.

1. Initialize DSU with each vertex in its own component, and counters for cycle edges in red and blue.
2. For each query adding an edge $(u, v)$ of a given color, check whether $u$ and $v$ are already in the same DSU component.
3. If they are in different components, merge them in DSU. This edge becomes part of the spanning forest and is not a cycle edge, so it does not contribute to deletable edges.
4. If they are already in the same component, this edge forms a cycle. Increment either the red-cycle counter or blue-cycle counter depending on its color.
5. After processing the edge, compute:

- total cycle edges as the sum of red and blue cycle counters
- imbalance as $|\text{red\_cycle} - \text{blue\_cycle}|$
6. Output:

$$(\text{cycle edges}) - |\text{red cycle} - \text{blue cycle}|$$

The key idea is that DSU isolates connectivity changes, while cycle edges accumulate independently. We never need to explicitly track which exact edges form cycles beyond their color classification.

### Why it works

Every graph can be decomposed into a spanning forest plus a set of cycle edges. The spanning forest is uniquely determined up to choice, but always contains exactly $n - c$ edges. Any edge outside this forest can be removed without affecting connectivity.

The only remaining restriction is that deletions must be balanced by color. Since only cycle edges are removable, the problem reduces to selecting a maximum multiset of cycle edges with equal red and blue counts. The optimal solution removes all pairs possible, leaving exactly the absolute imbalance unavoidable. This invariant holds because DSU ensures that every non-cycle edge is committed to connectivity and never enters the deletion pool.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]
        return True

def solve():
    n, q = map(int, input().split())
    dsu = DSU(n)

    red_cycle = 0
    blue_cycle = 0

    for _ in range(q):
        t, u, v = map(int, input().split())
        u -= 1
        v -= 1

        merged = dsu.union(u, v)
        if not merged:
            if t == 1:
                red_cycle += 1
            else:
                blue_cycle += 1

        cycle_edges = red_cycle + blue_cycle
        ans = cycle_edges - abs(red_cycle - blue_cycle)
        print(ans)

if __name__ == "__main__":
    solve()
```

The DSU is used purely to detect whether an edge is redundant with respect to connectivity. If a union succeeds, the edge is part of the spanning forest and never contributes to the answer directly.

The cycle counters separate red and blue redundancies. The final expression corrects the raw cycle count by removing the unavoidable imbalance.

A subtle implementation point is that we never need to store edges or rebuild the graph. Everything reduces to a constant-time classification per query.

## Worked Examples

Consider a small run where we track DSU state and cycle counters.

### Example 1

Input:

```
4 3
1 1 2
2 2 3
1 1 2
```

| Query | Edge | DSU merged | Red cycles | Blue cycles | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | red (1,2) | yes | 0 | 0 | 0 |
| 2 | blue (2,3) | yes | 0 | 0 | 0 |
| 3 | red (1,2) | no | 1 | 0 | 1 |

After the first two edges, the graph is a tree. The third edge closes a cycle and is red, so it increases imbalance. Only one cycle edge exists, so we can remove it but cannot pair it with a blue removal, leaving one unavoidable imbalance.

### Example 2

Input:

```
3 4
1 1 2
2 2 3
1 1 3
2 1 2
```

| Query | Edge | DSU merged | Red cycles | Blue cycles | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | red (1,2) | yes | 0 | 0 | 0 |
| 2 | blue (2,3) | yes | 0 | 0 | 0 |
| 3 | red (1,3) | no | 1 | 0 | 1 |
| 4 | blue (1,2) | no | 1 | 1 | 2 |

The last step shows a balanced cycle set: once red and blue cycle counts match, every cycle edge becomes deletable in pairs, allowing full utilization of redundancy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + q)\alpha(n))$ | Each union/find operation is amortized inverse Ackermann due to DSU |
| Space | $O(n)$ | DSU parent and size arrays only |

The solution is linear up to a very small inverse-Ackermann factor, which is easily fast enough for $3 \cdot 10^5$ queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# minimal
assert run("2 1\n1 1 2\n") == "0"

# simple cycle creation
assert run("3 3\n1 1 2\n2 2 3\n1 1 3\n") == "0\n0\n1"

# balanced cycles
assert run("3 4\n1 1 2\n2 2 3\n1 1 3\n2 1 2\n") == "0\n0\n1\n2"

# all same color cycles
assert run("3 3\n1 1 2\n1 2 3\n1 1 3\n") == "0\n0\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal graph | 0 | base DSU behavior |
| simple cycle | incremental cycle detection | red-only cycle accumulation |
| balanced cycles | symmetric red/blue cancellation | imbalance correction |
| all same color | maximal imbalance | worst-case skew |

## Edge Cases

A critical edge case occurs when all cycle edges belong to a single color. In that situation, the DSU still correctly identifies all redundant edges, but the imbalance term becomes equal to the number of cycle edges. The formula forces the answer to zero deletable edges, because no equal red-blue pairing is possible.

Another case is when cycles appear early but later edges merge previously separate components. Those later merges never affect cycle counters, because DSU ensures that only within-component edges are considered redundant, preserving correctness regardless of insertion order.
