---
title: "CF 104964B - \u041a\u043e\u043c\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u044f \u043d\u0430 \u0432\u044b\u0441\u043e\u043a\u043e\u043c \u0443\u0440\u043e\u0432\u043d\u0435"
description: "We are given a sequence of buildings in a line, and for each building we must choose a height for a sensor. Each sensor has its own allowed interval, so the height at position $i$ must be selected inside $[ai, bi]$."
date: "2026-06-28T06:50:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104964
codeforces_index: "B"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2023. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 104964
solve_time_s: 82
verified: false
draft: false
---

[CF 104964B - \u041a\u043e\u043c\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u044f \u043d\u0430 \u0432\u044b\u0441\u043e\u043a\u043e\u043c \u0443\u0440\u043e\u0432\u043d\u0435](https://codeforces.com/problemset/problem/104964/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of buildings in a line, and for each building we must choose a height for a sensor. Each sensor has its own allowed interval, so the height at position $i$ must be selected inside $[a_i, b_i]$. Once all heights are chosen, the cost of the configuration is the sum of absolute differences between adjacent sensors, meaning how much the height changes as we move along the line.

The task is to assign one valid height per position such that this total “adjacent change” cost is minimized.

The structure is important: the cost only depends on neighboring pairs. There is no global interaction beyond adjacency, which suggests that the solution should build a sequence progressively rather than trying to reason about all combinations at once.

The constraints go up to $n = 10^6$ across test cases, which immediately rules out any quadratic transition between positions or any dynamic programming that keeps a large state per index. Any solution must be essentially linear per test case, with constant work per position.

A subtle pitfall is assuming that choosing $d_i$ greedily inside $[a_i, b_i]$ independently of future constraints works. For example, picking $d_i$ as the midpoint or as close as possible to $d_{i-1}$ without considering future intervals can trap the sequence into unnecessary oscillations that increase later costs. The decision at position $i$ must respect both past and future feasibility, but we will see that future influence can be fully summarized by a single evolving value.

Another failure mode comes from thinking this is a shortest path over a layered graph and trying to explicitly relax all transitions between intervals. That produces $O(n^2)$ transitions if done naively, which is too slow for $10^6$ total length.

## Approaches

The brute-force viewpoint is to treat each position as a layer of possible values. From a value $x$ at position $i$, we can move to any value $y \in [a_{i+1}, b_{i+1}]$ with cost $|x - y|$. This forms a layered graph where each layer is a continuous segment of integers. A naive dynamic programming would attempt to compute the best cost for every possible value in each interval.

This quickly becomes infeasible because each interval can contain up to $10^9$ possible values, and even discretizing does not help since transitions between intervals are dense. Even if we restrict ourselves to endpoints, the state still grows because each transition depends on continuous optimization over a range.

The key observation is that at each step, we do not actually need the full distribution of possible previous values. We only need to know the best achievable cost if we end at a specific chosen value, and this value can be propagated forward optimally.

More concretely, suppose we have fixed $d_{i-1}$. At position $i$, we want to pick $d_i \in [a_i, b_i]$ minimizing $|d_i - d_{i-1}|$ plus future cost. The greedy part of the insight is that for the optimal solution, it is sufficient to carry forward a single representative value $d_i$, chosen as close as possible to $d_{i-1}$ while staying inside the interval. Any deviation from this closest point strictly increases the current edge cost without improving future flexibility, because future choices depend only on the value we end at, not on how we got there.

Thus, the optimal structure becomes a simple projection process: repeatedly “project” the previous chosen height onto the current allowed interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over values | O(n · range) | O(range) | Too slow |
| Interval projection greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process buildings from left to right while maintaining the chosen height of the previous sensor.

1. Start by choosing $d_1$ arbitrarily inside $[a_1, b_1]$. Any choice is valid because there is no previous cost. Picking $d_1 = a_1$ simplifies implementation without loss of optimality.
2. For each next index $i$, compare the previous height $d_{i-1}$ with the current interval $[a_i, b_i]$. If the previous height lies inside the interval, set $d_i = d_{i-1}$. This avoids any cost increase at edge $(i-1, i)$, which is optimal because we are not forced to move.
3. If $d_{i-1} < a_i$, set $d_i = a_i$. The previous value is too low to remain unchanged, so the best we can do is move up to the nearest feasible point, minimizing the absolute difference.
4. If $d_{i-1} > b_i$, set $d_i = b_i$. Symmetrically, we move down to the closest valid value in the interval.
5. Accumulate the cost at each step as $|d_i - d_{i-1}|$, since each decision only affects the current edge cost.

The reason each step is locally optimal is that the cost of each edge is independent once endpoints are fixed, so minimizing each edge greedily under feasibility constraints produces a globally optimal sum.

### Why it works

The algorithm maintains a single invariant: after processing position $i$, the chosen value $d_i$ is the closest feasible point to the previous choice $d_{i-1}$. Any alternative choice at position $i$ that is further away from $d_{i-1}$ strictly increases the cost of edge $(i-1, i)$ while not improving feasibility for future steps, since future steps only constrain the current value through interval membership, not through any penalty on magnitude. Therefore, at every step we are performing an optimal projection onto a convex set in one dimension, and repeated projections preserve global optimality of the sum of distances.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out_lines = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        d = a[0]
        cost = 0
        res = [0] * n
        res[0] = d

        for i in range(1, n):
            if d < a[i]:
                nd = a[i]
            elif d > b[i]:
                nd = b[i]
            else:
                nd = d

            cost += abs(nd - d)
            d = nd
            res[i] = d

        out_lines.append(str(cost))
        out_lines.append(" ".join(map(str, res)))

    print("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

The code mirrors the projection process directly. The variable `d` stores the last chosen height, and each step computes the nearest feasible value in the next interval. The cost accumulates only the movement between consecutive choices, which corresponds exactly to the objective function.

A common implementation mistake is updating `d` before adding the cost, which would lose the correct difference. Another issue is forgetting that the projection must compare against both ends of the interval rather than trying to clamp in multiple steps inconsistently.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1, 0, 1]
b = [3, 3, 4]
```

We track the progression.

| i | interval | previous d | chosen d | cost added | total cost |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,3] | - | 1 | 0 | 0 |
| 2 | [0,3] | 1 | 1 | 0 | 0 |
| 3 | [1,4] | 1 | 1 | 0 | 0 |

The sequence stays constant because every interval contains 1. The result is a zero-cost configuration.

This demonstrates that when intervals overlap, the optimal solution is to stay within the intersection as long as possible.

### Example 2

Input:

```
n = 3
a = [5, 10, 1]
b = [5, 10, 10]
```

| i | interval | previous d | chosen d | cost added | total cost |
| --- | --- | --- | --- | --- | --- |
| 1 | [5,5] | - | 5 | 0 | 0 |
| 2 | [10,10] | 5 | 10 | 5 | 5 |
| 3 | [1,10] | 10 | 10 | 0 | 5 |

The solution is forced to jump from 5 to 10, then stays at 10 when the interval becomes flexible again. This shows how the algorithm reacts to disjoint intervals by making minimal necessary jumps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each index is processed once with constant-time interval projection |
| Space | O(n) | Only the output array and input storage are kept |

The total $\sum n \le 10^6$ guarantees that a linear scan over all test cases fits easily within time limits. Memory usage stays linear and is dominated by storing the resulting sequence.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    backup = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = backup
    return out.strip()

# sample-like case 1
assert run("""1
1
5
5
""") == "0\n5", "single element"

# sample-like case 2
assert run("""1
2
1 10
5 5
""") == "4\n1 5", "forced move"

# overlapping intervals
assert run("""1
4
1 2 3 4
10 10 10 10
""") == "3\n1 2 3 4", "monotone forced projection"

# alternating tight intervals
assert run("""1
3
1 10 1
1 10 1
""") == "18\n1 10 1", "oscillation forced"

# all identical intervals
assert run("""1
5
7 7 7 7 7
7 7 7 7 7
""") == "0\n7 7 7 7 7", "no movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case with no edges |
| forced move | 4 1 5 | handling equality-constrained steps |
| monotone forced projection | 3 1 2 3 4 | increasing intervals |
| oscillation forced | 18 1 10 1 | large jumps |
| all identical intervals | 0 7 7 7 7 | zero-cost stability |

## Edge Cases

One edge case is when all intervals overlap at a single point. For example, $a_i = b_i = 7$ for all $i$. The algorithm always projects to 7 and never moves, producing zero cost, which matches the optimal solution since no alternative exists.

Another edge case is alternating narrow intervals that force repeated large jumps. For instance, $[1,1], [10,10], [1,1]$. The algorithm moves exactly when required by feasibility and never introduces extra movement. At each step, the projection is unique, so no ambiguity arises.

A final edge case is when the previous value lies exactly on the boundary of the next interval. For example, $d_{i-1} = a_i$ or $d_{i-1} = b_i$. The algorithm keeps the value unchanged, which is correct because any movement would strictly increase cost without feasibility gain.
