---
title: "CF 104640C - \u041f\u0440\u044b\u0436\u043a\u0438 \u043c\u0435\u0436\u0434\u0443 \u0432\u0441\u0435\u043b\u0435\u043d\u043d\u044b\u043c\u0438"
description: "We are given a graph where vertices represent universes and edges represent portals. Each portal has a minimum energy requirement, meaning you can only traverse that portal if your current energy level is at least a given threshold. Energy starts at zero."
date: "2026-06-29T16:49:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104640
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104640
solve_time_s: 89
verified: true
draft: false
---

[CF 104640C - \u041f\u0440\u044b\u0436\u043a\u0438 \u043c\u0435\u0436\u0434\u0443 \u0432\u0441\u0435\u043b\u0435\u043d\u043d\u044b\u043c\u0438](https://codeforces.com/problemset/problem/104640/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph where vertices represent universes and edges represent portals. Each portal has a minimum energy requirement, meaning you can only traverse that portal if your current energy level is at least a given threshold. Energy starts at zero.

Whenever you enter a universe for the first time, your energy permanently increases by a value assigned to that universe. You start from a fixed universe, and from there you may travel along any sequence of usable portals, gradually increasing your energy as you discover new universes.

The task is to determine the maximum total energy you can accumulate by the end of this process, which is equivalent to the total sum of values of all universes that become reachable under these constraints.

The constraint sizes immediately rule out any solution that repeatedly simulates all possible paths. With up to one hundred thousand universes and two hundred thousand portals, any approach that explores states of the form “current node plus visited set” is infeasible. Even a shortest path style algorithm over expanded states would explode combinatorially because energy depends on the order in which nodes are visited.

A subtle difficulty comes from circular dependency. A portal might be unusable early because its requirement is too high, but once we collect enough energy from other universes, it becomes usable and may unlock more universes. This means reachability is not static.

A common pitfall is to treat this as a standard reachability problem and simply ignore weights, or to run Dijkstra over nodes with edge weights. That fails because the constraint is not additive along edges, it is a global evolving threshold.

Another failure case appears when a node that provides large energy is only accessible through a high threshold edge. A naive greedy traversal that never revisits blocked edges will miss such nodes even though they are crucial for unlocking the rest of the graph.

## Approaches

The brute-force idea is to simulate all possible ways of visiting universes. Starting from the initial universe, at each step we try every currently reachable portal, move through it if allowed, and recursively continue. Each state would need to remember which universes have been visited and the current energy. The branching factor grows quickly because each new universe both changes energy and changes future reachability. In the worst case this leads to exponential exploration over subsets of nodes.

The key observation is that the only thing that matters for unlocking edges is the current total energy, which is exactly the sum of values of already visited nodes. Once a node becomes reachable, visiting it only increases energy, which can only unlock more edges. There is no mechanism that decreases flexibility.

This monotonic structure suggests a growing reachable set process. If we knew the final set of reachable nodes, their total sum would determine the final energy, and that same energy determines which edges should have been usable. This circular dependency can be resolved by repeatedly expanding what is reachable using the current energy estimate.

We can maintain the set of edges whose requirement is already satisfied, and merge their endpoints into connected components. Once a component containing the start node becomes large enough, its total node value increases energy, potentially unlocking more edges, which may merge more components into the start component. This creates a natural fixed point process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Exhaustive state simulation | Exponential | Exponential | Too slow |
| Threshold propagation with DSU + iterative activation | O((n + m) log m) or O((n + m) α(n)) | O(n + m) | Accepted |

## Algorithm Walkthrough

We maintain a disjoint set union structure over universes, and we gradually activate portals as the energy increases. Each activation may merge components, and only the component containing the start universe contributes to future energy growth.

1. Initialize a disjoint set union over all universes. Each universe starts as its own component, and each component stores the sum of its node values. The starting universe is immediately considered visited, so the initial energy equals its value.
2. Sort all portals by their required energy in increasing order. This allows us to activate them progressively once the energy becomes large enough.
3. Keep a pointer over the sorted portals. Repeatedly activate all portals whose requirement is at most the current energy. Activation means performing union operations in the DSU.
4. After activating all currently usable portals, find the component containing the starting universe. Compute its total sum, which represents the best energy achievable with the currently unlocked structure.
5. If this new energy is larger than the previous value, update the energy and repeat the process, since higher energy may unlock additional portals that were previously blocked.
6. Stop when a full pass over the portal list does not activate any new portal or does not increase the reachable component size.

The key idea is that every time energy increases, we expand the set of usable edges, and every such expansion can only increase connectivity of the start component, never reduce it.

### Why it works

At any moment, the DSU built from all activated edges represents exactly the connectivity under the constraint that all used portals have requirement at most the current energy. The component of the start node in this structure represents all universes that are truly reachable under that energy level. Since energy is defined as the sum of values of visited universes, recomputing it from this component is consistent with the process of visiting each universe once when it becomes reachable. Because both energy and the set of activated edges only grow over time, the process must converge to a fixed point where no new edge can be activated and no new node can join the start component. That fixed point is the maximal achievable energy.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n, val):
        self.parent = list(range(n))
        self.size = [1] * n
        self.sum = val[:]  # component sums

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.sum[a] += self.sum[b]
        return True

