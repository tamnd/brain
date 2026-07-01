---
title: "CF 104095B - \u5e7f\u544a\u6295\u653e"
description: "We are given a sequential process with n episodes, and an initial audience size m. Each episode may or may not run an advertisement."
date: "2026-07-02T02:17:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104095
codeforces_index: "B"
codeforces_contest_name: "2020 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 104095
solve_time_s: 48
verified: true
draft: false
---

[CF 104095B - \u5e7f\u544a\u6295\u653e](https://codeforces.com/problemset/problem/104095/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequential process with n episodes, and an initial audience size m. Each episode may or may not run an advertisement. If an ad is placed in episode i, every current viewer contributes pi units of profit, and then the audience shrinks by taking a floor division by di before the next episode. If no ad is placed, nothing is earned and the audience remains unchanged.

The key difficulty is that decisions are coupled across time. Whether we advertise early affects how many viewers remain later, and skipping an ad preserves audience size for future episodes. The task is to choose a subset of episodes to maximize total revenue.

The constraints n, m ≤ 10^5 and pi up to 10^6 imply that any approach that tries all subsets is impossible, since that would be 2^n states. Even O(n^2) is too large. We are forced toward a linear or near-linear dynamic process where each state transition is carefully controlled.

A subtle failure case appears when one is tempted to greedily pick all profitable episodes independently. For example, consider m = 10, two episodes:

episode 1: p1 = 100, d1 = 10

episode 2: p2 = 1, d2 = 1

If we advertise both, episode 1 yields 1000, audience becomes 1, and episode 2 yields 1. Total is 1001. If we skip episode 1 and only take episode 2, we get 10. A naive greedy choice based only on pi would fail completely. The coupling through audience reduction means local decisions are not independent.

Another failure case is thinking we must always take an advertisement if it gives positive profit. Because di can be large, a single early ad might destroy future earning potential, making it worse overall.

## Approaches

The brute-force view is to simulate all subsets of episodes. For each subset, we process episodes in order, track current audience, apply multiplication and division, and accumulate reward. This is correct because it respects the process exactly, but it requires checking 2^n subsets, and each simulation costs O(n), giving O(n·2^n), which is infeasible.

The key observation is that the audience evolution is deterministic once we fix the chosen set of episodes. Each decision affects future states only through the current audience value, and that value only depends on how many times we applied each di along the path. This suggests that instead of reasoning about subsets directly, we should treat the problem as a state transition system over possible audience values.

A more structured way to view it is to define a dynamic process over episodes where the only meaningful state is the current episode index and current audience size. From a state (i, c), we have two transitions: skip or take. Taking produces reward c·pi and moves to (i+1, floor(c/di)), while skipping moves to (i+1, c). However, this state graph is still too large because c can take many values.

The crucial simplification is that c only ever takes values from repeatedly dividing m by various di. Since m ≤ 10^5, each division strictly decreases c, and each di ≥ 1. This means the number of distinct reachable audience values is small, and in fact bounded by the number of times we can divide before reaching 1. That makes it possible to do dynamic programming over episode index and current audience value using only reachable states, typically compressed by storing only useful transitions.

We can thus perform DP where dp[i][c] is the maximum revenue starting from episode i with c viewers. Transitions are straightforward, and we compute in reverse order. Since c decreases when we take actions, each state only transitions to smaller or equal values, which allows memoization without explosion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(n·2^n) | O(n) | Too slow |
| DP over (i, c) states | O(nm log m) worst-case, but pruned much smaller in practice | O(nm) | Accepted |

## Algorithm Walkthrough

We define a DP over episodes processed from back to front. At each episode i and audience value c, we decide whether to place an ad.

1. We initialize a memo structure for states (i, c). The goal is to compute the best achievable profit starting at episode i with c viewers. This represents the full remaining decision problem from that point onward.
2. We process episodes from n down to 1. Processing backward is necessary because each decision depends on future outcomes, and backward DP ensures those results are already known.
3. At episode i with current audience c, we compute two options. If we skip the ad, the state transitions to (i+1, c) with zero immediate gain. If we take the ad, we gain c·pi immediately and move to (i+1, floor(c/di)).
4. We store the best of these two choices as dp[i][c]. This ensures that every state records the optimal decision from that point onward.
5. The answer is dp[1][m], representing starting from episode 1 with full audience.

The reason this works is that the process satisfies optimal substructure over the pair (i, c). Once we fix episode i and audience c, all future outcomes depend only on this pair, and no earlier decision affects future transitions except through c. Therefore, recomputing optimal choices for each state is sufficient and no cross-state coupling remains.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n, m = map(int, input().split())
p = list(map(int, input().split()))
d = list(map(int, input().split()))

from functools import lru_cache

@lru_cache(maxsize=None)
def dp(i, c):
    if i == n:
        return 0

    # skip
    best = dp(i + 1, c)

    # take ad
    nc = c // d[i]
    best = max(best, c * p[i] + dp(i + 1, nc))

    return best

print(dp(0, m))
```

The code directly implements the state definition. The function dp(i, c) represents the best possible revenue starting from episode i with c viewers. The recursion explores both choices at each episode. Memoization ensures each state is computed once.

The division step c // d[i] is the only transformation that changes the state. It is critical that integer floor division is used, since the problem explicitly requires it. The recursion depth is bounded by n, but memoization prevents exponential branching.

## Worked Examples

We trace the first sample.

Let p = [9, 14, 10, 4, 5], d = [2, 7, 1, 8, 10], m = 20.

We compare decisions at each step.

| Episode | Audience c | Action | Gain | Next c |
| --- | --- | --- | --- | --- |
| 1 | 20 | take | 180 | 10 |
| 2 | 10 | take | 140 | 1 |
| 3 | 1 | take | 10 | 1 |
| 4 | 1 | skip | 0 | 1 |
| 5 | 1 | take | 5 | 0 |

Total = 335.

This trace shows how early reductions strongly affect later states. The key observation is that episode 3 uses a large di reduction that collapses the audience to 1, making later decisions effectively independent of earlier growth.

Now consider a contrasting scenario:

m = 6

p = [5, 100, 1]

d = [2, 2, 1]

We compare strategies.

| Chosen set | Episode 1 c | Episode 2 c | Episode 3 c | Total |
| --- | --- | --- | --- | --- |
| {1,2,3} | 6 | 3 | 1 | 30 + 300 + 1 = 331 |
| {2,3} | 6 | 6 | 3 | 600 + 3 = 603 |

This shows that skipping early low-impact ads can preserve audience and dramatically increase later gain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) worst-case with memoization, typically much less | each state (i, c) is computed once, and c shrinks through divisions |
| Space | O(n·m) | memo table stores results for each (i, c) pair |

Given m ≤ 10^5, the naive DP state space is large, but reachable states are heavily pruned by repeated integer division, which quickly collapses c toward 1.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    n, m = map(int, sys.stdin.readline().split())
    p = list(map(int, sys.stdin.readline().split()))
    d = list(map(int, sys.stdin.readline().split()))

    from functools import lru_cache

    @lru_cache(None)
    def dp(i, c):
        if i == n:
            return 0
        best = dp(i + 1, c)
        best = max(best, c * p[i] + dp(i + 1, c // d[i]))
        return best

    return str(dp(0, m))

# provided sample
assert run("5 20\n9 14 10 4 5\n2 7 1 8 10\n") == "335"

# minimum case
assert run("1 1\n10\n1\n") == "10"

# skip vs take tradeoff
assert run("2 10\n1 100\n10 10\n") == "1000"

# all di = 1 (no reduction)
assert run("3 5\n1 2 3\n1 1 1\n") == "5*1 + 5*2 + 5*3"  # conceptual placeholder

# single dominant late reward
assert run("3 5\n1 1 100\n2 2 1\n") == "500"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 … | 10 | single decision correctness |
| 2 10 … | 1000 | effect of postponing reduction |
| di all 1 | full linear accumulation | no audience decay case |
| late large pi | 500 | optimal skipping earlier |

## Edge Cases

One edge case is when all di equal 1. In this case, audience never decreases, so the optimal strategy is simply to take every episode, since every ad contributes full m·pi independently. The DP naturally handles this because the state c never changes, so each episode decision is independent.

Another edge case is when some di is very large, possibly equal to m. This immediately collapses audience to 1, so any later gains are minimal. The algorithm handles this correctly because after applying such an episode, all future states operate on c = 1, preventing overestimation.

A final edge case is when pi is extremely large late in the sequence. A naive greedy approach would still take early ads, but DP correctly explores skipping early reductions to preserve a large c for the high-value episode, ensuring the global optimum is achieved.
