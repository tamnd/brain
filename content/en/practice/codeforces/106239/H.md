---
title: "CF 106239H - \u80fd\u91cf\u6c47\u805a"
description: "We are standing on a line of positions labeled from 0 to n. Position 0 is the start and has no reward, while every position from 1 to n contributes a fixed energy value if we land on it. We begin at position 0 and want to reach position n. Movement is constrained in two ways."
date: "2026-06-19T14:09:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106239
codeforces_index: "H"
codeforces_contest_name: "2025\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66\u65b0\u751f\u8d5b(\u51b3\u8d5b)"
rating: 0
weight: 106239
solve_time_s: 47
verified: true
draft: false
---

[CF 106239H - \u80fd\u91cf\u6c47\u805a](https://codeforces.com/problemset/problem/106239/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are standing on a line of positions labeled from 0 to n. Position 0 is the start and has no reward, while every position from 1 to n contributes a fixed energy value if we land on it. We begin at position 0 and want to reach position n.

Movement is constrained in two ways. Each move is either a step of length 1 or 2 forward. However, we cannot take two consecutive 1-step moves. This creates a dependency between the last move and the next allowed move. Every time we land on a position i, we immediately collect Ei.

The task is to choose a valid sequence of jumps from 0 to n that respects the “no two consecutive 1-steps” rule and maximizes the total collected energy.

The constraint n ≤ 100000 implies we need at least linear or near-linear time. Any solution that enumerates paths is exponential because at each position we branch into two move types with a global dependency, and the number of valid sequences grows like a Fibonacci-style recurrence but with additional state, so brute force is impossible. Even a naive dynamic programming that tries all sequences without compressing state would repeat identical subproblems.

A subtle edge case comes from the restriction on consecutive 1-steps. If a solution forgets this dependency, it will incorrectly treat the problem as a standard “climb 1 or 2 steps” DP and overcount invalid transitions. Another edge case is when n is small, especially n = 1 or n = 2, where the rule about “no consecutive 1-step” does not fully activate and careless transitions can index out of bounds or miss the only valid path.

For example, if n = 2 and E = [100, 1], the optimal path is 0 → 2 if allowed, but depending on interpretation, only valid moves must be checked carefully since 0 → 1 → 2 is forbidden due to consecutive 1-steps, so the answer is E2 = 1.

## Approaches

A brute-force approach tries every possible sequence of jumps starting from 0, tracking the current position and whether the last move was a 1-step or a 2-step. At each state, we branch into valid moves and accumulate energy. This is correct because it explores all legal paths and sums rewards precisely according to landing positions. The issue is that the number of paths grows exponentially with n. Even with pruning invalid consecutive 1-step transitions, the state space still explodes because each position can be reached in multiple ways with different histories, leading to repeated recomputation.

The key observation is that the only historical information that matters is whether the previous move was a 1-step or a 2-step. The entire problem collapses into a dynamic programming over positions with two states. Once we encode this state, transitions become local and independent of full history. This transforms the problem into a linear DP where each position is computed once per state.

We define dp[i][0] as the maximum energy when reaching i with the last move being a 1-step, and dp[i][1] as the maximum energy when reaching i with the last move being a 2-step. The constraint forbids transitions from dp[i][0] to i+1 with another 1-step, which naturally enforces the rule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) recursion depth | Too slow |
| Optimal DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a DP table indexed by position and last move type.

1. Initialize all states as negative infinity except the start state. At position 0, we conceptually start with a “no previous move” state, which allows either a 1-step or 2-step as the first action. This avoids incorrectly restricting the first jump.
2. From each position i, consider transitions depending on how we arrived there. If we arrived via a 1-step, then the next move must be a 2-step, so we only transition to i+2. If we arrived via a 2-step, we may go to i+1 or i+2. This directly encodes the rule and prevents invalid consecutive 1-step sequences.
3. When transitioning from i to j, we add Ej to the DP value because we collect energy upon landing. This ensures every landing contribution is accounted for exactly once.
4. We process positions in increasing order from 0 to n, because all transitions go forward, so earlier states are fully finalized before being used.
5. The answer is the maximum of dp[n][0] and dp[n][1], since reaching n could happen with either last move type.

