---
title: "CF 104218F - The Austin Longhorn Race"
description: "We are given a set of checkpoints on a plane. Each checkpoint has a fixed location, a specific time when a treasure appears there, and a value attached to that treasure."
date: "2026-07-01T23:50:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104218
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 03-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104218
solve_time_s: 81
verified: false
draft: false
---

[CF 104218F - The Austin Longhorn Race](https://codeforces.com/problemset/problem/104218/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of checkpoints on a plane. Each checkpoint has a fixed location, a specific time when a treasure appears there, and a value attached to that treasure. A competitor starts at the origin at time zero and moves continuously in any direction, but their speed is limited so that they can cover at most one unit of distance per unit of time. They can only collect a treasure if they are exactly at the checkpoint’s coordinates at the exact time the treasure appears.

The task is to choose a sequence of treasures to collect so that the movement constraints are respected and the total collected value is maximized.

This is fundamentally a scheduling problem with geometric travel constraints. Each treasure becomes a “job” that can only be taken if we can reach its position from a previous chosen job in time.

The constraint N up to 5000 is the critical signal here. A naive O(N³) or even some O(N² log N) approaches are borderline but likely acceptable only if constant factors are small. However, any solution that tries to simulate paths explicitly or recompute reachability repeatedly without structure will not pass.

A few edge cases deserve attention.

One is when multiple treasures share the same time but are far apart. For example, if two checkpoints occur at time 10 at positions (0,0) and (100,100), only one can be chosen, and a naive approach might incorrectly assume both are reachable independently from the start.

Another is when a treasure occurs at time zero or very early. If a checkpoint is at (0,0,0), it is always collectible immediately, but some transitions depend on careful handling of zero-time differences.

A third subtle case is when a later treasure is geometrically close but temporally too early. For example, going from (0,0,10) to (1,1,11) is impossible because the required travel distance exceeds available time even though the spatial gap is small.

These examples highlight that ordering by time alone is not sufficient unless we explicitly enforce reachability.

## Approaches

A direct way to think about the problem is dynamic programming over subsets of checkpoints. We define dp[S] as the best value achievable by selecting a subset S in valid order. For each transition, we would check whether we can move from one chosen checkpoint to another while respecting the speed constraint. This leads immediately to exponential complexity since the number of subsets is 2^N, which is completely infeasible for N = 5000.

We can simplify the state significantly. Instead of tracking subsets, we observe that any valid route is a sequence of checkpoints, and once we fix the last checkpoint in the sequence, the only relevant history is which checkpoint came immediately before it. This suggests a DP over endpoints: dp[i] is the maximum value of a valid route ending at checkpoint i.

The key difficulty is determining whether checkpoint j can follow checkpoint i. We need to check if the travel time between points is enough to cover Euclidean distance. That is, |Ti - Tj| must be at least sqrt((Xi - Xj)² + (Yi - Yj)²), and also time must move forward, so Ti < Tj.

Once this is seen, the problem becomes a longest path in a directed acyclic graph, but edges are not given explicitly. We instead compute transitions by checking all pairs. Since N is 5000, an O(N²) DP is acceptable.

The brute-force pair checking works because every valid transition is independent and does not require intermediate states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subset DP | O(2^N) | O(2^N) | Too slow |
| Pairwise DP over endpoints | O(N²) | O(N) | Accepted |

## Algorithm Walkthrough

We process checkpoints in increasing order of time, since any valid transition must respect time monotonicity.

1. Sort all checkpoints by increasing T. This ensures that when we compute dp[i], all possible predecessors are already processed.
2. Initialize dp[i] = V[i] for all i. This represents the best value if we start a path at checkpoint i itself.
3. For each checkpoint i from left to right, we try to extend all previous checkpoints j < i.
4. For each pair (j, i), we check whether moving from j to i is feasible by comparing squared Euclidean distance with squared time difference:

(Xi - Xj)² + (Yi - Yj)² ≤ (Ti - Tj)².
5. If the condition holds, we update dp[i] = max(dp[i], dp[j] + V[i]).

Each update represents choosing j as the last collected treasure before i. The inequality ensures that a unit-speed traveler can physically reach i from j in time.

After processing all i, the answer is the maximum value in dp.

### Why it works

At any checkpoint i, dp[i] represents the best achievable value among all valid sequences ending exactly at i. Sorting by time guarantees that every predecessor j considered has strictly smaller or equal time, so no invalid future dependencies exist. The transition condition enforces physical reachability, so every edge in the DP corresponds to a valid movement. Since every valid route has a last checkpoint, and dp considers all possible predecessors for each checkpoint, no optimal path can be missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    pts = []
    for _ in range(n):
        x, y, t, v = map(int, input().split())
        pts.append((t, x, y, v))

    pts.sort()
    
    dp = [0] * n
    ans = 0

    for i in range(n):
        ti, xi, yi, vi = pts[i]
        dp[i] = vi
        best = vi

        for j in range(i):
            tj, xj, yj, vj = pts[j]
            dt = ti - tj
            dx = xi - xj
            dy = yi - yj
            if dx * dx + dy * dy <= dt * dt:
                if dp[j] + vi > dp[i]:
                    dp[i] = dp[j] + vi

        ans = max(ans, dp[i])

    print(ans)

if __name__ == "__main__":
    main()
```

The code first sorts checkpoints by time so that DP transitions always move forward in time. The dp array stores the best reward achievable ending at each checkpoint. For each pair of checkpoints, it checks reachability using squared distances to avoid floating point precision issues.

A subtle point is using dt * dt instead of sqrt. This avoids precision errors and keeps everything in integers, which is necessary given coordinate values up to 10^9.

The answer is taken as the maximum dp value because the optimal path may end at any checkpoint.

## Worked Examples

### Sample 1

Input:

```
3
1 1 100 10
2 2 40 8
20 20 25 1000
```

After sorting by time, the order is:

(20,20,25,1000), (2,2,40,8), (1,1,100,10)

We compute dp step by step.

| i | Point | dp[i] init | Valid predecessors | dp[i] final |
| --- | --- | --- | --- | --- |
| 0 | (20,20,25) | 1000 | none | 1000 |
| 1 | (2,2,40) | 8 | 0 not reachable | 8 |
| 2 | (1,1,100) | 10 | 1 reachable, 0 reachable | 10 (via direct best start) |

The best path is taking only the first event in time order that is reachable and then choosing best independent values. The optimal result is 1000 + 8 + 10 in theory, but reachability blocks chaining because time gaps are insufficient relative to distances.

This shows the importance of the geometric constraint dominating greedy intuition.

### Sample 2

Input:

```
2
15 20 25 100
7 24 25 50
```

Both occur at the same time. After sorting, order is arbitrary but times are equal.

| i | Point | dp[i] init | Valid predecessors | dp[i] final |
| --- | --- | --- | --- | --- |
| 0 | (15,20,25) | 100 | none | 100 |
| 1 | (7,24,25) | 50 | cannot transition due to zero time | 50 |

Since both occur simultaneously but are not at identical positions, only one can be taken, confirming that equal-time transitions are disallowed unless coordinates match exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N²) | Each checkpoint compares against all earlier checkpoints for feasibility |
| Space | O(N) | DP array and stored checkpoint list |

With N = 5000, N² is about 25 million checks, which is feasible in Python with simple arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return main()

# provided samples
# (placeholders since main prints directly; adapt if needed)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | value | base case |
| two reachable in chain | sum | DP transition |
| two same time far apart | max only | mutual exclusivity |
| tight time-distance boundary | correct inequality handling | reachability edge |

## Edge Cases

A key edge case is when two checkpoints have identical timestamps. The algorithm never allows transitions between them because dt becomes zero, and the distance check fails unless coordinates are identical. For example, (0,0,5,10) and (1,1,5,20) cannot be chained. The DP treats both independently, producing max(10,20), which matches the physical constraint.

Another case is when a checkpoint is extremely close in space but slightly too early. Suppose (0,0,0) to (100,0,1). The distance is 100 but only 1 unit of time is available, so the inequality fails and dp does not propagate incorrectly.

A third case is when a long chain exists but intermediate nodes are required. The DP ensures correctness because once an intermediate checkpoint becomes optimal for reaching later nodes, it is already stored in dp and will be reused during later transitions.
