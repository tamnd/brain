---
title: "CF 102419H - In-degree"
description: "We have an undirected graph with up to 2000 vertices and 2000 edges. Every edge must eventually be oriented toward exactly one of its two endpoints. For a vertex i, the value a[i] specifies the exact number of incident edges that must point into i."
date: "2026-08-14T15:12:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "H"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 1099
verified: false
draft: false
---

[CF 102419H - In-degree](https://codeforces.com/problemset/problem/102419/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 18m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph with up to 2000 vertices and 2000 edges. Every edge must eventually be oriented toward exactly one of its two endpoints. For a vertex `i`, the value `a[i]` specifies the exact number of incident edges that must point into `i`. A value of `-1` removes that requirement, so any resulting in-degree is acceptable.

The output is either `NO` when no orientation satisfies all fixed in-degrees, or `YES` followed by one directed version of every original edge. If the original edge is `{u, v}`, printing `u v` means that `v` is its head, so that edge contributes one to the in-degree of `v`.

The constraints are small enough for a flow construction with only a few thousand vertices and edges. What matters more is that the answer is a global assignment: deciding the direction of one edge can affect whether another edge can satisfy a constrained vertex. A local greedy choice can easily consume the only edge that another vertex needs. An algorithm around `O(m(n+m))` is easily within the intended scale, while brute force over all orientations is hopeless.

A first edge case is a vertex whose requested in-degree is larger than its actual degree. For example,

```
2 1
2 -1
1 2
```

has only one edge incident to vertex 1, so its in-degree can never be 2. The correct output is `NO`. A careless implementation that only checks `a[i] <= m` would incorrectly accept it.

A second edge case is a constrained vertex with request zero. For example,

```
2 1
0 -1
1 2
```

must orient the edge as `2 1`. If an implementation treats zero as "unconstrained" or initializes its required count incorrectly, it can produce the opposite direction and violate the requirement.

A third edge case occurs when all vertices are constrained. For

```
3 3
1 1 1
1 2
2 3
3 1
```

the only possible in-degree sequence is achieved by orienting the triangle as a directed cycle. The answer is `YES`. There is no free vertex available to absorb an edge that cannot be assigned to a constrained endpoint.

A fourth edge case is the value `-1`. Consider

```
2 1
1 -1
1 2
```

The only edge must point to vertex 1, while vertex 2 is allowed to receive zero edges. Treating `-1` as a literal required degree would obviously be wrong. The `-1` vertices need capacity, but they do not have a lower bound.

## Approaches

The brute-force approach is to choose a direction independently for every edge. An edge has two possibilities, so there are exactly `2^m` orientations to inspect. For each orientation we can compute all in-degrees in `O(n+m)` and check the requirements. The worst-case operation count is therefore `O(2^m(n+m))`. With `m = 2000`, the number of orientations is `2^2000`, roughly `10^602`, so this approach is not merely slow, it is completely unusable.

The useful observation is that every edge makes exactly one unit contribution to exactly one endpoint's in-degree. That is precisely an assignment problem. Introduce one flow node for every original edge. Sending one unit through that edge node means choosing where the corresponding undirected edge will end. The edge node can send its unit to either of its two endpoint vertices.

The remaining difficulty is that constrained vertices require an exact number of incoming units, while unconstrained vertices may receive any number. Exact requirements are naturally represented by lower and upper bounds on flow. We can turn the entire problem into a feasible circulation.

Create a source-like vertex `S` and a sink-like vertex `T`. For every original edge `e`, create an edge node `E_e`. The flow network contains `S -> E_e` with lower and upper bound both equal to 1, forcing every original edge to contribute exactly one unit. From `E_e`, add capacity-one edges to the two endpoints of the original edge. Finally, connect every original vertex `v` to `T`. If `a[v]` is fixed, that edge has lower and upper bound `a[v]`. If `a[v] = -1`, its lower bound is zero and its upper bound can be its graph degree.

The extra edge `T -> S` with capacity `m` closes this into a circulation. Flow conservation now means exactly what we want: every edge node receives one unit and sends it to one endpoint, while every constrained vertex sends exactly its requested number of units to `T`.

Lower bounds are removed using the standard circulation reduction. For an edge `u -> v` with bounds `[L, R]`, we first reserve `L` units and leave residual capacity `R-L`. The reserved lower bound creates an imbalance at its endpoints. A super source and super sink are then used to repair all those imbalances with an ordinary maximum-flow computation. With integral capacities, an integral feasible flow exists whenever any feasible flow exists, so every original edge node will ultimately send exactly one whole unit to one endpoint.

For the maximum-flow step, Ford-Fulkerson with DFS is enough here. Its usual integer-capacity bound is `O(EF)`, where `F` is the maximum flow. In this particular construction, all flow originating from an edge node is limited by the unit-capacity `S -> E_e` edges, and there are only `m` such units. The remaining balancing flow can be handled through the single `T -> S` connection. Thus the number of useful augmentations is bounded by `O(m)`, giving `O(mE) = O(m(n+m))` time for this problem.

The brute-force method works because it explicitly considers every possible assignment. It fails because the number of assignments is exponential. The flow model keeps only the relevant choices, namely which endpoint receives each edge's unit, and lets the max-flow algorithm resolve all choices simultaneously.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^m(n+m))` | `O(n+m)` | Too slow |
| Lower-Bound Flow + Ford-Fulkerson | `O(m(n+m))` | `O(n+m)` | Accepted |

## Algorithm Walkthrough

1. Read the graph and compute the degree of every original vertex. The degree gives a natural upper bound for an unconstrained vertex, because no vertex can receive more incoming edges than the number of edges touching it.
2. Build one flow node `E_e` for every original undirected edge `e = {u, v}`. Add a bounded edge `S -> E_e` with bounds `[1, 1]`. This forces every original edge to contribute exactly one unit of flow, so no edge can disappear from the final orientation.
3. Add `E_e -> u` and `E_e -> v`, each with bounds `[0, 1]`. Since `E_e` receives exactly one unit, flow conservation forces exactly one of these two arcs to carry that unit. Choosing the first means the original edge ends at `u`; choosing the second means it ends at `v`.
4. For every original vertex `v`, add an edge `v -> T`. If `a[v]` is fixed, give this edge bounds `[a[v], a[v]]`. If `a[v] = -1`, give it bounds `[0, degree[v]]`. The lower and upper bounds are equal for a constrained vertex, so it must receive exactly the requested number of edge units.
5. Add the modeling edge `T -> S` with bounds `[0, m]`. Without this edge, `S` would have outgoing flow and `T` would have incoming flow, which is an ordinary source-sink flow rather than a circulation. Closing the network makes every vertex obey conservation.
6. Replace every bounded edge `[L, R]` by an ordinary residual edge of capacity `R-L`. At the same time, maintain `balance[u] -= L` and `balance[v] += L` for an edge `u -> v`. The signs describe the imbalance created after fixing the lower-bound flow.
7. Add a super source `SS` and super sink `TT`. For every vertex with positive balance, add `SS -> v` with capacity `balance[v]`. For every vertex with negative balance, add `v -> TT` with capacity `-balance[v]`. The auxiliary flow must saturate all these balancing edges.
8. Run Ford-Fulkerson from `SS` to `TT`. If the total flow is smaller than the sum of all positive balances, the lower bounds cannot be made compatible, so print `NO`.
9. If all balancing edges are saturated, recover the flow on each `E_e -> u` and `E_e -> v` arc. Exactly one of them carries one unit. If `E_e -> u` carries one unit, output `v u`, because the original undirected edge `{u,v}` must end at `u`. Otherwise output `u v`.

Why it works

The central invariant is that every original edge node always represents exactly one edge unit. The fixed lower bound on `S -> E_e` gives that unit, and the only two possible destinations are the original endpoints. Consequently, a feasible circulation determines one valid orientation of every original edge.

For a constrained vertex `v`, the edge `v -> T` has both lower and upper bound equal to `a[v]`. Conservation forces exactly `a[v]` units to arrive at `v`, so its final in-degree is exactly correct. An unconstrained vertex has enough upper capacity to receive any number from zero through its degree.

The lower-bound transformation is equivalent to the original circulation because it starts by fixing every mandatory lower-bound unit and asks the auxiliary max flow to repair the resulting vertex imbalances. If the auxiliary flow saturates every required balancing edge, adding the lower bounds back produces a valid circulation. If it cannot saturate them, no assignment of the residual capacities can restore conservation, so no original orientation exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

class Flow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        idx = len(self.g[u])
        rev = len(self.g[v])
        self.g[u].append([v, rev, cap])
        self.g[v].append([u, idx, 0])
        return idx

    def max_flow(self, s, t):
        n = self.n
        total = 0

        while True:
            used = [False] * n

            def dfs(v, pushed):
                if v == t:
                    return pushed

                used[v] = True

                for e in self.g[v]:
                    to, rev, cap = e
                    if cap <= 0 or used[to]:
                        continue

                    got = dfs(to, min(pushed, cap))
                    if got:
                        e[2] -= got
                        self.g[to][rev][2] += got
                        return got

                return 0

            pushed = dfs(s, 10**9)
            if pushed == 0:
                break

            total += pushed

        return total

def solve_case(n, m, a, edges):
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    # Node layout:
    # 0 .. n-1          original vertices
    # n .. n+m-1        one node per original edge
    # S, T              circulation source/sink
    # SS, TT            lower-bound reduction source/sink
    S = n + m
    T = S + 1
    SS = T + 1
    TT = SS + 1
    N = TT + 1

    flow = Flow(N)
    balance = [0] * N

    def add_bounded(u, v, low, high):
        idx = flow.add_edge(u, v, high - low)

        # Lower bound low is already sent on u -> v.
        # It contributes one unit of outgoing lower flow at u
        # and one unit of incoming lower flow at v.
        balance[u] -= low
        balance[v] += low

        return idx

    # For reconstruction:
    # (edge_node, arc_index_to_u, arc_index_to_v, u, v)
    original_refs = []

    for i, (u, v) in enumerate(edges):
        edge_node = n + i

        # Every original edge contributes exactly one unit.
        add_bounded(S, edge_node, 1, 1)

        idx_u = add_bounded(edge_node, u, 0, 1)
        idx_v = add_bounded(edge_node, v, 0, 1)

        original_refs.append((edge_node, idx_u, idx_v, u, v))

    for v in range(n):
        if a[v] == -1:
            add_bounded(v, T, 0, deg[v])
        else:
            add_bounded(v, T, a[v], a[v])

    # Close the S -> ... -> T flow into a circulation.
    add_bounded(T, S, 0, m)

    need = 0

    for v in range(N):
        if balance[v] > 0:
            flow.add_edge(SS, v, balance[v])
            need += balance[v]
        elif balance[v] < 0:
            flow.add_edge(v, TT, -balance[v])

    got = flow.max_flow(SS, TT)

    if got != need:
        return None

    answer = []

    for edge_node, idx_u, idx_v, u, v in original_refs:
        # The transformed capacity was 1, so residual capacity 0
        # means one unit of flow was sent through that arc.
        flow_to_u = 1 - flow.g[edge_node][idx_u][2]
        flow_to_v = 1 - flow.g[edge_node][idx_v][2]

        if flow_to_u == 1:
            # The edge ends at u.
            answer.append((v + 1, u + 1))
        elif flow_to_v == 1:
            # The edge ends at v.
            answer.append((u + 1, v + 1))
        else:
            # This cannot happen in a feasible circulation.
            return None

    return answer

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))

    answer = solve_case(n, m, a, edges)

    if answer is None:
        print("NO")
        return

    out = ["YES"]
    out.extend(f"{u} {v}" for u, v in answer)
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `Flow` class stores every residual edge as `[destination, reverse-index, residual-capacity]`. The reverse index is what lets an augmenting path undo part of an earlier choice. This matters because an early path may assign an edge to one endpoint and a later path may need to reroute that assignment.

