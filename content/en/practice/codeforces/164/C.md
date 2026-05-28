---
title: "CF 164C - Machine Programming"
description: "We have several jobs, each with a start time, a duration, and a profit. A machine that starts a job stays occupied for the entire interval from s through s + t - 1. At most k jobs may run simultaneously because we only own k machines. The goal is not to schedule all jobs."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 164
codeforces_index: "C"
codeforces_contest_name: "VK Cup 2012 Round 3"
rating: 2400
weight: 164
solve_time_s: 136
verified: true
draft: false
---

[CF 164C - Machine Programming](https://codeforces.com/problemset/problem/164/C)

**Rating:** 2400  
**Tags:** flows, graphs  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several jobs, each with a start time, a duration, and a profit. A machine that starts a job stays occupied for the entire interval from `s` through `s + t - 1`. At most `k` jobs may run simultaneously because we only own `k` machines.

The goal is not to schedule all jobs. We may discard some of them. We want the subset whose total profit is maximum while never exceeding `k` overlapping jobs at any moment.

The output is a binary array. Position `i` equals `1` if the `i`-th job is selected and `0` otherwise.

The constraints completely shape the solution. There are at most `1000` jobs, which is small enough for graph constructions with around `O(n^2)` edges, but too large for exponential search. The number of machines is at most `50`, which suggests some kind of flow or DP over limited capacity. Time coordinates reach `10^9`, so iterating over every time moment is impossible. Any valid solution must compress the timeline down to only meaningful event points.

A subtle detail is the interval definition. A job occupying `[s, s+t-1]` conflicts with another job starting before `s+t`. For example:

```
2 1
1 2 5
3 1 7
```

The first job occupies times `1,2`. The second starts at `3`, so they do not overlap and both may be chosen. A careless implementation using closed intervals `[s, s+t]` would incorrectly reject this pair.

Another easy mistake appears when multiple jobs share the same start or end time.

```
3 1
1 2 5
1 1 4
2 1 4
```

The first job occupies `1,2`. The second occupies `1`. The third occupies `2`. We cannot take the first together with either smaller job, but we may take the second and third together for total profit `8`. Any implementation that sorts incorrectly or handles equal coordinates inconsistently may accidentally allow three overlapping jobs at time `1` or `2`.

The last dangerous case is when many jobs overlap but `k > 1`.

```
4 2
1 5 10
2 3 8
3 2 7
4 1 6
```

Here up to two jobs may run simultaneously. A greedy strategy that always picks the highest-profit non-overlapping job fails because overlaps are allowed up to capacity `k`. The problem is not ordinary weighted interval scheduling.

## Approaches

The brute-force idea is straightforward. We try every subset of jobs, verify whether at any time more than `k` jobs overlap, and keep the best profit. Correctness is obvious because every possible answer is examined.

The problem is the size of the search space. With `n = 1000`, the number of subsets is `2^1000`, which is astronomically impossible. Even checking only `2^40` subsets would already be far beyond the limit.

A more refined brute-force direction is dynamic programming on intervals. For `k = 1`, the problem becomes classic weighted interval scheduling. We sort jobs by finishing time and use binary search to connect each interval to the next compatible one. That gives an `O(n log n)` solution.

The obstacle is that `k` may exceed `1`. Once multiple overlaps are allowed, the state no longer depends only on the latest chosen interval. Different machines may currently be occupied by different jobs ending at different moments. A direct DP over machine states explodes combinatorially.

The key observation is that the constraint is fundamentally about capacity over time. At any moment, at most `k` jobs may pass through that point. This is exactly the kind of structure min-cost max-flow models naturally.

We compress all distinct time coordinates. Between consecutive times, we create timeline edges with capacity `k`. Sending one unit of flow represents one machine moving forward through time. Choosing a job means diverting one unit of flow through a special edge that jumps from its start time to its end time while collecting profit.

Because profits must be maximized, we convert them into negative costs and compute a minimum-cost flow. The timeline edges have cost `0`, while each job edge has cost `-c_i`. A flow path may either idle through time or use profitable job edges whenever beneficial.

This transforms the scheduling constraint into standard flow conservation and edge capacities. Capacity `k` on timeline edges guarantees no more than `k` simultaneous jobs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^2) | O(n) | Too slow |
| Optimal Min-Cost Flow | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. For every job, compute its ending moment as `e = s + t`.

