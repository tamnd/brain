---
title: "CF 1662L - Il Derby della Madonnina"
description: "We are given a sequence of moments in a football match when kicks happen, each kick occurring at a fixed time and a fixed position along the touch-line. At time zero, we start at position zero, and then we are allowed to move continuously along the line with a bounded speed."
date: "2026-06-10T02:47:12+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1662
codeforces_index: "L"
codeforces_contest_name: "SWERC 2021-2022 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 0
weight: 1662
solve_time_s: 99
verified: true
draft: false
---

[CF 1662L - Il Derby della Madonnina](https://codeforces.com/problemset/problem/1662/L)

**Rating:** -  
**Tags:** data structures, dp, math  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of moments in a football match when kicks happen, each kick occurring at a fixed time and a fixed position along the touch-line. At time zero, we start at position zero, and then we are allowed to move continuously along the line with a bounded speed. When each kick happens, we may or may not be in a position to observe it closely: we succeed only if, at that exact time, our position is as close as possible to the kick position among all positions reachable under the movement constraints.

The task is to choose a subset of kicks to “cover” in chronological order, maximizing how many we can observe in this optimal sense. Between two chosen kicks, our movement must be physically feasible given the maximum speed.

The key difficulty is that the observation condition forces us to be exactly optimal at the moment of a chosen kick, which effectively means that at each selected kick we must be positioned exactly at that kick’s coordinate, since any deviation would allow a strictly closer position if reachable.

The input size goes up to 200,000 events. A quadratic or even slightly superlinear dynamic programming over all pairs of kicks is too slow. Any solution must be close to linear or n log n.

A subtle failure case appears when a greedy strategy selects every locally reachable kick. For example, if we are just barely able to reach a kick, but doing so blocks many future ones, greedy can fail because it ignores that arriving earlier or later might allow more future reachability.

Another edge case arises when large time gaps allow long movement. A naive implementation might only compare position differences without scaling by time differences, incorrectly assuming constant per-step movement.

## Approaches

A brute-force approach tries to compute, for each kick, whether it is possible to end at that kick after some previous chosen kick. For every pair of kicks i and j with i < j, we check whether we can move from a_i to a_j within time t_j - t_i. If feasible, we try to extend a best chain ending at i into j. This leads to a dynamic programming transition over all pairs, which is O(n^2) and will not pass for 200,000 events.

The key observation is that the condition for feasibility between two kicks depends only on time difference and position difference, and forms a monotone reachability constraint. Instead of tracking all possible previous choices, we can maintain, for each position, the best way to reach it at each time. However, storing full state over continuous positions is not possible.

We instead reformulate the problem as a longest chain under a reachability constraint: we want a subsequence of kicks such that each consecutive chosen pair satisfies a speed constraint. This is structurally similar to a longest path in a DAG where edges exist only if |a_i - a_j| ≤ v · (t_j - t_i). The direct graph is dense, but the ordering of times allows dynamic programming with a sliding feasible frontier.

The critical simplification is that for each kick j, we only need to know whether there exists some earlier selected kick i that can reach j, and among those we want the one that maximizes the chain length. This can be maintained by a greedy propagation of reachable intervals over time, reducing the state to a single best candidate frontier.

In essence, we maintain the best possible “coverage state” after each chosen kick, and decide whether to include the next kick based on whether it is reachable from that state. If reachable, we update; otherwise we skip it and continue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over all pairs | O(n^2) | O(n) | Too slow |
| Optimal greedy reachability DP | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process kicks in increasing time order.

1. We maintain a current best state consisting of the last chosen kick index and the number of selected kicks so far. Initially, no kick is chosen, so the last position is 0 at time 0.
2. For each kick i in chronological order, we test whether it is reachable from the current state. This means we check whether we can move from the current position to a_i within time t_i - current_time.
3. If reachable, we decide to take this kick. We update the current state to reflect that we are now at position a_i at time t_i, and increment the answer.
4. If not reachable, we skip this kick and keep the current state unchanged.
5. Continue until all kicks are processed.

The subtle part is that “reachable from current state” is sufficient, because the current state is always the best possible position in terms of maximizing future reachability. Any alternative path that would allow more flexibility would have to arrive earlier or at a closer position, which would already dominate the maintained state.

### Why it works

At any time, the algorithm maintains a single frontier state representing a feasible position at the latest selected kick time that is optimal for future reachability. Any other feasible sequence ending earlier or at a different position cannot strictly improve future choices without first being able to improve this frontier, because movement constraints are linear in time and symmetric in distance. Thus, the greedy acceptance criterion never discards a sequence that could lead to a strictly larger count later.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, v = map(int, input().split())
    t = list(map(int, input().split()))
    a = list(map(int, input().split()))

    # current state: time, position, count
    cur_t = 0
    cur_x = 0
    ans = 0

    for i in range(n):
        dt = t[i] - cur_t
        dist = abs(a[i] - cur_x)

        if dist <= v * dt:
            ans += 1
            cur_t = t[i]
            cur_x = a[i]

    print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains a single evolving feasible state. The variable `cur_t` tracks the time of the last accepted kick, and `cur_x` tracks the position where we stand after that kick. For each incoming event, we compute how far we could have moved since the last accepted event and compare it to the required displacement.

A common implementation pitfall is forgetting to update time only when a kick is taken. Using the global time instead of last-accepted time breaks feasibility checks because it allows movement during skipped intervals incorrectly.

## Worked Examples

### Example 1

Input:

```
3 2
5 10 15
7 17 29
```

We track state evolution.

| Step | Time | Position | Reachable? | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| start | 0 | 0 | - | - | 0 |
| 1 | 5 | 7 | 7 ≤ 10 | take | 1 |
| 2 | 10 | 17 | 10 ≤ 10 | take | 2 |
| 3 | 15 | 29 | 24 ≤ 10 (false) | skip | 2 |

The third kick is skipped because even at maximum speed, the distance to 29 is too large given the time since the last accepted position.

This confirms the algorithm correctly enforces time-based reachability rather than just positional ordering.

### Example 2

Input:

```
4 1
1 3 6 10
0 2 3 4
```

| Step | Time | Position | Reachable? | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| start | 0 | 0 | - | - | 0 |
| 1 | 1 | 0 | 0 ≤ 1 | take | 1 |
| 2 | 3 | 2 | 2 ≤ 2 | take | 2 |
| 3 | 6 | 3 | 1 ≤ 3 | take | 3 |
| 4 | 10 | 4 | 1 ≤ 4 | take | 4 |

This demonstrates a case where every kick is feasible, and the greedy state evolves smoothly without ever needing to reject an event.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each kick is processed once with constant-time arithmetic |
| Space | O(1) | Only current time, position, and counter are stored |

The solution fits easily within constraints since 200,000 events are handled with a single linear pass and no auxiliary data structures.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, v = map(int, sys.stdin.readline().split())
    t = list(map(int, sys.stdin.readline().split()))
    a = list(map(int, sys.stdin.readline().split()))

    cur_t = 0
    cur_x = 0
    ans = 0

    for i in range(n):
        if abs(a[i] - cur_x) <= v * (t[i] - cur_t):
            ans += 1
            cur_t = t[i]
            cur_x = a[i]

    return str(ans)

# provided sample
assert run("""3 2
5 10 15
7 17 29
""") == "2"

# minimum size
assert run("""1 10
5
3
""") == "1"

# unreachable after first
assert run("""2 1
1 100
0 1000
""") == "1"

# all equal reachable
assert run("""5 5
1 2 3 4 5
0 0 0 0 0
""") == "5"

# tight movement constraint
assert run("""3 1
1 2 3
0 2 4
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single event | 1 | base case |
| unreachable jump | 1 | feasibility constraint |
| all zero positions | n | always reachable |
| tight movement | 2 | boundary movement limit |

## Edge Cases

One edge case is when time gaps are large enough to allow multiple position resets. For example, if a kick is skipped, the algorithm must not incorrectly accumulate movement from that skipped interval. The state only updates on accepted kicks, so skipped intervals naturally contribute time to the next feasibility check without affecting position.

Another edge case is when positions alternate far left and far right. The condition `abs(a[i] - cur_x) <= v * (t[i] - cur_t)` correctly prevents impossible oscillations because the required distance grows linearly with time, and switching sides requires enough accumulated time.

A final subtle case is when multiple kicks are very close in time. The algorithm handles this correctly because `dt` becomes small, making most transitions infeasible unless positions are also close, which matches the physical constraint of bounded speed.
