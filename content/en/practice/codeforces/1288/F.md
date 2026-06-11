---
title: "CF 1288F - Red-Blue Graph"
description: "We have a bipartite graph. Every edge may stay unused, may be painted red for cost r, or may be painted blue for cost b. Some vertices are marked red, some blue, and some uncolored. A red vertex requires strictly more incident red edges than incident blue edges."
date: "2026-06-11T19:04:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "flows"]
categories: ["algorithms"]
codeforces_contest: 1288
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 80 (Rated for Div. 2)"
rating: 2900
weight: 1288
solve_time_s: 202
verified: false
draft: false
---

[CF 1288F - Red-Blue Graph](https://codeforces.com/problemset/problem/1288/F)

**Rating:** 2900  
**Tags:** constructive algorithms, flows  
**Solve time:** 3m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We have a bipartite graph. Every edge may stay unused, may be painted red for cost `r`, or may be painted blue for cost `b`.

Some vertices are marked red, some blue, and some uncolored.

A red vertex requires strictly more incident red edges than incident blue edges. A blue vertex requires strictly more incident blue edges than incident red edges. Uncolored vertices do not care.

The task is to assign a color to each edge, possibly leaving it uncolored, so that every colored vertex satisfies its inequality and the total painting cost is minimum.

The graph is bipartite, with at most 200 vertices on each side and at most 200 edges. These bounds are very small for flow algorithms. A network with roughly 400 vertices and a few thousand edges is completely manageable within the time limit. On the other hand, every edge has three possible states, so brute forcing edge colors would require `3^m` possibilities, which is hopeless when `m = 200`.

The most dangerous part of the problem is that the constraints are expressed as inequalities on counts of incident red and blue edges. A direct formulation in terms of edge colors looks awkward. The key observation is that these inequalities can be converted into flow-balance constraints.

Consider a red vertex of degree 1.

```
R -- e
```

The only way to satisfy it is to make `e` red. Leaving it uncolored gives `0 > 0`, which is false. Painting it blue gives `0 > 1`, also false.

A solution that merely checks whether red edges are at least as many as blue edges would incorrectly accept the uncolored edge.

Another subtle case is a colored vertex with no incident edges.

```
R
```

The condition requires red count > blue count, that is `0 > 0`, which is impossible. The answer must be `-1`.

Multiple edges also matter.

```
Left 1 --- Right 1
Left 1 --- Right 1
```

The two parallel edges are distinct decisions. Any solution that compresses them into a single edge loses information and may output the wrong coloring.

## Approaches

A brute-force solution would assign one of three states to every edge: uncolored, red, or blue. After choosing all states, we could count incident red and blue edges at every vertex and check the inequalities.

The idea is completely correct, but the search space contains `3^m` colorings. With `m = 200`, this number is astronomically large.

The first useful observation is that the actual colors are less important than the difference between red and blue counts.

Take an edge connecting left vertex `u` and right vertex `v`.

Suppose we interpret:

- red edge as directing one unit from `u` to `v`
- blue edge as directing one unit from `v` to `u`
- uncolored edge as sending nothing

Then for every left-side vertex:

```
outflow - inflow
=
(# red incident edges) - (# blue incident edges)
```

For every right-side vertex the sign is reversed:

```
inflow - outflow
=
(# red incident edges) - (# blue incident edges)
```

Now rewrite the vertex requirements.

For a left red vertex:

```
red > blue
```

becomes

```
outflow > inflow
```

For a left blue vertex:

```
inflow > outflow
```

The conditions for right-side vertices are symmetric.

This converts the problem into finding a flow where certain vertices must have strictly positive excess and others strictly negative excess.

The second observation is that every edge can carry at most one unit in one direction. Choosing the direction determines whether the edge becomes red or blue. Choosing no flow means the edge remains uncolored.

At this point the problem becomes a feasible circulation with lower bounds.

Every graph edge contributes one directed edge in each direction:

```
u -> v   capacity 1   cost r
v -> u   capacity 1   cost b
```

Using the first direction means painting that edge red. Using the second means painting it blue. Using neither means leaving it uncolored.

The vertex inequalities are encoded through circulation constraints. After introducing a super source and super sink, they become lower-bound requirements on certain balancing edges.

The resulting task is a minimum-cost feasible circulation with lower bounds. Since all limits are at most 200, a standard lower-bound reduction followed by min-cost flow is easily fast enough. This is exactly the intended solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^m) | O(m) | Too slow |
| Lower-Bound Min-Cost Flow | O(VE·flow) in SPFA-based implementation | O(V+E) | Accepted |

## Algorithm Walkthrough

### Flow Interpretation

Let the left part contain vertices `1..n1` and the right part contain vertices `n1+1..n1+n2`.

For every original edge `(u,v)`:

- add `u -> v` with capacity `1`, cost `r`
- add `v -> u` with capacity `1`, cost `b`

Sending one unit through `u -> v` means the edge is red.

Sending one unit through `v -> u` means the edge is blue.