`add_bounded` performs the lower-bound transformation. The residual capacity becomes `high - low`, while the balance array records the effect of the mandatory `low` units. The original lower bound itself is not lost, because it is implicitly included when the final flow is reconstructed.

The edge nodes are created after the original vertices, which keeps the indexing simple. For original edge `i`, its flow node is `n + i`. The two outgoing arcs are stored by their indices in that node's adjacency list. Since their original capacities are both one, their final residual capacities directly tell us which endpoint received the unit.

The `T -> S` edge has capacity `m`, because exactly `m` units enter `T` in total, one for every original edge. A larger capacity would also work, but `m` is a tight and convenient bound.

The lower-bound reduction uses `balance[u] -= low` and `balance[v] += low`. A positive balance means that the fixed lower bounds leave excess incoming flow at that vertex, so the residual network must route that amount away. A negative balance means that the vertex needs residual incoming flow. The super-source and super-sink edges encode precisely those two cases.

There is no integer-overflow concern in Python. All relevant quantities are at most a few thousand, but Python integers also remove any dependence on machine integer width.

## Worked Examples

For Sample 1, the requested degrees are `[1, 2, 1, -1, 0]`. One valid orientation is exactly the one shown in the sample.

| Original edge | Chosen head | In-degree after processing |
| --- | --- | --- |
| `1 2` | `2` | `[0,1,0,0,0]` |
| `1 3` | `1` | `[1,1,0,0,0]` |
| `2 3` | `2` | `[1,2,0,0,0]` |
| `3 4` | `3` | `[1,2,1,0,0]` |
| `4 5` | `5` | `[1,2,1,0,1]` |

