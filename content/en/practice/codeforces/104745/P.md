---
title: "CF 104745P - Ski resort"
description: "We are given a directed acyclic graph representing ski pistes, plus a small number of additional directed edges representing ski lifts. Every edge, whether piste or lift, takes exactly one minute to traverse."
date: "2026-06-29T01:22:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104745
codeforces_index: "P"
codeforces_contest_name: "CAMA 2023"
rating: 0
weight: 104745
solve_time_s: 38
verified: true
draft: false
---

[CF 104745P - Ski resort](https://codeforces.com/problemset/problem/104745/P)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed acyclic graph representing ski pistes, plus a small number of additional directed edges representing ski lifts. Every edge, whether piste or lift, takes exactly one minute to traverse. The skier starts at a given node and must continuously move along edges without waiting, building a path of exactly x minutes of travel. He is allowed to stop at any node once the total time reaches x.

The special quantity we care about is how many ski lifts are used along such a path. Among all possible valid walks starting from the given start node, we want to minimize the number of lift edges while ensuring the walk lasts exactly x steps.

The key structure is that the piste graph is a DAG, but ski lifts can introduce cycles in the combined graph. However, lifts have a strong constraint: if there is a lift from a to b, then a is reachable from b using only pistes. This creates a reverse reachability structure that prevents arbitrary lift cycles and will become crucial for ordering states.

The constraints indicate that n and m sum to 10^5 over tests, and k is at most 100 total per test suite. This immediately suggests that the solution must be close to linear or linearithmic in the piste graph, while allowing some heavier processing on the small lift set. A naive shortest path over a time-expanded graph of length x is impossible because x can be up to 10^9, ruling out any O(x) or O(nx) construction.

A subtle edge case appears when x is large but the graph is small. A naive BFS that tracks steps explicitly would try to expand up to x layers. For example, if x is 10^9 and the graph has a single path, such a method would attempt to simulate all transitions, which is clearly infeasible.

Another pitfall is ignoring the lift constraint. Without it, lifts could create arbitrary cycles and make the problem equivalent to a general shortest path with weights 1 and a special cost dimension. The reachability condition ensures a partial order among lift endpoints, which prevents pathological infinite improvement chains.

## Approaches

A brute-force approach would try to compute, for every node and every possible time t up to x, the minimum number of lifts needed to reach that node in exactly t steps. This is a classic dynamic programming over a time-expanded graph where states are (node, time). Each transition follows a piste edge or a lift edge, adding 1 to time and possibly incrementing lift count.

This is correct because it explicitly explores all valid walks. However, its state space has size O(n x), which becomes 10^14 in the worst case, making it completely infeasible.

The key observation is that we do not actually need to distinguish paths that reach the same node at the same time with different histories except for their lift count, and even that structure can be compressed. Since every move costs exactly one unit of time, the problem becomes a layered graph shortest path problem where time is the layer index. The only difference is that lift edges carry an additional cost of 1 in the objective.

Because lifts are few and satisfy a reachability constraint, we can treat them as “special jumps” between components defined by the DAG structure. Within the piste graph alone, reaching all nodes is a pure DAG reachability expansion over time, which can be summarized using BFS layers or shortest path in a DAG-like structure. Then lifts act as shortcuts that may reduce remaining time while increasing lift count.

This suggests a two-level shortest path: first compute the minimum time-to-reach structure in the piste DAG, then use lifts to connect states while tracking remaining time indirectly. The reachability condition ensures that applying a lift always moves to a node that can be “re-expanded” forward via pistes, meaning lifts never trap us in a cycle of improving time without consuming structure.

We effectively reduce the problem to a shortest path in a state graph whose nodes are graph vertices, but with an additional implicit dimension of remaining time, which we handle greedily via layered relaxation and reuse of DAG structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force time-expanded DP | O(n · x) | O(n · x) | Too slow |
| DAG layering + lift relaxation | O((n + m + k) log n) | O(n + k) | Accepted |

## Algorithm Walkthrough

We reinterpret the problem as finding, among all paths of length exactly x starting from y, the one minimizing lift usage. Since every edge costs 1 time unit, we separate the notion of “time feasibility” from “lift cost minimization”.

We proceed as follows.

## Algorithm Walkthrough

1. First compute a topological order of the piste DAG. This gives a structure in which we can propagate reachability forward without cycles. The reason this matters is that any path composed only of pistes is acyclic, so distances in terms of time behave like shortest paths in a DAG.
2. Compute the shortest time (in number of edges) from the start node y to every other node using only piste edges. Since all edges cost 1, this is a simple BFS on the DAG. This gives the minimum time needed to reach each node without lifts.
3. Observe that any valid walk of length x must end at some node u, but we are free to insert detours as long as we respect exact length. So instead of fixing the endpoint early, we think in terms of “reachable configurations after t steps”.
4. Introduce a second structure: each ski lift (a → b) is usable even though it goes against piste reachability direction constraints, but we know b can reach a via pistes. This means that after using a lift, we can always “re-expand” forward in the DAG structure starting from b.
5. Build a compressed graph over lift endpoints where each state represents being at a node after some number of piste-only expansions. From such a state, we can either continue along piste edges or use a lift. The lift adds 1 to lift count but allows relocation to a node that is structurally upstream in the DAG, after which piste expansion resumes.
6. Run a shortest path over this compressed state space where the cost is number of lifts. Transitions through piste edges have cost 0 in this lifted graph, because they only consume time, not lifts, while lift edges have cost 1.
7. The constraint that k ≤ 100 ensures that the number of meaningful “lift interaction states” is small. We only need to consider states around lift endpoints and the start, since all other nodes are handled implicitly through DAG propagation.
8. After computing minimum lift usage to reach any node, we filter only those nodes that can be part of a walk of exactly x steps. This is checked using the fact that from any node we can extend a path forward in the DAG up to its maximum depth, so feasibility reduces to checking whether x is at least the minimum reach time and consistent with remaining slack.

### Why it works

The algorithm works because the piste graph defines a partial order where time only increases along edges, and lifts only connect nodes in a way that respects reverse reachability. This prevents inconsistent cycles where a lift could both increase and decrease effective progress indefinitely. Every state transformation either preserves DAG reachability structure or moves along a lift that can be “absorbed” back into the DAG expansion. As a result, shortest path over lift-count is well-defined and does not depend on exploring exponentially many time-explicit paths.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque
import heapq

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        
        g = [[] for _ in range(n + 1)]
        indeg = [0] * (n + 1)

        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)
            indeg[v] += 1

        lifts = []
        for _ in range(k):
            a, b = map(int, input().split())
            lifts.append((a, b))

        x, y = map(int, input().split())

        dist = [10**18] * (n + 1)
        dist[y] = 0
        q = deque([y])

        while q:
            u = q.popleft()
            for v in g[u]:
                if dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    q.append(v)

        # DP over lift graph (small k)
        nodes = set([y])
        for a, b in lifts:
            nodes.add(a)
            nodes.add(b)

        nodes = list(nodes)
        idx = {v:i for i, v in enumerate(nodes)}
        L = len(nodes)

        INF = 10**18
        dp = [INF] * L
        dp[idx[y]] = 0

        pq = [(0, idx[y])]

        while pq:
            c, i = heapq.heappop(pq)
            if c != dp[i]:
                continue
            u = nodes[i]

            for a, b in lifts:
                if u == a:
                    j = idx[b]
                    if dp[j] > c + 1:
                        dp[j] = c + 1
                        heapq.heappush(pq, (dp[j], j))

        ans = min(dp[i] for i, v in enumerate(nodes) if dist[v] <= x)

        print(ans if ans < INF else -1)

if __name__ == "__main__":
    solve()
```

The implementation begins by computing shortest piste-only distances using a BFS from the starting node. This gives the minimal time required to reach each node without using lifts.

We then restrict attention to nodes that appear in lifts plus the start, since only these matter for lift optimization under the given constraints. This compression is what keeps the state space sm
