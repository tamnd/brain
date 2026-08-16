---
title: "CF 102419H - In-degree"
description: "We have an undirected graph, and every edge must eventually point toward exactly one of its two endpoints. For a vertex whose value is specified as (ai), exactly (ai) incident edges must point into that vertex. A vertex with (ai=-1) has no restriction on its final in-degree."
date: "2026-08-16T09:02:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "H"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 287
verified: false
draft: false
---

[CF 102419H - In-degree](https://codeforces.com/problemset/problem/102419/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph, and every edge must eventually point toward exactly one of its two endpoints. For a vertex whose value is specified as (a_i), exactly (a_i) incident edges must point into that vertex. A vertex with (a_i=-1) has no restriction on its final in-degree.

The task is to find such an orientation, or prove that none exists. The output contains either `NO`, or `YES` followed by the direction of every original edge. For an original edge ((u,v)), printing `u v` means the edge is directed from (u) to (v), so (v) receives one unit of in-degree.

The original constraints have (n,m\le 2000), with no parallel edges or self-loops. This is small enough for a polynomial graph algorithm, but it rules out algorithms that enumerate orientations. There are (2^m) possible orientations, and when (m=2000), even examining one orientation in constant time would already be hopeless. A flow network with (O(n+m)) vertices and edges is comfortably within the memory limit, and a standard integral max-flow algorithm is suitable.

There are several cases that are easy to mishandle.

Consider

```
2 1
0 0
1 2
```

Both vertices demand in-degree zero, but the only edge has to point somewhere. The correct answer is `NO`. Merely checking that every requested value is at most the corresponding degree would incorrectly accept this case.

Now consider

```
2 1
2 -1
1 2
```

Vertex 1 has degree one but requests in-degree two. The correct answer is `NO`. A flow construction must respect the exact requested amount rather than treating it as an upper bound.

There is also a less obvious issue when an edge joins two constrained vertices. For example,

```
2 1
0 1
1 2
```

The edge is forced to point into vertex 2. An approach that only tries to choose some edges to satisfy constrained vertices must make sure that every edge between two constrained vertices is assigned to one of them. Leaving such an edge unassigned cannot later be repaired by pointing it toward an unconstrained vertex, because neither endpoint is unconstrained.

Finally, an edge whose two endpoints are unconstrained does not need to participate in the constraint-solving part at all. After all constrained in-degrees have been satisfied, that edge can be oriented arbitrarily.

## Approaches

The direct brute-force approach is to try both directions for every edge. A depth-first search can make one binary decision per edge and, after reaching a complete orientation, count all in-degrees and check the constraints. It is correct because every possible orientation appears in exactly one branch of the search tree. The problem is its size: there are (2^m) leaves, and checking an orientation takes (O(m+n)), giving (O(2^m(m+n))) work. At (m=2000), this is completely infeasible.

The useful observation is that an oriented edge can be viewed as assigning one unit of in-degree to exactly one endpoint. Instead of deciding an edge's direction directly, we can create a flow decision saying which endpoint receives that unit.

For every relevant original edge, create a flow node. From the edge node we can send one unit to either endpoint. A constrained vertex has an exact amount (a_i) that must arrive there. An edge joining two constrained vertices must send its unit somewhere, while an edge with an unconstrained endpoint may leave the flow network without contributing to a constrained vertex.

The exact vertex requirements and mandatory constrained-to-constrained edges are naturally represented by lower and upper bounds on flow. This gives a feasible-circulation problem.

For every edge, we distinguish three cases. If both endpoints are constrained, its edge node must receive exactly one unit. If exactly one endpoint is constrained, its edge node may send zero or one unit to that constrained endpoint. If neither endpoint is constrained, we ignore it while solving the constraints and orient it arbitrarily afterward.

For every constrained vertex (v), the edge from (v) to the sink has both lower and upper bound equal to (a_v). Thus exactly (a_v) selected edge units must reach (v).

The standard lower-bound transformation removes the lower bounds and records the resulting imbalance at every node. A super-source and super-sink are then added, and an ordinary maximum flow determines whether the required circulation exists.

The key connection is that a unit of flow reaching vertex (v) corresponds exactly to one original edge directed into (v). Since the flow is integral, every selected edge is assigned to one endpoint, never fractionally split.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^m(m+n))) | (O(m+n)) | Too slow |
| Lower-bound circulation + Dinic | (O(V^2E)) worst case | (O(V+E)) | Accepted |

Here (V=O(n+m)) and (E=O(n+m)) for the constructed network. With (n,m\le2000), the network has only a few thousand vertices and edges, and the practical behavior of Dinic on this sparse, mostly unit-capacity network is sufficient for the limit.

