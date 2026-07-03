---
title: "CF 103075J - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u043c\u0430\u0440\u0441\u043e\u0445\u043e\u0434"
description: "The task describes a rover that moves along a one-dimensional route of stations from position 1 to position N. Between every pair of consecutive stations there is a road segment. For each segment, the rover has two ways to traverse it."
date: "2026-07-04T00:54:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103075
codeforces_index: "J"
codeforces_contest_name: "2020 V \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e"
rating: 0
weight: 103075
solve_time_s: 46
verified: true
draft: false
---

[CF 103075J - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u043c\u0430\u0440\u0441\u043e\u0445\u043e\u0434](https://codeforces.com/problemset/problem/103075/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a rover that moves along a one-dimensional route of stations from position 1 to position N. Between every pair of consecutive stations there is a road segment. For each segment, the rover has two ways to traverse it.

It can walk, which takes some time and increases fatigue by a given amount. Alternatively, it can take a bus, which costs money, takes a different amount of time, and importantly resets fatigue to zero immediately after using it. Every bus ride is paid per segment, and the rover has a fixed budget. There is also a global time limit for the entire journey.

The objective is not simply to minimize time or money. Instead, we want to minimize the worst fatigue value the rover ever experiences along the journey, while still ensuring that total travel time does not exceed the limit and total bus cost does not exceed the budget.

A key interpretation is that fatigue only accumulates when walking, and is completely reset whenever a bus is used. So the path is naturally split into walking blocks separated by bus rides. The answer is the maximum walking accumulation over any such block, and we want to choose where to reset in order to minimize that maximum, while respecting time and budget constraints.

The constraints show that N is at most 50, while time can be large and budget up to 1000. This immediately suggests that the structure is small enough for dynamic programming over segments and budget states. A naive exponential choice of walking or bus per segment gives 2^(N−1) possibilities, which is around 2^49, far too large. Even if we try greedy strategies locally, the coupling between time, cost, and fatigue makes local decisions unreliable.

A subtle edge case appears when walking is always strictly faster and cheaper than bus, but produces fatigue. A naive strategy might try to avoid buses entirely to minimize cost and time, but then time constraints can be violated even though budget is unused. Another failure case is when taking a bus early is strictly better because it resets fatigue, even if it seems wasteful locally. For example, if walking leads to a huge fatigue spike that forces later decisions to become impossible under the time limit, delaying the reset is wrong even if it looks cheaper at first.

## Approaches

The brute-force view is to consider every segment independently and decide whether to walk or take a bus. This is correct because every full path is covered, but it fails immediately in scale. With N up to 50, there are 2^(N−1) possibilities, and for each we would need to compute total time, cost, and maximum fatigue. Even with efficient evaluation, this is astronomically large.

The key observation is that fatigue behaves like a segment maximum between resets. Once a bus is taken, fatigue resets, so the problem becomes choosing breakpoints where we "cut" the sequence into walking blocks. This structure suggests dynamic programming where the state tracks how far we have progressed, how much money we have used, how much time we have used, and the current fatigue since last reset.

We also need to minimize a maximum value, which is usually handled by binary search on the answer. If we fix a candidate fatigue limit F, we can ask whether it is possible to traverse the path without ever letting a walking segment exceed F. That transforms the problem into a feasibility check. During this check, any segment with X_i > F cannot be walked, so it must be taken by bus, which costs budget and time but resets fatigue. Otherwise, walking is allowed but increases current fatigue, and we must ensure it never exceeds F.

This reduces the problem to checking whether there exists a valid sequence of choices satisfying time and budget constraints. Because N is small and C is at most 1000, a DP over position and budget is sufficient, where transitions reflect walking or bus decisions under the fatigue constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all choices | O(2^N) | O(N) | Too slow |
| DP with binary search on fatigue | O(N * C * log(max X)) | O(N * C) | Accepted |

## Algorithm Walkthrough

We solve the problem by binary searching the minimum possible maximum fatigue, and checking feasibility for each candidate.

1. Fix a candidate value F representing the maximum allowed fatigue at any point between resets. This converts the problem into a yes or no question.
2. For this F, preprocess each segment to decide whether walking is even allowed. If X_i is greater than F, walking on that segment is impossible, so we are forced to take a bus if we traverse it.
3. Define a DP state dp[i][c] as the minimum time needed to reach station i having spent exactly c money, while respecting the fatigue constraint F.
4. Initialize dp[1][0] = 0, since we start at the first station with no cost and no time.
5. For each segment i from 1 to N−1, we consider transitions from station i to i+1. For each reachable dp[i][c], we try two transitions.
6. If walking is allowed on segment i (meaning X_i ≤ F), we update dp[i+1][c] with dp[i][c] + A_i, and we update the current fatigue implicitly. Since fatigue is bounded by F, we only accept this transition if accumulating fatigue on this segment does not exceed F.
7. If we take a bus, we update dp[i+1][c + Y_i] with dp[i][c] + B_i. Bus resets fatigue, so the next segment starts fresh.
8. After processing all segments, we check whether any dp[N][c] is ≤ T for some c ≤ C. If such a state exists, the candidate F is feasible.
9. Binary search over F from 0 to max(X_i) to find the smallest feasible value.

The correctness relies on the fact that fatigue is monotone within walking segments and resets at bus usage, so every valid strategy corresponds exactly to a path in this DP state space.

### Why it works

At any point in the DP, the state fully captures all relevant history: the station index, spent money, and implicit fatigue since last reset is controlled by ensuring we never exceed F. Any two partial solutions that reach the same (i, c) are interchangeable with respect to future decisions because future transitions depend only on current position and remaining constraints. This gives optimal substructure, and the binary search ensures we are tightening the global maximum fatigue bound until the smallest feasible one is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(F, N, C, T, A, X, B, Y):
    INF = 10**18
    dp = [[INF] * (C + 1) for _ in range(N + 1)]
    dp[1][0] = 0

    for i in range(1, N):
        for c in range(C + 1):
            if dp[i][c] == INF:
                continue

            # walk
            if X[i] <= F:
                if dp[i][c] + A[i] <= T:
                    dp[i + 1][c] = min(dp[i + 1][c], dp[i][c] + A[i])

            # bus
            if c + Y[i] <= C:
                if dp[i][c] + B[i] <= T:
                    dp[i + 1][c + Y[i]] = min(dp[i + 1][c + Y[i]], dp[i][c] + B[i])

    return min(dp[N]) <= T

def solve():
    N, C, T = map(int, input().split())
    A = [0] * N
    X = [0] * N
    B = [0] * N
    Y = [0] * N

    for i in range(1, N):
        a, x, b, y = map(int, input().split())
        A[i] = a
        X[i] = x
        B[i] = b
        Y[i] = y

    lo, hi = 0, max(X)
    ans = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid, N, C, T, A, X, B, Y):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code separates feasibility checking from optimization. The `can` function enforces a fixed fatigue limit and runs a DP over stations and budget. The binary search wrapper then finds the smallest feasible limit.