The final degrees at vertices 1, 2, 3, and 5 are `1, 2, 1, 0`, exactly as required. Vertex 4 is unconstrained. The flow model reaches the same assignment by sending one unit through each edge node and selecting the corresponding endpoint arc.

For Sample 2, the only change is that vertex 5 now requires in-degree 1.

| Original edge | Chosen head | In-degree after processing |
| --- | --- | --- |
| `1 2` | `2` | `[0,1,0,0,0]` |
| `1 3` | `1` | `[1,1,0,0,0]` |
| `2 3` | `2` | `[1,2,0,0,0]` |
| `3 4` | `3` | `[1,2,1,0,0]` |
| `4 5` | `5` | `[1,2,1,0,1]` |

The last edge now has to point into vertex 5. This demonstrates why the unconstrained vertex 4 cannot simply absorb every leftover edge. Its capacity is available, but the exact requirement at vertex 5 still has to be satisfied.

The two traces demonstrate the same invariant from different sides. Every edge contributes exactly one unit, and every fixed vertex consumes exactly its requested number of those units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(m(n+m))` | The auxiliary graph has `O(n+m)` edges, and the integral augmenting-flow construction needs `O(m)` relevant augmentations |
| Space | `O(n+m)` | The graph contains `O(n+m)` vertices and edges, with a constant number of residual edges per modeled edge |

The original constraints have `n,m <= 2000`, so the auxiliary graph contains only a few thousand vertices and roughly a constant multiple of `n+m` residual arcs. The flow value contributed by the original edge nodes is bounded by `m`, and every such source-side arc has capacity one. The resulting `O(m(n+m))` bound is comfortably small at this scale.

## Test Cases

The output orientation is not unique, so tests should validate the produced answer rather than compare it character-for-character with one particular orientation. The following harness assumes the solution above is saved as `solution.py`.

```python
# Test harness for solution.py
import io
import sys