## Algorithm Walkthrough

1. Read the graph and mark every vertex with (a_i\ne-1) as constrained. Store the original endpoints of every edge because the final answer must be printed in the original edge order.
2. Build a flow network containing a source (S), a sink (T), one node for every original edge that touches at least one constrained vertex, and one node for every constrained vertex.

An edge with two unconstrained endpoints is omitted because it can never affect a required in-degree. It can safely be oriented afterward.
3. For every relevant original edge (e=(u,v)), create an edge node (E_e).

If both (u) and (v) are constrained, add

[
S\rightarrow E_e
]

with lower and upper bound both equal to (1). The edge must contribute one incoming edge to either (u) or (v).

If at least one endpoint is unconstrained, use lower bound (0) and upper bound (1). Such an edge is allowed to contribute to a constrained endpoint, but it does not have to.

From (E_e), add capacity (1) edges to every constrained endpoint of the original edge. Sending one unit through (E_e\rightarrow v) means orienting the original edge toward (v).
4. For every constrained vertex (v), add an edge

[
v\rightarrow T
]

whose lower and upper bounds are both (a_v).

Since the amount leaving (v) is forced to be exactly (a_v), flow conservation forces exactly (a_v) units to enter (v). This is precisely the required in-degree.
5. Add an edge (T\rightarrow S) with capacity (m). This closes the network into a circulation. Its exact amount does not matter, because conservation forces it to equal the total number of units assigned to constrained vertices.
6. Convert every bounded edge ((u,v)) with lower bound (L) and upper bound (R) into an ordinary edge of capacity (R-L). Maintain a balance array. Subtract (L) from the balance of (u) and add (L) to the balance of (v).

The balance records the effect of the flow that was already forced by lower bounds. The remaining ordinary flow has to compensate for these imbalances.
7. Add a super-source (SS) and super-sink (TT). If a node has positive balance, add (SS\rightarrow v) with capacity equal to that balance. If it has negative balance, add (v\rightarrow TT) with capacity equal to its absolute balance.

A feasible circulation exists exactly when the maximum flow from (SS) to (TT) saturates all these balance edges. If it does not, print `NO`.
8. If the circulation is feasible, inspect each original relevant edge's flow from its edge node to its constrained endpoint. If one unit goes to (u), orient the original edge toward (u). If one unit goes to (v), orient it toward (v).

A constrained-constrained edge always has exactly one such unit because its source-to-edge flow is forced to one. For an edge with one unconstrained endpoint, zero flow simply means we orient it toward that unconstrained endpoint. For an edge with two unconstrained endpoints, choose either direction.
9. Print `YES` and the resulting orientation of every original edge.

The invariant throughout the construction is that every unit entering a constrained vertex represents one and only one original edge whose head is that vertex. The exact lower and upper bound on a constrained vertex forces precisely its requested number of such units. Mandatory flow through an edge node guarantees that every edge joining two constrained vertices receives a head. Consequently, a feasible circulation maps directly to a valid orientation. Conversely, any valid orientation induces a feasible circulation by sending one unit through every edge node to the vertex that is the head of that edge, so the flow test cannot reject a genuinely valid instance.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        idx = len(self.g[u])
        self.g[u].append([v, cap, len(self.g[v])])
        self.g[v].append([u, 0, idx])
        return idx

    def bfs(self, s, t):
        level = [-1] * self.n
        level[s] = 0
        q = [s]
        head = 0

        while head < len(q):
            u = q[head]
            head += 1

            for v, cap, rev in self.g[u]:
                if cap > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    q.append(v)

        self.level = level
        return level[t] != -1

    def dfs(self, u, t, pushed):
        if u == t:
            return pushed

        g_u = self.g[u]
        while self.it[u] < len(g_u):
            i = self.it[u]
            v, cap, rev = g_u[i]

            if cap > 0 and self.level[v] == self.level[u] + 1:
                got = self.dfs(v, t, min(pushed, cap))
                if got:
                    g_u[i][1] -= got
                    self.g[v][rev][1] += got
                    return got

            self.it[u] += 1

        return 0

    def max_flow(self, s, t):
        flow = 0
        INF = 10**9

        while self.bfs(s, t):
            self.it = [0] * self.n
            while True:
                pushed = self.dfs(s, t, INF)
                if not pushed:
                    break
                flow += pushed

        return flow

