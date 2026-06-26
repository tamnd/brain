---
title: "CF 105710H - Lobotomy"
description: "We are given a network of neurons, where each neuron is a node and each synapse is an undirected connection between two neurons. Unlike a standard simple graph, multiple synapses can connect the same pair of neurons, and a synapse can even connect a neuron to itself."
date: "2026-06-26T08:01:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105710
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 2-12-25 Div. 1 (Advanced)"
rating: 0
weight: 105710
solve_time_s: 70
verified: true
draft: false
---

[CF 105710H - Lobotomy](https://codeforces.com/problemset/problem/105710/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a network of neurons, where each neuron is a node and each synapse is an undirected connection between two neurons. Unlike a standard simple graph, multiple synapses can connect the same pair of neurons, and a synapse can even connect a neuron to itself.

The doctor wants to perform exactly one cut, meaning we remove a single synapse. A synapse is considered dangerous if removing it breaks the brain into at least two disconnected components, so some neurons can no longer reach others. The task is to identify all synapses whose removal would disconnect the graph, and output their identifiers in sorted order. If no such synapse exists, we output -1.

Each synapse has a unique integer ID, and we must reason in terms of these IDs, not just endpoints.

The constraint on the number of neurons and synapses goes up to a few hundred thousand. This immediately rules out any quadratic or per-edge re-simulation approach. Any solution that tries to remove each edge and run a BFS or DFS would cost O(m(n + m)), which is far too large.

The key subtlety is that the graph is not simple. Parallel edges completely change the definition of a “critical” connection. For example, if two synapses connect the same pair of neurons, removing one of them never disconnects that pair, even if the underlying structure would otherwise be fragile.

A naive approach that ignores this will fail on cases like:

Input:

```
3 2
1 0 1
2 0 1
```

Here there are two parallel synapses between the same pair of nodes. Even though the endpoints look like a bridge in a simple graph, neither edge should be removed because the other still preserves connectivity. A naive bridge-finding algorithm would incorrectly label them as bridges.

Another failure mode happens with self-loops. A synapse from a neuron to itself never contributes to connectivity between different components, so removing it can never disconnect the graph. Treating it like a normal edge leads to incorrect inclusion.

## Approaches

A brute-force solution would iterate over every synapse, remove it, and run a DFS to check whether the graph is still connected. Each connectivity check costs O(n + m), so the total complexity becomes O(m(n + m)). With up to 200,000 edges, this is infeasible.

The structure of the problem suggests we are really being asked to find bridges in an undirected graph. A bridge is an edge that, when removed, increases the number of connected components. The classical solution is Tarjan’s algorithm using DFS timestamps and low-link values, which computes all bridges in linear time O(n + m).

However, the presence of multiple edges introduces a complication. Tarjan’s algorithm assumes a simple graph. If two nodes are connected by more than one edge, none of those edges should ever be considered a bridge, because at least one alternate direct route always remains.

This leads to the key refinement: we first compress the multigraph structure by tracking how many synapses exist between each unordered pair of nodes. Then we run a standard bridge-finding DFS, but we only accept an edge as a valid bridge if it is a bridge in the DFS sense and it is the only synapse between its endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Remove each edge + DFS | O(m(n + m)) | O(n + m) | Too slow |
| Tarjan bridges with multiplicity filtering | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We treat each synapse as a distinct edge with an ID, but we also group edges by their endpoint pair.

1. We build an adjacency list storing, for each neuron, all incident synapses along with their destination and ID. At the same time, we count how many synapses connect each unordered pair of neurons. This lets us later distinguish unique edges from duplicates.
2. We run a DFS over the graph to compute discovery times and low-link values. These values capture the earliest reachable ancestor from each subtree, which is the standard tool for detecting bridges.
3. During DFS, when we traverse an edge from u to v, we skip the reverse tree-edge immediately but otherwise apply the standard Tarjan logic: after visiting v, we check whether low[v] > disc[u]. If this inequality holds, then the edge (u, v) is a bridge candidate.
4. Before finalizing that edge as a bridge, we check whether the pair (u, v) has more than one synapse. If it does, we discard all edges between u and v from being bridges, since redundancy guarantees connectivity even after removal.
5. We collect all synapse IDs that satisfy both conditions: they are DFS bridges and belong to a unique edge pair.
6. Finally, we sort the resulting IDs and output them. If none exist, we output -1.

Why it works is tied to two invariants. First, DFS low-link values correctly characterize whether a subtree has an alternative back-edge to an ancestor, which is exactly the condition for an edge to be non-essential in connectivity. Second, edge multiplicity acts as an independent structural guarantee: if two vertices share at least two edges, removing one cannot disconnect them, regardless of the DFS structure. Combining these two facts ensures that every reported synapse is truly the unique critical connection between two parts of the graph.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n, m = map(int, input().split())

edges = []
adj = [[] for _ in range(n)]
pair_count = {}

for i in range(m):
    eid, u, v = map(int, input().split())
    edges.append((u, v, eid))
    adj[u].append((v, i))
    adj[v].append((u, i))

    a, b = (u, v) if u <= v else (v, u)
    pair_count[(a, b)] = pair_count.get((a, b), 0) + 1

disc = [-1] * n
low = [0] * n
timer = 0
is_bridge = [False] * m

def dfs(u, pe):
    global timer
    disc[u] = low[u] = timer
    timer += 1

    for v, eid in adj[u]:
        if eid == pe:
            continue

        if disc[v] == -1:
            dfs(v, eid)
            low[u] = min(low[u], low[v])

            if low[v] > disc[u]:
                is_bridge[eid] = True
        else:
            low[u] = min(low[u], disc[v])

for i in range(n):
    if disc[i] == -1:
        dfs(i, -1)

res = []

for i, (u, v, eid) in enumerate(edges):
    a, b = (u, v) if u <= v else (v, u)
    if is_bridge[i] and pair_count[(a, b)] == 1:
        res.append(eid)

if not res:
    print(-1)
else:
    res.sort()
    print(*res)
```

The DFS maintains discovery and low-link arrays exactly as in the standard bridge algorithm. The only deviation is that we explicitly track edge identities, since multiple synapses can exist between the same endpoints. The `pe` parameter prevents immediately revisiting the edge we came from, which is necessary in undirected DFS to avoid false cycles.

The `pair_count` map enforces the multigraph correction. Even if Tarjan marks an edge as a bridge structurally, we only accept it when it is the sole connection between its endpoints.

A subtle implementation detail is that we store bridge information per edge index, not per node pair, because multiple distinct synapses may connect the same nodes.

## Worked Examples

### Example 1

Input:

```
4 4
212 3 0
238 1 2
394 2 0
281 0 1
```

| Step | Current node | DFS action | low updates | bridges found |
| --- | --- | --- | --- | --- |
| 1 | 0 | start DFS | low[0]=0 | none |
| 2 | 1 | visit from 0 | low[1]=1 | none |
| 3 | 2 | visit from 1 | low[2]=2 | edge 238 candidate |
| 4 | 0 | explore next edge | low updated via back edges | none |
| 5 | finish | check edges | validate uniqueness | 212 kept |

The only edge that becomes critical is the synapse 212, since its removal separates a subtree that cannot reconnect via any alternative back-edge or parallel connection.

This trace shows how a single DFS tree edge becomes a bridge only when no back-edge exists to higher ancestors.

### Example 2

Input:

```
3 3
101 0 1
102 0 2
103 2 1
```

| Step | DFS tree | low values | bridge condition |
| --- | --- | --- | --- |
| 0 | 0-1-2 structure forms cycle | all nodes reachable | no low[v] > disc[u] |
| 1 | cycle detected | low links collapse | no bridges |

Here every edge participates in a cycle, so each node has an alternate route. The low-link values always propagate back to the root, preventing any bridge condition from triggering.

The final output is -1, confirming that the entire graph remains connected under any single cut.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS visits each node and edge once, with constant-time bridge checks |
| Space | O(n + m) | adjacency list, recursion stack, and auxiliary arrays |

The linear complexity is necessary given up to 200,000 synapses. Any solution relying on repeated graph traversal would exceed the time limit, while this approach processes the structure in a single pass.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n, m = map(int, input().split())
    edges = []
    adj = [[] for _ in range(n)]
    pair_count = {}

    for i in range(m):
        eid, u, v = map(int, input().split())
        edges.append((u, v, eid))
        adj[u].append((v, i))
        adj[v].append((u, i))
        a, b = (u, v) if u <= v else (v, u)
        pair_count[(a, b)] = pair_count.get((a, b), 0) + 1

    sys.setrecursionlimit(10**7)
    disc = [-1]*n
    low = [0]*n
    timer = 0
    is_bridge = [False]*m

    def dfs(u, pe):
        nonlocal timer
        disc[u] = low[u] = timer
        timer += 1
        for v, eid in adj[u]:
            if eid == pe:
                continue
            if disc[v] == -1:
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    is_bridge[eid] = True
            else:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)

    res = []
    for i, (u, v, eid) in enumerate(edges):
        a, b = (u, v) if u <= v else (v, u)
        if is_bridge[i] and pair_count[(a, b)] == 1:
            res.append(eid)

    return " ".join(map(str, sorted(res))) if res else "-1"

# custom cases

# single edge is bridge
assert run("2 1\n5 0 1\n") == "5", "single edge"

# cycle has no bridges
assert run("3 3\n1 0 1\n2 1 2\n3 2 0\n") == "-1", "cycle"

# parallel edges block bridges
assert run("2 2\n10 0 1\n11 0 1\n") == "-1", "parallel edges"

# chain
assert run("4 3\n1 0 1\n2 1 2\n3 2 3\n") == "1 2 3", "chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge | 5 | basic bridge detection |
| cycle | -1 | no bridges in cycles |
| parallel edges | -1 | multiplicity handling |
| chain | 1 2 3 | all edges are bridges |

## Edge Cases

A self-loop is the simplest non-obvious case. For input like:

```
2 1
100 0 0
```

the DFS sees an edge from a node to itself. It never satisfies the bridge condition because it does not connect different components in the first place. The algorithm ignores it correctly since it neither appears as a tree edge leading to a new node nor satisfies low[v] > disc[u].

Parallel edges between the same nodes demonstrate why structural DFS alone is insufficient:

```
2 2
1 0 1
2 0 1
```

Even though each edge individually looks like a candidate bridge in a naive traversal, the pair_count check filters them out. Both endpoints remain connected after removing either synapse, so neither is output.

A linear chain of nodes shows the intended positive case:

```
4 3
1 0 1
2 1 2
3 2 3
```

Every edge is the only connection between its endpoints, and no back-edges exist, so each satisfies the bridge condition and is correctly reported.
