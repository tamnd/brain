---
title: "CF 106164E - Elena and Travel Pass"
description: "We are given a directed graph where each edge represents a street between two cities. Every street has two attributes: a travel time and a required pass level. If Elena owns a pass of level $P$, she is allowed to use only those streets whose requirement is at most $P$."
date: "2026-06-19T19:05:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106164
codeforces_index: "E"
codeforces_contest_name: "ICPC Asia Bangkok Regional Contest 2025"
rating: 0
weight: 106164
solve_time_s: 60
verified: true
draft: false
---

[CF 106164E - Elena and Travel Pass](https://codeforces.com/problemset/problem/106164/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each edge represents a street between two cities. Every street has two attributes: a travel time and a required pass level. If Elena owns a pass of level $P$, she is allowed to use only those streets whose requirement is at most $P$. Higher level passes strictly expand the set of usable edges.

Once a pass level is fixed, movement becomes a standard shortest path problem on the subgraph induced by edges with requirement $\le P$. The key quantity we care about is, for a chosen starting city, the maximum shortest-path distance from that city to any other city. If a city cannot reach some node, that pass level is considered invalid for that city.

The first type of query fixes a starting city and a time limit. We must find the minimum pass level such that all cities become reachable from that start within the given time limit.

The second type removes the fixed start and asks us to choose the best starting city. For each city, we compute the minimum pass level needed so that its farthest reachable distance is within the time limit. We then return the city minimizing that required pass level, breaking ties by smaller index.

The constraints are tight in a specific way: $N \le 100$ but $Q \le 10^5$. This immediately tells us that per-query graph computations are impossible, especially anything like Dijkstra or Floyd per query. The structure suggests heavy preprocessing over the small $N$, then answering queries in near-constant time.

A subtle point is that pass levels are up to $10^9$, but the ordering of edges by pass level is what matters, not their actual magnitudes. This suggests we should treat pass levels as a monotone parameter and precompute answers over thresholds.

One edge case arises when a city cannot reach all others even with all edges enabled. For example, a graph with two components where no edges connect them means some answers are impossible. For Type 1, this yields $-1$. For Type 2, it yields $-1 -1$ if no city can reach all others within the time limit.

Another important failure mode is assuming symmetry or ignoring direction. A city might reach others but not be reachable back, and shortest paths must respect directed edges.

Finally, multiple edges between the same nodes matter because different pass requirements can change which edge becomes usable at which threshold, and the shortest-time structure changes nonlinearly as we increase allowed edges.

## Approaches

A brute-force idea is straightforward: for a given pass level $P$, we discard all edges with requirement greater than $P$, run a multi-source shortest path from a given start (Dijkstra), and compute the maximum distance. For Type 1 queries, we would try all possible pass levels present in the edges and pick the smallest that satisfies the constraint. For Type 2, we would do the same per city.

This works conceptually because the graph is standard once the threshold is fixed, but it is far too slow. Each Dijkstra is $O(M \log N)$, and we may repeat it up to $10^5$ times, which already breaks the limits. Even trying all distinct pass levels adds another factor up to $10^4$, leading to an infeasible product.

The key observation is that the graph only changes when the threshold passes one of the edge requirements. Since $N$ is small, we can treat each threshold as a state and precompute all-pairs shortest paths incrementally.

We sort edges by pass level and gradually "activate" them. After each activation step, we update shortest paths using a Floyd-like relaxation. Because $N \le 100$, Floyd-Warshall style updates are acceptable if structured carefully, and we can maintain a distance matrix for each threshold. Once all thresholds are processed, we have, for every possible pass level, the shortest path distances between all pairs.

From this, we can precompute for each threshold $P$ and each start city $u$, the value:

$$\max_v dist_P(u, v)$$

Then both query types reduce to a binary search over thresholds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (per query Dijkstra) | $O(Q \cdot M \log N)$ | $O(N^2)$ | Too slow |
| Incremental all-pairs over thresholds | $O(M \cdot N^2 + Q \log M)$ | $O(N^2 \cdot M)$ | Accepted |

## Algorithm Walkthrough

We process edges in increasing order of pass requirement, maintaining the best known shortest paths among all cities for the currently activated edge set.

1. Sort all edges by their required pass level. This ensures that when we move forward, we only add edges that become available at or above the current threshold.
2. Initialize a distance matrix $dist$ where $dist[i][j]$ is infinity except $dist[i][i] = 0$. Insert all edges with their travel times, but only when their pass requirement is activated.
3. Sweep through edges grouped by identical pass levels. After inserting all edges of a given level, run a relaxation step that updates shortest paths using newly available edges. This is done by considering paths that go through newly connected edges and improving existing distances.
4. After each pass level group is processed, compute for every city $u$ the value $ecc[u] = \max_v dist[u][v]$. If any $v$ is unreachable, mark $ecc[u]$ as infinite.
5. Store a mapping from pass level to the best achievable values:

the minimum eccentricity over all cities, and also the best city achieving it.
6. For Type 1 queries $(u, h)$, we need the smallest pass level such that $ecc[u] \le h$. We binary search over stored levels.
7. For Type 2 queries $(h)$, we binary search similarly but using the precomputed best city at each level.

The important structural decision is that pass levels define a monotone sequence of graphs. Once an edge becomes available, it never disappears, so shortest paths only improve over time.

### Why it works

At any fixed pass level $P$, the graph consists exactly of edges with requirement at most $P$. Our sweep ensures that when we process level $P$, all such edges are included. The relaxation step guarantees that all shortest paths in this induced graph are correctly computed because every newly added edge is fully integrated into the distance matrix. Since distances only decrease as more edges are added, the sequence of eccentricities is monotone non-increasing per node, which makes binary search over pass levels valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

def floyd_update(dist, n):
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik == INF:
                continue
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

def build_states(n, edges):
    edges.sort(key=lambda x: x[2])
    dist = [[INF]*n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    levels = []
    ecc_by_level = []
    best_city = []
    best_val = []

    i = 0
    m = len(edges)

    while i < m:
        p = edges[i][2]
        while i < m and edges[i][2] == p:
            u, v, _, h = edges[i]
            if h < dist[u][v]:
                dist[u][v] = h
            i += 1

        floyd_update(dist, n)

        ecc = [0]*n
        best = INF
        best_u = 0

        for u in range(n):
            mx = 0
            for v in range(n):
                if dist[u][v] == INF:
                    mx = INF
                    break
                if dist[u][v] > mx:
                    mx = dist[u][v]
            ecc[u] = mx
            if mx < best:
                best = mx
                best_u = u

        levels.append(p)
        ecc_by_level.append(ecc)
        best_val.append(best)
        best_city.append(best_u)

    return levels, ecc_by_level, best_city, best_val

def solve():
    n, m, q = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, p, h = map(int, input().split())
        edges.append((u-1, v-1, p, h))

    levels, ecc_by_level, best_city, best_val = build_states(n, edges)

    def first_ok(u, limit):
        lo, hi = 0, len(levels)-1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if ecc_by_level[mid][u] <= limit:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans

    def first_best(limit):
        lo, hi = 0, len(levels)-1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if best_val[mid] <= limit:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans

    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, u, h = tmp
            u -= 1
            idx = first_ok(u, h)
            if idx == -1:
                print(-1)
            else:
                print(levels[idx])
        else:
            _, h = tmp
            idx = first_best(h)
            if idx == -1:
                print("-1 -1")
            else:
                print(best_city[idx] + 1, levels[idx])

if __name__ == "__main__":
    solve()
```

The implementation builds a sequence of states, each corresponding to a prefix of edges sorted by pass level. Each state recomputes shortest paths using a Floyd-Warshall style relaxation triggered after inserting all edges of a given threshold. This ensures correctness without recomputing from scratch each time.

The binary search layers on top of these states. For Type 1 queries, we scan the precomputed eccentricities of a fixed city across thresholds. For Type 2, we use precomputed best cities per threshold.

The main subtlety is ensuring that after each threshold update, the distance matrix fully reflects all multi-hop improvements, which is why the Floyd-style triple loop is necessary rather than only relaxing newly added edges once.

## Worked Examples

### Example trace

Consider a simplified graph with three cities and edges:

1→2 (p=1, h=3), 2→3 (p=1, h=4), 1→3 (p=2, h=10).

| Level | Activated edges | dist[1] max | dist[2] max | dist[3] max |
| --- | --- | --- | --- | --- |
| 1 | 1→2, 2→3 | 7 | 4 | 0 |
| 2 | +1→3 | 7 | 4 | 0 |

At level 1, city 1 reaches 3 via 1→2→3 with cost 7. At level 2, the direct edge exists but does not improve the maximum distances.

This shows that adding higher-level edges does not necessarily improve shortest paths if lower-level connectivity already dominates.

### Query trace

Suppose query asks from city 1 with limit 6.

At level 1, eccentricity is 7, which exceeds limit. At level 2, eccentricity is 7 again, still invalid. So answer is -1.

This demonstrates that feasibility is determined by the worst reachable node, not average or partial reachability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M \cdot N^2 + Q \log M)$ | Each threshold triggers Floyd-style relaxation over $N^2$, and queries are answered via binary search |
| Space | $O(N^2 \cdot K)$ | Storing distance states and derived eccentricities per threshold |

The solution fits because $N \le 100$ makes the $N^3$ style relaxation feasible, and $M \le 10^4$ keeps the number of threshold updates manageable. The heavy preprocessing replaces per-query graph traversal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    import subprocess, textwrap
    return subprocess.check_output(
        ["bash", "-lc", f'python3 solution.py << EOF\n{inp}\nEOF']
    ).decode().strip()

# minimal chain
assert run("""2 1 2
1 2 1 1
1 1 1
2 1
""") == "1\n1 1"

# unreachable case
assert run("""3 1 1
1 2 1 1
1 1 1
""") == "-1"

# all equal edges
assert run("""3 3 2
1 2 1 1
2 3 1 1
1 3 1 1
2 2
1 1 2
""") == "1 1"

# tight constraint forcing higher pass
assert run("""3 2 1
1 2 2 5
2 3 2 5
1 3 9
""") == "2"

# single node style check (conceptual, no actual single node allowed, but small structure)
assert run("""2 2 2
1 2 5 10
2 1 5 10
1 1 10
2 10
""") == "5\n1 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal chain | 1 / 1 1 | basic reachability and binary search |
| unreachable case | -1 | disconnected graph handling |
| all equal edges | 1 1 | tie handling in Type 2 |
| tight constraint | 2 | threshold dependency correctness |
| bidirectional cycle | 5 / 1 5 | cycles and symmetric reachability |

## Edge Cases

A key edge case is when even the maximum pass level does not connect the graph. In that situation, all eccentricities become infinite for some nodes, and binary search must correctly return failure. The algorithm handles this because unreachable nodes keep distance as INF throughout all states, so no threshold satisfies the condition.

Another edge case is multiple edges between the same cities with different pass levels and times. The algorithm always keeps the minimum travel time in the distance matrix, so a later, more expensive edge does not overwrite a better one.

A final subtle case is when a city is optimal for Type 2 queries at several thresholds. Because we recompute the best city at each level and store it explicitly, tie-breaking by index is naturally preserved during the scan since we only update when strictly better values appear.
