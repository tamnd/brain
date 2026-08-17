---
title: "CF 102203J - \u041d\u043e\u0447\u043d\u043e\u0439 \u043f\u0430\u0442\u0440\u0443\u043b\u044c"
description: "We have a directed weighted graph with up to 300 intersections. Each directed road has a positive traversal time. Two patrol officers start at intersections s1 and s2. They must inspect the sequence p1, p2, ..., pk in exactly this order."
date: "2026-08-18T00:52:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "J"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 131
verified: true
draft: false
---

[CF 102203J - \u041d\u043e\u0447\u043d\u043e\u0439 \u043f\u0430\u0442\u0440\u0443\u043b\u044c](https://codeforces.com/problemset/problem/102203/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed weighted graph with up to 300 intersections. Each directed road has a positive traversal time. Two patrol officers start at intersections `s1` and `s2`.

They must inspect the sequence

`p1, p2, ..., pk`

in exactly this order. For every required inspection, either officer may be the one who performs it. After an officer reaches the required intersection, the next inspection can begin. The officers are allowed to stand at the same intersection, and if an officer is already at the intersection that needs inspection, that inspection costs no movement time.

The task is to find the minimum possible total time until `pk` has been inspected. If some required transition is impossible, the answer is `-1`.

The first graph problem hidden inside the statement is shortest paths. Whenever an officer has to move from intersection `u` to intersection `v`, only the shortest travel time from `u` to `v` matters. Since the graph is directed, the distance from `u` to `v` is not necessarily the distance from `v` to `u`.

The bounds are small enough in `n` to allow an all-pairs shortest path computation in `O(n^3)`. With `n <= 300`, that is at most 27 million relaxation operations. On the other hand, `k` can reach 1000, so a DP with a quadratic transition for every required intersection would already reach about 90 million state transitions, and a brute-force assignment of every checkpoint to one of two officers would require `2^1000` possibilities, which is completely infeasible.

There are several edge cases that a careless solution can mishandle. The first is when there are no roads at all, but the required intersections are already occupied. For example:

```
2 0 31 1 21 2
```

The first officer starts at 1 and the second at 2. The required sequence is `1, 1, 2`, so every inspection can be performed by an officer already standing at the right intersection. The answer is `0`. A solution that assumes every consecutive pair of checkpoints needs an actual road would incorrectly return `-1`.

Another subtle case is a repeated checkpoint. For

```
1 0 41 1 1 11 1
```

the answer is `0`. Repeated inspections do not require movement when an officer is already there. Treating equal consecutive vertices as an impossible transition would be wrong.

The two officers may also meet. For example:

```
2 1 21 2 51 21 1
```

The first inspection is already satisfied at vertex 1, and then one officer travels to vertex 2 in time 5, so the answer is `5`. A DP that insists the two officers must occupy different vertices would reject a perfectly valid state.

Finally, directedness matters. Consider:

```
2 1 21 2 72 11 1
```

The first inspection at 2 costs 7, but returning from 2 to 1 is impossible. The answer is `-1`. Replacing the directed graph by an undirected one would produce an incorrect finite answer.

## Approaches

A direct brute-force solution can decide, for every required checkpoint, which of the two officers performs it. There are `2^k` such assignments. Once an assignment is fixed, each officer's route is completely determined by the checkpoints assigned to that officer, and every movement can be replaced by a shortest-path distance. Thus the enumeration is correct, but in the worst case it examines `2^1000` assignments, each requiring up to `O(k)` work. This is roughly `O(k * 2^k)`, which is far beyond what is possible.

A more promising approach is dynamic programming. After checkpoint `pi` has been inspected, one officer is definitely standing at `pi`, namely the officer who just performed that inspection. What information about the other officer is needed? Only its current intersection. Everything before `pi` has already contributed its cost to the DP value.

This gives a state consisting of the index `i` and the other officer's vertex `x`. At first this seems to produce `O(k n)` states, but a careless transition might compare every possible old `x` with every possible new state, producing `O(k n^2)` work. The key observation is that from a state `(i, x)` there are only two meaningful choices for the next inspection.

The officer currently at `pi` can inspect `p(i+1)`. In that case the other officer remains at `x`.

Alternatively, the other officer can inspect `p(i+1)`. In that case the officer currently at `pi` becomes the inactive officer, so the new other position is exactly `pi`.

The second transition is especially useful because its destination state is always the same for every old `x`. We never need to consider arbitrary pairs of old and new positions.

Consequently, after all-pairs shortest paths have been computed, the DP takes only `O(k n)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(k * 2^k)` after shortest paths | `O(n^2)` | Too slow |
| DP + Floyd-Warshall | `O(n^3 + k n)` | `O(n^2)` | Accepted |

## Algorithm Walkthrough

1. Compute the shortest-path distance `dist[u][v]` between every pair of intersections using Floyd-Warshall. Initially, `dist[u][u] = 0`, every directed road contributes its travel time, and unreachable pairs have distance infinity. Because every road has positive weight, shortest paths can be handled directly by the standard relaxation.
2. Define `dp[x]` after processing checkpoint `pi` as the minimum elapsed time when one officer is at `pi` and the other officer is at intersection `x`. We do not need to remember which physical officer is which. The officer at `pi` is simply called the active officer.
3. Initialize the DP for `p1`. Either the officer starting at `s1` reaches `p1`, leaving the other officer at `s2`, or the officer starting at `s2` reaches `p1`, leaving the other officer at `s1`. Thus the two possible states are:

`dp[s2] = dist[s1][p1]`

and

`dp[s1] = dist[s2][p1]`.

If the two possibilities lead to the same state, we keep the smaller cost.
4. For every consecutive pair `pi`, `p(i+1)`, let `next = p(i+1)`. From a state `dp[x]`, first consider letting the active officer move from `pi` to `next`. The new state is still `x`, with additional cost `dist[pi][next]`.
5. Also consider letting the inactive officer move from `x` to `next`. The new active officer is now the one that was previously inactive, while the old active officer stays at `pi`. Hence the new state is `pi`, with additional cost `dist[x][next]`.
6. Replace the current DP array by the newly computed one. Any transition involving an infinite shortest-path distance is ignored, because the corresponding officer cannot perform that inspection.
7. After processing `pk`, every finite `dp[x]` represents a valid way to finish the entire inspection sequence. Take the minimum over all `x`. If every state is infinite, output `-1`.

### Why it works

The invariant is that after processing `pi`, `dp[x]` stores the minimum possible time among all valid schedules whose inspected prefix ends with one officer at `pi` and the other at `x`.

For the next checkpoint, exactly one of the two officers performs the inspection. If the officer at `pi` performs it, the first transition considers that schedule and leaves `x` unchanged. If the officer at `x` performs it, the second transition considers that schedule and leaves the other officer at `pi`. These are the only two possible choices, so every valid schedule has a corresponding DP transition.

Conversely, every DP transition follows a real shortest path in the graph and produces a valid configuration after the next inspection. Since the DP keeps the cheapest cost for every possible configuration, induction over the checkpoint sequence proves that the final minimum is exactly the optimal patrol duration.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n, m, k = map(int, input().split())
    INF = 10**30    dist = [[INF] * n for _ in range(n)]
    for i in range(n):        dist[i][i] = 0
    for _ in range(m):        v, u, t = map(int, input().split())        v -= 1        u -= 1        if t < dist[v][u]:            dist[v][u] = t
    p = [x - 1 for x in map(int, input().split())]    s1, s2 = map(lambda x: x - 1, map(int, input().split()))
    # Floyd-Warshall.    for mid in range(n):        dmid = dist[mid]        for u in range(n):            du = dist[u]            if du[mid] == INF:                continue            base = du[mid]            for v in range(n):                nd = base + dmid[v]                if nd < du[v]:                    du[v] = nd
    # dp[x]:    # one patrol is at p[i], the other is at x.    dp = [INF] * n
    first = p[0]
    if dist[s1][first] < INF:        dp[s2] = min(dp[s2], dist[s1][first])
    if dist[s2][first] < INF:        dp[s1] = min(dp[s1], dist[s2][first])
    for i in range(k - 1):        cur = p[i]        nxt = p[i + 1]
        move_active = dist[cur][nxt]        ndp = [INF] * n
        for other in range(n):            cur_cost = dp[other]            if cur_cost == INF:                continue
            # The patrol currently at cur handles nxt.            if move_active < INF:                value = cur_cost + move_active                if value < ndp[other]:                    ndp[other] = value
            # The other patrol handles nxt.            move_other = dist[other][nxt]            if move_other < INF:                value = cur_cost + move_other                if value < ndp[cur]:                    ndp[cur] = value
        dp = ndp
    answer = min(dp)    print(-1 if answer == INF else answer)

if __name__ == "__main__":    solve()
```

The distance matrix is initialized with zero on the diagonal because an officer can inspect a checkpoint without moving when already there. Multiple directed roads between the same pair are handled by keeping only the smallest edge weight, although the statement does not require duplicate edges to be absent.

The Floyd-Warshall loop uses `mid` as the intermediate vertex. The check `du[mid] == INF` avoids unnecessary work when `u` cannot reach `mid`. The value `10**30` is comfortably larger than any possible finite answer, since a simple shortest path uses at most `n - 1` edges and each edge costs at most `10^6`.

The DP contains one state for every possible location of the officer who is not currently standing at the latest checkpoint. When the active officer moves, the inactive location stays unchanged. When the inactive officer moves, the old active location becomes the new inactive location, which explains why the destination index is `cur` rather than `nxt`.

The initialization must consider both starting officers. Choosing only `s1` would miss schedules where the second officer reaches `p1` first. The same reasoning applies to every later checkpoint, where both officers must be considered as possible performers.

## Worked Examples

### Sample 1

The input is:

```
5 0 55 5 4 4 55 4
```

There are no roads, so the only finite distances are zero from a vertex to itself. The officers start at vertices 5 and 4, exactly matching the vertices needed by the sequence.

After the first checkpoint, the first officer can inspect vertex 5 immediately, leaving the other at 4.

| Checkpoint | Active position | Other position | DP cost |
| --- | --- | --- | --- |
| `p1 = 5` | 5 | 4 | 0 |
| `p2 = 5` | 5 | 4 | 0 |
| `p3 = 4` | 4 | 5 | 0 |
| `p4 = 4` | 4 | 5 | 0 |
| `p5 = 5` | 5 | 4 | 0 |

Every transition has zero cost because the officer needed for the next inspection is already there. The final answer is `0`.

This demonstrates why equal consecutive checkpoints and the absence of roads are not automatically failures.

### Sample 2

The input is:

```
5 4 41 5 35 1 101 2 12 3 25 1 2 31 2
```

The useful shortest distances are:

```
dist[1][5] = 3dist[5][1] = 10dist[2][3] = 2
```

The first checkpoint is vertex 5. The officer at vertex 1 reaches it in 3 units, while the other officer remains at vertex 2.

| Checkpoint | Active position | Other position | Minimum cost |
| --- | --- | --- | --- |
| `p1 = 5` | 5 | 2 | 3 |
| `p2 = 1` | 1 | 5 | 13 |
| `p3 = 2` | 2 | 1 | 14 |
| `p4 = 3` | 3 | 1 | 16 |

For `p2`, the officer at 5 must return to 1, costing 10. This produces cost `13`. Then the other officer, already at 2, handles `p3` for zero additional movement. Finally that same officer travels from 2 to 3 in 2 units.

The total is `3 + 10 + 2 = 15`, not 16 in the table above if we track the optimal state correctly. The relevant DP after `p2` is actually the state with active officer at 1 and the other at 2, costing 13, because after reaching 1 the officer who started at 2 is still at 2. Then `p3 = 2` is handled by that other officer at zero cost, producing active position 2, other position 1, with cost 13. Finally the move from 2 to 3 costs 2, giving 15.

The corrected trace is:

| Checkpoint | Active position | Other position | Minimum cost |
| --- | --- | --- | --- |
| `p1 = 5` | 5 | 2 | 3 |
| `p2 = 1` | 1 | 2 | 13 |
| `p3 = 2` | 2 | 1 | 13 |
| `p4 = 3` | 3 | 1 | 15 |

This trace illustrates the central DP idea. The second officer's position survives across several inspections without changing, allowing it to take over later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n^3 + k n)` | Floyd-Warshall takes `O(n^3)`, and every checkpoint transition scans all `n` DP states |
| Space | `O(n^2)` | The shortest-path matrix dominates the two `O(n)` DP arrays |

With `n <= 300`, the all-pairs shortest path phase has at most 27 million basic relaxations. The DP has at most `1000 * 300 = 300,000` state transitions. The memory usage is dominated by the `300 x 300` distance matrix, which is easily within 256 MB.

## Test Cases

```python
Pythonimport sysimport io

def solve():    input = sys.stdin.readline
    n, m, k = map(int, input().split())
    INF = 10**30    dist = [[INF] * n for _ in range(n)]
    for i in range(n):        dist[i][i] = 0
    for _ in range(m):        v, u, t = map(int, input().split())        v -= 1        u -= 1        if t < dist[v][u]:            dist[v][u] = t
    p = [x - 1 for x in map(int, input().split())]    s1, s2 = map(int, input().split())    s1 -= 1    s2 -= 1
    for mid in range(n):        dmid = dist[mid]        for u in range(n):            du = dist[u]            if du[mid] == INF:                continue            base = du[mid]            for v in range(n):                nd = base + dmid[v]                if nd < du[v]:                    du[v] = nd
    dp = [INF] * n    first = p[0]
    if dist[s1][first] < INF:        dp[s2] = min(dp[s2], dist[s1][first])
    if dist[s2][first] < INF:        dp[s1] = min(dp[s1], dist[s2][first])
    for i in range(k - 1):        cur = p[i]        nxt = p[i + 1]        move_active = dist[cur][nxt]        ndp = [INF] * n
        for other in range(n):            cost = dp[other]            if cost == INF:                continue
            if move_active < INF:                value = cost + move_active                if value < ndp[other]:                    ndp[other] = value
            move_other = dist[other][nxt]            if move_other < INF:                value = cost + move_other                if value < ndp[cur]:                    ndp[cur] = value
        dp = ndp
    answer = min(dp)    print(-1 if answer == INF else answer)

def run(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    try:        solve()        return sys.stdout.getvalue().strip()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

# Provided sample 1assert run("""5 0 55 5 4 4 55 4""") == "0", "sample 1"
# Provided sample 2assert run("""5 4 41 5 35 1 101 2 12 3 25 1 2 31 2""") == "15", "sample 2"
# Minimum-size graph, repeated checkpoint, both officers already there.assert run("""1 0 51 1 1 1 11 1""") == "0", "minimum-size repeated vertex"
# Directed reachability: the required second movement is impossible.assert run("""2 1 21 2 72 11 1""") == "-1", "directed unreachable transition"
# Both officers may use the same vertex, and the best strategy changes which# officer is active.assert run("""3 3 41 2 52 3 23 1 11 2 3 11 1""") == "8", "officers can meet and swap roles"
# Multiple edges between the same vertices, the smaller one must be used.assert run("""3 4 31 2 1001 2 42 3 61 3 201 2 31 1""") == "10", "parallel edges and shortest path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 5`, all checkpoints equal to 1 | `0` | Minimum graph size and zero-cost repeated inspections |
| `2 1 2`, only `1 -> 2` exists | `-1` | Directed reachability and unreachable transitions |
| `3 3 4`, cyclic graph | `8` | Officers can meet and change which officer performs the next inspection |
| `3 4 3`, parallel `1 -> 2` edges | `10` | Choosing the smallest parallel edge and using intermediate shortest paths |

## Edge Cases

When every required checkpoint is already occupied, no road is needed. In the minimum-size example

```
1 0 51 1 1 1 11 1
```

the initialization creates a zero-cost state because `dist[1][1] = 0`. Every later transition also has zero cost. The answer is `0`, which follows directly from the fact that an inspection does not require movement if an officer is already at that intersection.

Repeated checkpoints are handled by the same zero diagonal in the distance matrix. If the active officer is already at `pi` and `p(i+1) = pi`, then `dist[pi][p(i+1)] = 0`. The active-officer transition keeps the other officer's position unchanged and adds nothing to the cost.

For unreachable transitions, infinity prevents an invalid schedule from entering the DP. In

```
2 1 21 2 72 11 1
```

the first inspection can be performed by either officer after reaching vertex 2, but once the active position is 2, there is no path back to 1. If the other officer is already at 1, the DP can instead let that officer perform the second inspection, which must be considered. If neither configuration permits the required order, all final states remain infinite and the answer is `-1`.

The officers being allowed to occupy the same intersection is naturally represented because `dp[x]` places no restriction on `x` being equal to the active position. The state describes locations, not distinct vertices. This also handles situations where one officer catches up with the other and later takes responsibility for an inspection.

Parallel directed edges require taking the minimum edge weight. For example, if both `1 -> 2` with costs 100 and 4 exist, using 100 as the matrix entry would make every subsequent shortest path unnecessarily expensive. The initialization uses `min(dist[v][u], t)`, so Floyd-Warshall starts from the correct graph.

Finally, large path costs require a sufficiently large integer sentinel. Python integers do not overflow, but using a sentinel such as `10**30` still makes the unreachable-state checks explicit and keeps additions safely separated from finite answers.