Sending nothing means the edge is uncolored.

### Encoding Vertex Constraints

For every left vertex:

- red vertex requires `outflow > inflow`
- blue vertex requires `inflow > outflow`
- uncolored vertex imposes no restriction

For every right vertex the sign is reversed.

Introduce special nodes `S` and `T`.

A left red vertex must export at least one extra unit. This is modeled by a lower-bound edge:

```
S -> vertex
lower = 1
upper = INF
```

A left blue vertex must import at least one extra unit:

```
vertex -> T
lower = 1
upper = INF
```

For right-side vertices the directions swap.

Uncolored vertices receive unrestricted balancing edges.

The standard lower-bound construction converts these requirements into node demands.

### Feasible Circulation

1. Build all edge-direction choices.
2. Add balancing edges for every vertex according to its color.
3. Add edge `T -> S` with infinite capacity.
4. Convert all lower bounds into node demands.
5. Create super source `SS` and super sink `TT`.
6. For every positive demand add `SS -> x`.
7. For every negative demand add `x -> TT`.
8. Run min-cost flow from `SS` to `TT`.
9. If not all demand can be satisfied, no valid coloring exists.
10. Otherwise reconstruct the chosen direction of every original edge.

### Why it works

Each unit of flow corresponds to choosing exactly one color for one original edge. If neither direction carries flow, the edge stays uncolored.

The circulation equations guarantee that every vertex receives exactly the imbalance required by its color. A red vertex is forced to have strictly more incident red edges than blue edges, while a blue vertex is forced to have the opposite inequality.

The lower-bound reduction is equivalent to the original circulation problem. A feasible flow in the transformed network exists if and only if a coloring satisfying all vertex constraints exists.

The cost of a flow equals the total painting cost because every unit sent through a red-direction edge contributes `r`, and every unit sent through a blue-direction edge contributes `b`.

Among all feasible colorings, min-cost flow returns the minimum-cost one.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10 ** 9

class Edge:
    __slots__ = ("to", "rev", "cap", "cost")

    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost

class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap, cost):
        fwd = Edge(to, len(self.g[to]), cap, cost)
        rev = Edge(fr, len(self.g[fr]), 0, -cost)
        self.g[fr].append(fwd)
        self.g[to].append(rev)
        return len(self.g[fr]) - 1

    def min_cost_flow(self, s, t):
        flow = 0
        cost = 0

        while True:
            dist = [INF] * self.n
            inq = [False] * self.n
            pv = [-1] * self.n
            pe = [-1] * self.n

            dist[s] = 0
            q = deque([s])
            inq[s] = True

            while q:
                v = q.popleft()
                inq[v] = False

                for i, e in enumerate(self.g[v]):
                    if e.cap > 0 and dist[e.to] > dist[v] + e.cost:
                        dist[e.to] = dist[v] + e.cost
                        pv[e.to] = v
                        pe[e.to] = i

                        if not inq[e.to]:
                            inq[e.to] = True
                            q.append(e.to)

            if dist[t] == INF:
                break

            add = INF
            cur = t

            while cur != s:
                e = self.g[pv[cur]][pe[cur]]
                add = min(add, e.cap)
                cur = pv[cur]

            cur = t

            while cur != s:
                e = self.g[pv[cur]][pe[cur]]
                e.cap -= add
                self.g[cur][e.rev].cap += add
                cur = pv[cur]

            flow += add
            cost += add * dist[t]

        return flow, cost

def solve():
    n1, n2, m, r, b = map(int, input().split())
    s1 = input().strip()
    s2 = input().strip()

    N = n1 + n2 + 4
    S = n1 + n2
    T = S + 1
    SS = T + 1
    TT = T + 2

    mcf = MinCostFlow(N)

    demand = [0] * N

    def add_lr(u, v, low, up, cost):
        if low > up:
            raise ValueError

        mcf.add_edge(u, v, up - low, cost)
        demand[u] -= low
        demand[v] += low

    deg = [0] * (n1 + n2)

    edge_refs = []

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v = n1 + (v - 1)

        deg[u] += 1
        deg[v] += 1

        idx_red = mcf.add_edge(u, v, 1, r)
        idx_blue = mcf.add_edge(v, u, 1, b)

        edge_refs.append((u, idx_red, v, idx_blue))

    for i in range(n1):
        c = s1[i]

        if c == 'R':
            add_lr(S, i, 1, INF, 0)
        elif c == 'B':
            add_lr(i, T, 1, INF, 0)
        else:
            add_lr(S, i, 0, INF, 0)
            add_lr(i, T, 0, INF, 0)

    for j in range(n2):
        v = n1 + j
        c = s2[j]

        if c == 'R':
            add_lr(v, T, 1, INF, 0)
        elif c == 'B':
            add_lr(S, v, 1, INF, 0)
        else:
            add_lr(S, v, 0, INF, 0)
            add_lr(v, T, 0, INF, 0)

    add_lr(T, S, 0, INF, 0)

    need = 0

    for i in range(N):
        if demand[i] > 0:
            mcf.add_edge(SS, i, demand[i], 0)
            need += demand[i]
        elif demand[i] < 0:
            mcf.add_edge(i, TT, -demand[i], 0)

    flow, cost = mcf.min_cost_flow(SS, TT)

    if flow != need:
        print(-1)
        return

    ans = []

    for u, idx_red, v, idx_blue in edge_refs:
        red_edge = mcf.g[u][idx_red]
        blue_edge = mcf.g[v][idx_blue]

        if mcf.g[v][red_edge.rev].cap == 1:
            ans.append('R')
        elif mcf.g[u][blue_edge.rev].cap == 1:
            ans.append('B')
        else:
            ans.append('U')

    print(cost)
    print("".join(ans))

