---
title: "CF 105482F - \u041f\u043e\u0433\u043e\u043d\u044f \u0432 \u041f\u0443\u0441\u0442\u043e\u0442\u0435"
description: "We have an undirected graph with n locations. The heroes start at location 1, the shelter is at location n, and Alioth has already occupied k locations. Alioth does not move like a single character. It spreads."
date: "2026-06-25T06:03:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105482
codeforces_index: "F"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105482
solve_time_s: 73
verified: true
draft: false
---

[CF 105482F - \u041f\u043e\u0433\u043e\u043d\u044f \u0432 \u041f\u0443\u0441\u0442\u043e\u0442\u0435](https://codeforces.com/problemset/problem/105482/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph with `n` locations. The heroes start at location `1`, the shelter is at location `n`, and Alioth has already occupied `k` locations.

Alioth does not move like a single character. It spreads. If a location becomes occupied at time `t`, it remains occupied forever and starts spreading further. In graph terms, the arrival time of Alioth at a vertex is simply the shortest distance from any initially occupied vertex.

We are allowed to build additional tunnels between locations. The goal is to add as many tunnels as possible while still allowing the heroes to reach the shelter strictly earlier than Alioth. If at some location both arrive at the same time, the heroes lose.

The input gives the initial graph and the set of infected locations. The output is the maximum number of new tunnels that can be built. If survival is impossible no matter what we do, we must print `-1`.

The graph contains up to `10^5` vertices and `2·10^5` edges. Any solution that tries to reason about all possible additional edges individually would be far too slow, because the complete graph contains roughly `n²/2` edges. We need a characterization that can be checked in linear or near-linear time.

The most dangerous edge case is when the shelter is already adjacent to an infected location.

Example:

```
4 5 1
3
1 4
3 4
4 2
1 3
3 2
```

Alioth starts at vertex `3`. The shelter is vertex `4`, and there is already an edge `3-4`. Alioth reaches the shelter in one step. Even if the heroes use a direct edge to the shelter, they also need one step, producing a tie. The correct answer is:

```
-1
```

A careless solution might assume that adding more edges can always help the heroes, but extra edges help Alioth too.

Another important case is when the shelter is not adjacent to any infected location.

Example:

```
3 1 1
2
1 3
```

We can add edge `1-2`, but we must not add edge `2-3`. The heroes can use the direct edge `1-3` and arrive in one step, while Alioth needs two steps to reach the shelter. The answer is:

```
1
```

## Approaches

A brute-force approach would try to reason about which missing edges may be added and which must remain absent. There are up to

$$\frac{n(n-1)}2$$

possible edges, which is about `5·10^9` when `n = 10^5`. Even iterating over all potential edges is impossible.

The key observation is that the heroes only need one safe route. Since we are free to add tunnels, the best route is obvious: connect `1` directly to `n` if that edge does not already exist, and travel in one move.

The heroes start at time `0` in vertex `1` and reach the shelter at time `1`.

For this plan to work, Alioth must reach vertex `n` strictly after time `1`. Since Alioth spreads through shortest paths, this means the distance from every infected vertex to `n` must be at least `2`.

What can make Alioth reach `n` in one step? Exactly an edge between an infected vertex and `n`.

This immediately gives the entire structure of the optimal graph.

If an infected vertex is already connected to `n` in the initial graph, Alioth reaches the shelter in one step regardless of what we add later. Survival is impossible, so the answer is `-1`.

Otherwise, we can add every missing edge except those connecting an infected vertex directly to `n`.

Those forbidden edges are the only ones that would reduce Alioth's arrival time at the shelter from at least `2` to exactly `1`.

Let `k` be the number of infected vertices. In a complete graph there are

$$\frac{n(n-1)}2$$

edges. We must exclude exactly `k` edges, namely `(infected, n)`.

So the maximum number of edges in a valid final graph is

$$\frac{n(n-1)}2 - k.$$

Since the graph already contains `m` edges, the maximum number of additional tunnels is

$$\frac{n(n-1)}2 - k - m.$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal | O(m + k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the infected vertices and mark them in a boolean array.
2. Read all existing edges.
3. While reading edges, check whether one endpoint is the shelter `n` and the other endpoint is infected.
4. If such an edge exists, print `-1`.

The shelter is already reachable by Alioth in one step. The heroes cannot arrive strictly earlier than that.
5. Otherwise compute

$$\text{complete} = \frac{n(n-1)}2.$$
6. The final graph may contain every edge except the `k` edges between infected vertices and the shelter.
7. The maximum number of new tunnels equals

$$\text{complete} - k - m.$$
8. Print that value.

### Why it works

If an infected vertex is adjacent to the shelter, Alioth reaches the shelter at time `1`. Any route from the heroes' starting location requires at least one move, so the best possible arrival time for the heroes is also `1`. The condition is strict, so survival is impossible.

Assume no infected vertex is adjacent to the shelter. Construct a graph containing every possible edge except the `k` forbidden edges `(infected, n)`.

The heroes travel directly from `1` to `n` in one step.

Alioth cannot reach `n` in one step because every edge from an infected vertex to `n` is absent. Hence Alioth reaches `n` no earlier than time `2`.

The heroes arrive at time `1`, which is strictly earlier.

Any additional edge not of the form `(infected, n)` does not reduce Alioth's arrival time at the shelter below `2`, so all such edges may safely be added. This graph is maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
infected = list(map(int, input().split()))

bad = [False] * (n + 1)
for v in infected:
    bad[v] = True

impossible = False

for _ in range(m):
    u, v = map(int, input().split())

    if u == n and bad[v]:
        impossible = True
    if v == n and bad[u]:
        impossible = True

if impossible:
    print(-1)
else:
    total_edges = n * (n - 1) // 2
    answer = total_edges - k - m
    print(answer)
```

The first part stores all infected vertices in a boolean array so membership checks are constant time.

While reading the edges, we only care about one condition: whether the shelter is already adjacent to an infected vertex. No graph traversal is needed.

If such an edge exists, the answer is immediately `-1`.

Otherwise, we compute the size of the complete graph and subtract the `k` permanently forbidden edges connecting infected vertices to the shelter. The graph already contains `m` edges, so the remaining count is exactly the number of tunnels that can still be built.

All arithmetic uses 64-bit sized values. In Python, integers are unbounded, so there is no overflow risk. The largest value of `n(n-1)/2` is about `5·10^9`, which comfortably fits anyway.

## Worked Examples

### Example 1

Input:

```
3 1 1
2
1 3
```

State during processing:

| Variable | Value |
| --- | --- |
| n | 3 |
| m | 1 |
| k | 1 |
| infected | {2} |
| infected adjacent to 3? | No |

Computation:

| Quantity | Value |
| --- | --- |
| Complete graph edges | 3 |
| Forbidden edges (infected, 3) | 1 |
| Existing edges | 1 |
| Answer | 3 - 1 - 1 = 1 |

Output:

```
1
```

The only forbidden edge is `2-3`. Every other missing edge may be added.

### Example 2

Input:

```
7 6 3
5 6 2
1 7
6 2
1 4
3 6
5 3
2 1
```

State during processing:

| Variable | Value |
| --- | --- |
| n | 7 |
| m | 6 |
| k | 3 |
| infected | {2,5,6} |
| infected adjacent to 7? | No |

Computation:

| Quantity | Value |
| --- | --- |
| Complete graph edges | 21 |
| Forbidden edges | 3 |
| Existing edges | 6 |
| Answer | 21 - 3 - 6 = 12 |

Output:

```
12
```

This example demonstrates the maximal construction. Every missing edge can be added except `2-7`, `5-7`, and `6-7`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m + k) | Read infected vertices and scan edges once |
| Space | O(n) | Boolean array marking infected vertices |

The constraints allow up to `10^5` vertices and `2·10^5` edges. A single linear scan is easily fast enough and fits comfortably within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    infected = list(map(int, input().split()))

    bad = [False] * (n + 1)
    for v in infected:
        bad[v] = True

    impossible = False

    for _ in range(m):
        u, v = map(int, input().split())
        if u == n and bad[v]:
            impossible = True
        if v == n and bad[u]:
            impossible = True

    if impossible:
        return "-1\n"

    total_edges = n * (n - 1) // 2
    return str(total_edges - k - m) + "\n"

# provided samples
assert run(
"""3 1 1
2
1 3
"""
) == "1\n"

assert run(
"""7 6 3
5 6 2
1 7
6 2
1 4
3 6
5 3
2 1
"""
) == "12\n"

assert run(
"""4 5 1
3
1 4
3 4
4 2
1 3
3 2
"""
) == "-1\n"

# minimum size
assert run(
"""3 1 1
2
1 3
"""
) == "1\n"

# shelter adjacent to infected
assert run(
"""5 1 1
2
2 5
"""
) == "-1\n"

# almost complete graph
assert run(
"""4 5 1
2
1 3
1 4
2 3
3 4
1 2
"""
) == "0\n"

# no forbidden existing edge
assert run(
"""5 0 2
2 3
"""
) == "8\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 1 | Basic valid construction |
| Sample 2 | 12 | Dense completion with several infected nodes |
| Sample 3 | -1 | Shelter already adjacent to infection |
| Minimum-size graph | 1 | Smallest valid instance |
| Single forbidden edge | -1 | Immediate impossibility |
| Almost complete graph | 0 | No additional tunnels available |
| No initial edges | 8 | Formula on sparse graph |

## Edge Cases

Consider again:

```
4 5 1
3
1 4
3 4
4 2
1 3
3 2
```

The shelter is vertex `4`. Since edge `3-4` already exists and vertex `3` is infected, Alioth reaches the shelter at time `1`.

The heroes cannot do better than time `1`, because any movement requires at least one edge traversal.

The algorithm detects the infected-shelter edge while scanning the input and immediately returns:

```
-1
```

Now consider:

```
3 1 1
2
1 3
```

There is no infected-shelter edge. The algorithm computes:

```
complete = 3
forbidden = 1
existing = 1
answer = 1
```

The heroes use the direct route `1 -> 3` in one step. Alioth must first go `2 -> 1 -> 3`, which takes two steps. The strict inequality is satisfied, so the output is correct.