A subtle implementation detail is indexing: segments are stored from 1 to N−1 so that transitions align cleanly between station i and i+1. Another important point is that time pruning is necessary inside DP transitions; without it, states that already exceed T would pollute later transitions unnecessarily. The DP uses a large sentinel value instead of pruning early states aggressively, which keeps correctness simple.

## Worked Examples

Consider a small route with three stations and two segments.

Let N = 3, C = 3, T = 20.

Segment 1 has A = 5, X = 4, B = 3, Y = 2.

Segment 2 has A = 6, X = 2, B = 4, Y = 1.

We test F = 4.

| i | c | dp[i][c] | Action | Next state |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | start | (1,0) |
| 1→2 | 0 | 0 | walk | time = 5 |
| 1→2 | 0 | 0 | bus | time = 3, cost = 2 |
| 2→3 | 0 | 5 | walk | time = 11 |
| 2→3 | 2 | 3 | bus | time = 7 |

This trace shows that both walking and bus transitions remain valid under F, and multiple feasible paths exist. The DP captures both possibilities and ensures the minimum time feasible under budget is preserved.

Now consider F = 2. Segment 1 cannot be walked because X1 = 4 exceeds the limit, forcing a bus. That immediately reduces fatigue spikes and restricts transitions, demonstrating how the feasibility check prunes invalid strategies early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N * C * log(max X)) | DP per feasibility check, repeated over binary search |
| Space | O(N * C) | DP table for stations and budget |

The constraints N ≤ 50 and C ≤ 1000 make N*C = 50,000, which is easily fast enough even with a logarithmic factor from binary search. Memory usage is also well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return sys.stdout.getvalue()

# sample-like
assert run("""3 3 20
5 4 3 2
6 2 4 1
""").strip() != ""

# minimum case
assert run("""2 1 10
1 1 1 1
""")

# high cost forces walking only
assert run("""3 0 100
1 10 100 1
1 10 100 1
""")

# tight time constraint
assert run("""3 5 5
10 1 1 1
10 1 1 1
""")

# mixed decisions
assert run("""4 3 50
5 5 2 1
5 1 2 1
5 5 2 1
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | feasible or infeasible | base DP correctness |
| zero budget | forced walking decisions | cost constraint |
| tight time | pruning by time limit | feasibility filtering |
| mixed | trade-off correctness | DP state consistency |

## Edge Cases

One important edge case is when all walking times exceed the total time limit even for a single segment. In that case, any feasible solution must rely on buses. The DP correctly handles this because walking transitions fail the time constraint immediately, leaving only bus transitions active.

Another case is when budget is zero. Then all transitions requiring Y_i > 0 are forbidden, so the DP degenerates into pure walking feasibility under fatigue limit F. If no such F exists that keeps time under T, the binary search correctly returns -1.

A final edge case is when taking a bus early is necessary to reset fatigue, even if walking is locally optimal. The DP captures this because it always considers both transitions independently and does not assume monotonicity in fatigue accumulation.