def solve():
    n, m, s = map(int, input().split())
    s -= 1

    a = list(map(int, input().split()))

    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1))

    edges.sort()

    dsu = DSU(n, a)

    energy = a[s]
    prev_energy = -1

    i = 0
    while energy != prev_energy:
        prev_energy = energy

        while i < m and edges[i][0] <= energy:
            _, u, v = edges[i]
            dsu.union(u, v)
            i += 1

        root = dsu.find(s)
        energy = dsu.sum[root]

    print(energy)

if __name__ == "__main__":
    solve()
```

The DSU stores both connectivity and the sum of values inside each component, which avoids recomputing sums after every merge. The pointer `i` ensures each edge is processed only once, since once its threshold is satisfied it remains active forever.

The outer loop is essential because activating edges can enlarge the start component, which increases energy, which may unlock more edges.

## Worked Examples

### Sample 1

Input:

```
5 4 1
1 1 1 1 1
1 2 2
1 3 1
1 4 3
1 5 5
```

We start with energy 1 from universe 1.

| Step | Energy | Activated edges (w ≤ energy) | Start component | New energy |
| --- | --- | --- | --- | --- |
| 1 | 1 | (1-3) | {1, 3} | 2 |
| 2 | 2 | (1-2) | {1, 2, 3} | 3 |
| 3 | 3 | (1-4) | {1, 2, 3, 4} | 4 |
| 4 | 4 | none new | unchanged | 4 |

When energy reaches 4, the edge to 5 still requires 5, so it is never activated. The process stabilizes at 4.

This demonstrates how energy growth and edge activation alternate until no new threshold is satisfied.

### Sample 2

Input:

```
4 3 1
3 2 1 10
1 2 3
2 3 5
1 3 4
```

Start energy is 3.

| Step | Energy | Activated edges (w ≤ energy) | Start component | New energy |
| --- | --- | --- | --- | --- |
| 1 | 3 | (1-2) | {1, 2} | 5 |
| 2 | 5 | (1-3), (2-3) | {1, 2, 3} | 6 |
| 3 | 6 | none new | unchanged | 6 |

The node with value 10 is unreachable because no path ever satisfies its required activation condition before it becomes isolated behind higher thresholds.

This shows how intermediate connectivity matters more than raw node values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) α(n)) | Each edge is processed once, each union/find is near constant amortized |
| Space | O(n + m) | DSU arrays plus edge storage |

The algorithm fits comfortably within limits because every portal is activated at most once, and each activation only triggers nearly constant DSU operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve() if solve() is not None else "").strip()

# provided samples
assert run("""5 4 1
1 1 1 1 1
1 2 2
1 3 1
1 4 3
1 5 5
""") == "4"

assert run("""4 3 1
3 2 1 10
1 2 3
2 3 5
1 3 4
""") == "6"

# minimal case
assert run("""1 0 1
7
""") == "7"

# disconnected graph
assert run("""3 0 1
5 6 7
""") == "5"

# chain unlocking
assert run("""4 3 1
1 1 1 1
1 2 0
2 3 0
3 4 0
""") == "4"

# high threshold blocking
assert run("""3 2 1
10 1 1
1 2 100
2 3 100
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node | 7 | single-node initialization |
| no edges | 5 | disconnected handling |
| zero-weight chain | 4 | full propagation |
| high thresholds | 10 | blocked expansion |

## Edge Cases

A key edge case is when all edges have thresholds larger than the initial energy. In that situation, the algorithm correctly performs no unions beyond the start node, and the answer remains the value of the starting universe alone.

Another edge case occurs when a single low-threshold edge connects to a large chain of higher-value nodes. The algorithm only unlocks the chain after energy increases sufficiently, and the iterative loop ensures that once the first connection is made, subsequent expansions are naturally triggered without revisiting earlier logic manually.

A final subtle case is when components merge indirectly through edges that become active much later. DSU handles this cleanly because once an edge is activated, its effect is permanent, and later increases in energy do not require reprocessing old edges or reversing decisions.