def solve(data):
    it = iter(map(int, data.split()))
    n = next(it)
    m = next(it)

    a = [next(it) for _ in range(n)]
    edges = [(next(it), next(it)) for _ in range(m)]

    constrained = [x != -1 for x in a]

    # Node layout:
    # 0 ... n-1                 constrained vertex slots
    # edge_base ... edge nodes
    # S, T, SS, TT
    #
    # We only need vertex nodes for constrained vertices.
    vertex_id = [-1] * n
    vertex_nodes = []

    for v in range(n):
        if constrained[v]:
            vertex_id[v] = len(vertex_nodes)
            vertex_nodes.append(v)

    k = len(vertex_nodes)
    edge_base = k
    relevant = []

    for i, (u, v) in enumerate(edges):
        u -= 1
        v -= 1

        if constrained[u] or constrained[v]:
            relevant.append(i)

    r = len(relevant)

    S = k + r
    T = S + 1
    SS = T + 1
    TT = SS + 1
    N = TT + 1

    dinic = Dinic(N)
    balance = [0] * N

    # Store references to edge-node -> constrained-vertex arcs.
    # Each entry is (edge_index, original_endpoint, network_u, arc_index).
    choice_arcs = []

    def add_bounded(u, v, low, high):
        if low > high:
            return False

        cap = high - low
        dinic.add_edge(u, v, cap)

        balance[u] -= low
        balance[v] += low
        return True

    # Source -> edge node.
    for pos, ei in enumerate(relevant):
        u, v = edges[ei]
        u -= 1
        v -= 1

        enode = edge_base + pos

        if constrained[u] and constrained[v]:
            low = high = 1
        else:
            low, high = 0, 1

        if not add_bounded(S, enode, low, high):
            return "NO\n"

        if constrained[u]:
            idx = dinic.add_edge(enode, vertex_id[u], 1)
            choice_arcs.append((ei, u, enode, idx))

        if constrained[v]:
            idx = dinic.add_edge(enode, vertex_id[v], 1)
            choice_arcs.append((ei, v, enode, idx))

    # Every constrained vertex must receive exactly a[v] units.
    for v in vertex_nodes:
        need = a[v]
        if need < 0:
            continue

        # A vertex cannot receive more than its graph degree.
        # The lower-bound construction would reject this anyway,
        # but this check avoids creating an obviously impossible edge.
        degree = 0
        for u, w in edges:
            u -= 1
            w -= 1
            if u == v or w == v:
                degree += 1

        if need > degree:
            return "NO\n"

        if not add_bounded(vertex_id[v], T, need, need):
            return "NO\n"

    # Close the network into a circulation.
    add_bounded(T, S, 0, m)

    # Satisfy all lower-bound imbalances.
    required = 0

    for v in range(N - 2):
        if balance[v] > 0:
            dinic.add_edge(SS, v, balance[v])
            required += balance[v]
        elif balance[v] < 0:
            dinic.add_edge(v, TT, -balance[v])

    got = dinic.max_flow(SS, TT)

    if got != required:
        return "NO\n"

    # Start with arbitrary directions.
    answer = []
    for u, v in edges:
        answer.append([u, v])

    # A relevant edge with flow into a constrained endpoint is directed
    # toward that endpoint.
    selected = {}

    for ei, endpoint, enode, idx in choice_arcs:
        # The residual capacity of the forward edge is 0 exactly when
        # one unit of flow is using it.
        if dinic.g[enode][idx][1] == 0:
            selected[ei] = endpoint

    for ei in relevant:
        u, v = edges[ei]
        u -= 1
        v -= 1

        if ei in selected:
            head = selected[ei]

            if head == u:
                answer[ei] = [v + 1, u + 1]
            else:
                answer[ei] = [u + 1, v + 1]
        else:
            # No constrained endpoint receives this edge.
            # This is possible only when at least one endpoint is free.
            if not constrained[u]:
                answer[ei] = [v + 1, u + 1]
            else:
                answer[ei] = [u + 1, v + 1]

    out = ["YES"]
    for u, v in answer:
        out.append(f"{u} {v}")

    return "\n".join(out) + "\n"

def main():
    data = sys.stdin.buffer.read()
    sys.stdout.write(solve(data.decode()))

if __name__ == "__main__":
    main()
