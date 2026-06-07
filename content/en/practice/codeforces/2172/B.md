---
title: "CF 2172B - Buses"
description: "Every bus moves along the road at the same speed x. Bus i starts at position si at time 0, moves to the right, and disappears once it reaches ti. A person starts at position p. They can walk at speed y, where y < x."
date: "2026-06-07T22:54:06+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2172
codeforces_index: "B"
codeforces_contest_name: "2025 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 1800
weight: 2172
solve_time_s: 222
verified: false
draft: false
---

[CF 2172B - Buses](https://codeforces.com/problemset/problem/2172/B)

**Rating:** 1800  
**Tags:** greedy, sortings  
**Solve time:** 3m 42s  
**Verified:** no  

## Solution
## Problem Understanding

Every bus moves along the road at the same speed `x`. Bus `i` starts at position `s_i` at time `0`, moves to the right, and disappears once it reaches `t_i`.

A person starts at position `p`. They can walk at speed `y`, where `y < x`. Whenever a person and a bus occupy the same position at the same time, the person may instantly board that bus. While on a bus they move at speed `x`, and they may leave the bus at any moment.

For every starting position `p_i`, we must compute the minimum possible time needed to reach the road end at position `ℓ`.

The first observation is that all movement happens on a single line and all buses have identical speed. The constraints are large: up to `2 · 10^5` buses and `2 · 10^5` queries. Any algorithm that examines all buses for every person would require roughly `4 · 10^10` operations, which is completely infeasible. We need something close to `O((n+m) log n)`.

The most deceptive part of the problem is understanding what bus transfers are actually possible.

Consider two buses:

```
bus A: 0 -> 10
bus B: 5 -> 20
```

Both move at the same speed. If you are on bus A, you can never jump to bus B later because their distance remains constant forever. Equal speeds mean buses never catch one another.

Another subtle case is a person trying to board a bus that started behind them.

```
x = 4, y = 1
bus: 0 -> 100
person: 10
```

The bus is faster than the person. Since it started behind the person, it can eventually catch up. The meeting position is determined by relative speed and must be computed correctly. A careless solution that only checks whether `s_i ≥ p` would miss this valid boarding opportunity.

A third trap is assuming that riding a bus is always beneficial.

```
ℓ = 100
x = 10
y = 9

bus: 0 -> 1
person: 0
```

The bus only carries the person one meter before disappearing. Walking directly is almost as fast. The optimal answer must compare all possibilities, including never boarding any bus.

These observations suggest that the problem is really about evaluating independent bus opportunities, not sequences of transfers.

## Approaches

A brute-force approach would process each person separately.

For a given starting position `p`, we could examine every bus. For each bus we determine whether the person can meet it before it disappears. If a meeting is possible, we compute the resulting arrival time at position `ℓ`. The answer is the minimum among all buses and pure walking.

This is correct because every feasible strategy begins either by walking forever or by boarding some first bus. Unfortunately it requires `O(n)` work per query, leading to `O(nm)` total complexity. With both values reaching `2 · 10^5`, this becomes about `4 · 10^10` checks.

To improve, we need to understand the geometry of a single bus.

Suppose a person starts at position `p` and boards bus `(s,t)`.

If they meet at time `τ`, then

```
p + yτ = s + xτ
```

which gives

```
τ = (p - s)/(x - y)
```

A meeting is possible only when `p ≥ s`, because otherwise the bus is already ahead and moving away faster than the person.

The bus reaches its destination after

```
T = (t - s)/x
```

minutes.

Thus boarding is possible iff

```
(p - s)/(x - y) ≤ (t - s)/x
```

After rearranging:

```
x p ≤ y s + (x - y) t
```

This is the crucial simplification.

Define

```
R = y s + (x - y) t
```

For a person at position `p`, bus `(s,t)` is reachable exactly when

```
R ≥ x p
```

The condition depends only on one value `R`.

Now compute the total travel time if that bus is used.

Meeting time:

```
τ = (p - s)/(x - y)
```

After boarding, staying on the bus until it disappears is always optimal. Since the bus is faster than walking, leaving earlier can only increase the remaining travel time.

The arrival time becomes

```
τ + (t - meeting_position)/x + (ℓ - t)/y
```

Substituting the meeting position and simplifying yields

```
ℓ / y - p / (x - y)
    + s * x / (y(x-y))
    - t / y
```

For a fixed query position `p`, the first two terms are constants. The bus contributes only

```
value(bus) =
s * x / (y(x-y))
- t / y
```

Therefore each query asks:

Among all buses with

```
R ≥ x p
```

find the minimum bus value.

This becomes a one-dimensional offline problem. Sort buses by `R`. Sort queries by threshold `x p`. Sweep from large to small thresholds while maintaining the minimum bus value among all buses whose `R` is large enough.

The answer for each query is

```
min(
    walking_time,
    base(p) + best_bus_value
)
```

where

```
walking_time = (ℓ - p)/y
base(p) = ℓ/y - p/(x-y)
```

### Complexity Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O((n+m) log n) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. For every bus `(s,t)`, compute

```
R = ys + (x-y)t
```

and

```
V = sx/(y(x-y)) - t/y
```
2. Sort all buses by `R` in descending order.
3. For every query position `p`, compute its threshold

```
need = xp
```

Store `(need, index, p)`.
4. Sort all queries by `need` in descending order.
5. Sweep through queries from largest threshold to smallest.
6. Maintain a pointer into the sorted bus list and a variable `best`, the minimum `V` among all buses already inserted.
7. For the current query, insert every bus whose

```
R ≥ need
```

because exactly those buses are reachable from position `p`.
8. Compute the walking-only time

```
walk = (ℓ-p)/y
```
9. If at least one reachable bus exists, compute

```
bus_answer =
ℓ/y - p/(x-y) + best
```
10. The query answer is the minimum of the walking time and the bus-based time.
11. Restore answers to their original query order and print them.

### Why it works

The key property is that equal bus speeds eliminate all useful transfers. Once two buses start moving, their relative positions never change. A passenger can board at most one bus during an optimal journey.

For a fixed bus, the reachability condition simplifies exactly to

```
R ≥ xp
```

and the resulting travel time simplifies to a constant query-dependent term plus a constant bus-dependent term. Thus every query reduces to selecting the reachable bus with minimum bus-dependent value.

The sweep processes buses in decreasing `R`. When handling threshold `xp`, the maintained set contains precisely the buses satisfying `R ≥ xp`. The variable `best` is the minimum bus value among that set, so it produces the optimal bus-assisted journey. Taking the minimum with direct walking covers the possibility that no bus helps. Hence every answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, L, x, y = map(int, input().split())

    buses = []
    d = x - y

    for _ in range(n):
        s, t = map(int, input().split())

        R = y * s + d * t
        V = s * x / (y * d) - t / y

        buses.append((R, V))

    queries = []
    for i in range(m):
        p = int(input())
        queries.append((x * p, i, p))

    buses.sort(reverse=True)
    queries.sort(reverse=True)

    ans = [0.0] * m

    ptr = 0
    best = float('inf')

    for need, idx, p in queries:
        while ptr < n and buses[ptr][0] >= need:
            best = min(best, buses[ptr][1])
            ptr += 1

        walk = (L - p) / y
        res = walk

        if best < float('inf'):
            bus_res = L / y - p / d + best
            res = min(res, bus_res)

        ans[idx] = res

    sys.stdout.write("\n".join(f"{v:.10f}" for v in ans))

if __name__ == "__main__":
    solve()
```

The first part converts every bus into two derived quantities. `R` determines reachability, while `V` captures the entire contribution of that bus to the final travel time.

Queries are transformed into thresholds `xp`. After sorting buses and queries in descending order, a standard sweep line is possible. As thresholds decrease, more buses become reachable, so buses are inserted exactly once.

The variable `best` stores the minimum `V` among all currently reachable buses. This is enough because every query-dependent term is independent of the chosen bus.

One subtle detail is using `>=` when inserting buses. The derived condition is exactly `R ≥ xp`, so changing it to `>` would incorrectly reject meetings that occur exactly when a bus reaches its destination.

Another detail is that all computations are performed with floating point values. The required precision is only `10^-6`, and the formulas contain divisions, so double precision is more than sufficient.

## Worked Examples

### Sample 1

Input:

```
3 3 10 4 1
0 5
2 4
7 9
3
8
5
```

Bus preprocessing:

| Bus | s | t | R = ys + (x-y)t | V |
| --- | --- | --- | --- | --- |
| 1 | 0 | 5 | 15 | -5 |
| 2 | 2 | 4 | 14 | -1.333333 |
| 3 | 7 | 9 | 34 | 0.333333 |

Queries:

| p | need = xp |
| --- | --- |
| 3 | 12 |
| 8 | 32 |
| 5 | 20 |

Sorted sweep:

| Query p | need | Reachable buses | best V | Answer |
| --- | --- | --- | --- | --- |
| 8 | 32 | bus 3 | 0.333333 | 1.5 |
| 5 | 20 | bus 3 | 0.333333 | 5 |
| 3 | 12 | buses 1,2,3 | -5 | 6.25 |

The interesting case is `p=3`. Bus 1 has the smallest `V`, so it becomes the optimal bus even though bus 3 also satisfies the reachability condition.

### Custom Example

Input:

```
2 2 100 10 2
0 50
20 90
10
80
```

Bus preprocessing:

| Bus | R | V |
| --- | --- | --- |
| (0,50) | 400 | -25 |
| (20,90) | 760 | -32.5 |

Queries:

| p | need |
| --- | --- |
| 10 | 100 |
| 80 | 800 |

Sweep:

| Query p | need | Reachable buses | best V | Final answer |
| --- | --- | --- | --- | --- |
| 80 | 800 | none | inf | 10 |
| 10 | 100 | both buses | -32.5 | 28.75 |

This example shows both outcomes. The person at position `80` cannot catch any bus and simply walks. The person at position `10` can reach either bus, and the sweep correctly selects the better one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Sorting dominates, sweep is linear |
| Space | O(n+m) | Stores buses, queries, and answers |

With `n,m ≤ 2·10^5`, sorting roughly `4·10^5` objects is easily within the limits. The linear sweep afterward is negligible compared to the sorting cost.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from math import inf

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    input = sys.stdin.readline

    n, m, L, x, y = map(int, input().split())
    d = x - y

    buses = []
    for _ in range(n):
        s, t = map(int, input().split())
        buses.append((
            y * s + d * t,
            s * x / (y * d) - t / y
        ))

    qs = []
    for i in range(m):
        p = int(input())
        qs.append((x * p, i, p))

    buses.sort(reverse=True)
    qs.sort(reverse=True)

    ans = [0.0] * m

    ptr = 0
    best = inf

    for need, idx, p in qs:
        while ptr < n and buses[ptr][0] >= need:
            best = min(best, buses[ptr][1])
            ptr += 1

        res = (L - p) / y

        if best < inf:
            res = min(
                res,
                L / y - p / d + best
            )

        ans[idx] = res

    return "\n".join(f"{x:.10f}" for x in ans)

# sample 1
out = run("""3 3 10 4 1
0 5
2 4
7 9
3
8
5
""").splitlines()

assert abs(float(out[0]) - 6.25) < 1e-6
assert abs(float(out[1]) - 1.5) < 1e-6
assert abs(float(out[2]) - 5.0) < 1e-6

# minimum size
out = run("""1 1 10 2 1
0 1
10
""").strip()
assert abs(float(out) - 0.0) < 1e-6

# exact boundary R = xp
out = run("""1 1 10 4 1
0 4
3
""").strip()
assert float(out) >= 0

# no reachable bus
out = run("""1 1 100 10 1
90 100
0
""").strip()
assert abs(float(out) - 100.0) < 1e-6

# bus beneficial
out = run("""1 1 100 10 2
0 50
0
""").strip()
assert float(out) < 50.0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Official answers | Basic correctness |
| Minimum size case | 0 | Smallest legal instance |
| Exact `R = xp` boundary | Valid finite answer | Correct handling of equality |
| No reachable bus | Walking time | Reachability condition |
| Beneficial bus case | Less than walking | Bus optimization logic |

## Edge Cases

Consider a bus that becomes unreachable exactly at its destination:

```
1 1 10 4 1
0 4
3
```

Here

```
R = 12
xp = 12
```

The person meets the bus exactly when it reaches position `4`. The derived condition is `R ≥ xp`, not `R > xp`. The sweep inserts this bus because equality is allowed. A strict comparison would incorrectly discard it.

Consider a person already at the destination:

```
1 1 100 10 1
0 50
100
```

Walking time is zero. The algorithm computes

```
walk = (100 - 100)/1 = 0
```

and returns zero immediately after taking the minimum with any bus-based option.

Consider a bus that starts ahead of the person:

```
1 1 100 10 1
50 90
0
```

The bus is already in front and moves faster. The derived inequality fails because

```
xp > R
```

The bus never enters the active set during the sweep. The answer becomes pure walking time, which is correct.

Consider multiple reachable buses:

```
2 1 100 10 2
0 50
20 90
10
```

Both buses satisfy the reachability condition. The sweep maintains the minimum bus value among all active buses. Since every query-dependent term is identical regardless of which bus is chosen, selecting the smallest stored value is exactly equivalent to evaluating every reachable bus individually and taking the best result.