Using `s + t` instead of `s + t - 1` converts the occupied interval into the half-open range `[s, e)`. Two jobs are compatible exactly when one starts at or after the other's `e`.
2. Collect all distinct start and end coordinates and sort them.

The actual numeric values may be as large as `10^9`, but only relative ordering matters. Coordinate compression reduces the graph size to at most `2n` nodes.
3. Build a directed graph over compressed time indices.

If the compressed times are `T[0], T[1], ..., T[m-1]`, create edges:

`i -> i+1` with capacity `k` and cost `0`.

These edges represent machines moving forward through time without performing jobs.
4. Add a source connected to the first time node with capacity `k`, and connect the last time node to the sink with capacity `k`.

This creates exactly `k` units of available machine flow.
5. For every job, add an edge from its compressed start index to its compressed end index.

The edge has:

capacity `1`

cost `-profit`

Taking this edge means one machine performs that job during its occupied interval.
6. Run min-cost max-flow from source to sink.

The flow naturally decides which job edges are profitable enough to use.
7. Recover the chosen jobs.

Every job edge whose capacity became `0` was fully used by the flow, so that job belongs to the optimal schedule.

### Why it works

Each unit of flow represents one machine traveling forward in time. Timeline edges preserve the limit of at most `k` simultaneous machines because only `k` units may cross any time segment.

A job edge occupies one machine from its start coordinate to its end coordinate. Since that edge bypasses intermediate timeline edges, the machine cannot simultaneously perform another overlapping job.

Flow conservation guarantees every machine follows a valid chronological sequence of jobs. The total flow cost equals the negative total profit of selected jobs. Minimizing cost is equivalent to maximizing profit.

Because all capacities and costs exactly encode the scheduling constraints and objective, every feasible flow corresponds to a valid schedule with identical profit, and every valid schedule corresponds to a feasible flow.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10**18

class Edge:
    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost

class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap, cost):
        fwd = Edge(to, len(self.g[to]), cap, cost)
        rev = Edge(fr, len(self.g[fr]), 0, -cost)
        self.g[fr].append(fwd)
        self.g[to].append(rev)

    def min_cost_flow(self, s, t, maxf):
        n = self.n
        flow = 0
        cost = 0

        potential = [0] * n

        while flow < maxf:
            dist = [INF] * n
            parent_v = [-1] * n
            parent_e = [-1] * n

            dist[s] = 0

            inq = [False] * n
            q = deque([s])
            inq[s] = True

            while q:
                v = q.popleft()
                inq[v] = False

                for i, e in enumerate(self.g[v]):
                    if e.cap <= 0:
                        continue

                    nd = dist[v] + e.cost + potential[v] - potential[e.to]

                    if nd < dist[e.to]:
                        dist[e.to] = nd
                        parent_v[e.to] = v
                        parent_e[e.to] = i

                        if not inq[e.to]:
                            inq[e.to] = True
                            q.append(e.to)

            if dist[t] == INF:
                break

            for v in range(n):
                if dist[v] < INF:
                    potential[v] += dist[v]

            addf = maxf - flow
            v = t

            while v != s:
                pv = parent_v[v]
                pe = parent_e[v]
                addf = min(addf, self.g[pv][pe].cap)
                v = pv

            v = t

            while v != s:
                pv = parent_v[v]
                pe = parent_e[v]
                e = self.g[pv][pe]

                e.cap -= addf
                self.g[v][e.rev].cap += addf

                cost += addf * e.cost
                v = pv

            flow += addf

        return flow, cost