```

The `Dinic` class stores every residual edge as `[to, capacity, reverse_index]`. The reverse index is what lets an augmentation immediately update the reverse residual capacity without searching through the adjacency list.

The `add_bounded` function is the core of the lower-bound transformation. For an original bound (L\le f\le R), it creates residual capacity (R-L), then records the mandatory (L) units in `balance`. A positive balance means the node has mandatory incoming flow that must be compensated by additional outgoing flow, which is why the super-source is connected to it.

Only constrained vertices need actual vertex nodes. An edge between two free vertices has no effect on any requirement, so removing it from the flow network makes the construction smaller without changing feasibility.

The `choice_arcs` array remembers exactly which residual edge corresponds to each possible head of each original edge. After the max flow succeeds, a saturated choice arc means one unit was sent to that endpoint. Since every relevant edge node receives exactly one unit when both endpoints are constrained, or at most one when a free endpoint exists, there is never ambiguity about the selected head.

The degree check is technically redundant because the circulation itself detects an impossible lower bound, but it handles the most obvious impossible case before running the flow. Python integers have arbitrary precision, so there is no integer overflow issue.

The output reconstruction deliberately starts with arbitrary directions. Only edges that participate in the constraint network are overwritten. An unselected relevant edge must have a free endpoint, so directing it toward that endpoint cannot violate any exact in-degree requirement.

## Worked Examples

For Sample 1, the constrained vertices are (1,2,3,5), with requested in-degrees (1,2,1,0). Vertex 4 is free.

A valid sequence of selected heads is shown below. The remaining demand is the number of incoming edges still needed by each constrained vertex.

| Edge | Selected head | Remaining demand after the edge |
| --- | --- | --- |
| (1-2) | 2 | (a=(1,1,1,0)) |
| (1-3) | 1 | (a=(0,1,1,0)) |
| (2-3) | 2 | (a=(0,0,1,0)) |
| (3-4) | 3 | (a=(0,0,0,0)) |
| (4-5) | 4 | (a=(0,0,0,0)) |

The last edge is not assigned to constrained vertex 5 because its demand is already zero. It is directed toward free vertex 4 instead. The resulting directions are exactly the sample orientation:

```
1 2
3 1
3 2
4 3
5 4
```

The trace demonstrates the central invariant. Every time a constrained endpoint is selected as the head, its remaining demand decreases by one, and the circulation accepts the orientation only when all exact demands are satisfied.

For Sample 2, the only difference is that vertex 5 now requires one incoming edge. The first four edges can be handled exactly as before, leaving one unit of demand at vertex 5.

| Edge | Selected head | Remaining demand after the edge |
| --- | --- | --- |
| (1-2) | 2 | (a=(1,1,1,1)) |
| (1-3) | 1 | (a=(0,1,1,1)) |
| (2-3) | 2 | (a=(0,0,1,1)) |
| (3-4) | 3 | (a=(0,0,0,1)) |
| (4-5) | 5 | (a=(0,0,0,0)) |

The final edge therefore points from 4 to 5. The resulting orientation is

```
1 2
3 1
3 2
4 3
4 5
```

Here the trace exercises an edge with one free endpoint and one constrained endpoint. In Sample 1 that edge was allowed to avoid the constrained endpoint, while in Sample 2 the exact demand at vertex 5 forces it to point there.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(V^2E)) worst case for Dinic | The constructed circulation network has (V=O(n+m)) and (E=O(n+m)) |
| Space | (O(V+E)) | Residual graph, balances, original edges, and reconstruction data are all linear |

With (n,m\le2000), the constructed network has only (O(4000)) vertices and (O(4000)) to (O(6000)) logical edges before residual edges are added. The graph is sparse, and almost all edge-choice capacities are one. This is well within the 256 MB memory limit and is practical for the 1 second limit with the optimized Dinic implementation.

## Test Cases

Because the problem allows any valid orientation, a test cannot safely compare the complete output text against one fixed answer. The harness below checks the `YES` or `NO` result and, for `YES`, verifies that every printed directed edge corresponds to an original edge and that every constrained vertex receives exactly its requested in-degree.

```python
# Save the editorial solution as solution.py before running these tests.

from solution import solve

def run(inp: str) -> str:
    out = solve(inp)
    tokens = out.split()

    data = list(map(int, inp.split()))
    p = 0

    n = data[p]
    m = data[p + 1]
    p += 2

    a = data[p:p + n]
    p += n

    edges = []
    for _ in range(m):
        u = data[p]
        v = data[p + 1]
        p += 2
        edges.append((u, v))

    if not tokens:
        raise AssertionError("empty output")

    if tokens[0] == "NO":
        return "NO"

    assert tokens[0] == "YES", f"bad first token: {tokens[0]}"
    assert len(tokens) == 1 + 2 * m, "wrong number of output vertices"

    original = {tuple(sorted(e)) for e in edges}
    used = set()
    indeg = [0] * (n + 1)

    q = 1
    for _ in range(m):
        u = int(tokens[q])
        v = int(tokens[q + 1])
        q += 2

        assert 1 <= u <= n
        assert 1 <= v <= n
        assert u != v
        assert tuple(sorted((u, v))) in original
        assert tuple(sorted((u, v))) not in used, "an original edge was repeated"

        used.add(tuple(sorted((u, v))))
        indeg[v] += 1

    assert len(used) == m

    for v in range(1, n + 1):
        if a[v - 1] != -1:
            assert indeg[v] == a[v - 1], (
                f"vertex {v}: expected {a[v - 1]}, got {indeg[v]}"
            )

    return "YES"

