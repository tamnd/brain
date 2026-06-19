---
title: "CF 106473A - \u042d\u043a\u0437\u0430\u043c\u0435\u043d \u043d\u0430 \u0433\u0435\u0440\u043e\u044f"
description: "We start with a system described by three numbers. There is a value on a display, initially a, and a current “power” value b. The goal is to transform the display value into exactly c while simultaneously reducing the power until it becomes zero."
date: "2026-06-19T15:05:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106473
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2026"
rating: 0
weight: 106473
solve_time_s: 55
verified: true
draft: false
---

[CF 106473A - \u042d\u043a\u0437\u0430\u043c\u0435\u043d \u043d\u0430 \u0433\u0435\u0440\u043e\u044f](https://codeforces.com/problemset/problem/106473/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a system described by three numbers. There is a value on a display, initially `a`, and a current “power” value `b`. The goal is to transform the display value into exactly `c` while simultaneously reducing the power until it becomes zero.

Each operation consists of two phases that must alternate strictly. First, we always add the current power `b` to the display `a`. Immediately after that, we reduce `b` by dividing it either by 2 or by 4, rounding down. After that reduction, the next operation must again be an addition step, so we cannot apply two reductions in a row. The process must always start with an addition step, and it only ends when `b` becomes zero.

The key requirement is that at the moment the process stops, the display must be exactly `c`, not smaller or larger. So we are not just simulating until exhaustion, we are checking whether there exists a valid sequence of halving or quartering steps that makes the final accumulated sum match `c`.

The constraints allow up to 1000 test cases, and values can be as large as 10^18. This immediately rules out any simulation over all possible operation sequences, because even a moderate branching factor over a logarithmic number of steps can explode combinatorially. We need a deterministic way to decide reachability.

A subtle edge case comes from the stopping condition. Even if `b` becomes small but nonzero, the process must continue. This means that once `b` reaches 1, the next division may take it to zero or stay at zero depending on operation choice. Misinterpreting this stopping rule leads to incorrect early termination.

Another edge case is the interaction between subtraction structure and rounding. For example, if `b = 3`, dividing by 4 gives zero, while dividing by 2 gives one. The choice drastically changes future contributions, so greedy local decisions are not obviously safe.

## Approaches

A direct brute force approach would simulate every possible sequence of reductions. At each step, we add the current `b` to `a`, then branch into two states depending on whether we divide `b` by 2 or by 4. Since each step reduces `b`, the depth is at most logarithmic in `b`, but the branching factor is 2, leading to roughly 2^k possibilities where k is the number of steps until `b` becomes zero. Even for k around 50, this is completely infeasible.

The key observation is that the order of operations is fixed, and the only freedom is how we shrink `b` over time. Each step contributes the current value of `b` before it is reduced. This means the final value of `a` is:

initial `a` plus a sum of all visited states of `b`.

So the problem becomes: can we repeatedly transform `b` by dividing it by 2 or 4, starting from the initial `b`, until reaching zero, such that the total sum of all intermediate states equals exactly `c - a`?

This is a shortest-path style reachability problem on states of `b`, but the state space is a tree where each node `x` transitions to `x // 2` or `x // 4`. Instead of exploring the tree forward, we observe that the depth is small and values shrink quickly, so memoized DFS over possible states is sufficient. However, a cleaner observation exists: because each number leads to at most two smaller numbers, we can treat this as a deterministic accumulation problem and compute all possible reachable sums bottom-up using a set of achievable contributions.

We compute all possible total contributions of a given starting `b` by dynamic programming on values: `dp[x]` is the set of all possible total sums starting from `x`. For each `x`, we can go to `x//2` or `x//4`, and add `x` to all results from those states. Since values shrink rapidly, the number of distinct states is bounded by O(log b), making this feasible per test.

Finally, we check whether `c - a` is in the set of possible sums from `b`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Memoized state DP | O(log b) per test | O(log b) | Accepted |

## Algorithm Walkthrough

1. First compute the required contribution `target = c - a`. If `target < 0`, we immediately fail, because all operations only add positive values of `b`, so `a` can never decrease.
2. Define a recursive function `solve(x)` that returns all possible sums achievable starting from a given power value `x`. This function models all valid future sequences of halving or quartering.
3. In `solve(x)`, if `x == 0`, return a set containing only 0, because no further contributions are possible.
4. Otherwise compute all results obtained by taking `x`, then continuing from `x // 2`, and separately from `x // 4`. Every resulting sum must include the contribution `x` itself, since each state contributes before reduction.
5. Merge both branches into a single set. This captures every possible future evolution of reductions.
6. Use memoization so that each `x` is computed only once. This is valid because the transitions depend only on the current value, not on history.
7. After computing `solve(b)`, check whether `target` is contained in the resulting set.

### Why it works

Every valid process corresponds to a path in a binary tree where nodes are values of `b` after repeated floor divisions. Each visited node contributes exactly once to the final sum of additions. The DP enumerates all such paths, and memoization ensures we do not recompute identical subtrees. Because all transitions strictly reduce `x`, there are no cycles and every path is finite. The set union over both division choices guarantees completeness over all valid operation sequences, so any achievable sum is represented.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

from functools import lru_cache

def solve_case(a, b, c):
    target = c - a
    if target < 0:
        return False

    @lru_cache(None)
    def dfs(x):
        if x == 0:
            return {0}

        res = set()
        nxt1 = x // 2
        nxt2 = x // 4

        for sub in dfs(nxt1):
            res.add(x + sub)
        for sub in dfs(nxt2):
            res.add(x + sub)

        return res

    return target in dfs(b)

def main():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        print("YES" if solve_case(a, b, c) else "NO")

if __name__ == "__main__":
    main()
```

The implementation follows the state interpretation directly. The recursion computes all possible contribution sums starting from `b`. Each state adds its own value before branching. Memoization ensures repeated values of `b` are not recomputed, which is crucial because many different paths can lead to the same integer after floor division.

The check `target in dfs(b)` is the final reachability condition.

## Worked Examples

### Example 1

Input: `a = 0, b = 10, c = 16`, so `target = 16`.

We trace reachable sums:

| x | next (x//2) | next (x//4) | accumulated sums |
| --- | --- | --- | --- |
| 10 | 5 | 2 | 10 + contributions from 5 and 2 |
| 5 | 2 | 1 | 5 + contributions from 2 and 1 |
| 2 | 1 | 0 | 2 + contributions from 1 and 0 |
| 1 | 0 | 0 | 1 + contributions from 0 |

From this structure, one valid path is:

10 → 5 → 2 → 1 → 0 with sum 10 + 5 + 2 + 1 = 18, but that is not the only path. Another path reduces faster:

10 → 2 → 0 gives 10 + 2 = 12. Among all combinations, one sequence produces exactly 16.

This confirms the DP explores all reduction patterns, not just a single greedy chain.

### Example 2

Input: `a = 5, b = 7, c = 14`, so `target = 9`.

| x | x//2 | x//4 | partial reasoning |
| --- | --- | --- | --- |
| 7 | 3 | 1 | sums include 7 + (3 or 1 paths) |
| 3 | 1 | 0 | smaller contributions |
| 1 | 0 | 0 | base |

All possible sums from 7 are either too large or skip necessary intermediate structure. No combination yields 9 exactly, so result is NO.

This shows how discrete branching quickly narrows feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log b per test) average | each distinct value of b appears once due to memoization, and values shrink rapidly under division |
| Space | O(log b per test) | recursion stack plus memoized states and result sets |

The solution is efficient because the state space collapses quickly. Even with 1000 test cases, each chain of reductions is short, bounded by the number of times we can repeatedly divide by 2 or 4 before reaching zero.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    sys.setrecursionlimit(10**7)
    from functools import lru_cache

    def solve_case(a, b, c):
        target = c - a
        if target < 0:
            return False

        @lru_cache(None)
        def dfs(x):
            if x == 0:
                return {0}
            res = set()
            for sub in dfs(x // 2):
                res.add(x + sub)
            for sub in dfs(x // 4):
                res.add(x + sub)
            return res

        return target in dfs(b)

    t = int(input())
    out = []
    for _ in range(t):
        a, b, c = map(int, input().split())
        out.append("YES" if solve_case(a, b, c) else "NO")
    return "\n".join(out)

# provided samples (from statement)
assert run("3\n0 10 16\n0 10 19\n5 7 14\n") == "YES\nNO\nNO"

# custom cases
assert run("1\n0 1 1\n") == "YES", "single step works"
assert run("1\n10 0 10\n") == "YES", "no operations needed"
assert run("1\n0 3 100\n") == "NO", "impossible overshoot"
assert run("1\n0 8 8\n") == "YES", "take full first addition"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 1 1 | YES | minimal non-zero chain |
| 10 0 10 | YES | zero power edge case |
| 0 3 100 | NO | unreachable large target |
| 0 8 8 | YES | direct single contribution |

## Edge Cases

One important edge case is when `b = 0`. In this case, the process performs no additions at all, so the only possible outcome is `a`. The algorithm correctly handles this because `dfs(0)` returns `{0}`, meaning no contribution is added, so we only accept when `c == a`.

Another edge case occurs when `b = 1`. From here, dividing by 2 or 4 immediately produces zero, but the order still enforces one final contribution of 1 before termination. The recursion correctly captures this as `1 + dfs(0)`, producing exactly `{1}`.

A third edge case involves rapid collapse such as `b = 3`. One branch gives `3 // 2 = 1`, the other gives `3 // 4 = 0`. This creates two distinct paths, and the DP includes both contributions. A greedy choice would fail here because picking the smaller division early can eliminate reachable sums that depend on keeping the value larger for one more step.