def solve():
    n, k = map(int, input().split())

    jobs = []
    coords = []

    for i in range(n):
        s, t, c = map(int, input().split())
        e = s + t

        jobs.append((s, e, c, i))

        coords.append(s)
        coords.append(e)

    coords = sorted(set(coords))
    idx = {x: i for i, x in enumerate(coords)}

    m = len(coords)

    SRC = m
    SNK = m + 1

    mcmf = MinCostFlow(m + 2)

    mcmf.add_edge(SRC, 0, k, 0)

    for i in range(m - 1):
        mcmf.add_edge(i, i + 1, k, 0)

    mcmf.add_edge(m - 1, SNK, k, 0)

    job_edges = [None] * n

    for s, e, c, original_idx in jobs:
        u = idx[s]
        v = idx[e]

        edge_index = len(mcmf.g[u])

        mcmf.add_edge(u, v, 1, -c)

        job_edges[original_idx] = (u, edge_index)

    mcmf.min_cost_flow(SRC, SNK, k)

    ans = [0] * n

    for i in range(n):
        u, ei = job_edges[i]
        e = mcmf.g[u][ei]

        if e.cap == 0:
            ans[i] = 1

    print(*ans)

if __name__ == "__main__":
    solve()
```

The graph contains one node for every compressed time coordinate. Timeline edges connect consecutive coordinates and carry up to `k` machines forward.

The most important implementation detail is the interval conversion. The original interval is inclusive on both ends, `[s, s+t-1]`. Converting it into `[s, s+t)` avoids off-by-one problems and makes compatibility checks much cleaner.

Each job edge stores capacity `1`. After the flow finishes, a used edge has residual capacity `0`. That is how the chosen jobs are reconstructed.

The shortest path computation uses reduced costs with potentials. Costs may be negative because profitable jobs have negative edge weights. Potentials guarantee non-negative reduced costs after each augmentation.

Another subtle detail is that we send exactly `k` units of flow, even if some machines stay idle. Idle machines simply traverse timeline edges with zero cost.

## Worked Examples

### Example 1

Input:

```
3 1
2 7 5
1 3 3
4 1 3
```

The intervals become:

| Job | Interval | Profit |
| --- | --- | --- |
| 1 | [2, 9) | 5 |
| 2 | [1, 4) | 3 |
| 3 | [4, 5) | 3 |

Compressed coordinates:

| Index | Time |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 4 |
| 3 | 5 |
| 4 | 9 |

Job edges:

| Job | Edge |
| --- | --- |
| 1 | 1 -> 4 |
| 2 | 0 -> 2 |
| 3 | 2 -> 3 |

The optimal flow path is:

| Step | Edge Used | Total Profit |
| --- | --- | --- |
| 1 | Job 2 | 3 |
| 2 | Job 3 | 6 |

Choosing Job 1 alone gives profit `5`, so the flow prefers Jobs 2 and 3.

This trace demonstrates how sequential compatible jobs naturally chain together through timeline edges.

### Example 2

Input:

```
4 2
1 5 10
2 3 8
3 2 7
4 1 6
```

Converted intervals:

| Job | Interval | Profit |
| --- | --- | --- |
| 1 | [1, 6) | 10 |
| 2 | [2, 5) | 8 |
| 3 | [3, 5) | 7 |
| 4 | [4, 5) | 6 |

At time range `[4,5)`, four jobs overlap, but only two machines exist.

The flow selects:

| Machine | Jobs |
| --- | --- |
| 1 | Job 1 |
| 2 | Job 2 |

Total profit becomes `18`.

The trace shows how capacity `k=2` is enforced automatically by timeline edge capacities. No more than two units of flow can cross the same time segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | The graph has O(n) nodes and O(n) edges, and min-cost flow performs at most k augmentations with shortest paths |
| Space | O(n^2) | Residual graph storage |

With `n <= 1000`, this comfortably fits inside the limits. The graph contains only a few thousand edges, and `k <= 50`, so the number of augmentations is small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from collections import deque

    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    input = input_data.readline

    INF = 10**18

    class Edge:
        def __init__(self, to, rev, cap, cost):
            self.to = to
            self.rev = rev
            self.cap = cap
            self.cost = cost

    class MinCostFlow:
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]

        def add_edge(self, fr, to, cap, cost):
            fwd = Edge(to, len(self.g[to]), cap, cost)
            rev = Edge(fr, len(self.g[fr]), 0, -cost)
            self.g[fr].append(fwd)
            self.g[to].append(rev)

        def min_cost_flow(self, s, t, maxf):
            n = self.n
            flow = 0
            potential = [0] * n

            while flow < maxf:
                dist = [INF] * n
                pv = [-1] * n
                pe = [-1] * n

                dist[s] = 0

                q = deque([s])
                inq = [False] * n
                inq[s] = True

                while q:
                    v = q.popleft()
                    inq[v] = False

                    for i, e in enumerate(self.g[v]):
                        if e.cap <= 0:
                            continue

                        nd = dist[v] + e.cost + potential[v] - potential[e.to]

                        if nd < dist[e.to]:
                            dist[e.to] = nd
                            pv[e.to] = v
                            pe[e.to] = i

                            if not inq[e.to]:
                                inq[e.to] = True
                                q.append(e.to)

                if dist[t] == INF:
                    break

                for i in range(n):
                    if dist[i] < INF:
                        potential[i] += dist[i]

                addf = maxf - flow
                v = t

                while v != s:
                    addf = min(addf, self.g[pv[v]][pe[v]].cap)
                    v = pv[v]

                v = t

                while v != s:
                    e = self.g[pv[v]][pe[v]]
                    e.cap -= addf
                    self.g[v][e.rev].cap += addf
                    v = pv[v]

                flow += addf

    n, k = map(int, input().split())

    jobs = []
    coords = []

    for i in range(n):
        s, t, c = map(int, input().split())
        e = s + t
        jobs.append((s, e, c, i))
        coords.extend([s, e])

    coords = sorted(set(coords))
    idx = {x: i for i, x in enumerate(coords)}

    m = len(coords)

    SRC = m
    SNK = m + 1

    mcf = MinCostFlow(m + 2)

    mcf.add_edge(SRC, 0, k, 0)

    for i in range(m - 1):
        mcf.add_edge(i, i + 1, k, 0)

    mcf.add_edge(m - 1, SNK, k, 0)

    pos = [None] * n

    for s, e, c, i in jobs:
        u = idx[s]
        v = idx[e]

        edge_id = len(mcf.g[u])

        mcf.add_edge(u, v, 1, -c)

        pos[i] = (u, edge_id)

    mcf.min_cost_flow(SRC, SNK, k)

    ans = []

    for i in range(n):
        u, ei = pos[i]
        ans.append("1" if mcf.g[u][ei].cap == 0 else "0")

    return " ".join(ans)

# provided sample
assert run(
"""3 1
2 7 5
1 3 3
4 1 3
"""
) == "0 1 1"

# minimum size
assert run(
"""1 1
1 1 10
"""
) == "1"

# overlapping jobs, only one machine
assert run(
"""2 1
1 5 10
2 3 9
"""
) == "1 0"

# touching intervals should both work
assert run(
"""2 1
1 2 5
3 1 6
"""
) == "1 1"

# two machines allow overlap
assert run(
"""3 2
1 5 10
2 3 9
3 2 8
"""
) == "1 1 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single job | `1` | Minimum-size boundary |
| Two overlapping jobs with k=1 | `1 0` | Capacity restriction |
| Touching intervals | `1 1` | Correct half-open interval handling |
| Heavy overlap with k=2 | `1 1 0` | Multiple simultaneous machines |

## Edge Cases

Consider jobs whose intervals only touch at endpoints.

```
2 1
1 2 5
3 1 6
```

The intervals become `[1,3)` and `[3,4)`. Their compressed edges connect consecutively without overlap. One flow unit may traverse both job edges in sequence, so both jobs are selected.

Now consider identical start times.

```
3 1
1 5 10
1 1 4
2 1 4
```

The first job occupies `[1,6)`. The other two occupy `[1,2)` and `[2,3)`. Since only one machine exists, the flow cannot simultaneously use the large interval edge and the smaller interval chain. The smaller chain yields profit `8`, while the long job yields `10`, so the algorithm correctly picks only the first job.

Finally, consider multiple machines.

```
4 2
1 5 10
2 3 8
3 2 7
4 1 6
```

All four jobs overlap near time `4`, but timeline edges have capacity `2`. At most two flow units can cross that segment, so the residual graph physically prevents choosing more than two overlapping jobs. The resulting schedule is always feasible by construction.
