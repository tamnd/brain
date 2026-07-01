---
title: "CF 104375K - Kingdom Power C."
description: "The game can be modeled as a directed graph where each level is a node and each prerequisite relation is a directed edge. If there is an edge from level u to level v, then finishing u unlocks v, so v becomes playable after u is completed."
date: "2026-07-01T17:31:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104375
codeforces_index: "K"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 104375
solve_time_s: 84
verified: true
draft: false
---

[CF 104375K - Kingdom Power C.](https://codeforces.com/problemset/problem/104375/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The game can be modeled as a directed graph where each level is a node and each prerequisite relation is a directed edge. If there is an edge from level `u` to level `v`, then finishing `u` unlocks `v`, so `v` becomes playable after `u` is completed.

A single playthrough, called a run, starts at any one of the designated starting levels and proceeds along directed edges, always moving to an unlocked level, until it reaches a level that has no outgoing transitions among the playable options, which is guaranteed to be one of the designated ending levels. After finishing a run, the player starts a new game plus from scratch, but with a strict restriction: every level used in any previous run becomes permanently unavailable for all future runs.

The goal is to maximize how many complete runs can be performed before it becomes impossible to start another run from any starting level and reach any ending level without reusing already consumed nodes.

The key interaction is that runs are not independent. Each run consumes all levels on its chosen path, and those nodes cannot be reused later. This turns the problem into selecting as many valid paths as possible from the set of starting nodes to the set of ending nodes, with the constraint that no node can appear in more than one path.

The constraints `N ≤ 100` strongly suggest that exponential enumeration of paths is not viable. Even a moderate branching factor graph can contain exponentially many simple paths between sources and sinks, so any approach that attempts to list or try all runs will fail. A polynomial flow-based or matching-based formulation is expected.

A subtle edge case appears when multiple starting levels can reach overlapping intermediate structures. For example, if two starts both lead into a shared chain before reaching a sink, naive greedy selection of one path can block more optimal combinations later.

Another edge case occurs when a level is both reachable from a start and lies on multiple potential paths to different ends. Choosing it early in a greedy path selection can reduce the total number of possible disjoint runs.

## Approaches

A direct attempt is to simulate runs greedily. One could repeatedly pick a starting node, find any path to an ending node using DFS or BFS, remove all nodes on that path, and repeat until no valid path exists. This is simple and each run is individually valid.

However, this approach depends heavily on the order in which paths are chosen. A locally valid path may consume a node that is critical for enabling two other disjoint paths later. In graphs with shared bottlenecks, greedy choices can reduce the total count significantly.

The core observation is that each run is a path from some source node to some sink node, and no node may be reused across runs. This is exactly a maximum number of vertex-disjoint paths problem in a directed graph with multiple sources and sinks.

This can be converted into a maximum flow problem using node splitting. Each node is split into an “in-node” and “out-node” connected by an edge of capacity one, enforcing that the node can be used in at most one run. Every original directed edge `u -> v` becomes an infinite capacity edge from `u_out` to `v_in`. A super source connects to all starting nodes, and all ending nodes connect to a super sink.

The maximum flow in this network equals the maximum number of disjoint valid runs. Each unit of flow corresponds to one full path from a start to an end, and the node capacity constraint guarantees that no level is reused across different runs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy path removal | Exponential in worst case | O(N + M) | Too slow / Incorrect |
| Max flow with node splitting | O(F · E) with Dinic, F ≤ N | O(N + M) | Accepted |

## Algorithm Walkthrough

We convert the problem into a flow network where paths correspond to runs and flow units correspond to completed playthroughs.

1. Split every node `i` into two nodes `i_in` and `i_out`, and connect them with an edge of capacity 1. This enforces that each level can be used in at most one run.
2. For every prerequisite edge `u -> v`, add a directed edge from `u_out` to `v_in` with infinite capacity. This preserves the original movement rules without restricting how many different runs can traverse the edge.
3. Add a super source node. Connect it to `s_in` for every starting level `s` with capacity 1. This ensures each starting level can initiate at most one run.
4. Add a super sink node. Connect `e_out` to the sink for every ending level `e` with capacity 1. This ensures each ending level can terminate at most one run.
5. Run a maximum flow algorithm from the super source to the super sink. The resulting flow value is the maximum number of disjoint runs.

The reason this construction works is that any valid run corresponds to a path in the flow network, and any unit of flow corresponds to selecting such a path. The node splitting guarantees disjointness across all runs.

### Why it works

Any feasible set of runs defines a set of vertex-disjoint paths from sources to sinks, and therefore can be mapped directly to a valid flow where each path carries one unit. Conversely, any integer flow can be decomposed into source-to-sink paths, and the capacity-one constraint on each split node ensures no node appears in more than one path. This establishes a one-to-one correspondence between valid solutions and feasible flows, so maximizing flow maximizes the number of runs.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Dinic:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.adj[u].append([v, c, len(self.adj[v])])
        self.adj[v].append([u, 0, len(self.adj[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = [s]
        self.level[s] = 0
        for u in q:
            for v, c, _ in self.adj[u]:
                if c > 0 and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] != -1

    def dfs(self, u, t, f):
        if u == t:
            return f
        for i in range(self.it[u], len(self.adj[u])):
            self.it[u] = i
            v, c, rev = self.adj[u][i]
            if c > 0 and self.level[v] == self.level[u] + 1:
                pushed = self.dfs(v, t, min(f, c))
                if pushed:
                    self.adj[u][i][1] -= pushed
                    self.adj[v][rev][1] += pushed
                    return pushed
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

n, s, e = map(int, input().split())
starts = list(map(int, input().split()))
ends = set(map(int, input().split()))
m = int(input())

N = 2 * n + 2
SRC = 2 * n
SNK = 2 * n + 1

dinic = Dinic(N)

for i in range(1, n + 1):
    dinic.add_edge(2 * (i - 1), 2 * (i - 1) + 1, 1)

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    dinic.add_edge(2 * u + 1, 2 * v, 10**9)

for st in starts:
    st -= 1
    dinic.add_edge(SRC, 2 * st, 1)

for en in ends:
    en -= 1
    dinic.add_edge(2 * en + 1, SNK, 1)

print(dinic.max_flow(SRC, SNK))
```

The implementation begins by building the node-split structure where each level contributes an in-node and out-node connected by capacity one. This is the mechanism that enforces single usage across all runs.

Prerequisite edges are added from out-nodes to in-nodes with large capacity so they do not constrain reuse beyond structure.

Starts connect from the super source into in-nodes, and ends connect from out-nodes into the super sink, ensuring each run begins and ends properly.

Finally, Dinic’s algorithm computes the maximum number of disjoint source-to-sink paths, which directly corresponds to the maximum number of game runs.

## Worked Examples

### Sample 1

Input:

```
3 1 1
2
3
3
1 2
2 3
1 3
```

We build split nodes: `1,2,3` each with capacity 1 through their internal edges. Start is node 2, end is node 3.

| Step | Flow Action | Used Path | Total Flow |
| --- | --- | --- | --- |
| 1 | Find augmenting path | 2 → 3 | 1 |

After sending one unit of flow, node 2 and node 3 are consumed. No other path can be formed because the only start and end have been exhausted.

Output is:

```
1
```

This shows a bottleneck where a single shared structure limits all possible runs.

### Sample 2

Input:

```
3 3 3
1 2 3
1 2 3
3
1 2
1 3
2 3
```

All nodes are both potential starts and ends, and edges allow full connectivity.

| Step | Flow Action | Used Path | Total Flow |
| --- | --- | --- | --- |
| 1 | Choose 1→2 | 1 → 2 | 1 |
| 2 | Choose 2→3 | 2 → 3 | 2 |
| 3 | Choose 3 | 3 → 3 | 3 |

Each node can serve exactly one run due to capacity constraints, and the structure allows full utilization.

Output:

```
3
```

This demonstrates that the model extracts as many disjoint source-to-sink paths as the graph structure permits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(F · E √V) | Dinic runs efficiently on this small graph, with at most N units of flow |
| Space | O(N + M) | Each node is split and each edge stored once in adjacency lists |

The constraints `N ≤ 100` make the flow network tiny, with at most a few hundred nodes and edges. Even a straightforward implementation of Dinic comfortably runs within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import check_output
    return check_output(["python3", "solution.py"], input=inp.encode()).decode().strip()

# provided samples
assert run("""3 1 1
2
3
3
1 2
2 3
1 3
""") == "1"

assert run("""3 3 3
1 2 3
1 2 3
3
1 2
1 3
2 3
""") == "3"

# custom cases
assert run("""1 1 1
1
1
0
""") == "1", "single node"

assert run("""4 1 1
1
4
3
1 2
2 3
3 4
""") == "1", "single chain"

assert run("""4 2 2
1 2
3 4
4
1 3
2 3
3 4
2 4
""") == "2", "two disjoint routes"

assert run("""5 1 1
1
5
6
1 2
2 5
1 3
3 5
2 4
4 5
""") == "1", "shared bottleneck"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | trivial start equals end |
| single chain | 1 | linear dependency |
| two disjoint routes | 2 | parallel path usage |
| shared bottleneck | 1 | node capacity constraint enforced |

## Edge Cases

A key edge case is when multiple valid paths compete for a single intermediate node. For example, if two starting levels both lead into a shared corridor before reaching different ends, only one run can pass through that corridor because the node capacity is one. The flow model naturally enforces this by saturating the split edge of the shared node after the first path is chosen.

Another case is when a starting level is also an ending level. The construction allows a direct connection from source to sink through that node, and its capacity restriction ensures it can only be used once across all runs. The flow will either use it as a standalone run or reserve it for a longer path, depending on global optimality.

A final case is a fully disconnected graph where no starting level can reach any ending level. In this situation, no augmenting path exists in the flow network, so the maximum flow is zero, matching the fact that no runs are possible.