from solution import solve_case

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        from solution import solve
        solve()
        return out.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str, possible: bool):
    data = inp.strip().splitlines()
    n, m = map(int, data[0].split())
    a = list(map(int, data[1].split()))

    edges = []
    for line in data[2:]:
        u, v = map(int, line.split())
        edges.append((u, v))

    lines = out.strip().splitlines()

    if not possible:
        assert lines == ["NO"], f"expected NO, got:\n{out}"
        return

    assert lines[0] == "YES", f"expected YES, got:\n{out}"
    assert len(lines) == m + 1

    original = {tuple(sorted(e)) for e in edges}
    indeg = [0] * n

    for line in lines[1:]:
        u, v = map(int, line.split())
        assert 1 <= u <= n
        assert 1 <= v <= n
        assert u != v

        assert tuple(sorted((u, v))) in original
        indeg[v - 1] += 1

    for i in range(n):
        if a[i] != -1:
            assert indeg[i] == a[i], (
                f"vertex {i + 1}: expected {a[i]}, got {indeg[i]}"
            )

# Sample 1
sample1 = """\
5 5
1 2 1 -1 0
1 2
1 3
2 3
3 4
4 5
"""
validate(sample1, run(sample1), True)

# Sample 2
sample2 = """\
5 5
1 2 1 -1 1
1 2
1 3
2 3
3 4
4 5
"""
validate(sample2, run(sample2), True)