solve()
```

The implementation follows the lower-bound reduction literally.

The helper `add_lr` inserts an edge with lower and upper bounds. The lower bound is removed from the capacity and recorded in the demand array. After all such edges are processed, the demand array tells us how much extra flow every node must receive or send.

The super source and super sink enforce those demands. If the resulting min-cost flow cannot saturate all demand edges, the original circulation was infeasible and the answer is `-1`.

Reconstruction is done by checking whether one of the two direction edges of an original graph edge carried one unit of flow. Exactly one direction corresponds to red, the other to blue, and neither corresponds to uncolored.

A common mistake is forgetting that parallel edges are distinct. The code stores a separate pair of flow edges for every original edge and reconstructs them individually.

## Worked Examples

### Sample 1

Input:

```
3 2 6 10 15
RRB
UB
3 2
2 2
1 2
1 1
2 1
1 1
```

One optimal solution is:

```
BUURRU
```

| Edge | Chosen Color |
| --- | --- |
| (3,2) | B |
| (2,2) | U |
| (1,2) | U |
| (1,1) | R |
| (2,1) | R |
| (1,1) | U |

Cost:

| Red edges | Blue edges | Total |
| --- | --- | --- |
| 2 × 10 | 1 × 15 | 35 |

The flow chooses exactly the edges needed to create the required excesses at the colored vertices while avoiding unnecessary painting costs.

### Custom Example

```
1 1 1 5 7
R
U
1 1
```

The only valid coloring paints the edge red.

| Step | Red Count at Vertex 1 | Blue Count at Vertex 1 |
| --- | --- | --- |
| Uncolored | 0 | 0 |
| Red | 1 | 0 |
| Blue | 0 | 1 |

Only the second row satisfies `red > blue`.

Output:

```
5
R
```

This example demonstrates how the strict inequality is enforced by the lower bound.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(VE·F) | Successive shortest augmenting path with SPFA |
| Space | O(V + E) | Flow graph storage |

Here `V` is roughly 400 and `E` is only a few thousand. With capacities bounded by small values and the official constraints capped at 200, the flow network easily fits inside the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old
    return out.getvalue().strip()

# sample 1
res = run("""3 2 6 10 15
RRB
UB
3 2
2 2
1 2
1 1
2 1
1 1
""")
assert res.splitlines()[0] == "35"

# minimum feasible
assert run("""1 1 1 5 7
R
U
1 1
""").splitlines()[0] == "5"

# impossible, colored isolated vertex
assert run("""1 1 0 5 7
R
U
""") == "-1"

# all uncolored
out = run("""1 1 1 5 7
U
U
1 1
""")
assert out.splitlines()[0] == "0"

# parallel edges
out = run("""1 1 2 1 1
R
U
1 1
1 1
""")
assert out.splitlines()[0] == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single red vertex with one edge | Cost 5 | Strict inequality |
| Colored isolated vertex | -1 | Infeasibility detection |
| All vertices uncolored | Cost 0 | Leaving everything uncolored |
| Parallel edges | Cost 1 | Correct handling of multiple edges |

## Edge Cases

### Colored Vertex With Degree Zero

Input:

```
1 1 0 5 5
R
U
```

The red vertex requires:

```
red > blue
```

which becomes:

```
0 > 0
```

There is no way to satisfy it.

During the lower-bound construction, the vertex receives a mandatory imbalance, but no graph edge can generate that imbalance. The feasible circulation check fails and the algorithm outputs `-1`.

### Strict Inequality Versus Non-Strict

Input:

```
1 1 1
R
U
```

Leaving the edge uncolored gives equal counts:

```
red = 0
blue = 0
```

Equal is not enough.

The lower-bound edge forces at least one unit of excess for the red vertex, so the circulation cannot choose the uncolored state. The only feasible solution paints the edge red.

### Multiple Parallel Edges

Input:

```
1 1 2
R
U
1 1
1 1
```

The two edges are independent choices.

The optimal solution paints exactly one edge red and leaves the other uncolored.

A solution that merged the two edges into one would lose the ability to distinguish those possibilities. The flow network keeps separate direction edges for every original edge, so reconstruction remains correct.
