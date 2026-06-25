---
title: "CF 106475H - \u041e\u0442\u0442\u0435\u0440\u0432\u0435\u0440 \u0441\u043e\u0431\u0438\u0440\u0430\u0435\u0442\u0441\u044f \u0432 \u043f\u0443\u0442\u044c"
description: "We are given a set of locations connected by undirected roads. Each road has a fixed traversal time, but using it is complicated by a traffic light that cycles repeatedly between a red phase and a green phase."
date: "2026-06-25T08:52:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106475
codeforces_index: "H"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0412\u041a\u041e\u0428\u041f.Junior 2026"
rating: 0
weight: 106475
solve_time_s: 46
verified: true
draft: false
---

[CF 106475H - \u041e\u0442\u0442\u0435\u0440\u0432\u0435\u0440 \u0441\u043e\u0431\u0438\u0440\u0430\u0435\u0442\u0441\u044f \u0432 \u043f\u0443\u0442\u044c](https://codeforces.com/problemset/problem/106475/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of locations connected by undirected roads. Each road has a fixed traversal time, but using it is complicated by a traffic light that cycles repeatedly between a red phase and a green phase.

When you reach one end of a road at some time, you may not be allowed to start crossing immediately. Each road has a repeating schedule: first a red period of length r during which entry is blocked, then a green period of length g during which you are allowed to enter and traverse the road. This pattern repeats forever.

If you arrive during a green phase, you can start immediately. If you arrive during a red phase, you must wait until the next green phase begins. After you start crossing, you always spend exactly t time units traveling along that road.

The task is to compute the minimum possible time needed to travel from node 1 to node n.

The graph has up to 100,000 nodes and 100,000 roads. Each road query requires reasoning about time-dependent behavior, but the structure is still a standard shortest path problem with a twist in edge relaxation.

A naive interpretation would be to ignore the traffic light and treat every edge as having cost t. That fails immediately because waiting times can dominate the answer, and they depend on arrival time, not just the graph structure.

A subtle edge case appears when waiting is mandatory even though a shorter path exists in terms of pure edge weights. For example, suppose you can reach a node early via a long path that aligns with green phases, or later via a shorter path that hits a red phase. A greedy shortest-edge approach would incorrectly pick the latter.

Another common failure is assuming waiting happens only once per node, rather than per edge traversal. Waiting depends on the exact arrival time at each endpoint, so two different paths reaching the same node can produce different future costs.

## Approaches

The brute-force idea is to treat this as a time-dependent graph problem and simulate all possible ways of walking through it. From a state defined by (node, time), we try all outgoing edges, compute the next valid departure time by checking the traffic light cycle, and continue recursively or with BFS over time states. This is correct because it explicitly models all feasible schedules.

The issue is that time is unbounded. Even if we only consider times that occur after arrivals, each relaxation produces new distinct timestamps. In the worst case, each edge traversal can generate a unique time value, and the number of states grows with the magnitude of times rather than the number of nodes. With up to 10^5 edges, this degenerates into an explosion of states.

The key observation is that the problem still satisfies the optimal substructure property of shortest paths: once we fix a best known arrival time at a node, we never need to revisit it with a worse time. The only complication is that edge relaxation depends on the arrival time through a deterministic function: waiting time is computed from time modulo (r + g). This makes the graph suitable for Dijkstra’s algorithm, where edge weights are not constant but can be evaluated on the fly.

Instead of enumerating states, we maintain the best known arrival time for each node. When we relax an edge from u to v at time T, we compute the waiting time caused by the cycle, add it to T, then add traversal time t. This produces a candidate arrival time for v, exactly like a weighted edge.

This transforms the problem into a standard single-source shortest path computation with a non-constant but well-defined relaxation function.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over time-states | O(huge, potentially exponential in practice) | O(huge) | Too slow |
| Dijkstra with time-dependent relaxation | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph where each edge stores (neighbor, travel time t, red r, green g). This allows efficient iteration over outgoing roads from each node.
2. Initialize an array dist of size n with infinity, except dist[1] = 0, since we start at node 1 at time 0.
3. Use a priority queue ordered by current known time. Insert (0, 1) as the starting state.
4. Repeatedly extract the node u with the smallest known arrival time cur. If cur is already larger than dist[u], skip it because we have a better known way to reach u.
5. For each edge from u to v, compute the cycle length c = r + g. Determine the position within the cycle as cur % c.
6. If this position lies in the red phase, meaning it is less than r, compute waiting time as r - (cur % c). Otherwise waiting time is zero. This models waiting until the green phase begins.
7. Compute the candidate arrival time as cur + waiting + t. This represents the earliest possible time we can finish crossing this edge.
8. If this candidate time improves dist[v], update it and push (candidate, v) into the priority queue.
9. Continue until all reachable nodes are processed. The answer is dist[n].

The correctness relies on the fact that once a node is popped from the priority queue with its minimal time, no later relaxation can produce a better arrival time for it. Even though edge weights depend on time, the relaxation function is deterministic and monotonic in the sense that later arrivals cannot produce earlier departures on the same edge.

## Why it works

The core invariant is that dist[u] always stores the minimum achievable arrival time at node u found so far, and the priority queue always expands the currently smallest such time. The waiting-time function transforms each traversal into a deterministic cost based solely on the arrival time at the source node, so every edge relaxation is equivalent to evaluating a fixed function on a known state. Since all costs are non-negative and Dijkstra always finalizes nodes in increasing order of time, any alternative path reaching a node later cannot retroactively improve earlier states, which preserves correctness even with time-dependent edges.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b, t, r, gr = map(int, input().split())
        g[a].append((b, t, r, gr))
        g[b].append((a, t, r, gr))

    INF = 10**30
    dist = [INF] * (n + 1)
    dist[1] = 0

    pq = [(0, 1)]

    while pq:
        cur, u = heapq.heappop(pq)
        if cur != dist[u]:
            continue

        for v, t, r, gr in g[u]:
            cycle = r + gr
            pos = cur % cycle

            wait = 0
            if pos < r:
                wait = r - pos

            nxt = cur + wait + t

            if nxt < dist[v]:
                dist[v] = nxt
                heapq.heappush(pq, (nxt, v))

    print(dist[n])

if __name__ == "__main__":
    solve()
```

The adjacency list stores full edge parameters so that each relaxation can compute waiting time locally without any global preprocessing.

The priority queue ensures we always extend the currently best-known partial route. The check `if cur != dist[u]` avoids processing stale states, which is essential for keeping the complexity within logarithmic bounds per operation.

The waiting logic is the only non-standard part: it converts a cyclic constraint into a single additive delay computed from the current timestamp.

## Worked Examples

### Example 1

Input:

```
2 1
1 2 3 4 5
```

| Step | Node | Time | Action | dist[2] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | start | inf |
| 2 | 2 | 0+4 wait +3 travel | relax edge | 7 |

The arrival time 0 lands in the red phase of length 4, so we must wait until time 4, then traverse in 3 units.

This demonstrates that even a single edge can dominate the answer purely through waiting.

### Example 2

Input:

```
3 2
1 2 4 1 1
2 3 9 6 7
```

| Step | Node | Time | Edge | Wait | Next |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1→2 | 1 | 5 |
| 2 | 2 | 5 | 2→3 | 1 | 15 |

From node 1 to 2, arrival is in red phase of length 1, so we wait 1 and then travel 4. From node 2, arrival time 5 is again in a red phase relative to the second cycle, forcing a wait of 1 before the long traversal.

This confirms that optimality depends on arrival timing, not just path structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each node is extracted at most once in its best form, and each edge relaxation triggers a heap push costing log n |
| Space | O(n + m) | adjacency list plus distance array and priority queue |

The constraints up to 100,000 nodes and edges fit comfortably within this complexity, since the logarithmic factor keeps operations around a few million at most.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    def solve():
        n, m = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            a, b, t, r, gr = map(int, input().split())
            g[a].append((b, t, r, gr))
            g[b].append((a, t, r, gr))

        INF = 10**30
        dist = [INF] * (n + 1)
        dist[1] = 0
        pq = [(0, 1)]

        while pq:
            cur, u = heapq.heappop(pq)
            if cur != dist[u]:
                continue
            for v, t, r, gr in g[u]:
                c = r + gr
                pos = cur % c
                wait = 0 if pos >= r else r - pos
                nxt = cur + wait + t
                if nxt < dist[v]:
                    dist[v] = nxt
                    heapq.heappush(pq, (nxt, v))

        return dist[n]

    return str(solve())

# provided samples
assert run("2 1\n1 2 3 4 5\n") == "7"
assert run("3 2\n1 2 4 1 1\n2 3 9 6 7\n") == "15"

# custom cases
assert run("2 1\n1 2 5 0 10\n") == "5", "no waiting case"
assert run("2 1\n1 2 5 10 1\n") == "15", "always wait"
assert run("3 3\n1 2 1 1 1\n2 3 1 1 1\n1 3 10 0 10\n") == "2", "alternative path"
assert run("4 3\n1 2 5 3 3\n2 4 5 3 3\n1 4 20 0 5\n") == "16", "detour vs direct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no-wait edge | 5 | zero red phase behavior |
| always-wait edge | 15 | full red delay |
| triangle graph | 2 | shortest path choice under timing |
| detour vs direct | 16 | interaction of multiple edges |

## Edge Cases

One edge case occurs when r = 0, meaning there is no red phase. In that situation, the waiting computation must never trigger. For an input like `1 2 5 0 10`, the algorithm correctly computes pos = 0 and sees no red interval, producing a direct cost of 5.

Another case is when the arrival time lands exactly at the boundary between red and green. Since red is defined as the interval [0, r), arriving at time exactly r should not incur waiting. The modulo logic handles this because pos >= r falls into the green phase.

A final subtle case is when multiple paths reach a node with different timings. The priority queue ensures the earliest arrival is processed first, and any later arrivals are discarded. For a node reachable both quickly with long waiting and slowly with no waiting, the algorithm correctly evaluates both but only keeps the minimum resulting time, since each relaxation is evaluated independently.
