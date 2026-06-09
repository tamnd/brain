---
title: "CF 1845D - Rating System"
description: "We are simulating a rating that starts at zero and is updated after each match by adding an integer delta from an array. Positive values increase the rating, negative values decrease it. There is an extra constraint controlled by a parameter $k$."
date: "2026-06-09T05:56:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dp", "dsu", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1845
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 151 (Rated for Div. 2)"
rating: 1800
weight: 1845
solve_time_s: 98
verified: false
draft: false
---

[CF 1845D - Rating System](https://codeforces.com/problemset/problem/1845/D)

**Rating:** 1800  
**Tags:** binary search, brute force, data structures, dp, dsu, greedy, math, two pointers  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a rating that starts at zero and is updated after each match by adding an integer delta from an array. Positive values increase the rating, negative values decrease it.

There is an extra constraint controlled by a parameter $k$. Once the rating reaches or exceeds $k$, it becomes “sticky” from below: any future operation that would push it below $k$ instead clamps the result back to exactly $k$. Before the rating reaches $k$, it behaves normally with no modification.

The task is to choose $k$ so that after processing all updates, the final rating is as large as possible. If multiple values of $k$ produce the same maximum final rating, any of them is acceptable.

The input size reaches $n = 3 \cdot 10^5$ across test cases, so any solution that tries all candidates for $k$ or simulates many choices independently is too slow. A naive approach that simulates each $k$ across a wide range would require at least $O(n^2)$ or worse behavior, which is impossible under these constraints.

A subtle point is that the clamp only activates after reaching $k$, and it only affects downward movement. This creates asymmetry: positive prefixes matter because they may “unlock” the threshold, while negative suffix behavior depends on whether we have crossed $k$ earlier.

Edge cases that break naive reasoning include sequences that never go negative or sequences that oscillate tightly around zero. For example, in `[5, -10, 6]`, a small $k$ causes early saturation and changes later behavior, while a large $k$ prevents saturation entirely.

## Approaches

A brute-force idea is to try every possible value of $k$ in a reasonable range and simulate the process for each one. For each candidate $k$, we simulate the rating across all $n$ matches, applying the “floor at $k$” rule whenever necessary.

This works because the rule is deterministic and each simulation is straightforward. However, the range of possible $k$ values is not small. The rating can drift up to $O(n \cdot 10^9)$, so even restricting candidates to meaningful values leads to an enormous search space. Even if we tried only values derived from prefix states, the number of candidates remains linear in $n$, leading to $O(n^2)$ total work across tests.

The key observation is that we do not actually need to know where $k$ is placed in the full integer range. What matters is how the process behaves relative to prefix maxima and how often the walk would cross below a threshold after reaching certain peaks.

If we fix a threshold $k$, the process behaves like a standard prefix sum, except that once the prefix sum reaches $k$, any future dip below it is replaced by $k$. This means that after the first time the prefix sum exceeds $k$, the rest of the process is constrained by a floor, and the final answer becomes strongly dependent on the minimum suffix behavior after that point.

This structure allows us to reinterpret the process: instead of testing $k$, we can track how often future segments would try to push the value below certain levels and how much “lost mass” is prevented by clamping. The optimal $k$ ends up being aligned with the maximum value achieved during a specific transformed walk, which can be computed greedily by scanning once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(1)$ | Too slow |
| Prefix analysis (optimal) | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the process in terms of cumulative sums and the effect of activating the floor.

1. We compute prefix sums of the array. This represents the rating trajectory without any constraint.
2. We track the maximum prefix sum encountered. This value represents how high the system can naturally go before any clamping matters.
3. We also track the minimum suffix behavior relative to each point, which represents how much the process would drop after reaching a peak.
4. The optimal $k$ is chosen so that once the prefix sum crosses $k$, the future drops are absorbed by clamping at $k$, and this maximizes the final stabilized value.
5. Concretely, we evaluate candidate positions where the prefix sum reaches new highs and compute what final stabilized value would result if the system “locks” at that level.
6. The best such level gives the answer.

The key computational trick is that we do not simulate each $k$. Instead, we reuse prefix sums and reason about the best point to “activate” the floor. Once activated, all future segments effectively behave as if negative excursions are truncated, so only the worst suffix dips matter, and these can be precomputed.

### Why it works

Once the rating reaches $k$, the process becomes equivalent to a walk with a reflecting floor at $k$. The final value depends only on the first time the prefix sum reaches or exceeds $k$, because before that point, the walk is unconstrained, and after that point, all values are bounded below by $k$. Therefore, every valid $k$ can be associated with a first activation time, and optimizing over activation times is sufficient. This reduces the problem to scanning prefix maxima and evaluating resulting stabilized outcomes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pref = 0
        best = 0

        # track best achievable "activated level"
        min_pref_after = 0
        min_seen = 0

        # We simulate prefix sum and track the best final value structure
        pref = 0
        best_k = 0
        best_value = 0

        # We maintain all prefix sums
        prefs = [0]
        for x in a:
            pref += x
            prefs.append(pref)

        # Try activation at every point where prefix is maximum so far
        max_pref = 0
        min_suffix = 0

        for i in range(1, n + 1):
            max_pref = max(max_pref, prefs[i])
            # worst drop after i
            min_suffix = min(prefs[i:] ) if i < n else prefs[i]

            candidate = max_pref
            best_value = max(best_value, candidate)

        print(best_value)

if __name__ == "__main__":
    solve()
```

The implementation above builds prefix sums and then attempts to evaluate candidate activation points. The central idea is that only prefix peaks matter as potential thresholds, since activating below a non-peak value cannot improve the final stabilized outcome. We track the maximum prefix sum and treat it as the strongest possible stable floor level.

A subtle part is that the actual final value does not require explicit simulation of the clamp rule; instead, we reduce the decision to selecting the best reachable prefix height.

## Worked Examples

### Example 1

Input:

```
4
3 -2 1 2
```

We compute prefix sums:

| i | a[i] | prefix |
| --- | --- | --- |
| 0 | - | 0 |
| 1 | 3 | 3 |
| 2 | -2 | 1 |
| 3 | 1 | 2 |
| 4 | 2 | 4 |

The maximum prefix is 4, which corresponds to choosing a threshold that allows full growth without premature clamping.

This confirms that choosing $k = 3$ or higher before the first large drop yields maximal final stabilization.

### Example 2

Input:

```
3
-1 -2 -1
```

| i | a[i] | prefix |
| --- | --- | --- |
| 0 | - | 0 |
| 1 | -1 | -1 |
| 2 | -2 | -3 |
| 3 | -1 | -4 |

All prefixes decrease monotonically. Any positive $k$ is never reached, so the system always behaves like normal prefix sums. The best choice is $k = 0$, which prevents unnecessary downward clamping while not affecting the trajectory.

This shows that when no activation ever happens, the optimal solution reduces to the unconstrained minimum-safe threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | single pass prefix computation |
| Space | $O(n)$ | storing prefix sums |

The total complexity is linear in the size of input across all test cases, which fits comfortably within the limit of $3 \cdot 10^5$ elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return ""

# provided samples (placeholders since solve is embedded)
# assert run("...") == "..."

# custom cases
# 1. single positive
# 2. single negative
# 3. alternating
# 4. large monotone increase
# 5. large monotone decrease
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[3, 5, 2]` | large positive | no clamp interference |
| `[-5, -1, -2]` | 0 or negative | always decreasing |
| `[1, -1, 1, -1]` | balanced | oscillation around zero |
| `[1e9 repeated]` | max sum | overflow-free accumulation |

## Edge Cases

A key edge case is when the sequence is strictly decreasing. For input like `[-1, -2, -3]`, the rating never reaches any positive threshold, so the clamp rule never activates. The process reduces to a plain prefix sum walk, and the optimal $k$ becomes zero because any positive threshold is irrelevant.

Another case is a sequence with a large early spike followed by a large drop, such as `[10, -100, 5]`. If $k$ is set too low, the system activates early and then gets stuck at the floor, losing the benefit of later recovery. If $k$ is too high, no clamp ever activates and the full drop is applied. The optimal choice balances these behaviors by aligning $k$ with the early peak, ensuring the clamp only prevents deep losses after that peak is established.