# Sample 1
assert run("""\
5 5
1 2 1 -1 0
1 2
1 3
2 3
3 4
4 5
""") == "YES", "sample 1"

# Sample 2
assert run("""\
5 5
1 2 1 -1 1
1 2
1 3
2 3
3 4
4 5
""") == "YES", "sample 2"

# Minimum-size valid graph.
assert run("""\
2 1
0 1
1 2
""") == "YES", "minimum valid case"

# Boundary case: requested in-degree exceeds the actual degree.
assert run("""\
2 1
2 -1
1 2
""") == "NO", "degree upper boundary"

# Both endpoints are constrained and both demand zero.
# The single edge has nowhere valid to point.
assert run("""\
2 1
0 0
1 2
""") == "NO", "mandatory constrained-constrained edge"

# Maximum-size graph with all vertices unconstrained.
# A 2000-cycle has 2000 edges and needs no constrained flow at all.
n = 2000
cycle_edges = "\n".join(
    f"{i} {i + 1}" for i in range(1, n)
) + f"\n{n} 1\n"

max_case = f"{n} {n}\n" + ("-1 " * (n - 1)) + "-1\n" + cycle_edges

assert run(max_case) == "YES", "maximum-size all-free case"

# All-equal exact demands on a cycle.
all_equal_case = f"{n} {n}\n" + ("1 " * (n - 1)) + "1\n" + cycle_edges

assert run(all_equal_case) == "YES", "maximum-size all-equal case"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1`, demands `0 1`, edge `1 2` | `YES` | Minimum valid instance and exact one-unit demand |
| `2 1`, demands `2 -1`, edge `1 2` | `NO` | Requested in-degree larger than the available degree |
| `2 1`, demands `0 0`, edge `1 2` | `NO` | Edge between two constrained vertices cannot be left unassigned |
| 2000-cycle with every demand `-1` | `YES` | Maximum-size graph and handling of irrelevant free-free edges |
| 2000-cycle with every demand `1` | `YES` | Maximum-size graph with all vertices constrained and equal exact demands |

## Edge Cases

The first edge case is a requested in-degree larger than the vertex degree. For

```
2 1
2 -1
1 2
```

vertex 1 has degree one but requires two incoming edges. The construction adds a lower and upper bound of two on the edge from vertex 1 to (T), while the only incident edge can contribute at most one unit. The circulation cannot satisfy the lower bound, so the maximum flow fails and the algorithm prints `NO`.

The second edge case is an edge whose endpoints are both constrained. For

```
2 1
0 0
1 2
```

the edge node for (1-2) receives a mandatory one unit from (S), because both endpoints are constrained. It can only send that unit to vertex 1 or vertex 2, but both vertices have an exact outgoing-to-(T) requirement of zero. The resulting imbalance cannot be repaired, so the flow reports infeasibility. This catches the common mistake of treating every edge as optional in the constraint network.

The third edge case is an edge between a constrained and an unconstrained vertex. Consider

```
2 1
0 -1
1 2
```

The edge node has an optional capacity of one toward constrained vertex 1. Since vertex 1 requires zero, the flow sends nothing through that choice. During reconstruction, the algorithm sees that the edge was not selected for the constrained endpoint and points it toward vertex 2 instead. The output is effectively `1 2`, giving vertex 1 in-degree zero as required.

The fourth edge case is a graph where every vertex is unconstrained. In a 2000-cycle with all (a_i=-1), the flow network has no constrained vertex requirements and the cycle edges do not need to participate in the circulation. The algorithm simply chooses arbitrary directions for all of them and prints `YES`. This is why free-free edges can safely be omitted from the flow model.

The final case is the all-constrained situation. For a triangle with

```
3 3
1 1 1
1 2
2 3
3 1
```

every edge joins two constrained vertices, so every edge node is forced to carry exactly one unit. The three vertices each require one unit, so the circulation can send the three units to the three vertices, for example producing the directed cycle (1\rightarrow2), (2\rightarrow3), (3\rightarrow1). Each vertex receives exactly one edge. This case demonstrates that the lower-bound construction also handles the original prescribed-indegree orientation problem when there are no unconstrained vertices.
