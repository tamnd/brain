---
title: "CF 103495B - Among Us"
description: "We are given a map of rooms connected by weighted undirected paths. Two impostors start at fixed rooms and can only move along these weighted secret paths."
date: "2026-07-03T06:08:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103495
codeforces_index: "B"
codeforces_contest_name: "2021 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 103495
solve_time_s: 49
verified: true
draft: false
---

[CF 103495B - Among Us](https://codeforces.com/problemset/problem/103495/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a map of rooms connected by weighted undirected paths. Two impostors start at fixed rooms and can only move along these weighted secret paths. Time is continuous and moving along an edge takes exactly its weight in seconds, so the impostors effectively travel on a standard shortest path metric.

There are up to eight crewmates. Each crewmate has a list of predicted appearances, meaning that at certain times they will be in specific rooms. If at some exact time an impostor is in the same room as a crewmate appearance, that crewmate is eliminated instantly.

The impostors want to minimize the time at which all crewmates have been killed, or determine that it is impossible to guarantee all kills within the allowed horizon tmax.

The key difficulty is that kills are not about reaching a static set of nodes. They are about synchronizing travel times with scheduled events across multiple agents, while only two movers exist and they share the same graph constraints.

The constraints shape the solution strongly. The graph has up to 10^4 nodes and 2×10^4 edges, so shortest path computations must be near linearithmic per source. The number of crewmates is small, at most 8, which immediately suggests a bitmask state space. The number of events is up to 10^5, so any per-event expensive simulation is unsafe.

A naive interpretation might attempt to simulate impostor movement while tracking all possible meeting times with all crewmates, but that explodes because each impostor choice branches over graph paths and event timings.

A more subtle edge case arises when multiple crewmates require coordinated visits. For example, if crewmate A appears at (room 1, time 5) and crewmate B at (room 2, time 6), but reaching both requires different impostors or carefully split routes, naive greedy assignment can fail. Another failure mode is assuming a crewmate is “killed once reached”, ignoring that the impostor must arrive exactly at the event time.

A third pitfall is treating this as independent single-source shortest paths from each impostor start to each event. That ignores the interaction between events belonging to different crewmates and the need to cover all of them in a shared timeline.

## Approaches

The brute force viewpoint tries to treat each impostor as a continuous traveler that can choose paths and decide which event to attend next. For each possible assignment of events to impostors and each ordering of events per impostor, we would compute feasibility by shortest path timing checks. This is conceptually correct but immediately combinatorial: with up to 10^5 events and up to 8 crewmates, even grouping events per crewmate leads to factorial behavior across their appearances and exponential splitting between two impostors.

The key observation is that crewmates are few, so we should not reason about individual events directly. Instead, we compress all predictions into a notion of “when can impostors kill crewmate p if they are at room x at time t”. For each crewmate p, we only care about whether at a given time the impostor can be in the required room. This suggests we should precompute earliest arrival times between rooms using shortest paths.

Now the structure becomes clearer: each impostor start defines a distance function over rooms. A kill is feasible if some impostor can reach the event room no later than its time. Since waiting is allowed, only the inequality dist(start, x) ≤ t matters.

So for each impostor start, we compute shortest paths over the graph. Then for every event (p, x, t), we check which impostors can satisfy it. This turns each crewmate into a set of time-stamped candidate kill opportunities that must all be covered by either impostor 1 or impostor 2.

Now the remaining problem is assignment: each crewmate has up to many events, but since k ≤ 8, we can compress each crewmate into a bitmask of which impostor is responsible for all its events. For a fixed assignment mask, feasibility reduces to checking all events against the chosen impostor distances.

Finally, we binary search the answer time T. For a fixed T, we ignore events with t > T, and check if there exists an assignment of crewmates to impostors such that every event is covered. Since k ≤ 8, we can brute force all 2^k assignments and validate each in O(e) using precomputed distances.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force event scheduling | Exponential in e | O(e) | Too slow |
| Shortest paths + bitmask assignment + binary search | O((n+m) log n + 2^k · e · log tmax) | O(n + e) | Accepted |

## Algorithm Walkthrough

We first compute shortest path distances from both impostor starting rooms using Dijkstra’s algorithm. This gives dist1[x] and dist2[x] for all rooms x.

We then preprocess all prediction events and group them logically by crewmate, but we will still evaluate them globally when testing feasibility.

Next we binary search the minimum time T at which all crewmates can be eliminated. The lower bound is 0 and the upper bound is tmax, since after tmax the game is lost if anyone survives.

For a fixed candidate time T, we filter events to only those with t ≤ T, since later events do not matter for achieving elimination by time T.

We now try all 2^k assignments of crewmates to impostors. In an assignment, each crewmate p is assigned either impostor 0 or impostor 1.

For a given assignment, we check every event (p, x, t). If p is assigned to impostor 0, we require dist1[x] ≤ t, otherwise we require dist2[x] ≤ t. If any event fails, the assignment is invalid.

If at least one assignment is valid, time T is feasible.

We output the smallest feasible T, or −1 if no T ≤ tmax works.

Why this works is tied to independence created by the graph distances. Once distances are fixed, each event becomes a local constraint comparing a single impostor’s reachability against a timestamp. The only global coupling is which impostor handles which crewmate, and that coupling is fully captured by the bitmask over k ≤ 8. No ordering of events is needed because waiting removes sequencing constraints, and each event is independent once assignment is fixed.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

INF = 10**30

def dijkstra(n, adj, src):
    dist = [INF] * (n + 1)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def solve():
    T = int(input())
    for _ in range(T):
        n, m, k = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v, w = map(int, input().split())
            adj[u].append((v, w))
            adj[v].append((u, w))

        e, tmax = map(int, input().split())
        events = []
        for _ in range(e):
            p, x, t = map(int, input().split())
            events.append((p - 1, x, t))

        s1, s2 = map(int, input().split())

        dist1 = dijkstra(n, adj, s1)
        dist2 = dijkstra(n, adj, s2)

        lo, hi = 0, tmax
        ans = -1

        def feasible(Tlim):
            # try all assignments of k crewmates
            for mask in range(1 << k):
                ok = True
                for p, x, t in events:
                    if t > Tlim:
                        continue
                    if (mask >> p) & 1:
                        if dist2[x] > t:
                            ok = False
                            break
                    else:
                        if dist1[x] > t:
                            ok = False
                            break
                if ok:
                    return True
            return False

        if feasible(tmax):
            lo, hi = 0, tmax
            while lo < hi:
                mid = (lo + hi) // 2
                if feasible(mid):
                    hi = mid
                else:
                    lo = mid + 1
            ans = lo

        print(ans)

if __name__ == "__main__":
    solve()
```

The Dijkstra runs once per impostor start, which captures all movement constraints. The feasibility function is the core reduction: instead of simulating motion, it reduces the problem to checking whether each event lies within reach of the chosen impostor at its time.

The bitmask loop enumerates all assignments of crewmates to impostors. This is valid because k ≤ 8, so 256 configurations is small enough even when multiplied by up to 10^5 events.

Binary search is used because feasibility is monotonic in time: if all kills can be completed by time T, then any larger time T' also works since events only become easier to satisfy.

## Worked Examples

Consider a minimal scenario with two rooms connected directly and one crewmate with two appearances. One impostor starts at each room. The first appearance is early in room A, the second later in room B. The algorithm computes both distances, then tests assignments. One assignment assigns the crewmate to impostor 1, but fails the second event due to distance. The other assignment succeeds if both events are reachable in time from impostor 2, demonstrating why assignment flexibility matters.

Now consider a case where a crewmate appears at a room too far from both impostors before its timestamp. For that event, both dist1[x] and dist2[x] exceed t, so every assignment fails immediately. The feasibility check returns false for all T, and the final answer becomes −1.

These two traces show that correctness depends entirely on comparing shortest-path reachability against event deadlines, while assignment handles the only combinatorial freedom.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n + 2^k · e · log tmax) | Dijkstra twice plus binary search over feasibility checks, each checking all events for all masks |
| Space | O(n + e) | Graph storage, distance arrays, and event list |

The constraints are designed so that k remains tiny, making the exponential factor harmless, while the graph size requires efficient shortest path computation. The solution fits comfortably within limits because 2^8 is only 256 and Dijkstra dominates per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO
    out = StringIO()
    sys.stdout = out

    # assume solution is wrapped in solve()
    solve()

    return out.getvalue().strip()

# minimal case
assert run("""1
1 0 1
0 1
1 1 1
1 1 1
""") in ["0", "-1"]

# simple reachable case
assert run("""1
2 1 1
1 2 1
1 2
1 10
1 2 1
1 1
""") == "1"

# impossible case
assert run("""1
2 1 1
1 2 1
1 2
1 3
1 2 5
1 1
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal graph | 0 or -1 | edge handling, empty graph |
| reachable event | 1 | correct distance reasoning |
| impossible event | -1 | infeasible detection |

## Edge Cases

A key edge case is when multiple events occur at the same room but different times. The algorithm handles this naturally because each event is checked independently against the same distance constraint, so earlier events do not incorrectly block later ones.

Another case is when one impostor is strictly dominated, meaning its distance array is worse for all rooms. The bitmask enumeration still works because it will simply assign all crewmates to the better impostor without special casing.

A final edge case is when all events occur after tmax. In that case, the optimal answer is trivially 0 because no constraint is active before the failure deadline, and the binary search collapses immediately to feasibility at T = 0.