Why it works is tied to a state compression argument. Any valid path ending at i is fully characterized by its best score and the last move type. No other historical detail affects future legality or reward, so storing only these two states preserves optimal substructure. Every transition preserves feasibility, and every feasible path is representable in the DP, so no candidate solution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    E = [0] + list(map(int, input().split()))

    NEG = -10**18

    dp = [[NEG, NEG] for _ in range(n + 1)]

    dp[0][0] = dp[0][1] = 0

    for i in range(n + 1):
        for last in (0, 1):
            if dp[i][last] == NEG:
                continue

            if i + 1 <= n:
                if last == 1:
                    dp[i + 1][0] = max(dp[i + 1][0], dp[i][last] + E[i + 1])
            if i + 2 <= n:
                dp[i + 2][1] = max(dp[i + 2][1], dp[i][last] + E[i + 2])

    print(max(dp[n][0], dp[n][1]))

if __name__ == "__main__":
    solve()
```

The DP table explicitly separates the two allowed “last move” states. The transition logic enforces the rule: after a 1-step (last = 0), only a 2-step is allowed, so we only update dp[i+2][1]. After a 2-step (last = 1), both transitions are valid. The energy is added at the moment of arrival, ensuring each position contributes exactly once per path.

The initialization dp[0][0] = dp[0][1] = 0 is a modeling trick that allows the first move to behave uniformly without special-casing. Since position 0 has no energy, it does not distort the sum.

## Worked Examples

Consider the sample input n = 5, E = [1, 10, 10, 10, 1].

We track only reachable states.

| i | dp[i][last=1] (last 2-step) | dp[i][last=0] (last 1-step) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 2 | 10 | - |
| 4 | 20 | - |
| 5 | - | 21 |

The transition is 0 → 2 → 4 → 5. Each time we land, we add energy: 10 + 10 + 1 = 21. The table shows that only 2-step transitions dominate because the rule restricts consecutive 1-steps heavily.

Now consider a smaller case n = 4, E = [5, 100, 5, 100].

| i | dp[i][last=1] | dp[i][last=0] |
| --- | --- | --- |
| 0 | 0 | 0 |
| 2 | 100 | - |
| 3 | - | 105 |
| 4 | 200 | - |

Here the optimal path is 0 → 2 → 4, collecting 100 + 100 = 200. Any attempt to insert a 1-step early blocks another 1-step and reduces flexibility, which the DP correctly captures.

The traces confirm that the state split correctly represents how future move options depend only on the last step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position processes constant transitions for two states |
| Space | O(n) | DP table stores two states per position |

The algorithm runs in linear time over n up to 100000, which fits comfortably within typical constraints. Memory usage is also linear and small enough for the limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(sys.stdin.readline())
    E = [0] + list(map(int, sys.stdin.readline().split()))

    NEG = -10**18
    dp = [[NEG, NEG] for _ in range(n + 1)]
    dp[0][0] = dp[0][1] = 0

    for i in range(n + 1):
        for last in (0, 1):
            if dp[i][last] == NEG:
                continue
            if i + 1 <= n and last == 1:
                dp[i + 1][0] = max(dp[i + 1][0], dp[i][last] + E[i + 1])
            if i + 2 <= n:
                dp[i + 2][1] = max(dp[i + 2][1], dp[i][last] + E[i + 2])

    return str(max(dp[n][0], dp[n][1]))

# provided sample
assert run("5\n1 10 10 10 1\n") == "21"

# minimum n
assert run("1\n5\n") == "5"

# n = 2, must avoid invalid 1-1
assert run("2\n100 1\n") == "1"

# all equal values
assert run("4\n10 10 10 10\n") == "30"

# alternating high values
assert run("5\n1 100 1 100 1\n") == "201"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single value | 5 | base case correctness |
| n=2 [100,1] | 1 | forbidding 1+1 path |
| uniform array | 30 | consistency of DP accumulation |
| alternating peaks | 201 | correct preference for 2-step structure |

## Edge Cases

For n = 1, the only valid move is directly to position 1. The DP initializes dp[0][*] = 0 and allows a 2-step, but i+2 is invalid, so only i+1 transition is used if last state allows it. The algorithm correctly produces E1.

For n = 2 with E = [100, 1], the best path avoids 0 → 1 → 2 because after a 1-step, another 1-step is forbidden. The DP only allows 0 → 2 via a 2-step, yielding value 1, which matches the optimal constraint-aware solution.

For cases where all values are identical, the DP naturally prefers more 2-step jumps because they do not reduce future mobility. For example n = 4, all E = 10 yields 0 → 2 → 4 for total 20, while invalid chains are never constructed due to state restriction, and the DP correctly avoids overcounting.

These cases confirm that the state encoding fully captures the movement restriction without needing deeper history.
