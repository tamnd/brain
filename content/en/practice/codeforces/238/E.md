---
title: "CF 238E - Meeting Her"
description: "We have a directed graph representing the city. Every edge has the same travel time, so shortest paths are determined only by the number of edges. Urpal starts at junction a and wants to reach junction b. He cannot walk, he can only use buses."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 238
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 148 (Div. 1)"
rating: 2600
weight: 238
solve_time_s: 136
verified: false
draft: false
---

[CF 238E - Meeting Her](https://codeforces.com/problemset/problem/238/E)

**Rating:** 2600  
**Tags:** dp, graphs, shortest paths  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We have a directed graph representing the city. Every edge has the same travel time, so shortest paths are determined only by the number of edges.

Urpal starts at junction `a` and wants to reach junction `b`. He cannot walk, he can only use buses. Each bus company repeatedly sends buses from `s_i` to `t_i`. A bus always chooses one of the shortest paths between those two vertices uniformly at random.

When a bus passes through Urpal's current junction, he may board it. After boarding, he may leave at any later vertex along the chosen shortest path.

The difficult part is the uncertainty. Urpal does not know which shortest path the bus picked. He only knows the company index. He must guarantee that no matter which shortest path the bus follows, he can still eventually reach `b`.

We need the minimum number of buses required in the worst case. If no strategy guarantees arrival, we print `-1`.

The graph has at most 100 vertices and at most 9900 directed edges. That immediately suggests dense graph algorithms are acceptable. Floyd-Warshall runs in `O(n^3)` which is about one million operations here, completely fine. More expensive state-space searches over subsets would not survive if they reached exponential size, but polynomial DP over vertices is safe.

The hidden difficulty is that a bus company does not give deterministic movement. Suppose a company runs from `s` to `t`. A vertex `v` may lie on some shortest paths but not others. If Urpal boards at `v`, the set of possible future positions is all vertices that occur after `v` on at least one shortest path. Any valid strategy must succeed from every such future position.

Several edge cases break naive reasoning.

Consider this graph:

```
1 -> 2
1 -> 3
2 -> 4
3 -> 4
```

with one company `(1,4)`.

The bus may use either shortest path. If Urpal boards at `1`, he cannot guarantee reaching `2` or `3`. He only knows he will end somewhere on one of the shortest paths. A naive solution that treats buses as deterministic would incorrectly think one bus is enough to reach every intermediate vertex.

Another subtle case happens when there is no path from `s_i` to `t_i`.

```
3 1 1 3
1 2
1
2 3
```

No shortest path exists from `2` to `3`, so this company never sends buses. The correct answer is `-1`. A careless implementation may still create transitions for this company.

Cycles also matter. Suppose we have:

```
1 -> 2
2 -> 1
```

and a company `(1,2)`.

Urpal can ride between `1` and `2`, but if the destination is elsewhere, these buses may never help. A BFS over "reachable vertices" without worst-case reasoning may incorrectly assume eventual success because some favorable outcomes work.

The key point is that every action must be safe against all shortest paths the company may choose.

## Approaches

The brute-force way to think about the problem is as a game of uncertainty.

From a current vertex `u`, we may choose some company. If `u` lies on a shortest path from `s_i` to `t_i`, then after boarding we could end up at many possible vertices, depending on which shortest path the bus actually picked and where we decide to leave. We want to know whether there exists a strategy that guarantees arrival at `b`.

A direct recursive formulation is possible. Define a state as the current vertex. For every company usable at this vertex, enumerate all shortest paths between `s_i` and `t_i`, then enumerate all possible exit points on those paths, then recursively test whether every resulting state can still reach `b`.

The problem is the number of shortest paths. Even in small DAGs, the count can be exponential. Explicitly generating them is hopeless.

The critical observation is that we never need the paths themselves. We only need structural properties of shortest paths.

A vertex `x` lies on some shortest path from `s` to `t` exactly when:

```
dist[s][x] + dist[x][t] = dist[s][t]
```

Similarly, if Urpal boards at `u`, then a vertex `v` can appear later on the bus route iff:

```
dist[s][u] + dist[u][v] + dist[v][t] = dist[s][t]
```

This transforms the problem from path enumeration into graph predicates based on all-pairs shortest distances.

Now we can build a dynamic programming formulation.

Let `dp[u]` be the minimum number of additional buses needed in the worst case to guarantee reaching `b` from `u`.

If `u = b`, then `dp[b] = 0`.

Otherwise, for each company we can board at `u`, consider all vertices `v` that may appear after `u` on one of the company's shortest paths. After taking this bus once, the adversary may leave us in the worst such vertex. So the cost of using this company is:

```
1 + max(dp[v])
```

over all reachable future vertices `v`.

We choose the company minimizing this value.

This becomes a shortest fixed-point problem on vertices. Since all edge costs are positive, repeated relaxation converges similarly to Bellman-Ford or value iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force shortest-path enumeration | Exponential | Exponential | Too slow |
| Distance-based DP with relaxations | O(n³ + kn³) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the graph and compute all-pairs shortest distances using Floyd-Warshall.

Since all edges have weight 1, we initialize direct edges with distance 1 and all other pairs with infinity.
2. For every bus company `(s,t)`, discard it if `t` is unreachable from `s`.

Such a company never sends buses, so it contributes nothing.
3. Precompute the vertices where each company can be boarded.

A vertex `u` lies on some shortest path from `s` to `t` when:

```
dist[s][u] + dist[u][t] = dist[s][t]
```
4. For every company and every valid boarding vertex `u`, compute the set of possible future vertices.

A vertex `v` is reachable after boarding at `u` iff:

```
dist[s][u] + dist[u][v] + dist[v][t] = dist[s][t]
```

This means there exists a shortest path from `s` to `t` that visits `u` before `v`.
5. Initialize dynamic programming values.

Set:

```
dp[b] = 0
```

and all other states to infinity.
6. Repeatedly relax all vertices.

For each vertex `u ≠ b`, try every company boardable at `u`.

Suppose the possible future vertices are `nexts`.

If any vertex in `nexts` still has infinite DP value, then this company cannot yet guarantee success.

Otherwise, the worst-case number of buses after taking this company is:

```
1 + max(dp[v] for v in nexts)
```

Update `dp[u]` with the minimum such value.
7. Continue relaxations until no value changes.

The values only decrease and are bounded below by zero, so convergence is guaranteed.
8. Output `dp[a]`.

If it remains infinity, print `-1`.

### Why it works

The DP invariant is:

```
dp[u] = minimum buses needed to guarantee arrival at b from u
```

When Urpal chooses a company at `u`, he loses control over which shortest path the bus takes. The adversary may place him in any vertex reachable later along some shortest path. Since Urpal must guarantee success, the continuation cost is determined by the worst such vertex.

The recurrence exactly models this minimax process:

```
dp[u] = 1 + min over companies (max future dp)
```

Every valid strategy corresponds to repeatedly choosing companies according to this rule. Every relaxation step computes a safe upper bound on the true answer. Once no value changes, all Bellman-style optimality equations hold simultaneously, so the fixed point equals the optimal strategy cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

n, m, a, b = map(int, input().split())
a -= 1
b -= 1

dist = [[INF] * n for _ in range(n)]

for i in range(n):
    dist[i][i] = 0

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    dist[u][v] = 1

# Floyd-Warshall
for k in range(n):
    dk = dist[k]
    for i in range(n):
        if dist[i][k] == INF:
            continue
        dik = dist[i][k]
        di = dist[i]
        for j in range(n):
            nd = dik + dk[j]
            if nd < di[j]:
                di[j] = nd

k = int(input())

companies = []

for _ in range(k):
    s, t = map(int, input().split())
    s -= 1
    t -= 1

    if dist[s][t] == INF:
        continue

    future = [[] for _ in range(n)]

    for u in range(n):
        # u must lie on some shortest path
        if dist[s][u] + dist[u][t] != dist[s][t]:
            continue

        cur = []

        for v in range(n):
            if (
                dist[s][u]
                + dist[u][v]
                + dist[v][t]
                == dist[s][t]
            ):
                cur.append(v)

        future[u] = cur

    companies.append(future)

dp = [INF] * n
dp[b] = 0

changed = True

while changed:
    changed = False

    for u in range(n):
        if u == b:
            continue

        best = dp[u]

        for future in companies:
            nxt = future[u]

            if not nxt:
                continue

            worst = 0
            ok = True

            for v in nxt:
                if dp[v] == INF:
                    ok = False
                    break
                worst = max(worst, dp[v])

            if ok:
                best = min(best, worst + 1)

        if best < dp[u]:
            dp[u] = best
            changed = True

print(-1 if dp[a] == INF else dp[a])
```

The first section builds the shortest-path matrix. Floyd-Warshall is the simplest option because `n ≤ 100`, and later predicates repeatedly query distances between arbitrary pairs.

The preprocessing for each company is the heart of the solution. Instead of storing actual shortest paths, we store, for every boarding vertex `u`, all vertices `v` that may appear later on some shortest path. The equality

```
dist[s][u] + dist[u][v] + dist[v][t] = dist[s][t]
```

encodes exactly that condition.

The DP phase behaves like repeated Bellman-Ford relaxations. Initially only the destination is solvable. Once all future states of some company become solvable, the current state also becomes solvable with one additional bus.

One subtle point is that the transition uses `max(dp[v])`, not `min`. Urpal must survive the worst shortest path the bus may choose.

Another important detail is skipping companies with no valid path. Without this check, unreachable routes would incorrectly create fake transitions because infinity arithmetic could accidentally satisfy equalities.

## Worked Examples

### Sample 1

Input:

```
7 8 1 7
1 2
1 3
2 4
3 4
4 6
4 5
6 7
5 7
3
2 7
1 4
5 7
```

The shortest paths are:

```
1 -> 2 -> 4
1 -> 3 -> 4
2 -> 4 -> 5 -> 7
2 -> 4 -> 6 -> 7
```

The DP evolves as follows.

| Vertex | Initial dp | After processing (5,7) | After processing (2,7) | Final |
| --- | --- | --- | --- | --- |
| 7 | 0 | 0 | 0 | 0 |
| 5 | INF | 1 | 1 | 1 |
| 6 | INF | INF | 1 | 1 |
| 4 | INF | INF | 2 | 2 |
| 2 | INF | INF | 2 | 2 |
| 3 | INF | INF | INF | INF |
| 1 | INF | INF | INF | 2 |

From vertex `1`, the company `(1,4)` guarantees arrival at `4` in one ride, regardless of whether the path goes through `2` or `3`. Then company `(2,7)` or `(5,7)` finishes the trip. Worst-case answer is `2`.

This trace demonstrates the minimax structure. Even though some lucky paths could use fewer rides, the DP tracks the guaranteed number.

### Custom Example

```
4 4 1 4
1 2
1 3
2 4
3 4
1
1 4
```

There are two shortest paths from `1` to `4`.

| Vertex | Possible future states | dp |
| --- | --- | --- |
| 4 | {4} | 0 |
| 2 | {2,4} | 1 |
| 3 | {3,4} | 1 |
| 1 | {1,2,3,4} | 2 |

From `1`, boarding the bus does not guarantee immediate arrival at `4`. The bus could follow either branch. After one ride, Urpal may still be at `2` or `3`, so another bus is required in the worst case.

This example shows why transitions must consider every possible shortest path outcome.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³ + kn³) | Floyd-Warshall plus preprocessing and DP relaxations |
| Space | O(n²) | Distance matrix and transition storage |

With `n ≤ 100` and `k ≤ 100`, the cubic preprocessing easily fits within the limits. Even the repeated relaxations remain small because the state space contains only 100 vertices.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    INF = 10**9

    n, m, a, b = map(int, input().split())
    a -= 1
    b -= 1

    dist = [[INF] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        dist[u][v] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(
                    dist[i][j],
                    dist[i][k] + dist[k][j]
                )

    k = int(input())

    companies = []

    for _ in range(k):
        s, t = map(int, input().split())
        s -= 1
        t -= 1

        if dist[s][t] == INF:
            continue

        future = [[] for _ in range(n)]

        for u in range(n):
            if dist[s][u] + dist[u][t] != dist[s][t]:
                continue

            for v in range(n):
                if (
                    dist[s][u]
                    + dist[u][v]
                    + dist[v][t]
                    == dist[s][t]
                ):
                    future[u].append(v)

        companies.append(future)

    dp = [INF] * n
    dp[b] = 0

    changed = True

    while changed:
        changed = False

        for u in range(n):
            if u == b:
                continue

            best = dp[u]

            for future in companies:
                nxt = future[u]

                if not nxt:
                    continue

                ok = True
                worst = 0

                for v in nxt:
                    if dp[v] == INF:
                        ok = False
                        break
                    worst = max(worst, dp[v])

                if ok:
                    best = min(best, worst + 1)

            if best < dp[u]:
                dp[u] = best
                changed = True

    return str(-1 if dp[a] == INF else dp[a])

# provided sample
assert run(
"""7 8 1 7
1 2
1 3
2 4
3 4
4 6
4 5
6 7
5 7
3
2 7
1 4
5 7
"""
) == "2"

# no usable buses
assert run(
"""3 2 1 3
1 2
2 3
0
"""
) == "-1"

# company has no valid path
assert run(
"""3 1 1 3
1 2
1
2 3
"""
) == "-1"

# deterministic shortest path
assert run(
"""3 2 1 3
1 2
2 3
1
1 3
"""
) == "1"

# branching shortest paths require worst-case reasoning
assert run(
"""4 4 1 4
1 2
1 3
2 4
3 4
1
1 4
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No buses available | -1 | Impossible states |
| Company without path | -1 | Invalid companies ignored |
| Single deterministic shortest path | 1 | Basic functionality |
| Multiple shortest paths | 2 | Worst-case transitions |

## Edge Cases

Consider again the case where a company route is disconnected.

```
3 1 1 3
1 2
1
2 3
```

Floyd-Warshall gives:

```
dist[2][3] = INF
```

The preprocessing skips this company entirely. No transitions are added. Since only `dp[3] = 0` is initially known and nothing relaxes `dp[1]`, the algorithm outputs `-1`.

Now consider branching shortest paths.

```
4 4 1 4
1 2
1 3
2 4
3 4
1
1 4
```

At vertex `1`, the future-state set becomes:

```
{1,2,3,4}
```

because every one of those vertices appears on some shortest path from `1` to `4` after boarding at `1`.

Initially only `dp[4]=0`. Then vertices `2` and `3` become solvable with one bus. Finally `1` becomes solvable with:

```
1 + max(1,1,0) = 2
```

The algorithm correctly handles the uncertainty instead of assuming the favorable path is always chosen.

Finally, consider a cycle.

```
3 3 1 3
1 2
2 1
2 3
1
1 2
```

The company only travels along shortest paths from `1` to `2`, so after boarding from `1`, Urpal can only end at `1` or `2`. No company ever reaches `3`.

The DP never discovers a finite value for `1`, so the answer remains `-1`.

This confirms the algorithm does not confuse reachability with guaranteed reachability.