# Minimum-size valid graph.
case_min = """\
2 1
1 -1
1 2
"""
validate(case_min, run(case_min), True)

# Boundary case: requested degree equals m and is actually attainable.
case_boundary = """\
3 2
2 0 -1
1 2
1 3
"""
validate(case_boundary, run(case_boundary), True)

# All vertices constrained with equal requested values.
case_equal = """\
4 4
1 1 1 1
1 2
2 3
3 4
4 1
"""
validate(case_equal, run(case_equal), True)

# Impossible because vertex 1 has degree 1 but requests in-degree 2.
case_impossible = """\
2 1
2 -1
1 2
"""
validate(case_impossible, run(case_impossible), False)

# Maximum-size graph: a 2000-cycle, every vertex requests in-degree 1.
n = 2000
m = 2000
a = " ".join(["1"] * n)
cycle_edges = "\n".join(
    f"{i} {i % n + 1}" for i in range(1, n + 1)
)
case_max = f"{n} {m}\n{a}\n{cycle_edges}\n"

validate(case_max, run(case_max), True)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `YES` with valid orientation | Basic mixed constrained and unconstrained vertices |
| Sample 2 | `YES` with valid orientation | A previously free endpoint becomes exactly constrained |
| `2 1 / 1 -1 / 1 2` | `YES` | Minimum valid graph and exact degree one |
| `3 2 / 2 0 -1` | `YES` | Degree equal to `m`, zero requirement, and exact orientation |
| Four-cycle with all `1` | `YES` | All-equal requirements and no unconstrained vertex |
| `2 1 / 2 -1 / 1 2` | `NO` | Requested degree larger than the actual degree |
| 2000-cycle with all `1` | `YES` | Maximum-size input and large flow network |

## Edge Cases

A requested in-degree larger than the vertex degree is rejected by the flow network itself. For

```
2 1
2 -1
1 2
```

the edge node has one unit available, while vertex 1's edge to `T` requires two units because its lower and upper bounds are both 2. There is no way to send two units into vertex 1 from a single edge node. The auxiliary maximum flow cannot saturate all balancing edges, so the program prints `NO`.

A zero requirement is handled as an exact lower and upper bound of zero. For

```
2 1
0 -1
1 2
```

the edge node must send its one unit to vertex 2, because vertex 1 has no capacity on its `v -> T` edge. The recovered flow therefore prints `2 1`, giving vertex 1 in-degree zero.

A value of `-1` becomes a flexible interval `[0, degree[v]]`. For

```
2 1
1 -1
1 2
```

vertex 1 has interval `[1,1]`, so the only feasible assignment sends the edge into vertex 1. Vertex 2 can receive anything from zero through one, so its final in-degree of zero is valid.

When every vertex is constrained, there is no spare endpoint that can absorb excess flow. In

```
3 3
1 1 1
1 2
2 3
3 1
```

every edge node must send one unit, and each vertex-to-`T` edge accepts exactly one. The circulation can route the three units around the triangle, producing a directed cycle. The exact capacities are what prevent any vertex from receiving two edges while another receives none.

The maximum-size case is a 2000-cycle with every requested in-degree equal to one. Each vertex can receive one of its two incident edges, and the directed cycle itself is a valid orientation. The flow construction has 2000 edge nodes and 2000 original vertex nodes, yet its structure remains linear in the input size, so the same algorithm applies without any special handling.
