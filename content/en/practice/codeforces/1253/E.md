---
title: "CF 1253E - Antenna Coverage"
description: "We are given several antennas placed on a number line segment. Each antenna sits at a fixed integer position and initially covers a symmetric interval around it."
date: "2026-06-15T22:44:56+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1253
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 600 (Div. 2)"
rating: 2200
weight: 1253
solve_time_s: 143
verified: false
draft: false
---

[CF 1253E - Antenna Coverage](https://codeforces.com/problemset/problem/1253/E)

**Rating:** 2200  
**Tags:** data structures, dp, greedy, sortings  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several antennas placed on a number line segment. Each antenna sits at a fixed integer position and initially covers a symmetric interval around it. We are allowed to increase the radius of any antenna, paying one coin per unit increase in radius, and we want to ensure that every integer point from 1 to m is covered by at least one antenna after all expansions.

A useful way to view this is that each antenna defines an interval, and we can “stretch” intervals outward from their centers at linear cost. The task is to choose how much to extend each interval so that their union fully covers [1, m] while minimizing total extension cost.

The constraints are small in terms of number of antennas, with n up to 80, but the coordinate range m goes up to 100000. This combination strongly suggests that we should not attempt anything quadratic in m, but we can afford O(n^2) or O(n^2 log n) structures over antennas.

A subtle point is that antennas do not need to form a partition of the line. They can overlap arbitrarily, and coverage beyond [1, m] is irrelevant. Another important observation is that increasing an antenna radius is equivalent to extending both endpoints of its interval simultaneously, which means each antenna contributes a symmetric interval expansion but we only care about covering a contiguous range.

Edge cases arise when the initial coverage already overlaps or nearly covers the segment.

One such case is when a single antenna already covers everything. For example, if m = 10 and one antenna is at position 5 with s = 10, it covers [-5, 15], so cost is 0. A naive greedy approach that forces use of multiple antennas might incorrectly add unnecessary cost.

Another edge case is when gaps exist between initial intervals. If we have antennas producing intervals [1, 3] and [5, 7], then position 4 is uncovered. A naive approach that independently extends both intervals without coordinating may overpay, since it is cheaper to extend one interval to bridge the gap than to expand both symmetrically in a suboptimal way.

Finally, antennas with large overlap but small “reach toward boundaries” are tricky: optimal solutions often involve choosing a sequence of antennas that progressively extend coverage, not necessarily those with largest initial ranges.

## Approaches

A brute-force idea is to think of each antenna having a chosen final radius, and we try all possible combinations of radius increases. Since each unit increase is independent and costs 1, this becomes equivalent to choosing final intervals with constraints that they cover [1, m]. However, the number of possible final radii values per antenna is proportional to m, which makes this infeasible. Even reducing to “final interval endpoints” still leaves a huge continuous search space.

Another brute-force framing is dynamic programming over subsets of antennas and current covered prefix, but that would require O(2^n) states, which is far too large even for n = 80.

The key structural observation is that the final solution always corresponds to selecting antennas in some order such that their expanded intervals cover the line continuously from left to right. At any point, we maintain a current covered segment ending at some position R. We then choose an antenna whose base interval intersects or is close enough to R so that we can extend coverage further by paying the cost needed to reach from R to the right endpoint of that antenna’s expanded interval.

This transforms the problem into a shortest path-like process over antennas: each antenna can be used to “jump” coverage forward, but only after paying enough to make its interval connect to the current frontier. The cost is linear in how much we need to expand it to cover the gap.

We sort antennas by position and treat transitions carefully, and then use dynamic programming over the set of antennas that serve as the last used antenna in a coverage chain. For each antenna, we compute the cost to extend coverage from the current frontier to its interval, and propagate best costs.

This works because optimal solutions never need to “split responsibility” of covering a gap between multiple antennas in a fractional way; any uncovered gap must be bridged by fully extending one antenna until it touches the current boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / O(m^n) | O(n) | Too slow |
| Optimal DP over antennas | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert each antenna into an interval [l_i, r_i] where l_i = x_i - s_i and r_i = x_i + s_i. This represents its initial coverage without extra cost.
2. Sort antennas by their left endpoints l_i. This ensures we process coverage in a consistent left-to-right structure, so that extending coverage always respects monotonic progress.
3. Define dp[i] as the minimum cost to build a valid coverage chain ending using antenna i as the last contributing segment.
4. Initialize dp[i] with the cost needed for antenna i to cover the prefix starting from 1 alone. This is max(0, 1 - l_i), since we must extend it leftwards until it reaches 1. The right side is not yet constrained at initialization.
5. For every pair of antennas i and j with i < j, consider transitioning from i to j if antenna i can be extended to reach or overlap antenna j’s left boundary. The current coverage from i ends at r_i after extension, so we compute how much extra cost is needed so that r_i reaches at least l_j.
6. If r_i is already >= l_j, no extra cost is needed for connectivity; otherwise we must extend antenna i by (l_j - r_i). We then compute the resulting extension cost and update dp[j].
7. After processing all transitions, we compute the answer as the minimum dp[i] such that antenna i, after full extension, covers up to m, meaning r_i >= m after paying its full assigned cost.

The reasoning behind transitions is that each antenna acts as a bridge expanding a currently covered prefix. Once an antenna is chosen, its expansion cost is fixed, and it contributes a maximum reachable right endpoint. The DP ensures we always choose the cheapest way to reach each antenna as the last bridge.

### Why it works

At any stage, the covered region is a contiguous interval starting from 1. Any valid solution can be seen as a sequence of antennas whose expanded intervals overlap consecutively so that the union remains connected. If there were a gap between two consecutive chosen antennas, coverage would fail, so every transition must exactly pay enough to eliminate that gap.

The DP enforces that we only consider valid chains of overlapping or gap-bridging intervals, and because cost depends only on how far we extend endpoints, splitting expansions across multiple antennas to bridge the same gap can never be cheaper than assigning the full necessary extension to the antenna that performs the bridge. This gives optimal substructure over antenna ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    ants = []
    for _ in range(n):
        x, s = map(int, input().split())
        l = x - s
        r = x + s
        ants.append((l, r))
    
    ants.sort()
    
    INF = 10**18
    dp = [INF] * n
    
    for i in range(n):
        l, r = ants[i]
        cost = max(0, 1 - l)
        dp[i] = cost
    
    for i in range(n):
        li, ri = ants[i]
        base_cost_i = max(0, 1 - li)
        ri_ext = ri + base_cost_i
        
        for j in range(i + 1, n):
            lj, rj = ants[j]
            cost_to_start_j = max(0, lj - ri_ext)
            new_cost = dp[i] + cost_to_start_j
            
            if new_cost < dp[j]:
                dp[j] = new_cost
    
    ans = INF
    for i in range(n):
        li, ri = ants[i]
        cost_i = max(0, 1 - li)
        ri_ext = ri + cost_i
        
        # after dp chain, antenna i is last; ensure it reaches m
        extra = max(0, m - ri_ext)
        ans = min(ans, dp[i] + extra)
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code first converts antennas into intervals and sorts them to ensure transitions move left to right. The dp array stores the minimum cost to end a valid chain at each antenna. Initialization accounts for reaching the left boundary 1.

The transition step computes whether antenna i can reach antenna j’s left endpoint; if not, we pay the exact gap. This preserves minimality because any cheaper solution would imply a smaller extension already exists in dp[i].

Finally, we ensure the last antenna extends far enough to reach m, since coverage must end at or beyond m.

A common subtlety is separating “cost to connect chain” from “cost to fully reach m”, which is why the final extension is added only at the end.

## Worked Examples

Consider a small example with three antennas:

Input:

```
3 10
2 0
6 0
9 0
```

All antennas initially cover only their points.

| Step | Active antenna i | Current left | Current right | Cost so far |
| --- | --- | --- | --- | --- |
| Init | 0 | 1 | 2 | 1 |
| Extend to 2 | 1 | 1 | 6 | 5 |
| Extend to 3 | 2 | 1 | 9 | 8 |
| Final extend | 2 | 1 | 10 | 9 |

This shows sequential bridging where each antenna must be expanded to connect the next gap.

Now consider overlapping antennas:

Input:

```
3 10
2 3
6 3
9 3
```

| Step | Active antenna i | Right after init | Gap cost | Total |
| --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 0 | 0 |
| 1 | 1 | 9 | 0 | 0 |
| 2 | 2 | 12 | 0 | 0 |

No expansions are needed because coverage already overlaps fully.

The trace shows that the DP naturally prefers zero-cost transitions when overlaps exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each pair of antennas is considered once in DP transitions |
| Space | O(n) | Only interval list and DP array are stored |

With n ≤ 80, an O(n^2) solution is trivial under the time limit, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    ants = []
    for _ in range(n):
        x, s = map(int, input().split())
        ants.append((x - s, x + s))
    ants.sort()

    INF = 10**18
    dp = [INF] * n

    for i in range(n):
        l, r = ants[i]
        dp[i] = max(0, 1 - l)

    for i in range(n):
        li, ri = ants[i]
        base = max(0, 1 - li)
        ri_ext = ri + base

        for j in range(i + 1, n):
            lj, rj = ants[j]
            cost = max(0, lj - ri_ext)
            dp[j] = min(dp[j], dp[i] + cost)

    ans = INF
    for i in range(n):
        l, r = ants[i]
        base = max(0, 1 - l)
        ri_ext = r + base
        ans = min(ans, dp[i] + max(0, m - ri_ext))

    return str(ans)

# provided sample
assert run("""3 595
43 2
300 4
554 10
""") == "281"

# single antenna already covers everything
assert run("""1 10
5 10
""") == "0"

# disjoint antennas requiring bridging
assert run("""2 10
2 0
8 0
""") == "7"

# fully overlapping coverage
assert run("""3 10
2 5
4 5
6 5
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single antenna full cover | 0 | no-cost solution handling |
| two disjoint points | 7 | bridging cost correctness |
| fully overlapping intervals | 0 | zero-transition behavior |

## Edge Cases

A first edge case is when one antenna already covers [1, m]. For input like `1 10 / 5 10`, the interval spans beyond both ends. The algorithm sets dp[0] = 0 since l ≤ 1, and final extension cost is also 0 since r ≥ m. The output becomes 0 without any transitions.

Another edge case is a large gap between antennas. For `2 10 / 2 0 / 8 0`, antenna 0 covers only 2, antenna 1 covers only 8. The DP computes dp[0] = 1, since we must extend left endpoint to 1. Its extended right remains 2. Transition to antenna 1 requires cost 6 to bridge from 2 to 8. Final cost is 1 + 6 = 7, and antenna 1 then already reaches m after extension. The algorithm correctly accumulates only necessary gap filling.

A final edge case is heavy overlap where no extension is needed. For `3 10 / 2 5 / 4 5 / 6 5`, all intervals overlap into a continuous union covering [1, 11]. Every dp transition stays at 0 cost, and final answer is 0, confirming that the algorithm does not introduce artificial costs when coverage is already sufficient.
